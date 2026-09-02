"""Intent tests for the metabolic-flux adapter — Reactome metabolic-pathway co-membership.

An undirected vote: sign=+1, verb "channels", mode "", network "metabolic", both orderings.
Only genes in a pathway UNDER the Metabolism subtree count (the scoping is load-bearing). Entrez ids
normalized to symbols; unmapped dropped."""

from homeostat.metabolic import (
    ENTREZ,
    PATHWAY,
    SPECIES,
    co_metabolism_events,
    metabolic_pathways,
    pair_up,
)

ENTREZ_SYMBOL = {"10": "HK1", "20": "GPI", "30": "PFKL", "99": "SRC"}


def _rrow(entrez, pathway, species="Homo sapiens"):
    r = [""] * 6
    r[ENTREZ], r[PATHWAY], r[SPECIES] = entrez, pathway, species
    return r


# ---- the pure metabolic-subtree BFS ----------------------------------------------


def test_metabolic_pathways_collects_the_subtree():
    relation = [
        ["ROOT", "MET_A"],
        ["MET_A", "MET_B"],
        ["ROOT", "MET_C"],
        ["SIGNALING", "SIG_X"],  # a different subtree, not reachable from ROOT
    ]
    assert metabolic_pathways(relation, root="ROOT") == {"ROOT", "MET_A", "MET_B", "MET_C"}


# ---- the pure co-membership pairing ----------------------------------------------


def test_pair_up_is_distinct_sorted_unordered_pairs():
    assert pair_up(["GPI", "HK1", "PFKL"]) == [("GPI", "HK1"), ("GPI", "PFKL"), ("HK1", "PFKL")]
    assert pair_up(["A", "A"]) == []  # deduped -> a singleton pathway makes no edge
    assert pair_up(["B", "A"]) == [("A", "B")]  # sorted


# ---- grouping + emission on real shapes ------------------------------------------


def test_co_metabolism_emits_both_orderings_for_metabolic_pathways_only():
    metabolic = {"MET_GLYCOLYSIS"}
    rows = [
        _rrow("10", "MET_GLYCOLYSIS"),  # HK1, metabolic
        _rrow("20", "MET_GLYCOLYSIS"),  # GPI, metabolic
        _rrow("99", "SIG_PATHWAY"),  # SRC, NOT metabolic -> excluded
        _rrow("30", "MET_GLYCOLYSIS", species="Mus musculus"),  # non-human -> excluded
    ]
    events = co_metabolism_events(rows, metabolic, ENTREZ_SYMBOL)
    edges = {(e.subject, e.target) for e in events}
    assert edges == {("GPI", "HK1"), ("HK1", "GPI")}  # one pair, both orderings
    e = events[0]
    assert (e.network, e.verb, e.sign, e.mode) == ("metabolic", "channels", 1, "")


def test_unmapped_entrez_is_dropped():
    metabolic = {"MET_P"}
    rows = [_rrow("10", "MET_P"), _rrow("77777", "MET_P")]  # 77777 not in the symbol map
    events = co_metabolism_events(rows, metabolic, ENTREZ_SYMBOL)
    assert events == []  # only HK1 maps -> singleton pathway -> no edge
