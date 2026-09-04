"""Intent tests for the constraint object — the weighted relational web + its bridge to the engine.
Authored from the design (THEORY_OF_THE_CASE Part II), not generated."""

from homeostat.search import eliminate_two_sign
from homeostat.web import (
    Coupling,
    RelationalWeb,
    ancestor_cone,
    distances_to,
    induced_subweb,
    kill_matrix,
    node_convergence,
    nodes,
    reachers,
    reaches,
    reverse_adjacency,
    web_adjacency,
)

# ---- the web + its pure pieces ---------------------------------------------------


def test_nodes_are_the_bounded_universe():
    web = RelationalWeb((Coupling("a", "b", 1.0, +1), Coupling("b", "c", 1.0, +1)))
    assert nodes(web) == ["a", "b", "c"]  # sorted, unique — the candidate universe


def test_web_adjacency_honours_ternary_direction():
    web = RelationalWeb(
        (
            Coupling("a", "b", 1.0, +1),  # a→b only
            Coupling("c", "d", 1.0, -1),  # d→c only
            Coupling("e", "f", 1.0, 0),  # both ways
        )
    )
    adj = web_adjacency(web)
    assert adj["a"] == ["b"] and adj["b"] == []  # directed forward
    assert adj["d"] == ["c"] and adj["c"] == []  # directed backward
    assert adj["e"] == ["f"] and adj["f"] == ["e"]  # undirected → both legs


def test_web_adjacency_min_weight_floors_weak_couplings():
    web = RelationalWeb((Coupling("a", "b", 0.2, +1), Coupling("a", "c", 0.9, +1)))
    adj = web_adjacency(web, min_weight=0.5)
    assert adj["a"] == ["c"]  # the 0.2 coupling is below the floor -> no path


def test_reaches_self_and_transitive_and_none():
    adj = {"a": ["b"], "b": ["c"], "c": []}
    assert reaches(adj, "a", "a") is True  # a symptom can be its own source
    assert reaches(adj, "a", "c") is True  # transitive
    assert reaches(adj, "c", "a") is False  # no path back (directed)


# ---- the bridge to the engine ----------------------------------------------------


def test_kill_matrix_kills_sources_that_cannot_reach_a_symptom():
    # source→A, source→B, decoy→A. Only `source` reaches both symptoms.
    web = RelationalWeb(
        (
            Coupling("source", "A", 1.0, +1),
            Coupling("source", "B", 1.0, +1),
            Coupling("decoy", "A", 1.0, +1),
        )
    )
    cands, cons = kill_matrix(web, ["A", "B"])
    assert cands == ["A", "B", "decoy", "source"]
    assert cons["explains:A"] == ["B"]  # only B cannot reach A
    assert cons["explains:B"] == ["A", "decoy"]  # A and decoy cannot reach B


def test_end_to_end_directed_web_recovers_the_unique_source():
    # The load-bearing integration: web -> kill_matrix -> the REAL engine -> the source.
    web = RelationalWeb(
        (
            Coupling("source", "A", 1.0, +1),
            Coupling("source", "B", 1.0, +1),
            Coupling("decoy", "A", 1.0, +1),
        )
    )
    cands, cons = kill_matrix(web, ["A", "B"])
    traj = eliminate_two_sign(cands, cons, {})
    assert traj.sigma is not None  # resolved to a unique survivor
    assert traj.survivors_left == ["source"]  # the one source that propagates to every symptom


def test_undirected_web_stays_plural_where_directed_would_collapse():
    # Same shape but UNDIRECTED: with both-way flow, A itself reaches source→B, so several nodes
    # explain both symptoms -> genuine σ_sem>0 plurality -> STUCK (the Jeeves selector's cue).
    web = RelationalWeb(
        (
            Coupling("source", "A", 1.0, 0),
            Coupling("source", "B", 1.0, 0),
            Coupling("decoy", "A", 1.0, 0),
        )
    )
    cands, cons = kill_matrix(web, ["A", "B"])
    traj = eliminate_two_sign(cands, cons, {})
    assert traj.sigma is None and traj.bottom is False  # plural, not resolved, not ⊥
    assert len(traj.survivors_left) > 1  # undirected can't pin which node is the source


