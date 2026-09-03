"""homeostat.structural -- the biophysics base bank: a physics-orthogonal COMPARTMENT CENSOR.

The deepest, most trustworthy bank. It emits NEGATIVE-sign coupling events from deterministic
sequence biophysics, so a pair of genes whose derived cellular compartments cannot co-exist has its
coupling VETOED: `couple_verdict` returns "killed" when any network censors an edge another asserts,
and "censor" when the physics rules it out alone. This is the edge-fence of
docs/PROTEIN_ROLE_GEOMETRY.md -- not a fold, not an imported structure, not a role classifier, just
the founder's "environments that can't co-exist can't couple", read off the sequence.

Everything here is a PURE decision over a sequence, Detective-pinnable on synthetic strings before
any data. The physical constants are established, not learned: the Kyte-Doolittle hydropathy scale
(Kyte & Doolittle, J Mol Biol 1982) and the standard genetic code. The one biological modelling
choice -- how an N-terminal signal marks secretion -- sits in `has_signal_peptide`, flagged
as the knob to refine; the compatibility rule is the founder's mechanism (disjoint compartments
cannot meet).
"""

from __future__ import annotations

from collections.abc import Mapping

from homeostat.event import Event

STRUCTURAL = "structural"

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

# Transmembrane defaults: a 19-residue window; mean hydropathy >= 1.6 spans a lipid bilayer.
# The signal-peptide h-region is shorter and scanned only over the N-terminus.
TM_WINDOW = 19
TM_THRESHOLD = 1.6
SIGNAL_WINDOW = 8
SIGNAL_THRESHOLD = 1.6
SIGNAL_NTERM = 30


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

    Pure over `(str, int, float)`. Overlapping windows form a single run -> one segment;
    a sequence shorter than the window has no window and returns 0. Deterministic, no orientation.
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


def has_signal_peptide(aa: str) -> bool:
    """Whether an N-terminal secretory signal is present. Pure over `str`.

    THE BIOLOGICAL KNOB (refine, do not trust blindly): a deterministic proxy for a cleavable
    signal peptide -- a `SIGNAL_WINDOW`-residue stretch of mean hydropathy >= `SIGNAL_THRESHOLD` in
    the first `SIGNAL_NTERM` residues. It stands in for "this protein is translocated / secreted"; a
    fuller model (n/h/c regions, the -3/-1 cleavage rule; von Heijne) is the obvious refinement.
    """
    nterm = aa[:SIGNAL_NTERM]
    return any(m >= SIGNAL_THRESHOLD for m in _window_means(nterm, SIGNAL_WINDOW))


def exposure(aa: str) -> str:
    """Classify the compartment the protein's sequence exposes it to -- the code the fence reads.

    Pure over `str`.
    - "membrane"      -- >= 1 span: a spanner is exposed to BOTH sides, so it meets anything.
    - "secreted"      -- 0 spans AND an N-terminal signal: translocated, extracellular/luminal only.
    - "cytoplasmic"   -- 0 spans, no signal: not translocated, intracellular only.
    - "indeterminate" -- too short to read a window: the informational zero, never a fence.
    """
    if len(aa) < TM_WINDOW:
        return "indeterminate"
    if tm_segments(aa) >= 1:
        return "membrane"
    if has_signal_peptide(aa):
        return "secreted"
    return "cytoplasmic"


def compartment_verdict(exposure_a: str, exposure_b: str) -> str:
    """The fence decision for one pair from their exposure codes. Pure over `(str, str)`; symmetric.

    - "incompatible"  -- exactly {"secreted", "cytoplasmic"}: disjoint compartments that never meet,
      so the coupling is physically impossible -> emit the censor (a proof-quality veto).
    - "compatible"    -- a membrane spanner (meets either side), or a shared compartment (both
      secreted / both cytoplasmic): the physics does not forbid it, so emit nothing.
    - "indeterminate" -- either side unread: abstain, the informational zero.
    """
    if exposure_a == "indeterminate" or exposure_b == "indeterminate":
        return "indeterminate"
    if exposure_a == "membrane" or exposure_b == "membrane":
        return "compatible"
    if {exposure_a, exposure_b} == {"secreted", "cytoplasmic"}:
        return "incompatible"
    return "compatible"


def structural_events(proteins: Mapping[str, str]) -> list[Event]:
    """Emit the compartment-censor events for a scoped gene -> protein-sequence map.

    For every unordered gene pair whose exposures are `compartment_verdict`-"incompatible", emit a
    negative-sign `Event` in BOTH orderings (the fence is symmetric; both orderings guarantee it
    contradicts whichever ordering a positive bank drew). `events_to_web` then resolves any edge a
    positive network also asserts to "killed" and drops it. Exposure is computed once per gene, then
    paired; sorted for determinism. Provenance verb "isolates" is data, not a fired role -- a censor
    is read by sign, never verb.
    """
    exps = {gene: exposure(seq) for gene, seq in proteins.items()}
    genes = sorted(exps)
    events: list[Event] = []
    for i, a in enumerate(genes):
        for b in genes[i + 1 :]:
            if compartment_verdict(exps[a], exps[b]) == "incompatible":
                events.append(Event(STRUCTURAL, "isolates", a, b, -1))
                events.append(Event(STRUCTURAL, "isolates", b, a, -1))
    return events


def read_structural(proteins: Mapping[str, str]) -> dict[str, object]:
    """Convenience read: the per-gene exposure map plus the emitted censor events. I/O-free."""
    return {
        "exposure": {gene: exposure(seq) for gene, seq in proteins.items()},
        "censors": structural_events(proteins),
    }
