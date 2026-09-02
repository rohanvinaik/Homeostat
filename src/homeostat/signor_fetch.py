"""homeostat.signor_fetch — the I/O shell for the SIGNOR dump: download, cache, hash-pin, stream.

No biology and no decisions here (the renderer `signor.py` holds those, pure): fetch the human
SIGNOR TSV once, cache it gitignored under `data/signor/`, pin its sha256 for drift, and stream its
tab-split rows into `signor.signor_events`. SIGNOR's `getData.php` serves tab-separated text with no
header (29 cols) and 403s a bare urllib User-Agent, so the request sets one. I/O-only — Detective-
inexpressible (takes URLs / paths / live bytes); intent-tested with a synthetic fixture.
"""

from __future__ import annotations

import hashlib
import urllib.request
from collections.abc import Iterator
from pathlib import Path

from homeostat import paths
from homeostat.util import atomic_write_text

_UA = "curl/8.4"  # SIGNOR 403s a default urllib User-Agent
_CHUNK = 1 << 20


def sha256(path: Path) -> str:
    """The sha256 hex digest of a file, read in chunks (the dump is ~21 MB)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(_CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str = paths.SIGNOR_URL, dest: Path = paths.SIGNOR_TSV) -> Path:
    """Download the SIGNOR dump to `dest`, atomically via a `.part` sibling (a crash mid-write can
    never leave a torn cache). Overwrites any existing file — use `ensure` to fetch only if absent.
    Returns `dest`. Sets the required User-Agent header.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=120) as resp, open(part, "wb") as out:  # noqa: S310
        while chunk := resp.read(_CHUNK):
            out.write(chunk)
    part.replace(dest)
    return dest


def ensure(url: str = paths.SIGNOR_URL, dest: Path = paths.SIGNOR_TSV) -> Path:
    """Return the cached dump, downloading it once (and writing its sha256 sidecar) if absent.

    Idempotent: an existing cache is used as-is — re-hash it against `SIGNOR_SHA` / the manifest to
    detect a stale version; delete the file to force a refresh.
    """
    if not dest.exists():
        fetch(url, dest)
        atomic_write_text(paths.SIGNOR_SHA, sha256(dest) + "\n")
    return dest


def load_rows(path: Path = paths.SIGNOR_TSV) -> Iterator[list[str]]:
    """Stream the cached TSV as tab-split field lists (no header) — input to `signor.signor_events`.
    Yields lazily so the 43K-row / 21 MB dump never fully materializes.
    """
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            yield line.rstrip("\n").split("\t")
