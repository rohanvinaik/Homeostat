"""§8.4 robustness — selection enrichment on the PBS pile, LD-BLOCK corrected.

The passed §8.4 (`eir_enrich`, p=0.0005) permuted per-variant; the 50k pile
variants are in LD, so that overstates confidence. This makes the **1Mb window the
exchangeable unit** (block bootstrap) so the effective n reflects LD (~1,579
blocks, not 50k variants) — NOT clumping to lead SNPs (forbidden, Law 2).

Criterion FROZEN in docs/runs/2026-08-30-eir-enrich-ldblock-PREREGISTRATION.md
(committed e1b02a2, before this file). Run: make eir-enrich-block.
"""

import datetime
import gzip
import heapq
import random
import statistics
import sys
from dataclasses import dataclass, field

from homeostat import paths
from homeostat.eir_cohort import PILE
from homeostat.eir_enrich import MIN_POPS, TOP_K, maf_bin
from homeostat.enrich import SAS_POPS, Track, mean_stat
from homeostat.util import atomic_write_json

BLOCK_BP = 1_000_000
RES_PER_BLOCK = 100  # sampled positions per block for control-block iHS estimate
N_PERM = 2000
SEED = 20_260_830
OUT = paths.EIR / "eir_selection_enrichment_ldblock.json"


@dataclass
class _BlockAcc:
    """Per-1Mb-block accumulator: variant count, MAF sum, bounded position sample."""

    n: int = 0
    maf_sum: float = 0.0
    res: list[int] = field(default_factory=list)


