"""C1 — cross-population fungibility: is a mechanism's differentiated-member set population-specific?

The headline claim is that the same mechanism is realized by different genes in different populations.
The measurable premise, from real 1000G data: for each mechanism member, WHICH superpopulation drives
its differentiation (the population whose allele frequency is most extreme at the gene's lead variant)?
If a single mechanism's members are driven by DIFFERENT populations, then "which member carries the
population-differentiated variant" is population-dependent — the fungibility signal.

Then the machinery: build a per-population role read (a member is a component IN population P if it is
P-driven AND co-expresses/binds the seed) for two populations, and hand both to Regenesis
`common_frame` — which should recover the invariant role-frame while the filler tokens differ by pop.

Honest scope: this shows the fungibility SIGNAL in the data + that the reasoning recovers the invariant
frame across disjoint fillers. A fully convincing C1 still needs a curated mechanism KNOWN to use
disjoint genes per population (see PROOF_POINTS C1) — this measures the premise, it does not curate it.

    PYTHONPATH=src python3 validation/c1_crosspop.py     # one focused VCF pass over the members
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "probes"))
from local_fst import POPS, gene_pop_profile  # noqa: E402

from a1_panel import MECHANISMS  # noqa: E402

FOCAL_MIN = 0.15  # a lead-variant AF shift of >0.15 toward one population = population-driven


def driver(freqs: dict[str, float]) -> tuple[str, float]:
    """The population whose AF is most extreme vs the mean of the others, and the shift magnitude."""
    best_pop, best_mag = "none", 0.0
    for p in POPS:
        others = [freqs[q] for q in POPS if q != p]
        mag = abs(freqs[p] - sum(others) / len(others))
        if mag > best_mag:
            best_pop, best_mag = p, mag
    return best_pop, best_mag


def main() -> None:
    members = {g for _, ms in MECHANISMS.values() for g in ms}
    seeds = {s for s, _ in MECHANISMS.values()}
    prof = gene_pop_profile(members | seeds)
    labels = json.loads(Path("/tmp/a1_labels.json").read_text())
    # gene -> (coexpr, binds) within its mechanism (from the A1 signal computation)
    sig = {(v["mech"], v["gene"]): (v["coexpr"], v["binds"]) for v in labels.values()}

    print("per-mechanism: driver population of each member's lead variant (real 1000G)\n")
    diverse = []
    for mech, (seed, mem) in MECHANISMS.items():
        rows = []
        for g in mem:
            if g in prof:
                p, mag = driver(prof[g])
                if mag >= FOCAL_MIN:
                    rows.append((g, p, mag))
        drivers = Counter(p for _, p, _ in rows)
        print(f"  {mech:<16} pop-driven members: "
              + ", ".join(f"{g}[{p}]" for g, p, _ in sorted(rows, key=lambda r: -r[2])))
        print(f"  {'':<16} driver-pop spread: {dict(drivers)}  ({len(drivers)} distinct pops)")
        if len(drivers) >= 2:
            diverse.append((mech, seed, mem, rows))

    print(f"\n{len(diverse)}/{len(MECHANISMS)} mechanisms have members driven by ≥2 different "
          f"populations — the fungibility signal (which member is differentiated is population-specific).")

    # common_frame demo on the mechanism with the widest driver spread
    if diverse:
        mech, seed, mem, rows = max(diverse, key=lambda d: len({r[1] for r in d[3]}))
        pops_here = sorted({p for _, p, _ in rows})
        p1, p2 = pops_here[0], pops_here[1]
        outdir = Path("/tmp")
        for pop in (p1, p2):
            facts = []
            for i, g in enumerate(mem):
                tok = f"{pop.lower()}g{i + 1}"
                gp = driver(prof[g]) if g in prof else ("none", 0.0)
                coexp, binds = sig.get((mech, g), (False, False))
                if gp[0] == pop and gp[1] >= FOCAL_MIN:  # differentiated IN this population
                    facts.append(f"{tok} differentiates population")
                    facts.append(f"{tok} dominates population")
                if coexp:
                    facts.append(f"{tok} tracks seed")
                if binds:
                    facts.append(f"{tok} binds seed")
            (outdir / f"c1_{pop}.txt").write_text(". ".join(facts) + ".")
        print(f"\ncommon_frame demo mechanism: {mech} (seed {seed})")
        print(f"  wrote /tmp/c1_{p1}.txt and /tmp/c1_{p2}.txt — disjoint pop-driven fillers, same roles")
        print(f"  → run Regenesis common_frame([/tmp/c1_{p1}.txt, /tmp/c1_{p2}.txt]) to recover the frame")


if __name__ == "__main__":
    main()
