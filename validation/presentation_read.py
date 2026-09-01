"""Presentation-read machinery — genes-from-free-corpus + censored bridge + degree-matched null.

The reusable, symptom-agnostic core behind the CLI (`read.py`). Given a set of named phenotypes and a
keyword map (phenotype -> trait-substring list), it pulls genes from the free corpus (GWAS catalog +
DISEASES text-mined/curated + HPO), and provides the bridge/null helpers. It IMPOSES nothing and hard-
codes no particular condition — the caller supplies whatever presentation it wants to read.
"""

from __future__ import annotations

import csv
import random
import re
from pathlib import Path

NET = Path(__file__).resolve().parent.parent / "data" / "network"
LIT = Path(__file__).resolve().parent.parent / "data" / "literature"
GWAS = NET / "gwas-catalog-download-associations-alt-full.tsv"
_SPLIT = re.compile(r"\s*[;,]\s*|\s+-\s+")
_NOISE = re.compile(r"(-AS\d*$|-DT$|^MIR|^LINC|^RN[AU]|P\d+$|HG$|rRNA)", re.I)
TM_CONF_MIN = 1.5


def _clean(g: str) -> bool:
    return bool(g) and 2 <= len(g) <= 12 and not _NOISE.search(g)


def extract(pheno_names: set[str], kw: dict) -> tuple[dict, dict]:
    """gene-sets + matched trait-terms for the requested phenotypes, from GWAS + DISEASES + HPO.

    `kw` maps each phenotype name to its trait-keyword list. The CLI passes {symptom: [symptom_text]}
    for fully dynamic matching, so ANY symptom works — nothing is hard-coded."""
    genes = {p: set() for p in pheno_names}
    terms = {p: set() for p in pheno_names}

    def hit(name: str) -> list[str]:
        nl = name.lower()
        return [p for p in pheno_names if any(k in nl for k in kw[p])]

    with GWAS.open(encoding="utf-8", errors="replace") as fh:  # GWAS catalog (col14 gene, col34 trait)
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for row in r:
            if len(row) <= 34 or not row[34].strip():
                continue
            hs = hit(row[34])
            if hs:
                gs = [g.strip() for g in _SPLIT.split(row[14]) if _clean(g.strip())]
                for p in hs:
                    genes[p].update(gs)
                    terms[p].add(row[34])
    for fname, conf in (("diseases_textmining.tsv", 5), ("diseases_knowledge.tsv", None)):
        for row in csv.reader((LIT / fname).open(encoding="utf-8", errors="replace"), delimiter="\t"):
            if len(row) <= 3:
                continue
            if conf is not None:
                try:
                    if float(row[conf]) < TM_CONF_MIN:
                        continue
                except (ValueError, IndexError):
                    continue
            g = row[1].strip()
            if not _clean(g):
                continue
            for p in hit(row[3]):
                genes[p].add(g)
                terms[p].add(row[3])
    with (LIT / "hpo_genes_to_phenotype.txt").open(encoding="utf-8", errors="replace") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for row in r:
            if len(row) < 4 or not _clean(row[1].strip()):
                continue
            for p in hit(row[3]):
                genes[p].add(row[1].strip())
                terms[p].add(row[3])
    return genes, terms


def bridge_counts(sets: dict, adj: dict, universe: list) -> dict:
    """# genes touching ≥k of the sets (member OR STRING neighbor of a member), for each k."""
    n = len(sets)
    counts = {k: 0 for k in range(2, n + 1)}
    for g in universe:
        nbrs = adj.get(g, set())
        t = sum(1 for s in sets.values() if g in s or not nbrs.isdisjoint(s))
        for k in range(2, n + 1):
            if t >= k:
                counts[k] += 1
    return counts


def degree_bins(universe: list, adj: dict, nbins: int = 20) -> tuple[dict, list]:
    """Assign each universe gene to a degree quantile bin; return (bin_of, bins=list of gene-lists)."""
    ordered = sorted(universe, key=lambda g: len(adj.get(g, ())))
    bins = [ordered[i * len(ordered) // nbins:(i + 1) * len(ordered) // nbins] for i in range(nbins)]
    bin_of = {g: i for i, b in enumerate(bins) for g in b}
    return bin_of, bins


def sample_matched(s: set, bin_of: dict, bins: list, rng: random.Random) -> set:
    """A random gene-set matched to s's degree-bin profile (controls the connectivity confound)."""
    need: dict[int, int] = {}
    for g in s:
        need[bin_of[g]] = need.get(bin_of[g], 0) + 1
    out: set = set()
    for b, cnt in need.items():
        out.update(rng.sample(bins[b], min(cnt, len(bins[b]))))
    return out
