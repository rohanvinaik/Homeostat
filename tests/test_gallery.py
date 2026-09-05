"""Claim-integrity tests for the runnable gallery."""

from homeostat.resolve import Cluster, complete_target_rank


def _cluster(*entities: str) -> Cluster:
    return Cluster(frozenset(entities), ())


def test_complete_axis_rank_rejects_a_candidate_with_only_one_axis_member():
    ranked = [(_cluster("LRRK2", "ARFGAP1", "ARHGEF7"), 1.0)]

    assert complete_target_rank(ranked, {"LRRK2", "NOD2", "RIPK2"}) is None


def test_complete_axis_rank_requires_a_positive_scoring_complete_candidate():
    axis = {"LRRK2", "NOD2", "RIPK2"}
    ranked = [
        (_cluster(*axis), 0.0),
        (_cluster("DECOY"), 2.0),
        (_cluster(*axis, "TRAF6"), 1.0),
    ]

    assert complete_target_rank(ranked, axis) == 3
