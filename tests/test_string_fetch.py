"""Intent tests for the STRING I/O shell — synthetic gzip fixtures, never the live network.

`load_rows` space-splits the links file (header dropped); `load_alias_map` builds ENSP→symbol from
the tab-separated info file (header dropped); `ensure` is idempotent. `fetch` hits the network and
is exercised by the real download, not here."""

import gzip

from homeostat import string, string_fetch


def _gz(path, text):
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        fh.write(text)
    return path


def test_load_rows_space_splits_and_drops_header(tmp_path):
    p = _gz(
        tmp_path / "links.txt.gz",
        "protein1 protein2 experimental database textmining combined_score\n"
        "9606.ENSP_A 9606.ENSP_B 312 0 0 311\n"
        "9606.ENSP_A 9606.ENSP_C 0 500 0 499\n",
    )
    rows = list(string_fetch.load_rows(p))
    assert len(rows) == 2  # header dropped
    assert rows[0] == ["9606.ENSP_A", "9606.ENSP_B", "312", "0", "0", "311"]


def test_load_alias_map_builds_ensp_to_symbol(tmp_path):
    p = _gz(
        tmp_path / "info.txt.gz",
        "#string_protein_id\tpreferred_name\tprotein_size\tannotation\n"
        "9606.ENSP_A\tRIPK2\t540\tReceptor-interacting kinase\n"
        "9606.ENSP_B\tTRAF6\t522\tE3 ubiquitin ligase\n",
    )
    alias = string_fetch.load_alias_map(p)
    assert alias == {"9606.ENSP_A": "RIPK2", "9606.ENSP_B": "TRAF6"}


def test_load_rows_feeds_the_renderer_end_to_end(tmp_path):
    links = _gz(
        tmp_path / "links.txt.gz",
        "protein1 protein2 experimental database textmining combined_score\n"
        "9606.ENSP_A 9606.ENSP_B 312 0 0 311\n",  # experimental -> kept
    )
    info = _gz(
        tmp_path / "info.txt.gz",
        "#string_protein_id\tpreferred_name\tprotein_size\tannotation\n"
        "9606.ENSP_A\tRIPK2\t540\tx\n9606.ENSP_B\tTRAF6\t522\ty\n",
    )
    alias = string_fetch.load_alias_map(info)
    events = string.string_events(string_fetch.load_rows(links), alias)
    got = [(e.subject, e.target, e.network, e.sign) for e in events]
    assert got == [("RIPK2", "TRAF6", "physical", 1)]


def test_ensure_does_not_redownload_a_present_cache(tmp_path, monkeypatch):
    dest = _gz(tmp_path / "links.txt.gz", "header\n")
    sha = tmp_path / "links.sha256"

    def _boom(*a, **k):
        raise AssertionError("fetch called despite a present cache")

    monkeypatch.setattr(string_fetch, "fetch", _boom)
    assert string_fetch.ensure("http://x", dest, sha) == dest
