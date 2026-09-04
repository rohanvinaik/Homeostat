"""Intent tests for the resolve-narrow engine (increment 1) — candidate enumeration + coverage.
Authored from the design; `connected_components` / `cluster_coverage` are Detective-pinned."""

from homeostat.comedy import Comedy
from homeostat.quest import Quest
from homeostat.resolve import cluster_coverage, connected_components, story_clusters
from homeostat.tragedy import Tragedy

# ---- connected_components: the candidate-clustering primitive ---------------------


def test_connected_components_merges_overlapping_sets():
    assert connected_components([frozenset({"a", "b"}), frozenset({"b", "c"})]) == [
        frozenset({"a", "b", "c"})
    ]


def test_connected_components_keeps_disjoint_separate():
    comps = connected_components([frozenset({"a", "b"}), frozenset({"c", "d"})])
    assert set(comps) == {frozenset({"a", "b"}), frozenset({"c", "d"})}


def test_connected_components_bridges_two_groups_through_a_shared_set():
    # {a,b} and {c,d} are disjoint until {b,c} bridges them -> ONE component (transitive merge).
    comps = connected_components(
        [frozenset({"a", "b"}), frozenset({"c", "d"}), frozenset({"b", "c"})]
    )
    assert comps == [frozenset({"a", "b", "c", "d"})]


def test_connected_components_empty_is_empty():
    assert connected_components([]) == []


# ---- cluster_coverage: the first alignment factor --------------------------------


def test_cluster_coverage_is_the_fraction_of_the_shadow_spanned():
    assert cluster_coverage(frozenset({"A", "B", "X"}), frozenset({"A", "B", "C", "D"})) == 0.5


def test_cluster_coverage_full_and_none():
    assert cluster_coverage(frozenset({"A"}), frozenset({"A"})) == 1.0
    assert cluster_coverage(frozenset({"A"}), frozenset()) == 0.0  # no shadow -> 0


# ---- story_clusters: the candidate enumeration -----------------------------------


def test_story_clusters_two_disjoint_substories_are_two_candidates():
    # a tragedy on {FLAW,SINK} and a comedy on {X,Y} share nothing -> two candidate mechanisms.
    genres = {
        "tragedy": [Tragedy("FLAW", "SINK", "doomed")],
        "comedy": [Comedy("X", "Y", "vicious")],
    }
    clusters = story_clusters(genres)
    assert len(clusters) == 2
    assert {cl.entities for cl in clusters} == {
        frozenset({"FLAW", "SINK"}),
        frozenset({"X", "Y"}),
    }


def test_story_clusters_a_shared_entity_fuses_reads_into_one_candidate():
    # tragedy FLAW->SINK and a quest whose hero joins SINK share SINK -> ONE cluster (a coherent
    # sub-etiology: the doom, and the roundabout that addresses it).
    genres = {
        "tragedy": [Tragedy("FLAW", "SINK", "doomed")],
        "quest": [Quest("HERO", ("SINK", "OTHER"), 1.0, "resolving")],
    }
    clusters = story_clusters(genres)
    assert len(clusters) == 1
    assert clusters[0].entities == frozenset({"FLAW", "SINK", "HERO", "OTHER"})
    assert len(clusters[0].members) == 2  # the tragedy + the quest, one candidate mechanism
