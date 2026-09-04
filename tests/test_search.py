"""Intent tests for the σ-search primitives — authored from the design, not generated. The
orchestrator `eliminate_two_sign` is tested in test_two_sign.py; this file pins the pure toolkit."""

from homeostat.search import (
    coverage,
    covers_shadow,
    entropy_bits,
    falsifiable,
    knee_index,
    max_coverage_survivors,
    resolved,
    survivors,
    survivors_killed,
)

# ---- pure decisions --------------------------------------------------------------


def test_survivors_removes_killed_preserves_order():
    assert survivors(["a", "b", "c"], [["b"]]) == ["a", "c"]
    assert survivors(["a", "b"], []) == ["a", "b"]
    assert survivors(["a", "b", "c"], [["b"], ["c"]]) == ["a"]


def test_survivors_dedups_candidates():
    assert survivors(["a", "a", "b"], [["b"]]) == ["a"]


def test_entropy_bits():
    assert entropy_bits(1) == 0.0  # resolved -> zero entropy
    assert entropy_bits(0) == 0.0  # nothing coheres -> also zero (abstention, not resolution)
    assert entropy_bits(2) == 1.0
    assert entropy_bits(4) == 2.0


def test_resolved_only_at_one():
    assert resolved(1) is True
    assert resolved(0) is False  # abstention, not resolution
    assert resolved(2) is False


def test_falsifiable_guard():
    assert falsifiable(3, [2, 1]) is True  # plurality + every step killed a rival
    assert falsifiable(1, [1]) is False  # no plurality to resolve
    assert falsifiable(3, []) is False  # nothing was resolved
    assert falsifiable(3, [2, 0]) is False  # a confirming (κ=0) step -> self-confirming / SDIS


def test_knee_index_is_bulk_to_tail_transition():
    assert knee_index([3, 2, 1]) == 2  # first κ<=1 at index 2
    assert knee_index([1, 1]) == 0  # already in the tail
    assert knee_index([3, 2]) == 2  # stayed in the bulk -> len
    assert knee_index([]) == 0


def test_survivors_killed_counts_current_survivors():
    assert survivors_killed(["b", "c"], ["a", "b", "c"]) == 2
    assert survivors_killed(["b"], ["a", "b", "c"]) == 1
    assert survivors_killed(["x"], ["a", "b"]) == 0  # not among the living -> kills nothing
    assert survivors_killed(["a", "b"], ["a", "b"]) == 2  # would empty (caller's admissibility)


def test_covers_shadow_true_only_when_no_positive_constraint_kills():
    assert covers_shadow("x", [["a", "b"], ["c"]]) is True  # killed by none -> reaches all observed
    assert covers_shadow("x", []) is True  # no constraints -> vacuously covers
    assert covers_shadow("x", [["a"], ["x", "c"]]) is False  # killed by one -> misses an observed


def test_max_coverage_survivors_returns_the_best_partial_covers():
    # kill-sets {b}, {b,c}: coverage a=2, b=0, c=1 -> the argmax is [a]
    assert max_coverage_survivors(["a", "b", "c"], [["b"], ["b", "c"]]) == ["a"]


def test_max_coverage_survivors_ties_preserve_order_and_dedup():
    # a and d each covered by both constraints (killed by neither) -> both returned, order kept
    assert max_coverage_survivors(["a", "d", "a"], [["b"], ["c"]]) == ["a", "d"]


def test_max_coverage_survivors_empty_candidates_is_empty():
    assert max_coverage_survivors([], [["a"]]) == []


def test_coverage_counts_constraints_the_candidate_satisfies():
    assert coverage("x", [["a"], ["b"]]) == 2  # x in neither kill-set -> reaches both observed
    assert coverage("x", [["x"], ["b"]]) == 1  # killed by the first -> reaches one
    assert coverage("x", [["x"], ["x", "b"]]) == 0  # killed by both -> reaches none
    assert coverage("x", []) == 0  # no constraints -> covers nothing
