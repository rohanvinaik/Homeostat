"""homeostat.render — the read as a human-readable STORY (the machine's CALL in the interface).

`driver.drive` / `person.read_person` compute a `DriverRead`, but nothing surfaces it; this is the
other half of the operator/computer interface — the precise CALL the operator answers next turn.
Story-led (the answer IS a story, not a ranked gene): the narrative account FIRST — a Dr. House read
in the same language that reads Shakespeare (Winston's thesis made tangible) — then WHAT REMAINS and
how-solved (the σ_sem completeness), then MY QUESTION (the mechanism-level Jeeves counter-ask), the
treatment, and WHAT the operator's own hypotheses got right.

Pure: `render(read) -> str`, judgment-free orchestration over pinned phrase-decisions. The decidable
sub-decisions (verb → Polti situation, genre verdict → clause, verdict → headline, outcome →
phrase) are total string functions, Detective-pinned; the assembly is intent-tested (a
`DriverRead` is a domain object with no `--input` form). Reuses `narrative.genre_triples`
so the dramatic account is READ, never re-derived.
"""

from __future__ import annotations

from homeostat.driver import DriverRead
from homeostat.narrative import genre_triples

_DRAMATIC = {"harm": "pursuit", "betray": "revenge", "seize": "obtaining", "pursue": "pursuit"}


def _entities(entities: frozenset[str]) -> str:
    """A cluster's entity set → a stable ``{A, B, C}`` string (sorted for determinism). Pure."""
    return "{" + ", ".join(sorted(entities)) + "}"


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


def verdict_clause(verdict: str, survivors: int) -> str:
    """The WHAT-REMAINS headline for a clinical verdict. Named codes: RESOLVED (one mechanism),
    BOTTOM (certified ⊥, a proof of non-membership), DEGENERATE (self-confirming, σ_sem=0), ASK (a
    plurality remains — a measurement is owed), ABSTAIN (no dimension separates). Pure over str/int.
    """
    if verdict == "RESOLVED":
        return "Resolved to a single mechanism — the structure explains this shadow."
    if verdict == "BOTTOM":
        return (
            "Certified ⊥: no lawful mechanism in the relevant sources explains this shadow "
            "(a proof, not a failed search)."
        )
    if verdict == "DEGENERATE":
        return "Degenerate: the read is self-confirming — nothing was falsified (σ_sem = 0)."
    if verdict == "ASK":
        return f"{survivors} mechanisms fit this story equally; I cannot yet separate them."
    return "Abstained: no available dimension separates the mechanisms that remain."


def render(read: DriverRead) -> str:
    """A `DriverRead` → a story-led, human-readable report (the machine's CALL). Judgment-free
    orchestration over the pinned phrase-decisions above + the read's own computed structure — it
    adds no biology and makes no ranking of its own. Five sections, each omitted when it has nothing
    to say: THE STORY (the genres + the Regenesis dramatic account), WHAT REMAINS (verdict +
    how-solved + the ranked mechanisms), MY QUESTION (the counter-ask, when a measurement is owed),
    TREATMENT (laments), WHAT YOU GOT RIGHT (the ledger). Intent-tested (domain-object input).
    """
    lines: list[str] = []

    # --- THE STORY (tier-1 genres + tier-2 dramatic account) ---
    story = read.story
    beats: list[str] = []
    for t in story.genres.get("tragedy", []):
        if t.verdict in ("doomed", "suppressed"):
            beats.append(tragedy_clause(t.origin, t.sink, t.verdict))
    for c in story.genres.get("comedy", []):
        if c.verdict in ("vicious", "homeostatic"):
            beats.append(comedy_clause(c.a, c.b, c.verdict))
    for q in story.genres.get("quest", []):
        if q.verdict in ("resolving", "entangling"):
            beats.append(quest_clause(q.hero, list(q.joined), q.verdict))
    for f in story.genres.get("allegory", []):
        if f.verdict == "fungible":
            beats.append(allegory_clause(f.a, f.b, f.verdict, f.banks))

    lines.append("THE STORY")
    if beats:
        lines.extend(f"  {b}" for b in beats)
        triples = genre_triples(story.genres)
        if triples and story.account is not None:
            situations = " + ".join(dict.fromkeys(dramatic_situation(v) for _, v, _ in triples))
            lines.append(f"  (read through the same engine that reads Macbeth: {situations})")
    else:
        lines.append("  The dynamics are quiet — no genre fired an opinionated verdict here.")

    # --- WHAT REMAINS (verdict + how-solved + the ranked mechanisms) ---
    pct = round(read.completeness.resolved * 100)
    lines.append("")
    lines.append(f"WHAT REMAINS  —  how solved: {pct}%")
    lines.append(f"  {verdict_clause(read.verdict, len(read.ranked))}")
    for cluster, score in read.ranked:
        lines.append(f"    · {_entities(cluster.entities)}   {score:.2f}")

    # --- MY QUESTION (the counter-ask, when a measurement is owed) ---
    if read.completeness.i_solve is not None:
        lines.append("")
        lines.append("MY QUESTION TO YOU  (the counter-ask)")
        lines.append(
            f"  Measure {read.completeness.i_solve} — its value distinguishes the mechanisms that"
        )
        lines.append("  remain. Tell me, and the story resolves.")
    elif read.probe is not None:
        lines.append("")
        lines.append("MY QUESTION TO YOU  (the counter-ask)")
        verb = "confirm" if read.probe.kind == "confirm" else "rule out"
        lines.append(f"  Measure {read.probe.dimension} — to {verb} the surviving candidates.")

    # --- TREATMENT (the laments) ---
    if story.treatment:
        lines.append("")
        lines.append("TREATMENT")
        for lam in story.treatment:
            lines.append(f"  {lament_clause(lam.mourned, lam.substitute, lam.verdict)}")

    # --- WHAT YOU GOT RIGHT (the operator ledger) ---
    if read.operator:
        lines.append("")
        lines.append("WHAT YOU GOT RIGHT")
        for h in read.operator:
            lines.append(f"  {outcome_clause(h.subject, h.verb, h.target, h.outcome)}")

    return "\n".join(lines)
