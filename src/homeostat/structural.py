"""homeostat.structural -- the biophysics base: a CONFIDENCE-GATED structural-class read.

Its job in the story math: bar two proteins from resolving to the SAME fungible role when they are
physically incompatible -- the subfunctionalized-paralog case (fungibility.py). Not a coupling veto,
not a fold, not an imported structure: a CLASS read off the sequence that speaks only when
CONFIDENT and otherwise abstains (the OTP informational zero).

The lesson that shaped it (fire-before-trust): an earlier version hard-called an ambiguous read (one
N-terminal hydrophobic window -> "secreted") and false-vetoed real cytoplasmic proteins. The fix is
not more data nor a weaker statistic -- it is Homeostat's own confidence discipline: propagate only
CONFIDENT facts, abstain on ambiguity. From pure sequence two classes are confident -- multi-pass
integral membrane (>= MEMBRANE_MIN_SPANS spans) and fully soluble (0 spans); the ambiguous middle
(1-2 spans: single-pass vs an internal patch) abstains. Constants are established physics (Kyte &
Doolittle 1982; the genetic code), never learned. The thresholds are the biological knob.
"""

from __future__ import annotations

TM_WINDOW = 19
TM_THRESHOLD = 1.6
# A confident integral-membrane protein is MULTI-pass: a single hydrophobic window is as likely an
# internal patch of a soluble protein (the LRRK2/NOD2 false positive), not confident. The knob.
MEMBRANE_MIN_SPANS = 3

# Kyte-Doolittle hydropathy (positive = hydrophobic). Established physical constants, not learned.
KYTE_DOOLITTLE: dict[str, float] = {
    "A": 1.8,
    "R": -4.5,
    "N": -3.5,
    "D": -3.5,
    "C": 2.5,
    "Q": -3.5,
    "E": -3.5,
    "G": -0.4,
    "H": -3.2,
    "I": 4.5,
    "L": 3.8,
    "K": -3.9,
    "M": 1.9,
    "F": 2.8,
    "P": -1.6,
    "S": -0.8,
    "T": -0.7,
    "W": -0.9,
    "Y": -1.3,
    "V": 4.2,
}

# The standard genetic code (codon -> amino acid; "*" = stop). A fixed biological fact, not a prior.
CODON_TABLE: dict[str, str] = {
    "TTT": "F",
    "TTC": "F",
    "TTA": "L",
    "TTG": "L",
    "CTT": "L",
    "CTC": "L",
    "CTA": "L",
    "CTG": "L",
    "ATT": "I",
    "ATC": "I",
    "ATA": "I",
    "ATG": "M",
    "GTT": "V",
    "GTC": "V",
    "GTA": "V",
    "GTG": "V",
    "TCT": "S",
    "TCC": "S",
    "TCA": "S",
    "TCG": "S",
    "CCT": "P",
    "CCC": "P",
    "CCA": "P",
    "CCG": "P",
    "ACT": "T",
    "ACC": "T",
    "ACA": "T",
    "ACG": "T",
    "GCT": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",
    "TAT": "Y",
    "TAC": "Y",
    "TAA": "*",
    "TAG": "*",
    "CAT": "H",
    "CAC": "H",
    "CAA": "Q",
    "CAG": "Q",
    "AAT": "N",
    "AAC": "N",
    "AAA": "K",
    "AAG": "K",
    "GAT": "D",
    "GAC": "D",
    "GAA": "E",
    "GAG": "E",
    "TGT": "C",
    "TGC": "C",
    "TGA": "*",
    "TGG": "W",
    "CGT": "R",
    "CGC": "R",
    "CGA": "R",
    "CGG": "R",
    "AGT": "S",
    "AGC": "S",
    "AGA": "R",
    "AGG": "R",
    "GGT": "G",
    "GGC": "G",
    "GGA": "G",
    "GGG": "G",
}


def translate(cds: str) -> str:
    """Translate an in-frame coding sequence to protein, stopping at the first stop codon.

    Pure over `str`: upper-cased, read in non-overlapping triplets; a trailing partial codon or any
    codon with a non-ACGT letter is dropped (not guessed). Returns the protein up to the first "*".
    """
    seq = cds.upper()
    out: list[str] = []
    for i in range(0, len(seq) - 2, 3):
        aa = CODON_TABLE.get(seq[i : i + 3])
        if aa is None:
            continue
        if aa == "*":
            break
        out.append(aa)
    return "".join(out)


def _window_means(aa: str, window: int) -> list[float]:
    """Mean Kyte-Doolittle hydropathy over each sliding window of `window` residues (unknown = 0.0).

    Pure. Empty when the sequence is shorter than one window -- nothing to average, not a zero.
    """
    if window <= 0 or len(aa) < window:
        return []
    vals = [KYTE_DOOLITTLE.get(c, 0.0) for c in aa]
    means: list[float] = []
    running = sum(vals[:window])
    means.append(running / window)
    for i in range(window, len(vals)):
        running += vals[i] - vals[i - window]
        means.append(running / window)
    return means


def tm_segments(aa: str, window: int = TM_WINDOW, threshold: float = TM_THRESHOLD) -> int:
    """Count membrane spans: maximal runs of windows whose mean hydropathy >= `threshold`.

    Pure over `(str, int, float)`. Overlapping windows form a single run -> one segment; a sequence
    shorter than the window has no window and returns 0. Deterministic, no orientation.
    """
    means = _window_means(aa, window)
    segments = 0
    in_run = False
    for m in means:
        if m >= threshold:
            if not in_run:
                segments += 1
                in_run = True
        else:
            in_run = False
    return segments


def structural_class(aa: str) -> str:
    """The CONFIDENCE-GATED structural class of a protein -- the code the fungibility gate reads.

    Pure over `str`. Only confident calls speak; the ambiguous middle abstains.
    - "membrane"  -- >= MEMBRANE_MIN_SPANS spans: a confident MULTI-pass integral membrane protein.
    - "soluble"   -- 0 spans: confidently NOT integral-membrane (not secreted-vs-cytosol).
    - "uncertain" -- 1..MEMBRANE_MIN_SPANS-1 spans, or too short: the informational zero.
    """
    if len(aa) < TM_WINDOW:
        return "uncertain"
    spans = tm_segments(aa)
    if spans >= MEMBRANE_MIN_SPANS:
        return "membrane"
    if spans == 0:
        return "soluble"
    return "uncertain"


def structural_compatibility(class_a: str, class_b: str) -> str:
    """Whether two proteins' confident classes let them be the SAME role. Pure; symmetric.

    - "incompatible"  -- DIFFERENT confident classes (membrane vs soluble): an integral multi-pass
      membrane protein and a fully soluble one cannot be one role -> BAR the fungibility merge.
    - "compatible"    -- the same confident class (both membrane / both soluble): no barrier.
    - "indeterminate" -- either class "uncertain": abstain, the informational zero, never a bar.
    """
    if class_a == "uncertain" or class_b == "uncertain":
        return "indeterminate"
    if class_a != class_b:
        return "incompatible"
    return "compatible"
