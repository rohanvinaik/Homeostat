"""Intent tests for the PBS-restricted candidate-set construction (the new
load-bearing logic): top-K-by-PBS seeds, hard vs seeded, control naturalness."""

from homeostat.pbs_restricted import candidate_set, pbs_seeds
from homeostat.pbs_restricted_compare import jaccard


def test_seeds_are_top_k_by_pbs_within_string():
    weights = {"A": 0.9, "B": 0.5, "C": 0.8, "D": 0.1, "Z": 0.99}
    string_adj = {"A": {"B"}, "B": {"A"}, "C": {"B"}, "D": {"A"}}  # Z NOT in STRING
    seeds = pbs_seeds(weights, string_adj, 2)
    # Z has highest PBS but is not a STRING node -> excluded; top-2 of {A,B,C,D} = A,C
    assert seeds == ["A", "C"]


def test_hard_candidate_set_is_seeds_plus_controls_only():
    string_adj = {"A": {"X"}, "C": {"Y"}, "X": {"A"}, "Y": {"C"}}
    cand = candidate_set(["A", "C"], string_adj, "hard")
    # hard: no neighbor growth -> X, Y excluded; LRRK2/NOD2/RIPK2 force-added
    assert "A" in cand and "C" in cand
    assert "X" not in cand and "Y" not in cand
    assert {"LRRK2", "NOD2", "RIPK2"} <= cand


def test_seeded_candidate_set_grows_one_hop():
    string_adj = {"A": {"X"}, "C": {"Y"}, "X": {"A"}, "Y": {"C"}}
    cand = candidate_set(["A", "C"], string_adj, "seeded")
    # seeded: seeds' STRING neighbors X, Y are pulled in (candidate bridges)
    assert {"A", "C", "X", "Y"} <= cand


def test_jaccard():
    assert jaccard(["a", "b", "c"], ["a", "b", "c"]) == 1.0
    assert jaccard(["a", "b"], ["c", "d"]) == 0.0
    assert jaccard(["a", "b", "c", "d"], ["a", "b"]) == 0.5  # 2 common / 4 union
