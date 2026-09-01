"""Intent tests for the TWO-SIGN elimination — authored from the design (NEGATIVE_SPECIFICATION,
SYSTEM_DESIGN.md LAW 3b), not generated. The positive sign eliminates to a survivor; the negative
sign (censors) may empty the set, and an emptied set is the certified ⊥ (a proof of non-membership),
never a failed search."""

from homeostat.search import constraint_disposition, eliminate_two_sign

# ---- the pure two-sign decision --------------------------------------------------


def test_constraint_disposition_inert_when_kills_nothing():
    assert constraint_disposition(0, 3, is_censor=False) == "inert"  # positive confirms nothing
    assert constraint_disposition(0, 3, is_censor=True) == "inert"  # censor rules nothing out
    assert constraint_disposition(-1, 3, is_censor=True) == "inert"  # guard: negative κ


def test_constraint_disposition_partial_eliminate_either_sign():
    assert constraint_disposition(1, 3, is_censor=False) == "eliminate"
    assert constraint_disposition(2, 3, is_censor=True) == "eliminate"  # censor: partial eliminator


def test_constraint_disposition_the_sign_asymmetry_at_the_boundary():
    # κ == alive_count is the whole asymmetry: positive may not empty; censor emptying IS ⊥.
    assert constraint_disposition(3, 3, is_censor=False) == "inadmissible"  # positive may not empty
    assert constraint_disposition(3, 3, is_censor=True) == "bottom"  # censor emptying = certified ⊥
    assert constraint_disposition(5, 3, is_censor=True) == "bottom"  # over-covering still ⊥
    assert constraint_disposition(1, 1, is_censor=True) == "bottom"  # censor kills sole survivor


# ---- the two-sign engine ---------------------------------------------------------


def test_positive_only_resolves_like_the_one_sign_engine():
    # No censors → pure positive elimination to a unique survivor.
    cands = ["A", "B", "C"]
    cons = {"c1": ["B"], "c2": ["C"]}
    traj = eliminate_two_sign(cands, cons, {})
    assert traj.survivors_left == ["A"] and traj.sigma == 2
    assert traj.bottom is False and traj.falsifiable is True


def test_censor_certifies_bottom_when_it_rules_out_all_survivors():
    # A censor ruling out every candidate → certified ⊥ (no lawful mechanism, with proof).
    cands = ["A", "B"]
    traj = eliminate_two_sign(cands, {}, {"forbid": ["A", "B"]})
    assert traj.bottom is True
    assert traj.survivors_left == []
    assert traj.sigma is None  # ⊥ is not a resolution


def test_censor_rules_out_the_sole_survivor_is_bottom_not_resolved():
    # Positive narrows {A,B,C} → {A}; then a censor rules out A → ⊥, NOT RESOLVED
    # (the ⊥ check must precede the resolved check).
    cands = ["A", "B", "C"]
    cons = {"c1": ["B"], "c2": ["C"]}
    traj = eliminate_two_sign(cands, cons, {"forbid_A": ["A"]})
    assert traj.bottom is True and traj.survivors_left == []


def test_treatment_response_censor_collapses_plurality_to_the_mechanism():
    # Crown-jewel scenario: positive leaves {drugX, decoy} plural; a treatment-response censor
    # rules out `decoy` (the drug resolved a symptom decoy cannot reach) → unique survivor.
    cands = ["drugX", "decoy", "other"]
    cons = {"explains:S": ["other"]}  # positive: `other` cannot explain symptom S
    censors = {"tx_response": ["decoy"]}  # negative: `decoy` ruled out by the treatment response
    traj = eliminate_two_sign(cands, cons, censors)
    assert traj.survivors_left == ["drugX"] and traj.sigma == 2
    assert traj.bottom is False and traj.falsifiable is True  # plurality + steps killed rivals


def test_stuck_plurality_when_no_admissible_constraint_separates():
    # Two survivors, no constraint of either sign can separate them without emptying → STUCK (the
    # discrimination selector's cue to add a new dimension), not ⊥ and not resolved.
    cands = ["A", "B"]
    traj = eliminate_two_sign(cands, {}, {})
    assert traj.sigma is None and traj.survivors_left == ["A", "B"]
    assert traj.bottom is False  # a plural residual is not a certified ⊥


def test_censor_as_partial_eliminator_competes_in_the_greedy_step():
    # A censor with 0 < κ < |alive| is a partial eliminator; here it removes one of three, and a
    # positive constraint finishes the resolution.
    cands = ["A", "B", "C"]
    cons = {"pos": ["C"]}
    censors = {"neg": ["B"]}
    traj = eliminate_two_sign(cands, cons, censors)
    assert traj.survivors_left == ["A"] and traj.bottom is False and traj.sigma == 2


# ---- positive-path behaviors (migrated from the retired eliminate_to_survivor) ---


def test_positive_bulk_then_tail_kappa_pattern():
    traj = eliminate_two_sign(["a", "b", "c", "d"], {"k1": ["b", "c"], "k2": ["d"]}, {})
    assert traj.sigma == 2
    assert [s.kappa for s in traj.steps] == [2, 1]  # bulk (kills a cluster) then tail


def test_positive_never_empties_the_set():
    # A positive constraint that would kill ALL survivors is inadmissible -> STUCK, never ⊥.
    traj = eliminate_two_sign(["a", "b"], {"k1": ["a", "b"]}, {})
    assert traj.sigma is None and traj.survivors_left == ["a", "b"]
    assert traj.bottom is False  # only a censor can certify ⊥


def test_kappa_zero_constraint_leaves_a_plural_residual():
    # A κ=0 constraint (kills no live survivor) resolves nothing -> STUCK plural (σ_sem>0).
    traj = eliminate_two_sign(["a", "b"], {"k1": ["x"]}, {})
    assert traj.sigma is None and traj.survivors_left == ["a", "b"]


def test_single_candidate_is_not_falsifiable():
    traj = eliminate_two_sign(["a"], {}, {})
    assert traj.sigma == 0  # trivially resolved in zero steps
    assert traj.falsifiable is False  # no plurality to resolve -> not a real finding
