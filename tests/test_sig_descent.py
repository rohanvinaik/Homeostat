"""Intent tests for personalized (selection-weighted) κ and the control-rank report."""

from homeostat import kappa
from homeostat.sig_descent import _control_report, _ranks


def test_personalized_pagerank_lifts_the_prior_node():
    # A—B—C path; unweighted κ favors the center B. A PBS prior concentrated on the
    # leaf C must lift C's rank above where uniform κ puts it.
    adj = {"A": {"B"}, "B": {"A", "C"}, "C": {"B"}}
    unw = kappa.pagerank(adj)
    pbs = kappa.personalized_pagerank(adj, {"C": 1.0})
    assert pbs["C"] > unw["C"]  # the prior lifted C
    assert pbs["C"] > pbs["A"]  # and C now outranks the symmetric leaf A


def test_personalized_pagerank_zero_prior_falls_back_to_uniform():
    adj = {"A": {"B"}, "B": {"A", "C"}, "C": {"B"}}
    assert kappa.personalized_pagerank(adj, {}) == kappa.pagerank(adj)


def test_personalized_pagerank_is_deterministic():
    adj = {"A": {"B"}, "B": {"A", "C"}, "C": {"B", "D"}, "D": {"C"}}
    prior = {"A": 0.4, "D": 0.6}
    assert kappa.personalized_pagerank(adj, prior) == kappa.personalized_pagerank(adj, prior)


def test_ranks_are_one_based_descending():
    r = _ranks({"a": 0.5, "b": 0.9, "c": 0.1}, ["a", "b", "c"])
    assert r == {"b": 1, "a": 2, "c": 3}


def test_control_report_lift_sign():
    # κ_PBS ranks controls better (smaller rank) than κ_unweighted -> positive lift.
    genes = ["LRRK2", "NOD2", "RIPK2", "X", "Y", "Z"]
    kpbs = {"LRRK2": 0.9, "NOD2": 0.8, "RIPK2": 0.7, "X": 0.1, "Y": 0.05, "Z": 0.01}
    kunw = {"X": 0.9, "Y": 0.8, "Z": 0.7, "LRRK2": 0.1, "NOD2": 0.05, "RIPK2": 0.01}
    weights = dict.fromkeys(genes, 0.0)
    rep = _control_report(genes, kpbs, kunw, weights)
    assert rep["_mean_control_rank"]["lift_vs_unweighted"] > 0  # κ_PBS ranks them better
