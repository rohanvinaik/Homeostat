"""Intent tests for the per-person OTP positioning layer — authored from the design
(SYSTEM_DESIGN.md §9, the Peitho Discrimination Guarantee), not generated."""

from homeostat.otp import OPPOSE, ORTHOGONAL, SUPPORT
from homeostat.position import (
    Position,
    deviation,
    discriminates,
    hamming,
    mine_zero,
    position,
    signature,
)

# ---- pure decisions --------------------------------------------------------------


def test_deviation_signed_off_baseline():
    assert deviation(72.0, 60.0) == 12.0  # above baseline
    assert deviation(50.0, 60.0) == -10.0  # below baseline


def test_deviation_abstains_without_reading_or_baseline():
    assert deviation(None, 60.0) is None  # no reading -> informational zero
    assert deviation(72.0, None) is None  # no baseline -> informational zero
    assert deviation(None, None) is None


def test_mine_zero_is_median_of_present_values():
    assert mine_zero([60.0, 62.0, 64.0]) == 62.0  # odd -> middle
    assert mine_zero([60.0, 64.0]) == 62.0  # even -> mean of middles
    assert mine_zero([60.0, None, 64.0, None]) == 62.0  # None peers dropped


def test_mine_zero_none_when_nothing_present():
    assert mine_zero([]) is None
    assert mine_zero([None, None]) is None  # no peer readings -> no baseline


def test_hamming_counts_differing_dimensions():
    assert hamming((1, 0, -1), (1, 0, -1)) == 0  # identical
    assert hamming((1, 0, -1), (1, 1, -1)) == 1  # one differs
    assert hamming((1, 0), (1, 0, -1)) == 1  # length mismatch counts the extra dim


def test_discriminates_is_the_structural_break_test():
    assert discriminates((1, 0, -1), (1, 1, -1)) is True  # different positions
    assert discriminates((1, 0, -1), (1, 0, -1)) is False  # same signature = a structural break


# ---- the positioning composition -------------------------------------------------


def test_position_projects_signed_ternary_off_the_mined_zero():
    assert position("hr", 90.0, 60.0, tol=5.0) == Position("hr", SUPPORT, 30.0, 60.0)  # well above
    assert position("hr", 40.0, 60.0, tol=5.0) == Position("hr", OPPOSE, 20.0, 60.0)  # well below
    assert position("hr", 62.0, 60.0, tol=5.0).sign == ORTHOGONAL  # within band -> abstain
    assert position("hr", 62.0, 60.0, tol=5.0).depth == 2.0  # depth kept when the sign abstains


def test_position_abstains_with_no_reading_or_no_baseline():
    p = position("hr", None, 60.0, tol=5.0)
    assert p.sign == ORTHOGONAL
    assert p.depth == 0.0
    q = position("hr", 90.0, None, tol=5.0)
    assert q.sign == ORTHOGONAL
    assert q.depth == 0.0


def test_signature_is_signs_in_sorted_dimension_order():
    positions = {
        "fatigue": Position("fatigue", SUPPORT, 3.0, 0.0),
        "allergy": Position("allergy", OPPOSE, 1.0, 0.0),
        "hr": Position("hr", ORTHOGONAL, 0.0, 60.0),
    }
    # sorted dims: allergy, fatigue, hr -> (-1, +1, 0)
    assert signature(positions) == (OPPOSE, SUPPORT, ORTHOGONAL)
