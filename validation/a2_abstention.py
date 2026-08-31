"""A2 — adversarial abstention: the engine rejects the false-positives naive methods accept.

A single-locus / naive method promotes a gene on ONE signal: it co-expresses with the seed, or it
overlaps the disease's GWAS traits, or it is a high-degree hub. Each of those is a documented
false-positive source. This builds synthetic genes that are exactly those false-positives — plus
positive controls that SHOULD promote — feeds the whole batch to the mechanism universe, and checks:

  1. NO false-positive archetype reaches `component` or above:
       - co-expression only        (a naive co-expression hit)
       - trait-overlap only         (a naive GWAS-overlap hit)
       - differentiation only       (population structure with no mechanistic co-occurrence)
       - hub: every qualifying fact BUT promiscuous (the censor must hold it below component)
  2. The positive controls DO reach their tier (component / core), so abstention is not just inertia.
  3. Over random fact-subsets, no gene reaches core without the genuine conjunction.

This is name-blind (opaque tokens) and deterministic (fixed archetypes + seeded random draws). It emits
the batch fact-text + the per-token expectation; run the batch through Regenesis and compare.

    PYTHONPATH=src python3 validation/a2_abstention.py     # writes /tmp/a2_batch.txt + expectations
"""

from __future__ import annotations

import json
import random
from pathlib import Path

# The six primitive facts (emitted lemmas), and the archetypes built from them.
FACTS = [
    "differentiates population",
    "dominates population",
    "tracks seed",
    "binds seed",
    "wires presentation",
    "floods traits",
]

# archetype -> (set of facts, adversarial expectation: may it reach component+?)
ARCHETYPES = {
    "coexpr_only": (["tracks seed"], False),  # naive co-expression hit
    "wiring_only": (["wires presentation"], False),  # naive GWAS-overlap hit
    "diff_only": (
        ["differentiates population", "dominates population"],
        False,
    ),  # pop-structure only
    "hub_flood": (
        [
            "tracks seed",
            "differentiates population",
            "dominates population",
            "wires presentation",
            "floods traits",
        ],
        False,
    ),  # qualifies BUT promiscuous -> censor
    "real_component": (["tracks seed", "differentiates population"], True),  # positive control
    "real_core": (["tracks seed", "differentiates population", "dominates population"], True),
    "lacks": (["lacks data"], False),  # informational zero -> diagnostic
}
N_EACH = 3
N_RANDOM = 20
SEED = 0


def build() -> tuple[str, dict]:
    facts_out: list[str] = []
    expect: dict[str, dict] = {}
    idx = 0

    def add(archetype: str, gene_facts: list[str], may_promote: bool) -> None:
        nonlocal idx
        idx += 1
        tok = f"g{idx}"
        for f in gene_facts:
            facts_out.append(f"{tok} {f}")
        expect[tok] = {"archetype": archetype, "may_reach_component": may_promote}

    for name, (gene_facts, may) in ARCHETYPES.items():
        for _ in range(N_EACH):
            add(name, gene_facts, may)

    rng = random.Random(SEED)
    for _ in range(N_RANDOM):
        k = rng.randint(1, len(FACTS))
        subset = rng.sample(FACTS, k)
        # ground truth per the rules: component needs differentiate ∧ (a co-occurrence lens) ∧ not floods
        cooc = {"tracks seed", "binds seed", "wires presentation"} & set(subset)
        qualifies = "differentiates population" in subset and cooc and "floods traits" not in subset
        add("random", subset, bool(qualifies))

    return ". ".join(facts_out) + ".", expect


def main() -> None:
    text, expect = build()
    Path("/tmp/a2_batch.txt").write_text(text)
    Path("/tmp/a2_expect.json").write_text(json.dumps(expect, indent=0))
    n_fp = sum(1 for v in expect.values() if not v["may_reach_component"])
    n_pos = len(expect) - n_fp
    print(
        f"A2 batch: {len(expect)} synthetic genes — {n_fp} must-NOT-promote, {n_pos} positive controls"
    )
    print("wrote /tmp/a2_batch.txt (fact-text) + /tmp/a2_expect.json (per-token expectation)")
    print("\nexpectation by archetype:")
    for name in list(ARCHETYPES) + ["random"]:
        toks = [t for t, v in expect.items() if v["archetype"] == name]
        may = next(
            (v["may_reach_component"] for v in expect.values() if v["archetype"] == name), None
        )
        tag = (
            "may reach component"
            if (name != "random" and may)
            else "varies (per subset)"
            if name == "random"
            else "MUST stay below component"
        )
        print(f"  {name:<14} {len(toks):>2} genes — {tag}")


if __name__ == "__main__":
    main()
