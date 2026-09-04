"""Intent tests for the operator-injected hypothesis (incr.3 — fluid intelligence, tested).
Authored from the design; `edge_outcome` is Detective-pinned."""

from homeostat.event import Event
from homeostat.operator import HypothesisOutcome, edge_outcome, operator_ledger


def _reg(verb, s, t):
    return Event("regulatory", verb, s, t, 1)


# ---- edge_outcome: judge one hypothesis edge against the shadow ----------------------


def test_edge_outcome_unobserved_endpoint_is_standing():
    assert edge_outcome(0, 1, 1) == "standing"  # subject unobserved
    assert edge_outcome(1, 0, 1) == "standing"  # target unobserved


def test_edge_outcome_amplify_same_direction_is_confirmed():
    # A up, B up, amplify (+1): perturbing A up drives B up -> the shadow agrees.
    assert edge_outcome(1, 1, 1) == "confirmed"


def test_edge_outcome_inhibit_opposite_direction_is_confirmed():
    # A up, B down, inhibit (-1): perturbing A up drives B DOWN -> confirmed.
    assert edge_outcome(1, -1, -1) == "confirmed"


def test_edge_outcome_amplify_opposite_direction_is_contradicted():
    # A up but B down under amplify (+1): the edge predicts B up -> contradicted.
    assert edge_outcome(1, -1, 1) == "contradicted"


def test_edge_outcome_inhibit_same_direction_is_contradicted():
    # A up, B up under inhibit (-1): the edge predicts B down -> contradicted.
    assert edge_outcome(1, 1, -1) == "contradicted"


# ---- operator_ledger: judge the whole hypothesis set ---------------------------------


def test_operator_ledger_classifies_each_proposal():
    edges = [
        _reg("amplifies", "A", "B"),  # A up, B up -> confirmed
        _reg("amplifies", "C", "D"),  # C up, D down -> contradicted
        _reg("amplifies", "E", "Z"),  # Z unobserved -> standing
        _reg("binds", "F", "G"),  # non-regulatory verb -> standing (untestable)
    ]
    observed = {"A": 1, "B": 1, "C": 1, "D": -1, "E": 1, "F": 1, "G": 1}
    ledger = operator_ledger(edges, observed, {"amplifies": 1, "inhibits": -1})
    assert ledger == [
        HypothesisOutcome("A", "amplifies", "B", "confirmed"),
        HypothesisOutcome("C", "amplifies", "D", "contradicted"),
        HypothesisOutcome("E", "amplifies", "Z", "standing"),
        HypothesisOutcome("F", "binds", "G", "standing"),
    ]
