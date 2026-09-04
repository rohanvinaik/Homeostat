"""Intent tests for the coherence meter (SSL §9.3 — the NML/KT-calibrated coherence scalar).
Authored from the design; the pure decisions are Detective-pinned."""

from homeostat.meter import coherence_meter, nml_regret

# ---- coherence_meter: the calibrated net confirmation --------------------------------


def test_meter_empty_is_the_informational_zero():
    # no predictions -> no coherence axis -> 0.0 (the quest's ORTHOGONAL, not a low score).
    assert coherence_meter(0, 0, 0) == 0.0


def test_meter_all_confirmed_is_positive_and_small_sample_honest():
    # 2/2 confirmed scores BELOW 20/20 confirmed — the whole point of the NML calibration:
    # a raw confirmed/n would give 1.0 for both; the KT denominator penalizes the small sample.
    assert coherence_meter(2, 0, 0) == 2 / 3.5
    assert coherence_meter(20, 0, 0) == 20 / 21.5
    assert coherence_meter(2, 0, 0) < coherence_meter(20, 0, 0)


def test_meter_all_contradicted_is_negative():
    assert coherence_meter(0, 5, 0) == -5 / 6.5
    assert coherence_meter(0, 5, 0) < 0


def test_meter_balanced_confirm_contradict_is_zero():
    assert coherence_meter(5, 5, 0) == 0.0


def test_meter_contradiction_hurts_more_than_standing():
    # same confirmed count; 5 contradictions cancel to 0, but 5 standings only dilute -> stays > 0.
    assert coherence_meter(5, 0, 5) > coherence_meter(5, 5, 0)
    assert coherence_meter(5, 0, 5) == 5 / 11.5


def test_meter_standing_dilutes_toward_zero_never_subtracts():
    # standing grows n (dilutes) but the numerator is unchanged -> lower magnitude, same sign.
    assert coherence_meter(2, 0, 8) == 2 / 11.5
    assert 0 < coherence_meter(2, 0, 8) < coherence_meter(2, 0, 0)


# ---- nml_regret: the reported calibration cost ---------------------------------------


def test_nml_regret_is_zero_below_two_outcomes():
    assert nml_regret(0) == 0.0
    assert nml_regret(1) == 0.0


def test_nml_regret_is_log2_n_for_the_three_outcome_meter():
    # (m-1)/2 * log2(n) with m=3 -> log2(n): n=2 -> 1 bit, n=4 -> 2 bits.
    assert nml_regret(2) == 1.0
    assert nml_regret(4) == 2.0
