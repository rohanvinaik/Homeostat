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
