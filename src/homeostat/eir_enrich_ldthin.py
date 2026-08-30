"""§8.4 robustness — LD-THINNED selection-enrichment re-test.

Replaces the miscalibrated block-collapsing test (its control pool was starved
because the pile spans >half the genome's 1Mb windows). Here we THIN the PILE to
one random variant per 1Mb window (~independent) and run the ORIGINAL per-variant
MAF-matched permutation against the FULL, undepleted reservoir — so effective n
reflects LD without depleting controls. Random representative (not max-PBS) → no
lead-SNP selection (Law-2-clean; thinning is variance calibration, the object is
still the full pile).

Criterion FROZEN in docs/runs/2026-08-30-eir-enrich-ldthin-PREREGISTRATION.md
(committed 8a72ade). Run: make eir-enrich-thin.
"""

import datetime
import random
import statistics
import sys

from homeostat import paths
from homeostat.eir_cohort import PILE
from homeostat.eir_enrich import MIN_POPS, TOP_K, scan_pile
from homeostat.enrich import SAS_POPS, Track, mean_stat
from homeostat.util import atomic_write_json

BLOCK_BP = 1_000_000
N_PERM = 2000
SEED = 20_260_830
OUT = paths.EIR / "eir_selection_enrichment_ldthin.json"


def thin_pile(pile: list[tuple[str, int, int]], rng: random.Random) -> list[tuple[str, int, int]]:
    """One random variant per 1Mb window (approx. independent representatives).
    Windows iterated in sorted order so the seeded pick is deterministic."""
    by_win: dict[tuple[str, int], list[tuple[str, int, int]]] = {}
    for c, p, b in pile:
        by_win.setdefault((c, p // BLOCK_BP), []).append((c, p, b))
    return [rng.choice(by_win[w]) for w in sorted(by_win)]


def maf_matched_perm(
    need: dict[int, int],
    control_ihs: dict[int, list[float]],
    observed: float,
    n_perm: int,
    rng: random.Random,
) -> tuple[float, int]:
    """MAF-bin-matched per-variant permutation. Returns (add-one p, n_used).
    Pure — testable without bigwigs."""
    ge = 0
    n_used = 0
    for _ in range(n_perm):
        vals: list[float] = []
        for b, k in need.items():
            pool = control_ihs.get(b, [])
            if pool:
                vals.extend(rng.sample(pool, min(k, len(pool))))
        if vals:
            n_used += 1
            if statistics.fmean(vals) >= observed:
                ge += 1
    return ((1 + ge) / (1 + n_used) if n_used else 1.0), n_used


def main() -> None:
    if OUT.exists():
        print(f"[eir-thin] already complete ({OUT}); delete to re-run")
        return
    if not PILE.exists():
        sys.exit(f"[eir-thin] pile missing: {PILE} — run `make eir-pile` first")

    print("[eir-thin] scanning pile (top-K + MAF reservoir) ...")
    pile, reservoir = scan_pile(PILE)
    thinned = thin_pile(pile, random.Random(SEED))
    print(f"[eir-thin] thinned {len(pile)} pile variants -> {len(thinned)} (1 per 1Mb window)")

    tracks = [Track(p) for p in SAS_POPS]

    def ihs(chrom: str, pos: int) -> float | None:
        return mean_stat(tracks, chrom, pos, MIN_POPS)

    full_pile_set = {(c, p) for c, p, _b in pile}  # controls exclude the WHOLE pile
    thin_ihs = [v for c, p, _b in thinned if (v := ihs(c, p)) is not None]
    observed = statistics.fmean(thin_ihs) if thin_ihs else 0.0

    # per-MAF-bin control iHS, precomputed once (permute over cached floats).
    need: dict[int, int] = {}
    for _c, _p, b in thinned:
        need[b] = need.get(b, 0) + 1
    control_ihs: dict[int, list[float]] = {}
    for b in need:
        vals = []
        for c, p in reservoir.get(b, []):
            if (c, p) in full_pile_set:
                continue
            v = ihs(c, p)
            if v is not None:
                vals.append(v)
        control_ihs[b] = vals
    underfilled = [b for b, k in need.items() if len(control_ihs[b]) < k]

    print(f"[eir-thin] permuting ({N_PERM}) ...")
    p_val, n_used = maf_matched_perm(need, control_ihs, observed, N_PERM, random.Random(SEED + 1))

    result = {
        "stage": "§8.4 selection enrichment on the PBS pile — LD-thinned",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "preregistration": "docs/runs/2026-08-30-eir-enrich-ldthin-PREREGISTRATION.md (8a72ade)",
        "unit": "1 random variant per 1Mb window (LD decorrelation; NOT lead-SNP clumping)",
        "dials": {
            "block_bp": BLOCK_BP,
            "top_k": TOP_K,
            "n_perm": N_PERM,
            "min_pops": MIN_POPS,
            "seed": SEED,
        },
        "thinned_variants": len(thinned),
        "thinned_with_ihs": len(thin_ihs),
        "observed_mean_ihs": round(observed, 5),
        "ldthin_permutation_p": round(p_val, 5),
        "control_bins_underfilled": underfilled,
        "n_used_perms": n_used,
        "passes_p05": p_val < 0.05,
    }
    atomic_write_json(OUT, result)
    print(
        f"[eir-thin] observed {observed:.4f} over {len(thin_ihs)} thinned variants; "
        f"LD-thinned p={p_val:.5f} (passes={p_val < 0.05})"
    )
    print(f"[eir-thin] complete -> {OUT}")


if __name__ == "__main__":
    main()
