"""Intent tests for trait-wiring — the GWAS pleiotropy prior (a node-weight, not an edge).

The load-bearing parse: MAPPED_GENE separates multiple genes by ", " and intergenic flanks by " - "
(space-hyphen-space), so an internal-hyphen symbol like MIR9-2HG survives while RPL21P80 - UNC5D
splits. The weight is the count of DISTINCT traits a gene maps to."""

from homeostat.trait_wiring import (
    MAPPED_GENE_COL,
    MAPPED_TRAIT_COL,
    parse_genes,
    parse_traits,
    trait_wiring,
)


def _row(gene, trait):
    r = [""] * (MAPPED_TRAIT_COL + 1)
    r[MAPPED_GENE_COL], r[MAPPED_TRAIT_COL] = gene, trait
    return r


def test_parse_genes_splits_multi_and_intergenic_but_keeps_internal_hyphens():
    assert parse_genes("TRAF6") == ["TRAF6"]
    assert parse_genes("MIR9-2HG, TMEM161B-DT") == ["MIR9-2HG", "TMEM161B-DT"]  # ", " split
    assert parse_genes("RPL21P80 - UNC5D") == ["RPL21P80", "UNC5D"]  # intergenic " - " split
    assert parse_genes("NR") == [] and parse_genes("") == []  # not-reported / empty drop


def test_parse_traits_splits_efo_labels():
    assert parse_traits("intelligence") == ["intelligence"]
    assert parse_traits("body mass index, obesity") == ["body mass index", "obesity"]
    assert parse_traits("") == []


def test_trait_wiring_counts_distinct_traits_per_gene():
    rows = [_row("A", "t1"), _row("A", "t2"), _row("A", "t1"), _row("B - C", "t1")]
    # A maps to {t1, t2} (the repeat does not double-count); the intergenic pair each gets t1
    assert trait_wiring(rows) == {"A": 2, "B": 1, "C": 1}
