"""Homeostat CLI — drop symptoms, get a shrugged mechanistic read. The intended UX, runnable.

    PYTHONPATH=src python3 validation/read.py "<symptom>, <symptom>, <symptom>, ..."
    PYTHONPATH=src python3 validation/read.py "<symptom>, ..." --genotype <promethease.json>

Nothing is hard-coded: each symptom is matched dynamically against trait names in the free corpus, so
any presentation works. It pulls each symptom's genes (GWAS + DISEASES + HPO), finds the specific
low-connectivity genes that BRIDGE the symptoms (generic hubs censored), runs a degree-matched
permutation null so it never overstates, and prints the candidate modules + the honest shrug. The final
LAB-COAT HANDOFF block is for the agent/clinician-scientist to narrate into a causal HYPOTHESIS — which
you then validate or reject. NOT a diagnosis. NOT medical advice. A lead.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "probes"))
from lrrk2_slice2 import string_adjacency  # noqa: E402
from presentation_read import bridge_counts, degree_bins, extract, sample_matched  # noqa: E402

import random  # noqa: E402

R_NULL = 200


def resolve(symptoms: list[str]) -> tuple[dict, dict]:
    """symptom text -> (name -> keyword list). Fully dynamic: each symptom matches trait names that
    contain its own text. No condition is hard-coded — whatever you type is what it reads."""
    kw, display = {}, {}
    for s in symptoms:
        name = s.strip()
        kw[name] = [name.lower()]
        display[name] = name
    return kw, display


def specific_bridges(sets: dict, adj: dict, need: int) -> list[tuple]:
    """genes touching ≥`need` of the sets (member or neighbor), censored by top-decile degree, spec-first."""
    universe = set().union(*sets.values())
    cand = universe | {n for s in sets.values() for m in s for n in adj.get(m, ())}
    touch = {}
    for g in cand:
        nbrs = adj.get(g, set())
        t = sum(1 for s in sets.values() if g in s or (nbrs & s))
        if t >= need:
            touch[g] = t
    deg = {g: len(adj.get(g, set())) for g in touch}
    cut = sorted(deg.values(), reverse=True)[max(1, len(deg) // 10) - 1] if deg else 10**9
    return sorted(((g, deg[g], touch[g]) for g in touch if deg[g] < cut), key=lambda r: r[1])


def genotype_overlay(candidate_genes: list[str], path: str, mag_min: float = 2.0) -> None:
    """OPTIONAL n=1 sharpening: which candidate genes does THIS person carry notable variants in?

    Reads a promethease-style JSON ({rsid: {genes, magnitude, repute, summary}}). PERSONAL — the input
    and this output stay on the machine; nothing here is committed or transmitted."""
    try:
        data = json.load(open(path))
    except (OSError, ValueError) as e:
        print(f"\n(genotype overlay skipped — could not read {path}: {e})")
        return
    cand = set(candidate_genes)
    hits = []
    for rsid, v in data.items():
        if not isinstance(v, dict):
            continue
        try:
            mag = float(v.get("magnitude") or 0)
        except (TypeError, ValueError):
            mag = 0.0
        if mag < mag_min:
            continue
        raw_genes = v.get("genes") or []
        gs = raw_genes if isinstance(raw_genes, list) else str(raw_genes).replace(";", ",").split(",")
        for g in (x.strip() for x in gs):
            if g in cand:
                hits.append((g, mag, rsid, v.get("repute", ""), (v.get("summary") or "")[:70]))
    hits.sort(key=lambda h: -h[1])
    print("\n" + "-" * 78)
    print("YOUR n=1 OVERLAY (from your genotype — PERSONAL, stays on this machine, never committed):")
    if not hits:
        print("  no notable variants in the candidate genes — the population lead isn't personally sharpened.")
    else:
        print(f"  of the candidate mechanism genes, you carry NOTABLE variants (magnitude ≥ {mag_min}) in:")
        for g, mag, rsid, rep, summ in hits[:20]:
            print(f"    {g:<9} {rsid:<12} mag={mag:<4} {rep:<4} {summ}")
    print("  → this sharpens a population shrug into a personal lead. Validate against your labs.")


def jeeves(names: list, genes: dict, display: dict, adj: dict) -> list[str]:
    """Jeeves mode — notice the SHAPE of the result and pre-empt the obvious next query, from the data
    geometry alone (no LLM). The intelligence is paying attention to the chained-obvious, not erudition:
    a desert phenotype's genes still sit next to *something* — point there; the real signal usually
    concentrates in a pair, not the whole set — say which; wait where the user is about to need it."""
    import itertools

    def deg(g):
        return len(adj.get(g, set()))

    universe = len({g for s in genes.values() for g in s} | set(adj)) or 1

    def shared_with(n, m):  # genes of n that are members of, or STRING-bound to, m
        return (genes[n] & genes[m]) | {g for g in genes[n] if adj.get(g, set()) & genes[m]}

    nudges = []
    # (1) A desert can barely speak alone — but where do its few genes actually live? Re-home it.
    for n in names:
        if 0 < len(genes[n]) <= 15:
            scored = [(len(shared_with(n, m)), m) for m in names if m != n]
            best_n, best = max(scored, default=(0, None))
            if best and best_n:
                via = ", ".join(sorted(shared_with(n, best), key=deg)[:4])
                nudges.append(f"'{display[n]}' is nearly data-empty on its own — but {best_n} of its few genes "
                              f"are shared with or bound to '{display[best]}' ({via}). If '{display[n]}' is the "
                              f"real question, that's where it can speak:  read.py \"{display[n]}, {display[best]}\"")
    # (2) The sharpest signal is the pair whose overlap most EXCEEDS chance for its size — not the two
    #     biggest sets (that is just size). Rank by enrichment = observed / expected-by-size.
    best_pair, best_enr, best_sh = None, 1.5, []
    for a, b in itertools.combinations(names, 2):
        sh = [g for g in (genes[a] & genes[b]) if deg(g) < 100]
        exp = len(genes[a]) * len(genes[b]) / universe
        enr = len(sh) / exp if exp > 0 else 0
        if len(sh) >= 3 and enr > best_enr:
            best_pair, best_enr, best_sh = (a, b), enr, sh
    if best_pair:
        top = ", ".join(sorted(best_sh, key=deg)[:6])
        nudges.append(f"the densest thread isn't the whole set — it's '{display[best_pair[0]]}' + "
                      f"'{display[best_pair[1]]}', which overlap {best_enr:.1f}× more than their sizes predict "
                      f"({len(best_sh)} specific genes: {top}). I'd point the lab coat there first.")
    return nudges


def main() -> None:
    argv = sys.argv[1:]
    geno = None
    if "--genotype" in argv:
        i = argv.index("--genotype")
        geno = argv[i + 1] if i + 1 < len(argv) else None
        argv = argv[:i] + argv[i + 2:]
    raw = " ".join(argv)
    symptoms = [s for s in raw.replace(";", ",").split(",") if s.strip()]
    if not symptoms:
        print('usage: read.py "<symptom>, <symptom>, ..." [--genotype <promethease.json>]')
        return
    kw, display = resolve(symptoms)
    names = list(kw)

    print("HOMEOSTAT · a reading, not a ruling.")
    print("  I pull the genes that live under each symptom from open data, find what actually connects")
    print("  them, and tell you what that means — and, as carefully, what it doesn't. I can rank and")
    print("  connect; I will not impute the mechanism's *purpose*. Building that is the lab-coat's job,")
    print("  and I'll hand you exactly what it needs. (Research hypothesis generation. Not medical advice.)\n")
    genes, terms = extract(set(names), kw)
    adj = string_adjacency(700)

    print("what you handed me, and how much the open literature actually knows about each:")
    sparse = []
    for n in names:
        ts = sorted(terms[n])
        note = "  ← a data desert; medicine has all but ceded this one, so it can barely speak here" \
            if len(genes[n]) <= 10 else ""
        if len(genes[n]) <= 10:
            sparse.append(n)
        print(f"  {display[n]:<22}{len(genes[n]):>5} genes   e.g. {', '.join(ts[:2]) or '(nothing found)'}{note}")

    # bridge on the full set; if it collapses on a data-desert symptom, drop the sparsest and SAY so.
    sets = {n: genes[n] for n in names}
    need = len(names)
    bridges = specific_bridges(sets, adj, need)
    dropped = None
    if not bridges and len(names) > 2 and sparse:
        dropped = min(names, key=lambda n: len(genes[n]))
        sets = {n: genes[n] for n in names if n != dropped}
        need = len(sets)
        bridges = specific_bridges(sets, adj, need)

    if dropped:
        print(f"\n(the whole set won't converge — '{display[dropped]}' is too data-starved to reach. I read the "
              f"other {need} where the data can, and I'll point you back at '{display[dropped]}' below.)")
    print(f"\nwhat connects them — the specific genes bridging all {need} of these symptoms. I dropped the")
    print("generic hubs on purpose: a gene that touches everything explains nothing.")
    print("  " + (" ".join(f"{g}" for g, d, _ in bridges[:24]) if bridges else "(nothing specific bridges them — the honest answer is 'no shared thread I can see')"))

    # degree-matched null — reported as MEANING, not a verdict-word
    universe = sorted(set(adj) | {g for s in sets.values() for g in s})
    bin_of, bins = degree_bins(universe, adj)
    k = len(sets)
    obs = bridge_counts(sets, adj, universe)[k]
    rng = random.Random(0)
    nul = [bridge_counts({p: sample_matched(s, bin_of, bins, rng) for p, s in sets.items()}, adj, universe)[k]
           for _ in range(R_NULL)]
    nm = sum(nul) / len(nul)
    p = (sum(1 for x in nul if x >= obs) + 1) / (R_NULL + 1)
    print(f"\nhow much to trust it: {obs} genes bridge all {k}, against {nm:.0f} expected purely by chance "
          f"(p={p:.2f}).")
    if p < 0.05 and obs > nm:
        print("  that is above chance — a genuine lead. Still a hypothesis, but one worth chasing hard.")
    else:
        print("  that is *not* above chance. Read the genes above as 'worth a look', not 'the mechanism' —")
        print("  the connections are real but no denser than coincidence would give. The missing piece is the")
        print("  one medicine is also missing: your genes AND your symptoms together, at scale. Holding this")
        print("  at 'lead' instead of dressing it up is the honest part, and the whole point.")

    for nudge in jeeves(names, genes, display, adj):
        print("\n▸ " + nudge)

    if geno:
        genotype_overlay([g for g, _, _ in bridges], geno)

    print("\n" + "=" * 78)
    print("LAB-COAT HANDOFF (for the agent / clinician-scientist):")
    print("  Group the bridge genes above into functional modules and narrate the most coherent CAUSAL")
    print("  HYPOTHESIS they support — cite the genes, connect the symptoms, and state where the data")
    print("  stops (the desert symptoms, the null). Frame as hypothesis to validate/reject, never a")
    print("  diagnosis. See docs/EXAMPLE_CASE_READ.md for the worked form.")


if __name__ == "__main__":
    main()
