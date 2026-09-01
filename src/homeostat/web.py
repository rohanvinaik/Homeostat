"""homeostat.web — the constraint object: a weighted relational web, and its bridge to the engine.

The kill-matrix the σ-search runs over has a SHAPE (THEORY_OF_THE_CASE Part II, "The constraint
object is a weighted relational web"): a bounded set of regulatory nodes joined by WEIGHTED,
TERNARY-directed couplings. This module holds that web (the container) and compiles it, together
with one person's observed deviations, into the `(candidates, constraints)` kill-matrix that
`search.eliminate_to_survivor` / `loop.resolve_presentation` consume.

Object-AGNOSTIC: the specific couplings are DATA plugged in (the SDIS-seeded content step, canon
§13.1). Nothing here authors a coupling; it only reduces whatever web it is handed to a kill-matrix.

The reduction, in one line: a candidate mechanism is a candidate SOURCE node; an observed symptom
is a constraint that KILLS every source that cannot propagate to it. Drive H → 0 and the surviving
source is the mechanism.

The load-bearing design properties, realized here:
- **Weighted; weak couplings do not carry.** `min_weight` gates propagation — a coupling below the
  floor supplies no path (the Kuramoto coupling-gain floor).
- **Ternary direction; absence = the informational zero.** `direction ∈ {+1: a→b, -1: b→a, 0:
  undirected}`; a MISSING coupling is *no opinion*, never "uncoupled" — it supplies no path, it
  cannot assert non-reachability.
- **Direction earned, buys efficiency not correctness.** Undirected (0) couplings propagate both
  ways (the safe base — they never wrongly kill a source); a directed coupling collapses more
  sources, and belongs only where the relation earned it.
- **Bounded universe.** The candidate set is exactly the web's finite node set — which is what makes
  σ finite and the elimination terminate.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Coupling:
    """One weighted, ternary-directed coupling between two regulatory nodes.

    `weight` is the coupling strength. `direction` is the ternary: +1 = signal flows a→b, -1 = flows
    b→a, 0 = undirected (both ways — the safe co-movement default). There is no Coupling for an
    absent edge: absence is the informational zero (no opinion), not a zero-weight coupling.
    """

    a: str
    b: str
    weight: float
    direction: int  # +1 (a→b), -1 (b→a), 0 (undirected / both ways)


@dataclass(frozen=True)
class RelationalWeb:
    """The bounded constraint object: the couplings that span its finite node set."""

    couplings: tuple[Coupling, ...]


def nodes(web: RelationalWeb) -> list[str]:
    """The web's bounded node set — every coupling endpoint, sorted, unique. This IS the candidate
    universe: each node is a candidate deviation-source. Pure over `RelationalWeb`."""
    seen: set[str] = set()
    for c in web.couplings:
        seen.add(c.a)
        seen.add(c.b)
    return sorted(seen)


def web_adjacency(web: RelationalWeb, min_weight: float = 0.0) -> dict[str, list[str]]:
    """Compile the web into a directed one-hop adjacency `{node: [downstream neighbours]}`, applying
    the ternary direction and the `min_weight` propagation floor.

    A directed coupling (+1) adds a→b; (-1) adds b→a; an undirected coupling (0) adds both legs; a
    coupling with `weight < min_weight` adds nothing (it does not carry the signal). Neighbour lists
    are sorted for determinism. Orchestration over the couplings; intent-tested.
    """
    adj: dict[str, set[str]] = {}
    for c in web.couplings:
        adj.setdefault(c.a, set())
        adj.setdefault(c.b, set())
    for c in web.couplings:
        if c.weight < min_weight:
            continue
        if c.direction >= 0:  # +1 (a→b) or 0 (undirected: the a→b leg)
            adj[c.a].add(c.b)
        if c.direction <= 0:  # -1 (b→a) or 0 (undirected: the b→a leg)
            adj[c.b].add(c.a)
    return {n: sorted(nbrs) for n, nbrs in adj.items()}


def reaches(adj: dict[str, list[str]], source: str, target: str) -> bool:
    """Does `source` propagate to `target` over the compiled adjacency? A node reaches itself
    (`source == target` → True: a symptom can be its own source). Breadth-first over the directed
    one-hop adjacency. Pure over `(dict[str, list[str]], str, str)`.
    """
    if source == target:
        return True
    seen: set[str] = {source}
    queue: deque[str] = deque([source])
    while queue:
        n = queue.popleft()
        for m in adj.get(n, ()):
            if m == target:
                return True
            if m not in seen:
                seen.add(m)
                queue.append(m)
    return False


def kill_matrix(
    web: RelationalWeb, observed: list[str], min_weight: float = 0.0
) -> tuple[list[str], dict[str, list[str]]]:
    """Reduce (web + a person's observed deviations) to the `(candidates, constraints)` kill-matrix
    the σ-search consumes.

    `observed` is the node-ids where a deviation is seen (the symptoms — the 'leaves'). Candidates =
    the web's whole bounded node set (each a candidate source). For each observed symptom S, the
    constraint `explains:S` kills every candidate that CANNOT reach S — a source that does not
    propagate to the symptom cannot be the mechanism. Hand the result to
    `resolve_presentation` (or `eliminate_to_survivor`): the surviving source is the mechanism.

    A symptom always reaches itself, so no constraint can empty the candidate set; a constraint that
    resolves nothing (κ = 0, S reachable from every source) is left to the engine's own
    admissibility. Bridge — intent-tested (and end-to-end through the real engine).
    """
    ns = nodes(web)
    adj = web_adjacency(web, min_weight)
    constraints: dict[str, list[str]] = {}
    for s in observed:
        constraints[f"explains:{s}"] = [c for c in ns if not reaches(adj, c, s)]
    return ns, constraints
