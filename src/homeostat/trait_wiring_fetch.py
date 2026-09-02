"""homeostat.trait_wiring_fetch — I/O shell for the GWAS Catalog associations zip.

No biology, no decisions (`trait_wiring.py` holds the aggregation): fetch the ontology-annotated
zip once (~73.5 MB), cache it gitignored under `data/gwas/`, sha256-pin it, and stream the inner TSV
as tab-split rows. I/O-only, Detective-inexpressible; intent-tested. `fetch` hits the network.
"""

from __future__ import annotations

import io
import urllib.request
import zipfile
from collections.abc import Iterator
from pathlib import Path

from homeostat import paths
from homeostat.util import atomic_write_text, sha256

_UA = "curl/8.4"
_CHUNK = 1 << 20


def fetch(url: str, dest: Path, timeout: int = 300) -> Path:
    """Download `url` to `dest`, atomically via a `.part` sibling; User-Agent set."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(part, "wb") as out:  # noqa: S310
        while chunk := resp.read(_CHUNK):
            out.write(chunk)
    part.replace(dest)
    return dest


def ensure(
    url: str = paths.GWAS_URL, dest: Path = paths.GWAS_ZIP, sha: Path = paths.GWAS_SHA
) -> Path:
    """Return the cached zip, downloading it once (and writing its sha256 sidecar) if absent."""
    if not dest.exists():
        fetch(url, dest)
        atomic_write_text(sha, sha256(dest) + "\n")
    return dest


def load_rows(path: Path = paths.GWAS_ZIP) -> Iterator[list[str]]:
    """Stream the associations TSV from inside the zip as tab-split rows, header dropped. The TSV
    member is found dynamically (its name carries the release date). Lazy — ~1.19M rows."""
    with zipfile.ZipFile(path) as zf:
        member = next(n for n in zf.namelist() if n.endswith(".tsv"))
        with zf.open(member) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8", errors="replace")
            next(text, None)  # drop the header row
            for line in text:
                yield line.rstrip("\n").split("\t")
