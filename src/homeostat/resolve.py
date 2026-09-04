"""homeostat.resolve — the resolve-narrow engine: rank candidate MECHANISMS, disambiguate subtypes.

Where `narrative.read_story` generates the story WIDE (all the genre reads over the scoped
structure), this closes it NARROW: it groups the reads into candidate mechanisms and ranks them by
how well each coheres with THIS person's signals, driving H = log₂(candidate mechanisms) → 0.

A candidate mechanism is NOT a gene (ranking genes was the subject-fallacy we cut) — it is a
CONNECTED STORY-CLUSTER: the genre instances that share entities (a tragedy whose sink feeds a
vicious comedy, addressed by a quest = one coherent sub-etiology). The two autisms surface as two
clusters; the engine resolves which is THIS person's by coverage of their shadow × the cluster's own
internal phase-coherence, through the ModelAtlas blend (`recommend.score_candidate`). A surviving
plurality is not collapsed — it yields the Jeeves DO-THIS (the discriminating measurement).

Increment 1 (here): the candidate enumeration + coverage. The coherence-fit, the operator-injected
hypothesis (fluid-intelligence as a tested input, never ground truth), and the resolve loop follow.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Cluster:
    """A candidate mechanism: a connected story-cluster. `entities` is the gene/marker set it spans;
    `members` are the ``(genre, instance)`` reads inside it — the resolve-narrow unit."""

    entities: frozenset[str]
    members: tuple[tuple[str, object], ...]


def connected_components(sets: list[frozenset[str]]) -> list[frozenset[str]]:
    """Merge overlapping entity-sets into connected components: two story reads belong to the SAME
    candidate mechanism iff they share an entity (transitively). A set overlapping two disjoint
    groups MERGES them. Order-independent in result; empty -> []. Pure over the list of entity-sets.
    """
    comps: list[set[str]] = []
    for raw in sets:
        s = set(raw)
        overlapping = [c for c in comps if c & s]
        for c in overlapping:
            s |= c
            comps.remove(c)
        comps.append(s)
    return [frozenset(c) for c in comps]


def cluster_coverage(entities: frozenset[str], observed: frozenset[str]) -> float:
    """The COVERAGE alignment factor: the fraction of the observed shadow this candidate spans,
    ``|entities ∩ observed| / |observed|`` in [0, 1] — does the sub-story explain what we SEE? No
    observed -> 0.0 (nothing to cover). Pure over two sets.
    """
    if not observed:
        return 0.0
    return len(entities & observed) / len(observed)


def _tagged(genres: Mapping[str, list]) -> list[tuple[frozenset[str], str, object]]:
    """Each genre instance -> ``(its entity set, genre name, instance)``. The heterogeneous readers
    share no base type, so the entity projection is per-genre; held here, not in the readers."""
    out: list[tuple[frozenset[str], str, object]] = []
    for c in genres.get("comedy", []):
        out.append((frozenset({c.a, c.b}), "comedy", c))
    for t in genres.get("tragedy", []):
        out.append((frozenset({t.origin, t.sink}), "tragedy", t))
    for f in genres.get("allegory", []):
        out.append((frozenset({f.a, f.b}), "allegory", f))
    for q in genres.get("quest", []):
        out.append((frozenset({q.hero, *q.joined}), "quest", q))
    return out


def story_clusters(genres: Mapping[str, list]) -> list[Cluster]:
    """Group the story reads into candidate mechanisms: connected story-clusters over shared
    entities. Each cluster carries its entity span and the ``(genre, instance)`` reads inside it.
    Orchestration over the pinned `connected_components`; intent-tested.
    """
    tagged = _tagged(genres)
    comps = connected_components([ents for ents, _, _ in tagged])
    clusters = [
        Cluster(comp, tuple((name, inst) for ents, name, inst in tagged if ents & comp))
        for comp in comps
    ]
    return sorted(clusters, key=lambda cl: tuple(sorted(cl.entities)))
