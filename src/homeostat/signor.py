"""homeostat.signor — the SIGNOR adapter: curated directed signaling relations → L2 `Event`s.

SIGNOR (https://signor.uniroma2.it) publishes GENE-LEVEL directed causal relations — `A --effect-->
B` with an explicit mechanism and a confidence score — so the regulatory network's directed edges
come out by field access, with no Reactome-style complex-decomposition (the entity types are
explicit, filterable columns, not buried in reaction structure). The full human dump is one TSV file
(`getData.php?organism=9606&format=csv`, no header, 29 columns).

Object-agnostic, and the biology stays the founder's: the **effect→sign policy** (which of SIGNOR's
effect strings count as +1 activation / -1 inhibition / 0 skip — where the `activity`-vs-`quantity`
call lives) is a `Mapping` the caller supplies, never defaulted here. Entity normalization
(proteinfamily/complex/synonym → canonical gene atomics) and the template-sentence/mechanism
enrichment are a separate harmonizing layer, added on top; nothing here authors biology.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from homeostat.event import Event

# SIGNOR column indices (getData csv, tab-separated, no header, 29 cols).
A, TYPE_A, ID_A = 0, 1, 2
B, TYPE_B, ID_B = 4, 5, 6
EFFECT, MECHANISM = 8, 9
DIRECT, SCORE = 22, 27
_MIN_COLS = 28


def row_disposition(type_a: str, type_b: str, sign: int) -> str:
    """The keep/skip decision for one SIGNOR relation, given the sign its effect resolved to.

    Returns a named code: ``"skip-nonprotein"`` if either endpoint is not a protein (a complex,
    chemical, phenotype, … — those belong to other networks, not the gene-level regulatory one);
    ``"skip-noeffect"`` if the effect resolved to sign 0 (not in the policy, or a skipped effect
    like `form complex` / `unknown`); ``"emit"`` otherwise. The effect→sign lookup is the caller's;
    this pins the filter over expressible types. Pure over `(str, str, int)`.
    """
    if type_a != "protein" or type_b != "protein":
        return "skip-nonprotein"
    if sign == 0:
        return "skip-noeffect"
    return "emit"


def row_to_event(fields: list[str], effect_policy: Mapping[str, int]) -> Event | None:
    """One SIGNOR row → a regulatory `Event`, or None (malformed / filtered out).

    `effect_policy` maps each SIGNOR effect string to a sign (+1/-1/0). A protein→protein relation
    whose effect resolves to ±1 becomes `Event(network="regulatory", verb=<mechanism>, subject=A,
    target=B, sign)`; the SIGNOR `mechanism` (phosphorylation, binding, …) is the role-action verb,
    falling back to ``"regulate"`` when blank. Composition over the pinned `row_disposition`.
    """
    if len(fields) <= _MIN_COLS:
        return None
    sign = effect_policy.get(fields[EFFECT], 0)
    if row_disposition(fields[TYPE_A], fields[TYPE_B], sign) != "emit":
        return None
    verb = fields[MECHANISM] or "regulate"
    return Event("regulatory", verb, fields[A], fields[B], sign)


def signor_events(rows: Iterable[list[str]], effect_policy: Mapping[str, int]) -> list[Event]:
    """Render a stream of SIGNOR rows (each a list of tab-split fields) into regulatory `Event`s,
    under the founder's `effect_policy`. I/O-free orchestration over `row_to_event`; intent-tested.
    (The `direct` flag and the confidence `score` are carried in the raw rows but not yet consumed —
    direct-only filtering and score-as-weight are noted refinements, not defaulted here.)
    """
    out: list[Event] = []
    for r in rows:
        e = row_to_event(r, effect_policy)
        if e is not None:
            out.append(e)
    return out
