"""probes/lrrk2_slice4.py — Slice 4: CONVERGENCE. Does the triad survive agreement across independent lenses?

No single lens holds LRRK2 (Slices 1-3: killed by trait-wiring, buried by STRING, mid-rank by
promiscuity). So the test is convergence — a gene is kept where INDEPENDENT witnesses agree, and the
junk fails at least one. Three independent-ish witnesses vote on each gene in Slice 2's 289-cloud:

  vote_string : in the STRING high-confidence (700) core grown from NOD2  (physical co-occurrence)
  vote_spec   : NOT a promiscuity hub (below Slice 3's spine floor)         (specificity)
  vote_coexpr : GTEx tissue-expression profile correlates with NOD2 (>=0.5) (co-functional, orthogonal)

support = # votes; a gene is BORN into the final mechanism where support >= 2 (converges on >=2
independent lenses). Thresholds are round/principled, NOT tuned to keep LRRK2 — the per-gene vote
table is printed so any fishing would be visible. Reproducible:

    PYTHONPATH=src python3 probes/lrrk2_slice4.py
"""

from __future__ import annotations

import csv
import gzip
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lrrk2_slice2 import SEED, grow, presentation_genes, string_adjacency  # noqa: E402
from lrrk2_slice3 import hub_counts  # noqa: E402

from homeostat.nodes import BORN, node_status  # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data" / "network"
TRIAD = {"NOD2", "RIPK2", "LRRK2"}
KNOWN_HUBS = {"HLA-DRB1", "HLA-DQA1", "IL12B", "TNFSF15", "IL18R1", "IL1RL1", "LACC1"}
COEXPR_MIN = 0.5  # moderate positive correlation
RECUR_MIN = 2  # converge on >= 2 independent lenses


def gtex_profiles(genes: set[str]) -> dict[str, list[float]]:
    """symbol -> log1p tissue-median-TPM vector (52 tissues) for the requested genes."""
    prof: dict[str, list[float]] = {}
    with gzip.open(DATA / "gtex_median_tpm.gct.gz", "rt", errors="replace") as fh:
        next(fh), next(fh), next(fh)  # #1.2, dims, column header
        r = csv.reader(fh, delimiter="\t")
        for row in r:
            if len(row) > 2 and row[1] in genes and row[1] not in prof:
                prof[row[1]] = [math.log1p(float(x)) for x in row[2:]]
    return prof


def pearson(a: list[float], b: list[float]) -> float:
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    return num / (da * db) if da > 0 and db > 0 else 0.0


def main() -> None:
    presentation = presentation_genes()
    cloud, _ = grow(SEED, string_adjacency(400), presentation)
    string700, _ = grow(SEED, string_adjacency(700), presentation)  # the high-confidence core
    hc = hub_counts(cloud)
    floor = sorted(hc.values(), reverse=True)[max(1, len(cloud) // 10) - 1]  # Slice 3 spine floor
    prof = gtex_profiles(cloud)
    nod2 = prof.get("NOD2")

    votes: dict[str, tuple[int, int, int]] = {}
    for g in cloud:
        v_string = 1 if g in string700 else 0
        v_spec = 1 if hc.get(g, 0) < floor else 0
        v_coexpr = 1 if (nod2 and g in prof and pearson(prof[g], nod2) >= COEXPR_MIN) else 0
        votes[g] = (v_string, v_spec, v_coexpr)

    born = [g for g in cloud if node_status(sum(votes[g]), 0, RECUR_MIN) == BORN]

    print(f"cloud {len(cloud)} | STRING-700 core {len(string700)} | spine floor hub-count>={floor}\n")
    print("triad — vote breakdown (string, spec, coexpr) = support:")
    for g in sorted(TRIAD):
        s, p, c = votes[g]
        print(f"  {g:<10} ({s},{p},{c}) = {s + p + c}   born={g in born}")
    print("surviving hubs — vote breakdown:")
    for g in sorted(KNOWN_HUBS & set(cloud)):
        s, p, c = votes[g]
        print(f"  {g:<10} ({s},{p},{c}) = {s + p + c}   born={g in born}")
    print()
    print(f"BORN (converge on >= {RECUR_MIN} independent lenses): {len(born)} genes")
    print(f"  triad in born: {sorted(TRIAD & set(born))}  ({len(TRIAD & set(born))}/3)")
    print(f"  hubs  in born: {sorted(KNOWN_HUBS & set(born))}")
    triad_ct = sum(1 for g in TRIAD if g in born) / 3
    hub_ct = sum(1 for g in (KNOWN_HUBS & set(cloud)) if g in born) / max(1, len(KNOWN_HUBS & set(cloud)))
    print(f"  triad survival rate {triad_ct:.0%} vs hub survival rate {hub_ct:.0%}")
    if len(born) <= 40:
        print("  members:", ", ".join(sorted(born)))


if __name__ == "__main__":
    main()
