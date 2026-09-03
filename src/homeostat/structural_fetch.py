"""homeostat.structural_fetch -- I/O shell for the structural bank: per-gene CDS from Ensembl REST.

No biology, no decisions (structural.py holds those): for a gene set, resolve each HGNC symbol
to its canonical transcript (lookup/symbol) and fetch that transcript's coding sequence
(sequence/id?type=cds), caching each CDS once under data/structural/cds/<SYMBOL>.fa (gitignored,
user-amortized). I/O-only; `fetch_cds` hits the network. GRCh38, current Ensembl release.
"""

from __future__ import annotations

import json
import urllib.request
from collections.abc import Iterable
from pathlib import Path

from homeostat import paths
from homeostat.util import atomic_write_text

_UA = "homeostat/0.1 (github.com/rohanvinaik/Homeostat)"
_TIMEOUT = 30


def _get(url: str, accept: str) -> str:
    """GET `url` with the given Accept header (Ensembl requires a User-Agent); return the body."""
    req = urllib.request.Request(url, headers={"User-Agent": _UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:  # noqa: S310
        return resp.read().decode("utf-8")


def canonical_transcript(symbol: str) -> str:
    """Resolve an HGNC gene symbol to its Ensembl canonical transcript id (versioned).

    Hits `lookup/symbol/homo_sapiens/<symbol>`; raises if Ensembl returns no canonical transcript
    (a real absence to surface, never silently skipped).
    """
    url = f"{paths.ENSEMBL_REST}/lookup/symbol/homo_sapiens/{symbol}"
    data = json.loads(_get(url, "application/json"))
    tx = data.get("canonical_transcript")
    if not tx:
        raise ValueError(f"no canonical transcript for {symbol!r} (Ensembl lookup returned none)")
    return str(tx)


def _parse_fasta(text: str) -> str:
    """Join the sequence lines of a single-record FASTA (header lines dropped), upper-cased."""
    return "".join(line.strip() for line in text.splitlines() if not line.startswith(">")).upper()


def fetch_cds(symbol: str) -> str:
    """Fetch the coding sequence for `symbol`'s canonical transcript from Ensembl. Network.

    Returns the in-frame nucleotide CDS (starts at ATG); raises on no transcript or empty CDS.
    """
    tx = canonical_transcript(symbol).split(".")[0]  # sequence/id rejects the .NN version suffix
    cds = _parse_fasta(_get(f"{paths.ENSEMBL_REST}/sequence/id/{tx}?type=cds", "text/x-fasta"))
    if not cds:
        raise ValueError(f"empty CDS for {symbol!r} (transcript {tx})")
    return cds


def ensure(genes: Iterable[str], cache_dir: Path = paths.STRUCTURAL_CDS_DIR) -> dict[str, str]:
    """Return `{symbol: CDS}` for the scoped genes, fetching+caching any not already on disk.

    User-amortized: each gene's CDS is written once to `<cache_dir>/<SYMBOL>.fa` and reused after. A
    symbol that fails to resolve raises (a curated gene with no CDS is a bug, not an abstention).
    Order-independent; the returned dict is keyed by symbol.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    out: dict[str, str] = {}
    for symbol in genes:
        path = cache_dir / f"{symbol}.fa"
        if path.exists():
            out[symbol] = path.read_text(encoding="utf-8").strip()
            continue
        cds = fetch_cds(symbol)
        atomic_write_text(path, cds + "\n")
        out[symbol] = cds
    return out
