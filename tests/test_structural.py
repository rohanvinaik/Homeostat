"""Intent tests for the structural biophysics bank -- the physics-orthogonal compartment censor.

Authored from intent, not characterization: a protein sequence reads to a compartment exposure by
deterministic Kyte-Doolittle hydropathy, and two genes whose exposures are disjoint (one secreted,
one cytoplasmic) can never meet, so their coupling is censored (a negative-sign Event the two-sign
engine resolves to "killed"). Synthetic sequences chosen so each biophysical class is unambiguous.
"""

from homeostat.structural import (
    STRUCTURAL,
    compartment_verdict,
    exposure,
    has_signal_peptide,
    structural_events,
    tm_segments,
    translate,
)

# A clean membrane spanner: a 25-residue leucine run (KD 3.8) flanked by acidic loops (KD -3.5).
MEMBRANE = "D" * 10 + "L" * 25 + "D" * 10
# A secreted protein: a short N-terminal hydrophobic h-region (10 L), too short to span, then polar.
SECRETED = "L" * 10 + "D" * 40
# A cytoplasmic protein: hydrophilic throughout, no N-terminal signal.
CYTOPLASMIC = "D" * 40
# Too short to read one transmembrane window.
SHORT = "ML"


def test_translate_reads_triplets_stops_and_drops_bad_codons():
    assert translate("ATGGCCTAA") == "MA"  # M, A, then stop truncates
    assert translate("atgttg") == "ML"  # case-insensitive
    assert translate("ATGNNNGCC") == "MA"  # the unknown NNN codon is dropped, not guessed
    assert translate("AT") == ""  # a partial codon yields nothing


def test_tm_segments_counts_maximal_hydrophobic_runs():
    assert tm_segments("D" * 40) == 0  # hydrophilic: no span
    assert tm_segments("L" * 25) == 1  # one long hydrophobic helix is one segment
    assert tm_segments("L" * 25 + "D" * 20 + "I" * 25) == 2  # two spans separated by a loop
    assert tm_segments("ML") == 0  # shorter than one window


def test_signal_peptide_needs_an_nterminal_hydrophobic_hregion():
    assert has_signal_peptide(SECRETED) is True
    assert has_signal_peptide(CYTOPLASMIC) is False


def test_exposure_classes():
    assert exposure(MEMBRANE) == "membrane"  # span present -> exposed both sides
    assert exposure(SECRETED) == "secreted"  # signal, no span -> extracellular only
    assert exposure(CYTOPLASMIC) == "cytoplasmic"  # no signal, no span -> intracellular only
    assert exposure(SHORT) == "indeterminate"  # nothing to read -> informational zero


def test_compartment_verdict_fences_only_disjoint_compartments():
    assert compartment_verdict("secreted", "cytoplasmic") == "incompatible"
    assert compartment_verdict("cytoplasmic", "secreted") == "incompatible"  # symmetric
    assert (
        compartment_verdict("membrane", "cytoplasmic") == "compatible"
    )  # spanner meets either side
    assert compartment_verdict("membrane", "secreted") == "compatible"
    assert compartment_verdict("secreted", "secreted") == "compatible"  # shared compartment
    assert compartment_verdict("cytoplasmic", "cytoplasmic") == "compatible"
    assert compartment_verdict("indeterminate", "cytoplasmic") == "indeterminate"  # abstain


def test_structural_events_emits_symmetric_censor_for_incompatible_pairs_only():
    censors = structural_events({"S": SECRETED, "C": CYTOPLASMIC})
    # both orderings of the one disjoint pair, each a negative-sign structural censor
    assert len(censors) == 2
    assert {(e.subject, e.target) for e in censors} == {("C", "S"), ("S", "C")}
    assert all(e.sign == -1 and e.network == STRUCTURAL for e in censors)

    # a membrane spanner meets either side: no fence
    assert structural_events({"M": MEMBRANE, "C": CYTOPLASMIC}) == []
