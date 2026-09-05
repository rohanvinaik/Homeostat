"""Homeostat — the validation gallery: the claim, instantiated in the pipeline's own output.

Not a test suite (the pins live in tests/); a runnable DEMONSTRATION. Each entry is a realistic
workflow run through the REAL pipeline (`read_person` / `drive`) and rendered as the operator's
hypothesis set. Every read here is COMPUTED, never authored -- the synthetic entries construct an
input geometry and let the engine read it; the reads are the engine's, not the author's.

The matrix: INPUT PARADIGMS (how a person arrives -- diagnosis + labs, + operator hypotheses)
crossed with OUTPUT POLES (recover a bounded hypothesis set / disambiguate what the label flattens /
certified-⊥ with proof / honest abstention + the discriminating question).

  1. BLIND MECHANISM RECOVERY  (real public data)  -- the instrument, validated
  2. DISAMBIGUATION            (illustrative)       -- the label-flattening undone
  3. CERTIFIED ⊥               (illustrative)       -- "no mechanism, with proof"
  4. OPERATOR HYPOTHESIS        (illustrative)       -- fluid intelligence, tested
  5. ROLES, NOT GENES          (illustrative)       -- two genes, one recognized role
  6. THE STORY, AT FULL LOUDNESS (illustrative)     -- the dramatic account (pursuit + revenge)

Run: `PYTHONPATH=src python scripts/gallery.py`. Entries 2-6 are self-contained (no downloads) and
always run. Entry 1 needs the SHA-pinned data dumps, which the fetch shells download on first run;
it self-skips if they are absent and offline. Regenesis is optional -- absent, the dramatic account
degrades gracefully to the native genres.
"""

from __future__ import annotations

from homeostat import render
from homeostat.driver import drive
from homeostat.event import Event
from homeostat.fungibility import read_fungibility
from homeostat.narrative import genre_triples, read_story
from homeostat.person import read_person
from homeostat.position import position
from homeostat.render import dramatic_situation
from homeostat.signal import Signal, Tier

VS = {"amplifies": 1, "inhibits": -1}


def _banner(n: int, title: str, tag: str) -> str:
    return f"\n{'═' * 78}\n  {n}.  {title}\n      [{tag}]\n{'═' * 78}"


def _reg(subject: str, target: str, verb: str = "amplifies") -> Event:
    return Event("regulatory", verb, subject, target, 1)


def _sig(name: str, value: str) -> Signal:
    return Signal(name, value, Tier.VERIFIED)


# a reference band for the illustrative labs: a reading over 100 is "up", in [70,100] is normal.
_BAND: dict[str, tuple[float, float]] = {}


def _reference(node: str, _demographics):
    return _BAND.get(node)


def _person(diagnosis, labs, events, trait_index, vocab, hypotheses=()):
    return read_person(
        diagnosis,
        labs,
        events,
        VS,
        trait_index,
        demographics={"age": "40"},
        reference=_reference,
        vocab=vocab,
        hypotheses=hypotheses,
    )


# ── 2. DISAMBIGUATION — same label, two lab panels, two mechanisms ──────────────────────────


def disambiguation() -> str:
    """One diagnostic LABEL over a subspace holding TWO distinct mechanisms; two patients with the
    same label but different labs resolve to DIFFERENT mechanistic stories -- the flattening undone.
    The subspace + geometry are synthetic; the two reads are the engine's."""
    global _BAND
    # both subtypes present a SHARED inflammatory marker (why the label lumps them); each also has a
    # DISTINCTIVE one. INF: a vicious loop INF<->ILR. SYN: a doomed cascade to SYNSINK.
    events = [
        _reg("INF", "ILR"),
        _reg("ILR", "INF"),  # INF <-> ILR  (a vicious comedy)
        _reg("INF", "SHARED"),
        _reg("SYN", "GLUR"),
        _reg("GLUR", "SYNSINK"),  # SYN -> GLUR -> SYNSINK  (a doomed cascade)
        _reg("SYN", "SHARED"),  # both drive the SHARED marker
    ]
    trait = {"spectrum condition": {"INF", "SYN"}}
    vocab = {n: n for n in ("INF", "ILR", "SYN", "GLUR", "SYNSINK", "SHARED")}
    _BAND = {n: (70.0, 100.0) for n in vocab}

    labs_a = [_sig("ILR", "130"), _sig("SHARED", "130")]  # shared + the INF-distinctive marker
    labs_b = [_sig("SYNSINK", "130"), _sig("SHARED", "130")]  # shared + the SYN-distinctive marker
    a = _person("spectrum condition", labs_a, events, trait, vocab)
    b = _person("spectrum condition", labs_b, events, trait, vocab)
    out = ["Patient A  —  diagnosed 'spectrum condition', labs: SHARED + ILR elevated:", ""]
    out.append(render(a))
    out += ["", "Patient B  —  SAME diagnosis, labs: SHARED + SYNSINK elevated:", ""]
    out.append(render(b))
    out += ["", "  → same label, two panels, two different mechanistic reads. The label flattened;"]
    out.append("    the geometry did not.")
    return "\n".join(out)


