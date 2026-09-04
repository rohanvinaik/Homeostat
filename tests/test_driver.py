"""Intent tests for the driver — the generate-wide/resolve-narrow read as a ranked recommendation.
Authored from the design; the pure ranker is Detective-pinned, drive() is validated end-to-end."""

from homeostat.driver import drive, rank_candidates
from homeostat.event import Event
from homeostat.position import position

VS = {"amplifies": 1, "inhibits": -1}


def _reg(verb, subj, tgt):
    return Event("regulatory", verb, subj, tgt, 1)


# ---- the pure ranker -------------------------------------------------------------


def test_rank_candidates_orders_by_coverage():
    # A covers both constraints (in neither kill-set), B covers none -> A ranked first.
    ranked = rank_candidates(["A", "B"], [["B"], ["B"]], n_observed=2)
    assert ranked == [("A", 1.0), ("B", 0.0)]


def test_rank_candidates_zero_observed_is_all_zero():
    assert rank_candidates(["A", "B"], [], n_observed=0) == [("A", 0.0), ("B", 0.0)]


def test_rank_candidates_actually_reorders_by_score():
    # the higher-coverage candidate must come FIRST even when it is LAST in input -- the sort is the
    # ranking, not decoration. (A covers both; B neither; input order is ["B", "A"].)
    assert rank_candidates(["B", "A"], [["B"], ["B"]], n_observed=2) == [("A", 1.0), ("B", 0.0)]


def test_rank_candidates_single_observed_still_ranks():
    # n_observed == 1 is a valid read: the boundary is <= 0, not <= 1, so it ranks, not zeroes out.
    assert rank_candidates(["A", "B"], [["B"]], n_observed=1) == [("A", 1.0), ("B", 0.0)]


# ---- the composed read -----------------------------------------------------------


def test_drive_recovers_the_unique_source_and_ranks_it():
    # source amplifies A and B; decoy only A. A and B both observed UP -> source is the unique
    # directed cause reaching both, polarity-consistent -> RESOLVED, ranked first.
    ev = [
        _reg("amplifies", "source", "A"),
        _reg("amplifies", "source", "B"),
        _reg("amplifies", "decoy", "A"),
    ]
    pos = {"A": position("A", 1.0, 0.0, 0.0), "B": position("B", 1.0, 0.0, 0.0)}
    read = drive(ev, pos, VS)
    assert read.verdict == "resolved"
    assert read.ranked[0][0] == "source"
    assert read.trajectory.survivors_left == ["source"]


def test_drive_polarity_censor_certifies_bottom_on_a_contradictory_pattern():
    # source amplifies A and B; A observed UP but B observed DOWN. No single perturbation of source
    # explains both -> the polarity censor rules it out -> certified ⊥ (no lawful mechanism).
    ev = [_reg("amplifies", "source", "A"), _reg("amplifies", "source", "B")]
    pos = {"A": position("A", 1.0, 0.0, 0.0), "B": position("B", -1.0, 0.0, 0.0)}
    read = drive(ev, pos, VS)
    assert "source" in read.censored["polarity"]  # ruled out by mechanistic contradiction
    assert read.verdict == "bottom" and read.trajectory.bottom is True
