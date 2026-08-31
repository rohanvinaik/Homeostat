"""A1 + E1 — positive-control panel across 8 documented mechanisms, blind to gene identity.

Each mechanism is a seed + its textbook members (established complexes/pathways — the ground truth).
For each, the scope = true members + generic GWAS hubs + random decoys, scored on the domain-general
lenses ONLY (no inflammation-specific trait-wiring): population differentiation, GTEx co-expression
with the seed, STRING physical binding to the seed, and the promiscuity censor. Lenses are computed by
the same helpers as the LRRK2 probe; the reasoning is name-blind (opaque tokens).

Two calibrations make the free-data lenses discriminate (see the diagnosis in VALIDATION_RESULTS.md):
  - DIFFERENTIATION is scored as a genome-wide PERCENTILE of local whole-region max-Fst (top decile =
    `dominant`, top third = `moderate`), not the absolute Wright bands — the whole-region max is
    count-biased and saturates on an absolute scale, so a relative cut (the original genetic-lens
    design, lrrk2_genetic_diff) is what makes it a filter rather than a free pass.
  - CO-EXPRESSION cutoff is the 95th percentile of the shuffled-seed null over a large RANDOM genome
    background, not the tiny scope — otherwise broadly-expressed decoys clear a weak per-scope null.

A1 passes if members reach `component`+ far above random decoys and the hubs are censored. E1 rides
along: 8 domains, zero per-domain code — only the seed + member list change.

    PYTHONPATH=src python3 validation/a1_panel.py     # first run does the (cached) VCF Fst pass
"""

from __future__ import annotations

import json
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "probes"))
from local_fst import REFGENE, gene_maxfst  # noqa: E402

from l2_lrrk2 import gtex_null_cutoff  # noqa: E402
from lrrk2_slice2 import string_adjacency  # noqa: E402
from lrrk2_slice3 import hub_counts  # noqa: E402
from lrrk2_slice4 import gtex_profiles, pearson  # noqa: E402

from homeostat.l2_encoder import data_facts  # noqa: E402

MECHANISMS = {
    "nod2_signaling": ("NOD2", ["RIPK2", "XIAP", "CARD9", "BIRC2", "BIRC3"]),
    "mismatch_repair": ("MLH1", ["MSH2", "MSH6", "PMS2", "MSH3", "PMS1"]),
    "complement": ("C3", ["C5", "C2", "CFB", "CFH", "CFI", "C4BPA"]),
    "coagulation": ("F2", ["F5", "F7", "F9", "F10", "F13A1", "FGA", "FGB", "FGG", "VWF"]),
    "ldl_clearance": ("LDLR", ["APOB", "PCSK9", "LDLRAP1", "APOE"]),
    "mitophagy": ("PINK1", ["PRKN", "PARK7", "FBXO7"]),
    "inflammasome": ("NLRP3", ["PYCARD", "CASP1", "IL1B", "IL18", "NEK7"]),
    "type1_ifn": ("TBK1", ["IRF3", "IRF7", "STING1", "MAVS", "DDX58"]),
}
HUBS = ["HLA-DQA1", "HLA-DRB1", "HLA-B", "HLA-DRB5"]
N_DECOYS = 8
N_BACKGROUND = 2000  # random genes for the genome-wide Fst + co-expression null distributions
SEED_RNG = 0
DOMINANT_PCT = 90  # top decile of genome-wide differentiation
MODERATE_PCT = 66  # top third


def refgene_symbols() -> list[str]:
    syms = set()
    proc = subprocess.Popen(["gzip", "-dc", str(REFGENE)], stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:  # type: ignore[union-attr]
        f = line.split("\t")
        if len(f) >= 13 and f[12] and not f[12].startswith(("MIR", "LINC", "LOC")):
            syms.add(f[12])
    proc.wait()
    return sorted(syms)


def _pct(values: list[float], p: int) -> float:
    s = sorted(values)
    return s[min(len(s) - 1, len(s) * p // 100)]


def main() -> None:
    seeds = {s for s, _ in MECHANISMS.values()}
    members = {g for _, ms in MECHANISMS.values() for g in ms}
    all_syms = refgene_symbols()
    rng = random.Random(SEED_RNG)
    pool = sorted(set(all_syms) - seeds - members - set(HUBS))
    decoys = rng.sample(pool, N_DECOYS)
    background = rng.sample(sorted(set(pool) - set(decoys)), N_BACKGROUND)

    panel_genes = seeds | members | set(HUBS) | set(decoys)
    fst = gene_maxfst(panel_genes | set(background), cache=Path("/tmp/panel_bg_fst.tsv"))
    bg_vals = [fst[g] for g in background if g in fst]
    dom_cut, mod_cut = _pct(bg_vals, DOMINANT_PCT), _pct(bg_vals, MODERATE_PCT)

    def rel_tier(g: str) -> str:
        if g not in fst:
            return "nodata"
        f = fst[g]
        return "dominant" if f >= dom_cut else "moderate" if f >= mod_cut else "none"

    prof = gtex_profiles(panel_genes)
    bg_prof = gtex_profiles(set(background[:800]))  # background for the co-expression null
    adj700 = string_adjacency(700)
    hc = hub_counts(panel_genes)
    prom = sorted(hc.values(), reverse=True)
    prom_cut = prom[max(1, len(prom) // 10) - 1] if prom else 10**9

    labels: dict[str, dict] = {}
    tok = 0
    outdir = Path("/tmp")
    for mech, (seed, mem) in MECHANISMS.items():
        scope = [seed] + mem + HUBS + decoys
        seed_vec = prof.get(seed)
        cut = gtex_null_cutoff(seed_vec, bg_prof) if seed_vec else 1.0  # background-calibrated
        binders = adj700.get(seed, set())
        facts: list[str] = []
        for g in scope:
            tok += 1
            t = f"x{tok}"
            tier = rel_tier(g)
            coexp = bool(seed_vec and g in prof and pearson(prof[g], seed_vec) >= cut)
            binds = g in binders and g != seed
            floods = hc.get(g, 0) >= prom_cut
            facts.extend(data_facts(t, tier, coexp, binds, False, floods))
            role = "seed" if g == seed else "member" if g in mem else "hub" if g in HUBS else "decoy"
            labels[t] = {"mech": mech, "gene": g, "role": role, "tier": tier,
                         "coexpr": coexp, "binds": binds, "floods": floods,
                         "fst": round(fst[g], 4) if g in fst else None}
        (outdir / f"a1_{mech}.txt").write_text(". ".join(facts) + ".")

    (outdir / "a1_labels.json").write_text(json.dumps(labels, indent=0))
    from collections import Counter
    tiers = Counter(v["tier"] for v in labels.values())
    print(f"panel: {len(MECHANISMS)} mechanisms | {len(members)} members | {len(HUBS)} hubs | "
          f"{len(decoys)} decoys | background {len(bg_vals)} genes")
    print(f"differentiation percentile cuts (genome bg): dominant≥{dom_cut:.3f} moderate≥{mod_cut:.3f}")
    print(f"tier distribution now: {dict(tiers)}")
    print(f"promiscuity flood cut (top decile) ≥ {prom_cut} traits")
    print(f"decoys (random, seed {SEED_RNG}): {', '.join(decoys)}")
    print("per-mechanism scopes -> /tmp/a1_<mech>.txt ; labels -> /tmp/a1_labels.json")


if __name__ == "__main__":
    main()
