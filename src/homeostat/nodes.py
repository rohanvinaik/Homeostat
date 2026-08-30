"""homeostat.nodes — node birth, death, consolidation: the one piece beyond Peitho.

The mechanism graph's shape is unknown a priori, so the σ-trajectory search (`search.py`) must GROW
and PRUNE the candidate set itself. This module is the object-agnostic **lifecycle** of a node
(a candidate mechanism component), grounded in the founder's SSL:

- **BIRTH (induction — SSL IV-G / m2).** A candidate accrues support from each recurrence across the
  population; once it recurs ≥ `recur_min` times UNCONTRADICTED, it is BORN (fires as a component).
  Sub-threshold candidates keep accruing; they do not fire.
- **DEATH (negative learning).** A candidate that meets a near-miss — a "does not", a population or
  presentation where the coupling fails — is WITHDRAWN before it fires. You learn at the residual.
- **OSCILLATION (SSL §16.6).** A candidate CONFIRMED in some reads and CONTRADICTED in others is
  over-general; the response is to SPECIALIZE it with a discriminating guard if one exists, else the
  oscillation IS the finding (logged, not promoted).
- **CONSOLIDATION (SSL §5.11).** Drop what a resolution no longer needs (the withdrawn nodes).

Object-agnostic: a node is an id + its support/contradiction counts (+ feature sets for
specialization). WHAT a residual proposes as a new node is the data geometry's job (the object),
never this module's — this is the lifecycle only. Birth is *triggered* by the search's STUCK signal
(`search.sigma_trajectory` returning `sigma=None`); this module decides what happens to a node once
proposed, not what to propose.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

# Node lifecycle states — named string codes (two states that mean different things must not
# collapse into one truthy check).
CANDIDATE = "CANDIDATE"  # sub-threshold, uncontradicted — still accruing, does not fire
BORN = "BORN"  # recurred ≥ recur_min, uncontradicted — promoted, fires as a component
DEAD = "DEAD"  # contradicted and never confirmed — a pure near-miss, withdrawn before firing
OSCILLATING = "OSCILLATING"  # confirmed AND contradicted — over-general; specialize or log


# ---- the atomic pure decisions (Detective-pinnable) --------------------------------------


def node_status(support: int, contradictions: int, recur_min: int) -> str:
    """The lifecycle status of a node from its evidence counts. A total function over named codes.

    Order matters and encodes the theory: a node both confirmed and contradicted OSCILLATES (the
    over-general signature) — that outranks birth, so an over-general node is never silently
    promoted. A node only ever contradicted is DEAD (near-miss withdrawal). An uncontradicted node
    is BORN once it
    recurs ≥ `recur_min` (and at least once — no birth from zero evidence, even at recur_min = 0);
    otherwise it is a still-accruing CANDIDATE. Pure over `(int, int, int)`.
    """
    if support > 0 and contradictions > 0:
        return OSCILLATING
    if contradictions > 0:
        return DEAD
    if support >= recur_min and support > 0:
        return BORN
    return CANDIDATE


def next_counts(support: int, contradictions: int, confirmed: bool) -> tuple[int, int]:
    """Accrue one observation: a confirmation raises support, a contradiction raises contradictions.
    The confidence-accrual (m2) and the withdraw-on-"does-not" of SSL IV-G, as one total decision.
    Pure over `(int, int, bool)`."""
    if confirmed:
        return support + 1, contradictions
    return support, contradictions + 1


def specialization_guard(confirming: list[list[str]], contradicting: list[list[str]]) -> list[str]:
    """The discriminating guard for an oscillating node (SSL §16.6): the features shared by EVERY
    confirming instance and present in NO contradicting instance. A non-empty result means the node
    can be SPECIALIZED to that guard (narrowed so it no longer fires on the contradicting cases); an
    empty result means the oscillation cannot be discriminated and IS the finding, to be logged, not
    promoted. Empty `confirming` yields no guard. Pure over `(list[list[str]], list[list[str]])`.
    """
    if not confirming:
        return []
    common: set[str] = set(confirming[0])
    for feats in confirming[1:]:
        common &= set(feats)
    bad: set[str] = set()
    for feats in contradicting:
        bad |= set(feats)
    return sorted(common - bad)


# ---- the node and its lifecycle operators (orchestration over the pure decisions) ---------


@dataclass(frozen=True)
class Node:
    """A candidate mechanism component. `support` counts confirming recurrences, `contradictions`
    counts near-misses. Its firing state is `status(recur_min)`; the content it stands for is the
    data geometry's (the object), not held here."""

    ident: str
    support: int = 0
    contradictions: int = 0

    def status(self, recur_min: int) -> str:
        """This node's lifecycle status at the given recurrence threshold."""
        return node_status(self.support, self.contradictions, recur_min)


def observe(node: Node, confirmed: bool) -> Node:
    """Return the node after one observation (confirmation or contradiction). Non-mutating."""
    s, c = next_counts(node.support, node.contradictions, confirmed)
    return replace(node, support=s, contradictions=c)


def born(nodes: list[Node], recur_min: int) -> list[Node]:
    """The nodes that FIRE — promoted by uncontradicted recurrence. These are what the search treats
    as live mechanism components."""
    return [n for n in nodes if n.status(recur_min) == BORN]


def oscillating(nodes: list[Node], recur_min: int) -> list[Node]:
    """The over-general nodes (confirmed AND contradicted) — candidates for specialization, else the
    finding is the oscillation itself."""
    return [n for n in nodes if n.status(recur_min) == OSCILLATING]


def consolidate(nodes: list[Node], recur_min: int) -> list[Node]:
    """Drop the DEAD nodes (near-miss withdrawal + safe-forget, SSL §5.11); keep everything still
    live or accruing (BORN / CANDIDATE / OSCILLATING). Order-preserving. This is the prune half of
    node birth/death."""
    return [n for n in nodes if n.status(recur_min) != DEAD]
