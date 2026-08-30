"""Intent tests for the literature-count loader and study-bias tertile matching."""

import gzip

from homeostat.annotation_recovery_studybias import eligible_3way, tertiles
from homeostat.litcount import load_pubmed_counts, load_symbol_map


def _write_gz(path, text):
    with gzip.open(path, "wt", encoding="utf-8") as f:
        f.write(text)


def test_pubmed_counts_distinct_human_only(tmp_path):
    gene_info = tmp_path / "gene_info.gz"
    _write_gz(
        gene_info,
        "#tax_id\tGeneID\tSymbol\n9606\t100\tGENEA\n9606\t200\tGENEB\n",
    )
    g2p = tmp_path / "gene2pubmed.gz"
    _write_gz(
        g2p,
        "#tax_id\tGeneID\tPubMed_ID\n"
        "9606\t100\t1\n"
        "9606\t100\t2\n"
        "9606\t100\t1\n"  # duplicate PMID -> not double counted
        "10090\t100\t9\n"  # mouse row -> excluded
        "9606\t200\t5\n",
    )
    counts = load_pubmed_counts(g2p, gene_info)
    assert counts["GENEA"] == 2  # PMIDs 1,2 distinct; mouse row ignored
    assert counts["GENEB"] == 1


def test_symbol_map_reads_geneid_symbol(tmp_path):
    gene_info = tmp_path / "gi.gz"
    _write_gz(gene_info, "#tax_id\tGeneID\tSymbol\n9606\t7\tTP53\n")
    assert load_symbol_map(gene_info) == {"7": "TP53"}


def test_tertiles_cut_points():
    # 9 values 0..8 -> n//3=3 -> s[3]=3 ; 2n//3=6 -> s[6]=6
    assert tertiles(list(range(9))) == (3, 6)


def test_3way_requires_same_tertile():
    # gene -> (degree, participation, pbs, p)
    scores = {
        "C": (100, 0.5, 0.05, 0.01),
        "G_same": (110, 0.1, 0.06, 0.5),
        "G_offtert": (105, 0.1, 0.05, 0.5),
    }
    tertile = {"C": 2, "G_same": 2, "G_offtert": 0}
    elig = eligible_3way(["C"], ["G_same", "G_offtert"], scores, tertile)
    assert elig["C"] == ["G_same"]  # G_offtert excluded by tertile despite deg+pbs match
