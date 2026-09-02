"""Intent tests for the fungibility (allegory) interpretive layer.

A resembles pair is only the seed; fungibility is earned by convergence on shared partners across
independent confirming banks (≥2 = fungible/H3, 1 = coincidental, 0 = seed-only). Two paralogs that
share only *each other* have not converged on a role — that never counts."""

from homeostat.event import Event
from homeostat.fungibility import (
    Fungible,
    banks_converged,
    fungibility_verdict,
    paralog_seeds,
    partners_by_bank,
    read_fungibility,
)


def _res(a, b):
    return Event("evolutionary", "resembles", a, b, 1, "")


def _amp(a, b):
    return Event("regulatory", "amplifies", a, b, 1)


def _bind(a, b):
    return Event("physical", "binds", a, b, 1)


def _chan(a, b):
    return Event("metabolic", "channels", a, b, 1)


# ---- the pure verdict ------------------------------------------------------------


def test_fungibility_verdict_thresholds_on_independent_banks():
    assert fungibility_verdict(0) == "seed-only"  # resemblance alone, do not fold
    assert fungibility_verdict(1) == "coincidental"  # one bank could be chance
    assert fungibility_verdict(2) == "fungible"  # H3: orthogonal banks converge
    assert fungibility_verdict(3) == "fungible"


# ---- the seed + partner extraction -----------------------------------------------


def test_paralog_seeds_are_resembles_pairs_sorted_deduped():
    events = [_res("B", "A"), _res("A", "B"), _res("C", "C"), _amp("A", "B")]
    assert paralog_seeds(events) == {("A", "B")}  # sorted, deduped, self + non-seed dropped


def test_partners_by_bank_is_undirected_over_confirming_banks_only():
    events = [_amp("A", "C"), _bind("A", "D"), _res("A", "B"), _amp("A", "A")]
    partners = partners_by_bank(events)
    assert partners["regulatory"] == {"A": {"C"}, "C": {"A"}}  # undirected, self-loop dropped
    assert partners["physical"] == {"A": {"D"}, "D": {"A"}}
    assert "evolutionary" not in partners  # the seed bank never confirms


# ---- convergence counting --------------------------------------------------------


def test_banks_converged_counts_shared_third_parties_not_the_pair_itself():
    partners = partners_by_bank([_amp("A", "C"), _amp("B", "C"), _bind("A", "C"), _bind("B", "C")])
    assert banks_converged("A", "B", partners) == 2  # share C in regulatory AND physical
    # sharing only each other is not convergence on a role
    only_each_other = partners_by_bank([_amp("A", "B"), _amp("B", "A")])
    assert banks_converged("A", "B", only_each_other) == 0


# ---- the read --------------------------------------------------------------------


def test_read_fungibility_two_banks_earns_fungible():
    events = [_res("A", "B"), _amp("A", "C"), _amp("B", "C"), _bind("A", "C"), _bind("B", "C")]
    assert read_fungibility(events) == [Fungible("A", "B", "fungible", 2)]


def test_read_fungibility_one_bank_is_coincidental():
    events = [_res("A", "B"), _amp("A", "C"), _amp("B", "C")]
    assert read_fungibility(events) == [Fungible("A", "B", "coincidental", 1)]


def test_read_fungibility_resemblance_without_convergence_is_seed_only():
    events = [_res("A", "B"), _amp("A", "X"), _amp("B", "Y"), _chan("A", "X"), _chan("B", "Y")]
    assert read_fungibility(events) == [Fungible("A", "B", "seed-only", 0)]  # paths diverge
