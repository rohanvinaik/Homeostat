"""§8.4 / §10.2 — selection-signature enrichment ON THE E/I/R PBS PILE.

The primary, legitimate validator (§10.2): is the top of the population-
differential PBS pile enriched for within-population selection signal (PopHuman
SAS iHS) beyond a MAF-MATCHED background? Annotation-blind throughout — uses no
gene annotation (§8.4), so it does not circle back through the held-out layer.

Runs on the §7 PBS pile (`eir_cohort`), NEVER on a p-value-selected set (Law 3).
MAF-matched because iHS and F_ST both track allele frequency — the §13.4
degree-confound lesson transported to frequency. Streams the pile once
(bounded memory): a size-K max-pile by PBS + a per-MAF-bin reservoir for controls.

Run: make eir-enrich. Idempotent.
"""

import datetime
import gzip
import heapq
import json
import random
import statistics
import sys

from homeostat import paths
from homeostat.eir_cohort import PILE
from homeostat.enrich import SAS_POPS, Track, mean_stat
from homeostat.util import atomic_write_json

TOP_K = 50000  # the bounded-d candidate set (§7): top of the PBS ranking
MAF_BIN_WIDTH = 0.025  # fixed-width MAF bins for matching (deterministic)
RESERVOIR_PER_BIN = 40000
N_PERM = 2000
MIN_POPS = 3
SEED = 20260829
OUT = paths.EIR / "eir_selection_enrichment.json"


def maf_bin(maf: float) -> int:
    return min(int(maf / MAF_BIN_WIDTH), int(0.5 / MAF_BIN_WIDTH) - 1)


def scan_pile(path) -> tuple[list[tuple[str, int, int]], dict[int, list[tuple[str, int]]]]:
    """One streaming pass: the top-K-by-PBS pile and a per-MAF-bin reservoir.

    Returns (pile, reservoir): pile = [(chrom, pos, maf_bin)] for the top-K PBS
    variants; reservoir[bin] = sampled [(chrom, pos)] for MAF-matched controls.
    Deterministic reservoir (Algorithm R, seeded).
    """
    rng = random.Random(SEED)
    heap: list[tuple[float, str, int, int]] = []  # (pbs, chrom, pos, maf_bin) min-heap
    reservoir: dict[int, list[tuple[str, int]]] = {}
    seen: dict[int, int] = {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        next(f)  # header
        for line in f:
            fld = line.rstrip("\n").split("\t")
            chrom, pos = fld[0], int(fld[1])
            maf, pbs_v = float(fld[7]), float(fld[9])
            b = maf_bin(maf)
            if len(heap) < TOP_K:
                heapq.heappush(heap, (pbs_v, chrom, pos, b))
            elif pbs_v > heap[0][0]:
                heapq.heapreplace(heap, (pbs_v, chrom, pos, b))
            # Algorithm-R reservoir per MAF bin
            seen[b] = seen.get(b, 0) + 1
            bucket = reservoir.setdefault(b, [])
            if len(bucket) < RESERVOIR_PER_BIN:
                bucket.append((chrom, pos))
            else:
                j = rng.randrange(seen[b])
                if j < RESERVOIR_PER_BIN:
                    bucket[j] = (chrom, pos)
    pile = [(c, p, b) for _pbs, c, p, b in heap]
    return pile, reservoir


def main() -> None:
    if OUT.exists():
        print(f"[eir-enrich] already complete ({OUT}); delete to re-run")
        return
    if not PILE.exists():
        sys.exit(f"[eir-enrich] pile missing: {PILE} — run `make eir-pile` first")

    print("[eir-enrich] scanning pile (top-K + MAF reservoir) ...")
    pile, reservoir = scan_pile(PILE)
    print(f"[eir-enrich] pile {len(pile)} variants; loading iHS tracks ...")
    tracks = [Track(p) for p in SAS_POPS]

    def ihs(chrom: str, pos: int) -> float | None:
        return mean_stat(tracks, chrom, pos, MIN_POPS)

    pile_set = {(c, p) for c, p, _b in pile}
    pile_ihs = [v for c, p, _b in pile if (v := ihs(c, p)) is not None]
    observed = statistics.fmean(pile_ihs) if pile_ihs else 0.0

    # MAF-matched control draws: same per-bin counts as the pile, from the
    # reservoir minus the pile itself.
    need: dict[int, int] = {}
    for _c, _p, b in pile:
        need[b] = need.get(b, 0) + 1
    control_pools = {
        b: [(c, p) for (c, p) in reservoir.get(b, []) if (c, p) not in pile_set] for b in need
    }
    missing = [b for b, k in need.items() if len(control_pools[b]) < k]

    rng = random.Random(SEED + 1)
    ge = 0
    n_used = 0
    for _ in range(N_PERM):
        vals = []
        for b, k in need.items():
            pool = control_pools[b]
            if not pool:
                continue
            for c, p in rng.sample(pool, min(k, len(pool))):
                v = ihs(c, p)
                if v is not None:
                    vals.append(v)
        if vals:
            n_used += 1
            if statistics.fmean(vals) >= observed:
                ge += 1
    p_val = (1 + ge) / (1 + n_used) if n_used else 1.0

    result = {
        "stage": "§8.4 selection-signature enrichment on the E/I/R PBS pile",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "validator": "PopHuman SAS iHS, MAF-matched permutation. Annotation-blind (§8.4). "
        "On the PBS pile, not a p-value set (Law 3).",
        "dials": {
            "top_k": TOP_K,
            "maf_bin_width": MAF_BIN_WIDTH,
            "n_perm": N_PERM,
            "min_pops": MIN_POPS,
            "seed": SEED,
        },
        "pile_variants": len(pile),
        "pile_with_ihs": len(pile_ihs),
        "pile_mean_ihs": round(observed, 5),
        "maf_matched_permutation_p": round(p_val, 5),
        "control_bins_underfilled": missing,
        "passes_p05": p_val < 0.05,
    }
    atomic_write_json(OUT, result)
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "pile_variants",
                    "pile_with_ihs",
                    "pile_mean_ihs",
                    "maf_matched_permutation_p",
                    "passes_p05",
                )
            },
            indent=2,
        )
    )
    print(f"[eir-enrich] complete -> {OUT}")


if __name__ == "__main__":
    main()
