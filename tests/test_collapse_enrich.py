"""Intent tests for the LD-collapse and the enrichment pure core, plus a
reader integration check against the real PopHuman file when present."""

from pathlib import Path

import pytest

from homeostat.collapse import Locus, collapse
from homeostat.enrich import af_bin, empirical_p, mean_stat

REAL_BW = Path(__file__).resolve().parents[1] / "data/selection_scans/iHS_GIH_10kb.bw"


def test_collapse_absorbs_within_window_and_keeps_lead():
    variants = [
        ("16", 30_900_000, 1.0),  # lead
        ("16", 30_950_000, 0.9),  # within 500kb -> absorbed
        ("16", 31_390_000, 0.8),  # within 500kb of lead -> absorbed
        ("16", 32_000_000, 0.7),  # beyond window of the LEAD -> new locus
        ("8", 30_900_000, 0.6),  # other chromosome -> new locus
    ]
    loci = collapse(variants, window_bp=500_000)
    assert loci == [
        Locus("16", 30_900_000, 1.0, 3),
        Locus("16", 32_000_000, 0.7, 1),
        Locus("8", 30_900_000, 0.6, 1),
    ]


def test_collapse_absorption_does_not_extend_territory():
    # 31.39M is absorbed by the 30.9M lead; a variant 400kb from the absorbed
    # one but >500kb from the lead must found its OWN locus.
    variants = [("1", 30_900_000, 1.0), ("1", 31_390_000, 0.9), ("1", 31_790_000, 0.8)]
    loci = collapse(variants, window_bp=500_000)
    assert [(lc.pos, lc.n_absorbed) for lc in loci] == [(30_900_000, 2), (31_790_000, 1)]


def test_collapse_deterministic_on_priority_ties():
    variants = [("2", 200, 1.0), ("1", 100, 1.0)]
    assert [lc.chrom for lc in collapse(variants)] == ["1", "2"]


class FakeTrack:
    def __init__(self, table):
        self.table = table

    def value_at(self, chrom, pos):
        return self.table.get((chrom, pos))


def test_mean_stat_abstains_below_min_pops():
    tracks = [FakeTrack({("1", 5): 2.0}), FakeTrack({("1", 5): 4.0}), FakeTrack({})]
    assert mean_stat(tracks, "1", 5, min_pops=2) == 3.0
    assert mean_stat(tracks, "1", 5, min_pops=3) is None  # abstain, never zero


def test_empirical_p_add_one():
    assert empirical_p(10.0, [1.0, 2.0, 3.0]) == pytest.approx(1 / 4)
    assert empirical_p(0.0, [1.0, 2.0, 3.0]) == pytest.approx(4 / 4)


def test_af_bin_edges():
    assert af_bin(0.0, 0.05) == 0
    assert af_bin(0.049, 0.05) == 0
    assert af_bin(0.05, 0.05) == 1
    assert af_bin(1.0, 0.05) == 19  # top edge folds into last bin


@pytest.mark.skipif(not REAL_BW.exists(), reason="PopHuman file not downloaded")
def test_bigwig_reader_on_real_pophuman_file():
    from homeostat.bigwig import BigWig

    with BigWig(str(REAL_BW)) as bw:
        assert len(bw.chroms) == 22
        bw.self_check()  # coverage within tolerance of header (see docstring)
        ivs = bw.query("chr2", 0, 1_000_000)
        for iv in ivs:
            assert 0 <= iv.value <= bw.max_val
            assert iv.end - iv.start == 10_000
