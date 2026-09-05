"""homeostat.completeness — the σ_sem completeness read: "how solved is this person's mechanism?"

The headline output SSL §2.5 makes possible: turn "have you solved this problem space?" from
rhetoric into a NUMBER. Understanding is the resolution of conceptual degrees of freedom under
constraint (SSL §1.1); a read's conceptual entropy is ``H = log₂|surviving candidate mechanisms|``
(§2.1), and structure (coverage × coherence × the meter) drives it toward 0.

For one person's read, the candidate mechanisms are the ranked story-clusters (`resolve`):
- ``H_0 = log₂(all candidate mechanisms)`` — the initial mechanism-uncertainty, in bits;
- the RANKING (coverage × coherence × meter) separates the losers away, leaving the near-tied
  PLURALITY it could not order (`top_band` — score within a relative band of the top);
- ``H_residual = log₂(plurality)`` — the plurality that remains = ``I_solve``, the information still
  to be TAUGHT (a measurement); ``resolved = (H_0 - H_residual)/H_0`` — SSL's ``L``, the fraction
  structure resolved for FREE (= Completeness at the structural boundary).

When a plurality survives (``H_residual > 0``), a measurement is owed — the mechanism-level Jeeves
DO-THIS (`resolve.cluster_discriminant`): the NODE whose measurement separates the tied mechanisms.
A neural net cannot report this — it has no notion of "these K mechanisms remain, here is the node
whose measurement separates them."
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class SpecCompleteness:
    """The σ_sem completeness of a read. `h0` = ``log₂(candidate mechanisms)``, the initial
    mechanism-uncertainty in bits; `h_residual` = ``log₂(surviving plurality)``, the near-tied
    mechanisms the ranking could not separate — the ``I_solve`` still to measure; `resolved` =
    ``(h0 - h_residual)/h0``, the fraction structure resolved for free (SSL's L; ``1.0`` iff it
    drove the read to a single mechanism); `i_solve` is the NODE to measure (the mechanism-level
    Jeeves DO-THIS) that would separate the surviving plurality, else None."""

    h0: float
    h_residual: float
    resolved: float
    i_solve: str | None


def resolution_entropy(count: int) -> float:
    """The Hartley conceptual entropy ``H = log₂(count)`` over `count` equiprobable candidate
    mechanisms (SSL §2.1). ``count <= 1`` → 0.0 (one or zero candidates carries no uncertainty).
    Pure over ``int``.
    """
    return math.log2(count) if count > 1 else 0.0


def spec_completeness(initial: int, survivors: int) -> tuple[float, float, float]:
    """The completeness metrics ``(h0, h_residual, resolved)`` from the candidate + survivor counts.
    ``h0 = H(initial)``, ``h_residual = H(survivors)`` (both via `resolution_entropy`), and
    ``resolved = (h0 - h_residual)/h0`` — the fraction structure resolved. ``h0 == 0`` (no
    uncertainty to begin with) → ``resolved = 1.0`` (vacuously complete). Pure over ``(int, int)``.
    """
    h0 = resolution_entropy(initial)
    h_residual = resolution_entropy(survivors)
    resolved = (h0 - h_residual) / h0 if h0 > 0 else 1.0
    return h0, h_residual, resolved


def top_band(scores: Sequence[float], band: float) -> list[int]:
    """The indices of the surviving PLURALITY: the candidate mechanisms whose score is positive AND
    within a relative `band` of the top — the near-tie the ranking could not separate (structure
    resolved the rest away). ``score > 0`` and ``score >= top * (1 - band)``. Empty scores or a
    non-positive top → [] (nothing covers); ``band = 0`` → exact top-ties only (the canonical
    symmetric-subtype case ties exactly). Pure over ``(Sequence[float], float)``.
    """
    if not scores:
        return []
    top = max(scores)
    if top <= 0:
        return []
    threshold = top * (1 - band)
    return [i for i, s in enumerate(scores) if s > 0 and s >= threshold]


def read_completeness(initial: int, survivors: int, i_solve: str | None = None) -> SpecCompleteness:
    """The completeness read from the candidate + surviving-plurality counts (the caller derives
    `survivors` via `top_band`, the near-tie the ranking could not separate) and the mechanism-level
    Jeeves node `i_solve` that would separate that plurality (None when structure resolved to one).
    Bundles the pinned `spec_completeness`.
    """
    h0, h_residual, resolved = spec_completeness(initial, survivors)
    return SpecCompleteness(h0, h_residual, resolved, i_solve)
