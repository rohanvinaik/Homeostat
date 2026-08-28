"""§13.3 — blind bridge recovery + the preregistered LRRK2 control.

Derivation side (annotation-blind): E/I/R loci -> positional gene envelopes
(refGene, positions only) -> gene scores -> STRING *physical* subgraph ->
connected components + connector genes that join otherwise-disjoint components
(the §5.7 bridge shape). Gene symbols are opaque identifiers here.

Evaluation side: `evaluate_preregistered()` — the ONLY place the control's
gene names appear (docs/runs/2026-08-28-lrrk2-control-PREREGISTRATION.md,
committed before this file existed). §5.9: the confirmation channel must not
feed the derivation.

Run: make bridge. Idempotent: skips if the output exists.
"""

import datetime
import gzip
import json
import sys
from bisect import bisect_right
from collections import deque

from homeostat import paths
from homeostat.util import atomic_write_json

# Dials — fixed by the preregistration; do not tune after.
FLANK_BP = 25_000
MIN_STRING_SCORE = 400
TOP_CONNECTORS = 20

NETWORK = paths.DATA / "network"
LINKS = NETWORK / "string_physical_links.txt.gz"
INFO = NETWORK / "string_protein_info.txt.gz"
REFGENE = NETWORK / "refGene_hg19.txt.gz"
BRIDGE_OUT = paths.EIR / "bridge_control.json"


# -- derivation ------------------------------------------------------------
def load_gene_envelopes() -> dict[str, tuple[str, int, int]]:
    """symbol -> (chrom, min_start, max_end) from refGene; positions only.

    Symbols mapping to multiple chromosomes keep the chrom with the most
    transcripts (ties: lexicographic) — counted, not silent.
    """
    per: dict[tuple[str, str], list[tuple[int, int]]] = {}
    with gzip.open(REFGENE, "rt", encoding="utf-8") as f:
        for line in f:
            fld = line.rstrip("\n").split("\t")
            chrom, tx_start, tx_end, symbol = fld[2], int(fld[4]), int(fld[5]), fld[12]
            if not chrom.startswith("chr") or "_" in chrom:
                continue
            c = chrom.removeprefix("chr")
            if c not in {str(i) for i in range(1, 23)}:
                continue
            per.setdefault((symbol, c), []).append((tx_start, tx_end))
    best: dict[str, tuple[str, int, int, int]] = {}
    for (symbol, c), spans in per.items():
        n = len(spans)
        cur = best.get(symbol)
        if cur is None or n > cur[3] or (n == cur[3] and c < cur[0]):
            best[symbol] = (c, min(s for s, _ in spans), max(e for _, e in spans), n)
    return {sym: (c, s, e) for sym, (c, s, e, _n) in best.items()}


def map_loci_to_genes(
    loci: list[tuple[str, int, float]],
    envelopes: dict[str, tuple[str, int, int]],
    flank: int = FLANK_BP,
) -> dict[str, float]:
    """Gene score = max lead-locus priority over loci within envelope +/- flank."""
    by_chrom: dict[str, list[tuple[int, int, str]]] = {}
    for sym, (c, s, e) in envelopes.items():
        by_chrom.setdefault(c, []).append((s, e, sym))
    for arr in by_chrom.values():
        arr.sort()
    scores: dict[str, float] = {}
    for chrom, pos, priority in loci:
        arr = by_chrom.get(chrom, [])
        hi = bisect_right(arr, (pos + flank, float("inf"), ""))
        for _s, e, sym in arr[:hi]:
            if e >= pos - flank and priority > scores.get(sym, 0.0):
                scores[sym] = priority
    return scores


def load_string_graph() -> dict[str, set[str]]:
    """Symbol-level adjacency from STRING physical links (score >= dial)."""
    name: dict[str, str] = {}
    with gzip.open(INFO, "rt", encoding="utf-8") as f:
        f.readline()
        for line in f:
            fld = line.rstrip("\n").split("\t")
            name[fld[0]] = fld[1]
    adj: dict[str, set[str]] = {}
    with gzip.open(LINKS, "rt", encoding="utf-8") as f:
        f.readline()
        for line in f:
            p1, p2, score = line.split()
            if int(score) < MIN_STRING_SCORE:
                continue
            a, b = name.get(p1), name.get(p2)
            if a is None or b is None or a == b:
                continue
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)
    return adj


def components(nodes: set[str], adj: dict[str, set[str]]) -> list[set[str]]:
    seen: set[str] = set()
    out = []
    for start in nodes:
        if start in seen:
            continue
        comp = {start}
        seen.add(start)
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj.get(u, set()) & nodes:
                if v not in seen:
                    seen.add(v)
                    comp.add(v)
                    queue.append(v)
        out.append(comp)
    return sorted(out, key=len, reverse=True)


def connectors(
    comps: list[set[str]],
    adj: dict[str, set[str]],
    in_g: set[str],
    scores: dict[str, float],
) -> list[dict]:
    """Genes outside G adjacent to >= 2 components — the bridge shape."""
    comp_of = {gene: i for i, comp in enumerate(comps) for gene in comp}
    ranked: list[tuple[int, float, str]] = []
    for gene, neigh in adj.items():
        if gene in in_g:
            continue
        joined = {comp_of[v] for v in neigh if v in comp_of}
        if len(joined) >= 2:
            score_sum = round(sum(scores[v] for v in neigh if v in comp_of), 4)
            ranked.append((len(joined), score_sum, gene))
    ranked.sort(key=lambda t: (-t[0], -t[1], t[2]))
    return [
        {"gene": g, "components_joined": n, "joined_score_sum": s}
        for n, s, g in ranked[:TOP_CONNECTORS]
    ]


