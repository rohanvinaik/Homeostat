"""homeostat.coherence — Regenesis-native SEMANTIC coherence for the driver's PREFER layer.

The self-contained default coherence is STRUCTURAL (`driver.proximity_coherence`: a candidate on a
short/direct path to the shadow tells a more parsimonious mechanism). This is the SEMANTIC override
the `drive(coherence=)` seam was built for: fire the SCOPED events through Regenesis's mechanism
universe ONCE and read which candidates take a mechanistic ROLE (amplifier / inhibitor / binder /
metabolizer / …), scored by the DEPTH of that role — the summed chain-improbability of the
derivations that fired it. A deep, multi-hop role coheres; a shallow one-hop over-fire scores ~0; a
gene that takes NO role is OMITTED (absence is neutral in `rank_candidates`, never a 0 that would
zero the candidate out — the seam's contract).

We feed Regenesis CONTRACTS, not prose — the pure in-process path (`understand(kind='contracts')`),
NOT `kind='text'` (which shells out to the GSE emit SUBPROCESS: ~157s vs ~ms, and the whole point of
Regenesis is to make that Java/Genesis round-trip obsolete). Our L2 `Event`s are already structured
SVO facts, so we emit each straight to an EVENT contract: real gene names as entity lemmas (with
`type_thread: []` -> opaque BY CONSTRUCTION, nothing imports world-knowledge of a name), the verb
lemmatized to its mechanism-universe class centroid. A Form fires from STRUCTURE — the verb's class
against the universe's registered `.index` centroids (`universes/mechanism/archetypes.index`). The
universe fires `universe_only` (its own role Forms, no narrative genre ground).

CARDINAL (docs/DOMAIN_INSTRUMENT_METHOD.md): if the read ABSTAINS on real events, that is a
centroid-REGISTRATION gap in the universe `.index` (or a verb missing from VERB_LEMMA) — calibrate
the centroids/map, NEVER fabricate a verb to make roles fire. "0 patterns" is honest abstention ONLY
once the emitted role verbs are proven reachable to the registered class centroids.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterable, Mapping
from pathlib import Path

from homeostat.event import Event

# The self-contained mechanism universe (authored role Forms + class-centroid .index), at the repo
# root: src/homeostat/coherence.py -> parents[2] == repo root.
MECHANISM_UNIVERSE = Path(__file__).resolve().parents[2] / "universes" / "mechanism"

# The L2 role-verbs -> their mechanism-universe class-centroid LEMMA (data-driven: the 5 distinct
# verbs across every network's events). `understand`'s DSL matches the lemma, not the surface verb
# ('amplifies' abstains, 'amplify' fires), so this is the whole canonicalization the GSE emit did.
# A verb absent here fires no Form -> its events are skipped (they carry no mechanistic role).
VERB_LEMMA = {
    "amplifies": "amplify",  # regulatory (SIGNOR up)   -> amplifier
    "inhibits": "inhibit",  # regulatory (SIGNOR down)  -> inhibitor
    "binds": "bind",  # physical                  -> binder
    "channels": "channel",  # metabolic                 -> metabolizer
    "resembles": "resemble",  # evolutionary              -> homolog
}


def coherence_from_patterns(
    patterns: Iterable[Mapping[str, object]], sidecar: Mapping[str, str]
) -> dict[str, float]:
    """Regenesis recognized-PATTERNS -> per-GENE semantic coherence in (0, 1]. PURE (the pinnable
    decision, extracted from the impure `understand` call).

    Each pattern is ``{name, subject, significance}`` where `subject` is the opaque story token and
    `significance` (>= 0) is the summed chain-improbability of the derivations that fired the Form —
    the role's DEPTH. The subject is mapped back to its gene through the render_story `sidecar`
    CASE-INSENSITIVELY: GSE emit lowercases the opaque token (`Gene2` -> `gene2`), so the join must
    reconcile case or every gene silently drops. Per gene, keep the MAX role significance, then
    normalize by the max across all genes -> (0, 1] (the same max-normalized shape `rank_candidates`
    uses for convergence). A subject not in the sidecar, or a gene whose best significance is 0 (a
    shallow over-fire, no depth), is OMITTED — absence is neutral in the ranker, never a 0 that
    zeroes the candidate. Empty / all-zero -> {} (no signal, not a crash).
    """
    by_lower = {k.lower(): v for k, v in sidecar.items()}  # GSE lowercases the emitted token
    best: dict[str, float] = {}
    for p in patterns:
        subject = p.get("subject")
        gene = by_lower.get(subject.lower()) if isinstance(subject, str) else None
        if gene is None:
            continue
        raw = p.get("significance", 0.0)
        sig = float(raw) if isinstance(raw, (int, float)) else 0.0
        if sig > best.get(gene, -1.0):
            best[gene] = sig
    top = max(best.values(), default=0.0)
    if top <= 0.0:
        return {}
    return {gene: sig / top for gene, sig in best.items() if sig > 0.0}


def event_contract(subject: str, verb: str, target: str, subject_id: str, target_id: str) -> dict:
    """One L2 Event's fields -> its Regenesis EVENT contract node.

    Real gene names are the entity lemmas; `type_thread: []` keeps them opaque (no
    world-knowledge import). `verb` is the class-centroid lemma (VERB_LEMMA);
    `verb_classes=[lemma]` is what the Form fires on (`verb_thread` unneeded -- proven).
    Coreference rides `entity_id`, so the SAME gene must get the SAME id across events for
    multi-hop chains (role DEPTH) to form. The caller resolves subject/target to a stable
    per-gene id and a mapped verb. Pure.
    """
    return {
        "contract_version": "2.0",
        "predicate": {
            "op": "EVENT",
            "args": [
                {"entity_id": subject_id, "lemma": subject, "type_thread": []},
                {"entity_id": target_id, "lemma": target, "type_thread": []},
            ],
            "features": {"verb": verb, "verb_thread": [], "verb_classes": [verb]},
        },
    }


def events_to_contracts(events: Iterable[Event]) -> str:
    """Events -> contract-JSONL for the PURE understand-contracts path (no GSE subprocess). Assigns
    each distinct gene a stable entity id (coreference -> multi-hop role depth), maps each
    verb to its class-centroid lemma, and drops events whose verb has no mapping (they carry no
    mechanistic role). One JSONL line per kept event. Impure over the Event objects (the pure
    per-event decision is `event_contract` + the VERB_LEMMA lookup).
    """
    evs = list(events)
    genes = sorted({g for e in evs for g in (e.subject, e.target)})
    ids = {g: f"e{k}" for k, g in enumerate(genes)}
    lines = []
    for e in evs:
        lemma = VERB_LEMMA.get(e.verb)
        if lemma is None:
            continue
        node = event_contract(e.subject, lemma, e.target, ids[e.subject], ids[e.target])
        lines.append(json.dumps(node, sort_keys=True))
    return "\n".join(lines)


def coherence_from_regenesis(
    events: Iterable[Event], universe_root: str | os.PathLike[str] = MECHANISM_UNIVERSE
) -> dict[str, float]:
    """Fire the SCOPED events through Regenesis ONCE -> per-candidate SEMANTIC coherence for
    `drive(coherence=)`. The IMPURE shell over the pinned `coherence_from_patterns`; the caller
    SCOPES which events to hand in (`events_to_contracts` emits what it is given).

    Emits the events to contract-JSONL (pure Python, no GSE subprocess), builds the mechanism
    Universe (`universe_only`: the domain's role Forms, no narrative ground -- replicating
    Regenesis's own `_universe`: a missing genres.index is a path never read under universe_only),
    fires the pure in-process `understand(kind='contracts')`, and reads the patterns. Subjects come
    back as the real gene names (case-preserved here), so the `{gene: gene}` map is an identity
    through the pinned `coherence_from_patterns`. The Regenesis engine is imported LAZILY so this
    self-contained package degrades to the structural default when it is absent (the ImportError
    propagates to the caller, which falls back to proximity).

    CARDINAL: an ABSTAINED read (no patterns) on real events is a centroid-registration gap (or a
    verb missing from VERB_LEMMA) -- calibrate, NEVER fabricate a verb. Returns {} on abstention.
    """
    from regenesis.instrument import understand
    from regenesis.library import Universe

    evs = list(events)
    contracts = events_to_contracts(evs)
    genes = {g for e in evs for g in (e.subject, e.target)}
    if not contracts:
        return {}
    root = os.fspath(universe_root)
    universe = Universe(
        root,
        os.path.join(root, "genres.index"),  # path only; unread under universe_only
        os.path.join(root, "archetypes.index"),  # the registered role-Form class centroids
        "NARRATIVE",
        True,  # universe_only: fire ONLY the domain's role Forms
    )
    out = understand(contracts, universe=universe, kind="contracts")
    return coherence_from_patterns(out.get("patterns", []), {g: g for g in genes})
