"""homeostat.render — the read as a human-readable hypothesis set (the machine's CALL).

`driver.drive` / `person.read_person` compute a `DriverRead`; this surfaces it as the operator's
half of the call-and-response, in the shape of Detective's minimal CLI: a legible, ranked, BOUNDED
set of candidate MECHANISMS (not a wall of every genre instance), each a short story over the genes
it spans, then the one measurement that would separate the leaders. Mechanistic reads and hypotheses
-- generative, reasoned-over, falsifiable -- never a claim of idempotent proof.

Story-led: each candidate is told through its genre reads (a Dr. House read in the language that
reads Shakespeare). Pure `render(read) -> str`, judgment-free orchestration; a candidate is shown
only if it EXPLAINS part of the shadow (score > 0, the reachability gate), top-K -- so the signal
the engine computed is not drowned in a wall of genre instances.
"""

from __future__ import annotations

from homeostat.clinic import ASK, BOTTOM, DEGENERATE, RESOLVED
from homeostat.driver import DriverRead
from homeostat.narrative import genre_triples

_DRAMATIC = {"harm": "pursuit", "betray": "revenge", "seize": "obtaining", "pursue": "pursuit"}
_TOP_K = 6  # candidates shown in full; the rest are counted, not dumped
_BEATS = 2  # story beats shown per candidate


def _entities(entities: frozenset[str]) -> str:
    """A cluster's entity set → a stable ``{A, B, C}`` string (sorted; elided past 8). Pure."""
    genes = sorted(entities)
    shown = ", ".join(genes[:8]) + (", …" if len(genes) > 8 else "")
    return "{" + shown + "}"


def dramatic_situation(verb: str) -> str:
    """The Polti dramatic situation a narrative verb names (`narrative.py`'s linkage, read for
    prose): ``harm``/``pursue`` → "pursuit", ``betray`` → "revenge", ``seize`` → "obtaining". An
    unmapped verb is returned verbatim (the honest fallback). Pure over str.
    """
    return _DRAMATIC.get(verb, verb)


def tragedy_clause(origin: str, sink: str, verdict: str) -> str:
    """One tragedy instance → a prose sentence. ``doomed``/``suppressed`` are opinionated (a real
    cascade to a locked sink); anything else abstains (the informational zero). Pure over str.
    """
    if verdict == "doomed":
        return f"A tragedy: {origin} drives an unstoppable cascade to a doomed sink at {sink}."
    if verdict == "suppressed":
        return f"A tragedy: {origin} drives {sink} down into a suppressed, locked-off sink."
    return f"An indeterminate arc from {origin} to {sink}: its paths disagree, so no doom holds."


def comedy_clause(a: str, b: str, verdict: str) -> str:
    """One comedy (mutual-regulation cycle) → a prose sentence. ``vicious`` is the pathological
    reinforcing loop; ``homeostatic`` the benign self-correcting one; else abstains. Pure over str.
    """
    if verdict == "vicious":
        return (
            f"A vicious comedy: {a} and {b} lock into a mutual-regulation loop turned pathological."
        )
    if verdict == "homeostatic":
        return f"A homeostatic comedy: {a} and {b} hold each other in check — self-correcting."
    return f"An indeterminate loop between {a} and {b}: the loop-gain sign does not settle."


def quest_clause(hero: str, joined: list[str], verdict: str) -> str:
    """One epic quest → a prose sentence. ``resolving`` is a coherent distant cure (the hero bridges
    the parts); ``entangling`` couples them without locking; else abstains. Pure over str/list/str.
    """
    parts = ", ".join(joined)
    if verdict == "resolving":
        return f"A resolving quest: {hero} reaches across to {parts} — a coherent distant cure."
    if verdict == "entangling":
        return f"An entangling quest: {hero} couples {parts}, but they never lock into a cure."
    return f"An indeterminate quest: {hero} touches {parts} with no coherence axis to resolve."


def allegory_clause(a: str, b: str, verdict: str, banks: int) -> str:
    """One allegory (fungibility) → a prose sentence. ``fungible`` is earned role-equivalence (≥2
    banks); other verdicts are unearned and abstain from the story (they feed treatment). str/int.
    """
    if verdict == "fungible":
        return f"An allegory: {a} and {b} are role-fungible — {banks} banks converge."
    return f"A resemblance between {a} and {b} that {banks} bank(s) did not confirm as fungible."


def lament_clause(mourned: str, substitute: str | None, verdict: str) -> str:
    """One treatment-tier lament → a prose sentence. ``substituted`` routes around the lost function
    with a fungible stand-in; ``palliative`` recognizes an irreplaceable loss. Pure over str/None.
    """
    if verdict == "substituted" and substitute is not None:
        return f"Route around the lost {mourned}: {substitute} can hold its role."
    return f"No stand-in for {mourned}: recognize the loss and manage a structured decline."


