"""Intent tests for the polarity-opposition censor — the native second sign from the directed web +
deviation signs. Authored from the biochemistry (persuade-first, conservative), not generated."""

import pytest

from homeostat.event import Event
from homeostat.polarity import net_polarities, polarity_censors, signed_adjacency

VS = {"amplifies": 1, "inhibits": -1}  # the regulatory-verb -> polarity map (driver-supplied)


def _ev(verb, subj, tgt, sign=1):
    return Event("regulatory", verb, subj, tgt, sign)


def test_signed_adjacency_maps_verb_to_polarity():
    adj = signed_adjacency([_ev("amplifies", "A", "B"), _ev("inhibits", "B", "C")], VS)
    assert adj == {"A": [("B", 1)], "B": [("C", -1)]}


def test_signed_adjacency_drops_the_sign_ambiguous_edge():
    # two events on A->B disagree on polarity -> no definite sign -> dropped
    adj = signed_adjacency([_ev("amplifies", "A", "B"), _ev("inhibits", "A", "B")], VS)
    assert adj == {}


def test_signed_adjacency_ignores_nonregulatory_and_censor_events():
    adj = signed_adjacency([_ev("binds", "A", "B"), _ev("amplifies", "C", "D", sign=-1)], VS)
    assert adj == {}  # 'binds' not in verb_sign; the sign<0 event is not a supported edge


def test_signed_adjacency_ignores_abstain_events():
    # a sign=0 (abstain / informational zero) event asserts nothing -> no signed edge is drawn.
    assert signed_adjacency([_ev("amplifies", "A", "B", sign=0)], VS) == {}


def test_signed_adjacency_neighbour_lists_are_sorted():
    # two targets of A inserted C-before-B -> the neighbour list is SORTED (documented determinism).
    adj = signed_adjacency([_ev("amplifies", "A", "C"), _ev("amplifies", "A", "B")], VS)
    assert adj == {"A": [("B", 1), ("C", 1)]}


def test_net_polarities_multiplies_signs_along_the_path():
    adj = {"A": [("B", 1)], "B": [("C", -1)]}
    # A->A identity +1; A->B +1; A->C = +1 * -1 = -1
    assert net_polarities(adj, "A") == {"A": 1, "B": 1, "C": -1}


def test_net_polarities_propagates_to_every_neighbour():
    # source fans out to two direct targets: both reached, each at its edge sign
    assert net_polarities({"A": [("B", 1), ("C", 1)]}, "A") == {"A": 1, "B": 1, "C": 1}


def test_net_polarities_omits_the_sign_ambiguous_node():
    # D reachable A->B->D (+*+ = +) and A->C->D (+*- = -) -> sign-ambiguous -> omitted
    adj = {"A": [("B", 1), ("C", 1)], "B": [("D", 1)], "C": [("D", -1)]}
    pols = net_polarities(adj, "A")
    assert pols["A"] == 1
    assert pols["B"] == 1
    assert pols["C"] == 1
    assert "D" not in pols  # conflicting net sign -> never guessed


def test_net_polarities_ambiguity_propagates_transitively():
    # D is sign-ambiguous, but its second sign arrives (via C->X->D) only AFTER D is first processed
    # -- so its ambiguity reaches descendant E only if the grow-branch RE-ENQUEUES D. E must be
    # omitted. (Kills `queue.append(m) -> pass`: without the re-enqueue, E stays a false +1.)
    adj = {
        "A": [("B", 1), ("C", 1)],
        "B": [("D", 1)],
        "C": [("X", 1)],
        "X": [("D", -1)],
        "D": [("E", 1)],
    }
    pols = net_polarities(adj, "A")
    assert pols == {"A": 1, "B": 1, "C": 1, "X": 1}  # only the sign-definite nodes
    assert "D" not in pols
    assert "E" not in pols


def test_net_polarities_terminates_on_a_positive_feedback_loop():
    # A<->B, both +: a feedback loop. The `not (new <= sset[m])` guard stops re-enqueuing once a set
    # is saturated, so it TERMINATES with both definite +1. (The `not False`/`<` mutants hang here.)
    assert net_polarities({"A": [("B", 1)], "B": [("A", 1)]}, "A") == {"A": 1, "B": 1}


def test_net_polarities_negative_feedback_loop_saturates_to_ambiguous():
    # A->B(+), B->A(-): the loop makes both signs reachable at each node -> both saturate to {+1,-1}
    # -> both omitted (sign-ambiguous), and it still terminates.
    assert net_polarities({"A": [("B", 1)], "B": [("A", -1)]}, "A") == {}


def test_net_polarities_raises_on_non_dict_adjacency():
    # signed_adj must be a mapping; a non-dict fails at the FIRST access -- `signed_adj.get` -- so
    # the crash is specifically 'no attribute get' (pins the crash SITE, not just the type).
    with pytest.raises(AttributeError, match="attribute 'get'"):
        net_polarities(-1, "")  # type: ignore[arg-type]


def test_polarity_censor_fires_on_a_mechanistic_contradiction():
    # A amplifies B and C; observed B UP, C DOWN -> no single perturbation of A explains both.
    adj = {"A": [("B", 1), ("C", 1)]}
    assert polarity_censors(adj, ["A"], {"B": 1, "C": -1}) == ["A"]


def test_polarity_censor_accommodates_when_a_direction_fits():
    # A amplifies B, inhibits C; observed B UP and C DOWN -> A perturbed UP explains both -> saved.
    adj = {"A": [("B", 1), ("C", -1)]}
    assert polarity_censors(adj, ["A"], {"B": 1, "C": -1}) == []  # persuasion succeeds


def test_polarity_censor_is_conservative_on_a_single_reached_observed():
    # one reachable observed -> some direction always fits -> never censored (needs contradiction).
    adj = {"A": [("B", 1)]}
    assert polarity_censors(adj, ["A"], {"B": 1}) == []


def test_polarity_censor_respects_the_sources_own_observed_direction():
    # A observed UP but A must be DOWN to explain B (amplifies B, B observed DOWN) -> contradiction.
    # (Captured by the comprehension: x=A gives observed[A]*pols[A]=+1 alongside B's required -1.)
    adj = {"A": [("B", 1)]}
    assert polarity_censors(adj, ["A"], {"A": 1, "B": -1}) == ["A"]


def test_polarity_censor_ignores_observed_the_source_cannot_reach():
    # A reaches only B, not Z; Z (unreached, sign-ambiguous or absent) contributes nothing -> saved.
    assert polarity_censors({"A": [("B", 1)]}, ["A"], {"B": 1, "Z": -1}) == []


def test_polarity_censors_returns_sorted_for_determinism():
    # two candidates each hit the same contradiction; the censor list is sorted (engine-stable).
    adj = {"A": [("B", 1), ("C", 1)], "X": [("B", 1), ("C", 1)]}
    assert polarity_censors(adj, ["X", "A"], {"B": 1, "C": -1}) == ["A", "X"]
