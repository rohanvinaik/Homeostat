"""probes/lrrk2_slice5.py — Slice 5: the GENETIC co-occurrence lens (gnomAD population shift).

LRRK2 failed the physical + expression lenses (Slice 4, support 1) because its relationship to NOD2 is
genetic/regulatory, not a stable complex or co-expression. This lens speaks that language: does a gene's
disease-variants show a South-Asian population shift (AF_sas > AF_nfe) like the presentation, which is
SA-elevated? Matched by rsID (gnomAD carries rsIDs), dodging the GRCh37/38 build mismatch.

    # 1. write the cloud's rsIDs:
    PYTHONPATH=src python3 probes/lrrk2_slice5.py rsids > /tmp/cloud_rsids.txt
    # 2. scan gnomAD once (bash), caching AF_sas/AF_nfe for those rsIDs (see the shell command run alongside)
    # 3. convergence with the 4th lens:
    PYTHONPATH=src python3 probes/lrrk2_slice5.py

Honest note: if LRRK2 is a shared Eurasian variant with SA-specific PENETRANCE (§7.4) rather than an
SA-frequency shift, this lens fails it too — and that is the §12.4 result (free marginal lenses cannot
see epistasis), shown not asserted.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lrrk2_slice2 import SEED, grow, presentation_genes, string_adjacency  # noqa: E402
from lrrk2_slice3 import hub_counts  # noqa: E402
from lrrk2_slice4 import gtex_profiles, pearson  # noqa: E402

from homeostat.nodes import BORN, node_status  # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data" / "network"
CACHE = Path("/tmp/gnomad_cloud_af.tsv")  # rsid \t af_sas \t af_nfe, from the gnomAD scan
_SPLIT = re.compile(r"\s*[;,]\s*|\s+-\s+")
GENE_COL, SNP_COL = 14, 21  # MAPPED_GENE, SNPS (0-based)
TRIAD = {"NOD2", "RIPK2", "LRRK2"}
KNOWN_HUBS = {"HLA-DRB1", "HLA-DQA1", "IL12B", "TNFSF15", "IL18R1", "IL1RL1", "LACC1"}
COEXPR_MIN = 0.5
RECUR_MIN = 2


def cloud_rsids(cloud: set[str]) -> dict[str, str]:
    """rsID -> gene, for the cloud genes' GWAS variants (from the 3 presentation files)."""
    files = ["gwas_leprosy.tsv", "gwas_crohns_disease.tsv", "gwas_inflammatory_bowel_disease.tsv"]
    out: dict[str, str] = {}
    for f in files:
        with (DATA / f).open(encoding="utf-8", errors="replace") as fh:
            r = csv.reader(fh, delimiter="\t")
            next(r, None)
            for row in r:
                if len(row) <= SNP_COL:
                    continue
                genes = {g.strip() for g in _SPLIT.split(row[GENE_COL])} & cloud
                if not genes:
                    continue
                for rs in re.split(r"[;,\s]+", row[SNP_COL]):
                    if rs.startswith("rs"):
                        for g in sorted(genes):  # sorted -> deterministic first-wins (set order varies)
                            out.setdefault(rs, g)
    return out


def sa_shift_vote(cloud: set[str], rs2gene: dict[str, str]) -> dict[str, int]:
    """vote_genetic per gene: 1 if a majority of its variants are SA-shifted (af_sas > af_nfe)."""
    tally: dict[str, list[int]] = {g: [] for g in cloud}
    with CACHE.open() as fh:
        for line in fh:
            rs, sas, nfe = line.rstrip("\n").split("\t")
            g = rs2gene.get(rs)
            if g is None:
                continue
            try:
                fs, fn = float(sas), float(nfe)
            except ValueError:
                continue
            tally[g].append(1 if fs > fn else 0)
    vote: dict[str, int] = {}
    for g, hits in tally.items():
        vote[g] = 1 if hits and sum(hits) / len(hits) >= 0.5 else 0
    return vote


def main() -> None:
    presentation = presentation_genes()
    cloud, _ = grow(SEED, string_adjacency(400), presentation)

    if len(sys.argv) > 1 and sys.argv[1] == "rsids":
        for rs in sorted(cloud_rsids(cloud)):
            print(rs)
        return

    string700, _ = grow(SEED, string_adjacency(700), presentation)
    hc = hub_counts(cloud)
    floor = sorted(hc.values(), reverse=True)[max(1, len(cloud) // 10) - 1]
    prof = gtex_profiles(cloud)
    nod2 = prof.get("NOD2")
    rs2gene = cloud_rsids(cloud)
    v_gen = sa_shift_vote(cloud, rs2gene)

    votes: dict[str, tuple[int, int, int, int]] = {}
    for g in cloud:
        votes[g] = (
            1 if g in string700 else 0,
            1 if hc.get(g, 0) < floor else 0,
            1 if (nod2 and g in prof and pearson(prof[g], nod2) >= COEXPR_MIN) else 0,
            v_gen.get(g, 0),
        )
    born = [g for g in cloud if node_status(sum(votes[g]), 0, RECUR_MIN) == BORN]

    print(f"cloud {len(cloud)} | genes with gnomAD variants: {sum(1 for g in cloud if v_gen.get(g))}\n")
    print("triad — votes (string, spec, coexpr, GENETIC) = support:")
    for g in sorted(TRIAD):
        s, p, c, x = votes[g]
        print(f"  {g:<10} ({s},{p},{c},{x}) = {s + p + c + x}   born={g in born}")
    print("surviving hubs — votes:")
    for g in sorted(KNOWN_HUBS & set(cloud)):
        s, p, c, x = votes[g]
        print(f"  {g:<10} ({s},{p},{c},{x}) = {s + p + c + x}   born={g in born}")
    print(f"\nBORN (converge on >= {RECUR_MIN}): {len(born)}")
    print(f"  triad in born: {sorted(TRIAD & set(born))}  ({len(TRIAD & set(born))}/3)")
    print(f"  hubs  in born: {sorted(KNOWN_HUBS & set(born))}")


if __name__ == "__main__":
    main()
