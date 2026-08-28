"""Intent tests for the Pan-UKBB transferability stat helpers."""

import math

from homeostat.panukbb import pearson, sign_concordance


def test_sign_concordance_all_agree():
    assert sign_concordance([(1.0, 2.0), (-1.0, -0.5), (0.3, 0.1)]) == 1.0


def test_sign_concordance_half_disagree():
    # two agree, two disagree -> 0.5; zero-beta pairs excluded.
    assert sign_concordance([(1.0, 1.0), (1.0, -1.0), (-2.0, -3.0), (-1.0, 2.0)]) == 0.5
    assert sign_concordance([(0.0, 1.0), (1.0, 1.0)]) == 1.0  # zero excluded


def test_pearson_perfect_and_anti():
    assert pearson([(1.0, 2.0), (2.0, 4.0), (3.0, 6.0)]) == 1.0
    assert math.isclose(pearson([(1.0, -1.0), (2.0, -2.0), (3.0, -3.0)]), -1.0, abs_tol=1e-9)


def test_pearson_degenerate_returns_zero():
    assert pearson([(1.0, 1.0)]) == 0.0
    assert pearson([(1.0, 5.0), (1.0, 6.0)]) == 0.0  # zero variance in x
