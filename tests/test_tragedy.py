"""Intent tests for the tragedy genre — a native OTP topology read over the regulatory web.

The cascade is polarity-blind reachability; polarity is the OTP ternary propagated by sign-product,
with disagreeing paths collapsing to the informational zero. A sink's verdict is its net drive:
net-up = doomed, net-down = suppressed (the H4 refusal), informational-zero = indeterminate. A cycle
(no source) is a different genre and yields nothing. (The OTP merge + signed graph it rides on are
pinned in test_topology.)"""

from homeostat.event import Event
from homeostat.otp import OPPOSE, ORTHOGONAL, SUPPORT
from homeostat.topology import signed_adjacency
from homeostat.tragedy import (
    Tragedy,
    doom_verdict,
    is_sink,
    net_signs,
    read_tragedy,
    sources,
)


def _amp(a, b):
    return Event("regulatory", "amplifies", a, b, 1)


def _inh(a, b):
    return Event("regulatory", "inhibits", a, b, 1)


# ---- the pure verdict ------------------------------------------------------------


def test_doom_verdict_reads_the_net_sign():
    assert doom_verdict(True, True, SUPPORT) == "doomed"  # driven up and locked
    assert doom_verdict(True, True, OPPOSE) == "suppressed"  # H4: a censor holds it down
    assert doom_verdict(True, True, ORTHOGONAL) == "indeterminate"  # paths disagree -> abstain
    assert doom_verdict(False, True, SUPPORT) == "not-doom"  # not a sink
    assert doom_verdict(True, False, SUPPORT) == "not-doom"  # no cascade reaches it


# ---- the OTP net-sign propagation ------------------------------------------------


def test_net_signs_flip_on_inhibition_and_disinhibit_on_two():
    assert net_signs(signed_adjacency([_amp("A", "B"), _amp("B", "C")]), "A")["C"] == SUPPORT
    assert net_signs(signed_adjacency([_amp("A", "B"), _inh("B", "C")]), "A")["C"] == OPPOSE
    # two inhibitions compose to a net-up drive (disinhibition)
    assert net_signs(signed_adjacency([_inh("A", "B"), _inh("B", "C")]), "A")["C"] == SUPPORT


def test_net_signs_collapse_disagreeing_paths_to_zero_and_survive_cycles():
    # A->B->S (up) and A->C->S (down): S is driven both ways -> the informational zero
    events = [_amp("A", "B"), _amp("B", "S"), _amp("A", "C"), _inh("C", "S")]
    assert net_signs(signed_adjacency(events), "A")["S"] == ORTHOGONAL
    # a cycle back to the pinned origin terminates and leaves the origin SUPPORT
    assert net_signs(signed_adjacency([_amp("A", "B"), _amp("B", "A")]), "A")["A"] == SUPPORT


# ---- the read --------------------------------------------------------------------


def test_read_tragedy_dooms_a_net_up_sink():
    assert read_tragedy([_amp("A", "B"), _amp("B", "C")]) == [Tragedy("A", "C", "doomed")]


def test_read_tragedy_suppresses_a_net_down_sink():
    # the H4 refusal, fired on structure: the terminal is driven down, not doomed
    assert read_tragedy([_amp("A", "B"), _inh("B", "C")]) == [Tragedy("A", "C", "suppressed")]


def test_read_tragedy_abstains_when_the_arc_disagrees():
    events = [_amp("A", "B"), _amp("B", "S"), _amp("A", "C"), _inh("C", "S")]
    assert read_tragedy(events) == [Tragedy("A", "S", "indeterminate")]


def test_read_tragedy_declines_a_cycle_with_no_origin():
    assert read_tragedy([_amp("A", "B"), _amp("B", "A")]) == []


def test_sources_and_is_sink():
    reach = {"A": {"B"}, "B": {"C"}}
    assert sources(reach) == {"A"} and is_sink(reach, "C") and not is_sink(reach, "B")
