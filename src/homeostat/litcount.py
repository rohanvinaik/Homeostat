"""Per-gene literature intensity (study bias) from NCBI gene2pubmed.

An INDEPENDENT study-intensity measure for the §3.2 study-bias control: does the
candidate-bridge pleiotropy enrichment survive matching on how well-studied each
gene is? gene2pubmed (GeneID → PubMed) counted distinct PMIDs per human gene,
mapped to HGNC symbol via gene_info. Free NCBI bulk files, no auth.
"""

import gzip

from homeostat import paths

GENE2PUBMED = paths.DATA / "network" / "gene2pubmed.gz"
GENE_INFO = paths.DATA / "network" / "Homo_sapiens.gene_info.gz"
HUMAN_TAXID = "9606"


def load_symbol_map(gene_info=GENE_INFO) -> dict[str, str]:
    """GeneID -> HGNC Symbol (human)."""
    out: dict[str, str] = {}
    with gzip.open(gene_info, "rt", encoding="utf-8") as f:
        header = f.readline().lstrip("#").rstrip("\n").split("\t")
        gi = header.index("GeneID")
        si = header.index("Symbol")
        for line in f:
            fld = line.rstrip("\n").split("\t")
            if len(fld) > max(gi, si):
                out[fld[gi]] = fld[si]
    return out


def load_pubmed_counts(gene2pubmed=GENE2PUBMED, gene_info=GENE_INFO) -> dict[str, int]:
    """Symbol -> number of DISTINCT PubMed IDs (human rows only).

    A gene absent from gene2pubmed -> not in the returned dict (caller treats as 0);
    that is a genuine 'never co-cited' signal, and study bias is exactly what this
    controls for.
    """
    symbol = load_symbol_map(gene_info)
    pmids: dict[str, set[str]] = {}
    with gzip.open(gene2pubmed, "rt", encoding="utf-8") as f:
        f.readline()  # header: #tax_id GeneID PubMed_ID
        for line in f:
            tax, gene_id, pmid = line.rstrip("\n").split("\t")
            if tax != HUMAN_TAXID:
                continue
            sym = symbol.get(gene_id)
            if sym is not None:
                pmids.setdefault(sym, set()).add(pmid)
    return {s: len(p) for s, p in pmids.items()}
