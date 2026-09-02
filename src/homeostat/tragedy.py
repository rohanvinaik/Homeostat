"""homeostat.tragedy — the first mechanism-genre, read NATIVE off the coupling web's topology.

A **tragedy** is a dysregulatory cascade: a directed cascade from a sub-threshold ORIGIN (the fatal
flaw — a source nothing upstream drives) that locks a downstream absorbing SINK (the doom). THESIS
ch.9's M3/M4: the flaw serves the doom; the outcome is the given, and reading the arc that makes it
inevitable is the point. The genre is READ OFF the graph the events ARE — not inferred from diction.

Two axes, kept apart (the significance-weighting set-theory conception + OTP; substrate in
`homeostat.topology`):
- **Reachability is polarity-BLIND** (κ = coverage = the forward-reachable SET; an edge is an edge).
  The cascade propagates over EVERY opinionated regulatory coupling — amplify AND inhibit — stopping
  only at the **informational zero** (absence: no coupling), the one non-carrying OTP state.
- **Polarity is the OTP ternary that rides each edge** and composes by sign-PRODUCT along the path
  (two inhibitions = a net-up disinhibition); drives merging at a node OTP-combine, and disagreeing
  paths collapse to the informational zero — the topology declines a doom it cannot drive.

The verdict at a reached sink is that net sign: net-SUPPORT = ``doomed``; net-OPPOSE = suppressed
(the H4 refusal — a censor holds it down); the informational zero = ``indeterminate`` (abstain). A
cascade with no source (a cycle) is a different genre (the vicious loop) and is declined here.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from homeostat.event import Event
from homeostat.kappa import reachable
from homeostat.otp import OPPOSE, ORTHOGONAL, SUPPORT
from homeostat.topology import otp_combine, signed_adjacency


@dataclass(frozen=True)
class Tragedy:
    """One tragic arc: a cascade from `origin` (the fatal flaw) locking `sink` (the doom), with the
    net-sign verdict — ``"doomed"`` (net-up), ``"suppressed"`` (net-down: H4), or
    ``"indeterminate"`` (the informational zero: the arc's paths disagree, so no doom holds)."""

    origin: str
    sink: str
    verdict: str


def reach_graph(signed_adj: dict[str, dict[str, int]]) -> dict[str, set[str]]:
    """The polarity-BLIND reachability adjacency (edge presence only) — every opinionated coupling
    carries the signal, so a signed-0 edge still couples; only absence fails to. Pure."""
    return {u: set(nbrs) for u, nbrs in signed_adj.items()}


def sources(reach_adj: dict[str, set[str]]) -> set[str]:
    """Nodes with an out-edge but no in-edge — the cascade ORIGINS (nothing upstream drives them).
    Pure over the reachability adjacency."""
    targets = {t for outs in reach_adj.values() for t in outs}
    return set(reach_adj) - targets


def is_sink(reach_adj: dict[str, set[str]], node: str) -> bool:
    """Does `node` have no onward regulatory edge — a candidate absorbing state (the doom)? Pure."""
    return not reach_adj.get(node)


def net_signs(signed_adj: dict[str, dict[str, int]], origin: str) -> dict[str, int]:
    """Forward-propagate the OTP ternary from `origin` (SUPPORT — the perturbed fatal flaw is 'on')
    over the signed graph: each edge multiplies its source's net by its sign, and contributions
    merging at a node OTP-combine (disagreement -> the informational zero). Iterated to a fixpoint;
    ORTHOGONAL only ever spreads (absorbing), so it terminates and cycles are safe. `origin` stays
    pinned SUPPORT (it is driven from outside). Orchestration over `otp_combine`; intent-tested.
    """
    net: dict[str, int] = {origin: SUPPORT}
    changed = True
    while changed:
        changed = False
        for u, nbrs in signed_adj.items():
            if u not in net:
                continue
            for v, sign in nbrs.items():
                if v == origin:
                    continue
                contrib = net[u] * sign
                merged = otp_combine(net[v], contrib) if v in net else contrib
                if v not in net or net[v] != merged:
                    net[v] = merged
                    changed = True
    return net


def doom_verdict(is_terminal: bool, reached: bool, net_sign: int) -> str:
    """The pure tragedy verdict for one node. Named codes, never bools:
    - ``"not-doom"`` — not a locked endpoint (not a sink, or no cascade reaches it);
    - ``"doomed"`` — a sink the cascade drives net-SUPPORT (up): the locked absorbing doom;
    - ``"suppressed"`` — a sink driven net-OPPOSE (down): the H4 refusal, a held/quenched terminal;
    - ``"indeterminate"`` — a sink whose net drive is the informational zero: the paths disagree, so
      the topology asserts no doom (abstention, not a guess).
    Pure over (bool, bool, ternary int).
    """
    if not (is_terminal and reached):
        return "not-doom"
    if net_sign == SUPPORT:
        return "doomed"
    if net_sign == OPPOSE:
        return "suppressed"
    return "indeterminate"


def read_tragedy(events: Iterable[Event]) -> list[Tragedy]:
    """Read the tragedies in a regulatory event stream: for each origin, the cascade's reachable
    sinks, each carried through the pinned `doom_verdict` over the OTP net sign propagated to it.
    Origins with no cascade, and cycles with no origin, yield nothing. Orchestration over the pinned
    decisions + `kappa.reachable`; intent-tested.
    """
    evs = list(events)
    signed = signed_adjacency(evs)
    reach = reach_graph(signed)
    out: list[Tragedy] = []
    for origin in sorted(sources(reach)):
        net = net_signs(signed, origin)
        for node in sorted(reachable(reach, origin)):
            verdict = doom_verdict(is_sink(reach, node), True, net.get(node, ORTHOGONAL))
            if verdict != "not-doom":
                out.append(Tragedy(origin, node, verdict))
    return out
