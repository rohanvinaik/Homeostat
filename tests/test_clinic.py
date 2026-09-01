"""Intent tests for the end-to-end clinical read — authored from the design (SYSTEM_DESIGN.md §9),
not generated. Positions decide what is observed; reachability compiles the positive constraints;
censors are the negative sign; a plural residual becomes a Jeeves question or an abstention."""

from homeostat.clinic import (
    ABSTAIN,
    ASK,
    BOTTOM,
    DEGENERATE,
    RESOLVED,
    clinical_verdict,
    observed_symptoms,
    read_from_events,
    read_presentation,
)
from homeostat.event import Event
from homeostat.jeeves import Probe
from homeostat.otp import ORTHOGONAL, SUPPORT
from homeostat.position import Position
from homeostat.web import Coupling, RelationalWeb

# ---- the pure verdict ------------------------------------------------------------


def test_clinical_verdict_all_branches():
    assert clinical_verdict(True, False, False, False) == BOTTOM  # ⊥ outranks everything
    assert clinical_verdict(False, True, True, False) == RESOLVED  # unique + falsifiable
    assert clinical_verdict(False, True, False, False) == DEGENERATE  # unique but self-confirming
    assert clinical_verdict(False, False, False, True) == ASK  # plural + a probe discriminates
    assert clinical_verdict(False, False, False, False) == ABSTAIN  # plural + nothing discriminates


def test_observed_symptoms_filters_the_informational_zero():
    positions = {
        "A": Position("A", SUPPORT, 5.0, 0.0),  # deviated -> observed
        "B": Position("B", ORTHOGONAL, 0.0, 0.0),  # at baseline -> abstains
    }
    assert observed_symptoms(positions) == ["A"]


# ---- the end-to-end read ---------------------------------------------------------


def _dir_web():
    # source -> A, source -> B, decoy -> A (directed): only `source` reaches both symptoms.
    return RelationalWeb(
        (
            Coupling("source", "A", 1.0, +1),
            Coupling("source", "B", 1.0, +1),
            Coupling("decoy", "A", 1.0, +1),
        )
    )


def _positions(*deviated):
    # every named node deviated (SUPPORT); sources sit at baseline (informational zero).
    nodes = {"A", "B", "source", "decoy"}
    return {
        n: Position(n, SUPPORT if n in deviated else ORTHOGONAL, 1.0 if n in deviated else 0.0, 0.0)
        for n in nodes
    }


def test_resolved_recovers_the_unique_source():
    r = read_presentation(_dir_web(), _positions("A", "B"), censors={}, probes=[])
    assert r.verdict == RESOLVED and r.mechanism == "source"


def test_treatment_response_censor_can_certify_bottom():
    # The positive search narrows to `source`; a treatment-response censor rules `source` out ->
    # certified ⊥ (no lawful mechanism), never a false RESOLVED.
    r = read_presentation(_dir_web(), _positions("A", "B"), censors={"tx": ["source"]}, probes=[])
    assert r.verdict == BOTTOM and r.mechanism is None
    assert r.trajectory.survivors_left == []


def _undirected_two_source_web():
    # m1 and m2 both undirected-coupled to symptom S -> both explain S -> plural, unseparated.
    return RelationalWeb((Coupling("m1", "S", 1.0, 0), Coupling("m2", "S", 1.0, 0)))


def _plural_positions():
    # only S is deviated; m1/m2 sit at baseline (informational zero).
    nodes = ("S", "m1", "m2")
    return {n: Position(n, SUPPORT if n == "S" else ORTHOGONAL, 0.0, 0.0) for n in nodes}


def test_plural_residual_becomes_the_jeeves_question():
    splitter = Probe("marker", "confirm", {"m1": 1, "m2": -1, "S": 0})  # splits the survivors
    r = read_presentation(
        _undirected_two_source_web(), _plural_positions(), censors={}, probes=[splitter]
    )
    assert r.verdict == ASK and r.probe is splitter


def test_plural_residual_abstains_when_no_probe_discriminates():
    useless = Probe("flat", "confirm", {"m1": 1, "m2": 1, "S": 1})  # EIG 0
    r = read_presentation(
        _undirected_two_source_web(), _plural_positions(), censors={}, probes=[useless]
    )
    assert r.verdict == ABSTAIN and r.probe is None


# ---- end-to-end from a multi-network event stream --------------------------------


def _reg_events():
    # regulatory (directed) events building: source->A, source->B, decoy->A.
    return [
        Event("regulatory", "amplify", "source", "A", 1),
        Event("regulatory", "amplify", "source", "B", 1),
        Event("regulatory", "amplify", "decoy", "A", 1),
    ]


def test_read_from_events_resolves_from_a_directed_event_web():
    r = read_from_events(
        _reg_events(),
        _positions("A", "B"),
        active_roles=set(),
        probes=[],
        directed_networks={"regulatory"},
    )
    assert r.verdict == RESOLVED and r.mechanism == "source"


def test_read_from_events_active_role_censor_certifies_bottom():
    # a developmental censor rules `source` out FOR role `kinase`; with that role active -> ⊥.
    events = _reg_events() + [Event("developmental", "closes_off", "source", "kinase", -1)]
    r = read_from_events(
        events,
        _positions("A", "B"),
        active_roles={"kinase"},
        probes=[],
        directed_networks={"regulatory"},
    )
    assert r.verdict == BOTTOM and r.mechanism is None
