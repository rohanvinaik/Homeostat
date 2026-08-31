"""probes/lrrk2_genetic_diff.py — the GENERALIZED genetic lens: population differentiation, any group.

The SA-vs-EUR axis was the motivating example (founder's n=1), not the signal. The signal is a
variant being **differentiated across ANY isolatable group** — a population-structure signature,
direction-free (canon SS7 PBS). This replaces the coin-flip 'SAS>EUR' binary (44% of variants) with
'is this variant strongly differentiated across the superpopulations', which is rare and specific.
Per variant: max pairwise Hudson Fst across EUR/SAS/EAS/AFR/AMR (homeostat.pbs.hudson_fst). Per gene:
its most-differentiated variant. Vote = top decile by differentiation (Slice-3 spine-floor convention;
principled and shown, NOT tuned to LRRK2). ABSTAIN (·) = no 1000G data (the informational zero).

    gzip-free: cache from Ensembl 5-pop fetch at /tmp/1000g_5pop_af.tsv
    PYTHONPATH=src python3 probes/lrrk2_genetic_diff.py
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lrrk2_slice2 import SEED, grow, presentation_genes, string_adjacency  # noqa: E402
from lrrk2_slice3 import hub_counts  # noqa: E402
from lrrk2_slice4 import gtex_profiles, pearson  # noqa: E402
from lrrk2_slice5 import cloud_rsids  # noqa: E402

from homeostat.nodes import BORN, node_status  # noqa: E402
from homeostat.pbs import HAP_N, hudson_fst  # noqa: E402

CACHE = Path("/tmp/1000g_5pop_af.tsv")
POPS = ["EUR", "SAS", "EAS", "AFR", "AMR"]
TRIAD = {"NOD2", "RIPK2", "LRRK2"}
KNOWN_HUBS = {"HLA-DRB1", "HLA-DQA1", "IL12B", "TNFSF15", "IL18R1", "IL1RL1", "LACC1"}
COEXPR_MIN = 0.5
RECUR_MIN = 2


def variant_maxfst(freqs: dict[str, float]) -> float:
    """Max pairwise Hudson Fst across the 5 superpops for one variant (differentiation magnitude)."""
    return max(
        hudson_fst(freqs[a], HAP_N[a], freqs[b], HAP_N[b]) for a, b in combinations(POPS, 2)
    )


def load_gene_diff(rs2gene: dict[str, str]) -> tuple[dict[str, float], dict[str, list]]:
    """gene -> max differentiation (over its variants); plus per-gene variant detail."""
    gene_fst: dict[str, float] = {}
    detail: dict[str, list] = {}
    with CACHE.open() as fh:
        next(fh)  # header
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) < 3 + len(POPS):
                continue
            rs, allele, src = f[0], f[1], f[2]
            freqs = {p: float(f[3 + i]) for i, p in enumerate(POPS)}
            g = rs2gene.get(rs)
            if g is None:
                continue
            fst = variant_maxfst(freqs)
            detail.setdefault(g, []).append((rs, allele, src, freqs, fst))
            gene_fst[g] = max(gene_fst.get(g, 0.0), fst)
    return gene_fst, detail


def main() -> None:
    pres = presentation_genes()
    cloud, _ = grow(SEED, string_adjacency(400), pres)
    string700, _ = grow(SEED, string_adjacency(700), pres)
    hc = hub_counts(cloud)
    floor = sorted(hc.values(), reverse=True)[max(1, len(cloud) // 10) - 1]
    prof = gtex_profiles(cloud)
    nod2 = prof.get("NOD2")
    rs2gene = cloud_rsids(cloud)
    gene_fst, detail = load_gene_diff(rs2gene)

    with_data = [g for g in cloud if g in gene_fst]
    ranked = sorted(with_data, key=lambda g: gene_fst[g], reverse=True)
    n_top = max(1, len(with_data) // 10)  # top-decile differentiation (Slice-3 convention)
    diff_yes = set(ranked[:n_top])
    fst_cut = gene_fst[ranked[n_top - 1]] if ranked else 0.0
    rank_of = {g: i + 1 for i, g in enumerate(ranked)}

    print(f"cloud {len(cloud)} | genes with 1000G data: {len(with_data)} | abstained: {len(cloud) - len(with_data)}")
    print(f"differentiation vote = top decile by max-pairwise-Fst: {n_top} genes, Fst >= {fst_cut:.3f}\n")

    votes: dict[str, tuple[int, int, int, int, str]] = {}
    for g in cloud:
        s = 1 if g in string700 else 0
        p = 1 if hc.get(g, 0) < floor else 0
        c = 1 if (nod2 and g in prof and pearson(prof[g], nod2) >= COEXPR_MIN) else 0
        if g not in gene_fst:
            gv, x = "abstain", 0
        elif g in diff_yes:
            gv, x = "yes", 1
        else:
            gv, x = "no", 0
        votes[g] = (s, p, c, x, gv)
    born = [g for g in cloud if node_status(sum(votes[g][:4]), 0, RECUR_MIN) == BORN]

    def tag(v: str) -> str:
        return {"yes": "Y", "no": "N", "abstain": "·"}[v]

    print("triad — votes (string, spec, coexpr, GENETIC-diff) = support   [Y/N/·]:")
    for g in sorted(TRIAD):
        s, p, c, x, gv = votes[g]
        rk = f"Fst {gene_fst[g]:.3f} rank {rank_of[g]}/{len(with_data)}" if g in gene_fst else "no data"
        print(f"  {g:<10} ({s},{p},{c},{tag(gv)}) = {s + p + c + x}   born={g in born}   [{rk}]")
        for rs, allele, src, freqs, fst in detail.get(g, []):
            fr = " ".join(f"{p_}={freqs[p_]:.3g}" for p_ in POPS)
            print(f"        {rs} ({allele},{src}) maxFst={fst:.3f}  {fr}")
    print("named hubs — votes:")
    for g in sorted(KNOWN_HUBS & set(cloud)):
        s, p, c, x, gv = votes[g]
        rk = f"Fst {gene_fst[g]:.3f} rank {rank_of[g]}/{len(with_data)}" if g in gene_fst else "no data"
        print(f"  {g:<10} ({s},{p},{c},{tag(gv)}) = {s + p + c + x}   born={g in born}   [{rk}]")

    hubs_in = KNOWN_HUBS & set(cloud)
    print(f"\nBORN (converge on >= {RECUR_MIN}): {len(born)}")
    print(f"  triad in born: {sorted(TRIAD & set(born))}  ({len(TRIAD & set(born))}/3)")
    print(f"  hubs  in born: {sorted(KNOWN_HUBS & set(born))}")
    print(f"  triad survival {len(TRIAD & set(born)) / 3:.0%}  vs  named-hub survival "
          f"{len(KNOWN_HUBS & set(born)) / max(1, len(hubs_in)):.0%}")


if __name__ == "__main__":
    main()
