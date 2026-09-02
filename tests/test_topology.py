"""Intent tests for the shared genre substrate — OTP merge + the signed regulatory graph.

`otp_combine` returns the shared value when two drives agree and the informational zero when they
disagree. `signed_adjacency` signs regulatory edges by verb (amplify +1 / inhibit -1), collapses a
pair that is both to the informational zero, and drops self-loops and non-regulatory edges."""

from homeostat.event import Event
from homeostat.otp import OPPOSE, ORTHOGONAL, SUPPORT
from homeostat.topology import otp_combine, signed_adjacency


def _amp(a, b):
    return Event("regulatory", "amplifies", a, b, 1)


def _inh(a, b):
    return Event("regulatory", "inhibits", a, b, 1)


def test_otp_combine_agrees_or_falls_to_the_informational_zero():
    assert otp_combine(SUPPORT, SUPPORT) == SUPPORT
    assert otp_combine(OPPOSE, OPPOSE) == OPPOSE
    assert otp_combine(SUPPORT, OPPOSE) == ORTHOGONAL  # disagreement -> no opinion
    assert otp_combine(SUPPORT, ORTHOGONAL) == ORTHOGONAL


def test_signed_adjacency_signs_by_verb_mixes_to_zero_drops_self_and_nonreg():
    events = [_amp("A", "B"), _inh("A", "B"), _amp("A", "C"), _amp("B", "B")]
    events.append(Event("physical", "binds", "A", "C", 1))
    adj = signed_adjacency(events)
    assert adj["A"]["B"] == ORTHOGONAL  # amplify + inhibit on the same pair -> informational zero
    assert adj["A"]["C"] == SUPPORT  # amplify only; the physical edge is not regulatory
    assert "B" not in adj  # B's only out-edge was a self-loop, dropped
