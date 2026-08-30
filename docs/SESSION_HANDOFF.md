# PRE-COMPACT HANDOFF — Homeostat, 2026-08-30

*Written to the discipline of `compaction_drift_overconfidence_notes.md` (all three
notes). This session's failure was **Note 3 — method substitution**: with the design
in front of me I substituted my fluent statistical default for the data-geometry method
the design specifies, and never noticed, because a statistical pipeline is something I
build competently and it produced running results. Note 3's fix is the ONE NEXT ACTION
below. This handoff is structured (not a story), states the next action as one
imperative (not an open question), attaches the WHY to each constraint, preserves the
founder's own words verbatim, and points LOUDLY at the sources that can contradict it —
because the summary is not the truth; the sources are.*

---

## ★ READ THESE IN FULL, LITERALLY, BEFORE ANYTHING ELSE — no workaround, no substitute

**Read every line of every file below. Do NOT grep it. Do NOT skim it. Do NOT read the
first N lines. Do NOT read a summary of it (including any summary I wrote). Do NOT tell
yourself "I recall the key points" or "reading the relevant section is equivalent." It
is NOT equivalent, and substituting a workaround for a literal full read is the exact
move that caused this whole session's failure. Open each file and read it top to
bottom.**

1. `~/Projects/Homeostat/CLAUDE.md` — the auto-loaded laws (rewritten 2026-08-30). LAW 1
   = DATA-GEOMETRY, NOT STATISTICS.
2. `~/Projects/Homeostat/AGENTS.md` — the gate (rewritten 2026-08-30).
3. `~/Projects/Homeostat/docs/THEORY_OF_THE_CASE.md` — the derived design + **Part V,
   the pathology record of this session's four statistical probes**.
4. `~/Projects/Homeostat/docs/REGULATORY_DEFICIT_PROGRAM.md` — the founding canon,
   verbatim, authoritative. Every line, including Appendix C.
5. `~/Projects/Kaggle_Killer/DATA_GEOMETRY_ARCHITECTURE.md` — the founder's ACTUAL
   architecture this project instantiates (OTP, Informational Zero, COEC, GSE, HDC). The
   1050-line file, in full — this is the positive content of "data geometry."
6. `~/Projects/rohan-vinaik.github.io/papers/Core Documents/AI_architecture_papers/compaction_drift_overconfidence_notes.md`
   — the three drift notes. Note 3 (method substitution) is this session's failure mode.
