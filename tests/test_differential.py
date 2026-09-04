"""Intent tests for the structured differential (GDiff-ported): a deviation read against a reference
DISTRIBUTION (center + spread), carrying typed `kind` and information-content `surprise`.
Paired with the Detective characterization under tests/detective/ per the two-step discipline.

Note: mine_spread's cases are in SEPARATE tests on purpose. A guard-inversion mutant makes
mine_spread([]) crash (median of empty); if the empty-case assertion preceded a value assertion in
one test, the crash would shadow it -- a crash-kill, not a value-kill (NEGATIVE_SPECIFICATION
Def. 1.4). Isolating each case lets the value assertions pin the return value cleanly.
"""

from homeostat.differential import (
    DEPLETED,
    ELEVATED,
    NONE,
    Differential,
    differential_kind,
    make_differential,
    mine_spread,
    surprise,
)


def test_mine_spread_single_value_has_zero_dispersion():
    assert mine_spread([5.0]) == 0.0  # a single reading has zero dispersion (standalone value-pin)


def test_mine_spread_is_the_median_absolute_deviation():
    # center = median([1,2,3,4,5]) = 3; abs devs = [2,1,0,1,2]; MAD = median = 1.0
    assert mine_spread([1.0, 2.0, 3.0, 4.0, 5.0]) == 1.0
    assert mine_spread([None, 2.0, None, 4.0]) == 1.0  # None-filtered: center 3, MAD 1


def test_mine_spread_none_when_nothing_present():
    assert mine_spread([]) is None  # nothing present -> no reference dispersion
    assert mine_spread([None, None]) is None  # all-None -> nothing present


def test_surprise_is_the_standardized_departure():
    assert surprise(90.0, 60.0, 10.0) == 3.0  # 30 units, 3 spreads into the tail
    assert surprise(60.0, 60.0, 10.0) == 0.0  # at the center -> no surprise
    # abstentions -> informational zero, never a division blow-up
    assert surprise(None, 60.0, 10.0) == 0.0
    assert surprise(90.0, None, 10.0) == 0.0
    assert surprise(90.0, 60.0, None) == 0.0
    assert surprise(90.0, 60.0, 0.0) == 0.0  # degenerate reference: no surprise SCALE


def test_differential_kind_is_typed_by_spread_units():
    assert differential_kind(90.0, 60.0, 10.0, k=2.0) == ELEVATED  # 30 > 2*10
    assert differential_kind(30.0, 60.0, 10.0, k=2.0) == DEPLETED  # -30 < -2*10
    assert differential_kind(65.0, 60.0, 10.0, k=2.0) == NONE  # within the band
    assert differential_kind(None, 60.0, 10.0, k=2.0) == NONE  # abstention
    assert differential_kind(90.0, 60.0, 0.0, k=2.0) == NONE  # degenerate reference


def test_make_differential_composes_kind_surprise_and_spread():
    assert make_differential(90.0, 60.0, 10.0, 2.0) == Differential(ELEVATED, 3.0, 10.0)
    assert make_differential(30.0, 60.0, 10.0, 2.0) == Differential(DEPLETED, 3.0, 10.0)
    # abstention: informational zero, but the spread it was read against is still carried
    assert make_differential(None, 60.0, 10.0, 2.0) == Differential(NONE, 0.0, 10.0)