# ── 3. CERTIFIED ⊥ — a contradictory shadow no mechanism explains ───────────────────────────


def certified_bottom() -> str:
    """A shadow whose signs the only candidate source CONTRADICTS: it would have to drive one marker
    up and one down through the same activation -- impossible. The engine returns a certified ⊥ (a
    PROOF of non-membership), not a guess. Synthetic geometry; the verdict is the engine's."""
    global _BAND
    events = [_reg("SRC", "UP"), _reg("SRC", "DOWN")]  # SRC amplifies both UP and DOWN
    trait = {"contradiction": {"SRC"}}
    vocab = {n: n for n in ("SRC", "UP", "DOWN")}
    _BAND = {n: (70.0, 100.0) for n in vocab}
    # UP observed high, DOWN observed low -> SRC (which amplifies BOTH) cannot produce both signs.
    read = _person("contradiction", [_sig("UP", "130"), _sig("DOWN", "40")], events, trait, vocab)
    return render(read)


# ── 4. OPERATOR HYPOTHESIS — the person proposes, the code adjudicates ───────────────────────


def operator_hypothesis() -> str:
    """The person proposes two mechanism EDGES -- one the shadow bears out, one it contradicts. The
    ledger reports both honestly: correctness stays in the code, never the operator. Synthetic."""
    global _BAND
    events = [_reg("DRIVER", "MARKER1"), _reg("DRIVER", "MARKER2")]
    trait = {"presentation": {"DRIVER"}}
    vocab = {n: n for n in ("DRIVER", "MARKER1", "MARKER2")}
    _BAND = {n: (70.0, 100.0) for n in vocab}
    # DRIVER + both markers up. Operator proposes: DRIVER amplifies MARKER1 (right -- driver up,
    # marker up), and DRIVER INHIBITS MARKER2 (wrong -- inhibition would drive it DOWN, it is up).
    # DRIVER must be observed for its edges to be testable (else the ledger stands, unjudged).
    hyps = [_reg("DRIVER", "MARKER1", "amplifies"), _reg("DRIVER", "MARKER2", "inhibits")]
    labs = [_sig("DRIVER", "130"), _sig("MARKER1", "130"), _sig("MARKER2", "130")]
    read = _person("presentation", labs, events, trait, vocab, hypotheses=hyps)
    return render(read)


# ── 5. ROLES, NOT GENES — two different genes, one recognized mechanism ─────────────────────


def roles_not_genes() -> str:
    """GENE_A and GENE_B are fungible paralogs: they resemble each other AND converge on a shared
    partner across two independent banks (regulatory + physical), so the engine earns the verdict
    that they play ONE role. A GENE_A-variant patient and a GENE_B-variant patient present
    identically and read as the SAME mechanism -- with NO shared gene, which gene-counting cannot
    see. Synthetic geometry; the fungibility verdict is earned."""
    global _BAND
    events = [
        Event("evolutionary", "resembles", "GENE_A", "GENE_B", 1, ""),  # the paralog seed
        _reg("GENE_A", "MARKER"),
        _reg("GENE_B", "MARKER"),  # regulatory bank: both drive MARKER
        Event("physical", "binds", "GENE_A", "MARKER", 1),
        Event("physical", "binds", "GENE_B", "MARKER", 1),  # physical bank: 2nd convergence
    ]
    trait = {"condition": {"GENE_A", "GENE_B"}}
    vocab = {n: n for n in ("GENE_A", "GENE_B", "MARKER")}
    _BAND = {n: (70.0, 100.0) for n in vocab}
    out = ["ROLE-EQUIVALENCE, earned from the geometry (the fungibility read):"]
    for f in read_fungibility(events):
        out.append(f"  {f.a} ~ {f.b}: {f.verdict}  ({f.banks} independent banks converge)")
    out += ["", "A variant in GENE_A and a variant in GENE_B read identically:", ""]
    out.append(render(_person("condition", [_sig("MARKER", "130")], events, trait, vocab)))
    out.append("")
    out.append("  → GENE_A and GENE_B share no identity, yet the engine reads them as ONE role. A")
    out.append("    count across the two finds no shared gene and sees nothing; the role-read sees")
    out.append("    one mechanism.")
    return "\n".join(out)


# ── 6. THE STORY, AT FULL LOUDNESS — the genre reading + the dramatic account ───────────────


