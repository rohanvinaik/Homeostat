"""Intent tests for the tiered signal container — authored from the design."""

import dataclasses

from homeostat.signal import Signal, Tier


def test_tier_values():
    assert Tier.VERIFIED.value == "verified"
    assert Tier.REPORTED.value == "reported"
    assert Tier.ABSENT.value == "absent"


def test_signal_carries_tier_verbatim():
    s = Signal(ident="rs2201841", state="C;C", tier=Tier.VERIFIED)
    assert s.ident == "rs2201841"
    assert s.state == "C;C"  # kept verbatim — no normalization
    assert s.tier is Tier.VERIFIED


def test_signal_is_frozen():
    s = Signal(ident="x", state="A;G", tier=Tier.REPORTED)
    raised = False
    try:
        s.state = "G;G"  # type: ignore[misc]
    except dataclasses.FrozenInstanceError:
        raised = True
    assert raised
