"""Intent tests for the SIGNOR adapter — from the design and real SIGNOR rows, not generated.
The effect->sign policy is the founder's config; these use an activity-only sample policy to pin the
mechanics (protein-protein filter, effect lookup, mechanism-as-verb)."""

from homeostat.signor import (
    EFFECT,
    MECHANISM,
    TYPE_A,
    TYPE_B,
    A,
    B,
    row_disposition,
    row_to_event,
    signor_events,
)

# a sample policy (NOT the founder's final one): activity effects only
POLICY = {"up-regulates activity": 1, "down-regulates activity": -1}


def _row(a, ta, b, tb, effect, mech="binding"):
    r = [""] * 29
    r[A], r[TYPE_A] = a, ta
    r[B], r[TYPE_B] = b, tb
    r[EFFECT], r[MECHANISM] = effect, mech
    return r


# ---- the pure keep/skip decision -------------------------------------------------


def test_row_disposition_codes():
    assert row_disposition("protein", "protein", 1) == "emit"
    assert row_disposition("protein", "protein", -1) == "emit"
    assert row_disposition("protein", "smallmolecule", 1) == "skip-nonprotein"  # other network
    assert row_disposition("complex", "protein", 1) == "skip-nonprotein"
    assert row_disposition("protein", "protein", 0) == "skip-noeffect"  # not in policy / skipped


# ---- row -> Event on real SIGNOR shapes ------------------------------------------


def test_activation_becomes_a_directed_regulatory_event():
    # RIPK2 --up-regulates activity--> TRAF6 (the edge Reactome buried in a complex)
    row = _row("RIPK2", "protein", "TRAF6", "protein", "up-regulates activity", "binding")
    e = row_to_event(row, POLICY)
    assert e is not None
    assert (e.network, e.subject, e.target, e.sign) == ("regulatory", "RIPK2", "TRAF6", 1)
    assert e.verb == "binding"  # SIGNOR mechanism is the role-action verb


def test_effect_not_in_policy_is_skipped():
    # NOD2 --up-regulates quantity by expression--> IRF4 ; the activity-only policy omits quantity
    row = _row("NOD2", "protein", "IRF4", "protein", "up-regulates quantity by expression", "txn")
    assert row_to_event(row, POLICY) is None


def test_nonprotein_endpoint_is_skipped():
    # DHFR --down-regulates quantity--> dihydrofolate (a small molecule) -> other network
    row = _row("DHFR", "protein", "dihydrofolate", "smallmolecule", "down-regulates activity")
    assert row_to_event(row, POLICY) is None


def test_verb_falls_back_when_mechanism_blank():
    row = _row("NOD2", "protein", "ATG16L1", "protein", "up-regulates activity", "")
    e = row_to_event(row, POLICY)
    assert e is not None and e.verb == "regulate"


def test_signor_events_filters_the_stream():
    rows = [
        _row("RIPK2", "protein", "TRAF6", "protein", "up-regulates activity"),  # kept
        _row(
            "NOD2", "protein", "IRF4", "protein", "up-regulates quantity by expression"
        ),  # dropped
        _row("DHFR", "protein", "dhf", "smallmolecule", "down-regulates activity"),  # dropped
    ]
    events = signor_events(rows, POLICY)
    assert [(e.subject, e.target, e.sign) for e in events] == [("RIPK2", "TRAF6", 1)]
