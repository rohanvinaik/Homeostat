"""Pure carving primitives for §13.4 — no I/O, deterministic.

A "carving" here is a partition of a gene set into communities, produced from
real PPI structure by greedy modularity maximization at a given resolution.
The resolution sweep IS the oracle ensemble (§6.3): each gamma is a different
mu. Participation coefficient measures how much a gene bridges communities —
the §5.8 bridge signal, read structurally.
"""

from collections import defaultdict


def cnm_communities(
    adj: dict[str, set[str]],
    nodes: list[str],
    gamma: float = 1.0,
) -> dict[str, int]:
    """Greedy (Clauset-Newman-Moore) modularity communities at resolution gamma.

    Deterministic: candidate merges are the community pairs sharing an edge,
    and ties in delta-Q break by the (smaller, larger) community-id pair.
    Returns node -> community id. Degree-0 nodes each form a singleton.

    delta_Q(a,b) = e_ab/m - gamma * deg_a * deg_b / (2 m^2)
    """
    node_set = set(nodes)
    deg = {n: len(adj.get(n, set()) & node_set) for n in nodes}
    m = sum(deg.values()) // 2
    if m == 0:
        return {n: i for i, n in enumerate(nodes)}

    comm = {n: i for i, n in enumerate(nodes)}
    comm_deg = {i: deg[n] for i, n in enumerate(nodes)}
    # edges between communities: symmetric, stored once per unordered pair
    between: dict[tuple[int, int], int] = defaultdict(int)
    for n in nodes:
        for nb in adj.get(n, set()) & node_set:
            if n < nb:  # each edge once
                ca, cb = comm[n], comm[nb]
                if ca != cb:
                    between[(min(ca, cb), max(ca, cb))] += 1

    members: dict[int, set[str]] = {i: {n} for i, n in enumerate(nodes)}

    def delta_q(a: int, b: int, e_ab: int) -> float:
        return e_ab / m - gamma * comm_deg[a] * comm_deg[b] / (2 * m * m)

    while between:
        best_pair = None
        best_dq = 0.0
        for (a, b), e_ab in between.items():
            dq = delta_q(a, b, e_ab)
            if dq > best_dq or (dq == best_dq and best_pair is not None and (a, b) < best_pair):
                best_dq = dq
                best_pair = (a, b)
        if best_pair is None or best_dq <= 0:
            break
        a, b = best_pair  # merge b into a
        for n in members[b]:
            comm[n] = a
        members[a] |= members.pop(b)
        comm_deg[a] += comm_deg.pop(b)
        # rebuild edges touching a or b
        new_between: dict[tuple[int, int], int] = defaultdict(int)
        for (x, y), e in between.items():
            if (x, y) == (a, b):
                continue
            x2 = a if x == b else x
            y2 = a if y == b else y
            if x2 == y2:
                continue
            new_between[(min(x2, y2), max(x2, y2))] += e
        between = new_between
    return comm


def participation(
    adj: dict[str, set[str]],
    nodes: list[str],
    comm: dict[str, int],
) -> dict[str, float]:
    """Participation coefficient P_i = 1 - sum_s (k_is/k_i)^2 (Guimera-Amaral).

    High P = edges spread across communities (a bridge). Degree-0 nodes -> 0.
    """
    node_set = set(nodes)
    out: dict[str, float] = {}
    for n in nodes:
        neigh = adj.get(n, set()) & node_set
        k = len(neigh)
        if k == 0:
            out[n] = 0.0
            continue
        per_comm: dict[int, int] = defaultdict(int)
        for nb in neigh:
            per_comm[comm[nb]] += 1
        out[n] = 1.0 - sum((c / k) ** 2 for c in per_comm.values())
    return out


def shuffle_labels(comm: dict[str, int], seed: int) -> dict[str, int]:
    """Permute community labels across nodes (the null carving): same class
    sizes, structure destroyed. Deterministic given seed."""
    import random

    rng = random.Random(seed)
    labels = list(comm.values())
    rng.shuffle(labels)
    return dict(zip(sorted(comm), labels, strict=True))
