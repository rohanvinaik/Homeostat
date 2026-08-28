"""Canonical repo-relative paths. Everything under data/ is gitignored."""

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"

# Index genotype R (directly-observed tier — the raw array export, copied local)
GENOTYPE_DIR = DATA / "genotype"
GENOTYPE_RAW = GENOTYPE_DIR / "genome_R_v5_full_build37.txt"
GENOTYPE_SOURCE = Path(
    "/Users/rohanvinaik/Desktop/Desktop/Genetics/genome_Rohan_Vinaik_v5_Full_20220112035411.txt"
)

# 1000 Genomes phase 3 (GRCh37) sites-only VCF with per-superpop AFs
REFERENCE_DIR = DATA / "reference"
SITES_VCF = REFERENCE_DIR / "ALL.wgs.phase3_v5c.sites.vcf.gz"
SITES_VCF_PART = REFERENCE_DIR / "ALL.wgs.phase3_v5c.sites.vcf.gz.part"
SITES_VCF_EXPECTED = REFERENCE_DIR / "sites_vcf.expected_bytes"
SITES_VCF_URL = (
    "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/"
    "ALL.wgs.phase3_shapeit2_mvncall_integrated_v5c.20130502.sites.vcf.gz"
)

# E/I/R outputs
EIR = DATA / "e_i_r"
SHARDS = EIR / "shards"
SCAN_PROGRESS = EIR / "scan_progress.json"
CANDIDATES = EIR / "candidates.tsv.gz"
SUMMARY = EIR / "summary.json"

AUTOSOMES = [str(c) for c in range(1, 23)]
