"""homeostat.producer — the positions PRODUCER: a person's readings become the read's input,
`dict[node, Position]`, each a structured differential against its reference.

MARKER path (this module's v1): a marker's reference is a PUBLISHED demographic interval [low, high]
(looked up by marker + demographics). The population norm reads the OBSERVATION -- is a marker
abnormal -- never the MECHANISM (which pathway the shadow implicates; the geometry reads that
population-free). This SHARPENS Law 1 rather than breaking it (Law 1 forbids a frequency becoming
the VERDICT, never a reference range lighting a pixel of the shadow -- docs/decisions/).

The interval IS the informational-zero band: `reference_center_spread` converts [low, high] to
(center, spread), and `position.place` reads the deviation against it with k=1. The reference is
GIVEN, not mined -- `mine_zero`/`mine_spread` are for the DISCOVERED (gene/pathway) references, not
markers. The literature table itself (`(marker, demographic) -> [low, high]`) is the data seam.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from math import isfinite

from homeostat.ground import ground
from homeostat.position import Position, place
from homeostat.signal import Signal


def reference_center_spread(low: float, high: float) -> tuple[float, float]:
    """Convert a published reference interval [low, high] to the (center, spread) a Position reads
    against: the midpoint and the half-width. With k=1 the informational-zero band is exactly
    [low, high] -- inside is normal (NONE), outside is ELEVATED/DEPLETED, and `surprise` counts
    half-widths into the tail. A malformed interval (high < low) yields a negative spread, which
    `place` reads as a degenerate reference (abstain). Pure over `(float, float)`.
    """
    center = (low + high) / 2.0
    spread = (high - low) / 2.0
    return center, spread


def parse_marker(state: str) -> float | None:
    """Parse a marker's raw state string to a FINITE float, or None when it is not a numeric marker
    -- a genotype ("A;G"), a unit-laden or empty string. A None is an honest skip: the reading is
    not a numeric marker this producer places (a genotype defers to the genotype pole). Pure over
    `str`.
    """
    try:
        value = float(state)
    except (TypeError, ValueError):
        return None
    return value if isfinite(value) else None


def signals_to_positions(
    signals: Iterable[Signal],
    demographics: Mapping[str, str],
    reference: Callable[[str, Mapping[str, str]], tuple[float, float] | None],
    vocab: dict[str, str],
    k: float = 1.0,
) -> dict[str, Position]:
    """Produce the read's input from a person's marker readings: each Signal grounded to a node,
    looked up against its demographic reference interval, and PLACED as a structured Position (the
    signed coordinate + differential + tier). A reading is honestly DROPPED -- never faked -- when
    it is ungroundable, non-numeric (a genotype, deferred), or has no demographic reference. The
    covariate correction lives entirely in `reference`'s key: age 8 and age 80 resolve to different
    intervals, so a normal-for-age value never reads as a deviation. Orchestration over the pinned
    `ground` / `parse_marker` / `reference_center_spread` / `place`; integration-tested end to end.
    """
    out: dict[str, Position] = {}
    for sig in signals:
        node = ground(sig.ident, vocab).node
        if node is None:
            continue
        value = parse_marker(sig.state)
        if value is None:
            continue
        interval = reference(node, demographics)
        if interval is None:
            continue
        center, spread = reference_center_spread(*interval)
        out[node] = place(node, value, center, spread, k, sig.tier)
    return out
