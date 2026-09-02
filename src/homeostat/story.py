"""homeostat.story — the L2→L3 bridge: events → opaque-token SVO sentences for Regenesis.

Regenesis reads subject-verb-object EVENT SENTENCES, not a frozen graph (ETIOLOGY_ENGINE.md §3).
This renders `list[Event]` into that L3 form so the story layer (STORY_LAYER.md) can `understand()`:

- **One transitive SVO sentence per event** — `<opaque-subject> <verb> <opaque-target>.` The verb
  is the network's RESERVED role-verb (amplifies/inhibits/binds/resembles/co-metabolizes); every
  sentence has a verb + object (never bare), the two hard dialect constraints.
- **Opaque gene tokens** (`Gene1`, …); the real gene is kept in a SIDECAR map, outside reasoning.
  Opacity is load-bearing: an opaque proper noun carries no world-knowledge, so GSE cannot import
  what it "knows" about a real gene name — the role is forced from STRUCTURE (the verbs, who-relates
  -to-whom), never the token. That enforces the no-hard-coded-gene→role cardinal rule at the input,
  and IS the fungibility trick: two tokens firing the same verb get the same role.
- **The RAW events render, not the collapsed couplings** — the several events on one gene-pair (one
  per network) are exactly the convergence a conjunction rule fires on (`if x amplifies y and x
  binds y then x becomes component`). The caller SCOPES which events to render; this renders them.
"""

from __future__ import annotations

from collections.abc import Iterable

from homeostat.event import Event


def assign_tokens(genes: list[str]) -> dict[str, str]:
    """Map each distinct gene symbol to a stable opaque token (`Gene1`, …). Pure over a list.

    Sorted + deduped so the assignment is deterministic across runs; the numbering is opaque (it
    carries no meaning the reasoning may key on — that is the point).
    """
    return {g: f"Gene{i}" for i, g in enumerate(sorted(set(genes)), 1)}


def event_sentence(verb: str, subject_token: str, target_token: str) -> str:
    """One transitive L3 SVO sentence: ``"<subject> <verb> <target>."``. Pure over three strings.
    The verb carries the role-class Forms fire on; subject/target are opaque tokens.
    """
    return f"{subject_token} {verb} {target_token}."


def render_story(events: Iterable[Event]) -> tuple[str, dict[str, str]]:
    """Render an event stream into (L3 story text, sidecar) — the input to a Regenesis `understand`.

    `story text` is the transitive opaque-token SVO sentences joined into GSE-emittable prose. The
    `sidecar` maps each opaque token to its real gene, kept outside reasoning for read-back.
    Orchestration over the pinned `assign_tokens` / `event_sentence`; intent-tested.
    """
    evs = list(events)
    token = assign_tokens([g for e in evs for g in (e.subject, e.target)])
    sentences = [event_sentence(e.verb, token[e.subject], token[e.target]) for e in evs]
    sidecar = {opaque: real for real, opaque in token.items()}
    return " ".join(sentences), sidecar
