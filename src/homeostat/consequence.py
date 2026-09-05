"""homeostat.consequence — the genotype consequence VECTOR: a variant's deterministic effect on its
gene, as a dense feature vector for fungibility-by-cosine (the genotype pole's shape, design A).

A genotype is a PRIOR on the mechanism (docs/GENOTYPE_POLE.md), never an observation. Its magnitude
is the CONSEQUENCE of the variant -- how much it changes what the gene can do -- read
across orthogonal axes:
- structural-consequence (this module): the variant's effect on the PROTEIN (`structural.py`:
  structural_class flip + composition / gravy / charge / aromaticity deltas);
- biophysics (`biophysics.py`): its effect on the local DNA structural mechanics;
- presence/rarity: the reference-departure gate.

Two variants whose consequence vectors are SIMILAR are fungible for the mechanism (cosine, at the
interpretive layer -- never in the elimination gate). Pure over strings/tuples; Detective-pinnable.
"""

from __future__ import annotations

from math import sqrt

from homeostat.biophysics import bendability, yr_ry_balance
from homeostat.structural import (
    aromaticity,
    composition,
    composition_distance,
    gravy,
    net_charge,
    structural_class,
)

_CONFIDENT = frozenset({"membrane", "soluble"})


def class_shift(ref_class: str, var_class: str) -> float:
    """The magnitude of a structural-class change: 0.0 same class; 1.0 a confident FLIP
    (membrane<->soluble, a physical can't-be-both change -- the biggest functional shift); 0.5 a
    partial shift to/from `uncertain` (one side abstains). Pure over `(str, str)`.
    """
    if ref_class == var_class:
        return 0.0
    if ref_class in _CONFIDENT and var_class in _CONFIDENT:
        return 1.0
    return 0.5


def structural_consequence(ref_aa: str, var_aa: str) -> tuple[float, float, float, float, float]:
    """The variant's structural consequence on the protein, as five non-negative deltas: the
    class-shift magnitude, the composition L1 distance, and the ``|delta|`` in gravy / net charge /
    aromaticity. Orchestration over the pinned `structural.py` reads; intent-tested.
    """
    return (
        class_shift(structural_class(ref_aa), structural_class(var_aa)),
        composition_distance(composition(ref_aa), composition(var_aa)),
        abs(gravy(ref_aa) - gravy(var_aa)),
        abs(net_charge(ref_aa) - net_charge(var_aa)),
        abs(aromaticity(ref_aa) - aromaticity(var_aa)),
    )


def _delta(ref_val: float | None, var_val: float | None) -> float:
    """``|ref - var|`` when both present, else 0.0 -- a missing measure carries no delta
    (the informational zero). Pure over `(float | None, float | None)`.
    """
    if ref_val is None or var_val is None:
        return 0.0
    return abs(ref_val - var_val)


def biophysics_consequence(ref_dna: str, var_dna: str) -> tuple[float, float]:
    """The variant's effect on the local DNA structural mechanics, as two non-negative deltas:
    ``|d bendability|`` and ``|d (YR/RY balance)|``. A missing measure (no-dinucleotide
    sequence) contributes 0.0. Orchestration over pinned `biophysics.py`; intent-tested.
    """
    return (
        _delta(bendability(ref_dna), bendability(var_dna)),
        _delta(yr_ry_balance(ref_dna), yr_ry_balance(var_dna)),
    )


def consequence_vector(
    ref_aa: str, var_aa: str, ref_dna: str, var_dna: str, rarity: float
) -> tuple[float, ...]:
    """The full consequence vector (design A, dense): the five structural-consequence deltas,
    then the two biophysics deltas, then the presence/rarity gate. Non-negative throughout; the zero
    vector is a variant of no measured consequence. Orchestration; intent-tested.
    """
    return (
        *structural_consequence(ref_aa, var_aa),
        *biophysics_consequence(ref_dna, var_dna),
        rarity,
    )


def consequence_similarity(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    """Cosine similarity of two consequence vectors -- the genotype-level FUNGIBILITY read: two
    variants whose consequences point the same way are fungible for the mechanism. In [0, 1] (the
    vectors are non-negative). A zero vector has no direction, so similarity is 0.0 -- never a
    spurious 1.0. Pure over equal-length tuples.
    """
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = sqrt(sum(x * x for x in a))
    nb = sqrt(sum(y * y for y in b))
    if not na or not nb:
        return 0.0
    return dot / (na * nb)
