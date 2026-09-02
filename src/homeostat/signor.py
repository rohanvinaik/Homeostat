"""homeostat.signor — the SIGNOR adapter: curated directed signaling relations → L2 `Event`s.

SIGNOR (https://signor.uniroma2.it) publishes GENE-LEVEL directed causal relations — `A --effect-->
B` with an explicit mechanism and a confidence score — so the regulatory network's directed edges
come out by field access, with no Reactome-style complex-decomposition (the entity types are
explicit, filterable columns, not buried in reaction structure). The full human dump is one TSV file
(`getData.php?organism=9606&format=csv`, no header, 29 columns).

The effect→event mapping is the settled design (2026-09-02), not a per-string knob — it is the
`effect` field's own grammar decomposed into three orthogonal dimensions:

- **direction** (`up`/`down`) → the reserved directed **verb** `amplifies` / `inhibits`. This is the
  regulatory POLARITY, and it rides the verb precisely because `Event.sign` is coupling
  support/censor, NOT polarity. SIGNOR only ever asserts a relation (never "A does not regulate B"),
  so **every emitted edge is `sign=+1`** (it witnesses the coupling exists); a real inhibitory edge
  is `inhibits`/+1, never a censor. Censors (−1) come from their own sources (physics-orthogonal
  exclusions, developmental closing-off, treatment-response), never from a SIGNOR inhibition.
- **mode** (`activity` / `quantity` / bare) → a peer `mode` marker on the SAME edge (the GSE
  set-theory/density op, not a scalar, not a separate network): `activity` = the target's functional
  state changes (post-translational); `abundance` = how much of the target exists changes
  (expression/stability). Both are peers — significance is κ-density over the derivation graph,
  super-additive only at bridges — so neither outranks the other, and a bare `up/down-regulates`
  (direction known, channel unspecified) emits the base edge with no marker (mode-level zero).
- **null** (`unknown`, `form complex`) → no directed claim → skipped. `form complex` is a
  physical-binding assertion, a different network.

Entity normalization (proteinfamily/complex/synonym → canonical gene atomics) and centroid
calibration (SIGNOR's `mechanism` column populates the reserved-verb class centroids) are a separate
harmonizing layer on top; nothing here authors biology.
"""

from __future__ import annotations

from collections.abc import Iterable

from homeostat.event import Event

# SIGNOR column indices (getData csv, tab-separated, no header, 29 cols).
A, TYPE_A, ID_A = 0, 1, 2
B, TYPE_B, ID_B = 4, 5, 6
EFFECT, MECHANISM = 8, 9
DIRECT, SCORE = 22, 27
_MIN_COLS = 28


def parse_effect(effect: str) -> tuple[int, str] | None:
    """Decompose a SIGNOR `effect` string into `(polarity, mode)`, or None if no directed claim.

    `polarity` is +1 (`up-regulates*`) or -1 (`down-regulates*`) — the regulatory sign, which
    becomes the `amplifies`/`inhibits` verb (NOT `Event.sign`). `mode` is the channel the regulation
    acts through: ``"activity"`` (functional-state) if the effect names activity, ``"abundance"`` if
    it names quantity (every `by expression/repression/stabilization/destabilization` submode folds
    in — peer submodes, not intensity tiers), or ``""`` for a bare direction (mode-level zero).
    Returns None for `unknown` / `form complex` / anything with no direction. Pure over `str`.
    """
    if effect.startswith("up-regulates"):
        polarity = 1
    elif effect.startswith("down-regulates"):
        polarity = -1
    else:
        return None
    if "activity" in effect:
        mode = "activity"
    elif "quantity" in effect:
        mode = "abundance"
    else:
        mode = ""
    return polarity, mode


def row_disposition(type_a: str, type_b: str, has_effect: bool) -> str:
    """The keep/skip decision for one SIGNOR relation. Pure over `(str, str, bool)`.

    Returns a named code: ``"skip-nonprotein"`` if either endpoint is not a protein (a complex,
    chemical, phenotype, … — those belong to other networks, not the gene-level regulatory one);
    ``"skip-noeffect"`` if the effect made no directed claim (`has_effect` False — `parse_effect`
    returned None); ``"emit"`` otherwise.
    """
    if type_a != "protein" or type_b != "protein":
        return "skip-nonprotein"
    if not has_effect:
        return "skip-noeffect"
    return "emit"


def row_to_event(fields: list[str]) -> Event | None:
    """One SIGNOR row → a regulatory `Event`, or None (malformed / filtered out).

    A protein→protein relation with a directed effect becomes `Event("regulatory", <amplifies|
    inhibits>, A, B, sign=+1, mode=<activity|abundance|"">)`: the verb carries the regulatory
    polarity, `sign=+1` asserts the coupling exists (SIGNOR never censors), and `mode` is the peer
    channel marker. Composition over the pinned `parse_effect` / `row_disposition`.
    """
    if len(fields) <= _MIN_COLS:
        return None
    parsed = parse_effect(fields[EFFECT])
    if row_disposition(fields[TYPE_A], fields[TYPE_B], parsed is not None) != "emit":
        return None
    assert parsed is not None  # row_disposition == "emit" implies has_effect
    polarity, mode = parsed
    verb = "amplifies" if polarity > 0 else "inhibits"
    return Event("regulatory", verb, fields[A], fields[B], 1, mode)


def signor_events(rows: Iterable[list[str]]) -> list[Event]:
    """Render a stream of SIGNOR rows (each a list of tab-split fields) into regulatory `Event`s.

    I/O-free orchestration over `row_to_event`; intent-tested. (The `direct` flag and confidence
    `score` ride the raw rows but are not yet consumed — direct-only filtering and score-as-a-
    search-order-prior are noted refinements, never significance, which is κ over the graph.)
    """
    out: list[Event] = []
    for r in rows:
        e = row_to_event(r)
        if e is not None:
            out.append(e)
    return out
