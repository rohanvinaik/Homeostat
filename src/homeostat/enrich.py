"""§13.2 — selection-signature enrichment of the E/I/R pile. Annotation-blind.

Test: are the top E/I/R loci (LD-collapsed) enriched for within-population
haplotype selection signal (PopHuman iHS, 10kb windows) relative to
AF-matched control sites drawn from the same array-matched pool?

Design points, all recorded in the output:
- iHS is haplotype/within-population — causally independent of the between-
  population AF divergence (PBS) that built the pile (checkpoint §10.1).
- Windows with no iHS data are ABSTENTIONS, never zeros; sites without
  sufficient population coverage are excluded symmetrically from pile and pool.
- Empirical permutation p with add-one correction; seeded, deterministic.
- Known simplification: control draws are per-site AF-matched without
  within-set spacing constraints (negligible at pool size ~590k).

Run: make enrich. Idempotent: skips if the output exists.
"""

import bisect
import datetime
import gzip
import json
import random
import statistics
import sys

from homeostat import paths
from homeostat.bigwig import BigWig
from homeostat.collapse import collapse
from homeostat.util import atomic_write_json

# The dials, as typed constants (used in code) mirrored into DIALS (the record
# written to the output so every run carries its assumptions).
WINDOW_BP = 500_000
TOP_K_LOCI = 1000
AF_BIN_WIDTH = 0.05
MIN_POPS_WITH_DATA = 3
N_CONTROL_SETS = 2000
SEED = 20260828
EXCLUDE_BP_AROUND_PILE = 500_000
SAS_POPS = ["BEB", "GIH", "ITU", "PJL", "STU"]
EUR_POPS = ["CEU", "GBR"]

DIALS = {
    "window_bp": WINDOW_BP,
    "top_k_loci": TOP_K_LOCI,
    "af_bin_width": AF_BIN_WIDTH,
    "min_pops_with_data": MIN_POPS_WITH_DATA,
    "n_control_sets": N_CONTROL_SETS,
    "seed": SEED,
    "exclude_bp_around_pile": EXCLUDE_BP_AROUND_PILE,
    "sas_pops": SAS_POPS,
    "eur_pops": EUR_POPS,
    "stat": "mean per-population iHS (10kb window containing the site)",
}

ENRICHMENT = paths.EIR / "enrichment.json"
LOCI = paths.EIR / "loci.tsv.gz"


class Track:
    """One population's iHS windows, preloaded to per-chrom sorted arrays."""

    def __init__(self, pop: str):
        path = paths.DATA / "selection_scans" / f"iHS_{pop}_10kb.bw"
        self.by_chrom: dict[str, tuple[list[int], list[int], list[float]]] = {}
        with BigWig(str(path)) as bw:
            bw.self_check()
            for name, (_cid, size) in bw.chroms.items():
                ivs = bw.query(name, 0, size)
                chrom = name.removeprefix("chr")
                self.by_chrom[chrom] = (
                    [iv.start for iv in ivs],
                    [iv.end for iv in ivs],
                    [iv.value for iv in ivs],
                )

    def value_at(self, chrom: str, pos: int) -> float | None:
        entry = self.by_chrom.get(chrom)
        if entry is None:
            return None
        starts, ends, vals = entry
        i = bisect.bisect_right(starts, pos) - 1
        if i >= 0 and pos < ends[i]:
            return vals[i]
        return None


def mean_stat(tracks: list[Track], chrom: str, pos: int, min_pops: int) -> float | None:
    """Mean iHS across populations at a site; None (abstain) below min_pops."""
    vals = [v for t in tracks if (v := t.value_at(chrom, pos)) is not None]
    if len(vals) < min_pops:
        return None
    return statistics.fmean(vals)


def empirical_p(pile_value: float, control_values: list[float]) -> float:
    """One-sided add-one permutation p: P(control >= pile)."""
    ge = sum(1 for c in control_values if c >= pile_value)
    return (1 + ge) / (1 + len(control_values))


def af_bin(af: float, width: float) -> int:
    return min(int(af / width), int(1 / width) - 1)


