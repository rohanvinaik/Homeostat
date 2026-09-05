"""The CONNECTION MAP: given a set of diagnoses (from the glossary), which ones are actually WIRED
together in the multi-network interactome? Deterministic, bounded, computed -- not asserted.

Without molecular observations (a shadow) the pipeline cannot name a single central mechanism; that
is the honest limit. But it CAN answer "which of these conditions are mechanistically adjacent" from
the reference + the web alone: two conditions are wired if their genes DIRECTLY couple, or share a
DIRECT regulator (1-hop, high-confidence >=2-network couplings). Full forward-reach floods (a dense
graph connects everything); 1-hop does not. Diffuse gene sets (e.g. ADHD's ~1800) bridge to almost
anything, so their adjacency is reported but flagged non-specific.

Run: PYTHONPATH=src python scripts/connect.py "Disease One" "Disease Two" ...  (glossary disease
names; needs the data dumps + the glossary present). With no args, a neutral PUBLIC demo set runs.
"""

from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path

from homeostat import (
    metabolic,
    metabolic_fetch,
    paths,
    signor,
    signor_fetch,
    string,
    string_fetch,
)
from homeostat.event import events_to_web
from homeostat.prior_web import DIRECTED_NETWORKS
from homeostat.web import web_adjacency

GLOSSARY = Path(paths.DATA) / "glossary" / "diagnosis_genes.json"
DIFFUSE = 200  # a gene set larger than this bridges non-specifically; flag its adjacencies

# a neutral PUBLIC demo set. Pass your own diagnosis names as CLI args instead -- the presentation
# is always caller-supplied, so no personal cluster is ever hard-coded into the repo.
DEMO = ["Crohn's disease", "Ulcerative colitis", "Ankylosing spondylitis"]


def _web_adj():
    signor_fetch.ensure()
    _, info = string_fetch.ensure_all()
    alias = string_fetch.load_alias_map(info)
    ncbi, rel, gi = metabolic_fetch.ensure_all()
    mids = metabolic.metabolic_pathways(metabolic_fetch.load_tsv(rel))
    esym = metabolic_fetch.load_entrez_symbol(gi)
    events = [
        *signor.signor_events(signor_fetch.load_rows()),
        *string.string_events(string_fetch.load_rows(), alias),
        *metabolic.co_metabolism_events(metabolic_fetch.load_tsv(ncbi), mids, esym),
    ]
    return web_adjacency(events_to_web(events, directed_networks=DIRECTED_NETWORKS), 2.0)


def connection_map(presentation: dict[str, str]) -> str:
    if not GLOSSARY.exists():
        raise SystemExit(f"glossary missing at {GLOSSARY} -- run: python scripts/build_glossary.py")
    glossary = json.loads(GLOSSARY.read_text())
    adj = _web_adj()
    nodes = set(adj)
    total = {lab: glossary.get(name, {}).get("genes", []) for lab, name in presentation.items()}
    genes = {lab: set(gs) & nodes for lab, gs in total.items()}
    # 1-hop forward targets of each condition's genes (the direct downstream)
    targets = {lab: {t for g in gs for t in adj.get(g, ())} for lab, gs in genes.items()}

    out = ["COVERAGE (glossary genes present in the >=2-network web):"]
    for lab in presentation:
        flag = "  <diffuse: adjacency non-specific>" if len(genes[lab]) > DIFFUSE else ""
        out.append(
            f"  {lab:11} {len(genes[lab]):>4} of {len(total[lab]):>4} genes"
            f"  ({len(targets[lab])} direct targets){flag}"
        )

    out.append("")
    out.append("WIRING  (direct gene-gene couplings · shared direct regulators):")
    for a, b in combinations(presentation, 2):
        direct = sum(1 for g in genes[a] if set(adj.get(g, ())) & genes[b])
        direct += sum(1 for g in genes[b] if set(adj.get(g, ())) & genes[a])
        shared = targets[a] & targets[b]
        diffuse = len(genes[a]) > DIFFUSE or len(genes[b]) > DIFFUSE
        tag = "  (non-specific — one side diffuse)" if diffuse else ""
        verdict = "WIRED" if (direct or (shared and not diffuse)) else "no direct link"
        out.append(
            f"  {a:11}<->{b:11} {direct:>3} direct · {len(shared):>4} shared-reg  [{verdict}]{tag}"
        )
        if shared and not diffuse:
            out.append(f"      shared regulators: {sorted(shared)[:12]}")
    return "\n".join(out)


if __name__ == "__main__":
    names = sys.argv[1:] or DEMO
    present = {n[:11]: n for n in names}  # label = disease name truncated for the columns
    print(connection_map(present))
