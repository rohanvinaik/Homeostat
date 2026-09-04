"""homeostat.recommend — the PREFER layer: rank the require-survivors into a recommendation.

The read is a RECOMMENDATION ENGINE over mechanisms (classical AI, no embeddings), ported tight from
ModelAtlas's `navigate`. REQUIRE (directed-cone + two-sign elimination) hard-filters the admitted
candidates; PREFER ranks them by a MULTIPLICATIVE product of alignment factors (kappa-coverage,
shadow-direction alignment, coherence -- each in [0, 1], so failing one demotes) TIMES a SUBMODULAR
combine of the soft info-theoretic signals (convergence, rarity/H5, absence/H6 -- rewards, so the
score is not bounded at 1). The output is a RANKED list, never a flat survivor set.

The pure ranking DECISIONS live here; the per-candidate signals are DATA the caller extracts from
the web / positions (kept separate so the ported blend carries no domain translation).
"""

from __future__ import annotations

from collections.abc import Sequence

# Each next-strongest soft signal counts by decay^rank -- a calibration knob, not a load-bearing
# constant (ModelAtlas tunes its own). The design is the diminishing-returns shape, not the value.
SUBMODULAR_DECAY = 0.5


def submodular_combine(signals: Sequence[float], decay: float = SUBMODULAR_DECAY) -> float:
    """Combine soft-signal deltas with DIMINISHING RETURNS: ``1 + sum(sig_i * decay**rank_i)``, rank
    descending by magnitude. The strongest counts fully, the second by ``decay``, the third by
    ``decay**2`` -- so several signals firing the same way do not double-count what is really one
    piece of information (the SSL bulk->tail: marginal coverage is antitone). Order-independent
    (sorted internally). Empty -> 1.0. Ported from ModelAtlas `_submodular_combine`. Pure.
    """
    if not signals:
        return 1.0
    return 1.0 + sum(sig * (decay**i) for i, sig in enumerate(sorted(signals, reverse=True)))


def score_candidate(
    alignment_factors: Sequence[float],
    soft_signals: Sequence[float],
    decay: float = SUBMODULAR_DECAY,
) -> float:
    """One candidate's recommendation score: the PRODUCT of the alignment factors (each in [0, 1] --
    kappa-coverage, direction-alignment, coherence -- so any one near zero demotes the candidate)
    TIMES the submodular combine of the soft signals (convergence, rarity, absence -- rewards).
    ModelAtlas's multiplicative-factors x submodular-soft blend, ported. Not bounded at 1. Pure.
    """
    product = 1.0
    for factor in alignment_factors:
        product *= factor
    return product * submodular_combine(soft_signals, decay)
