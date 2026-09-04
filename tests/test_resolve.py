"""Intent tests for the resolve-narrow engine (increment 1) — candidate enumeration + coverage.
Authored from the design; `connected_components` / `cluster_coverage` are Detective-pinned."""

from homeostat.comedy import Comedy
from homeostat.event import Event
from homeostat.polarity import signed_adjacency as polar_adjacency
from homeostat.quest import Quest
from homeostat.resolve import (
    cluster_coherence,
    cluster_coverage,
    cluster_discriminant,
    cluster_meter,
    connected_components,
    rank_clusters,
    story_clusters,
)
from homeostat.topology import signed_adjacency as ternary_adjacency
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


def test_cluster_coverage_reach_credits_reaching_not_containing():
    # source S reaches symptom O (O's ancestor cone includes S) but the cluster does NOT contain O.
    # With `reach` the cluster covers O -> 1.0; without it (membership) S not in shadow -> 0.0.
    reach = {"O": {"S", "O"}}
    assert cluster_coverage(frozenset({"S"}), frozenset({"O"}), reach) == 1.0
    assert cluster_coverage(frozenset({"S"}), frozenset({"O"})) == 0.0


def test_cluster_coverage_reach_unreached_symptom_is_zero():
    # a cluster that neither is nor reaches the symptom scores 0 even with a reach map.
    assert cluster_coverage(frozenset({"Z"}), frozenset({"O"}), {"O": {"S", "O"}}) == 0.0


def test_cluster_coverage_reach_self_reach_is_covered():
    # the observed node as its own reacher, in the cluster -> covered (pins the reach residual).
    assert cluster_coverage(frozenset({"x"}), frozenset({"x"}), {"x": {"x"}}) == 1.0


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


# ---- cluster_coherence + rank_clusters (increment 2) -----------------------------


def test_cluster_coherence_reinforcing_cascade_phase_locks():
    # A->B->C all +1 (a vicious reinforcing dysregulation) -> the phasors align -> r = 1.
    assert cluster_coherence(frozenset({"A", "B", "C"}), {"A": {"B": 1}, "B": {"C": 1}}) == 1.0


def test_cluster_coherence_self_correcting_loop_destructively_interferes():
    # A->B (+1), B->A (-1): a homeostatic/balancing loop -> opposing phasors cancel -> r ~ 0 (NOT a
    # pathological reinforcing mechanism).
    assert cluster_coherence(frozenset({"A", "B"}), {"A": {"B": 1}, "B": {"A": -1}}) < 1e-9


def test_cluster_coherence_no_in_cluster_edges_is_zero():
    assert cluster_coherence(frozenset({"A"}), {"A": {"B": 1}}) == 0.0  # B outside the cluster


# ---- cluster_meter: the calibrated predictive coherence (SSL §9.3, the meter) --------


def test_cluster_meter_best_source_confirms_the_shadow():
    # {A,B}, A amplifies B, B observed up -> perturbing A +1 explains B: (1,0,0) -> 1/(1+1.5) = 0.4.
    assert cluster_meter(frozenset({"A", "B"}), {"A": [("B", 1)]}, {"B": 1}) == 0.4


def test_cluster_meter_no_entities_is_zero():
    assert cluster_meter(frozenset(), {"A": [("B", 1)]}, {"B": 1}) == 0.0


def test_cluster_meter_reach_credits_reaching_the_shadow():
    # A reaches symptom B (amplifies), B observed up, cluster {A} does NOT contain B.
    # With `reach`, A's record is scored against B -> meter > 0 (membership gave 0).
    reach = {"B": {"A", "B"}}
    assert cluster_meter(frozenset({"A"}), {"A": [("B", 1)]}, {"B": 1}, reach) == 0.4
    assert cluster_meter(frozenset({"A"}), {"A": [("B", 1)]}, {"B": 1}) == 0.0


def test_cluster_meter_scores_only_the_clusters_own_shadow():
    # an observed node OUTSIDE the cluster's entities is not the cluster's to explain -> excluded
    # from obs_in, so it never dilutes the meter (each cluster scored on its own sub-etiology).
    inside = cluster_meter(frozenset({"A", "B"}), {"A": [("B", 1)]}, {"B": 1})
    outside = cluster_meter(frozenset({"A", "B"}), {"A": [("B", 1)]}, {"B": 1, "Z": 1})
    assert inside == outside == 0.4  # Z (outside {A,B}) is filtered, no dilution


