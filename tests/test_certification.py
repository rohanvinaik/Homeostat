"""Intent tests for the certification gate (full-C): the verification tier of a person's
observations gates whether a verdict is a CERTIFICATE. VERIFIED can certify; REPORTED is a run-kill
that constrains the read but banks nothing toward certification (NEGATIVE_SPECIFICATION Def. 1.4).
The verdict code is TAGGED with its trust boundary, never collapsed to a weaker verdict.
Paired with the Detective characterization under tests/detective/ per the two-step discipline.
"""

from homeostat.clinic import (
    BOTTOM,
    RESOLVED,
    is_certified,
    read_from_events,
    weakest_tier,
)
from homeostat.event import Event
from homeostat.otp import ORTHOGONAL, SUPPORT
from homeostat.position import Position
from homeostat.signal import Tier

V = Tier.VERIFIED.value
R = Tier.REPORTED.value
A = Tier.ABSENT.value


# ---- the pure decisions ----------------------------------------------------------


def test_weakest_tier_empty_is_vacuously_verified():
    # No observation weakens the read -> there is nothing to downgrade.
    assert weakest_tier([]) == V


def test_weakest_tier_is_the_weakest_link():
    assert weakest_tier([V, V]) == V
    assert weakest_tier([V, R]) == R  # one reported datum caps the whole read
    assert weakest_tier([R, A]) == A  # absent is weaker than reported
    assert weakest_tier([A, V, R]) == A  # order-independent minimum


def test_is_certified_requires_a_certificate_verdict_on_verified_evidence():
    assert is_certified("resolved", V) is True
    assert is_certified("bottom", V) is True
    # a certificate resting on reported evidence banks nothing toward certification
    assert is_certified("resolved", R) is False
    assert is_certified("bottom", R) is False
    # non-certificate verdicts are never certified, even on verified evidence
    assert is_certified("ask", V) is False
    assert is_certified("abstain", V) is False
    assert is_certified("degenerate", V) is False


# ---- end-to-end through the real read --------------------------------------------


def _reg_events():
    # directed regulatory web: source->A, source->B, decoy->A (only `source` reaches both).
    return [
        Event("regulatory", "amplify", "source", "A", 1),
        Event("regulatory", "amplify", "source", "B", 1),
        Event("regulatory", "amplify", "decoy", "A", 1),
    ]


def _positions(a_tier=Tier.VERIFIED, b_tier=Tier.VERIFIED):
    # A and B are the observed symptoms (deviated) at the given tiers; sources sit at baseline.
    return {
        "A": Position("A", SUPPORT, 1.0, 0.0, a_tier),
        "B": Position("B", SUPPORT, 1.0, 0.0, b_tier),
        "source": Position("source", ORTHOGONAL, 0.0, 0.0),
        "decoy": Position("decoy", ORTHOGONAL, 0.0, 0.0),
    }


def test_resolved_on_verified_evidence_is_certified():
    r = read_from_events(
        _reg_events(), _positions(), active_roles=set(), probes=[], directed_networks={"regulatory"}
    )
    assert r.verdict == RESOLVED
    assert r.mechanism == "source"
    assert r.certified is True
    assert r.certification_tier is Tier.VERIFIED


def test_resolved_on_reported_evidence_is_tagged_uncertified_not_collapsed():
    # One REPORTED observation: the mechanism is STILL RESOLVED (never collapsed to ABSTAIN), but
    # the read names its trust boundary -- uncertified, tier REPORTED.
    r = read_from_events(
        _reg_events(),
        _positions(a_tier=Tier.REPORTED),
        active_roles=set(),
        probes=[],
        directed_networks={"regulatory"},
    )
    assert r.verdict == RESOLVED
    assert r.mechanism == "source"
    assert r.certified is False
    assert r.certification_tier is Tier.REPORTED


def test_bottom_on_reported_evidence_is_an_uncertified_bottom():
    # A certified-shape ⊥ that rests on a REPORTED observation is reported UNCERTIFIED.
    events = _reg_events() + [Event("developmental", "closes_off", "source", "kinase", -1)]
    r = read_from_events(
        events,
        _positions(a_tier=Tier.REPORTED),
        active_roles={"kinase"},
        probes=[],
        directed_networks={"regulatory"},
    )
    assert r.verdict == BOTTOM
    assert r.mechanism is None
    assert r.certified is False
    assert r.certification_tier is Tier.REPORTED
