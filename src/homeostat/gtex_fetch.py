"""homeostat.gtex_fetch — I/O shell for the GTEx v8 per-sample TPM matrix + sample→tissue map.

No biology, no decisions (`coexpression.py` holds the pure readout): fetch the two files once (the
~1.63 GB gene×sample matrix + the sample annotations), cache them gitignored under `data/gtex/`,
sha256-pin each, and expose two loaders — the SAMPID→tissue map and a SCOPED expression read (stream
the matrix once, keep only the requested genes' vectors). I/O-only, Detective-inexpressible;
intent-tested with synthetic fixtures. `fetch` hits the network.
"""

from __future__ import annotations

import gzip
import urllib.request
from collections.abc import Iterable
from pathlib import Path

from homeostat import paths
from homeostat.util import atomic_write_text, sha256

_UA = "curl/8.4"
_CHUNK = 1 << 20


def fetch(url: str, dest: Path, timeout: int = 300) -> Path:
    """Download `url` to `dest`, atomically via a `.part` sibling; User-Agent set. `timeout` is the
    socket read timeout (generous for the multi-GB matrix, which streams steadily)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(part, "wb") as out:  # noqa: S310
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
    """Ensure both GTEx files are cached (the TPM matrix + the sample attributes). Returns
    (tpm_matrix, sample_attributes)."""
    tpm = ensure(paths.GTEX_TPM_URL, paths.GTEX_TPM, paths.GTEX_TPM_SHA)
    attrs = ensure(paths.GTEX_ATTRS_URL, paths.GTEX_ATTRS, paths.GTEX_ATTRS_SHA)
    return tpm, attrs


def load_sample_tissue(path: Path = paths.GTEX_ATTRS) -> dict[str, str]:
    """Map each SAMPID to its detailed tissue (SMTSD) from the tab-separated attributes file. The
    two columns are found by header NAME (robust to order); the per-sample label the render groups
    by. Header dropped."""
    with open(path, encoding="utf-8") as fh:
        header = next(fh).rstrip("\n").split("\t")
        sid, tissue = header.index("SAMPID"), header.index("SMTSD")
        out: dict[str, str] = {}
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) > max(sid, tissue):
                out[parts[sid]] = parts[tissue]
    return out


def load_expression(
    symbols: Iterable[str], path: Path = paths.GTEX_TPM
) -> tuple[list[str], dict[str, list[float]]]:
    """Stream the gzipped `.gct` ONCE, keeping only the requested genes' per-sample TPM vectors.

    Returns `(sample_ids, {symbol: tpm_vector})` — `sample_ids` in column order (the header row,
    fields[2:]), each aligned to it. The preamble (``#1.2`` + dims line) is skipped; each gene row
    is `Name Description <tpm...>` and `Description` is the gene symbol.
    """
    wanted = set(symbols)
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        next(fh)  # #1.2
        next(fh)  # <nrows> <ncols>
        sample_ids = fh.readline().rstrip("\n").split("\t")[2:]
        expr: dict[str, list[float]] = {}
        for line in fh:
            fields = line.rstrip("\n").split("\t")
            if len(fields) > 2 and fields[1] in wanted:
                expr[fields[1]] = [float(v) for v in fields[2:]]
    return sample_ids, expr
