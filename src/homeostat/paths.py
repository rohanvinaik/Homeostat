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

# Ensembl Compara human homologies (the evolutionary / fungibility renderer's substrate).
# One gzipped TSV (human vs all species; we keep only human WITHIN-species paralogs). Tab-separated,
# header present; both endpoints carry an Ensembl protein id, normalized to symbols via the STRING
# info map (shared). Gitignored, re-downloadable; the sha256 sidecar pins the version built against.
HOMOLOGY_DIR = DATA / "homology"
HOMOLOGY_TSV = HOMOLOGY_DIR / "Compara.112.protein_default.homologies.tsv.gz"
HOMOLOGY_SHA = HOMOLOGY_DIR / "Compara.112.protein_default.homologies.sha256"
HOMOLOGY_URL = (
    "https://ftp.ensembl.org/pub/release-112/tsv/ensembl-compara/homologies/homo_sapiens/"
    "Compara.112.protein_default.homologies.tsv.gz"
)

# Reactome metabolic pathways + NCBI gene_info (the metabolic-flux renderer's substrate).
# Metabolic-flux = co-membership in a Reactome pathway under the Metabolism subtree (R-HSA-1430728);
# scoping to that subtree is load-bearing (unscoped co-membership just re-states regulatory).
# Three files: NCBI2Reactome (Entrez→pathway), the pathway hierarchy, gene_info (Entrez→symbol).
METABOLIC_DIR = DATA / "metabolic"
NCBI2REACTOME = METABOLIC_DIR / "NCBI2Reactome.txt"
REACTOME_RELATION = METABOLIC_DIR / "ReactomePathwaysRelation.txt"
GENE_INFO = METABOLIC_DIR / "Homo_sapiens.gene_info.gz"
NCBI2REACTOME_SHA = METABOLIC_DIR / "NCBI2Reactome.sha256"
REACTOME_RELATION_SHA = METABOLIC_DIR / "ReactomePathwaysRelation.sha256"
GENE_INFO_SHA = METABOLIC_DIR / "Homo_sapiens.gene_info.sha256"
NCBI2REACTOME_URL = "https://reactome.org/download/current/NCBI2Reactome.txt"
REACTOME_RELATION_URL = "https://reactome.org/download/current/ReactomePathwaysRelation.txt"
GENE_INFO_URL = "https://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz"
