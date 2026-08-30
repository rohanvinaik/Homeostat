"""Intent tests for the §8.4 LD-block permutation (pure part)."""

import random

from homeostat.eir_enrich_block import maf_matched_block_perm


def test_enriched_when_pile_blocks_exceed_controls():
    # observed above every control block -> no null draw reaches it -> small p.
    need = {0: 3}
    control_by_bin = {0: [0.1, 0.2, 0.15, 0.05, 0.12]}
    p, n_used, underfilled = maf_matched_block_perm(
        need, control_by_bin, observed=0.9, n_perm=1000, rng=random.Random(0)
    )
    assert p < 0.05
    assert n_used == 1000
    assert underfilled == []


def test_null_when_observed_matches_control_level():
    need = {0: 3}
    control_by_bin = {0: [0.5] * 10}  # every draw averages exactly 0.5
    p, _n, _u = maf_matched_block_perm(
        need, control_by_bin, observed=0.5, n_perm=1000, rng=random.Random(0)
    )
    assert p > 0.05  # ties count via add-one -> p == 1.0


def test_underfilled_bin_is_reported():
    need = {0: 5, 1: 2}
    control_by_bin = {0: [0.1, 0.2], 1: [0.3, 0.4, 0.5]}  # bin 0 has fewer than needed
    _p, _n, underfilled = maf_matched_block_perm(
        need, control_by_bin, observed=0.9, n_perm=100, rng=random.Random(0)
    )
    assert underfilled == [0]
