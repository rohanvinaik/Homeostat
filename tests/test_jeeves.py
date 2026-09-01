"""Intent tests for the Jeeves discrimination-dimension selector — authored from the design
(SYSTEM_DESIGN.md §9/§12.3, value-of-information), not generated."""

import math

from homeostat.jeeves import Probe, expected_information_gain, probe_gain, select_probe

# ---- the pure EIG decision -------------------------------------------------------


def test_eig_singletons_resolve_everything():
    assert expected_information_gain([1, 1, 1]) == math.log2(3)  # full separation


def test_eig_single_class_discriminates_nothing():
    assert expected_information_gain([3]) == 0.0  # all survivors agree -> no gain
    assert expected_information_gain([0, 5]) == 0.0  # one real class -> no gain


def test_eig_uneven_split_between_zero_and_max():
    # {2,1} over n=3: log2(3) - (2/3)*log2(2) = 1.585 - 0.667
    assert expected_information_gain([2, 1]) == math.log2(3) - (2 * math.log2(2)) / 3


def test_eig_degenerate_inputs_are_zero():
    assert expected_information_gain([]) == 0.0
    assert expected_information_gain([1]) == 0.0  # n<=1


# ---- probe gain over the live survivors ------------------------------------------


def test_probe_gain_buckets_live_survivors_by_predicted_sign():
    predicted = {"A": 1, "B": -1, "C": 1}
    # over {A,B,C}: classes {A,C}(+1), {B}(-1) -> sizes [2,1]
    assert probe_gain(predicted, ["A", "B", "C"]) == expected_information_gain([2, 1])


def test_probe_gain_missing_prediction_is_the_orthogonal_class():
    predicted = {"A": 1}  # B unpredicted -> orthogonal 0 class
    # {A}(+1), {B}(0) -> sizes [1,1] -> full split
    assert probe_gain(predicted, ["A", "B"]) == math.log2(2)


# ---- the selection ---------------------------------------------------------------


def test_select_returns_highest_eig_probe():
    survivors = ["A", "B", "C"]
    weak = Probe("all_same", "confirm", {"A": 1, "B": 1, "C": 1})  # EIG 0
    strong = Probe("splits", "rule_out", {"A": 1, "B": -1, "C": 0})  # 3 classes -> max
    assert select_probe(survivors, [weak, strong]) is strong


def test_confirm_and_rule_out_compete_on_one_eig_scale():
    survivors = ["A", "B"]
    confirm = Probe("sym", "confirm", {"A": 1, "B": 1})  # EIG 0
    rule_out = Probe("tx", "rule_out", {"A": 1, "B": -1})  # splits -> EIG 1
    # the negative-sign probe wins because it discriminates, regardless of kind
    assert select_probe(survivors, [confirm, rule_out]) is rule_out


def test_select_abstains_when_nothing_discriminates():
    survivors = ["A", "B"]
    useless = Probe("d", "confirm", {"A": 1, "B": 1})
    assert select_probe(survivors, [useless]) is None  # informational zero at the selector


def test_select_breaks_ties_by_dimension_name():
    survivors = ["A", "B"]
    p_b = Probe("b_dim", "confirm", {"A": 1, "B": -1})  # EIG 1
    p_a = Probe("a_dim", "confirm", {"A": 1, "B": -1})  # EIG 1, same gain
    assert select_probe(survivors, [p_b, p_a]) is p_a  # alphabetically first wins
