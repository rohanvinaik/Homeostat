"""Intent tests for the marker placement core: `reference_center_spread` (a published interval ->
center + spread) and `place` (a full structured Position whose signed coordinate and differential
`kind` AGREE by construction). Paired with the Detective characterization per the two-step.
"""

from homeostat.differential import DEPLETED, ELEVATED, NONE
from homeostat.otp import OPPOSE, ORTHOGONAL, SUPPORT
from homeostat.position import place
from homeostat.producer import reference_center_spread
from homeostat.signal import Tier


def test_reference_center_spread_is_midpoint_and_half_width():
    assert reference_center_spread(70.0, 100.0) == (85.0, 15.0)
    assert reference_center_spread(0.0, 10.0) == (5.0, 5.0)


def test_place_sign_and_kind_agree_by_construction():
    # reference interval [70, 100] -> center 85, spread 15; k=1 -> the band is exactly [70, 100].
    c, s = reference_center_spread(70.0, 100.0)
    hi = place("glucose", 120.0, c, s, k=1.0)  # above the band
    assert hi.sign == SUPPORT and hi.differential.kind == ELEVATED
    lo = place("glucose", 50.0, c, s, k=1.0)  # below the band
    assert lo.sign == OPPOSE and lo.differential.kind == DEPLETED
    mid = place("glucose", 85.0, c, s, k=1.0)  # inside the band -> informational zero
    assert mid.sign == ORTHOGONAL and mid.differential.kind == NONE


def test_place_carries_the_tier_and_the_surprise():
    c, s = reference_center_spread(70.0, 100.0)
    p = place("glucose", 130.0, c, s, k=1.0, tier=Tier.REPORTED)
    assert p.tier is Tier.REPORTED
    assert p.differential.surprise == 3.0  # (130-85)/15 = 3 half-widths into the tail


def test_place_degenerate_reference_is_the_informational_zero():
    # a zero-spread (or None) reference cannot calibrate surprise -> abstain on BOTH channels.
    z = place("marker", 100.0, 50.0, 0.0, k=1.0)
    assert z.sign == ORTHOGONAL and z.differential.kind == NONE and z.differential.surprise == 0.0
    n = place("marker", 100.0, None, None, k=1.0)
    assert n.sign == ORTHOGONAL and n.differential.kind == NONE