def outcome_clause(subject: str, verb: str, target: str, outcome: str) -> str:
    """One operator hypothesis outcome → a prose sentence. ``confirmed`` the shadow bears it out,
    ``contradicted`` it opposes, ``standing`` it is untestable on this shadow. Pure over str.
    """
    edge = f"{subject} {verb} {target}"
    if outcome == "confirmed":
        return f"Your hypothesis that {edge} — the shadow confirms it."
    if outcome == "contradicted":
        return f"Your hypothesis that {edge} — the shadow contradicts it; it falls out."
    return f"Your hypothesis that {edge} — untestable on this shadow (it stands, unjudged)."


def verdict_clause(verdict: str, candidates: int) -> str:
    """The one-line read headline for a clinical verdict (the clinic CODE values, LOWERCASE).
    RESOLVED (one mechanism), BOTTOM (certified ⊥, a proof of non-membership), DEGENERATE (self-
    confirming, σ_sem=0), ASK (a plurality a measurement separates), else ABSTAIN (a plurality, none
    yet separable). `candidates` = the count of shadow-explaining mechanisms. Pure over str/int.
    """
    plural = "s" if candidates != 1 else ""
    if verdict == RESOLVED:
        return "resolved to a single mechanism."
    if verdict == BOTTOM:
        return "certified ⊥ — nothing in scope explains the presentation (a proof)."
    if verdict == DEGENERATE:
        return "degenerate — self-confirming; nothing was falsified."
    if verdict == ASK:
        return f"{candidates} candidate mechanism{plural} fit; a measurement separates them."
    return f"{candidates} candidate mechanism{plural} fit; none yet separable."


def _cluster_beats(members: tuple) -> list[str]:
    """A candidate cluster's own story: its member ``(genre, instance)`` reads rendered to clauses,
    opinionated verdicts only (the rest abstain from the story). Pure over the members tuple.
    """
    beats: list[str] = []
    for genre, inst in members:
        if genre == "tragedy" and inst.verdict in ("doomed", "suppressed"):
            beats.append(tragedy_clause(inst.origin, inst.sink, inst.verdict))
        elif genre == "comedy" and inst.verdict in ("vicious", "homeostatic"):
            beats.append(comedy_clause(inst.a, inst.b, inst.verdict))
        elif genre == "quest" and inst.verdict in ("resolving", "entangling"):
            beats.append(quest_clause(inst.hero, list(inst.joined), inst.verdict))
        elif genre == "allegory" and inst.verdict == "fungible":
            beats.append(allegory_clause(inst.a, inst.b, inst.verdict, inst.banks))
    return beats


def render(read: DriverRead) -> str:
    """A `DriverRead` → a story-led, BOUNDED hypothesis set (the machine's CALL). Judgment-free
    orchestration over the pinned phrase-decisions + the read's own structure. Sections, omitted
    when empty: THE READ (verdict headline), CANDIDATE MECHANISMS (shadow-explaining clusters,
    score > 0, top-K, each with genes + story), WHAT I CAN'T YET TELL (the counter-ask), TREATMENT
    (laments), WHAT YOU GOT RIGHT (the ledger). Intent-tested (domain-object input).
    """
    lines: list[str] = []
    candidates = [(cl, sc) for cl, sc in read.ranked if sc > 0.0]
    lines.append(f"THE READ  —  {verdict_clause(read.verdict, len(candidates))}")

    if candidates:
        lines.append("")
        lines.append("CANDIDATE MECHANISMS  (ranked by how much of the presentation each explains)")
        for i, (cl, _sc) in enumerate(candidates[:_TOP_K], 1):
            lines.append(f"  {i}. {_entities(cl.entities)}")
            for beat in _cluster_beats(cl.members)[:_BEATS]:
                lines.append(f"       {beat}")
        extra = len(candidates) - _TOP_K
        if extra > 0:
            lines.append(f"  … and {extra} more that partially explain the presentation.")
        triples = genre_triples(read.story.genres)
        if triples and read.story.account is not None:
            sits = " + ".join(dict.fromkeys(dramatic_situation(v) for _, v, _ in triples))
            lines.append(f"  (read through the same engine that reads Macbeth: {sits})")

    if read.completeness.i_solve is not None:
        lines.append("")
        lines.append("WHAT I CAN'T YET TELL  —  and the measurement that would")
        lines.append(f"  Measure {read.completeness.i_solve}; it separates the leading candidates.")
    elif read.probe is not None:
        lines.append("")
        lines.append("WHAT I CAN'T YET TELL  —  and the measurement that would")
        verb = "confirm" if read.probe.kind == "confirm" else "rule out"
        lines.append(f"  Measure {read.probe.dimension} — to {verb} the surviving candidates.")

    if read.story.treatment:
        lines.append("")
        lines.append("TREATMENT")
        for lam in read.story.treatment:
            lines.append(f"  {lament_clause(lam.mourned, lam.substitute, lam.verdict)}")

    if read.operator:
        lines.append("")
        lines.append("WHAT YOU GOT RIGHT")
        for h in read.operator:
            lines.append(f"  {outcome_clause(h.subject, h.verb, h.target, h.outcome)}")

    return "\n".join(lines)
