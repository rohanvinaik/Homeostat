"""GTEx co-expression grounding channel — the second, PPI-independent structure.

Each gene -> its cross-tissue median-TPM vector (log1p); a co-expression edge
exists between two genes iff their Pearson correlation over the 54 GTEx tissues
is >= tau. Independent of STRING physical topology by construction (expression
covariation, not binding).
"""

import gzip
import statistics
from math import sqrt

from homeostat import paths

GTEX = paths.DATA / "network" / "gtex_median_tpm.gct.gz"
DEFAULT_TAU = 0.7


def load_expression(genes: set[str]) -> dict[str, list[float]]:
    """symbol -> log1p cross-tissue median-TPM vector, for genes in `genes`.

    The GCT has 2 header lines then columns: Name, Description(symbol), <tissues>.
    A symbol with multiple rows keeps the highest-mean row (deterministic).
    """
    best: dict[str, tuple[float, list[float]]] = {}
    with gzip.open(GTEX, "rt", encoding="utf-8") as f:
        f.readline()  # version line
        f.readline()  # dims line
        header = f.readline().rstrip("\n").split("\t")
        n_tissue = len(header) - 2
        for line in f:
            fld = line.rstrip("\n").split("\t")
            if len(fld) != 2 + n_tissue:
                continue
            sym = fld[1]
            if sym not in genes:
                continue
            vec = [log1p_safe(v) for v in fld[2:]]
            mean = statistics.fmean(vec)
            if sym not in best or mean > best[sym][0]:
                best[sym] = (mean, vec)
    return {sym: vec for sym, (_m, vec) in best.items()}


def log1p_safe(s: str) -> float:
    try:
        x = float(s)
    except ValueError:
        return 0.0
    return sqrt(max(x, 0.0) + 1.0) - 1.0  # variance-stabilising, monotone in x


def _pearson(a: list[float], b: list[float]) -> float:
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((x - mb) ** 2 for x in b)
    if va == 0 or vb == 0:
        return 0.0
    cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    return cov / sqrt(va * vb)


def coexpression_edges(
    expr: dict[str, list[float]], tau: float = DEFAULT_TAU
) -> dict[str, set[str]]:
    """Symmetric adjacency of gene pairs with cross-tissue correlation >= tau."""
    genes = sorted(expr)
    adj: dict[str, set[str]] = {g: set() for g in genes}
    for i, gi in enumerate(genes):
        for gj in genes[i + 1 :]:
            if _pearson(expr[gi], expr[gj]) >= tau:
                adj[gi].add(gj)
                adj[gj].add(gi)
    return adj
