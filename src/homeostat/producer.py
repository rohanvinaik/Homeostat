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
