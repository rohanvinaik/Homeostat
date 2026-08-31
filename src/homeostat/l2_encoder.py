"""L2 role encoder — the pure decision turning a gene's data-signals into L3 role-facts.

The signal layer (Fst differentiation over 1000G, GTEx co-expression) is computed by the
I/O shell; this is the pure, Detective-pinnable core: given a gene's boolean signals, emit
the L3 fact sentences (opaque token subject · role verb · literal object — transitive, so a
rule antecedent can fire).

Directed signaling roles (senses/relays/amplifies) are NOT emitted here — they come from the
known-mechanism substrate (docs/ETIOLOGY_ENGINE.md §2b). L2 emits the data-derived roles
(§3b): population differentiation (the genetic lens), co-expression with the mechanism seed
(the expression lens), and the informational zero when the genetic lens has no data on the
gene (abstain != no — an active signal, not a null).

NOTE: the signals here are BOOLEAN, so significance degenerates to hop-counting (every fact
weighs one bit). Graded intensity — the Fst magnitude / correlation strength riding as a
scalar on the fixed role-meaning (GSE) — is the depth layer, deferred (needs the real
magnitudes wired through each lens).
"""

from __future__ import annotations


def data_facts(
    token: str, diff_data: bool, differentiated: bool, coexpresses_seed: bool
) -> list[str]:
    """The L3 facts a gene's real data-signals license, as sentence strings.

    Genetic (differentiation) lens: `differentiates population` when it has data and the gene
    is population-structured; `lacks data` when the lens abstains (no 1000G data) — the
    informational zero, never silence. Expression lens (independent): `tracks seed` when it
    co-moves with the seed. Genetic data present but not differentiated licenses no
    differentiation fact (a measured no).
    """
    facts: list[str] = []
    if not diff_data:
        facts.append(f"{token} lacks data")
    elif differentiated:
        facts.append(f"{token} differentiates population")
    if coexpresses_seed:
        facts.append(f"{token} tracks seed")
    return facts
