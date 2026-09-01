"""Intent tests for the σ-trajectory search core — authored from the design, not generated."""

from homeostat.search import (
    eliminate_to_survivor,
    entropy_bits,
    falsifiable,
    knee_index,
    marginal_kill,
    resolved,
    sigma_trajectory,
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


def test_marginal_kill_counts_new_only():
    assert marginal_kill(["a", "b"], []) == 2
    assert marginal_kill(["a", "b"], ["a"]) == 1
    assert marginal_kill(["a", "a"], []) == 1  # dedup within the kill-set
    assert marginal_kill([], ["a"]) == 0


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


# ---- the trajectory orchestrator -------------------------------------------------


def test_trajectory_resolves_and_is_falsifiable():
    t = sigma_trajectory(["a", "b", "c"], {"k1": ["b"], "k2": ["c"]}, "a")
    assert t.sigma == 2
    assert t.survivors_left == ["a"]
    assert t.falsifiable is True
    assert [s.constraint for s in t.steps] == ["k1", "k2"]


def test_trajectory_bulk_then_tail():
    t = sigma_trajectory(["a", "b", "c", "d"], {"k1": ["b", "c"], "k2": ["d"]}, "a")
    assert t.sigma == 2
    assert [s.kappa for s in t.steps] == [2, 1]  # bulk then tail
    assert knee_index([s.kappa for s in t.steps]) == 1


def test_trajectory_stuck_needs_node_birth():
    # The only constraint would kill the target -> inadmissible -> STUCK (residual for node birth).
    t = sigma_trajectory(["a", "b"], {"k1": ["a"]}, "a")
    assert t.sigma is None
    assert t.survivors_left == ["a", "b"]
    assert t.falsifiable is False


def test_trajectory_no_plurality_is_not_falsifiable():
    t = sigma_trajectory(["a"], {}, "a")
    assert t.sigma == 0
    assert t.falsifiable is False  # resolving nothing is not a real resolution


# ---- the seedless (eliminate-to-survivor) trajectory -----------------------------


def test_survivors_killed_counts_current_survivors():
    assert survivors_killed(["b", "c"], ["a", "b", "c"]) == 2
    assert survivors_killed(["b"], ["a", "b", "c"]) == 1
    assert survivors_killed(["x"], ["a", "b"]) == 0  # not among the living -> kills nothing
    assert (
        survivors_killed(["a", "b"], ["a", "b"]) == 2
    )  # would empty (admissibility is the caller's)


def test_eliminate_resolves_to_the_survivor_not_a_target():
    # No target is protected: a and b are eliminated, so c EMERGES as the mechanism.
    t = eliminate_to_survivor(["a", "b", "c"], {"k1": ["a"], "k2": ["b"]})
    assert t.sigma == 2
    assert t.survivors_left == ["c"]
    assert t.falsifiable is True


def test_eliminate_bulk_then_tail():
    t = eliminate_to_survivor(["a", "b", "c", "d"], {"k1": ["b", "c"], "k2": ["d"]})
    assert t.sigma == 2
    assert [s.kappa for s in t.steps] == [2, 1]  # bulk (kills a cluster) then tail
    assert knee_index([s.kappa for s in t.steps]) == 1


def test_eliminate_never_empties_the_set():
    # A constraint that would kill ALL survivors is an over-constraint -> inadmissible -> STUCK.
    t = eliminate_to_survivor(["a", "b"], {"k1": ["a", "b"]})
    assert t.sigma is None
    assert t.survivors_left == ["a", "b"]
    assert t.falsifiable is False


def test_eliminate_plural_residual_needs_node_birth():
    # A κ=0 constraint (kills no survivor) resolves nothing -> STUCK plural residual (σ_sem>0).
    t = eliminate_to_survivor(["a", "b"], {"k1": ["x"]})
    assert t.sigma is None
    assert t.survivors_left == ["a", "b"]


def test_eliminate_single_candidate_is_not_falsifiable():
    t = eliminate_to_survivor(["a"], {})
    assert t.sigma == 0  # trivially "resolved" in zero steps
    assert t.falsifiable is False  # no plurality to resolve -> not a real finding
