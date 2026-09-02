"""homeostat.string_fetch — I/O shell for the STRING physical dump + its ENSP→symbol map.

No biology, no decisions (the renderer `string.py` holds those, pure): fetch the two gzipped
STRING files once, cache them gitignored under `data/string/`, sha256-pin each, stream the
physical links as space-split rows, and build the ENSP→gene-symbol map from the protein-info
file (the first harmonizing-normalization input). I/O-only — Detective-inexpressible;
intent-tested with synthetic fixtures. `fetch` hits the network (exercised by the real download).
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


def fetch(url: str, dest: Path) -> Path:
    """Download `url` to `dest`, atomically via a `.part` sibling. Sets the User-Agent header."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=180) as resp, open(part, "wb") as out:  # noqa: S310
        while chunk := resp.read(_CHUNK):
            out.write(chunk)
    part.replace(dest)
    return dest


def ensure(url: str, dest: Path, sha: Path) -> Path:
    """Return the cached file, downloading it once (and writing its sha256 sidecar) if absent."""
    if not dest.exists():
        fetch(url, dest)
        atomic_write_text(sha, sha256(dest) + "\n")
    return dest


def ensure_all() -> tuple[Path, Path]:
    """Ensure both STRING files are cached (links + info). Returns (links, info)."""
    links = ensure(paths.STRING_LINKS_URL, paths.STRING_LINKS, paths.STRING_LINKS_SHA)
    info = ensure(paths.STRING_INFO_URL, paths.STRING_INFO, paths.STRING_INFO_SHA)
    return links, info


def load_rows(path: Path = paths.STRING_LINKS) -> Iterator[list[str]]:
    """Stream the gzipped physical-links file as SPACE-split field lists, skipping the header.

    Header: `protein1 protein2 experimental database textmining combined_score`. Lazy — the human
    physical subnetwork is millions of rows.
    """
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        next(fh, None)  # drop the header row
        for line in fh:
            yield line.split()


def load_alias_map(path: Path = paths.STRING_INFO) -> dict[str, str]:
    """Build the ENSP → preferred_name (gene symbol) map from the gzipped protein-info file.

    Tab-separated, header dropped (`#string_protein_id preferred_name protein_size annotation`).
    The harmonizing normalization input the renderer keys on.
    """
    alias: dict[str, str] = {}
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        next(fh, None)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                alias[parts[0]] = parts[1]
    return alias
