"""homeostat.polarity — the polarity-opposition censor: the NATIVE second sign, from the directed
web + the observed deviation signs alone (no treatment-response required).

A candidate source explains the shadow only if a SINGLE perturbation of it produces the observed
pattern of deviations. Regulation has a sign (SIGNOR's up/down -> the `amplifies`/`inhibits` verb),
so a source drives each gene it reaches by the NET polarity of the path (the product of the edge
signs). If no single perturbation direction d in {+1, -1} makes those driven directions agree with
what was actually observed, the source is a mechanistic IMPOSSIBILITY -- a hard censor, not a soft
down-rank (biochemistry, not search relevance).

The strength of a censor is backed by CONSERVATIVE application (PERSUASION BEFORE EXECUTION): each
candidate is first tried in BOTH directions to accommodate it, and only a candidate that cannot be
saved either way is censored. Sign-AMBIGUOUS reach (paths that disagree on net sign) and unreached
observed contribute nothing -- a censor is a proof of impossibility, so it fires only where the sign
is genuinely determined (Law 5, "never guess a direction", now for polarity). This module holds the
pure decisions; `verb_sign` (the regulatory-verb -> polarity map) is DATA the driver supplies.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Collection, Iterable, Mapping

from homeostat.event import Event

Edge = tuple[str, int]
SignedAdj = dict[str, list[Edge]]


def signed_adjacency(events: Iterable[Event], verb_sign: Mapping[str, int]) -> SignedAdj:
    """The directed SIGNED adjacency ``{subject: [(target, polarity)]}`` from the regulatory events:
    each supported event's `verb` maps to a polarity via `verb_sign` (e.g. amplifies +1 / inhibits
    -1). An edge whose events DISAGREE on polarity is sign-ambiguous and DROPPED (a coupling with no
    definite sign is no polarity-path); a verb absent from `verb_sign` (non-regulatory) contributes
    nothing; a censor event (sign <= 0) is not a supported edge. Neighbour lists sorted. Pure.
    """
    edge_signs: dict[tuple[str, str], set[int]] = {}
    for e in events:
        p = verb_sign.get(e.verb)
        if p is not None and e.sign > 0:
            edge_signs.setdefault((e.subject, e.target), set()).add(p)
    adj: SignedAdj = {}
    for (subject, target), signs in sorted(edge_signs.items()):
        if len(signs) == 1:  # sign-definite edge only
            adj.setdefault(subject, []).append((target, next(iter(signs))))
    return adj


def net_polarities(signed_adj: SignedAdj, source: str) -> dict[str, int]:
    """Net path polarity from `source` to every SIGN-DEFINITE node: the product of the edge signs
    along the path, when it is IDENTICAL over all directed paths. A node reached by two paths of
    opposite net sign is sign-AMBIGUOUS and omitted (never guessed). `source`->`source` is +1 (the
    identity: a source's own perturbation reaches itself with its own sign). Worklist sign-set
    fixpoint -- each node's set saturates at {+1, -1}, so it converges. Pure.
    """
    sset: dict[str, set[int]] = {source: {1}}
    queue: deque[str] = deque([source])
    while queue:
        n = queue.popleft()
        for m, pol in signed_adj.get(n, ()):
            new = {s * pol for s in sset[n]}
            if m not in sset:
                sset[m] = set(new)
                queue.append(m)
            elif not new <= sset[m]:
                sset[m] |= new
                queue.append(m)  # its set grew -- re-propagate
    return {node: next(iter(s)) for node, s in sset.items() if len(s) == 1}


def polarity_censors(
    signed_adj: SignedAdj, candidates: Collection[str], observed: Mapping[str, int]
) -> list[str]:
    """The sources censored by regulatory-polarity contradiction. For each candidate, the required
    perturbation direction to explain a reached observed X is ``d_X * P(source->X)`` (net polarity);
    a source that is ITSELF observed also fixes its own direction. PERSUASION BEFORE EXECUTION: if
    some single direction satisfies every requirement, the candidate is accommodated (not censored);
    only a candidate whose requirements demand BOTH +1 and -1 -- an impossibility -- is censored.
    Sign-ambiguous / unreached observed contribute nothing (conservative). Returns the sorted
    censored sources. Pure over `(SignedAdj, Collection[str], Mapping[str, int])`.
    """
    censored: list[str] = []
    for source in candidates:
        pols = net_polarities(signed_adj, source)
        # If the source is itself observed, its own direction is already here: it reaches itself
        # (pols[source] = +1), so `x = source` is captured by the comprehension. An observed gene
        # the source does NOT reach sign-definitely (`x not in pols`) is skipped -- unreached
        # deviations contribute nothing (conservative).
        required = {observed[x] * pols[x] for x in observed if x in pols}
        if len(required) > 1:  # no single perturbation direction works -> mechanistic impossibility
            censored.append(source)
    return sorted(censored)
