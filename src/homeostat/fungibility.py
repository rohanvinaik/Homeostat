"""homeostat.fungibility — the ALLEGORY interpretive layer: fungibility earned by traversal.

Allegory is not a story-frame detector (tragedy/comedy are); it is the fungibility LAYER that makes
the whole read robust to token substitution — the anti-population-medicine move (recover the
mechanism whose CAST varies: gene-pool {X} in one person, a paralog {Y} in another, one shadow).

Fungibility is NOT decided at the gene. A `resembles`/paralog edge (the evolutionary bank) is only
the SEED — "these two MIGHT be one role." The VERDICT inverts the SparseWiki "Jordan-vs-Jordan"
disambiguation: where an ambiguous token's senses FAN OUT under multi-bank traversal (divergence
resolves *which* meaning), two paralogs are fungible where their relational positions FAN IN — they
converge on the SAME partners across INDEPENDENT confirming banks (regulatory/physical/metabolic).
Convergence across orthogonal banks is improbable-and-coherent (H3, orthogonal partials summing,
pointed at IDENTITY not coupling), so fungibility is EARNED by the geometry, never asserted at the
token. Paralogs that resemble but whose paths diverge (subfunctionalized) are NOT folded -- and the
STRUCTURAL ELIMINATOR (structural.py) removes a merge only on a FUNDAMENTAL physical blocker
(membrane-integral vs soluble cannot be one role), abstaining on everything moderate. Structure
CLEANS the space -- it excludes the impossible, is the informational zero elsewhere, and NEVER
promotes: the coupling convergence carries the positive signal, the story engine decides over the
survivors. (Global similarity is not pathway-fungibility -- the role is a LOCAL site.)
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from homeostat.event import Event
from homeostat.structural import structural_class, structural_compatibility

SEED_BANK = "evolutionary"
SEED_VERB = "resembles"
CONFIRMING_BANKS = frozenset({"regulatory", "physical", "metabolic"})


@dataclass(frozen=True)
class Fungible:
    """One paralog seed and its earned verdict: `a` < `b` (the resembles pair), `verdict` —
    ``"fungible"`` (≥2 independent banks converge on shared partners: H3), ``"coincidental"`` (one
    bank only), or ``"seed-only"`` (resemblance alone, no confirmation) — and `banks`, the count of
    independent confirming banks whose paths converged."""

    a: str
    b: str
    verdict: str
    banks: int


def paralog_seeds(events: Iterable[Event]) -> set[tuple[str, str]]:
    """The `resembles` pairs from the evolutionary bank — the fungibility SEEDS, each once as
    (a < b), self-pairs dropped. Pure over the event stream; intent-tested."""
    seeds: set[tuple[str, str]] = set()
    for e in events:
        if e.network == SEED_BANK and e.verb == SEED_VERB and e.subject != e.target:
            seeds.add((e.subject, e.target) if e.subject < e.target else (e.target, e.subject))
    return seeds


def partners_by_bank(events: Iterable[Event]) -> dict[str, dict[str, set[str]]]:
    """`{bank: {gene: {partners}}}` over the CONFIRMING banks only, edges undirected (both endpoints
    are partners), self-loops dropped. The relational position each gene occupies per bank — what
    the traversal converges on. Orchestration; intent-tested."""
    banks: dict[str, dict[str, set[str]]] = {}
    for e in events:
        if e.network in CONFIRMING_BANKS and e.subject != e.target:
            pmap = banks.setdefault(e.network, {})
            pmap.setdefault(e.subject, set()).add(e.target)
            pmap.setdefault(e.target, set()).add(e.subject)
    return banks


def banks_converged(a: str, b: str, partners: dict[str, dict[str, set[str]]]) -> int:
    """How many independent confirming banks place `a` and `b` at the SAME relational position —
    i.e. share a partner OTHER than each other (the pair itself is the seed, never confirmation).
    Each such bank is an orthogonal witness that the two paralogs fill one role. Orchestration; pure
    over the partner maps; intent-tested."""
    count = 0
    for pmap in partners.values():
        shared = (pmap.get(a, set()) - {a, b}) & (pmap.get(b, set()) - {a, b})
        if shared:
            count += 1
    return count


def fungibility_verdict(banks_converged: int, structural: str = "indeterminate") -> str:
    """The pure fungibility decision: bank convergence, gated by the structural ELIMINATOR. Codes:
    - ``"subfunctionalized"`` -- `structural == "incompatible"`: a FUNDAMENTAL physical blocker
      (cannot be one role, e.g. membrane-integral vs soluble) removes the merge, any convergence;
    - else the count threshold: fungible (>=2), coincidental (1), seed-only (0).
    Structure CLEANS (excludes the impossible, else abstains) and NEVER promotes: a match or an
    abstention leaves the count untouched. Pure over `(int, str)`; `structural` defaults to abstain.
    """
    if structural == "incompatible":
        return "subfunctionalized"
    if banks_converged >= 2:
        return "fungible"
    if banks_converged == 1:
        return "coincidental"
    return "seed-only"


def read_fungibility(
    events: Iterable[Event], proteins: Mapping[str, str] | None = None
) -> list[Fungible]:
    """Read the fungibility layer: for each paralog seed, the verdict earned by how many independent
    confirming banks its traversal converges across, gated by structure. Reports every
    seed with its verdict (the ``"fungible"`` ones are the role-equivalences the read may fold).

    `proteins` (gene -> AA sequence) enables the structural gate: a seed whose two proteins are in
    DIFFERENT confident classes is barred ``"subfunctionalized"`` regardless of convergence. Absent
    (or a gene missing), the gate abstains -- convergence-only, back-compatible. Orchestration over
    the pinned `fungibility_verdict` / `structural_compatibility`; intent-tested.
    """
    evs = list(events)
    partners = partners_by_bank(evs)
    seqs = proteins or {}
    out: list[Fungible] = []
    for a, b in sorted(paralog_seeds(evs)):
        n = banks_converged(a, b, partners)
        structural = "indeterminate"
        if a in seqs and b in seqs:
            structural = structural_compatibility(
                structural_class(seqs[a]), structural_class(seqs[b])
            )
        out.append(Fungible(a, b, fungibility_verdict(n, structural), n))
    return out
