"""B3 — leave-one-lens-out ablation: what is each lens actually carrying?

Generates the LRRK2 scope's real L2 signals ONCE (via the shared probe computation), then emits the
assembled fact-text with each lens's facts removed in turn. Feed each fact-text to the same mechanism
universe and compare the ledger to the full read. This is the input generator + the ablation matrix;
the ledgers come from the real engine (Regenesis understand over universes/mechanism) — run the
printed fact-texts through it and fill the OBSERVED column, or feed /tmp/b3_*.txt directly.

The rule structure (component.rules) predicts a NON-trivial result, which is the point:
  - differentiation (Fst) is the conserved conjunct of EVERY convergence rule -> dropping it should
    collapse all components (it is a necessary gate BY DESIGN — the program is population-differential
    mechanism, so this is on-thesis, not fragility);
  - the co-occurrence lenses (co-expr / binding / wiring) are the interchangeable first conjunct ->
    dropping any ONE should leave genes that still hold another co-occurrence lens at component
    (this is the real robustness claim: convergence across the interchangeable set carries it);
  - the censor (floods) is load-bearing for specificity -> dropping it should let the promiscuous
    hubs reach component.

    PYTHONPATH=src python3 validation/b3_ablation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "probes"))
from l2_lrrk2 import HUBS, TRIAD, build_context, scope_signals  # noqa: E402

from homeostat.l2_encoder import data_facts  # noqa: E402

# The lens -> the emitted fact lemmas it contributes (confirmed against a live probe run).
LENS_FACTS = {
    "differentiation (Fst)": ["differentiates population", "dominates population"],
    "co-expression (GTEx)": ["tracks seed"],
    "physical binding (STRING)": ["binds seed"],
    "trait-wiring (GWAS)": ["wires presentation"],
    "specificity censor": ["floods traits", "floods trait"],
}


def assemble(per_gene: dict[str, list[str]], drop: list[str]) -> str:
    """Join every gene's facts into one text, removing any fact whose predicate is in `drop`."""
    kept = []
    for facts in per_gene.values():
        for f in facts:
            pred = f.split(" ", 1)[1] if " " in f else f  # strip the "geneN " subject
            if pred not in drop:
                kept.append(f)
    return ". ".join(kept) + "."


def main() -> None:
    ctx = build_context()
    scope = [g for g in list(TRIAD) + HUBS if g in ctx["cloud"]]
    token = {g: f"gene{i + 1}" for i, g in enumerate(scope)}
    per_gene: dict[str, list[str]] = {}
    for g, _fst, tier, coexp, binds, wires, _traits, floods in scope_signals(scope, ctx):
        per_gene[token[g]] = data_facts(token[g], tier, coexp, binds, wires, floods)

    print("token -> gene:", ", ".join(f"{token[g]}={g}" for g in scope))
    print("\n=== FULL (baseline) ===")
    full = assemble(per_gene, drop=[])
    print(full)
    outdir = Path("/tmp")
    (outdir / "b3_FULL.txt").write_text(full)
    for lens, preds in LENS_FACTS.items():
        text = assemble(per_gene, drop=preds)
        slug = lens.split(" ")[0].lower()
        (outdir / f"b3_drop_{slug}.txt").write_text(text)
        print(f"\n=== DROP: {lens} ===")
        print(text)
    print("\nWrote /tmp/b3_FULL.txt and /tmp/b3_drop_*.txt for the engine pass.")


if __name__ == "__main__":
    main()
