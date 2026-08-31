"""probes/lrrk2_slice5_1000g.py — the genetic lens over 1000G phase-3 WGS (non-coding-inclusive).

Slice 5 over gnomAD EXOMES ABSTAINED on LRRK2/RIPK2 — their disease variants are non-coding and
absent from an exome sites file (exactly the regulatory layer the program is about, canon SS2/SS11.5).
1000G phase-3 is WGS, so it carries those variants, with per-superpopulation AF (SAS_AF / EUR_AF).
This re-runs the genetic lens over 1000G and, critically, distinguishes ABSTAIN (no data = the
informational zero) from a measured NO (SAS_AF <= EUR_AF) — conflating them is the measurement/
decision gap the design forbids (canon SS6.15).

    # 1. one-time extraction (cached), from the repo root:
    gzip -dc data/reference/ALL.wgs.phase3_v5c.sites.vcf.gz \
        | python3 <scratch>/extract_af_1000g.py       # writes /tmp/1000g_cloud_af.tsv
    # 2. the 4-lens convergence with the 1000G genetic lens:
    PYTHONPATH=src python3 probes/lrrk2_slice5_1000g.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lrrk2_slice2 import SEED, grow, presentation_genes, string_adjacency  # noqa: E402
from lrrk2_slice3 import hub_counts  # noqa: E402
from lrrk2_slice4 import gtex_profiles, pearson  # noqa: E402
from lrrk2_slice5 import cloud_rsids  # noqa: E402

from homeostat.nodes import BORN, node_status  # noqa: E402

CACHE = Path("/tmp/1000g_cloud_af.tsv")  # rsid \t sas \t eur
TRIAD = {"NOD2", "RIPK2", "LRRK2"}
KNOWN_HUBS = {"HLA-DRB1", "HLA-DQA1", "IL12B", "TNFSF15", "IL18R1", "IL1RL1", "LACC1"}
COEXPR_MIN = 0.5
RECUR_MIN = 2


def genetic_vote(cloud: set[str], rs2gene: dict[str, str]):
    """Per gene: 'yes' if a majority of its 1000G variants are SA-shifted (SAS_AF > EUR_AF),
    'no' if measured but not, 'abstain' if the gene has NO 1000G variant (the informational zero)."""
    tally: dict[str, list[int]] = {g: [] for g in cloud}
    detail: dict[str, list[tuple[str, float, float]]] = {g: [] for g in cloud}
    for line in CACHE.open():
        rs, sas, eur = line.rstrip("\n").split("\t")
        g = rs2gene.get(rs)
        if g is None:
            continue
        try:
            fs, fe = float(sas), float(eur)
        except ValueError:
            continue
        tally[g].append(1 if fs > fe else 0)
        detail[g].append((rs, fs, fe))
    vote: dict[str, str] = {}
    for g, hits in tally.items():
        if not hits:
            vote[g] = "abstain"
        elif sum(hits) / len(hits) >= 0.5:
            vote[g] = "yes"
        else:
            vote[g] = "no"
    return vote, detail


def _gtag(v: str) -> str:
    return {"yes": "Y", "no": "N", "abstain": "·"}[v]


def main() -> None:
    pres = presentation_genes()
    cloud, _ = grow(SEED, string_adjacency(400), pres)
    string700, _ = grow(SEED, string_adjacency(700), pres)
    hc = hub_counts(cloud)
    floor = sorted(hc.values(), reverse=True)[max(1, len(cloud) // 10) - 1]
    prof = gtex_profiles(cloud)
    nod2 = prof.get("NOD2")
    rs2gene = cloud_rsids(cloud)
    v_gen, detail = genetic_vote(cloud, rs2gene)

    n_data = sum(1 for g in cloud if v_gen[g] != "abstain")
    print(f"cloud {len(cloud)} | genes with 1000G data: {n_data} | abstained: {len(cloud) - n_data}\n")

    votes: dict[str, tuple[int, int, int, int, str]] = {}
    for g in cloud:
        s = 1 if g in string700 else 0
        p = 1 if hc.get(g, 0) < floor else 0
        c = 1 if (nod2 and g in prof and pearson(prof[g], nod2) >= COEXPR_MIN) else 0
        x = 1 if v_gen[g] == "yes" else 0
        votes[g] = (s, p, c, x, v_gen[g])
    born = [g for g in cloud if node_status(sum(votes[g][:4]), 0, RECUR_MIN) == BORN]

    print("triad — votes (string, spec, coexpr, GENETIC) = support   [genetic Y/N/·=abstain]:")
    for g in sorted(TRIAD):
        s, p, c, x, gv = votes[g]
        print(f"  {g:<10} ({s},{p},{c},{_gtag(gv)}) = {s + p + c + x}   born={g in born}")
        for rs, fs, fe in detail[g]:
            print(f"        {rs}: SAS={fs:.4g} EUR={fe:.4g}  {'SA-shift' if fs > fe else 'no shift'}")
    print("surviving hubs — votes:")
    for g in sorted(KNOWN_HUBS & set(cloud)):
        s, p, c, x, gv = votes[g]
        print(f"  {g:<10} ({s},{p},{c},{_gtag(gv)}) = {s + p + c + x}   born={g in born}")
    print(f"\nBORN (converge on >= {RECUR_MIN}): {len(born)}")
    print(f"  triad in born: {sorted(TRIAD & set(born))}  ({len(TRIAD & set(born))}/3)")
    print(f"  hubs  in born: {sorted(KNOWN_HUBS & set(born))}")


if __name__ == "__main__":
    main()
