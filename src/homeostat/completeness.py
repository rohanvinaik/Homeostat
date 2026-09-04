"""homeostat.completeness — the σ_sem completeness read: "how solved is this person's mechanism?"

The headline output SSL §2.5 makes possible: turn "have you solved this problem space?" from
rhetoric into a NUMBER. Understanding is the resolution of conceptual degrees of freedom under
constraint (SSL §1.1); a read's conceptual entropy is ``H = log₂|surviving candidate mechanisms|``
(§2.1), and structure (coverage × coherence × the meter) drives it toward 0.

For one person's read, the candidate mechanisms are the ranked story-clusters (`resolve`):
- ``H_0 = log₂(all candidate mechanisms)`` — the initial mechanism-uncertainty, in bits;
- structure RULES OUT the mechanisms that explain none of the shadow (score 0 — no coverage /
  coherence / confirmation), leaving the SURVIVORS it could not eliminate;
- ``H_residual = log₂(survivors)`` — the plurality that remains = ``I_solve``, the information still
  to be TAUGHT (a measurement); ``resolved = (H_0 - H_residual)/H_0`` — SSL's ``L``, the fraction
  structure resolved for FREE (= Completeness at the structural boundary).

When a plurality survives (``H_residual > 0``), a measurement is owed — the Jeeves DO-THIS. (For now
that is the elimination-level probe `drive` already selected; the mechanism-level Jeeves that
discriminates the cluster plurality directly is resolve increment 3.) A neural net cannot report
this — it has no notion of "these K mechanisms remain, here is the measurement that separates them."
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

from homeostat.jeeves import Probe


@dataclass(frozen=True)
class SpecCompleteness:
    """The σ_sem completeness of a read. `h0` = ``log₂(candidate mechanisms)``, the initial
    mechanism-uncertainty in bits; `h_residual` = ``log₂(surviving mechanisms)``, the plurality
    structure could not rule out — the ``I_solve`` still to be measured; `resolved` = ``(h0 -
    h_residual)/h0``, the fraction structure resolved for free (SSL's L; ``1.0`` iff it drove the
    read to a single mechanism); `i_solve` is the discriminating measurement owed when a plurality
    remains (the Jeeves DO-THIS), else None."""

    h0: float
    h_residual: float
    resolved: float
    i_solve: Probe | None


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


def read_completeness(
    ranked: Sequence[tuple[object, float]], probe: Probe | None = None
) -> SpecCompleteness:
    """The completeness read over the ranked candidate mechanisms (`resolve.rank_clusters` output):
    ``initial`` = all candidates, ``survivors`` = those structure did NOT rule out (score > 0 — they
    cover / cohere / confirm some of the shadow). The Jeeves `probe` is carried as ``i_solve`` ONLY
    when a plurality survives (``survivors > 1``) — a measurement is owed exactly then. Over the
    pinned `spec_completeness`.
    """
    initial = len(ranked)
    survivors = sum(1 for _, score in ranked if score > 0.0)
    h0, h_residual, resolved = spec_completeness(initial, survivors)
    i_solve = probe if survivors > 1 else None
    return SpecCompleteness(h0, h_residual, resolved, i_solve)
