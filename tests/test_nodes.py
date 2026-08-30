"""Intent tests for node birth/death/consolidation — authored from the design, not generated."""

from homeostat.nodes import (
    BORN,
    CANDIDATE,
    DEAD,
    OSCILLATING,
    Node,
    born,
    consolidate,
    next_counts,
    node_status,
    observe,
    oscillating,
    specialization_guard,
)

# ---- pure decisions --------------------------------------------------------------


def test_node_status_births_on_uncontradicted_recurrence():
    assert node_status(3, 0, 2) == BORN
    assert node_status(2, 0, 2) == BORN  # support == recur_min


def test_node_status_candidate_below_threshold():
    assert node_status(1, 0, 2) == CANDIDATE


def test_node_status_dead_when_only_contradicted():
    assert node_status(0, 2, 2) == DEAD  # a pure near-miss, never confirmed


def test_node_status_oscillates_when_both():
    assert node_status(2, 1, 2) == OSCILLATING  # over-general outranks birth


def test_node_status_no_birth_from_zero_evidence():
    # Even at recur_min == 0, a node with no support does not spontaneously fire.
    assert node_status(0, 0, 0) == CANDIDATE


def test_next_counts_accrual():
    assert next_counts(1, 0, True) == (2, 0)  # confirmation raises support
    assert next_counts(1, 0, False) == (1, 1)  # contradiction raises contradictions
    assert next_counts(0, 0, True) == (1, 0)


def test_specialization_guard_finds_discriminator():
    # 'a' is in every confirming instance and no contradicting one -> a usable guard.
    assert specialization_guard([["a", "x"], ["a", "y"]], [["b"]]) == ["a"]


def test_specialization_guard_none_when_shared_with_contradicting():
    # 'a' is common to confirming but also present in a contradicting instance -> no guard.
    assert specialization_guard([["a"], ["a"]], [["a"]]) == []


def test_specialization_guard_empty_confirming():
    assert specialization_guard([], [["a"]]) == []


def test_specialization_guard_no_contradicting_keeps_all_common():
    assert specialization_guard([["a", "b"], ["a", "b"]], []) == ["a", "b"]


# ---- node + lifecycle operators --------------------------------------------------


def test_node_status_method():
    assert Node("n1").status(2) == CANDIDATE
    assert Node("n1", support=2).status(2) == BORN


def test_observe_is_non_mutating_accrual():
    n = Node("n1")
    assert observe(n, True) == Node("n1", support=1, contradictions=0)
    assert observe(Node("n1", 1, 0), False) == Node("n1", support=1, contradictions=1)
    assert n == Node("n1")  # original untouched


def test_born_filters_firing_nodes():
    assert born([Node("a", 2, 0), Node("b", 1, 0)], 2) == [Node("a", 2, 0)]


def test_oscillating_filters_over_general():
    assert oscillating([Node("a", 1, 1), Node("b", 2, 0)], 2) == [Node("a", 1, 1)]


def test_consolidate_drops_dead_keeps_rest():
    nodes = [Node("a", 0, 1), Node("b", 2, 0)]  # a is DEAD, b is BORN
    assert consolidate(nodes, 2) == [Node("b", 2, 0)]
