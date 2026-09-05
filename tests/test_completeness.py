"""Intent tests for the σ_sem completeness read (SSL §2.5 — "how solved is this mechanism?").
Authored from the design; the pure decisions are Detective-pinned."""

from homeostat.completeness import (
    read_completeness,
    resolution_entropy,
    spec_completeness,
    top_band,
)

# ---- resolution_entropy: the Hartley conceptual entropy -------------------------------


def test_resolution_entropy_is_log2_of_the_candidate_count():
    assert resolution_entropy(4) == 2.0
    assert resolution_entropy(2) == 1.0


def test_resolution_entropy_one_or_zero_candidates_is_no_uncertainty():
    assert resolution_entropy(1) == 0.0
    assert resolution_entropy(0) == 0.0


# ---- spec_completeness: the metrics from the counts ----------------------------------


def test_spec_completeness_structure_resolved_to_one_is_complete():
    assert spec_completeness(4, 1) == (2.0, 0.0, 1.0)


def test_spec_completeness_a_surviving_plurality_is_partial():
    assert spec_completeness(4, 2) == (2.0, 1.0, 0.5)


def test_spec_completeness_all_survive_resolves_nothing():
    assert spec_completeness(4, 4) == (2.0, 2.0, 0.0)


def test_spec_completeness_no_initial_uncertainty_is_vacuously_complete():
    assert spec_completeness(1, 1) == (0.0, 0.0, 1.0)


# ---- top_band: the surviving plurality (near-tie the ranking could not separate) -----


def test_top_band_unique_top_is_a_single_survivor():
    assert top_band([1.0, 0.4, 0.0], 0.0) == [0]  # exact: only the top score


def test_top_band_exact_ties_are_the_plurality():
    assert top_band([1.0, 1.0, 0.3], 0.0) == [0, 1]  # two exact ties (the symmetric-subtype case)


def test_top_band_relative_band_includes_near_ties():
    # band 0.2: within 20% of the top (1.0) -> score >= 0.8; 0.9 qualifies, 0.5 does not.
    assert top_band([1.0, 0.9, 0.5], 0.2) == [0, 1]


def test_top_band_no_positive_score_is_empty():
    assert top_band([0.0, 0.0], 0.0) == []
    assert top_band([], 0.0) == []


def test_top_band_only_strictly_positive_scores_survive_even_at_a_full_band():
    # band 1.0 -> threshold 0, but a 0-score is still NOT a covering mechanism: only score > 0
    # survives (the "positive score = covers something" requirement, independent of the band).
    assert top_band([1.0, 0.0], 1.0) == [0]


# ---- read_completeness: bundle the counts + the Jeeves node ---------------------------


def test_read_completeness_single_survivor_is_resolved_no_measurement():
    # 4 candidates, ranking resolved to 1 -> complete, nothing to measure.
    sc = read_completeness(4, 1, None)
    assert sc.resolved == 1.0
    assert sc.h_residual == 0.0
    assert sc.i_solve is None


def test_read_completeness_plurality_carries_the_jeeves_node():
    # 2 of 4 survive as a near-tie -> half resolved, and the node to measure is carried.
    sc = read_completeness(4, 2, "TP53")
    assert sc.h_residual == 1.0
    assert sc.resolved == 0.5
    assert sc.i_solve == "TP53"
