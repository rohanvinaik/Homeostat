"""Intent tests for the §13.3 derivation pieces and the preregistered
evaluation function, on synthetic structures (no real data required)."""

from homeostat.bridge import (
    components,
    connectors,
    evaluate_preregistered,
    map_loci_to_genes,
    shortest_dist,
)


def _adj(*edges):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


def test_map_loci_scores_by_max_priority_within_flank():
    envelopes = {"GENEA": ("1", 1000, 2000), "GENEB": ("1", 50_000, 60_000)}
    loci = [("1", 2010, 0.5), ("1", 1500, 0.9), ("1", 40_000, 0.3)]
    scores = map_loci_to_genes(loci, envelopes, flank=100)
    assert scores == {"GENEA": 0.9}  # 2010 within flank; 40k not; max wins
    scores_wide = map_loci_to_genes(loci, envelopes, flank=15_000)
    assert scores_wide["GENEB"] == 0.3


def test_components_and_connector_bridge_shape():
    # Two clusters {A,B} and {C,D}; X (outside G) bridges them — §5.7 shape.
    adj = _adj(("A", "B"), ("C", "D"), ("A", "X"), ("X", "C"))
    in_g = {"A", "B", "C", "D"}
    comps = components(in_g, adj)
    assert sorted(len(c) for c in comps) == [2, 2]
    top = connectors(comps, adj, in_g, {g: 1.0 for g in in_g})
    assert top[0]["gene"] == "X"
    assert top[0]["components_joined"] == 2


def test_shortest_dist_respects_node_subset():
    adj = _adj(("A", "B"), ("B", "C"), ("A", "C"))
    assert shortest_dist(adj, {"A", "B", "C"}, "A", "C") == 1
    assert shortest_dist(adj, {"A", "B"}, "A", "C") is None


def test_evaluation_clause_a_via_path():
    adj = _adj(("LRRK2", "RIPK2"), ("RIPK2", "NOD2"))
    in_g = {"LRRK2", "NOD2", "RIPK2"}
    comps = components(in_g, adj)
    ev = evaluate_preregistered(in_g, comps, adj, [])
    assert ev["verdict"] == "PASS" and ev["clause_a"]


def test_evaluation_clause_b_connector_recovery():
    # NOD2 absent from G; RIPK2 recovered as a connector -> clause (b).
    ev = evaluate_preregistered(
        {"LRRK2", "OTHER"},
        [{"LRRK2"}, {"OTHER"}],
        {},
        [{"gene": "RIPK2", "components_joined": 2, "joined_score_sum": 1.0}],
    )
    assert ev["verdict"] == "PASS" and ev["clause_b"] and not ev["clause_a"]


def test_evaluation_not_evaluable_when_anchors_missing():
    ev = evaluate_preregistered({"OTHER"}, [{"OTHER"}], {}, [])
    assert ev["verdict"].startswith("NOT-EVALUABLE")


def test_evaluation_fail_when_present_but_disconnected():
    ev = evaluate_preregistered({"LRRK2", "NOD2"}, [{"LRRK2"}, {"NOD2"}], {}, [])
    assert ev["verdict"] == "FAIL"
