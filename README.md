# Homeostat

**A per-person engine that reads the single coupled *mechanism* underneath a set of symptoms — and
says, just as carefully, when there is no mechanism it can honestly find.** Named for Ashby's
homeostat, the machine that finds its own equilibrium, because the thing under study is regulation.

> Homeostat produces **hypotheses to interrogate, not diagnoses.** It is a research instrument, not a
> clinician; nothing here is medical advice. It is also honest about its own limits by construction —
> that honesty is the product, not a disclaimer on it.

---

## The person it is for

You have a handful of diagnoses that don't add up. A sleep problem, an attention problem, something
inflammatory the specialists keep renaming every visit. You can feel that they're connected — treat
one and another quietly eases; miss the thing that helps and three of them flare within days. You are,
as it happens, usually right about this: you have spent years watching the one system no one else has
continuous access to. What you *don't* have is a **mechanism** — the single coupled cause underneath —
that you could take to a doctor and test.

The system, meanwhile, usually can't give you one. Each specialist tunnels into their own organ and
returns an exotic, poor-fitting label — or a shrug. Not out of malice. Their main instrument is simply
pointed at a different object than the one you're describing.

## The object it's pointed at

Medicine reads an unwell person by **projection.** It collapses a very high-dimensional pattern of
deviations — hundreds of measurable quantities, each displaced from where it would sit in a
well-regulated version of *that same person* — onto a handful of named axes, the diagnostic criteria,
and counts how many cross a population threshold. Genetics finds causes the same way, by **counting**:
which variant appears more often in patients than in controls, `p < 5×10⁻⁸`.

For a clean single-cause disease, that works. But the projection is lossy in one specific, fatal way:
**it discards the combination.** A pattern that is *below threshold on every named axis on its own*,
yet coherent as a *joint* displacement, falls straight through — because the signal lives in the
correlations *between* the axes that the projection just flattened. The thing you're reporting is a
**shadow**: a coherent state that many weak, individually-unremarkable signals cast *in concert*,
stored in no single one of them.

Three things make that shadow invisible to a counting instrument, and each is **structural — not a
matter of sample size:**

- **Control is distributed.** A symptom sits at the end of a long, redundant pathway; no single step
  holds enough control for its failure to register on its own.
- **The parts are interchangeable.** One person breaks the pathway at step 12; another at step 30 with
  a different gene doing the same job; a third has a spare covering for the first. *Same mechanism
  every time, no shared gene* — so a count, which looks for a shared gene, finds nothing.
- **The state is dynamic.** The mechanism is a meta-stable balance that holds until enough of the
  coupling shifts and it tips — which is exactly why "treating one part makes another vanish."

A shadow cannot be found by inspecting light sources one at a time, at any sample size. More data does
not fix it. That is the whole problem in a sentence, and it is why a fragmented system of
single-specialty reads is *structurally* positioned never to see the thing you're reporting.

## So it reads a different object

Homeostat stops counting and recovers the **mechanism.** It treats the deviation pattern as a shadow
cast on a **prior web of biological couplings**, and asks the inverse question: *what single source,
reachable through the web, could cast exactly this shadow?* Then it **eliminates** — keeping a
candidate only if it positively reaches the observed deviations **and** is not ruled out by a
contradicting signal.

The reframe is one flat sentence: **significance is not how *common* a mechanism is — it is how much of
*this person's* shadow it explains.** Coverage of the shadow, not frequency in a population, is the
measure of "complete." That inversion is the whole idea.

## "But you're just making up a plausible story"

Here is the sharpest thing you can say against all of this, and it is worth saying plainly:

> *This is a machine that finds a plausible story in noise. Give it any symptoms and it hands you a
> confident mechanism. It's a Ouija board with a gene ontology — you cannot tell me it's **real**.*

That objection is correct about the failure mode, and it is the exact failure the entire design exists
to refuse. Four ways it survives the audit:

- **It abstains.** Feed it a thin or contradictory signal and it does not manufacture a story — it
  returns a **certified nothing**, "no mechanism the known biology can resolve explains this, *with a
  proof*," which is a categorically different object from "I didn't find one." A romanticism machine
  finds sacrifice in a grocery list; the refusal is the immune system against precisely that.
- **It hands you a falsifier, not a verdict.** The output is a *bounded, ranked set of candidate
  mechanisms* plus the single measurement that would separate or kill the leaders — a hypothesis space
  you can test, never "you have disease X."
- **It is deterministic and auditable.** There is no trained model — nothing to fit to the answer, no
  weights to hide a hallucination in. Every step traces back to the web, the eliminations, and the
  signals. You can read *why* each candidate is on the list.
- **It recovers mechanisms it was not told.** Given the public inflammatory-bowel gene set as a search
  space and a three-node inflammatory shadow — blind to the answer — it returns a bounded set of
  legible candidate mechanisms with the known **LRRK2–NOD2–RIPK2** inflammatory bridge among them.

The confabulation objection assumes a system that always answers. This one's defining move is knowing
when *not* to.

## What it actually does, once you trust it that far

Four moves make the read possible, and no other tool combines them:

1. **It reads roles, not genes.** The gene is the interchangeable part; the *role it plays* is the
   invariant. Two different genes filling the same role, in two different people, are recognized as the
   same mechanism — which is how it sees through the "no shared gene" problem that defeats counting.
2. **It triangulates across the geometries of biology.** No single free dataset shows a mechanism, so
   it reads several — how genes relate by regulation, physical binding, evolution, metabolism,
   co-expression — and trusts only what independent views *agree* on. Convergence is the signal; a
   claim only one view supports is dropped.
