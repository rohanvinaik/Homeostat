"""Intent tests for the SIGNOR adapter — from the settled design and real rows, not generated.

The effect→event mapping is the grammar decomposition (2026-09-02): direction→verb (amplifies /
inhibits, the polarity), mode→peer marker (activity/abundance/bare), and EVERY emitted edge is
sign=+1 (SIGNOR asserts the coupling exists — an inhibition is `inhibits`/+1, never a censor)."""

from homeostat.signor import (
    EFFECT,
    MECHANISM,
    TYPE_A,
    TYPE_B,
    A,
    B,
    parse_effect,
    row_disposition,
    row_to_event,
    signor_events,
)


def _row(a, ta, b, tb, effect, mech="binding"):
    r = [""] * 29
    r[A], r[TYPE_A] = a, ta
    r[B], r[TYPE_B] = b, tb
    r[EFFECT], r[MECHANISM] = effect, mech
    return r


# ---- the pure effect-string decomposition ----------------------------------------


def test_parse_effect_direction_and_mode():
    assert parse_effect("up-regulates activity") == (1, "activity")
    assert parse_effect("down-regulates activity") == (-1, "activity")
    # every quantity submode folds into the abundance channel (peer submodes, not tiers)
    assert parse_effect("up-regulates quantity by expression") == (1, "abundance")
    assert parse_effect("down-regulates quantity by destabilization") == (-1, "abundance")
    assert parse_effect("up-regulates quantity") == (1, "abundance")
    # bare direction: mode-level informational zero
    assert parse_effect("up-regulates") == (1, "")
    assert parse_effect("down-regulates") == (-1, "")
    # no directed claim
    assert parse_effect("unknown") is None
    assert parse_effect("form complex") is None


# ---- the pure keep/skip decision -------------------------------------------------


def test_row_disposition_codes():
    assert row_disposition("protein", "protein", True) == "emit"
    assert row_disposition("protein", "smallmolecule", True) == "skip-nonprotein"  # other network
    assert row_disposition("complex", "protein", True) == "skip-nonprotein"
    assert row_disposition("protein", "protein", False) == "skip-noeffect"  # unknown / form complex


# ---- row -> Event on real SIGNOR shapes ------------------------------------------


def test_activation_becomes_a_positive_amplifies_edge():
    # RIPK2 --up-regulates activity--> TRAF6 (the edge Reactome buried in a complex)
    row = _row("RIPK2", "protein", "TRAF6", "protein", "up-regulates activity", "binding")
    e = row_to_event(row)
    assert e is not None
    assert (e.network, e.verb, e.subject, e.target, e.sign, e.mode) == (
        "regulatory",
        "amplifies",
        "RIPK2",
        "TRAF6",
        1,
        "activity",
    )


def test_inhibition_is_inhibits_but_still_positive_sign():
    # THE correction: an inhibitory edge asserts the coupling EXISTS -> sign=+1; polarity = verb.
    row = _row("PTEN", "protein", "AKT1", "protein", "down-regulates activity")
    e = row_to_event(row)
    assert e is not None
    assert e.verb == "inhibits"
    assert e.sign == 1  # NOT -1: an inhibition is support, never a censor
    assert e.mode == "activity"


def test_quantity_is_the_abundance_channel_same_edge():
    row = _row("NOD2", "protein", "IRF4", "protein", "up-regulates quantity by expression", "txn")
    e = row_to_event(row)
    assert e is not None
    assert (e.verb, e.sign, e.mode) == ("amplifies", 1, "abundance")


def test_bare_direction_emits_the_base_edge_with_no_marker():
    row = _row("NOD2", "protein", "ATG16L1", "protein", "up-regulates")
    e = row_to_event(row)
    assert e is not None
    assert (e.verb, e.sign, e.mode) == ("amplifies", 1, "")


def test_nonprotein_endpoint_is_skipped():
    row = _row("DHFR", "protein", "dihydrofolate", "smallmolecule", "down-regulates activity")
    assert row_to_event(row) is None


def test_noeffect_is_skipped():
    row = _row("A", "protein", "B", "protein", "form complex")  # physical binding, other network
    assert row_to_event(row) is None


def test_signor_events_filters_the_stream():
    rows = [
        _row("RIPK2", "protein", "TRAF6", "protein", "up-regulates activity"),  # kept
        _row("PTEN", "protein", "AKT1", "protein", "down-regulates activity"),  # kept (inhibits/+1)
        _row("A", "protein", "B", "protein", "form complex"),  # dropped (no directed claim)
        _row("DHFR", "protein", "dhf", "smallmolecule", "down-regulates activity"),  # nonprotein
    ]
    events = signor_events(rows)
    assert [(e.subject, e.target, e.verb, e.sign) for e in events] == [
        ("RIPK2", "TRAF6", "amplifies", 1),
        ("PTEN", "AKT1", "inhibits", 1),
    ]