def shortest_dist(adj: dict[str, set[str]], nodes: set[str], a: str, b: str) -> int | None:
    if a not in nodes or b not in nodes:
        return None
    dist = {a: 0}
    queue = deque([a])
    while queue:
        u = queue.popleft()
        if u == b:
            return dist[u]
        for v in adj.get(u, set()) & nodes:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return None


# -- evaluation (the ONLY place control names appear; see preregistration) --
def evaluate_preregistered(
    in_g: set[str],
    comps: list[set[str]],
    adj: dict[str, set[str]],
    top_connectors: list[dict],
) -> dict:
    lrrk2, nod2, ripk2 = "LRRK2", "NOD2", "RIPK2"
    comp_of = {gene: i for i, comp in enumerate(comps) for gene in comp}
    present = {g: g in in_g for g in (lrrk2, nod2, ripk2)}

    clause_a = False
    a_detail = ""
    if present[lrrk2] and present[nod2]:
        ci, cj = comp_of.get(lrrk2), comp_of.get(nod2)
        if ci is not None and ci == cj:
            comp = comps[ci]
            d_ln = shortest_dist(adj, comp, lrrk2, nod2)
            adjacent = nod2 in adj.get(lrrk2, set())
            on_path = False
            if ripk2 in comp and d_ln is not None:
                d_lr = shortest_dist(adj, comp, lrrk2, ripk2)
                d_rn = shortest_dist(adj, comp, ripk2, nod2)
                on_path = d_lr is not None and d_rn is not None and d_lr + d_rn == d_ln
            clause_a = adjacent or on_path
            a_detail = (
                f"same component (size {len(comp)}), d(L,N)={d_ln}, "
                f"adjacent={adjacent}, ripk2_on_shortest_path={on_path}"
            )
        else:
            a_detail = f"different components ({ci} vs {cj})"
    else:
        a_detail = f"presence: {present}"

    connector_names = [c["gene"] for c in top_connectors]
    clause_b = (present[lrrk2] or present[nod2]) and any(
        g in connector_names for g in (lrrk2, nod2, ripk2)
    )

    if clause_a or clause_b:
        verdict = "PASS"
    elif not (present[lrrk2] or present[nod2]):
        verdict = "NOT-EVALUABLE (neither anchor gene received a positional mapping)"
    else:
        verdict = "FAIL"
    return {
        "verdict": verdict,
        "clause_a": clause_a,
        "clause_a_detail": a_detail,
        "clause_b": clause_b,
        "presence_in_G": present,
        "preregistration": "docs/runs/2026-08-28-lrrk2-control-PREREGISTRATION.md (commit ff8808e)",
    }


def main() -> None:
    if BRIDGE_OUT.exists():
        print(f"[bridge] already complete ({BRIDGE_OUT}); delete to re-run")
        return
    for req in (LINKS, INFO, REFGENE, paths.EIR / "loci.tsv.gz"):
        if not req.exists():
            sys.exit(f"[bridge] missing input: {req}")

    print("[bridge] loading loci ...")
    loci: list[tuple[str, int, float]] = []
    with gzip.open(paths.EIR / "loci.tsv.gz", "rt", encoding="utf-8") as f:
        f.readline()
        for line in f:
            chrom, pos, priority, _n = line.rstrip("\n").split("\t")
            loci.append((chrom, int(pos), float(priority)))

    print("[bridge] positional gene mapping ...")
    envelopes = load_gene_envelopes()
    scores = map_loci_to_genes(loci, envelopes)
    in_g = set(scores)
    print(f"[bridge] {len(envelopes)} gene envelopes; G = {len(in_g)} scored genes")

    print("[bridge] loading STRING physical graph ...")
    adj = load_string_graph()
    print(f"[bridge] {len(adj)} proteins with edges >= {MIN_STRING_SCORE}")

    comps = components(in_g & set(adj), adj)
    sizes = [len(c) for c in comps[:10]]
    print(f"[bridge] {len(comps)} components; largest: {sizes}")
    top = connectors(comps, adj, in_g, scores)

    result = {
        "stage": "13.3 blind bridge recovery + preregistered control",
        "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "dials": {
            "flank_bp": FLANK_BP,
            "min_string_score": MIN_STRING_SCORE,
            "top_connectors": TOP_CONNECTORS,
        },
        "derivation": {
            "loci": len(loci),
            "gene_envelopes": len(envelopes),
            "genes_scored": len(in_g),
            "genes_in_graph": len(in_g & set(adj)),
            "components": len(comps),
            "component_sizes_top10": sizes,
            "top_connectors": top,
        },
        "evaluation": evaluate_preregistered(in_g, comps, adj, top),
    }
    atomic_write_json(BRIDGE_OUT, result)
    print(json.dumps(result["evaluation"], indent=2))
    print(f"[bridge] complete -> {BRIDGE_OUT}")


if __name__ == "__main__":
    main()
