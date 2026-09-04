"""Intent tests for the PREFER layer — the ported recommendation blend (submodular combine of soft
signals × product of alignment factors). Authored from the ModelAtlas design, not generated."""

from homeostat.recommend import score_candidate, submodular_combine


def test_submodular_combine_empty_is_neutral():
    assert submodular_combine([]) == 1.0  # no soft signal -> multiplicative identity


def test_submodular_combine_single_signal_counts_fully():
    assert submodular_combine([1.0], decay=0.5) == 2.0  # 1 + 1*decay^0


def test_submodular_combine_diminishing_and_order_independent():
    # sorted desc [0.6, 0.4]: 1 + 0.6*1 + 0.4*0.5 = 1.8; the weaker signal is discounted
    assert submodular_combine([0.6, 0.4], decay=0.5) == 1.8
    assert submodular_combine([0.4, 0.6], decay=0.5) == 1.8  # order-independent (sorted internally)


def test_submodular_combine_second_same_signal_is_discounted():
    # two 1.0 signals do NOT double to 3.0: the second counts by decay -> 1 + 1 + 0.5 = 2.5
    assert submodular_combine([1.0, 1.0], decay=0.5) == 2.5


def test_score_candidate_is_factor_product_times_soft_combine():
    assert score_candidate([1.0, 1.0], []) == 1.0  # product 1 * combine([]) 1
    assert score_candidate([0.5], [1.0], decay=0.5) == 1.0  # 0.5 * (1 + 1)
    assert score_candidate([0.5, 0.5], []) == 0.25  # product only; soft empty -> 1


def test_score_candidate_a_zero_alignment_factor_demotes():
    # coverage/alignment near zero demotes regardless of strong soft signals (the hard factors gate)
    assert score_candidate([0.0, 1.0], [1.0, 1.0]) == 0.0


def test_score_candidate_strongest_soft_signal_counts_fully_even_at_zero_decay():
    # decay**0 == 1: the top soft signal always counts fully -> 1.0 * (1 + 1.0) = 2.0
    assert score_candidate([1.0], [1.0], decay=0.0) == 2.0
