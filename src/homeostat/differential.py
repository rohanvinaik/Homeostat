"""homeostat.differential — the STRUCTURED differential (GDiff-ported): a deviation is not a scalar
but a typed, information-weighted difference read against a REFERENCE DISTRIBUTION, not a point.

Ported from GenomeVault's GDiff `differential_context` (genomevault/docs/GDIFF_RATIONALE.md): a
difference carries a KIND (`diff_type`), an information content (`local_entropy`), and a confidence,
read against a pool/template rather than a single reference. Here, per axis:

- the reference is a distribution SUMMARY (center + spread), mined from the peer-set (`mine_spread`
  is the dispersion twin of `position.mine_zero`'s median);
- `surprise` is the standardized departure ``|value - center| / spread`` -- monotone in -log P, the
  information content of the deviation: a departure into a tightly-constrained (low-spread) region
  carries MORE information than the same departure into a loose one (significance-weighting's
  "depth weighted by the branching freedom the reference afforded");
- `kind` is the TYPED departure (elevated / depleted / none for a marker; richer genotype kinds
  ride the same slot).

The elimination engine consumes only the Position's signed coordinate; THIS rich structure rides
alongside (`Position.differential`) for the interpretive layer (fungibility / roles / Regenesis).
Pure over floats; each decision Detective-pinnable.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median

ELEVATED = "elevated"  # value above the reference band
DEPLETED = "depleted"  # value below the reference band
NONE = "none"  # within the band -- the informational zero


@dataclass(frozen=True)
class Differential:
    """The structured differential on one axis: `kind` (the typed departure), `surprise` (the
    standardized departure ``|value-center|/spread``, monotone in -log P -- information content),
    and `spread` (the reference dispersion, None when no baseline). Read alongside the
    Position's `zero` (the center), it summarizes the full information-theoretic deviation.
    """

    kind: str
    surprise: float
    spread: float | None


def mine_spread(values: list[float | None]) -> float | None:
    """The reference distribution's dispersion: the MEDIAN ABSOLUTE DEVIATION of the present values
    (robust, the dispersion twin of `position.mine_zero`'s median). None when nothing is present.
    Pure over `list[float | None]`.
    """
    present = [v for v in values if v is not None]
    if not present:
        return None
    center = median(present)
    return float(median([abs(v - center) for v in present]))


def surprise(value: float | None, center: float | None, spread: float | None) -> float:
    """The information content of a deviation: the standardized departure ``|value - center| /
    spread`` -- monotone in -log P against the reference distribution. 0.0 on abstention (a missing
    reading or baseline) and on a degenerate reference (spread None or <= 0): a reference with no
    dispersion carries no surprise SCALE, so the honest reading is the informational zero, never a
    division blow-up. Pure over `(float?, float?, float?)`.
    """
    if value is None or center is None or spread is None or spread <= 0.0:
        return 0.0
    return abs(value - center) / spread


def differential_kind(
    value: float | None, center: float | None, spread: float | None, k: float
) -> str:
    """The TYPED departure: ELEVATED / DEPLETED when the reading is above / below the reference by
    more than `k` spreads, else NONE (within the band -- the informational zero). A missing reading,
    a missing baseline, or a degenerate reference (spread None or <= 0) is NONE. `k` is the band
    width in SPREAD-UNITS (surprising = beyond k spreads), the principled replacement for absolute
    tolerance. Pure over `(float?, float?, float?, float)`.
    """
    if value is None or center is None or spread is None or spread <= 0.0:
        return NONE
    if value - center > k * spread:
        return ELEVATED
    if center - value > k * spread:
        return DEPLETED
    return NONE


def make_differential(
    value: float | None, center: float | None, spread: float | None, k: float
) -> Differential:
    """Compose the structured differential from a reading against its mined reference distribution:
    the typed `kind`, the `surprise` (standardized departure), and the reference `spread`.
    Orchestration over the pinned `differential_kind` / `surprise`; intent-tested.
    """
    return Differential(
        differential_kind(value, center, spread, k), surprise(value, center, spread), spread
    )
