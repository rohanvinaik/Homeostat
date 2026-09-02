"""homeostat.trait_wiring — the tier-3 CALIBRATION PRIOR (GWAS pleiotropy node-weights).

Trait-wiring is NOT an edge and NOT significance (κ is). Per LAW 9 it is a per-gene node-weight
(how load-bearing a node tends to be) that only TUNES THE SEARCH, never asserts a coupling. The
weight is distinct-trait **pleiotropy** — how many traits a gene maps to across the GWAS catalog. A
many-trait gene is a BRIDGE (joins mechanism-clusters), so it is a cheap bridge-prior: the search
biases toward it, κ confirms or refuses the real significance. GWAS-as-search-prior is Law 1's one
sanctioned use of a population statistic (never the method, object, or verdict).
"""

from __future__ import annotations

from collections.abc import Iterable

# gwas-catalog-associations_ontology-annotated columns (tab), 0-indexed.
MAPPED_GENE_COL = 14  # MAPPED_GENE
MAPPED_TRAIT_COL = 34  # MAPPED_TRAIT (EFO-standardized)


def parse_genes(mapped_gene: str) -> list[str]:
    """Split a GWAS MAPPED_GENE field into symbols. Multiple genes are ", "-separated; intergenic
    flanks " - "-separated (space-hyphen-space, NOT a bare hyphen — so `MIR9-2HG` stays intact).
    Empty / "NR" drop out. Pure over the field string."""
    genes: list[str] = []
    for part in mapped_gene.split(", "):
        for token in part.split(" - "):
            gene = token.strip()
            if gene and gene != "NR":
                genes.append(gene)
    return genes


def parse_traits(mapped_trait: str) -> list[str]:
    """Split a MAPPED_TRAIT field into EFO trait labels (", "-separated); empties drop. Pure."""
    return [t.strip() for t in mapped_trait.split(", ") if t.strip()]


def trait_wiring(rows: Iterable[list[str]]) -> dict[str, int]:
    """The calibration prior: per gene, the count of DISTINCT traits it maps to — a pleiotropy
    node-weight (the cheap bridge-prior). A node-weight never an edge; a search-order prior never
    significance. Orchestration over `parse_genes` / `parse_traits`; intent-tested.
    """
    traits_by_gene: dict[str, set[str]] = {}
    for row in rows:
        if len(row) <= MAPPED_TRAIT_COL:
            continue
        traits = parse_traits(row[MAPPED_TRAIT_COL])
        for gene in parse_genes(row[MAPPED_GENE_COL]):
            traits_by_gene.setdefault(gene, set()).update(traits)
    return {gene: len(traits) for gene, traits in traits_by_gene.items()}
