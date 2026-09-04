"""homeostat.operator — the operator-injected hypothesis: fluid intelligence as a TESTED input.

The person understands their own health and can propose the beginnings of a mechanism —
CONNECTIONS between elements ("I think X drives my inflammation"). Those proposals are HYPOTHESES,
never ground truth: they enter the PREFER layer only (story + resolve + meter), NEVER the two-sign
elimination or the certified-⊥, so an operator can never FABRICATE a certified mechanism
(correctness stays in the code, not the operator). The dynamics then TEST them against the person's
actual shadow — if wrong they fall out, if right they accelerate the read (Rohan, 2026-09-04). The
operator LEDGER reports which proposals held (the CLI operator/code epistemology: the operator
proposes, the code adjudicates).

An operator edge ``subject --(verb→polarity)--> target`` predicts: perturbing `subject` in its
observed direction drives `target` by ``subject_sign × polarity``. Against the shadow that is
CONFIRMED (the shadow agrees), CONTRADICTED (opposes), or STANDING (an endpoint unobserved / verb
non-regulatory — untestable, the informational zero). Same alphabet as the coherence meter.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from homeostat.event import Event


@dataclass(frozen=True)
class HypothesisOutcome:
    """One operator hypothesis edge and how the shadow judged it. `subject`/`verb`/`target` echo the
    proposed coupling; `outcome` is ``"confirmed"`` (the shadow bears it out — lifts its cluster),
    ``"contradicted"`` (the shadow opposes it — the censor down-ranks), or ``"standing"`` (an
    endpoint unobserved or the verb non-regulatory — untestable, the informational zero)."""

    subject: str
    verb: str
    target: str
    outcome: str


def edge_outcome(subject_sign: int, target_sign: int, polarity: int) -> str:
    """Judge one operator edge against the shadow, from the endpoint signs and the polarity.
    Named codes: ``"standing"`` when either endpoint is unobserved (sign 0 — untestable, the
    informational zero); else ``"confirmed"`` iff ``target_sign == subject_sign * polarity`` (driven
    by the subject's observed direction, the edge predicts the target's observed direction) and
    ``"contradicted"`` otherwise (it predicts the opposite). Pure over ``(int, int, int)``.
    """
    if subject_sign == 0 or target_sign == 0:
        return "standing"
    return "confirmed" if target_sign == subject_sign * polarity else "contradicted"


def operator_ledger(
    hypotheses: Iterable[Event], observed: Mapping[str, int], verb_sign: Mapping[str, int]
) -> list[HypothesisOutcome]:
    """The operator ledger: judge each proposed hypothesis edge against the shadow. A verb absent
    from `verb_sign` (non-regulatory — no testable polarity) is STANDING; otherwise the polarity is
    ``verb_sign[verb]`` and `edge_outcome` reads it against the observed subject/target signs.
    Orchestration over the pinned `edge_outcome`; intent-tested.
    """
    out: list[HypothesisOutcome] = []
    for e in hypotheses:
        polarity = verb_sign.get(e.verb)
        if polarity is None:
            outcome = "standing"
        else:
            outcome = edge_outcome(observed.get(e.subject, 0), observed.get(e.target, 0), polarity)
        out.append(HypothesisOutcome(e.subject, e.verb, e.target, outcome))
    return out
