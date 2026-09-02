"""Intent tests for the metabolic I/O shell — synthetic fixtures, never the live network.

`load_tsv` tab-splits a plain Reactome file; `load_entrez_symbol` builds Entrez→symbol from the
gzipped gene_info (header lines skipped); `ensure` is idempotent. `fetch` hits the network,
exercised by the real download, not here."""

import gzip

from homeostat import metabolic_fetch


def test_load_tsv_tab_splits(tmp_path):
    p = tmp_path / "rel.txt"
    p.write_text("R-HSA-1430728\tR-HSA-1\nR-HSA-1\tR-HSA-2\n", encoding="utf-8")
    rows = list(metabolic_fetch.load_tsv(p))
    assert rows == [["R-HSA-1430728", "R-HSA-1"], ["R-HSA-1", "R-HSA-2"]]


def test_load_entrez_symbol_skips_header_and_maps(tmp_path):
    p = tmp_path / "gene_info.gz"
    with gzip.open(p, "wt", encoding="utf-8") as fh:
        fh.write("#tax_id\tGeneID\tSymbol\tmore\n9606\t10\tHK1\tx\n9606\t20\tGPI\ty\n")
    assert metabolic_fetch.load_entrez_symbol(p) == {"10": "HK1", "20": "GPI"}


def test_ensure_does_not_redownload_a_present_cache(tmp_path, monkeypatch):
    dest = tmp_path / "NCBI2Reactome.txt"
    dest.write_text("x\ty\n", encoding="utf-8")

    def _boom(*a, **k):
        raise AssertionError("fetch called despite a present cache")

    monkeypatch.setattr(metabolic_fetch, "fetch", _boom)
    assert metabolic_fetch.ensure("http://x", dest, tmp_path / "s.sha256") == dest
