"""probes/lrrk2_slice2.py — Slice 2: node-birth from the NOD2 seed via the STRING co-occurrence lens.

Slice 1 left NOD2 as the surviving seed (it bridges both disease clusters). Here node-birth GROWS
that seed: a neighbor is BORN into the mechanism only where TWO lenses converge — it is a STRING
co-occurrence neighbor of the current mechanism AND it wires to the presentation's traits (the GWAS
lens, i.e. it is one of the ~1300 presentation genes). recur_min = 2 = "needs both lenses" (uses the
real homeostat.nodes lifecycle).

Honest expectation (from the STRING recon): the seed grows to RIPK2 (NOD2's direct partner, RIP2) and
excludes the HLA hubs — but LRRK2, whose role is regulatory not a physical bind, is NOT reached by the
physical lens and needs a different (genetic) lens in a later slice. STRING alone is one witness, not
evidence. Reproducible:

    PYTHONPATH=src python3 probes/lrrk2_slice2.py
"""

from __future__ import annotations

import csv
import gzip
import re
from pathlib import Path

from homeostat.nodes import BORN, node_status

DATA = Path(__file__).resolve().parent.parent / "data" / "network"
SEED = "NOD2"
RECUR_MIN = 2  # a node is BORN only where 2 lenses converge (STRING co-occurrence + GWAS presence)
STRING_THRESHOLD = 400  # STRING "medium confidence"; reported at 700 too (not tuned to outcome)
MAX_HOPS = 4

TRIAD = {"NOD2", "RIPK2", "LRRK2"}
KNOWN_HUBS = {"HLA-DRB1", "HLA-DQA1", "IL12B", "TNFSF15", "IL18R1", "IL1RL1", "LACC1"}

_SPLIT = re.compile(r"\s*[;,]\s*|\s+-\s+")
_GENE_COL = 14


def presentation_genes() -> set[str]:
    """The GWAS trait-wiring lens: every gene across leprosy + Crohn's + IBD (Slice 1's candidate set)."""
    files = ["gwas_leprosy.tsv", "gwas_crohns_disease.tsv", "gwas_inflammatory_bowel_disease.tsv"]
    out: set[str] = set()
    for f in files:
        with (DATA / f).open(encoding="utf-8", errors="replace") as fh:
            r = csv.reader(fh, delimiter="\t")
            next(r, None)
            for row in r:
                if len(row) > _GENE_COL:
                    for g in _SPLIT.split(row[_GENE_COL]):
                        g = g.strip()
                        if g and g != "NR":
                            out.add(g)
    return out


def string_adjacency(threshold: int) -> dict[str, set[str]]:
    """Symbol-level STRING-physical adjacency for edges with combined_score >= threshold."""
    ensp2sym: dict[str, str] = {}
    with gzip.open(DATA / "string_protein_info.txt.gz", "rt", errors="replace") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for row in r:
            if len(row) >= 2:
                ensp2sym[row[0]] = row[1]
    adj: dict[str, set[str]] = {}
    with gzip.open(DATA / "string_physical_links.txt.gz", "rt", errors="replace") as fh:
        next(fh, None)
        for line in fh:
            a, b, s = line.split()
            if int(s) < threshold:
                continue
            ga, gb = ensp2sym.get(a), ensp2sym.get(b)
            if ga and gb:
                adj.setdefault(ga, set()).add(gb)
                adj.setdefault(gb, set()).add(ga)
    return adj


def grow(seed: str, adj: dict[str, set[str]], presentation: set[str]) -> tuple[set[str], list[int]]:
    """Node-birth from the seed: iteratively BORN = STRING-neighbor (support+1) AND presentation (support+1),
    recur_min = 2. Returns the grown mechanism and the count born per hop (the growth-κ trajectory)."""
    mechanism = {seed}
    frontier = {seed}
    per_hop: list[int] = []
    for _ in range(MAX_HOPS):
        candidates: set[str] = set()
        for g in frontier:
            candidates |= adj.get(g, set())
        candidates -= mechanism
        born = set()
        for c in candidates:
            support = 1 + (1 if c in presentation else 0)  # STRING-neighbor(1) + GWAS-present(1)
            if node_status(support, 0, RECUR_MIN) == BORN:
                born.add(c)
        if not born:
            break
        mechanism |= born
        per_hop.append(len(born))
        frontier = born
    return mechanism, per_hop


def main() -> None:
    presentation = presentation_genes()
    for threshold in (STRING_THRESHOLD, 700):
        adj = string_adjacency(threshold)
        mech, per_hop = grow(SEED, adj, presentation)
        print(f"=== STRING threshold {threshold} ===")
        print(f"grown mechanism: {len(mech)} genes  (born per hop: {per_hop})")
        print(f"  triad recovered: {sorted(TRIAD & mech)}  ({len(TRIAD & mech)}/3)")
        print(f"  hubs pulled in : {sorted(KNOWN_HUBS & mech)}  ({len(KNOWN_HUBS & mech)})")
        if len(mech) <= 30:
            print(f"  members: {', '.join(sorted(mech))}")
        print()


if __name__ == "__main__":
    main()
