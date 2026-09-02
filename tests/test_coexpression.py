"""Intent tests for the co-expression readout — OTP ternary co-deviation, not correlation.

A sample counts only where both genes are off baseline (informational zero drops the rest); aligned
= both deviate the same direction. The verdict reads the deterministic co-deviation: enough joint
perturbations, and consistently aligned (co-varies) / opposed (counter-varies) / mixed."""

from homeostat.coexpression import (
    codeviation,
    codeviation_verdict,
    coexpression_events,
    tissue_ternary,
)
from homeostat.event import Event


def test_codeviation_counts_joint_perturbations_and_alignment():
    # i0 both up (aligned); i1 a-only (drops); i2 both down (aligned); i3 opposed; i4 b-only (drops)
    a = [1, 1, -1, 1, 0]
    b = [1, 0, -1, -1, 1]
    assert codeviation(a, b) == (3, 2)  # 3 joint perturbations, 2 aligned


def test_codeviation_baseline_is_the_informational_zero():
    # every sample has at least one gene at baseline -> no joint perturbation at all
    assert codeviation([1, 0, -1], [0, 1, 0]) == (0, 0)


def test_codeviation_verdict_reads_the_deterministic_coupling():
    assert codeviation_verdict(1, 1, 5, 0.8) == "insufficient"  # fewer than min_support joints
    assert codeviation_verdict(10, 9, 5, 0.8) == "co-varies"  # 90% aligned >= 0.8
    assert codeviation_verdict(10, 1, 5, 0.8) == "counter-varies"  # 90% opposed >= 0.8
    assert codeviation_verdict(10, 5, 5, 0.8) == "uncoupled"  # 50/50, no consistent coupling


def test_codeviation_verdict_zero_joints_is_insufficient_not_a_crash():
    assert codeviation_verdict(0, 0, 0, 0.8) == "insufficient"  # guarded against 0/0


# ---- the render layer ------------------------------------------------------------


def test_tissue_ternary_positions_off_the_tissue_median():
    # median([1,1,1,100,100]) = 1; a >2-fold-up sample is +1, at-median is the informational zero
    assert tissue_ternary([1, 1, 1, 100, 100], 1.0) == [0, 0, 0, 1, 1]


def test_coexpression_events_co_varies_within_a_tissue_carries_the_tissue_as_mode():
    sample_ids = ["s1", "s2", "s3", "s4", "s5"]
    tissue = dict.fromkeys(sample_ids, "Liver")
    expr = {"A": [1, 1, 1, 100, 100], "B": [1, 1, 1, 100, 100]}  # deviate together at s4, s5
    events = coexpression_events(sample_ids, expr, tissue, min_support=1, consistency=0.8)
    assert events == [Event("coexpression", "tracks", "A", "B", 1, "Liver")]


def test_coexpression_events_counter_varies_is_opposes():
    sample_ids = ["s1", "s2", "s3", "s4", "s5"]
    tissue = dict.fromkeys(sample_ids, "Liver")
    expr = {"A": [1, 1, 1, 100, 100], "B": [100, 100, 100, 1, 1]}  # deviate opposite at s4, s5
    events = coexpression_events(sample_ids, expr, tissue, min_support=1, consistency=0.8)
    assert events == [Event("coexpression", "opposes", "A", "B", 1, "Liver")]


def test_coexpression_events_no_joint_perturbation_emits_nothing():
    sample_ids = ["s1", "s2", "s3", "s4", "s5"]
    tissue = dict.fromkeys(sample_ids, "Liver")
    expr = {"A": [1, 1, 1, 100, 100], "C": [100, 100, 1, 1, 1]}  # never both off-baseline together
    assert coexpression_events(sample_ids, expr, tissue, min_support=1, consistency=0.8) == []
