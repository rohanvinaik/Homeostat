"""homeostat.tragedy — the first mechanism-genre, read NATIVE off the coupling web's topology.

A **tragedy** is a dysregulatory cascade: a directed amplify chain from a sub-threshold ORIGIN
(the fatal flaw — a source nothing upstream drives) into a locked absorbing SINK (the doom — a
node with no onward relay). This is the meaning-mechanism M3/M4 of THESIS ch.9: the flaw serves
the doom; the outcome is the given, and reading the arc that makes it inevitable is the point.

The genre is **not** inferred from how a story reads (that is the diction substrate we reject) —
it is READ OFF the graph the events already ARE. Native to this project's own σ/κ terms; the
directed-graph primitive is `homeostat.kappa.reachable`, reused (waste not).

The **H4 refusal** (recover-vs-import): a terminal an inhibitor RESTRAINS is *compensated*, not
doomed — the genre abstains rather than import a doom the censor voids ("sometimes it's just
autoimmune"). And a cascade with no source is a *cycle*, which is a different genre (the vicious
loop / ironic comedy), so tragedy — which requires an origin — declines it by construction.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from homeostat.event import Event
from homeostat.kappa import reachable

REGULATORY = "regulatory"
AMPLIFY = "amplifies"
INHIBIT = "inhibits"


@dataclass(frozen=True)
class Tragedy:
    """One tragic arc: a cascade from `origin` (the fatal flaw) to `sink` (the doom), with the
    genre verdict — ``"doomed"`` (an uncensored absorbing state) or ``"compensated"`` (H4: the
    doom is restrained by a censor, so the read abstains from calling it doom)."""

    origin: str
    sink: str
    verdict: str


def regulatory_adjacency(events: Iterable[Event], verb: str) -> dict[str, set[str]]:
    """Directed adjacency `{subject: {targets}}` for one regulatory verb. Self-loops are dropped —
    a reflexive edge propagates the signal to no new node (Regenesis floors reflexivity likewise),
    so it is neither a cascade step nor a reason a node fails to be a sink. Orchestration over the
    event stream; intent-tested.
    """
    adj: dict[str, set[str]] = {}
    for e in events:
        if e.network == REGULATORY and e.verb == verb and e.subject != e.target:
            adj.setdefault(e.subject, set()).add(e.target)
    return adj


def sources(adj: dict[str, set[str]]) -> set[str]:
    """Nodes with an out-edge but no in-edge — the cascade ORIGINS (nothing upstream amplifies
    them; the sub-threshold fatal flaw the arc begins at). Pure over the adjacency."""
    targets = {t for outs in adj.values() for t in outs}
    return set(adj) - targets


def is_sink(adj: dict[str, set[str]], node: str) -> bool:
    """Does `node` have no onward amplify edge — a candidate absorbing state (the doom)? Pure."""
    return not adj.get(node)


def doom_verdict(is_terminal: bool, reached_by_cascade: bool, censored: bool) -> str:
    """The pure tragedy decision for one node. Named codes, never bools — the two refusals mean
    different things and must not collapse:
    - ``"not-doom"`` — not a locked cascade endpoint here (not a sink, or no cascade reaches it);
    - ``"compensated"`` — the H4 refusal: a sink an inhibitor restrains is not doom, it is held;
    - ``"doomed"`` — an uncensored absorbing state a cascade locks onto: the tragedy's given end.
    Pure over three booleans.
    """
    if not (is_terminal and reached_by_cascade):
        return "not-doom"
    if censored:
        return "compensated"
    return "doomed"


def read_tragedy(events: Iterable[Event]) -> list[Tragedy]:
    """Read the tragedies in a regulatory event stream: amplify-cascades from an origin into a
    sink, each carried through the pinned `doom_verdict` (an inhibited sink is compensated, not
    doomed). Origins with no cascade, and cycles with no origin, yield nothing. Orchestration over
    `regulatory_adjacency` / `sources` / `is_sink` / `doom_verdict` + `kappa.reachable`;
    intent-tested.
    """
    evs = list(events)
    amplify = regulatory_adjacency(evs, AMPLIFY)
    inhibit = regulatory_adjacency(evs, INHIBIT)
    censored = {t for outs in inhibit.values() for t in outs}
    out: list[Tragedy] = []
    for origin in sorted(sources(amplify)):
        for node in sorted(reachable(amplify, origin)):
            verdict = doom_verdict(is_sink(amplify, node), True, node in censored)
            if verdict != "not-doom":
                out.append(Tragedy(origin, node, verdict))
    return out
