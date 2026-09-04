"""homeostat.biophysics — DNA structural mechanics from sequence (the genotype pole's axis 2).

"Structure without structure" in its tightest form: a variant's effect on the LOCAL DNA's mechanical
structure, read straight off the sequence via literature dinucleotide scales -- deterministic, no
annotation. Ported tight from GenomeVault (`biophysical_properties.py`): the phase signal,
rigid (RY-biased) DNA <-> flexible (YR-biased) DNA. A variant that shifts the local YR/RY balance or
bendability sits in a structurally-significant spot. The genotype pole reads the DELTA (variant vs
reference local sequence). Pure over `str`; each decision Detective-pinnable.

Sources: Bolshoy et al. 1991 (bendability, PNAS 88:2312-2316); Drew & Travers 1984 / Trifonov 1980
(YR/RY dinucleotide flexibility). Y = pyrimidine (C, T); R = purine (A, G).
"""

from __future__ import annotations

# Dinucleotide bendability (Bolshoy et al. 1991); higher = more flexible, lower = more rigid.
BENDABILITY = {
    "AA": 0.06,
    "AT": 0.07,
    "TA": 0.07,
    "TT": 0.06,
    "AG": 0.08,
    "GA": 0.08,
    "TG": 0.08,
    "GT": 0.08,
    "AC": 0.09,
    "CA": 0.09,
    "TC": 0.09,
    "CT": 0.09,
    "GG": 0.075,
    "GC": 0.11,
    "CG": 0.09,
    "CC": 0.075,
}
PURINES = frozenset("AG")
PYRIMIDINES = frozenset("CT")


def bendability(dna: str) -> float | None:
    """Mean dinucleotide bendability over the sequence (Bolshoy scale) -- the DNA's flexibility.
    None when the sequence is too short (< 2 bases) or carries no scored dinucleotide (e.g. an
    N-run). Pure over `str`.
    """
    d = dna.upper()
    vals = [BENDABILITY[pair] for i in range(len(d) - 1) if (pair := d[i : i + 2]) in BENDABILITY]
    if not vals:
        return None
    return sum(vals) / len(vals)


def yr_ry_balance(dna: str) -> float | None:
    """The YR/RY balance ``(YR - RY) / (YR + RY)`` -- the rigid<->flexible phase signal.
    YR (pyrimidine->purine) is flexible; RY (purine->pyrimidine) is rigid. Positive = flexible,
    negative = rigid-biased, 0 = balanced (standard coding DNA). None when the sequence carries no
    YR or RY dinucleotide. Pure over `str`.
    """
    d = dna.upper()
    yr = ry = 0
    for i in range(len(d) - 1):
        first, second = d[i], d[i + 1]
        if first in PYRIMIDINES and second in PURINES:
            yr += 1
        elif first in PURINES and second in PYRIMIDINES:
            ry += 1
    total = yr + ry
    if total == 0:
        return None
    return (yr - ry) / total
