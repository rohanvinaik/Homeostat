from __future__ import annotations

import urllib.error

import pytest
from scripts.build_glossary import ensure_source


def test_ensure_source_downloads_atomically_and_reuses_the_cache(tmp_path):
    remote = tmp_path / "remote"
    remote.mkdir()
    source = remote / "human_disease_knowledge_filtered.tsv"
    source.write_bytes(b"gene\tdisease\n")
    cache = tmp_path / "cache"

    result = ensure_source("knowledge", cache, remote.as_uri())

    assert result.read_bytes() == source.read_bytes()
    assert result.with_suffix(".sha256").read_text() == (
        "995858d09dfeb1cdc60e4429dfe924188e8df35cc378c6a507a67df46b243211\n"
    )
    assert not result.with_suffix(result.suffix + ".part").exists()
    source.unlink()
    assert ensure_source("knowledge", cache, remote.as_uri()) == result


def test_ensure_source_rejects_an_unknown_channel(tmp_path):
    with pytest.raises(ValueError, match="unknown DISEASES channel"):
        ensure_source("rumour", tmp_path)


def test_ensure_source_removes_a_partial_file_after_failure(tmp_path):
    cache = tmp_path / "cache"

    with pytest.raises(urllib.error.URLError):
        ensure_source("experiments", cache, (tmp_path / "missing").as_uri())

    assert not (cache / "human_disease_experiments_filtered.tsv.part").exists()
