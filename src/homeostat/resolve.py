"""homeostat.resolve — the resolve-narrow engine: rank candidate MECHANISMS, disambiguate subtypes.

Where `narrative.read_story` generates the story WIDE (all the genre reads over the scoped
structure), this closes it NARROW: it groups the reads into candidate mechanisms and ranks them by
how well each coheres with THIS person's signals, driving H = log₂(candidate mechanisms) → 0.

A candidate mechanism is NOT a gene (ranking genes was the subject-fallacy we cut) — it is a
CONNECTED STORY-CLUSTER: the genre instances that share entities (a tragedy whose sink feeds a
vicious comedy, addressed by a quest = one coherent sub-etiology). The two autisms surface as two
clusters; the engine resolves which is THIS person's by THREE distinct signals — coverage of their
shadow × the cluster's internal phase-coherence × the calibrated predictive meter (SSL §9.3) — kept
orthogonal and combined through the ModelAtlas blend (`recommend.score_candidate`). A surviving
plurality is not collapsed — it yields the Jeeves DO-THIS (the discriminating measurement).

Built (here): candidate enumeration, coverage, internal-coherence, the calibrated predictive meter
(`cluster_meter` over `meter.coherence_meter`), and the ranked three-factor blend. Still to come:
the operator-injected hypothesis (fluid-intelligence as a tested input, never ground truth), the
Jeeves DO-THIS on a surviving plurality, and the GWAS relevance-seeding.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from homeostat.jeeves import expected_information_gain
from homeostat.meter import coherence_meter, source_outcomes
from homeostat.polarity import SignedAdj
from homeostat.quest import order_parameter, part_vector
from homeostat.recommend import score_candidate


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


def cluster_coverage(
    entities: frozenset[str],
    observed: frozenset[str],
    reach: Mapping[str, set[str]] | None = None,
) -> float:
    """The COVERAGE alignment factor: the fraction of the observed shadow this candidate EXPLAINS.
    A mechanism is relevant to the degree it REACHES the shadow, not contains it: with `reach` (each
    observed node -> its ancestor set, who reaches it), a cluster covers `o` iff one of its entities
    reaches `o` (``entities & reach[o]``). Without `reach` (None) it degenerates to membership
    ``|entities & observed|`` -- the self-only reach. In [0, 1]; no observed -> 0.0. Pure.
    """
    if not observed:
        return 0.0
    if reach is None:
        covered = len(entities & observed)
    else:
        covered = sum(1 for o in observed if entities & reach.get(o, frozenset({o})))
    return covered / len(observed)


def cluster_coherence(
    entities: frozenset[str], signed_adj: Mapping[str, Mapping[str, int]]
) -> float:
    """The INTERNAL-COHERENCE alignment factor: does the cluster's sub-web form a phase-locked
    (reinforcing) mechanism, or a conflicting / self-correcting structure? The Kuramoto order
    parameter over the sub-web's SIGNED EDGES (each edge -> a phasor via `quest.part_vector`,
    SUPPORT in-phase / OPPOSE antiphase / informational-zero a zero vector). A vicious reinforcing
    cascade phase-locks (high r -> a real dysregulation); a balancing or contradictory structure
    destructively interferes (low r -> not a pathological mechanism). Works for cycles and cascades
    alike (no source/depth needed). No in-cluster edges -> 0.0. Orchestration over the pinned
    `part_vector` / `order_parameter`.
    """
    vectors = [
        part_vector(sign, 0, 0)
        for u, nbrs in signed_adj.items()
        if u in entities
        for v, sign in nbrs.items()
        if v in entities
    ]
    return order_parameter(vectors)


def cluster_meter(
    entities: frozenset[str],
    signed_polar: SignedAdj,
    observed: Mapping[str, int],
    reach: Mapping[str, set[str]] | None = None,
) -> float:
    """The cluster's calibrated PREDICTIVE coherence: the best member-source's `coherence_meter`
    over the cluster's own observed shadow — the mechanism's load-bearing driver, the single
    perturbation that best explains the observed cone (`meter.source_outcomes`, the polarity-censor
    machinery read soft). Because each source is scored on its BEST perturbation direction
    (persuasion before execution: ``confirmed = max(n₊, n₋) ≥ contradicted``), the source-driven
    meter is already ≥ 0 — the negative pole is structurally the polarity CENSOR's domain (a hard
    veto upstream), not the ranker's, so `rank_clusters`'s ``max(0, ·)`` is a guard, never a
    truncation of live signal. `coherence_meter` keeps the full ternary (-1, 1) for any
    non-best-direction use. No entities → 0.0 (informational zero). Orchestration over the pinned
    `source_outcomes` / `coherence_meter`. The cluster's shadow is what it REACHES (`reach`, the
    sibling of `cluster_coverage`), not what it contains; None -> membership (the self-only reach).
    """
    if reach is None:
        obs_in = {o: observed[o] for o in observed if o in entities}
    else:
        obs_in = {o: observed[o] for o in observed if entities & reach.get(o, frozenset({o}))}
    meters = [
        coherence_meter(*source_outcomes(signed_polar, src, obs_in)) for src in sorted(entities)
    ]
    return max(meters) if meters else 0.0


def rank_clusters(
    clusters: list[Cluster],
    observed: Mapping[str, int],
    signed_ternary: Mapping[str, Mapping[str, int]],
    signed_polar: SignedAdj,
    reach: Mapping[str, set[str]] | None = None,
) -> list[tuple[Cluster, float]]:
    """Rank the candidate mechanisms (resolve-narrow): each cluster scored by the ModelAtlas blend
    (`recommend.score_candidate`) over THREE alignment factors, each a distinct signal (orthogonal
    information is kept, never collapsed): COVERAGE of the observed shadow × internal COHERENCE
    (`cluster_coherence`, phase-lock over the OTP-ternary sub-web `signed_ternary`) × the calibrated
    predictive METER (`cluster_meter`, the SSL §9.3 track record over the polarity sub-web
    `signed_polar`, DIRECTIONALLY GATED by `max(0, ·)` — a rectifier at the ranking boundary, not an
    abandonment of the ternary; the negative pole stays live for the censor). `observed` is the sign
    map (its keys are the shadow). Descending; ties keep order. A near-tie at the top is a surviving
    plurality — the Jeeves cue. Orchestration over the pinned factors + `score_candidate`.
    """
    shadow = frozenset(observed)
    scored = [
        (
            cl,
            score_candidate(
                [
                    cluster_coverage(cl.entities, shadow, reach),
                    cluster_coherence(cl.entities, signed_ternary),
                    max(0.0, cluster_meter(cl.entities, signed_polar, observed, reach)),
                ],
                [],
            ),
        )
        for cl in clusters
    ]
    return sorted(scored, key=lambda t: t[1], reverse=True)


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


def cluster_discriminant(entity_sets: list[list[str]]) -> str | None:
    """The mechanism-level Jeeves measurement: given the TIED candidate mechanisms' entity sets (the
    surviving plurality the ranking could not separate), the node whose membership best SPLITS them
    — a node in some but not all clusters, chosen by max `jeeves.expected_information_gain` over the
    ``[contains, does-not]`` partition (an even split carries the most information — the same
    Lindley/Howard EIG the elimination Jeeves uses, lifted from genes to mechanisms). Measuring
    whether that node is deviated tells you which mechanism is THIS person's. None when < 2 sets or
    no node discriminates (the tied mechanisms share the same span). Pure over ``list[list[str]]``.
    """
    sets = [set(s) for s in entity_sets]
    if len(sets) < 2:
        return None
    everywhere = set.intersection(*sets)
    best_node: str | None = None
    best_gain = 0.0
    for node in sorted(set().union(*sets) - everywhere):
        contain = sum(1 for s in sets if node in s)
        gain = expected_information_gain([contain, len(sets) - contain])
        if gain > best_gain:
            best_gain = gain
            best_node = node
    return best_node
