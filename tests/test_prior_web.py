"""Intent tests for the multi-network assembly — build_prior_web with explicit events (no live I/O).

Pins the load-bearing config: only regulatory is directed, so a coupling with a regulatory supporter
earns direction while an undirected-vote-only coupling does not; convergence raises weight."""

from homeostat.event import Event
from homeostat.prior_web import DIRECTED_NETWORKS, build_prior_web


def test_only_regulatory_is_directed():
    assert "regulatory" in DIRECTED_NETWORKS
    assert len(DIRECTED_NETWORKS) == 1


def test_regulatory_supporter_earns_direction_others_do_not():
    events = [
        Event("regulatory", "amplifies", "A", "B", 1),  # directed network
        Event("physical", "binds", "A", "B", 1),  # undirected vote, same coupling
        Event("evolutionary", "resembles", "C", "D", 1),  # undirected-only coupling
    ]
    web = build_prior_web(events)
    by_pair = {(c.a, c.b): c for c in web.couplings}
    ab = by_pair[("A", "B")]
    assert ab.weight == 2
    assert ab.direction == 1
    cd = by_pair[("C", "D")]
    assert cd.weight == 1
    assert cd.direction == 0


def test_undirected_convergence_without_regulatory_stays_undirected():
    events = [
        Event("physical", "binds", "X", "Y", 1),
        Event("metabolic", "co-metabolizes", "X", "Y", 1),
    ]
    web = build_prior_web(events)
    xy = next(c for c in web.couplings if (c.a, c.b) == ("X", "Y"))
    assert xy.weight == 2
    assert xy.direction == 0
