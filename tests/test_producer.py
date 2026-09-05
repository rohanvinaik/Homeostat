"""Intent + integration tests for the marker producer: `reference_center_spread` and `place` (the
placement core), `parse_marker` (the state parse), and `signals_to_positions` driven end to end
through the real read. Paired with the Detective characterization per the two-step.
"""

from homeostat.clinic import RESOLVED, read_from_events
from homeostat.differential import DEPLETED, ELEVATED, NONE
from homeostat.event import Event
from homeostat.otp import OPPOSE, ORTHOGONAL, SUPPORT
from homeostat.position import place
from homeostat.producer import parse_marker, reference_center_spread, signals_to_positions
from homeostat.signal import Signal, Tier

# ---- the placement core ----------------------------------------------------------


def test_reference_center_spread_is_midpoint_and_half_width():
    assert reference_center_spread(70.0, 100.0) == (85.0, 15.0)
    assert reference_center_spread(0.0, 10.0) == (5.0, 5.0)


def test_place_sign_and_kind_agree_by_construction():
    # reference interval [70, 100] -> center 85, spread 15; k=1 -> the band is exactly [70, 100].
    c, s = reference_center_spread(70.0, 100.0)
    hi = place("glucose", 120.0, c, s, k=1.0)  # above the band
    assert hi.sign == SUPPORT
    assert hi.differential.kind == ELEVATED
    lo = place("glucose", 50.0, c, s, k=1.0)  # below the band
    assert lo.sign == OPPOSE
    assert lo.differential.kind == DEPLETED
    mid = place("glucose", 85.0, c, s, k=1.0)  # inside the band -> informational zero
    assert mid.sign == ORTHOGONAL
    assert mid.differential.kind == NONE


def test_place_carries_the_tier_and_the_surprise():
    c, s = reference_center_spread(70.0, 100.0)
    p = place("glucose", 130.0, c, s, k=1.0, tier=Tier.REPORTED)
    assert p.tier is Tier.REPORTED
    assert p.differential.surprise == 3.0  # (130-85)/15 = 3 half-widths into the tail


def test_place_degenerate_reference_is_the_informational_zero():
    # a zero-spread (or None) reference cannot calibrate surprise -> abstain on BOTH channels.
    z = place("marker", 100.0, 50.0, 0.0, k=1.0)
    assert z.sign == ORTHOGONAL
    assert z.differential.kind == NONE
    assert z.differential.surprise == 0.0
    n = place("marker", 100.0, None, None, k=1.0)
    assert n.sign == ORTHOGONAL
    assert n.differential.kind == NONE


# ---- the state parse -------------------------------------------------------------


def test_parse_marker_numeric_or_none():
    assert parse_marker("90") == 90.0
    assert parse_marker("90.5") == 90.5
    assert parse_marker("A;G") is None  # a genotype -> deferred to the genotype pole
    assert parse_marker("") is None
    assert parse_marker("nan") is None  # a non-finite value is not a marker reading
    assert parse_marker("inf") is None


# ---- the full flow end to end ----------------------------------------------------

# Directed web: only `source` reaches BOTH symptoms A and B (decoy reaches only A).
_EVENTS = [
    Event("regulatory", "amplify", "source", "A", 1),
    Event("regulatory", "amplify", "source", "B", 1),
    Event("regulatory", "amplify", "decoy", "A", 1),
]
# A synthetic demographic reference table: A/B narrow [70,100]; sources wide-open (always normal).
_REF = {
    "A": (70.0, 100.0),
    "B": (70.0, 100.0),
    "source": (0.0, 1_000_000_000.0),
    "decoy": (0.0, 1_000_000_000.0),
}
_VOCAB = {n: n for n in ("A", "B", "source", "decoy")}  # identity grounding


def _reference(node, demographics):
    return _REF.get(node)


def _read(positions):
    return read_from_events(
        _EVENTS, positions, active_roles=set(), probes=[], directed_networks={"regulatory"}
    )


def test_producer_builds_structured_positions():
    positions = signals_to_positions(
        [Signal("A", "130", Tier.VERIFIED)], {"age": "40"}, _reference, _VOCAB
    )
    p = positions["A"]
    assert p.sign == SUPPORT
    assert p.differential.kind == ELEVATED
    assert p.differential.surprise == 3.0  # (130-85)/15
    assert p.tier is Tier.VERIFIED


def test_producer_full_flow_certified_on_verified_markers():
    signals = [
        Signal("A", "120", Tier.VERIFIED),
        Signal("B", "120", Tier.VERIFIED),
        Signal("source", "1", Tier.VERIFIED),
        Signal("decoy", "1", Tier.VERIFIED),
    ]
    r = _read(signals_to_positions(signals, {"age": "40"}, _reference, _VOCAB))
    assert r.verdict == RESOLVED
    assert r.mechanism == "source"
    assert r.certified is True
    assert r.certification_tier is Tier.VERIFIED


def test_producer_full_flow_uncertified_on_a_reported_marker():
    signals = [
        Signal("A", "120", Tier.REPORTED),  # a load-bearing marker only REPORTED
        Signal("B", "120", Tier.VERIFIED),
        Signal("source", "1", Tier.VERIFIED),
        Signal("decoy", "1", Tier.VERIFIED),
    ]
    r = _read(signals_to_positions(signals, {"age": "40"}, _reference, _VOCAB))
    assert r.verdict == RESOLVED
    assert r.mechanism == "source"
    assert r.certified is False
    assert r.certification_tier is Tier.REPORTED


def test_producer_drops_the_unplaceable():
    signals = [
        Signal("A", "120", Tier.VERIFIED),  # placeable
        Signal("B", "xyz", Tier.VERIFIED),  # non-numeric state -> dropped
        Signal("zzz", "50", Tier.VERIFIED),  # ungroundable -> dropped
        Signal("noref", "50", Tier.VERIFIED),  # groundable but no reference -> dropped
    ]
    vocab = dict(_VOCAB, noref="noref")
    positions = signals_to_positions(signals, {"age": "40"}, _reference, vocab)
    assert set(positions) == {"A"}  # only the fully-placeable reading survives
