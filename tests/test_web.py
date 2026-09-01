"""Intent tests for the constraint object — the weighted relational web + its bridge to the engine.
Authored from the design (THEORY_OF_THE_CASE Part II), not generated."""

from homeostat.search import eliminate_two_sign
from homeostat.web import (
    Coupling,
    RelationalWeb,
    kill_matrix,
    nodes,
    reaches,
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