def scan_blocks(path):
    """One streaming pass: the top-K-by-PBS pile plus a per-1Mb-block accumulator
    (variant count, MAF sum, and a bounded reservoir of positions) for EVERY
    block genome-wide (~3,100 blocks — small, so all are tracked).
    """
    rng = random.Random(SEED)
    heap: list[tuple[float, str, int, float]] = []  # (pbs, chrom, pos, maf)
    blocks: dict[tuple[str, int], _BlockAcc] = {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        next(f)
        for line in f:
            fld = line.rstrip("\n").split("\t")
            chrom, pos = fld[0], int(fld[1])
            maf, pbs_v = float(fld[7]), float(fld[9])
            if len(heap) < TOP_K:
                heapq.heappush(heap, (pbs_v, chrom, pos, maf))
            elif pbs_v > heap[0][0]:
                heapq.heapreplace(heap, (pbs_v, chrom, pos, maf))
            key = (chrom, pos // BLOCK_BP)
            b = blocks.get(key)
            if b is None:
                b = _BlockAcc()
                blocks[key] = b
            b.n += 1
            b.maf_sum += maf
            if len(b.res) < RES_PER_BLOCK:
                b.res.append(pos)
            else:
                j = rng.randrange(b.n)
                if j < RES_PER_BLOCK:
                    b.res[j] = pos
    pile = [(c, p, m) for _pbs, c, p, m in heap]
    return pile, blocks


def maf_matched_block_perm(
    need: dict[int, int],
    control_by_bin: dict[int, list[float]],
    observed: float,
    n_perm: int,
    rng: random.Random,
) -> tuple[float, int, list[int]]:
    """MAF-bin-matched permutation at BLOCK level: each draw samples `need[bin]`
    control blocks per MAF bin, statistic = mean of drawn block-mean-iHS. Returns
    (add-one p, n_used, underfilled_bins). Pure — testable without bigwigs.
    """
    underfilled = [b for b, k in need.items() if len(control_by_bin.get(b, [])) < k]
    ge = 0
    n_used = 0
    for _ in range(n_perm):
        vals: list[float] = []
        for b, k in need.items():
            pool = control_by_bin.get(b, [])
            if pool:
                vals.extend(rng.sample(pool, min(k, len(pool))))
        if vals:
            n_used += 1
            if statistics.fmean(vals) >= observed:
                ge += 1
    p = (1 + ge) / (1 + n_used) if n_used else 1.0
    return p, n_used, underfilled


def main() -> None:
    if OUT.exists():
        print(f"[eir-block] already complete ({OUT}); delete to re-run")
        return
    if not PILE.exists():
        sys.exit(f"[eir-block] pile missing: {PILE} — run `make eir-pile` first")

    print("[eir-block] scanning pile + per-block accumulators ...")
    pile, blocks = scan_blocks(PILE)
    tracks = [Track(p) for p in SAS_POPS]

    def ihs(chrom: str, pos: int) -> float | None:
        return mean_stat(tracks, chrom, pos, MIN_POPS)

    def block_mean_ihs(chrom: str, positions: list[int]) -> float | None:
        vals = [v for pos in positions if (v := ihs(chrom, pos)) is not None]
        return statistics.fmean(vals) if vals else None

    # pile blocks: mean-iHS over ALL pile variants in the window; MAF bin from
    # their mean MAF.
    pile_by_block: dict[tuple[str, int], list[tuple[int, float]]] = {}
    for c, p, m in pile:
        pile_by_block.setdefault((c, p // BLOCK_BP), []).append((p, m))

    print(f"[eir-block] {len(pile_by_block)} pile blocks; computing block iHS ...")
    pile_blocks: list[tuple[int, float]] = []
    for (chrom, _w), variants in pile_by_block.items():
        mi = block_mean_ihs(chrom, [pos for pos, _ in variants])
        if mi is None:
            continue
        mean_maf = sum(mm for _, mm in variants) / len(variants)
        pile_blocks.append((maf_bin(mean_maf), mi))
    observed = statistics.fmean([mi for _, mi in pile_blocks]) if pile_blocks else 0.0

    # control blocks: every block with no pile variant, iHS from its reservoir.
    pile_keys = set(pile_by_block)
    control_by_bin: dict[int, list[float]] = {}
    n_control = 0
    for key, b in blocks.items():
        if key in pile_keys or b.n == 0:
            continue
        mi = block_mean_ihs(key[0], b.res)
        if mi is None:
            continue
        control_by_bin.setdefault(maf_bin(b.maf_sum / b.n), []).append(mi)
        n_control += 1

    need: dict[int, int] = {}
    for bin_, _mi in pile_blocks:
        need[bin_] = need.get(bin_, 0) + 1

    print(f"[eir-block] permuting ({N_PERM}) over {n_control} control blocks ...")
    p_val, n_used, underfilled = maf_matched_block_perm(
        need, control_by_bin, observed, N_PERM, random.Random(SEED + 1)
    )

    result = {
        "stage": "§8.4 selection enrichment on the PBS pile — LD-block corrected",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "preregistration": "docs/runs/2026-08-30-eir-enrich-ldblock-PREREGISTRATION.md (e1b02a2)",
        "unit": "1Mb window (block bootstrap; NOT lead-SNP clumping)",
        "dials": {
            "block_bp": BLOCK_BP,
            "top_k": TOP_K,
            "res_per_block": RES_PER_BLOCK,
            "n_perm": N_PERM,
            "min_pops": MIN_POPS,
            "seed": SEED,
        },
        "pile_blocks_with_ihs": len(pile_blocks),
        "control_blocks_with_ihs": n_control,
        "observed_block_mean_ihs": round(observed, 5),
        "block_matched_permutation_p": round(p_val, 5),
        "control_bins_underfilled": underfilled,
        "passes_p05": p_val < 0.05,
        "note": "Block p is less extreme than the per-variant 0.0005 BY CONSTRUCTION "
        "(~1.6k blocks vs 50k variants); survival below 0.05 is the robust result.",
    }
    atomic_write_json(OUT, result)
    print(
        f"[eir-block] observed {observed:.4f} over {len(pile_blocks)} pile blocks; "
        f"block-matched p={p_val:.5f} (passes={p_val < 0.05})"
    )
    print(f"[eir-block] complete -> {OUT}")


if __name__ == "__main__":
    main()
