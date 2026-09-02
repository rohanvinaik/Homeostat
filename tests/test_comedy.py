"""Intent tests for the comedy genre — the mutual-regulation cycle, read by OTP loop-gain.

A mutual pair's loop-gain is the sign-product of its two edges: net-up (mutual amplification OR
mutual inhibition) = vicious; net-down (negative feedback) = homeostatic; a mixed-polarity edge =
indeterminate. A feed-forward graph (no reciprocal edge) is a cascade, not a comedy, and yields
nothing."""

from homeostat.comedy import Comedy, loop_verdict, read_comedy
from homeostat.event import Event
from homeostat.otp import OPPOSE, ORTHOGONAL, SUPPORT


def _amp(a, b):
    return Event("regulatory", "amplifies", a, b, 1)


def _inh(a, b):
    return Event("regulatory", "inhibits", a, b, 1)


# ---- the pure verdict ------------------------------------------------------------


def test_loop_verdict_reads_the_loop_gain():
    assert loop_verdict(SUPPORT) == "vicious"  # reinforcing / locked
    assert loop_verdict(OPPOSE) == "homeostatic"  # self-correcting negative feedback
    assert loop_verdict(ORTHOGONAL) == "indeterminate"  # a mixed edge -> no coherent gain


# ---- the read --------------------------------------------------------------------


def test_read_comedy_mutual_amplification_is_vicious():
    assert read_comedy([_amp("A", "B"), _amp("B", "A")]) == [Comedy("A", "B", "vicious")]


def test_read_comedy_mutual_inhibition_is_a_vicious_toggle():
    # -1 * -1 = +1: mutual repression is a bistable lock, not self-correction
    assert read_comedy([_inh("A", "B"), _inh("B", "A")]) == [Comedy("A", "B", "vicious")]


def test_read_comedy_negative_feedback_is_homeostatic():
    # A raises B, B lowers A -> the loop self-corrects (the happy ending)
    assert read_comedy([_amp("A", "B"), _inh("B", "A")]) == [Comedy("A", "B", "homeostatic")]


def test_read_comedy_mixed_edge_is_indeterminate():
    # A both amplifies and inhibits B -> that edge is the informational zero -> loop-gain 0
    events = [_amp("A", "B"), _inh("A", "B"), _amp("B", "A")]
    assert read_comedy(events) == [Comedy("A", "B", "indeterminate")]


def test_read_comedy_declines_a_feed_forward_cascade():
    assert read_comedy([_amp("A", "B"), _amp("B", "C")]) == []  # no reciprocal edge -> not a comedy


def test_read_comedy_reports_each_pair_once():
    events = [_amp("A", "B"), _amp("B", "A"), _amp("B", "C"), _amp("C", "B")]
    assert read_comedy(events) == [Comedy("A", "B", "vicious"), Comedy("B", "C", "vicious")]
