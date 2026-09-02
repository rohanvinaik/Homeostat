"""homeostat.homology_fetch — I/O shell for the Ensembl Compara human homologies dump.

No biology, no decisions (the renderer `homology.py` holds those, pure): fetch the gzipped Compara
homologies TSV once, cache it gitignored under `data/homology/`, sha256-pin it, and stream its
tab-split rows. The file is human-vs-all-species (mostly orthologs the renderer discards); its
endpoints carry Ensembl protein ids normalized to gene symbols via the shared STRING info map
(`string_fetch.load_alias_map`). I/O-only — Detective-inexpressible; intent-tested with a fixture.
"""

from __future__ import annotations

import gzip
import urllib.request
from collections.abc import Iterator
from pathlib import Path

from homeostat import paths
from homeostat.util import atomic_write_text, sha256

_UA = "curl/8.4"
_CHUNK = 1 << 20


def fetch(url: str = paths.HOMOLOGY_URL, dest: Path = paths.HOMOLOGY_TSV) -> Path:
    """Download the Compara dump to `dest`, atomically via a `.part` sibling. Sets the UA header."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=300) as resp, open(part, "wb") as out:  # noqa: S310
        while chunk := resp.read(_CHUNK):
            out.write(chunk)
    part.replace(dest)
    return dest


def ensure(url: str = paths.HOMOLOGY_URL, dest: Path = paths.HOMOLOGY_TSV) -> Path:
    """Return the cached dump, downloading it once (and writing its sha256 sidecar) if absent."""
    if not dest.exists():
        fetch(url, dest)
        atomic_write_text(paths.HOMOLOGY_SHA, sha256(dest) + "\n")
    return dest


def load_rows(path: Path = paths.HOMOLOGY_TSV) -> Iterator[list[str]]:
    """Stream the gzipped homologies TSV as tab-split field lists, skipping the header. Lazy — the
    file is ~140 MB gzipped, mostly cross-species orthologs the renderer filters out.
    """
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        next(fh, None)  # drop the header row
        for line in fh:
            yield line.rstrip("\n").split("\t")
