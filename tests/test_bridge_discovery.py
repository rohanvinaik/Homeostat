"""Intent test for the genome-wide degree-matched participation ranking."""

from homeostat.bridge_discovery import degree_matched_p


def test_degree_matched_p_ranks_high_participation_within_band():
    # Three genes of the SAME degree (2): X spans communities (high part), Y and Z
    # do not (low part). X should get the smallest degree-matched p.
    deg = {"X": 2, "Y": 2, "Z": 2}
    part = {"X": 0.5, "Y": 0.0, "Z": 0.0}
    p = degree_matched_p(part, deg, ["X", "Y", "Z"])
    assert p["X"] < p["Y"]
    assert p["X"] < p["Z"]
    # X is the sole highest-participation gene in its degree band -> p = 1/3
    assert abs(p["X"] - 1 / 3) < 1e-9


def test_degree_matched_p_isolated_band_returns_one():
    # A gene with a unique degree has a band of size 1 (itself) -> p = 1.0.
    deg = {"A": 5, "B": 100}
    part = {"A": 0.9, "B": 0.9}
    p = degree_matched_p(part, deg, ["A", "B"])
    assert p["A"] == 1.0 and p["B"] == 1.0
