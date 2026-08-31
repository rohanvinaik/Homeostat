"""L2 role encoder — pure decisions turning a gene's data-signals into L3 role-facts.

The signal layer (Fst differentiation over 1000G, GTEx co-expression) is computed by the
I/O shell; these are the pure, Detective-pinnable cores: given a gene's binned signals,
emit the L3 fact sentences (opaque token · role verb · literal object — transitive).

Directed signaling roles (senses/relays/amplifies) are NOT emitted here — they come from the
known-mechanism substrate (docs/ETIOLOGY_ENGINE.md §2b). L2 emits the data-derived roles
(§3b): population differentiation (the genetic lens), co-expression with the mechanism seed
(the expression lens), and the informational zero when the genetic lens has no data.

GRADED INTENSITY (GSE-native, docs/ETIOLOGY_ENGINE.md §3b): intensity is NOT a continuous
scalar — GSE rejects "arbitrary scalar multiples" and carries magnitude as discrete ORDINAL
markers stacked on a base primitive, which only reaches significance by becoming STRUCTURE
(a stronger tier fires an extra rule → deeper chain → higher κ). So the Fst magnitude is
binned into ordinal tiers and a top-tier gene STACKS an intensity marker (`dominates
population`) on the base fact (`differentiates population`); the universe's graded rule turns
that stack into a deeper derivation. Magnitude bands are the conventional Wright Fst
interpretation (>0.25 very-great, 0.05-0.25 moderate, <0.05 little) — principled, not tuned.
"""

from __future__ import annotations

DOMINANT_FST = 0.25  # Wright: very-great differentiation
MODERATE_FST = 0.05  # Wright: floor of moderate differentiation


def diff_tier(fst: float | None) -> str:
    """Bin a gene's max-pairwise Fst into an ordinal differentiation tier.

    None = the genetic lens has no data on the gene (abstain). Bands are Wright's conventional
    Fst interpretation, so the tier is a property of the magnitude, not a tuned cut.
    """
    if fst is None:
        return "nodata"
    if fst >= DOMINANT_FST:
        return "dominant"
    if fst >= MODERATE_FST:
        return "moderate"
    return "none"


def data_facts(token: str, tier: str, coexpresses_seed: bool, binds_seed: bool) -> list[str]:
    """The L3 facts a gene's binned data-signals license, as sentence strings.

    `nodata` -> the informational zero (`lacks data`, never silence). `dominant` stacks an
    intensity marker (`dominates population`) on the base differentiation fact — the ordinal
    "marker on a base primitive" that the universe's graded rule deepens. `moderate` emits the
    base only. `none` (has data, below the floor) licenses no differentiation fact. Co-expression
    (GTEx) and physical binding (STRING) are two further independent lenses — each an orthogonal
    surface, so a gene confirmed by more of them accumulates more converging facts (density -> κ).
    """
    facts: list[str] = []
    if tier == "nodata":
        facts.append(f"{token} lacks data")
    elif tier == "dominant":
        facts.append(f"{token} differentiates population")
        facts.append(f"{token} dominates population")
    elif tier == "moderate":
        facts.append(f"{token} differentiates population")
    if coexpresses_seed:
        facts.append(f"{token} tracks seed")
    if binds_seed:
        facts.append(f"{token} binds seed")
    return facts
