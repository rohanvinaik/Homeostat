"""homeostat.metabolic_fetch — I/O shell for the Reactome metabolic + NCBI gene_info dumps.

No biology, no decisions (the renderer `metabolic.py` holds those, pure): fetch three files once,
cache them gitignored under `data/metabolic/`, sha256-pin each, and stream/build the rows the
renderer consumes — Reactome NCBI2Reactome (Entrez→pathway) and ReactomePathwaysRelation (parent→
child), both
plain TSV, and the gzipped NCBI gene_info (Entrez→symbol). I/O-only — Detective-inexpressible;
intent-tested with fixtures. `fetch` hits the network (exercised by the real download).
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


def ensure_all() -> tuple[Path, Path, Path]:
    """Ensure all three files. Returns (ncbi2reactome, relation, gene_info)."""
    r = ensure(paths.NCBI2REACTOME_URL, paths.NCBI2REACTOME, paths.NCBI2REACTOME_SHA)
    rel = ensure(paths.REACTOME_RELATION_URL, paths.REACTOME_RELATION, paths.REACTOME_RELATION_SHA)
    gi = ensure(paths.GENE_INFO_URL, paths.GENE_INFO, paths.GENE_INFO_SHA)
    return r, rel, gi


def load_tsv(path: Path) -> Iterator[list[str]]:
    """Stream a plain (non-gzipped) Reactome TSV as tab-split field lists (no header to drop)."""
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            yield line.rstrip("\n").split("\t")


def load_entrez_symbol(path: Path = paths.GENE_INFO) -> dict[str, str]:
    """Build the Entrez-id → gene-symbol map from the gzipped NCBI gene_info file.

    Tab-separated; the header line begins with `#`. Columns: tax_id, GeneID (Entrez), Symbol, …
    """
    out: dict[str, str] = {}
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                out[parts[1]] = parts[2]
    return out
