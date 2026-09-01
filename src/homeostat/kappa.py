"""The κ / significance math, transported from Regenesis `significance.py`.

κ is a coherence measure **only over the mechanism-derivation graph** — the
what-implies-what of a *reconstructed* combination (§5.12, §12.13). Read over a
generic network (a universal interactome, STRING ∪ GTEx) it silently becomes a
topology statistic: a node's participation/hub-score in a pre-drawn map with no
person, no phenotype, no coherence-of-a-specific-combination in it. That is the
recorded death (§15, Act 2). So this module keeps only the derivation-graph
forms; the `pagerank` / `personalized_pagerank` participation-scorers — κ applied
to the undirected STRING/GTEx graph, and the §10.3 PBS-teleportation prior that
"demoted the known connectors" (Act 4) — are removed, not quarantined.

Faithful correspondence (definitions mirrored, not reinvented):
- `reachable`, `coverage`, `marginal_coverage`  -> verbatim (directed graphs;
  κ = marginal coverage over the derivation graph, §5).
- `weak_components`, `is_bridge`, `components_joined` -> a bridge joins two
  previously-DISJOINT components (§5.7/§5.8's definition) — structural, and
  legitimate ONLY over the derivation graph, never a generic interactome.
- `chain_significance`                           -> Σ log(out-degree) over the
  ancestor hops a chain navigates (§5). RANKING-ONLY.
"""

from collections import deque
from math import log


def reachable(adj: dict[str, set[str]], start: str) -> set[str]:
    """Forward-reachable set of `start` (excludes start), directed."""
    seen: set[str] = set()
    queue = deque(adj.get(start, set()))
    while queue:
        n = queue.popleft()
        if n not in seen:
            seen.add(n)
            queue.extend(adj.get(n, set()))
    return seen


def coverage(adj: dict[str, set[str]]) -> dict[str, int]:
    """κ base per node = |forward-reachable set| (Regenesis `coverage`)."""
    nodes = set(adj) | {t for outs in adj.values() for t in outs}
    return {n: len(reachable(adj, n)) for n in nodes}


def marginal_coverage(adj: dict[str, set[str]], node: str, selected: list[str]) -> int:
    """κ(v|S) = |cover(v) \\ cover(S)| (Regenesis `marginal_coverage`)."""
    covered: set[str] = set()
    for s in selected:
        covered |= reachable(adj, s)
        covered.add(s)
    return len(reachable(adj, node) - covered)


def weak_components(adj: dict[str, set[str]]) -> list[set[str]]:
    """Weakly-connected components (edges treated as undirected)."""
    undirected: dict[str, set[str]] = {}
    nodes = set(adj) | {t for outs in adj.values() for t in outs}
    for u in nodes:
        undirected.setdefault(u, set())
    for u, outs in adj.items():
        for v in outs:
            undirected[u].add(v)
            undirected[v].add(u)
    seen: set[str] = set()
    comps = []
    for start in nodes:
        if start in seen:
            continue
        comp = {start}
        seen.add(start)
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in undirected[u]:
                if v not in seen:
                    seen.add(v)
                    comp.add(v)
                    queue.append(v)
        comps.append(comp)
    return sorted(comps, key=len, reverse=True)


def is_bridge(adj: dict[str, set[str]], antecedent: str, consequent: str) -> bool:
    """Does adding antecedent->consequent join two previously-disjoint weak
    components? §5.7/§5.8's definition, verbatim (Regenesis `is_bridge`).
    Structural only; legitimate over the derivation graph, never a generic
    interactome (§5.12)."""
    comps = weak_components(adj)
    home = {n: i for i, c in enumerate(comps) for n in c}
    a, c = home.get(antecedent), home.get(consequent)
    return a is not None and c is not None and a != c


def components_joined(candidate_edges: set[str], base_components: list[set[str]]) -> int:
    """coverage_delta as bridge strength: how many DISTINCT base components a
    candidate's structural edges touch. >=2 => the candidate is a bridge."""
    home = {g: i for i, c in enumerate(base_components) for g in c}
    return len({home[g] for g in candidate_edges if g in home})


def chain_significance(chain: list[str], out_degree: dict[str, int]) -> float:
    """Σ log(out-degree) over the hops a directed chain navigates (§5). A forced
    hop (out-degree 1) adds 0; a hop through a high-branching hub scores by that
    branching. RANKING-ONLY."""
    sig = 0.0
    for node in chain[:-1]:
        deg = out_degree.get(node, 0)
        if deg > 0:
            sig += log(deg)
    return sig
