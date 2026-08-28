"""Hand-authored intent tests for the pure E/I/R scoring core (homeostat.pbs).

Written from the checkpoint's intent (§7.1 filter logic), not from the code:
R-matches-I on a diverged site is enriched; R-matches-E is deprioritized to
zero; sites with no E/I direction carry no priority.
"""

from homeostat import pbs

N = pbs.HAP_N


def test_fst_zero_when_populations_identical():
    assert pbs.hudson_fst(0.3, N["SAS"], 0.3, N["EUR"]) == 0.0


def test_fst_high_when_populations_diverged():
    assert pbs.hudson_fst(0.95, N["SAS"], 0.05, N["EUR"]) > 0.7


def test_fst_clamped_to_unit_interval():
    assert 0.0 <= pbs.hudson_fst(1.0, N["SAS"], 0.0, N["EUR"]) <= 1.0
    assert pbs.hudson_fst(0.0, N["SAS"], 0.0, N["EUR"]) == 0.0


def test_pbs_positive_iff_focal_branch_diverged():
    diverged = pbs.pbs(0.8, 0.2, 0.2, N["SAS"], N["EUR"], N["EAS"])
    assert diverged > 0.5
    # Divergence on the CLOSE branch, not the focal one: focal sits with the outgroup.
    not_focal = pbs.pbs(0.2, 0.8, 0.2, N["SAS"], N["EUR"], N["EAS"])
    assert not_focal < diverged / 2


def test_i_shifted_allele_directions():
    assert pbs.i_shifted_allele(0.7, 0.2, "A", "G") == "G"  # alt elevated in I
    assert pbs.i_shifted_allele(0.2, 0.7, "A", "G") == "A"  # ref elevated in I
    assert pbs.i_shifted_allele(0.5, 0.5, "A", "G") == "none"


def test_r_dosage_counts_alleles():
    assert pbs.r_dosage("GG", "G") == 2
    assert pbs.r_dosage("AG", "G") == 1
    assert pbs.r_dosage("AA", "G") == 0


def test_priority_enriches_r_matches_i_and_zeroes_r_matches_e():
    # §7.1: R matches I, differs from E -> enrich.
    assert pbs.priority(1.2, 2) == 1.2
    assert pbs.priority(1.2, 1) == 0.6
    # §7.1: R matches E -> deprioritize (to zero, since the queue is the prior).
    assert pbs.priority(1.2, 0) == 0.0


def test_priority_floors_negative_pbs():
    assert pbs.priority(-0.4, 2) == 0.0
