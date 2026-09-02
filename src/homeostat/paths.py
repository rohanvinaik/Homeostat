"""Canonical repo-relative paths. Everything under data/ is gitignored."""

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"

# Optional output namespace: HOMEOSTAT_TAG=_gnomad writes side-by-side variants of
# the pile + gate outputs (e.g. eir_pbs_pile_gnomad.tsv.gz) without clobbering the
# default (Pan-UKBB) results. Empty tag -> original filenames (backward compatible).
TAG = os.environ.get("HOMEOSTAT_TAG", "")


def tagged(name: str) -> Path:
    """EIR / name, with TAG inserted before the extension when set.

    'eir_pbs_pile.tsv.gz' -> 'eir_pbs_pile_gnomad.tsv.gz' when TAG='_gnomad'.
    """
    if not TAG:
        return EIR / name
    base, _dot, ext = name.partition(".")
    return EIR / f"{base}{TAG}.{ext}"


# Index genotype R (directly-observed tier — the raw array export, copied local).
# The personal source path is NEVER committed — set it locally via the env var.
GENOTYPE_DIR = DATA / "genotype"
GENOTYPE_RAW = GENOTYPE_DIR / "genome_R_v5_full_build37.txt"
GENOTYPE_SOURCE = Path(os.environ.get("HOMEOSTAT_GENOTYPE_SOURCE", ""))

# 1000 Genomes phase 3 (GRCh37) sites-only VCF with per-superpop AFs
REFERENCE_DIR = DATA / "reference"
SITES_VCF = REFERENCE_DIR / "ALL.wgs.phase3_v5c.sites.vcf.gz"
SITES_VCF_PART = REFERENCE_DIR / "ALL.wgs.phase3_v5c.sites.vcf.gz.part"
SITES_VCF_EXPECTED = REFERENCE_DIR / "sites_vcf.expected_bytes"
SITES_VCF_URL = (
    "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/"
    "ALL.wgs.phase3_shapeit2_mvncall_integrated_v5c.20130502.sites.vcf.gz"
)

# SIGNOR human curated directed-signaling dump (the regulatory renderer's substrate).
# One TSV (getData.php serves tab-separated despite format=csv), no header, 29 columns.
# Re-downloadable; the sha256 sidecar pins the version built against (SIGNOR updates → drift).
SIGNOR_DIR = DATA / "signor"
SIGNOR_TSV = SIGNOR_DIR / "signor_human_9606.tsv"
SIGNOR_SHA = SIGNOR_DIR / "signor_human_9606.sha256"
SIGNOR_URL = "https://signor.uniroma2.it/getData.php?organism=9606&format=csv"

# E/I/R outputs
EIR = DATA / "e_i_r"
SHARDS = EIR / "shards"
SCAN_PROGRESS = EIR / "scan_progress.json"
CANDIDATES = EIR / "candidates.tsv.gz"
SUMMARY = EIR / "summary.json"

AUTOSOMES = [str(c) for c in range(1, 23)]
