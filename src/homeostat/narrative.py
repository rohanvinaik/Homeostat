"""homeostat.narrative — the story-read: the four mechanism genres composed into ONE account.

The PREFER layer, replacing gene-ranking (the answer is a STORY, not a ranked gene). It runs the
four native genre readers over the (caller-scoped) structure, collects the tier-1 instances, and
fires a tier-2 DERIVATION OVER THE DERIVATIONS — the presentation-level account ("these comedies
feeding that tragedy add up to THIS") — through Regenesis's NARRATIVE universe: the same engine that
reads Shakespeare (Winston's thesis, that story understanding is one general capacity, made tangible
— a House-style read in the language that understands Macbeth).

The tier-2 goes through the PURE CONTRACTS path (`understand(kind='contracts')`), NOT the GSE-emit
text subprocess, so a greenfield clone needs only Regenesis's pure core — no GSE/Genesis. The engine
is imported LAZILY: absent, the read degrades to the tier-1 genres with `account=None` (a loud,
trivially-fixable gap). Plural, no single subject.

CARDINAL: a genre instance emits a fact ONLY for an opinionated verdict, mapped to its natural
narrative relation; the tier-2 recognizes what it recognizes (compute-not-impose). If the narrative
universe abstains on real genre-facts, that is a centroid-reachability gap to calibrate — NEVER
author a verb to force a read.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from homeostat.comedy import read_comedy
from homeostat.event import Event
from homeostat.fungibility import read_fungibility
from homeostat.lament import Lament, read_lament
from homeostat.quest import read_quest
from homeostat.tragedy import read_tragedy

# The hand-authored LINKAGE: each mechanism-genre verdict -> the Polti dramatic situation it IS,
# named by that Form's own trigger verb (the narrative universe's `archetypes.index`). NOT
# trigger-fishing: we compute the genre from the dynamics, so we assert its true dramatic kind. A
# closed domain of a few hand-pinned definitions (Winston's method) -- extend the tables to add a
# genre. Non-dramatic verdicts map to nothing (honest abstention at the meta level):
#   tragedy (doom cascade)  IS  PURSUIT   -- a flaw pursuing a node to ruin           -> "harm"
#   comedy  (vicious loop)  IS  REVENGE   -- two parts compounding each other's harm  -> "betray"
#   quest   (resolving)     IS  OBTAINING -- a distant hero obtaining the cure         -> "seize"
#   quest   (entangling)    IS  PURSUIT   -- a pursuit that fails to obtain            -> "pursue"
# allegory (fungibility) is a structural LENS, not a dramatic situation -> no tier-2 fact (it feeds
# the treatment tier instead); homeostatic comedy is the benign ending ("no crime here") -> none.
_TRAGEDY_VERB = {"doomed": "harm", "suppressed": "harm"}
_COMEDY_VERB = {"vicious": "betray"}
_ALLEGORY_VERB: dict[str, str] = {}
_QUEST_VERB = {"resolving": "seize", "entangling": "pursue"}


@dataclass(frozen=True)
class StoryRead:
    """The presentation-level story. `genres` is the tier-1 dynamics instances per genre (comedy /
    tragedy / allegory / quest); `account` is the tier-2 read (Regenesis's derivation-over-the-
    derivations through the narrative universe) — or None when the engine is absent (degradation to
    the native genres); `treatment` is the tier-3 therapeutic read (the laments — the POC of the
    treatment tier). Plural, no single subject."""

    genres: dict[str, list]
    account: dict | None
    treatment: list[Lament]


def genre_triples(genres: Mapping[str, list]) -> list[tuple[str, str, str]]:
    """The tier-1 genre instances -> ``(subject, verb, object)`` narrative triples for the tier-2
    meta-narrative. Only OPINIONATED verdicts (mapped in the ``_*_VERB`` tables) emit a triple; a
    quest emits one per joined part (the hero rescues/entangles each). Pure over the genre map.
    """
    out: list[tuple[str, str, str]] = []
    for t in genres.get("tragedy", []):
        verb = _TRAGEDY_VERB.get(t.verdict)
        if verb:
            out.append((t.origin, verb, t.sink))
    for c in genres.get("comedy", []):
        verb = _COMEDY_VERB.get(c.verdict)
        if verb:
            out.append((c.a, verb, c.b))
    for f in genres.get("allegory", []):
        verb = _ALLEGORY_VERB.get(f.verdict)
        if verb:
            out.append((f.a, verb, f.b))
    for q in genres.get("quest", []):
        verb = _QUEST_VERB.get(q.verdict)
        if verb:
            out.extend((q.hero, verb, part) for part in q.joined)
    return out


def triples_to_contracts(triples: list[tuple[str, str, str]]) -> str:
    """Narrative triples -> contract-JSONL for the pure understand-contracts tier-2 (no GSE
    subprocess). Each distinct entity gets a stable id (coreference -> the meta-narrative's arc);
    verb_classes=[verb] is what the narrative universe fires on. One line per triple. Pure.
    """
    genes = sorted({g for s, _, o in triples for g in (s, o)})
    ids = {g: f"e{k}" for k, g in enumerate(genes)}
    lines = []
    for s, verb, o in triples:
        node = {
            "contract_version": "2.0",
            "predicate": {
                "op": "EVENT",
                "args": [
                    {"entity_id": ids[s], "lemma": s, "type_thread": []},
                    {"entity_id": ids[o], "lemma": o, "type_thread": []},
                ],
                "features": {"verb": verb, "verb_thread": [], "verb_classes": [verb]},
            },
        }
        lines.append(json.dumps(node, sort_keys=True))
    return "\n".join(lines)


def _compose(triples: list[tuple[str, str, str]]) -> dict | None:
    """Fire the tier-2 derivation-over-the-derivations through the narrative universe via the PURE
    contracts path (no GSE). Lazy import -> None when the engine is absent (degrades gracefully).
    """
    if not triples:
        return None
    try:
        from regenesis.instrument import understand
    except ImportError:
        return None
    return understand(triples_to_contracts(triples), kind="contracts")  # universe=None -> narrative


def read_story(
    events: Iterable[Event], observed: Iterable[str], proteins: Mapping[str, str] | None = None
) -> StoryRead:
    """Read the presentation as a STORY: run the four native genre readers over the (caller-scoped)
    events, compose their instances into the tier-2 narrative account, and read the tier-3 treatment
    (laments). The caller SCOPES which events to hand in (relevance = the observed cone).
    Orchestration over the pinned readers + `genre_triples` + `read_lament`; the tier-2 is the
    pure-contracts derivation-over-derivations; intent-tested.
    """
    evs = list(events)
    obs = list(observed)
    genres = {
        "comedy": read_comedy(evs),
        "tragedy": read_tragedy(evs),
        "allegory": read_fungibility(evs, proteins),
        "quest": read_quest(evs, obs),
    }
    return StoryRead(genres, _compose(genre_triples(genres)), read_lament(genres))
