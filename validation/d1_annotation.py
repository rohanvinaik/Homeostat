"""D1 — annotation-recovery falsifier: does independently-known biology fall out of geometry?

The panel recovers components from THREE lenses — population differentiation (Fst), GTEx co-expression,
STRING physical binding. It never sees disease genetics. GWAS disease-trait association is therefore a
genuinely HELD-OUT annotation, independent of all three lenses. The falsifier: are the blind-recovered
components enriched for sharing their seed's SPECIFIC disease traits, versus the random decoys?

If yes, independently-curated disease biology (the GWAS catalog) fell out of a structure built only
from population genetics + expression + physical interaction — the §3.2 recovery test, run through the
real pipeline. A permutation null (shuffle the recovered/decoy label) gives the p-value.

    PYTHONPATH=src python3 validation/d1_annotation.py     # one pass over the GWAS catalog
"""

from __future__ import annotations

import csv
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "probes"))
from a1_panel import MECHANISMS  # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data" / "network"
CATALOG = DATA / "gwas-catalog-download-associations-alt-full.tsv"
GENE_COL, TRAIT_COL = 14, 34
_SPLIT = re.compile(r"\s*[;,]\s*|\s+-\s+")
COMPONENT = {"component", "core", "deep_core"}
N_PERM = 2000


def gene_traits(genes: set[str]) -> dict[str, set[str]]:
    """gene -> set of GWAS MAPPED_TRAITs (one pass over the full catalog)."""
    out: dict[str, set[str]] = {g: set() for g in genes}
    with CATALOG.open(encoding="utf-8", errors="replace") as fh:
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
                if g in out:
                    out[g].add(t)
    return out


def main() -> None:
    labels = json.loads(Path("/tmp/a1_labels.json").read_text())
    observed = json.loads(Path("/tmp/a1_observed.json").read_text())
    seeds = {s for s, _ in MECHANISMS.values()}
    genes = {v["gene"] for v in labels.values()} | seeds
    traits = gene_traits(genes)

    # generic-trait guard: drop traits shared by the injected promiscuous hubs (they share with everything)
    hub_genes = {v["gene"] for v in labels.values() if v["role"] == "hub"}
    generic = set().union(*(traits.get(h, set()) for h in hub_genes)) if hub_genes else set()

    recov_share, decoy_share = [], []  # 1/0 per gene: shares a specific seed trait?
    for tok, v in labels.items():
        if v["role"] in ("seed", "hub"):
            continue
        seed = MECHANISMS[v["mech"]][0]
        t_seed = traits.get(seed, set()) - generic  # the seed's SPECIFIC disease traits
        shares = int(bool((traits.get(v["gene"], set()) - generic) & t_seed))
        if observed.get(tok) in COMPONENT:
            recov_share.append(shares)
        elif v["role"] == "decoy":
            decoy_share.append(shares)

    def rate(xs: list[int]) -> float:
        return sum(xs) / max(1, len(xs))

    obs_gap = rate(recov_share) - rate(decoy_share)
    pool = recov_share + decoy_share
    k = len(recov_share)
    rng = random.Random(0)
    ge = 0
    for _ in range(N_PERM):
        rng.shuffle(pool)
        gap = rate(pool[:k]) - rate(pool[k:])
        if gap >= obs_gap:
            ge += 1
    p = (ge + 1) / (N_PERM + 1)

    print("D1 — annotation recovery: held-out annotation = shares the seed's SPECIFIC GWAS disease trait")
    print(f"  lenses used (blind to disease): Fst differentiation · GTEx co-expression · STRING binding")
    print(f"  recovered components sharing seed disease trait: {sum(recov_share)}/{len(recov_share)}"
          f"  = {rate(recov_share):.0%}")
    print(f"  random decoys sharing seed disease trait:        {sum(decoy_share)}/{len(decoy_share)}"
          f"  = {rate(decoy_share):.0%}")
    print(f"  enrichment gap = {obs_gap:+.0%}   permutation p = {p:.4f}  ({N_PERM} shuffles)")
    verdict = "PASS — known disease biology recovered from geometry that never used it" if (
        p < 0.05 and obs_gap > 0) else "NOT SIGNIFICANT"
    print(f"\nD1 VERDICT: {verdict}")


if __name__ == "__main__":
    main()
