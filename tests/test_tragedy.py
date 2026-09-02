"""Intent tests for the tragedy genre — a native topology read over the regulatory web.

A tragedy is an amplify-cascade from an origin (a source) into an uncensored sink (the doom). The
H4 refusal downgrades an *inhibited* sink to "compensated"; a cascade with no source (a cycle) is a
different genre and yields nothing. Self-loops never count (they propagate to no new node)."""

from homeostat.event import Event
from homeostat.tragedy import (
    Tragedy,
    doom_verdict,
    is_sink,
    read_tragedy,
    regulatory_adjacency,
    sources,
)


def _amp(a, b):
    return Event("regulatory", "amplifies", a, b, 1)


def _inh(a, b):
    return Event("regulatory", "inhibits", a, b, 1)


# ---- the pure decision -----------------------------------------------------------


def test_doom_verdict_names_the_three_states():
    assert doom_verdict(True, True, False) == "doomed"  # uncensored terminal a cascade reaches
    assert doom_verdict(True, True, True) == "compensated"  # H4: an inhibitor restrains the doom
    assert doom_verdict(False, True, False) == "not-doom"  # not a sink
    assert doom_verdict(True, False, False) == "not-doom"  # a sink no cascade reaches


# ---- the graph helpers -----------------------------------------------------------


def test_regulatory_adjacency_splits_by_verb_and_drops_self_loops():
    # self-loop B->B and the physical edge are both dropped from the amplify adjacency
    physical = Event("physical", "binds", "A", "B", 1)
    events = [_amp("A", "B"), _amp("B", "B"), _inh("X", "B"), physical]
    assert regulatory_adjacency(events, "amplifies") == {"A": {"B"}}
    assert regulatory_adjacency(events, "inhibits") == {"X": {"B"}}


def test_sources_are_origins_with_no_upstream():
    adj = {"A": {"B"}, "B": {"C"}}
    assert sources(adj) == {"A"}  # B has an upstream (A); C is a pure sink, not a source
    assert is_sink(adj, "C") and not is_sink(adj, "B")


# ---- the read --------------------------------------------------------------------


def test_read_tragedy_locks_a_cascade_onto_an_uncensored_sink():
    # A -> B -> C, C self-amplifies (a lock, still a sink); C is the uncensored doom.
    events = [_amp("A", "B"), _amp("B", "C"), _amp("C", "C")]
    assert read_tragedy(events) == [Tragedy("A", "C", "doomed")]  # B is a middle, never emitted


def test_read_tragedy_h4_refusal_compensates_an_inhibited_sink():
    events = [_amp("A", "B"), _amp("B", "C"), _inh("Z", "C")]
    assert read_tragedy(events) == [Tragedy("A", "C", "compensated")]


def test_read_tragedy_declines_a_cycle_with_no_origin():
    events = [_amp("A", "B"), _amp("B", "A")]  # a loop — no source, so no tragedy (it is a comedy)
    assert read_tragedy(events) == []


def test_read_tragedy_reports_each_origin_of_a_convergent_doom():
    # two independent origins whose cascades both lock onto the same sink S
    events = [_amp("P", "S"), _amp("Q", "S")]
    assert read_tragedy(events) == [Tragedy("P", "S", "doomed"), Tragedy("Q", "S", "doomed")]