3. **It reasons in two signs.** It weighs not only what *could* explain the presentation but what is
   *ruled out*, and can return that certified "there is no mechanism here." Most systems have no way to
   say this at all.
4. **It reads the mechanism as a *story*.** A control system's *dynamics* are exactly what narrative
   structure captures — so the answer comes back not as a ranked gene but as a **tragedy** (a flaw
   driving a node to a locked doom), a **vicious comedy** (a cycle where every compensation compounds),
   an **allegory** (one role, different genes), or an **epic quest** (the roundabout cure, scored by
   Kuramoto phase-coherence: do the coupled loops lock into a resolution?). These are composed —
   *through the same story-understanding engine that reads Shakespeare* — into a presentation-level
   account, so a multi-system mechanism literally comes back as *pursuit + revenge + obtaining*. That
   is Winston's thesis — story understanding as one general intelligence capacity — made tangible on
   biochemistry. And it's the extraction the alternative-medicine traditions never managed: keep the
   cross-mechanistic dynamics-grammar, drop the woo. Calling a pathway a comedy reads its *mechanics*
   correctly while claiming nothing about purpose — imputing purpose stays the human's job.

The reasoning is **classical AI and data geometry — not statistics, and not a machine-learning model.**
There is nothing to train, and that is deliberate: the intelligence is in the correctness of the
geometry, not the size of a network. It runs on the compute of a moderately-large potato.

## What a reading looks like

Give it the deviation pattern; it returns one of four honest endings — never a label:

- **A ranked set of candidate mechanisms**, each read as a story over the genes it spans, with the one
  measurement that would narrow them. *"Here is the mechanism, here is what holds it together, here is
  how much of you it explains."*
- **The next question** — when candidates fit equally it does not guess; it names the single
  measurement that would separate them. The most powerful input it has is often one you already carry
  in your own history.
- **A certified nothing** — "no mechanism the known biology can resolve explains this," with the proof.
- **An honest abstention** — "I cannot separate these without a measurement you don't have."

You can watch all four on real and illustrative inputs in **[`scripts/gallery.py`](scripts/gallery.py)**:
the blind LRRK2 recovery above; *disambiguation* (one diagnostic label, two different lab panels → two
different mechanistic stories — the flattening undone); a *certified ⊥*; and a *tested operator
hypothesis* (you propose an edge of the mechanism; the shadow confirms one and falsifies the other out —
your intuition enters as a **tested** input, never as ground truth). A companion tool,
**[`scripts/connect.py`](scripts/connect.py)**, answers a narrower question from diagnoses alone: given
several conditions, which are actually *wired together* in the interactome, and which only look related?

## The theory it instantiates

Homeostat is not a heuristic; it is a working instance of a body of formal theory:

- **Negative specification** — specifying by elimination, and the distinction that lets it certify a
  real negative: a *value*-kill certifies, a *run*-kill only constrains.
- **Significance-weighting** — coverage of the shadow as the endogenous oracle, in place of frequency.
- **Orthogonal ternary projection** — the signed-ternary algebra (support / oppose / abstain) the
  elimination runs in, with abstention a first-class value rather than a missing answer.
- **Regenesis** — deterministic, provenance-carrying story-understanding: it reads the surviving
  structure as a *role in a story*, which is what makes fungible mechanisms recognizable across genes.

## Where it actually is

Plainly, because it matters: **every layer is built, pinned on real open-biology data, and threaded
into a single read that runs end to end.** The engine, the per-person positioning, the six coupling
banks (each fired on its real dump — SIGNOR, STRING, Ensembl/Compara, Reactome, GTEx, GWAS), the
structural eliminator, the story layer, the resolve-narrow ranking, the σ_sem completeness read, the
operator-hypothesis ledger, the mechanism-level discriminating question, the input assembly (diagnosis →
subspace via a sourced disease-gene glossary; labs → shadow), and the story-led rendering that surfaces
the read — all built and wired into the apex `drive`. Every *pure decision* is verified to a
mutation-complete specification and covered by hand-written intent tests: **500 pass.** The gallery runs
the whole matrix on real and constructed inputs.

The honest remaining work is validation, not construction: a fully *blind* recovery of a known
multi-gene mechanism as the standing acceptance test, and richer input modalities (notes →
directionality, genotype). The deeper limit is not code — the data that would *settle* a read (one
person's genes and symptoms together, watched over time as the mechanism moves) is gated behind
institutions and money. Homeostat is built to work from the *free shadows* of that data, so its output
is a **testable hypothesis, never a proven mechanism and never a diagnosis** — and it is built to keep
telling you which is which.

## The point

Population medicine reads you by asking how common you are. This reads you by asking what, specifically,
is happening in *you* — and it will not pretend to an answer it cannot support. Run through it, the
rigor that the counting apparatus wields *against* the individual becomes the individual's: a legible,
auditable, falsifiable mechanism you can take to a clinician and test — one no one can wave away as
feelings, because every step of it is on the page. That is a redistribution of who gets to reason about
a body. The honesty is not the caveat on the tool. It is the tool.

## Read further

- [`docs/THESIS.md`](docs/THESIS.md) — the full theory: what understanding is, and why it comes home to
  biology. Start here for the *why*.
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — the as-built wiring map: every layer, its state, how the pieces
  connect. Start here for the *what and how*.
- [`docs/SYSTEM_DESIGN.md`](docs/SYSTEM_DESIGN.md) — the engineering design and the eleven laws that
  discipline it.
- [`docs/REGULATORY_DEFICIT_PROGRAM.md`](docs/REGULATORY_DEFICIT_PROGRAM.md) — the founding canon.

The formal substrate — specification complexity, negative specification, significance-weighting,
orthogonal ternary projection — is the author's own work, referenced from the design docs.
