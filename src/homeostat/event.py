"""homeostat.event — the L2 relational-event layer: the encoding contract between the networks and
the engine (SYSTEM_DESIGN.md §10 step 1, THESIS ch. 10).

Each network *narrates*: it renders its slice of the databases into signed relational events (a
network's signed-ternary vote on a coupling IS an event, and the polarity is the assertion — +1
witnesses the coupling, -1 censors it, 0 abstains). A candidate coupling therefore has a **signature
across the networks**, and the cross-network resolution operator is `couple_verdict` — convergent
support with no contradiction survives; a contradiction is a near-miss and is dropped; a censor-only
or all-abstain draws nothing. `events_to_web` compiles the positive result into the `RelationalWeb`
the built engine consumes; direction is earned only where a *directed-mechanism* network asserts it.

Object-AGNOSTIC (a faithful container, like signal.py): the `verb` vocabulary and WHICH networks
earn direction are the RENDERERS' domain (object-led, §13.1) — passed as data, never enumerated
here. Nothing in this module authors biology.
"""

from __future__ import annotations

from collections.abc import Collection, Iterable
from dataclasses import dataclass

from homeostat.web import Coupling, RelationalWeb


@dataclass(frozen=True)
class Event:
    """One L2 relational event — a network's signed vote on a coupling between two atomics.

    `network` names the emitting network (this IS the provenance/genus: which one witnessed it).
    `verb` is the role-action class the renderer emits (amplify, differentiate, closes-off, …), held
    as data, never enumerated here. `subject`/`target` are the coupled atomic ids (gene / role).
    `sign` is the OTP ternary vote: +1 assert the coupling, -1 censor it, 0 abstain (the
    informational zero).
    """

    network: str
    verb: str
    subject: str
    target: str
    sign: int


def couple_verdict(support: int, censor: int) -> str:
    """The cross-network resolution for one coupling, from its tally of votes across networks.

    `support` = how many networks assert the coupling (sign > 0); `censor` = how many rule it out
    (sign < 0). Returns a named code:

    - ``"killed"`` — support > 0 AND censor > 0: a cross-network **contradiction**, the near-miss;
      the disagreement removes the coupling (learn at the residual).
    - ``"censor"`` — censored by ≥1 network, none asserting: ruled out (the negative sign).
    - ``"coupling"`` — convergent support, uncontradicted: draw it (improbable-and-coherent).
    - ``"abstain"`` — none assert and none censor: the informational zero, draw nothing.

    Total over `(int, int)`. Counts are ≥ 0 by construction; a spurious negative simply fails the
    `> 0` guards and is treated as no vote.
    """
    if support > 0 and censor > 0:
        return "killed"
    if censor > 0:
        return "censor"
    if support > 0:
        return "coupling"
    return "abstain"


def events_to_web(events: Iterable[Event], directed_networks: Collection[str]) -> RelationalWeb:
    """Compile a multi-network event stream into the positive `RelationalWeb` the engine consumes.

    Events are grouped by their `(subject, target)` coupling; each group is resolved by
    `couple_verdict` over its support/censor tally, and only a ``"coupling"`` verdict is drawn — a
    cross-network contradiction (``"killed"``), a censor-only, or an all-abstain yields no edge
    (absence = the informational zero). A drawn coupling's `weight` is the convergence count (how
    many networks support it — a provisional strength until the renderers supply evidence-derived
    weights); its `direction` is +1 (subject→target) iff a *directed-mechanism* network
    (`directed_networks`) is among its supporters, else 0 (undirected — the safe base; direction is
    earned only where a directed network asserts it, LAW 3c). Groups are sorted for determinism.
    I/O-free orchestration over the pinned `couple_verdict`; intent-tested.
    """
    groups: dict[tuple[str, str], list[Event]] = {}
    for e in events:
        groups.setdefault((e.subject, e.target), []).append(e)

    couplings: list[Coupling] = []
    for (subject, target), evs in sorted(groups.items()):
        support = sum(1 for e in evs if e.sign > 0)
        censor = sum(1 for e in evs if e.sign < 0)
        if couple_verdict(support, censor) != "coupling":
            continue
        directed = any(e.sign > 0 and e.network in directed_networks for e in evs)
        couplings.append(Coupling(subject, target, float(support), 1 if directed else 0))
    return RelationalWeb(tuple(couplings))
