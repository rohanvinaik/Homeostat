"""Intent tests for the §8.4 LD-thinned re-test (pure parts)."""

import random

from homeostat.eir_enrich_ldthin import maf_matched_perm, thin_pile


def test_thin_takes_one_per_1mb_window():
    # three variants in window 0 of chr1, one in window 1 -> exactly 2 kept.
    pile = [
        ("1", 10, 0),
        ("1", 20, 0),
        ("1", 30, 0),
        ("1", 1_000_005, 1),
    ]
    thinned = thin_pile(pile, random.Random(0))
    windows = {(c, p // 1_000_000) for c, p, _b in thinned}
    assert len(thinned) == 2
    assert windows == {("1", 0), ("1", 1)}


def test_thin_is_deterministic_under_seed():
    pile = [("1", i, 0) for i in range(50)]  # all in window 0
    a = thin_pile(pile, random.Random(7))
    b = thin_pile(pile, random.Random(7))
    assert a == b and len(a) == 1


def test_perm_enriched_when_observed_exceeds_controls():
    need = {0: 5}
    control_ihs = {0: [0.1, 0.0, 0.2, 0.15, 0.05, 0.12, 0.08]}
    p, n_used = maf_matched_perm(need, control_ihs, observed=0.9, n_perm=1000, rng=random.Random(0))
    assert p < 0.05 and n_used == 1000


def test_perm_null_when_observed_matches_controls():
    need = {0: 5}
    control_ihs = {0: [0.5] * 12}
    p, _n = maf_matched_perm(need, control_ihs, observed=0.5, n_perm=1000, rng=random.Random(0))
    assert p > 0.05  # all ties -> add-one -> p == 1.0
