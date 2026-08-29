"""Intent tests for the §8.4 enrichment pure pieces: MAF binning and the
streaming top-K + reservoir scan (no bigwig / real data required)."""

import gzip

from homeostat import eir_enrich


def test_maf_bin_fixed_width():
    assert eir_enrich.maf_bin(0.0) == 0
    assert eir_enrich.maf_bin(0.024) == 0
    assert eir_enrich.maf_bin(0.025) == 1
    assert eir_enrich.maf_bin(0.5) == 19  # top edge folds into last bin


def test_scan_pile_topk_and_reservoir(tmp_path, monkeypatch):
    monkeypatch.setattr(eir_enrich, "TOP_K", 2)
    monkeypatch.setattr(eir_enrich, "RESERVOIR_PER_BIN", 100)
    p = tmp_path / "pile.tsv.gz"
    with gzip.open(p, "wt") as f:
        f.write("chrom\tpos\tref\talt\taf_csa\taf_eur\taf_eas\tmaf_csa\tfst_csa_eur\tpbs_csa\n")
        # pbs ascending 0.1..0.5; top-2 by pbs = the last two rows
        for i, pbs_v in enumerate([0.1, 0.2, 0.5, 0.4, 0.3]):
            f.write(f"1\t{100 + i}\tA\tG\t0.3\t0.2\t0.25\t0.30\t0.05\t{pbs_v}\n")
    pile, reservoir = eir_enrich.scan_pile(str(p))
    top_pbs_positions = {pos for _c, pos, _b in pile}
    assert top_pbs_positions == {102, 103}  # pbs 0.5 and 0.4
    assert len(pile) == 2
    # all rows share one maf bin (0.30 → bin 11 by fixed-width binning); the
    # reservoir holds them all (matching is consistent since pile and controls
    # bin identically).
    (only_bin,) = reservoir.keys()
    assert len(reservoir[only_bin]) == 5
