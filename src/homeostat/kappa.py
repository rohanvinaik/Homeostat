"""The κ / significance math, transported from Regenesis `significance.py`.

Faithful correspondence (definitions mirrored, not reinvented):
- `reachable`, `coverage`, `marginal_coverage`  -> verbatim (directed graphs;
  used for the LLM's directed proposed chains + chain_significance).
- `weak_components`, `is_bridge`                 -> verbatim: a bridge joins two
  previously-DISJOINT components (§13's definition).
- `chain_significance`                           -> Σ log(out-degree) over the
  ancestor hops a chain navigates (§5).

Transport note (documented, load-bearing): SIGNIFICANCE_WEIGHTING §5 states
κ = marginal coverage = hub-score = genealogy PageRank. Regenesis uses the
reachable-set-size FORM because its rule graph is a directed DAG where reachable
sets differ per node. On an UNDIRECTED gene structure graph (STRING physical,
GTEx co-expression) reachable-set-size degenerates to component size, so we use
the equivalent PAGERANK form of κ. Same quantity, the form that does not
degenerate on this substrate.
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
    components? §13's definition, verbatim (Regenesis `is_bridge`)."""
    comps = weak_components(adj)
    home = {n: i for i, c in enumerate(comps) for n in c}
    a, c = home.get(antecedent), home.get(consequent)
    return a is not None and c is not None and a != c


def pagerank(
    adj: dict[str, set[str]], damping: float = 0.85, iters: int = 100, tol: float = 1e-9
) -> dict[str, float]:
    """κ as hub-score: PageRank over the (undirected-symmetrised) graph.

    Deterministic: fixed iteration count with sorted node order, dangling mass
    redistributed uniformly. This is the §5 κ = hub-score = PageRank form.
    """
    undirected: dict[str, set[str]] = {}
    nodes = sorted(set(adj) | {t for outs in adj.values() for t in outs})
    for u in nodes:
        undirected.setdefault(u, set())
    for u, outs in adj.items():
        for v in outs:
            undirected[u].add(v)
            undirected[v].add(u)
    n = len(nodes)
    if n == 0:
        return {}
    rank = dict.fromkeys(nodes, 1.0 / n)
    for _ in range(iters):
        dangling = sum(rank[x] for x in nodes if not undirected[x])
        new = {}
        base = (1.0 - damping) / n + damping * dangling / n
        for node in nodes:
            s = 0.0
            for nb in undirected[node]:
                deg = len(undirected[nb])
                if deg:
                    s += rank[nb] / deg
            new[node] = base + damping * s
        if max(abs(new[x] - rank[x]) for x in nodes) < tol:
            rank = new
            break
        rank = new
    return rank


def personalized_pagerank(
    adj: dict[str, set[str]],
    prior: dict[str, float],
    damping: float = 0.85,
    iters: int = 100,
    tol: float = 1e-9,
) -> dict[str, float]:
    """κ with a non-uniform teleportation prior — the §10.3 selection-weighted κ.

    Identical to `pagerank` except the restart/dangling mass lands on nodes in
    proportion to `prior` (normalized over the node set) instead of uniformly. So
    genes under strong differential selection (high PBS) get higher PRIOR
    participation, and that prior DIFFUSES through the structure (a gene coupled to
    high-prior genes is lifted too — the coherence math, not a per-node multiply).
    Genes absent from `prior` get weight 0; if the prior sums to 0 it falls back to
    uniform (i.e. plain PageRank). Deterministic (sorted node order, fixed iters).
    """
    undirected: dict[str, set[str]] = {}
    nodes = sorted(set(adj) | {t for outs in adj.values() for t in outs})
    for u in nodes:
        undirected.setdefault(u, set())
    for u, outs in adj.items():
        for v in outs:
            undirected[u].add(v)
            undirected[v].add(u)
    n = len(nodes)
    if n == 0:
        return {}
    total = sum(max(prior.get(x, 0.0), 0.0) for x in nodes)
    if total <= 0.0:
        p = dict.fromkeys(nodes, 1.0 / n)
    else:
        p = {x: max(prior.get(x, 0.0), 0.0) / total for x in nodes}
    rank = dict(p)
    for _ in range(iters):
        dangling = sum(rank[x] for x in nodes if not undirected[x])
        new = {}
        for node in nodes:
            s = 0.0
            for nb in undirected[node]:
                deg = len(undirected[nb])
                if deg:
                    s += rank[nb] / deg
            new[node] = (1.0 - damping) * p[node] + damping * (s + dangling * p[node])
        if max(abs(new[x] - rank[x]) for x in nodes) < tol:
            rank = new
            break
        rank = new
    return rank


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
