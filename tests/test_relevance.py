"""Intent tests for the relevance filter (the input layer's first turn-component — diagnosis → the
possibly-relevant subspace). Authored from the design; the pure decisions are Detective-pinned."""

from homeostat.fungibility import Fungible
from homeostat.relevance import fungible_map, relevant_subspace, trait_gene_index


def _row(gene, trait):
    # a GWAS catalog row: gene at MAPPED_GENE_COL (14), trait at MAPPED_TRAIT_COL (34).
    r = [""] * 35
    r[14] = gene
    r[34] = trait
    return r


# ---- trait_gene_index: the diagnosis→gene reference ----------------------------------


def test_trait_gene_index_maps_trait_to_its_genes():
    rows = [_row("A", "adhd"), _row("B", "adhd"), _row("C", "autism")]
    assert trait_gene_index(rows) == {"adhd": {"A", "B"}, "autism": {"C"}}


def test_trait_gene_index_short_row_is_skipped():
    # a row without a MAPPED_TRAIT column contributes nothing (no IndexError).
    assert trait_gene_index([[""] * 10, _row("A", "adhd")]) == {"adhd": {"A"}}


def test_trait_gene_index_multi_gene_multi_trait_row():
    # "A, B" -> two genes; "x, y" -> two traits; each trait gets both genes.
    assert trait_gene_index([_row("A, B", "x, y")]) == {"x": {"A", "B"}, "y": {"A", "B"}}


def test_trait_gene_index_row_exactly_at_the_boundary_is_skipped():
    # a row of exactly MAPPED_TRAIT_COL (34) columns lacks the trait column (0-indexed 34 needs len
    # >= 35) -> skipped, never an IndexError. Pins the `<= MAPPED_TRAIT_COL` boundary.
    assert trait_gene_index([[""] * 34]) == {}


# ---- relevant_subspace: the tested relevance scope -----------------------------------


def test_relevant_subspace_is_canonical_widened_by_fungibility():
    # adhd's canonical genes {A,B}; A has a fungible partner A2 -> the subspace includes it.
    sub = relevant_subspace("adhd", {"adhd": {"A", "B"}}, {"A": {"A2"}, "B": set()})
    assert sub == {"A", "B", "A2"}


def test_relevant_subspace_unknown_diagnosis_is_empty():
    # the operator named a trait the catalog does not carry -> an honest empty miss.
    assert relevant_subspace("unknown", {"adhd": {"A"}}, {}) == set()


def test_relevant_subspace_no_fungible_is_just_the_canonical_genes():
    assert relevant_subspace("adhd", {"adhd": {"A", "B"}}, {}) == {"A", "B"}


# ---- fungible_map: only EARNED role-equivalence widens --------------------------------


def test_fungible_map_only_earned_pairs_widen_symmetrically():
    fungibles = [
        Fungible("A", "B", "fungible", 2),  # earned (>=2 banks) -> widens both ways
        Fungible("C", "D", "coincidental", 1),  # one bank -> does not widen
        Fungible("E", "F", "seed-only", 0),  # resemblance only -> does not widen
    ]
    assert fungible_map(fungibles) == {"A": {"B"}, "B": {"A"}}
