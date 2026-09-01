"""Intent tests for the κ spine, checked against the Regenesis definitions on
small directed/undirected graphs with known structure."""

from homeostat.kappa import (
    chain_significance,
    components_joined,
    coverage,
    is_bridge,
    marginal_coverage,
    reachable,
    weak_components,
)


def test_reachable_and_coverage_directed():
    # A -> B -> C, A -> D. cover(A)=3, cover(B)=1, cover(C)=0.
    adj = {"A": {"B", "D"}, "B": {"C"}}
    assert reachable(adj, "A") == {"B", "C", "D"}
    cov = coverage(adj)
    assert cov["A"] == 3 and cov["B"] == 1 and cov["C"] == 0 and cov["D"] == 0


def test_marginal_coverage_subtracts_selected():
    adj = {"A": {"B", "C"}, "X": {"C"}}
    # κ(A|∅) = |{B,C}| = 2; κ(A|{X}) removes C (reachable from X) -> {B} = 1.
    assert marginal_coverage(adj, "A", []) == 2
    assert marginal_coverage(adj, "A", ["X"]) == 1


def test_is_bridge_joins_disjoint_components():
    # {A,B} and {C,D} disjoint. A->C would bridge; A->B would not.
    adj = {"A": {"B"}, "C": {"D"}}
    assert is_bridge(adj, "A", "C")
    assert not is_bridge(adj, "A", "B")
    assert not is_bridge(adj, "A", "ZZZ")  # unknown node -> not a bridge


def test_weak_components_ignore_direction():
    adj = {"A": {"B"}, "C": {"D"}, "E": set()}
    comps = weak_components(adj)
    assert sorted(len(c) for c in comps) == [1, 2, 2]


def test_components_joined_counts_distinct_base_components():
    base_components = [{"A", "B"}, {"C", "D"}, {"E"}]
    # a candidate touching A, C, E touches 3 components; touching A, B touches 1.
    assert components_joined({"A", "C", "E"}, base_components) == 3
    assert components_joined({"A", "B"}, base_components) == 1


def test_chain_significance_forced_hop_is_zero():
    out_degree = {"hub": 8, "forced": 1, "mid": 3}
    # a single forced hop carries no surprise; a hub hop scores log(8).
    assert chain_significance(["forced", "x"], out_degree) == 0.0
    sig = chain_significance(["hub", "mid", "x"], out_degree)
    assert sig > 0
