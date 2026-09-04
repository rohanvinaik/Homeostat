"""Intent tests for the DNA structural-mechanics kernel (axis 2): bendability and
the YR/RY rigid<->flexible phase balance, ported from GenomeVault's literature dinucleotide scales.
Paired with the Detective characterization per the two-step. None/edge cases are ISOLATED so a
crash-prone mutant on them cannot shadow the value assertions (the mine_spread lesson).
"""

from homeostat.biophysics import bendability, yr_ry_balance


def test_bendability_is_mean_dinucleotide_flexibility():
    assert bendability("AA") == 0.06  # rigid A-tract (Bolshoy)
    assert bendability("GC") == 0.11  # most flexible
    assert bendability("gc") == 0.11  # case-insensitive


def test_bendability_none_when_no_scored_dinucleotide():
    assert bendability("A") is None  # too short for a dinucleotide
    assert bendability("") is None
    assert bendability("NN") is None  # no scored dinucleotide (N-run)


def test_yr_ry_balance_is_the_rigid_flexible_phase():
    assert yr_ry_balance("TA") == 1.0  # YR (pyrimidine->purine) -> flexible-biased
    assert yr_ry_balance("AT") == -1.0  # RY (purine->pyrimidine) -> rigid-biased
    assert yr_ry_balance("CG") == 1.0  # YR
    assert yr_ry_balance("GC") == -1.0  # RY
    assert yr_ry_balance("TAAT") == 0.0  # one YR + one RY -> balanced
    assert yr_ry_balance("TACG") == 1 / 3  # 2 YR + 1 RY -> fractional (kills the // mutant)


def test_yr_ry_balance_none_when_no_yr_or_ry():
    assert yr_ry_balance("AA") is None  # RR only -> no YR/RY dinucleotide
    assert yr_ry_balance("") is None
