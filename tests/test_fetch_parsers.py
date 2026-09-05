"""Synthetic-fixture tests for the fetch shells' PURE PARSERS — the half of each I/O shell that is
NOT the network. Each parser is fed a tiny hand-built file (a real gzip / zip / TSV in a tmpdir) and
its output asserted. This is real coverage AND a regression guard on the file grammars; the raw
download primitives are the deliberate no-mock boundary (excluded in pyproject's coverage report
config). Authored from the shells' documented formats, not generated."""

from __future__ import annotations

import gzip
import zipfile
from pathlib import Path

from homeostat import gtex_fetch, structural_fetch, trait_wiring_fetch


def _write_gz(path: Path, text: str) -> Path:
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        fh.write(text)
    return path


# ---- trait_wiring_fetch.load_rows (GWAS associations zip) ------------------------


def test_trait_wiring_load_rows_streams_the_tsv_inside_the_zip(tmp_path):
    # the loader finds the .tsv member dynamically (its name carries the release date) and drops
    # the header, yielding tab-split rows.
    z = tmp_path / "gwas.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("gwas-catalog-2026-01-01.tsv", "HDR_A\tHDR_B\nTP53\tcancer\nDRD2\tADHD\n")
    rows = list(trait_wiring_fetch.load_rows(z))
    assert rows == [["TP53", "cancer"], ["DRD2", "ADHD"]]  # header dropped, tab-split


# ---- gtex_fetch parsers ----------------------------------------------------------


def test_gtex_load_sample_tissue_maps_sampid_to_tissue_by_header_name(tmp_path):
    # columns located by NAME (robust to order): SAMPID -> SMTSD.
    p = tmp_path / "attrs.txt"
    p.write_text("OTHER\tSMTSD\tSAMPID\nx\tLiver\tS1\ny\tBrain - Cortex\tS2\n", encoding="utf-8")
    assert gtex_fetch.load_sample_tissue(p) == {"S1": "Liver", "S2": "Brain - Cortex"}


def test_gtex_load_expression_keeps_only_wanted_genes_aligned_to_samples(tmp_path):
    # gct: two preamble lines, then `Name Description <samples...>`, then one row per gene.
    gct = (
        "#1.2\n2\t2\nName\tDescription\tGTEX-1\tGTEX-2\n"
        "ENSG1\tGENEA\t1.0\t2.0\nENSG2\tGENEB\t3.0\t4.0\n"
    )
    p = _write_gz(tmp_path / "tpm.gct.gz", gct)
    sample_ids, expr = gtex_fetch.load_expression(["GENEA"], p)
    assert sample_ids == ["GTEX-1", "GTEX-2"]
    assert expr == {"GENEA": [1.0, 2.0]}  # GENEB not requested -> absent


# ---- structural_fetch parsers ----------------------------------------------------


def test_structural_parse_fasta_joins_sequence_lines_upper():
    assert structural_fetch._parse_fasta(">header line\natgc\naaTt\n") == "ATGCAATT"


def test_structural_load_proteins_bulk_keeps_longest_cds_per_gene_and_translates(tmp_path):
    # two transcripts for GENEA (keep the LONGER); one for GENEB. gene_symbol: in the header.
    fasta = (
        ">ENST1 gene_symbol:GENEA\nATGAAATAA\n"  # M K stop  -> short
        ">ENST2 gene_symbol:GENEA\nATGAAAAAATAA\n"  # M K K stop -> longer, wins
        ">ENST3 gene_symbol:GENEB\nATGTTTTGA\n"  # M F stop
    )
    p = _write_gz(tmp_path / "cds_all.fa.gz", fasta)
    out = structural_fetch.load_proteins_bulk(["GENEA", "GENEB"], p)
    assert set(out) == {"GENEA", "GENEB"}
    assert out["GENEA"].startswith("M") and len(out["GENEA"]) >= 3  # longest CDS translated
    assert out["GENEB"].startswith("M")


def test_structural_load_proteins_bulk_filters_to_requested_genes(tmp_path):
    fasta = ">ENST1 gene_symbol:GENEA\nATGAAATAA\n>ENST2 gene_symbol:OTHER\nATGTTTTGA\n"
    p = _write_gz(tmp_path / "cds.fa.gz", fasta)
    out = structural_fetch.load_proteins_bulk(["GENEA"], p)
    assert set(out) == {"GENEA"}  # OTHER filtered out
