"""probes/lrrk2_control.py — Slice 1 of the multi-lens LRRK2 positive control.

The FIRST honest baseline: candidates = every gene across leprosy ∪ Crohn's ∪ IBD (unbiased, no
hand-picking); ONE lens (GWAS trait-wiring); run the engine's elimination and see what survives.

We EXPECT this to fail to find LRRK2 — one lens is a single number in disguise, and the LRRK2
mechanism is compositional (RIPK2 is in the leprosy cluster, LRRK2/NOD2 in the gut cluster; no single
gene bridges both). It is run to see the failure mode concretely, not to succeed. Reproducible:

    PYTHONPATH=src python3 probes/lrrk2_control.py
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

from homeostat.search import entropy_bits, resolved, survivors

DATA = Path(__file__).resolve().parent.parent / "data" / "network"
MAPPED_GENE_COL = 14  # 0-based; GWAS-catalog "MAPPED_GENE"

# The two disease clusters the mechanism must bridge.
CLUSTER_FILES = {
    "leprosy": ["gwas_leprosy.tsv"],
    "gut": ["gwas_crohns_disease.tsv", "gwas_inflammatory_bowel_disease.tsv"],
}

TRIAD = {"LRRK2", "NOD2", "RIPK2"}  # the known compositional bridge (§9) — the answer to recover
KNOWN_HUBS = {"HLA-DRB1", "HLA-DQA1", "IL12B", "TNFSF15", "IL18R1", "IL1RL1", "LACC1"}

_SPLIT = re.compile(r"\s*[;,]\s*|\s+-\s+")  # ';' ',' or ' - ' (NOT bare '-', which is in gene names)


def genes_in(path: Path) -> set[str]:
    """The distinct mapped genes in one GWAS-catalog file (splitting multi-gene cells honestly)."""
    out: set[str] = set()
    with path.open(encoding="utf-8", errors="replace") as fh:
        reader = csv.reader(fh, delimiter="\t")
        next(reader, None)  # header
        for row in reader:
            if len(row) <= MAPPED_GENE_COL:
                continue
            for g in _SPLIT.split(row[MAPPED_GENE_COL]):
                g = g.strip()
                if g and g != "NR":
                    out.add(g)
    return out


def cluster_membership() -> dict[str, set[str]]:
    """gene -> set of clusters it wires to (from the GWAS trait-wiring lens)."""
    per_cluster = {c: set().union(*(genes_in(DATA / f) for f in files)) for c, files in CLUSTER_FILES.items()}
    membership: dict[str, set[str]] = {}
    for cluster, genes in per_cluster.items():
        for g in genes:
            membership.setdefault(g, set()).add(cluster)
    return membership


def main() -> None:
    membership = cluster_membership()
    candidates = sorted(membership)
    clusters = set(CLUSTER_FILES)

    # The trait-wiring lens as a KILL: a candidate that wires to only ONE cluster cannot be the bridge
    # on its own, so it is eliminated. (This is exactly the granularity that a single-gene view forces.)
    single_cluster_kill = [g for g in candidates if membership[g] != clusters]

    alive = survivors(candidates, [single_cluster_kill])

    print(f"candidates (leprosy ∪ Crohn's ∪ IBD): {len(candidates)} genes")
    print(f"killed by trait-wiring lens (single-cluster): {len(single_cluster_kill)}")
    print(f"survivors (wire to BOTH clusters): {len(alive)}")
    print(f"H = log2(survivors) = {entropy_bits(len(alive)):.2f} bits   resolved={resolved(len(alive))}")
    print()
    print("triad (the answer) survival:")
    for g in sorted(TRIAD):
        print(f"  {g:<10} wires={sorted(membership.get(g, set()))!s:<22} survived={g in alive}")
    print("known hubs survival:")
    for g in sorted(KNOWN_HUBS):
        if g in membership:
            print(f"  {g:<10} wires={sorted(membership[g])!s:<22} survived={g in alive}")
    print()
    triad_alive = TRIAD & set(alive)
    hubs_alive = KNOWN_HUBS & set(alive)
    print(f"VERDICT: {len(triad_alive)}/3 of the triad survived; {len(hubs_alive)} known hubs survived.")
    print("survivors:", ", ".join(alive) if len(alive) <= 40 else f"{len(alive)} genes (too many to list)")


if __name__ == "__main__":
    main()
