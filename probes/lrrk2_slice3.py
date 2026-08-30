"""probes/lrrk2_slice3.py — Slice 3: the spine-floor junk-killer on Slice 2's 289-gene cloud.

Slice 2 (STRING @400) grew NOD2 into 289 genes — the triad (incl. LRRK2) is in there, but so are the
generic hubs and ~280 junk. Significance-weighting §6 says the generic, over-connected nodes are
STRUCTURAL NOISE to be floored INTRINSICALLY by their promiscuity (the "generic ungrounded subject"),
not scored. So the first junk-killer is the SPINE FLOOR: rank the cloud by promiscuity (# distinct
traits a gene associates with, across the full GWAS catalog — genericness) and floor the top.

This is NOT tuned to keep LRRK2: we show the full ranked distribution and where the triad + named hubs
fall, then report survivors at a principled floor (top decile). It kills the generic HUBS; the specific
coincidental junk needs the next, independent lens (gnomAD population co-travel). Reproducible:

    PYTHONPATH=src python3 probes/lrrk2_slice3.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lrrk2_slice2 import SEED, grow, presentation_genes, string_adjacency  # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data" / "network"
FULL_CATALOG = DATA / "gwas-catalog-download-associations-alt-full.tsv"
_SPLIT = re.compile(r"\s*[;,]\s*|\s+-\s+")
GENE_COL, TRAIT_COL = 14, 34  # MAPPED_GENE, MAPPED_TRAIT (0-based)

TRIAD = {"NOD2", "RIPK2", "LRRK2"}
KNOWN_HUBS = {"HLA-DRB1", "HLA-DQA1", "IL12B", "TNFSF15", "IL18R1", "IL1RL1", "LACC1"}


def hub_counts(genes: set[str]) -> dict[str, int]:
    """# distinct traits each gene associates with in the full GWAS catalog (promiscuity = genericness)."""
    traits: dict[str, set[str]] = {g: set() for g in genes}
    with FULL_CATALOG.open(encoding="utf-8", errors="replace") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for row in r:
            if len(row) <= TRAIT_COL:
                continue
            t = row[TRAIT_COL].strip()
            if not t:
                continue
            for g in _SPLIT.split(row[GENE_COL]):
                g = g.strip()
                if g in traits:
                    traits[g].add(t)
    return {g: len(ts) for g, ts in traits.items()}


def main() -> None:
    presentation = presentation_genes()
    cloud, _ = grow(SEED, string_adjacency(400), presentation)
    print(f"Slice 2 cloud (STRING@400 grown from {SEED}): {len(cloud)} genes\n")

    hc = hub_counts(cloud)
    ranked = sorted(cloud, key=lambda g: hc.get(g, 0), reverse=True)

    print("most-promiscuous (spine-floor targets) — top 12:")
    for g in ranked[:12]:
        tag = " [HUB]" if g in KNOWN_HUBS else (" [TRIAD]" if g in TRIAD else "")
        print(f"  {g:<12} {hc.get(g, 0):>4} traits{tag}")
    print("\nwhere the triad falls (promiscuity rank / 289):")
    for g in sorted(TRIAD):
        if g in hc:
            print(f"  {g:<12} {hc[g]:>4} traits   rank {ranked.index(g) + 1}")

    # principled floor: kill the top decile by promiscuity (structural noise), no outcome tuning.
    n_floor = max(1, len(cloud) // 10)
    floored = set(ranked[:n_floor])
    survivors = [g for g in cloud if g not in floored]
    print(f"\nspine floor = kill top decile ({n_floor}) by promiscuity:")
    print(f"  survivors: {len(survivors)}  (killed {len(floored)})")
    print(f"  triad survived: {sorted(TRIAD & set(survivors))}  ({len(TRIAD & set(survivors))}/3)")
    print(f"  hubs killed:    {sorted(KNOWN_HUBS & floored)}")
    print(f"  hubs surviving: {sorted(KNOWN_HUBS & set(survivors))}")


if __name__ == "__main__":
    main()
