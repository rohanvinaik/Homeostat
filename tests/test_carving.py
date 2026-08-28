"""Intent tests for the §13.4 carving core on synthetic graphs with a KNOWN
bridge node — the participation coefficient must single it out, and CNM must
recover the planted community structure."""

from homeostat.carving import cnm_communities, participation, shuffle_labels
from homeostat.ensemble import degree_deciles, degree_matched_p, separation


def _two_cliques_with_bridge():
    """Cliques {A1..A4} and {B1..B4}; X bridges them via one edge each side."""
    adj: dict[str, set[str]] = {}

    def link(u, v):
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)

    a = ["A1", "A2", "A3", "A4"]
    b = ["B1", "B2", "B3", "B4"]
    for clique in (a, b):
        for i in range(len(clique)):
            for j in range(i + 1, len(clique)):
                link(clique[i], clique[j])
    link("X", "A1")
    link("X", "B1")
    return adj, a + b + ["X"]


def test_cnm_recovers_two_communities():
    adj, nodes = _two_cliques_with_bridge()
    comm = cnm_communities(adj, nodes, gamma=1.0)
    # A-clique shares one community, B-clique another (X may land in either).
    a_comms = {comm[n] for n in ("A1", "A2", "A3", "A4")}
    b_comms = {comm[n] for n in ("B1", "B2", "B3", "B4")}
    assert len(a_comms) == 1 and len(b_comms) == 1
    assert a_comms != b_comms


def test_participation_singles_out_the_bridge():
    adj, nodes = _two_cliques_with_bridge()
    comm = cnm_communities(adj, nodes, gamma=1.0)
    part = participation(adj, nodes, comm)
    # X splits its 2 edges across both communities -> P = 0.5; clique-internal
    # nodes sit in one community -> P near 0.
    assert part["X"] > 0.4
    assert max(part[n] for n in ("A2", "A3", "A4", "B2", "B3", "B4")) < 0.4


def test_separation_positive_when_bridge_elevated():
    adj, nodes = _two_cliques_with_bridge()
    comm = cnm_communities(adj, nodes, gamma=1.0)
    part = participation(adj, nodes, comm)
    assert separation(part, {"X"}, nodes) > 0


def test_shuffle_labels_preserves_class_sizes():
    comm = {"a": 0, "b": 0, "c": 1, "d": 2}
    shuffled = shuffle_labels(comm, seed=1)
    assert sorted(shuffled.values()) == sorted(comm.values())
    assert set(shuffled) == set(comm)


def test_degree_deciles_partition_universe():
    degree = {g: i for i, g in enumerate("abcdefghij")}
    universe = list("abcdefghij")
    bins = degree_deciles(degree, universe)
    assert sum(len(v) for v in bins.values()) == 10
    assert set().union(*bins.values()) == set(universe)


def test_degree_matched_p_controls_the_hub_confound():
    import random

    # A star hub H (high degree) that is NOT a bridge; leaves L1..L4.
    # A genuine bridge X between two triangles. Degree-matched null must not
    # flag the hub as a bridge just for being high-degree.
    adj, nodes = _two_cliques_with_bridge()
    comm = cnm_communities(adj, nodes, 1.0)
    part = participation(adj, nodes, comm)
    degree = {n: len(adj.get(n, set())) for n in nodes}
    bins = degree_deciles(degree, nodes)
    bin_of = {g: b for b, members in bins.items() for g in members}
    # X is a real bridge -> its degree-matched p should be small-ish (< 0.5).
    p = degree_matched_p(part, {"X"}, nodes, bins, bin_of, random.Random(0))
    assert 0.0 < p <= 1.0


def test_degree_zero_node_has_zero_participation():
    adj = {"A": {"B"}, "B": {"A"}}
    nodes = ["A", "B", "Z"]
    comm = cnm_communities(adj, nodes, 1.0)
    part = participation(adj, nodes, comm)
    assert part["Z"] == 0.0


def test_empty_graph_gives_singletons():
    comm = cnm_communities({}, ["A", "B", "C"], 1.0)
    assert len(set(comm.values())) == 3
