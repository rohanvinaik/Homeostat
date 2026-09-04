"""homeostat.coherence — Regenesis-native SEMANTIC coherence for the driver's PREFER layer.

The self-contained default coherence is STRUCTURAL (`driver.proximity_coherence`: a candidate on a
short/direct path to the shadow tells a more parsimonious mechanism). This is the SEMANTIC override
the `drive(coherence=)` seam was built for: fire the SCOPED story through Regenesis's mechanism
universe ONCE and read which candidates take a mechanistic ROLE (amplifier / inhibitor / binder /
metabolizer / …), scored by the DEPTH of that role — the summed chain-improbability of the
derivations that fired it. A deep, multi-hop role coheres; a shallow one-hop over-fire scores ~0; a
gene that takes NO role is OMITTED (absence is neutral in `rank_candidates`, never a 0 that would
zero the candidate out — the seam's contract).

The read is grounded in the ROLE VERB, never the gene token: `story.render_story` hands Regenesis
opaque-SVO prose (`Gene1 amplifies Gene2.`) plus a sidecar, so a Form fires from STRUCTURE — the
active universe's registered class centroids (`universes/mechanism/archetypes.index` trigger column)
— and the recognized subject (opaque token) is mapped BACK to its gene here. The universe fires
`universe_only` (its own role Forms, no narrative genre ground).

CARDINAL (docs/DOMAIN_INSTRUMENT_METHOD.md): if the read ABSTAINS on real prose, that is a
centroid-REGISTRATION gap in the universe `.index` trigger column — calibrate the centroids, NEVER
author the input to make roles fire. "0 patterns" is honest abstention ONLY once the emitted role
verbs are proven reachable to the registered class centroids.
"""

from __future__ import annotations

import os
from collections.abc import Iterable, Mapping
from pathlib import Path

from homeostat.event import Event
from homeostat.story import render_story

# The self-contained mechanism universe (authored role Forms + class-centroid .index), at the repo
# root: src/homeostat/coherence.py -> parents[2] == repo root.
MECHANISM_UNIVERSE = Path(__file__).resolve().parents[2] / "universes" / "mechanism"


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


def coherence_from_regenesis(
    events: Iterable[Event], universe_root: str | os.PathLike[str] = MECHANISM_UNIVERSE
) -> dict[str, float]:
    """Fire the SCOPED story through Regenesis ONCE -> per-candidate SEMANTIC coherence for
    `drive(coherence=)`. The IMPURE shell over the pinned `coherence_from_patterns`; the caller
    SCOPES which events to hand in (story.render_story renders what it is given).

    Renders the events to opaque-SVO prose + sidecar, constructs the mechanism Universe
    (`universe_only`: the domain's role Forms, no narrative ground — replicating Regenesis's own
    `_universe` construction: a missing genres.index is a path that is never read under
    universe_only), fires `understand(kind='text')` (universe-aware GSE emit -> the role Forms), and
    reads the recognized patterns. The Regenesis engine is imported LAZILY so this self-contained
    package degrades to the structural default when the engine is absent (ImportError propagates to
    the caller, which falls back to `drive`'s proximity coherence).

    CARDINAL: an ABSTAINED read (`out["abstained"]`, i.e. no patterns) on real prose is a
    centroid-registration gap — calibrate the universe `.index`, NEVER author the input. Returns {}
    on abstention (no semantic signal), which the ranker treats as neutral.
    """
    from regenesis.instrument import understand
    from regenesis.library import Universe

    text, sidecar = render_story(events)
    root = os.fspath(universe_root)
    universe = Universe(
        root,
        os.path.join(root, "genres.index"),  # path only; unread under universe_only
        os.path.join(root, "archetypes.index"),  # the registered role-Form class centroids
        "NARRATIVE",
        True,  # universe_only: fire ONLY the domain's role Forms
    )
    out = understand(text, universe=universe, kind="text")
    return coherence_from_patterns(out.get("patterns", []), sidecar)
