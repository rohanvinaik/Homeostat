"""homeostat.signal — the tiered sub-threshold signal (a faithful container).

A signal is one observed sub-threshold datum about an individual, carried with its
**verification tier** — the informational-zero discipline made explicit, straight from
the index-case genetic summary's ✓/○ tiering:

    VERIFIED  — directly present in the queryable data (the summary's ✓).
    REPORTED  — from an interpretation/report layer; the underlying datum is NOT
                independently re-verifiable here (the summary's ○). May be correct, but
                cannot carry weight until confirmed.
    ABSENT    — not present in the data at all (the array does not type it, etc.).

This module is a faithful CONTAINER only. It does NOT decide how a tier becomes a ternary
state, how signals combine, or what coheres — those are the coherence mechanism and the
constraint object, which are the design conversation, not baked in here. Recording the
tier without collapsing it is the whole point: an unverified signal and an absent one are
different, and both differ from a verified one. Annotation (association magnitudes,
directions) is deliberately NOT a field — it is held out (§3.1) for the falsifier.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Tier(str, Enum):
    """Verification tier of a signal — the ✓/○/absent distinction, kept typed."""

    VERIFIED = "verified"  # ✓ directly present in the data
    REPORTED = "reported"  # ○ report-layer, not independently re-verifiable
    ABSENT = "absent"  # not typed / not present at all


@dataclass(frozen=True)
class Signal:
    """One observed sub-threshold datum about an individual, with its tier.

    ``ident`` names the datum (e.g. a variant id or a marker). ``state`` is the raw
    observed value as a string (e.g. a genotype ``"A;G"``), kept verbatim — no
    normalization and no association magnitude (annotation is held out). ``tier`` is its
    verification tier. This is the input the coherence instrument consumes; it commits to
    nothing about how the datum is scored.
    """

    ident: str
    state: str
    tier: Tier
