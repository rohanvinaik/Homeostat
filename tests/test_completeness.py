"""Intent tests for the σ_sem completeness read (SSL §2.5 — "how solved is this mechanism?").
Authored from the design; `resolution_entropy` / `spec_completeness` are Detective-pinned."""

from homeostat.completeness import (
    read_completeness,
    resolution_entropy,
    spec_completeness,
)
from homeostat.jeeves import Probe

_PROBE = Probe("tachycardia", "confirm", {"m1": 1, "m2": -1})

# ---- resolution_entropy: the Hartley conceptual entropy -------------------------------


def test_resolution_entropy_is_log2_of_the_candidate_count():
    assert resolution_entropy(4) == 2.0
    assert resolution_entropy(2) == 1.0


def test_resolution_entropy_one_or_zero_candidates_is_no_uncertainty():
    assert resolution_entropy(1) == 0.0
    assert resolution_entropy(0) == 0.0


# ---- spec_completeness: the metrics from the counts ----------------------------------


def test_spec_completeness_structure_resolved_to_one_is_complete():
    # 4 candidates -> 1 survivor: H_0=2 bits, H_residual=0, structure resolved everything.
    assert spec_completeness(4, 1) == (2.0, 0.0, 1.0)


def test_spec_completeness_a_surviving_plurality_is_partial():
    # 4 -> 2: 1 bit resolved of 2 -> half resolved, 1 bit of I_solve remains.
    assert spec_completeness(4, 2) == (2.0, 1.0, 0.5)


def test_spec_completeness_all_survive_resolves_nothing():
    assert spec_completeness(4, 4) == (2.0, 2.0, 0.0)


def test_spec_completeness_no_initial_uncertainty_is_vacuously_complete():
    assert spec_completeness(1, 1) == (0.0, 0.0, 1.0)


# ---- read_completeness: over the ranked mechanisms -----------------------------------


def test_read_completeness_single_survivor_is_resolved_no_measurement_owed():
    # one mechanism covers the shadow (score > 0), the rest are ruled out -> resolved, no Jeeves.
    sc = read_completeness([("m1", 0.9), ("m2", 0.0), ("m3", 0.0)], _PROBE)
    assert sc.resolved == 1.0 and sc.h_residual == 0.0
    assert sc.i_solve is None  # nothing to discriminate


def test_read_completeness_plurality_owes_the_jeeves_measurement():
    # two mechanisms survive (both score > 0) -> a plurality -> the measurement is owed (I_solve).
    sc = read_completeness([("m1", 0.9), ("m2", 0.5), ("m3", 0.0)], _PROBE)
    assert sc.h_residual == 1.0 and sc.resolved < 1.0
    assert sc.i_solve is _PROBE  # the Jeeves DO-THIS is carried


def test_read_completeness_no_measurement_owed_when_structure_resolves():
    # even with a probe available, a single survivor owes no measurement.
    sc = read_completeness([("m1", 0.9), ("m2", 0.0)], _PROBE)
    assert sc.i_solve is None
