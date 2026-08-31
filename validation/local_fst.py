"""Local population differentiation (Fst) for arbitrary genes — no Ensembl, no network.

The A1 panel / E1 transfer / C1 cross-population all need per-gene population differentiation for
genes outside the LRRK2 cloud. Rather than extend the fragile Ensembl cache, compute it locally from
the 1000G phase-3 sites VCF (genome-wide per-superpop AF, by position) which is already in data/.

  gene -> region        via refGene (local)
  variants in region    by POSITION from the sites VCF (its ID column is '.', so position, not rsID)
  per-superpop AF       from the INFO EAS_AF/EUR_AF/SAS_AF/AFR_AF/AMR_AF fields
  gene differentiation  = max over its variants of max-pairwise Hudson Fst (homeostat.pbs, reused)

One streaming pass over the VCF covers every requested gene at once; the result is cached. This is
the same quantity load_gene_diff computes, sourced locally instead of from a per-cloud Ensembl pull.

    from local_fst import gene_maxfst
    fst = gene_maxfst({"NOD2", "RIPK2", ...})   # {gene: max_fst}; abstains (absent) if no variant
"""

from __future__ import annotations

import bisect
import subprocess
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from homeostat.pbs import HAP_N, hudson_fst  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
REFGENE = REPO / "data" / "network" / "refGene_hg19.txt.gz"
SITES_VCF = REPO / "data" / "reference" / "ALL.wgs.phase3_v5c.sites.vcf.gz"
POPS = ["EUR", "SAS", "EAS", "AFR", "AMR"]


def gene_regions(genes: set[str]) -> dict[str, list[tuple]]:
    """chrom(bare) -> sorted [(start, end, gene)] for the requested genes, from refGene (txStart..txEnd)."""
    spans: dict[str, tuple[str, int, int]] = {}
    proc = subprocess.Popen(["gzip", "-dc", str(REFGENE)], stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:  # type: ignore[union-attr]
        f = line.split("\t")
        if len(f) < 13:
            continue
        gene = f[12]
        if gene not in genes:
            continue
        chrom = f[2][3:] if f[2].startswith("chr") else f[2]  # 'chr1' -> '1'
        if "_" in chrom:  # skip haplotype/unplaced contigs
            continue
        start, end = int(f[4]), int(f[5])
        if gene in spans:  # widen to the union across transcripts
            c, s, e = spans[gene]
            if c == chrom:
                spans[gene] = (c, min(s, start), max(e, end))
        else:
            spans[gene] = (chrom, start, end)
    proc.wait()
    by_chrom: dict[str, list[tuple]] = {}
    for gene, (chrom, s, e) in spans.items():
        by_chrom.setdefault(chrom, []).append((s, e, gene))
    for chrom in by_chrom:
        by_chrom[chrom].sort()
    return by_chrom


def _af(info: str, key: str) -> float | None:
    """First ALT allele frequency for INFO key (multiallelic -> take the first)."""
    for field in info.split(";"):
        if field.startswith(key + "="):
            try:
                return float(field[len(key) + 1 :].split(",")[0])
            except ValueError:
                return None
    return None


def _variant_maxfst(freqs: dict[str, float]) -> float:
    return max(hudson_fst(freqs[a], HAP_N[a], freqs[b], HAP_N[b]) for a, b in combinations(POPS, 2))


def gene_maxfst(genes: set[str], cache: Path = Path("/tmp/panel_fst.tsv")) -> dict[str, float]:
    """gene -> max differentiation over its variants (one VCF pass); cached. Absent = abstain (no data)."""
    if cache.exists():
        cached: dict[str, float | None] = {}
        for line in cache.open():
            g, v = line.rstrip("\n").split("\t")
            cached[g] = None if v == "NA" else float(v)
        if genes <= set(cached):  # cache covers the request (incl. abstentions recorded as NA)
            return {g: c for g in genes if (c := cached[g]) is not None}

    by_chrom = gene_regions(genes)
    starts = {c: [iv[0] for iv in ivs] for c, ivs in by_chrom.items()}
    gene_fst: dict[str, float] = {}
    proc = subprocess.Popen(["gzip", "-dc", str(SITES_VCF)], stdout=subprocess.PIPE, text=True)
    seen = 0
    for line in proc.stdout:  # type: ignore[union-attr]
        if line.startswith("#"):
            continue
        seen += 1
        if seen % 10_000_000 == 0:
            print(f"  … {seen // 1_000_000}M variants scanned", file=sys.stderr)
        tab1 = line.find("\t")
        chrom = line[:tab1]
        ivs = by_chrom.get(chrom)
        if ivs is None:
            continue
        tab2 = line.find("\t", tab1 + 1)
        pos = int(line[tab1 + 1 : tab2])
        i = bisect.bisect_right(starts[chrom], pos) - 1
        hit = None
        for j in (i, i - 1):  # the interval whose start<=pos, and one before (nesting)
            if 0 <= j < len(ivs) and ivs[j][0] <= pos <= ivs[j][1]:
                hit = ivs[j][2]
                break
        if hit is None:
            continue
        info = line.rsplit("\t", 1)[-1]
        freqs = {p: _af(info, p + "_AF") for p in POPS}
        if any(v is None for v in freqs.values()):
            continue
        fst = _variant_maxfst(freqs)  # type: ignore[arg-type]
        if fst > gene_fst.get(hit, -1.0):
            gene_fst[hit] = fst
    proc.wait()
    with cache.open("w") as fh:  # record every requested gene, NA for abstentions
        for g in sorted(genes):
            fh.write(f"{g}\t{gene_fst[g]:.6f}\n" if g in gene_fst else f"{g}\tNA\n")
    return gene_fst


if __name__ == "__main__":
    req = set(sys.argv[1:])
    out = gene_maxfst(req) if req else {}
    for g in sorted(out):
        print(f"{g}\t{out[g]:.4f}")
    print(f"{len(out)}/{len(req)} genes with 1000G data", file=sys.stderr)
