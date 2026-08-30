"""Intent tests for the OTP ternary substrate — authored from the design, not generated."""

from homeostat.otp import OPPOSE, ORTHOGONAL, SUPPORT, ternary


def test_none_is_informational_zero():
    # No reading on this axis is honest abstention, never a fabricated 0-magnitude.
    assert ternary(None, 0.1) == ORTHOGONAL


def test_above_band_supports():
    assert ternary(0.5, 0.1) == SUPPORT


def test_below_band_opposes():
    assert ternary(-0.5, 0.1) == OPPOSE


def test_within_band_abstains():
    assert ternary(0.05, 0.1) == ORTHOGONAL
    assert ternary(-0.05, 0.1) == ORTHOGONAL


def test_band_edges_abstain():
    # At exactly +/- the band it is within tolerance -> abstain (strict inequality).
    assert ternary(0.1, 0.1) == ORTHOGONAL
    assert ternary(-0.1, 0.1) == ORTHOGONAL


def test_negative_tolerance_cannot_invert():
    # A negative tol is read as its magnitude; the band never flips.
    assert ternary(0.5, -0.1) == SUPPORT
    assert ternary(0.05, -0.1) == ORTHOGONAL
