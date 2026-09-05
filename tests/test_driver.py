"""Intent tests for the driver — generate-wide/resolve-narrow, read as a STORY. `drive` is validated
end-to-end through the composed read (elimination → story → resolve-narrow → σ_sem)."""

from homeostat.driver import drive
from homeostat.event import Event
from homeostat.operator import HypothesisOutcome
from homeostat.position import position

VS = {"amplifies": 1, "inhibits": -1}


def _reg(verb, subj, tgt):
    return Event("regulatory", verb, subj, tgt, 1)


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


def test_drive_closes_the_story_narrow_into_ranked_mechanisms():
    # the composed read now also CLOSES the wide story narrow: resolve.rank_clusters over the story-
    # clusters yields ranked candidate MECHANISMS. A cluster spanning the observed shadow leads with
    # a positive score (coverage × internal-coherence × the calibrated predictive meter).
    ev = [
        _reg("amplifies", "source", "A"),
        _reg("amplifies", "source", "B"),
        _reg("amplifies", "decoy", "A"),
    ]
    pos = {"A": position("A", 1.0, 0.0, 0.0), "B": position("B", 1.0, 0.0, 0.0)}
    read = drive(ev, pos, VS)
    assert read.ranked  # the resolve-narrow engine produced ranked mechanisms
    assert read.ranked[0][1] > 0.0  # the leading mechanism scores positive
    assert any({"A", "B"} <= cl.entities for cl, _ in read.ranked)  # a mechanism spans the shadow
    # the σ_sem completeness read: a valid resolved fraction, residual never exceeds initial.
    assert 0.0 <= read.completeness.resolved <= 1.0
    assert read.completeness.h_residual <= read.completeness.h0


def test_drive_operator_hypothesis_is_tested_never_ground_truth():
    # the operator proposes A amplifies B; A and B both observed up -> the shadow CONFIRMS it. It
    # enters the PREFER read and the ledger reports the confirmation -- but it NEVER enters the
    # elimination (REQUIRE still recovers the real source, untouched by the operator's edge).
    ev = [_reg("amplifies", "source", "A"), _reg("amplifies", "source", "B")]
    pos = {"A": position("A", 1.0, 0.0, 0.0), "B": position("B", 1.0, 0.0, 0.0)}
    read = drive(ev, pos, VS, hypotheses=[_reg("amplifies", "A", "B")])
    assert read.operator == [HypothesisOutcome("A", "amplifies", "B", "confirmed")]
    assert read.trajectory.survivors_left == ["source"]  # elimination untouched by the hypothesis


def test_drive_operator_contradicted_hypothesis_falls_out():
    # A up but B down; the operator proposes A amplifies B -> the shadow CONTRADICTS it (it predicts
    # B up). The ledger records the contradiction; correctness stays in the code, not the operator.
    ev = [_reg("amplifies", "source", "A")]
    pos = {"A": position("A", 1.0, 0.0, 0.0), "B": position("B", -1.0, 0.0, 0.0)}
    read = drive(ev, pos, VS, hypotheses=[_reg("amplifies", "A", "B")])
    assert read.operator == [HypothesisOutcome("A", "amplifies", "B", "contradicted")]


def test_drive_relevant_including_the_source_still_resolves():
    # the diagnosis subspace includes the true source -> the read resolves to it as before.
    ev = [
        _reg("amplifies", "source", "A"),
        _reg("amplifies", "source", "B"),
        _reg("amplifies", "decoy", "A"),
    ]
    pos = {"A": position("A", 1.0, 0.0, 0.0), "B": position("B", 1.0, 0.0, 0.0)}
    read = drive(ev, pos, VS, relevant={"source", "A", "B"})
    assert read.verdict == "resolved"
    assert read.trajectory.survivors_left == ["source"]


def test_drive_relevant_excluding_the_source_lets_the_label_fall_out():
    # the diagnosis subspace EXCLUDES the true source (option B): the shadow stays observed truth,
    # but no RELEVANT source explains it -> the read does NOT resolve, and the excluded source is
    # never surfaced. The label falls out, exactly like a wrong hypothesis.
    ev = [
        _reg("amplifies", "source", "A"),
        _reg("amplifies", "source", "B"),
        _reg("amplifies", "decoy", "A"),
    ]
    pos = {"A": position("A", 1.0, 0.0, 0.0), "B": position("B", 1.0, 0.0, 0.0)}
    read = drive(ev, pos, VS, relevant={"decoy", "A", "B"})  # source excluded
    assert read.verdict != "resolved"
    assert "source" not in read.trajectory.survivors_left


def test_drive_polarity_censor_certifies_bottom_on_a_contradictory_pattern():
    # source amplifies A and B; A observed UP but B observed DOWN. No single perturbation of source
    # explains both -> the polarity censor rules it out -> certified ⊥ (no lawful mechanism).
    ev = [_reg("amplifies", "source", "A"), _reg("amplifies", "source", "B")]
    pos = {"A": position("A", 1.0, 0.0, 0.0), "B": position("B", -1.0, 0.0, 0.0)}
    read = drive(ev, pos, VS)
    assert "source" in read.censored["polarity"]  # ruled out by mechanistic contradiction
    assert read.verdict == "bottom"
    assert read.trajectory.bottom is True