def test_single_symptom_is_degenerate():
    # One symptom, many sources reach it -> no plurality resolved -> not a real finding.
    web = RelationalWeb((Coupling("source", "A", 1.0, +1), Coupling("decoy", "A", 1.0, +1)))
    cands, cons = kill_matrix(web, ["A"])
    traj = eliminate_two_sign(cands, cons, {})
    assert traj.sigma is None  # a lone symptom does not pin a mechanism (stays plural)


# ---- relevance = the computed ancestor cone (scoping) -----------------------------


def test_reverse_adjacency_flips_each_carrying_edge():
    web = RelationalWeb((Coupling("a", "b", 1.0, +1), Coupling("c", "d", 1.0, 0)))
    radj = reverse_adjacency(web)
    assert radj["b"] == ["a"] and radj["a"] == []  # b's upstream is a; a has none
    assert radj["c"] == ["d"] and radj["d"] == ["c"]  # undirected -> both upstream


def test_reachers_is_the_ancestor_cone_including_self():
    radj = {"A": ["source", "decoy"], "source": [], "decoy": [], "B": ["source"]}
    assert reachers(radj, "A") == {"A", "source", "decoy"}  # includes A itself
    assert reachers(radj, "source") == {"source"}  # a root reaches only itself upstream


def test_ancestor_cone_is_the_union_over_observed_excluding_the_irrelevant():
    web = RelationalWeb(
        (
            Coupling("source", "A", 1.0, +1),
            Coupling("source", "B", 1.0, +1),
            Coupling("decoy", "A", 1.0, +1),
            Coupling("unrelated", "X", 1.0, +1),  # reaches neither A nor B
        )
    )
    # ancestors of A: {A, source, decoy}; of B: {B, source}; union sorted; X/unrelated excluded.
    assert ancestor_cone(web, ["A", "B"]) == ["A", "B", "decoy", "source"]


def test_induced_subweb_keeps_only_both_endpoint_couplings():
    web = RelationalWeb((Coupling("source", "A", 1.0, +1), Coupling("unrelated", "X", 1.0, +1)))
    sub = induced_subweb(web, {"source", "A"})
    assert sub.couplings == (Coupling("source", "A", 1.0, +1),)  # unrelated->X dropped


def test_scoping_to_the_cone_preserves_the_survivor():
    # The load-bearing property: the read on the cone-subweb recovers the SAME source as the full
    # web, over a smaller candidate universe -- provably lossless, and the irrelevant never enters.
    web = RelationalWeb(
        (
            Coupling("source", "A", 1.0, +1),
            Coupling("source", "B", 1.0, +1),
            Coupling("decoy", "A", 1.0, +1),
            Coupling("unrelated", "X", 1.0, +1),  # noise the cone must strip
        )
    )
    sub = induced_subweb(web, ancestor_cone(web, ["A", "B"]))
    cands, cons = kill_matrix(sub, ["A", "B"])
    traj = eliminate_two_sign(cands, cons, {})
    assert traj.survivors_left == ["source"]  # same survivor as the full-web read
    assert "unrelated" not in cands and "X" not in cands  # the irrelevant never entered


def test_node_convergence_is_mean_coupling_weight():
    web = RelationalWeb(
        (Coupling("A", "B", 3.0, 1), Coupling("A", "C", 1.0, 1), Coupling("B", "C", 2.0, 0))
    )
    # A: (A,B)=3,(A,C)=1 -> 2.0 ; B: (A,B)=3,(B,C)=2 -> 2.5 ; C: (A,C)=1,(B,C)=2 -> 1.5  (mean)
    assert node_convergence(web) == {"A": 2.0, "B": 2.5, "C": 1.5}


def test_distances_to_is_shortest_reverse_bfs():
    # forward a->b->c and a->c : reverse from c -> a is 1 (direct a->c beats a->b->c), b is 1.
    radj = {"c": ["b", "a"], "b": ["a"], "a": []}
    assert distances_to(radj, "c") == {"c": 0, "b": 1, "a": 1}


def test_distances_to_reaches_multi_hop_via_the_queue():
    # a->b->c chain: a is TWO hops from c, so BFS must enqueue b to reach a. (Kills append->pass.)
    radj = {"c": ["b"], "b": ["a"], "a": []}
    assert distances_to(radj, "c") == {"c": 0, "b": 1, "a": 2}
