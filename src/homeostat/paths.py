"""Canonical repo-relative paths. Everything under data/ is gitignored."""

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"

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

# STRING physical-interaction subnetwork (the physical-binding undirected-vote substrate).
# `links` = the detailed physical links (space-separated, gzipped, header:
# `protein1 protein2 experimental database textmining combined_score`; keys on Ensembl protein ids).
# `info` = the ENSP → preferred_name (gene symbol) map — the first harmonizing-normalization input.
# Both gitignored, re-downloadable; sha256 sidecars pin the version built against.
STRING_DIR = DATA / "string"
STRING_LINKS = STRING_DIR / "9606.protein.physical.links.detailed.v12.0.txt.gz"
STRING_INFO = STRING_DIR / "9606.protein.info.v12.0.txt.gz"
STRING_LINKS_SHA = STRING_DIR / "9606.protein.physical.links.detailed.v12.0.sha256"
STRING_INFO_SHA = STRING_DIR / "9606.protein.info.v12.0.sha256"
STRING_LINKS_URL = (
    "https://stringdb-downloads.org/download/protein.physical.links.detailed.v12.0/"
    "9606.protein.physical.links.detailed.v12.0.txt.gz"
)
STRING_INFO_URL = (
    "https://stringdb-downloads.org/download/protein.info.v12.0/9606.protein.info.v12.0.txt.gz"
)