def test_cluster_meter_is_non_negative_persuasion_before_execution():
    # a conflicting source is scored on its BEST perturbation direction, so the meter never drops
    # below 0 -- the negative pole is the censor's domain, not the ranker's.
    m = cluster_meter(frozenset({"A", "B", "C"}), {"A": [("B", 1), ("C", 1)]}, {"B": 1, "C": -1})
    assert m >= 0.0


# ---- rank_clusters: the three-factor blend (coverage x coherence x meter) -------------


def test_rank_clusters_orders_by_the_three_factor_blend():
    # {A,B}: covers B, internally coherent, source A confirms B -> positive, ranked first.
    # {X,Y}: covers none of the shadow -> coverage 0 -> score 0, ranked last.
    genres = {
        "tragedy": [Tragedy("A", "B", "doomed")],
        "comedy": [Comedy("X", "Y", "vicious")],
    }
    clusters = story_clusters(genres)
    ranked = rank_clusters(
        clusters,
        {"B": 1},
        {"A": {"B": 1}, "X": {"Y": 1}, "Y": {"X": 1}},  # ternary — internal coherence
        {"A": [("B", 1)], "X": [("Y", 1)], "Y": [("X", 1)]},  # polar — predictive meter
    )
    assert ranked[0][0].entities == frozenset({"A", "B"}) and ranked[0][1] > 0.0
    assert ranked[-1][1] == 0.0  # the uncovered cluster ranks last


def test_rank_clusters_from_the_real_producers_end_to_end():
    # drive BOTH adjacencies from the REAL producers over actual Events (not hand-literals), so the
    # pin is against the signal rank_clusters consumes in drive -- closing the producer-seam gap.
    events = [Event("regulatory", "amplifies", "A", "B", 1)]
    verb_sign = {"amplifies": 1, "inhibits": -1}
    clusters = story_clusters({"tragedy": [Tragedy("A", "B", "doomed")]})
    ranked = rank_clusters(
        clusters, {"B": 1}, ternary_adjacency(events), polar_adjacency(events, verb_sign)
    )
    assert ranked[0][0].entities == frozenset({"A", "B"}) and ranked[0][1] > 0.0


# ---- cluster_discriminant: the mechanism-level Jeeves (incr.3b) -----------------------


def test_cluster_discriminant_disjoint_pair_picks_a_splitter():
    # {A,B} vs {C,D}: any node splits them 1/1 -> the first (sorted) is the measurement.
    assert cluster_discriminant([["A", "B"], ["C", "D"]]) == "A"


def test_cluster_discriminant_shared_root_picks_the_differentiator():
    # {A,B} and {A,C} share A (measuring A discriminates nothing) -> B is the differentiator.
    assert cluster_discriminant([["A", "B"], ["A", "C"]]) == "B"


def test_cluster_discriminant_prefers_the_even_split():
    # A is in 2 of 4 clusters (an even 2/2 split, max EIG); B/C/D/E/F each in only 1 (uneven).
    sets = [["A", "B"], ["A", "C"], ["D", "E"], ["D", "F"]]
    assert cluster_discriminant(sets) == "A"


def test_cluster_discriminant_none_when_identical_or_single():
    assert cluster_discriminant([["A", "B"], ["A", "B"]]) is None  # identical span
    assert cluster_discriminant([["A", "B"]]) is None  # < 2 clusters


def test_cluster_discriminant_uses_the_correct_eig_partition():
    # 3 clusters; A (in 1) and M (in 2) TIE on the true EIG [contain, n-contain] (symmetric), so the
    # sort picks A. A malformed [contain, n+contain] breaks the tie toward M -- pins the partition.
    assert cluster_discriminant([["A", "M"], ["M"], ["Z"]]) == "A"


def test_cluster_discriminant_has_no_positive_gain_floor():
    # 100 disjoint singletons: the best split's EIG ~0.08. A discriminant MUST still be returned
    # (best_gain starts at 0.0, not a positive floor that would suppress thin splits at scale).
    assert cluster_discriminant([[f"a{i}"] for i in range(100)]) == "a0"