def load_candidates() -> list[tuple[str, int, float, float, str]]:
    """(chrom, pos, priority, af_sas, rsid) for every matched site."""
    rows = []
    with gzip.open(paths.CANDIDATES, "rt", encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        idx = {name: i for i, name in enumerate(header)}
        for line in f:
            fld = line.rstrip("\n").split("\t")
            try:
                af_sas = float(fld[idx["af_sas"]])
            except ValueError:
                continue
            rows.append(
                (
                    fld[idx["chrom"]],
                    int(fld[idx["pos"]]),
                    float(fld[idx["priority"]]),
                    af_sas,
                    fld[idx["rsid_r"]],
                )
            )
    return rows


def main() -> None:
    if ENRICHMENT.exists():
        print(f"[enrich] already complete ({ENRICHMENT}); delete to re-run")
        return
    if not paths.CANDIDATES.exists():
        sys.exit("[enrich] candidates.tsv.gz missing — run `make run` first")

    print("[enrich] loading candidates ...")
    rows = load_candidates()
    print(f"[enrich] {len(rows)} candidate sites")

    print("[enrich] collapsing to loci ...")
    positive = [(c, p, pr) for c, p, pr, _af, _rs in rows if pr > 0]
    loci = collapse(positive, WINDOW_BP)
    pile = loci[:TOP_K_LOCI]
    print(f"[enrich] {len(loci)} loci with priority > 0; pile = top {len(pile)}")

    tmp = LOCI.parent / (LOCI.name + ".tmp")
    with gzip.open(tmp, "wt", encoding="utf-8") as out:
        out.write("chrom\tpos\tpriority\tn_absorbed\n")
        for lc in loci:
            out.write(f"{lc.chrom}\t{lc.pos}\t{lc.priority:.6g}\t{lc.n_absorbed}\n")
    tmp.replace(LOCI)

    print("[enrich] preloading iHS tracks (self-checked) ...")
    sas_tracks = [Track(p) for p in SAS_POPS]
    eur_tracks = [Track(p) for p in EUR_POPS]

    min_pops = MIN_POPS_WITH_DATA
    pile_keyed = [(lc.chrom, lc.pos) for lc in pile]
    pile_sas = {k: mean_stat(sas_tracks, *k, min_pops) for k in pile_keyed}
    pile_eur = {k: mean_stat(eur_tracks, *k, 1) for k in pile_keyed}

    # Control pool: every matched site with data, AF-binned, away from pile loci.
    pile_by_chrom: dict[str, list[int]] = {}
    for chrom, pos in pile_keyed:
        bisect.insort(pile_by_chrom.setdefault(chrom, []), pos)

    def near_pile(chrom: str, pos: int) -> bool:
        arr = pile_by_chrom.get(chrom, [])
        i = bisect.bisect_left(arr, pos)
        r = EXCLUDE_BP_AROUND_PILE
        return (i > 0 and pos - arr[i - 1] <= r) or (i < len(arr) and arr[i] - pos <= r)

    print("[enrich] building AF-matched control pool ...")
    pool: dict[int, list[tuple[float, float]]] = {}  # af_bin -> [(sas_stat, eur_stat)]
    pool_abstained = 0
    for chrom, pos, _pr, af_sas, _rs in rows:
        if near_pile(chrom, pos):
            continue
        s = mean_stat(sas_tracks, chrom, pos, min_pops)
        if s is None:
            pool_abstained += 1
            continue
        e = mean_stat(eur_tracks, chrom, pos, 1)
        pool.setdefault(af_bin(af_sas, AF_BIN_WIDTH), []).append(
            (s, e if e is not None else float("nan"))
        )

    af_by_key = {(c, p): af for c, p, _pr, af, _rs in rows}
    usable: list[tuple[tuple[str, int], float, int]] = []
    for k in pile_keyed:
        v = pile_sas[k]
        b = af_bin(af_by_key[k], AF_BIN_WIDTH)
        if v is not None and b in pool:
            usable.append((k, v, b))
    pile_abstained = len(pile_keyed) - len(usable)
    pile_mean_sas = statistics.fmean(v for _k, v, _b in usable)
    eur_vals = [ev for k, _v, _b in usable if (ev := pile_eur[k]) is not None]
    pile_mean_eur = statistics.fmean(eur_vals) if eur_vals else None

    print(f"[enrich] permuting ({N_CONTROL_SETS} control sets) ...")
    rng = random.Random(SEED)
    control_sas, control_eur = [], []
    for _ in range(N_CONTROL_SETS):
        s_sum = e_sum = 0.0
        e_n = 0
        for _k, _v, b in usable:
            cs, ce = rng.choice(pool[b])
            s_sum += cs
            if ce == ce:  # not NaN
                e_sum += ce
                e_n += 1
        control_sas.append(s_sum / len(usable))
        control_eur.append(e_sum / e_n if e_n else float("nan"))

    result = {
        "stage": "13.2 selection-signature enrichment",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "dials": DIALS,
        "inputs": {
            "candidates": str(paths.CANDIDATES),
            "loci_total_priority_gt0": len(loci),
            "pile_loci": len(pile),
            "pile_abstained_no_ihs_data": pile_abstained,
            "pile_used": len(usable),
            "pool_sites_used": sum(len(v) for v in pool.values()),
            "pool_abstained_no_ihs_data": pool_abstained,
        },
        "sas_ihs": {
            "pile_mean": pile_mean_sas,
            "control_mean_of_means": statistics.fmean(control_sas),
            "control_sd_of_means": statistics.stdev(control_sas),
            "empirical_p_one_sided": empirical_p(pile_mean_sas, control_sas),
        },
        "eur_ihs_comparison": {
            "pile_mean": pile_mean_eur,
            "control_mean_of_means": statistics.fmean(control_eur),
            "empirical_p_one_sided": (
                empirical_p(pile_mean_eur, control_eur) if pile_mean_eur is not None else None
            ),
        },
        "outputs": {"loci": str(LOCI), "enrichment": str(ENRICHMENT)},
    }
    atomic_write_json(ENRICHMENT, result)
    print(json.dumps(result["sas_ihs"], indent=2))
    print(f"[enrich] complete -> {ENRICHMENT}")


if __name__ == "__main__":
    main()
