"""Intent tests for the SIGNOR I/O shell — synthetic fixtures, never the live network.

The shell is Detective-inexpressible (URLs / paths / live bytes), so it is intent-tested.
`load_rows` tab-splits a tiny fixture into the shape `signor_events` consumes, `sha256` is stable,
and `ensure` is idempotent (never re-downloads a present cache). `fetch` itself hits the network and
is exercised end-to-end by the real download, not here.
"""

import hashlib

import pytest

from homeostat import signor, signor_fetch

# two real SIGNOR row shapes, padded to 29 cols (tab-separated in the dump)
_ROW_A = ["RIPK2", "protein", "id1", "x", "TRAF6", "protein", "id2", "x", "up-regulates activity"]
_ROW_B = ["PTEN", "protein", "id3", "x", "AKT1", "protein", "id4", "x", "down-regulates activity"]


def _fixture(path):
    lines = ["\t".join(r + [""] * (29 - len(r))) for r in (_ROW_A, _ROW_B)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_load_rows_yields_tab_split_fields(tmp_path):
    p = _fixture(tmp_path / "signor.tsv")
    rows = list(signor_fetch.load_rows(p))
    assert len(rows) == 2
    assert all(len(r) == 29 for r in rows)
    assert rows[0][0] == "RIPK2"
    assert rows[0][4] == "TRAF6"


def test_load_rows_feeds_the_renderer_end_to_end(tmp_path):
    p = _fixture(tmp_path / "signor.tsv")
    events = signor.signor_events(signor_fetch.load_rows(p))
    assert [(e.subject, e.target, e.verb, e.sign) for e in events] == [
        ("RIPK2", "TRAF6", "amplifies", 1),
        ("PTEN", "AKT1", "inhibits", 1),
    ]


def test_sha256_matches_hashlib(tmp_path):
    p = tmp_path / "blob"
    p.write_bytes(b"signor-bytes")
    assert signor_fetch.sha256(p) == hashlib.sha256(b"signor-bytes").hexdigest()


def test_ensure_does_not_redownload_a_present_cache(tmp_path, monkeypatch):
    dest = _fixture(tmp_path / "signor.tsv")

    def _boom(*a, **k):  # ensure must NOT call fetch when the cache exists
        raise AssertionError("fetch called despite a present cache")

    monkeypatch.setattr(signor_fetch, "fetch", _boom)
    assert signor_fetch.ensure(dest=dest) == dest


def test_ensure_fetches_and_pins_when_absent(tmp_path, monkeypatch):
    dest = tmp_path / "signor.tsv"
    sha_sidecar = tmp_path / "signor.sha256"
    monkeypatch.setattr(signor_fetch.paths, "SIGNOR_SHA", sha_sidecar)

    def _fake_fetch(url, d):
        _fixture(d)
        return d

    monkeypatch.setattr(signor_fetch, "fetch", _fake_fetch)
    out = signor_fetch.ensure(dest=dest)
    assert out == dest
    assert dest.exists()
    assert sha_sidecar.read_text().strip() == signor_fetch.sha256(dest)


@pytest.mark.parametrize("missing", ["", " "])
def test_load_rows_missing_file_raises(tmp_path, missing):
    with pytest.raises(FileNotFoundError):
        list(signor_fetch.load_rows(tmp_path / f"nope{missing}.tsv"))
