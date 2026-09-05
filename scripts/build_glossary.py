"""Build the diagnosis→gene GLOSSARY from the Jensen-lab DISEASES database -- a run-once script over
the WHOLE disease set, so the reference is sourced and auditable, not hand-written.

DISEASES has three channels, and the glossary keeps them TIERED so provenance stays visible:
  - `curated`   : `knowledge` (manually curated DBs) + `experiments` (GWAS/TIGA) -- high confidence.
  - `textmined` : literature co-mention above a confidence floor -- BROADER, captures the conditions
                  common-variant GWAS under-serves (e.g. POTS), but co-mention is COMORBIDITY, not
                  proven causation (POTS's textmined genes are mostly comorbid EDS/MCAS genes).

`genes` = curated ∪ textmined -- a RELEVANCE reference; κ inside does the significance.
Nothing here asserts a cross-diagnosis mechanism; the pipeline computes that.

Source: https://download.jensenlab.org/human_disease_{knowledge,textmining,experiments}_filtered.tsv
Cached under data/diseases/ (gitignored dumps). Writes data/glossary/diagnosis_genes.json.
"""

from __future__ import annotations

import json
import urllib.request
from collections import defaultdict
from pathlib import Path

from homeostat import paths
from homeostat.util import atomic_write_text, sha256

DIS = Path(paths.DATA) / "diseases"
OUT = Path(paths.DATA) / "glossary" / "diagnosis_genes.json"
DISEASES_BASE_URL = "https://download.jensenlab.org"
CHANNELS = ("knowledge", "experiments", "textmining")
_CHUNK = 1024 * 1024
_UA = "Homeostat/0.1 (+https://github.com/rohanvinaik/Homeostat)"
TM_MIN = (
    1.5  # text-mining confidence floor: low enough to cover under-studied conditions (POTS ~1.5)
)
GENE, DISEASE = 1, 3  # column indices (gene_name, disease_name) -- shared across all three channels
TM_CONF = 5  # text-mining confidence column


def ensure_source(channel: str, directory: Path = DIS, base_url: str = DISEASES_BASE_URL) -> Path:
    """Return a cached DISEASES channel, downloading it atomically when absent."""
    if channel not in CHANNELS:
        raise ValueError(f"unknown DISEASES channel: {channel}")
    dest = directory / f"human_disease_{channel}_filtered.tsv"
    receipt = dest.with_suffix(".sha256")
    if dest.exists():
        if not receipt.exists():
            atomic_write_text(receipt, sha256(dest) + "\n")
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    url = f"{base_url.rstrip('/')}/{dest.name}"
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as response, part.open("wb") as output:
            while chunk := response.read(_CHUNK):
                output.write(chunk)
        part.replace(dest)
    except Exception:
        part.unlink(missing_ok=True)
        raise
    atomic_write_text(receipt, sha256(dest) + "\n")
    return dest


def ensure_sources() -> None:
    """Cache every source required to build the glossary."""
    for channel in CHANNELS:
        ensure_source(channel)


def _rows(channel: str):
    path = DIS / f"human_disease_{channel}_filtered.tsv"
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            cols = line.rstrip("\n").split("\t")
            if len(cols) > DISEASE and cols[GENE] and cols[DISEASE]:
                yield cols


def build() -> dict:
    curated: dict[str, set[str]] = defaultdict(set)
    textmined: dict[str, set[str]] = defaultdict(set)
    for channel in ("knowledge", "experiments"):
        for r in _rows(channel):
            curated[r[DISEASE]].add(r[GENE])
    for r in _rows("textmining"):
        try:
            conf = float(r[TM_CONF])
        except (ValueError, IndexError):
            continue
        if conf >= TM_MIN:
            textmined[r[DISEASE]].add(r[GENE])

    glossary: dict[str, dict] = {}
    for disease in sorted(set(curated) | set(textmined)):
        cur = sorted(curated.get(disease, set()))
        tm = sorted(textmined.get(disease, set()) - curated.get(disease, set()))
        glossary[disease] = {
            "genes": sorted(set(cur) | set(tm)),
            "curated": cur,  # textmined = genes - curated (derivable; not stored twice)
        }
    return glossary


def main() -> None:
    ensure_sources()
    glossary = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(glossary, sort_keys=True) + "\n")
    size_mb = OUT.stat().st_size / 1e6
    n_cur = sum(1 for e in glossary.values() if e["curated"])
    print(f"wrote {OUT}  ({len(glossary)} diseases, {n_cur} with curated genes, {size_mb:.1f} MB)")
    for dx in ("Crohn's disease", "Type 2 diabetes mellitus", "Parkinson's disease"):  # public
        e = glossary.get(dx, {"genes": [], "curated": []})
        tm = len(e["genes"]) - len(e["curated"])
        print(f"  {dx[:40]:42} {len(e['genes']):>4} genes ({len(e['curated'])} cur + {tm} tm)")


if __name__ == "__main__":
    main()
