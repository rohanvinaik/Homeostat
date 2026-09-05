"""Intent tests for the Compara homology I/O shell — synthetic gzip fixture, never the live network.

`load_rows` tab-splits the gzipped file (header dropped); `ensure` is idempotent. `fetch` hits the
network and is exercised by the real download, not here."""

import gzip

from homeostat import homology, homology_fetch

_HEADER = "gene_stable_id\tprotein_stable_id\tspecies\tidentity\thomology_type\t"
_HEADER += "homology_gene_stable_id\thomology_protein_stable_id\thomology_species\n"


def _row(protein_a, homology_type, protein_b, homology_species):
    cells = [""] * 8
    cells[1], cells[4], cells[6], cells[7] = protein_a, homology_type, protein_b, homology_species
    return "\t".join(cells)


def _gz(path, body):
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        fh.write(_HEADER + body)
    return path


def test_load_rows_tab_splits_and_drops_header(tmp_path):
    p = _gz(
        tmp_path / "homologies.tsv.gz",
        _row("ENSP_A", "within_species_paralog", "ENSP_B", "homo_sapiens") + "\n",
    )
    rows = list(homology_fetch.load_rows(p))
    assert len(rows) == 1  # header dropped
    assert rows[0][1] == "ENSP_A"
    assert rows[0][4] == "within_species_paralog"


def test_load_rows_feeds_the_renderer_end_to_end(tmp_path):
    p = _gz(
        tmp_path / "homologies.tsv.gz",
        _row("ENSP_A", "within_species_paralog", "ENSP_B", "homo_sapiens")
        + "\n"
        + _row("ENSP_A", "ortholog_one2one", "ENSPPTR_X", "pan_troglodytes")
        + "\n",
    )
    alias = {"9606.ENSP_A": "LRRK2", "9606.ENSP_B": "LRRK1"}
    events = homology.homology_events(homology_fetch.load_rows(p), alias)
    got = [(e.subject, e.target, e.network, e.sign) for e in events]
    assert got == [("LRRK2", "LRRK1", "evolutionary", 1)]  # ortholog dropped


def test_ensure_does_not_redownload_a_present_cache(tmp_path, monkeypatch):
    dest = _gz(tmp_path / "homologies.tsv.gz", "")
    monkeypatch.setattr(homology_fetch.paths, "HOMOLOGY_SHA", tmp_path / "h.sha256")

    def _boom(*a, **k):
        raise AssertionError("fetch called despite a present cache")

    monkeypatch.setattr(homology_fetch, "fetch", _boom)
    assert homology_fetch.ensure(dest=dest) == dest