7. `~/Projects/Regenesis/docs/SIGNIFICANCE_WEIGHTING.md` — the κ / significance-weighting
   machinery (canon Appendix B; the coherence measure, "surprise = −log P turned
   inward"). The one genuinely data-geometry piece already ported (`src/homeostat/kappa.py`).
8. The **"SDIS" grounding document** — the founder's own attempt to grope toward the
   mechanism with a built-in prior (named in their words below). **Location unknown to
   me; FIND IT before designing** (likely under `~/Projects/AuDHD_Correlation_Study` or
   the papers dir; ask the founder if not found). Do not proceed as if it doesn't exist.

---

## ★ THE FOUNDER'S OWN WORDS — the theory, verbatim (do NOT paraphrase these away)

*Preserved literally because my paraphrase is where the drift re-enters. Read these as
the specification. Two messages, 2026-08-30:*

> "The framing is off, both on a smaller detail and of the actual motivating conception
>
> I have no reason to reject studying the initiation of inflammation. Why? Sure, we know
> SOME of what causes inflammation, but the whole point of the "sub-threshold" stuff is
> that the actual mechanism that feeds into the presentation of inflammation, or a
> multifactorial condition like ADHD, might be far more complex than the surface level,
> full-blast statistical metric might otherwise show. Sure, there are the literal
> dopamine synthesis and uptake genes, ones that define neurons and their
> activity/signaling cascade. Those are obvious, and basic bioinformatics and genetics
> has already found them. The point here is to stop letting the signal there become
> noise that drowns out *other* eitiologies. For example, we KNOW there's a connection
> between autism and ADHD. The "SDIS" grounding document was my attempt to grope towards
> a mechanism with an in-built prior motivating my analysis. But the whole point of the
> project here is to *not* rely on statistics, but to use data geometry to find local
> points of entropic minima, information-theoretic coherence, so as to not simply find
> "gene X is found in 87% of people with condition Y", but using a systematic,
> mechanistic inferring data geometry pipeline to impute these sub-threshold signals
> that, in *combination* result in a phenotypic expression that is clinically
> significant (or not, but that's the obvious motivating benefit for why one would build
> this and study it). And it's why there was initial discussion of/inspiration from
> Ayurveda. Not "traditional good, allopathic bad", but to use the fact that traditional
> medicine generally, but also Ayurveda most specifically, is a battle-tested empirical
> approach to medicine that ends up addressing these mechanisms by definition, using
> time and empirical feedback to probe the etiology and impute the mechanism through raw
> data. The explanations for the mechanisms are generally a bit off and "woo"—"heat",
> "spirits", "energy"—but that doesn't really matter, because the "diagnosis", which is
> treated as a necessary prior in allopathic practice, is actually just a slapdash
> post-hoc, motivated meaning imposing stage. It's not the point, it's just a way of
> writing a story (in the Patrick Winston sense) for what medicine means as opposed to
> leaving it to a brittle set of mechanical rules. Makes sense?
>
> Smaller note, I don't know why you keep bringing up the "initiation vs switch off"
> stuff, I never said that, nor do I think it's true. Initiation is ALSO worth studying,
> regardless of the specific idiomatic presentation in me personally"

> "Damn it. I was worried about that. I don't know why your priors are SO heavily
> statistical. I hate statistics so much. It has its uses, but it's almost used these
> days as a cheap hack to actual engagement with a problem space.
>
> Please look into the "kaggle_killer" main directory setup, including the CLAUDE.md
> file located there. I had a similar problem that I worked to address. Learn from the
> lessons learned there, then use that to port over those guardrails into this
> directory. We don't have the context to do what we need, so I need you to introduce
> this system to prevent drift from the actual intended design. That'll probably also
> include some re-writing of the theory documentation to fully encode the actual theory
> … Once you do that, we basically have to rip out giant chunks of the project—most of
> the parts that aren't literally wiring—and rebuild it from scratch, using the session
> discipline. But that's for post-compact"

---

## ★ THE ONE NEXT ACTION (imperative — this IS Note 3's fix; do exactly this)

**Do NOT write any code. Do NOT resume any pipeline. FIRST, after literally reading the
files above, produce — in your OWN words, at the MECHANISM level — a restatement of (a)
the theory and (b) the exact data-flow of the method you propose, and hand it to the
founder to correct, on a conversational register.** Only after the founder confirms the
mechanism does the rip-and-rebuild begin.

- WHY own-words + mechanism-level (Note 3): a copy-paste proves nothing (I copied the
  right words while running the wrong model underneath). The lie hides one layer below
  the abstraction — I *did* believe "find coherent sub-threshold combinations," but the
  unexamined operation underneath was a statistic. The restatement must be forced down
  to *what is the geometric object, what coherence operation fires over it, what artifact
  it returns* — if the honest answer is "rank genes by a statistic," there is no
  data-geometry sentence to write, and the drift comes off.
- The test to run on your own restatement (Note 3, and the founder's phrasing of the
  gate): *where does the coherence-of-a-combination live, and where have I substituted a
  statistic for it?* If you cannot point at the geometry, you have not understood it yet.
- This is a CONVERSATION first, not a build. The founder said the rebuild is post-compact
  and that they will reason it out with you. Do NOT author the method solo.

## ★ FORBIDDEN (with WHY — the drift attractors, most-load-bearing first)

- **Reaching for ANY statistic as the method, the significance, or the object** —
  frequency, association, enrichment-vs-background, population-differentiation rank,
  network hub / participation score, p-value, pleiotropy count. WHY: this is THE drift.
  It was done 4× on 2026-08-30, each time feeling like rigor. Statistics is at most a
  cheap narrowing *prior*, never the method (CLAUDE.md LAW 1, auto-loads).
- **A workaround in place of a literal full read** of the files above. WHY: the founder
  named this explicitly as a repeated, annoying failure; and Note 3 says the abstraction
  is the camouflage — only full mechanism-level engagement catches the substitution.
- **Resuming `annotation-recovery`, `eir-enrich*`, `pbs-restricted`, `sig-descent`, or
  the participation `bridge-discovery`/`lrrk2-gate` as "the method."** WHY: they ARE the
  Part V pathology, preserved in git history as a record of the failure, not a design.
- **Building on the generic human interactome (STRING/GTEx) with no phenotype in the
  object.** WHY: it is a fixed, phenotype-free, person-free map; the gnomAD replication
  proved the population signal was inert in it (Part V, Act 2).
- **Editing the canon** (`REGULATORY_DEFICIT_PROGRAM.md`) or authoring the method solo.

## ★ RESOLVED — do NOT reopen (each with its reason)

1. The method is **data geometry (coherence of sub-threshold combinations), not
   statistics.** RESOLVED, load-bearing. A statistic is at most a cheap prior.
2. The phenotype is a **combination of sub-threshold signals; the loud statistical hits
   DROWN OUT the quiet coherent etiologies.** That drowning-out is the enemy the method
   exists to defeat. RESOLVED (founder's words, above).
3. A **diagnosis is a story** (Winston), not ground truth; **Ayurveda is a decorrelated,
   battle-tested carving-source**, a prior on combination, never an authority. RESOLVED.
4. The E/I/R **PBS pile is a search-order prior** (§7), not the candidate object. The old
   CLAUDE.md said otherwise — that was the poison, now fixed. RESOLVED.
5. **Initiation vs. resolution is NOT the axis** — the founder never said it, does not
   believe it; initiation is also worth studying. Drop it. RESOLVED (founder's words).

## ★ WHAT IS KEPT vs. RIPPED OUT (for the rebuild)

- **KEEP (wiring / substrate):** ingestion (`eir_cohort.py`, `gnomad_pile.py`, resumable
  downloads, `HOMEOSTAT_TAG` cohort-namespacing), `pbs.py` (as a *prior* computation
  only), `kappa.py` (the κ engine — the one genuinely data-geometry piece), GRCh37
  reference data, the lint/type/test/gate discipline.
- **RIP OUT (statistics wearing the method's clothes):** the gate/validator layer that
  treats the PBS pile as the object and participation/enrichment/pleiotropy as the
  significance. See `docs/THEORY_OF_THE_CASE.md` Part III for the explicit list.

## ★ RECONSTRUCTION TEST

From this alone, a fresh session must recover: (a) the method is **data-geometry
coherence of sub-threshold combinations, not statistics**; (b) the ONE next action is a
**mechanism-level own-words restatement handed to the founder, then a conversational
method design — NOT resuming any pipeline, NOT authoring solo**; (c) the forbidden set —
any statistic as the method, any workaround in place of a literal read, the four Part-V
pipelines as "design," the generic interactome as the object; (d) that it must
**literally read** the eight sources above, in full. If any is unclear, the sources
above ARE the truth — read them, do not reconstruct from this page.
