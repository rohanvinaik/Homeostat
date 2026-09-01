"""Intent tests for the L2 event layer — authored from the design (SYSTEM_DESIGN.md §10), not
generated. A network's signed vote is an event; the cross-network resolution draws a coupling only
on convergent, uncontradicted support; direction is earned only from a directed network."""

from homeostat.event import Event, couple_verdict, events_to_web

# ---- the pure cross-network resolution -------------------------------------------


def test_couple_verdict_all_codes():
    assert couple_verdict(2, 0) == "coupling"  # convergent support, uncontradicted
    assert couple_verdict(2, 1) == "killed"  # contradiction across networks = near-miss
    assert couple_verdict(0, 1) == "censor"  # ruled out, none asserting
    assert couple_verdict(0, 0) == "abstain"  # informational zero


def test_couple_verdict_single_support_is_a_coupling():
    assert couple_verdict(1, 0) == "coupling"  # one witness is enough to draw (weak, but drawn)


# ---- the compiler ----------------------------------------------------------------


def _reg(subject, target, sign=1):
    return Event("regulatory", "amplify", subject, target, sign)


def _evo(subject, target, sign=1):
    return Event("evolutionary", "cotravel", subject, target, sign)


DIRECTED = {"regulatory"}  # the directed-mechanism network(s) — passed as data, not baked in


def test_convergent_support_draws_a_weighted_coupling():
    web = events_to_web([_reg("A", "B"), _evo("A", "B")], DIRECTED)
    assert len(web.couplings) == 1
    c = web.couplings[0]
    assert (c.a, c.b) == ("A", "B") and c.weight == 2.0  # weight = convergence count


def test_direction_is_earned_only_from_a_directed_network():
    # regulatory (directed) supports -> +1; evolutionary alone -> undirected 0.
    directed = events_to_web([_reg("A", "B")], DIRECTED).couplings[0]
    assert directed.direction == 1
    undirected = events_to_web([_evo("A", "B")], DIRECTED).couplings[0]
    assert undirected.direction == 0


def test_cross_network_contradiction_drops_the_coupling():
    # one network asserts, another censors the same coupling -> killed -> not drawn.
    web = events_to_web([_reg("A", "B", 1), _evo("A", "B", -1)], DIRECTED)
    assert web.couplings == ()


def test_censor_only_and_abstain_draw_nothing():
    censor = events_to_web([_evo("A", "B", -1)], DIRECTED)
    assert censor.couplings == ()
    abstain = events_to_web([_evo("A", "B", 0)], DIRECTED)
    assert abstain.couplings == ()


def test_events_group_by_coupling_and_are_deterministic():
    evs = [_reg("C", "D"), _reg("A", "B"), _evo("A", "B")]
    web = events_to_web(evs, DIRECTED)
    # sorted by (subject, target): (A,B) before (C,D)
    assert [(c.a, c.b) for c in web.couplings] == [("A", "B"), ("C", "D")]