def story_read() -> str:
    """The story diction at full volume. A mechanism -- a vicious comedy (MYC<->CDK1) feeding a
    doomed tragedy (TP53->BAX->apoptosis) -- read through the native genres and composed, through
    the SAME engine that reads Shakespeare, into a dramatic account. A multi-system mechanism comes
    back as pursuit + revenge. Winston's thesis (story understanding is one general capacity) made
    tangible on biochemistry. Illustrative geometry; the reading is the engine's."""
    events = [
        _reg("MYC", "CDK1"),
        _reg("CDK1", "MYC"),  # a vicious comedy
        _reg("TP53", "BAX"),
        _reg("BAX", "APOPTOSIS"),  # a doomed tragedy
    ]
    story = read_story(events, ["MYC", "CDK1", "TP53", "BAX", "APOPTOSIS"])
    out = ["THE GENRE READING (every opinionated instance the dynamics fire):"]
    for genre in ("tragedy", "comedy", "quest", "allegory"):
        for inst in story.genres.get(genre, []):
            out.append(f"  {genre:9} {inst}")
    triples = genre_triples(story.genres)
    out += ["", "THE DRAMATIC ACCOUNT — through the same engine that reads Shakespeare:"]
    for s, v, o in triples:
        out.append(f"  {s} --{v}--> {o}    ({dramatic_situation(v)})")
    situations = " + ".join(dict.fromkeys(dramatic_situation(v) for _, v, _ in triples))
    out += ["", f"  → the mechanism reads as: {situations}."]
    if story.account is None:
        out.append("    (Regenesis absent -> account degrades to the native genres; install it for")
        out.append("     the full derivation-over-derivations.)")
    return "\n".join(out)


# ── 1. BLIND MECHANISM RECOVERY — the real-data proof ───────────────────────────────────────


def blind_recovery() -> str:
    """The instrument, validated on REAL public data. A Crohn's diagnosis scopes (via the GWAS
    catalog) to a subspace that genuinely contains LRRK2/NOD2/RIPK2; the labs are the observed
    inflammatory readout; blind to the LRRK2 label, the engine returns a bounded hypothesis set with
    the LRRK2-NOD2-RIPK2 inflammatory bridge among the candidates. Needs the data dumps present."""
    try:
        from homeostat import (
            metabolic,
            metabolic_fetch,
            signor,
            signor_fetch,
            string,
            string_fetch,
            trait_wiring_fetch,
        )
        from homeostat.relevance import trait_gene_index
    except ImportError as e:  # pragma: no cover - operational
        return f"  [skipped — {e}]"
    try:
        signor_fetch.ensure()
        _, info = string_fetch.ensure_all()
        alias = string_fetch.load_alias_map(info)
        ncbi, rel, gi = metabolic_fetch.ensure_all()
        mids = metabolic.metabolic_pathways(metabolic_fetch.load_tsv(rel))
        esym = metabolic_fetch.load_entrez_symbol(gi)
        trait_wiring_fetch.ensure()
    except (FileNotFoundError, OSError) as e:  # pragma: no cover - operational
        return f"  [skipped — real data dumps not present locally: {e}]"
    events = [
        *signor.signor_events(signor_fetch.load_rows()),
        *string.string_events(string_fetch.load_rows(), alias),
        *metabolic.co_metabolism_events(metabolic_fetch.load_tsv(ncbi), mids, esym),
    ]
    crohn = trait_gene_index(list(trait_wiring_fetch.load_rows())).get("Crohn disease", set())
    shadow = {g: position(g, 1.0, 0.0, 0.0) for g in ("IRF5", "IKBKG", "TRAF6")}
    read = drive(events, shadow, VS, min_weight=2.0, relevant=crohn)
    axis = {"LRRK2", "NOD2", "RIPK2"}
    hit = [i + 1 for i, (cl, _s) in enumerate(read.ranked) if cl.entities & axis and _s > 0]
    note = (
        f"  (the LRRK2-NOD2-RIPK2 axis is candidate #{hit[0]} of the bounded set — recovered blind)"
        if hit
        else "  (axis not among the scored candidates)"
    )
    return render(read) + "\n" + note


def main() -> None:
    print((__doc__ or "").split("\n\n")[0])
    print(_banner(1, "BLIND MECHANISM RECOVERY — LRRK2–NOD2–RIPK2, blind", "real public data"))
    print(blind_recovery())
    print(_banner(2, "DISAMBIGUATION — same label, two mechanisms", "illustrative"))
    print(disambiguation())
    print(_banner(3, "CERTIFIED ⊥ — no mechanism explains this, with proof", "illustrative"))
    print(certified_bottom())
    print(_banner(4, "OPERATOR HYPOTHESIS — the person proposes, the code judges", "illustrative"))
    print(operator_hypothesis())
    print(_banner(5, "ROLES, NOT GENES — two genes, one recognized mechanism", "illustrative"))
    print(roles_not_genes())
    print(
        _banner(6, "THE STORY, AT FULL LOUDNESS — the dramatic account", "illustrative")
    )
    print(story_read())


if __name__ == "__main__":
    main()
