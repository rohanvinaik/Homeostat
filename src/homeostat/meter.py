"""homeostat.meter — the coherence METER: a calibrated, small-sample-honest coherence scalar.

The rankable coherence the resolve-narrow engine needs, grounded in SSL §9.3 (the coherence
track record has a probability foundation — NML/Shtarkov). A candidate mechanism's predictions
against THIS person's shadow are a rate process over m=3 outcomes — **confirmed** (predicted sign
matches the observed deviation: SUPPORT survived positive elimination), **contradicted** (predicted
sign opposes it: the polarity censor's own contradiction), **standing** (no sign-definite opinion:
the informational zero) — the OTP ternary read as an elimination track record, NOT a consensus
vote-tally (`otp.py`'s forbidden move).

The minimax-regret-optimal calibration of such a rate process is the Normalized Maximum Likelihood
distribution, whose per-symbol realization is the Krichevsky–Trofimov (add-1/2) predictor with
cumulative regret ``log C_n = (m-1)/2 · log2 n`` (Rissanen/Shtarkov; for m=3, ``log2 n``). The meter
is the KT-calibrated NET confirmation — the difference of the KT confirm/contradict predictors —
which is the raw ternary order parameter made honest about sample size: 2/2 confirmed scores below
20/20, and a mechanism that only abstains collapses to the informational zero.

Why calibration and not a raw ratio: a raw ``confirmed / n`` overstates confidence for small n, the
exact un-normalized statistic the significance layer exists to replace. The `(n + m/2)` denominator
IS the regret, applied.
"""

from __future__ import annotations

import math
from collections.abc import Mapping

from homeostat.polarity import SignedAdj, net_polarities

_OUTCOMES = 3  # the coherence alphabet: confirmed / contradicted / standing (the OTP ternary)
_KT_SHRINKAGE = _OUTCOMES / 2  # m/2 — the Krichevsky–Trofimov add-1/2 shrinkage, summed over m


def coherence_meter(confirmed: int, contradicted: int, standing: int) -> float:
    """The calibrated coherence scalar in (-1, 1): the KT (add-1/2) minimax-regret predictor's NET
    confirmation ``(confirmed - contradicted) / (n + m/2)``, ``n = confirmed + contradicted +
    standing``.

    The +1/2 per category cancels in the numerator, leaving the two-sign net ``confirmed -
    contradicted`` (SUPPORT − OPPOSE); the ``n + m/2`` denominator carries the small-sample
    shrinkage, so the scalar is honest where a raw ratio is not. `standing` (the informational zero)
    dilutes toward 0 but never subtracts — a mechanism that only abstains reads 0 (no coherence
    axis), exactly as the quest's ORTHOGONAL zero vector. All-confirmed → +1 in the limit (0.4 at
    n=1, honest); all-contradicted → -1; balanced or empty → 0.0. Pure over ``(int, int, int)``.
    """
    n = confirmed + contradicted + standing
    if n <= 0:
        return 0.0
    return (confirmed - contradicted) / (n + _KT_SHRINKAGE)


def nml_regret(n: int) -> float:
    """The Shtarkov/NML minimax regret of the m=3 coherence meter over ``n`` predictions, in bits:
    ``log C_n = (m-1)/2 · log2 n = log2 n`` (m=3) — the calibration cost the meter pays, reported so
    the read can show its own small-sample penalty (auditability). ``n <= 1`` → 0.0 (a single
    outcome carries no regret). Pure over ``int``.
    """
    if n <= 1:
        return 0.0
    return (_OUTCOMES - 1) / 2 * math.log2(n)


def source_outcomes(
    signed_adj: SignedAdj, source: str, observed: Mapping[str, int]
) -> tuple[int, int, int]:
    """The ``(confirmed, contradicted, standing)`` track record of one candidate `source` against
    the observed shadow — the meter's ELIMINATION input, computed with the SAME `net_polarities`
    machinery the polarity censor uses, so "contradicted" here IS the censor's contradiction.

    For each observed node the source reaches sign-definitely, its required perturbation direction
    is ``observed[x] * P(source->x)`` (net polarity); its best single perturbation direction
    CONFIRMS the majority requirement and CONTRADICTS the minority — ``confirmed = max(n₊, n₋)``,
    ``contradicted = min(n₊, n₋)``. An observed node the source has no sign-definite opinion on
    (unreached or sign-ambiguous) is STANDING — the informational zero, which dilutes the meter but
    never subtracts (the quest's ORTHOGONAL). A source is censored iff ``contradicted >= 1`` (its
    requirements demand both directions); the meter is the soft-rank sibling of that hard veto.
    Pure over ``(SignedAdj, str, Mapping[str, int])``.
    """
    pols = net_polarities(signed_adj, source)
    required = [observed[x] * pols[x] for x in observed if x in pols]
    n_plus = required.count(1)
    n_minus = required.count(-1)
    confirmed = max(n_plus, n_minus)
    contradicted = min(n_plus, n_minus)
    standing = sum(1 for x in observed if x not in pols)
    return confirmed, contradicted, standing
