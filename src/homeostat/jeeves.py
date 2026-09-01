"""homeostat.jeeves — the discrimination-dimension selector (Jeeves mode).

The `STUCK`-branch (SYSTEM_DESIGN.md §9, §12.3): when two-sign elimination leaves a plural
survivor set that no measured constraint separates, the Discrimination Guarantee says do NOT
guess and do NOT grow nodes — add a DIMENSION. This module decides WHICH: rank the unmeasured
probes by their **expected information gain** over the current survivors (Lindley/Howard
value-of-information, the SSL §3.2 active-learning acquisition rule — classical information
theory, not a model), and return the highest-value one as the next question ("do you also have
allergies? persistent tachycardia?").

A probe carries `kind` — "confirm" (a positive μ probe: what would cohere?) or "rule_out" (a
negative μ⁻ probe: what would censor?, treatment-response most of all) — so the two signs compete
on one EIG scale; the kind only phrases the question. `select_probe` returns None when no
available dimension would discriminate (EIG 0 everywhere): honest abstention (the informational
zero — "I cannot separate these without a measurement you do not have").

Object-agnostic: a probe's `predicted` map (each live candidate → the sign it predicts on this
dimension) comes from the prior web; nothing here authors a prediction.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Probe:
    """One candidate dimension the selector could ask about.

    `dimension` names the axis; `kind` is "confirm" (positive sign) or "rule_out" (negative sign),
    which phrases the question, not the EIG; `predicted` maps each candidate-id to the ternary sign
    it predicts on this dimension (from the prior web). Measuring the dimension and observing a sign
    eliminates every candidate whose predicted sign differs.
    """

    dimension: str
    kind: str
    predicted: dict


def expected_information_gain(class_sizes: list[int]) -> float:
    """The expected information gain (mutual information) of a partition, in bits: how much
    measuring a dimension is expected to reduce H = log₂|survivors|.

    `class_sizes` are the survivor counts per outcome-class (per predicted sign). With n = Σ sizes
    and each outcome assumed to occur with probability sizeₛ/n (max-entropy over which survivor is
    true), EIG = log₂(n) − (1/n)·Σ sizeₛ·log₂(sizeₛ). A partition into singletons resolves
    everything (EIG = log₂ n); a single class discriminates nothing (EIG = 0). Empty/degenerate
    inputs (n ≤ 1 or one class) give 0.0. Always ≥ 0 (a mutual information). Pure over `list[int]`.
    """
    sizes = [s for s in class_sizes if s > 0]
    n = sum(sizes)
    if n <= 1 or len(sizes) <= 1:
        return 0.0
    e_post = sum(s * math.log2(s) for s in sizes) / n
    return math.log2(n) - e_post


def probe_gain(predicted: dict, survivors: list[str]) -> float:
    """The EIG of a probe over the current survivor set: bucket the LIVE survivors by the sign they
    predict on this dimension (a survivor with no prediction falls in the orthogonal `0` class — the
    probe cannot discriminate it), and return `expected_information_gain` of those class sizes.
    Composition over the pinned EIG; intent-tested.
    """
    live_signs = [predicted.get(s, 0) for s in survivors]
    counts = Counter(live_signs)
    return expected_information_gain(list(counts.values()))


def select_probe(survivors: list[str], probes: list[Probe]) -> Probe | None:
    """The Jeeves selection: the unmeasured probe with the greatest EIG over the plural survivors —
    the next question. Returns None when no probe would discriminate (EIG 0 everywhere): honest
    abstention (the informational zero — no available dimension separates the survivors). Ties break
    by dimension name for determinism. I/O-free orchestration over the pinned EIG; intent-tested.
    """
    best: Probe | None = None
    best_gain = 0.0
    for p in sorted(probes, key=lambda pr: pr.dimension):
        g = probe_gain(p.predicted, survivors)
        if g > best_gain:
            best_gain = g
            best = p
    return best
