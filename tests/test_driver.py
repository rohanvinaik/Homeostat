"""Intent tests for the driver — generate-wide/resolve-narrow, read as a STORY. `drive` is validated
end-to-end; the (now orphaned) `rank_candidates`/`proximity_coherence` stay Detective-pinned, kept
for the deferred recommendation ranker that will sort STORY-reads (not genes)."""

from homeostat.driver import drive, proximity_coherence, rank_candidates
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


def test_rank_candidates_convergence_breaks_a_coverage_tie():
    # A and B BOTH cover both observed (tied on coverage); convergence is the tie-breaker.
    # align 1.0 each; A soft 4/4=1.0 -> 1*(1+1)=2.0 ; B soft 1/4=0.25 -> 1*(1+0.25)=1.25 -> A first.
    ranked = rank_candidates(["B", "A"], [[], []], n_observed=2, convergence={"A": 4.0, "B": 1.0})
    assert ranked == [("A", 2.0), ("B", 1.25)]


def test_rank_candidates_survivor_absent_from_convergence_does_not_crash():
    # a survivor with no convergence datum -> soft skipped (no KeyError), ranked by coverage alone.
    assert rank_candidates(["Z"], [[]], 1, convergence={"A": 1.0}) == [("Z", 1.0)]


def test_rank_candidates_all_zero_convergence_skips_the_soft_signal():
    # max convergence 0 -> guard is `> 0`, so no soft signal (no ZeroDivision), rank by coverage.
    assert rank_candidates(["A"], [[]], 1, convergence={"A": 0.0}) == [("A", 1.0)]


def test_rank_candidates_convergence_normalizes_even_when_max_is_at_or_below_one():
    # max_conv == 1.0 still normalizes and applies (the guard is `> 0`, not `> 1`).
    ranked = rank_candidates(["A", "B"], [[], []], 2, convergence={"A": 1.0, "B": 0.5})
    assert ranked == [("A", 2.0), ("B", 1.5)]


def test_rank_candidates_zero_coverage_with_a_soft_signal_stays_zero():
    # align 0 (killed by its one constraint) -> 0 * (1 + soft) = 0.0, never None.
    assert rank_candidates(["x"], [["x"]], 1, convergence={"x": 1.0}) == [("x", 0.0)]


def test_rank_candidates_coherence_is_a_second_alignment_factor():
    # A and B tie on coverage (both cover the one observed); A has higher coherence -> A first.
    # A: align [1.0, 0.8] -> 0.8 ; B: align [1.0, 0.2] -> 0.2 (coherence multiplies coverage).
    ranked = rank_candidates(["B", "A"], [[]], 1, coherence={"A": 0.8, "B": 0.2})
    assert ranked == [("A", 0.8), ("B", 0.2)]


def test_rank_candidates_survivor_absent_from_coherence_does_not_crash():
    # a survivor with no coherence datum -> the coherence factor is skipped (no KeyError).
    assert rank_candidates(["Z"], [[]], 1, coherence={"A": 0.5}) == [("Z", 1.0)]


def test_proximity_coherence_favours_the_direct_regulator():
    # observed {C}; A->C direct (dist 1), D->E->C distant (dist 2). A=0.5 coheres more than D=1/3.
    radj = {"C": ["A", "E"], "E": ["D"], "A": [], "D": []}
    coh = proximity_coherence(["C"], radj)
    assert coh["C"] == 1.0  # C reaches itself (dist 0)
    assert coh["A"] == 0.5 and coh["E"] == 0.5  # direct regulators (dist 1)
    assert coh["D"] == 1 / 3 and coh["A"] > coh["D"]  # distant coheres less than direct


def test_proximity_coherence_is_the_mean_over_observed():
    # A reaches C (dist 1) and F (dist 2): coherence is the MEAN (1/2 + 1/3)/2, not the sum.
    radj = {"C": ["A"], "F": ["B"], "B": ["A"], "A": []}
    coh = proximity_coherence(["C", "F"], radj)
    assert coh["A"] == (1 / 2 + 1 / 3) / 2


# ---- the composed read -----------------------------------------------------------


def test_drive_recovers_the_unique_source_and_reads_it_as_a_story():
    # source amplifies A and B; decoy only A. A and B both observed UP -> source is the unique
    # directed cause reaching both, polarity-consistent -> RESOLVED. The PREFER STORY reads source
    # as a resolving-quest hero joining the two symptoms (not a ranked gene).
    ev = [
        _reg("amplifies", "source", "A"),
        _reg("amplifies", "source", "B"),
        _reg("amplifies", "decoy", "A"),
    ]
    pos = {"A": position("A", 1.0, 0.0, 0.0), "B": position("B", 1.0, 0.0, 0.0)}
    read = drive(ev, pos, VS)
    assert read.verdict == "resolved"
    assert read.trajectory.survivors_left == ["source"]  # REQUIRE recovers the source
    assert any(q.hero == "source" and q.verdict == "resolving" for q in read.story.genres["quest"])


def test_drive_polarity_censor_certifies_bottom_on_a_contradictory_pattern():
    # source amplifies A and B; A observed UP but B observed DOWN. No single perturbation of source
    # explains both -> the polarity censor rules it out -> certified ⊥ (no lawful mechanism).
    ev = [_reg("amplifies", "source", "A"), _reg("amplifies", "source", "B")]
    pos = {"A": position("A", 1.0, 0.0, 0.0), "B": position("B", -1.0, 0.0, 0.0)}
    read = drive(ev, pos, VS)
    assert "source" in read.censored["polarity"]  # ruled out by mechanistic contradiction
    assert read.verdict == "bottom" and read.trajectory.bottom is True
