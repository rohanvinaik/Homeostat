"""homeostat.position — the per-person OTP positioning layer.

The "position the presentation" step (SYSTEM_DESIGN.md §9), upstream of elimination: before any
candidate is killed, each reading (symptom / lab / vital / treatment-response) becomes a `Position`
on its dimension — a signed-ternary `sign` off the person's OWN mined baseline (prakriti/vikriti,
canon §6.7 — never a population reference range) and a `depth` magnitude. The informational zero
(sign 0) is honest abstention: no reading, or at baseline within tolerance.

A candidate's `signature` is its coordinate across dimensions. Two candidates that SHOULD differ but
share a signature are a structural break in the geometry — the **Discrimination Guarantee** (ported
from Peitho `position.py`): the fix is to ADD A DIMENSION (a new orthogonal measurement), never a
model and never a threshold. That repair is the Jeeves dimension-selector; this module supplies
the positions and the discrimination test it runs on.

Object-agnostic: the `tol` band and WHICH peer-set feeds `mine_zero` are DATA the caller supplies;
nothing here decides a baseline policy or authors an observation. Reuses `otp.ternary` for the
projection (this module is its first production consumer).
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median

from homeostat.otp import ternary
from homeostat.signal import Tier


@dataclass(frozen=True)
class Position:
    """One dimension's signed position for a candidate/observation.

    `sign` is the OTP ternary (+1 above the mined zero / -1 below / 0 the informational zero).
    `depth` is |signed deviation| (magnitude, 0.0 on abstention); `dimension` names the axis; `zero`
    is the mined baseline this position is read against (None when no baseline was available).
    `tier` is the observation's verification grade (VERIFIED can certify; REPORTED banks nothing
    toward a certified verdict), riding to `clinical_verdict` so the read names its trust boundary.
    """

    dimension: str
    sign: int
    depth: float
    zero: float | None
    tier: Tier = Tier.VERIFIED


def deviation(value: float | None, zero: float | None) -> float | None:
    """The signed deviation of a reading from the person's mined baseline: ``value - zero``.

    Returns None — an honest abstention (the informational zero) — when there is no reading
    (``value is None``) or no baseline (``zero is None``). No sign rule imposed: a baseline may be
    any real number (unlike Peitho's sales zero, a physiological setpoint is not ≤0-gated).
    Pure over ``(float | None, float | None)``.
    """
    if value is None or zero is None:
        return None
    return value - zero


def position(
    dimension: str, value: float | None, zero: float | None, tol: float, tier: Tier = Tier.VERIFIED
) -> Position:
    """Place a reading on its deviation dimension: ``sign = ternary(deviation, tol)`` and
    ``depth = |deviation|`` (0.0 on abstention). A None reading or None baseline yields the
    informational zero (sign 0, depth 0.0). `tier` carries the reading's verification grade onto the
    Position. Composition over the pinned `deviation` + `otp.ternary`; intent-tested.
    """
    dev = deviation(value, zero)
    depth = abs(dev) if dev is not None else 0.0
    return Position(dimension, ternary(dev, tol), depth, zero, tier)


def mine_zero(values: list[float | None]) -> float | None:
    """Mine a baseline from a peer-set of comparable readings — the MEDIAN of the present (non-None)
    values (robust to outliers, unlike a mean). Returns None when nothing is present.

    This is the pure prakriti/vikriti primitive (canon §6.7). WHICH peer-set feeds it — a person's
    longitudinal history of an axis, a within-person panel of comparable measures — is the DATA
    layer's call (object-led, §13.1), never decided here. Pure over ``list[float | None]``.
    """
    present = [v for v in values if v is not None]
    if not present:
        return None
    return float(median(present))


def signature(positions: dict[str, Position]) -> tuple[int, ...]:
    """A candidate's ternary signature: its signs across dimensions in a fixed (sorted-by-dimension)
    order — the coordinate the Discrimination Guarantee tests. Pure over ``dict[str, Position]``.
    """
    return tuple(positions[d].sign for d in sorted(positions))


def hamming(sig_a: tuple[int, ...], sig_b: tuple[int, ...]) -> int:
    """The number of dimensions on which two signatures differ, compared position-wise up to the
    shorter length; any length mismatch counts each extra dimension as a difference (a defensive
    over-report — compared signatures should share a dimension set). Pure over two sign-tuples.
    """
    n = min(len(sig_a), len(sig_b))
    shared = sum(1 for i in range(n) if sig_a[i] != sig_b[i])
    return shared + abs(len(sig_a) - len(sig_b))


def discriminates(sig_a: tuple[int, ...], sig_b: tuple[int, ...]) -> bool:
    """The Discrimination Guarantee: do two candidates occupy DIFFERENT positions? True iff their
    signatures differ (Hamming > 0). A False for two candidates that SHOULD differ is a structural
    break in the geometry — the fix is to add a dimension, never a model or a threshold. Pure over
    two sign-tuples.
    """
    return hamming(sig_a, sig_b) > 0
