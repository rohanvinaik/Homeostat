"""The §13.1 pipeline: one idempotent command that finishes whatever remains.

    make run          (or: PYTHONPATH=src python3 -m homeostat.pipeline)

Stages, each derived from filesystem artifacts, each safe to re-run:
  1. genotype   — copy the raw array export local, record sha256
  2. reference  — resume-download the 1000G sites VCF until size-complete
  3. scan       — stream-join against R's sites (chromosome-resumable)
  4. rank       — PBS + priority queue -> candidates.tsv.gz + summary.json
"""

import gzip
import hashlib
import shutil
import subprocess
import sys
import zlib

from homeostat import genotype, rank, scan
from homeostat.paths import (
    AUTOSOMES,
    CANDIDATES,
    GENOTYPE_DIR,
    GENOTYPE_RAW,
    GENOTYPE_SOURCE,
    SITES_VCF,
    SITES_VCF_EXPECTED,
    SITES_VCF_PART,
    SITES_VCF_URL,
    SUMMARY,
)


def _sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_genotype() -> None:
    if GENOTYPE_RAW.exists():
        return
    if not GENOTYPE_SOURCE.exists():
        sys.exit(f"index genotype export not found at {GENOTYPE_SOURCE}")
    GENOTYPE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = GENOTYPE_RAW.with_suffix(".tmp")
    shutil.copyfile(GENOTYPE_SOURCE, tmp)
    tmp.replace(GENOTYPE_RAW)
    print(f"[genotype] copied raw export -> {GENOTYPE_RAW}")


def _gzip_stream_ok(path) -> bool:
    """Full decompression pass. Size match is NOT integrity: a resumed transfer
    once delivered a size-exact file with corrupt bytes mid-stream (2026-08-28)."""
    try:
        with gzip.open(path, "rb") as g:
            while g.read(1 << 22):
                pass
        return True
    except (OSError, EOFError, zlib.error):
        return False


def ensure_reference() -> None:
    expected = int(SITES_VCF_EXPECTED.read_text().strip()) if SITES_VCF_EXPECTED.exists() else None
    if SITES_VCF.exists():
        if expected is not None and SITES_VCF.stat().st_size != expected:
            sys.exit(f"[reference] {SITES_VCF} size != expected {expected}; delete and re-run")
        return
    print("[reference] resuming download (curl -C -) ...")
    subprocess.run(
        ["curl", "-s", "-C", "-", "--retry", "10", "-o", str(SITES_VCF_PART), SITES_VCF_URL],
        check=True,
    )
    if expected is not None and SITES_VCF_PART.stat().st_size != expected:
        sys.exit("[reference] download incomplete after curl; re-run to resume")
    print("[reference] verifying gzip stream integrity (full decompression pass) ...")
    if not _gzip_stream_ok(SITES_VCF_PART):
        sys.exit(
            "[reference] downloaded file is size-complete but the gzip stream is "
            "CORRUPT; splice-repair by ranged re-fetch or delete the .part and re-run"
        )
    SITES_VCF_PART.replace(SITES_VCF)
    print(f"[reference] complete and verified -> {SITES_VCF}")


def main() -> None:
    ensure_genotype()
    ensure_reference()

    r_index, counts = genotype.parse_export(GENOTYPE_RAW)
    print(f"[genotype] parsed: {counts}")

    if len(scan.done_chroms()) < len(AUTOSOMES):
        print(f"[scan] resuming; done so far: {scan.done_chroms() or 'none'}")
        scan.scan(r_index)
        print(f"[scan] complete: {scan.done_chroms()}")
    else:
        print("[scan] already complete")

    if CANDIDATES.exists() and SUMMARY.exists():
        print("[rank] already complete (delete summary.json to re-rank)")
    else:
        summary = rank.rank(counts, _sha256(GENOTYPE_RAW))
        print(
            f"[rank] {summary['candidates_total']} candidates, "
            f"{summary['candidates_priority_gt0']} with priority > 0 -> {CANDIDATES}"
        )


if __name__ == "__main__":
    main()
