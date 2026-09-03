"""Intent tests for the structural biophysics base -- the confidence-gated structural-class read.

Authored from intent, not characterization: from pure sequence, a MULTI-pass hydrophobic profile is
confidently integral-membrane and a zero-span profile is confidently soluble; the ambiguous middle
(1-2 spans -- a single-pass TM or an internal patch) abstains. Two proteins in different confident
classes cannot be one fungible role (incompatible); same class or any abstention does not bar.
"""

from homeostat.structural import (
    structural_class,
    structural_compatibility,
    tm_segments,
    translate,
)

# Three hydrophobic runs separated by acidic gaps wider than a window -> 3 confident spans.
MULTIPASS = "L" * 25 + "D" * 20 + "I" * 25 + "D" * 20 + "V" * 25
# Hydrophilic throughout: zero spans -> confidently not integral-membrane.
SOLUBLE = "D" * 60
# One internal hydrophobic span: could be single-pass TM or an internal patch -> not confident.
SINGLE = "D" * 15 + "L" * 25 + "D" * 15
# Too short to read one window.
SHORT = "ML"


def test_translate_reads_triplets_stops_and_drops_bad_codons():
    assert translate("ATGGCCTAA") == "MA"  # M, A, then stop truncates
    assert translate("atgttg") == "ML"  # case-insensitive
    assert translate("ATGNNNGCC") == "MA"  # the unknown NNN codon is dropped, not guessed
    assert translate("AT") == ""  # a partial codon yields nothing


def test_tm_segments_counts_maximal_hydrophobic_runs():
    assert tm_segments("D" * 40) == 0  # hydrophilic: no span
    assert tm_segments("L" * 25) == 1  # one long hydrophobic helix is one segment
    assert tm_segments(MULTIPASS) == 3  # three spans separated by wide loops
    assert tm_segments("ML") == 0  # shorter than one window


def test_structural_class_speaks_only_when_confident():
    assert structural_class(MULTIPASS) == "membrane"  # >= 3 spans: confident multi-pass
    assert structural_class(SOLUBLE) == "soluble"  # 0 spans: confidently not integral-membrane
    assert structural_class(SINGLE) == "uncertain"  # 1 span: ambiguous -> abstain
    assert structural_class(SHORT) == "uncertain"  # too short -> abstain


def test_structural_compatibility_bars_only_confident_conflicts():
    assert structural_compatibility("membrane", "soluble") == "incompatible"
    assert structural_compatibility("soluble", "membrane") == "incompatible"  # symmetric
    assert structural_compatibility("membrane", "membrane") == "compatible"  # same confident class
    assert structural_compatibility("soluble", "soluble") == "compatible"
    assert structural_compatibility("uncertain", "soluble") == "indeterminate"  # abstain
    assert structural_compatibility("membrane", "uncertain") == "indeterminate"
