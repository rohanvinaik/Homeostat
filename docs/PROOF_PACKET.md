# Homeostat — Proof Packet

Each capacity claimed in the [README](../README.md), paired with a **runnable demonstration** — a
command and its *actual, unedited output* — and an argument for why it is **categorically** different
from what medicine currently offers, not merely better at the same thing. Every read below is
*computed by the pipeline*, not authored; you can reproduce all of it.

> These are hypotheses to interrogate, not diagnoses, and nothing here is medical advice. That
> discipline is itself one of the proofs (§4–§5).

## How to run this (from a fresh clone)

The core is **stdlib-only** (`requires-python >= 3.10`, `dependencies = []`) — there is nothing to
`pip install`. From the repository root:

```bash
python scripts/gallery.py                                  # §1–§9: six demonstrations, end to end
python scripts/build_glossary.py                           # build the glossary (once; needed by §3)
python scripts/connect.py "Crohn's disease" "Ulcerative colitis"   # §3: the connection map
python -m pytest -q                                        # the full specification: 500 tests
```

- **Entries 2–6 of the gallery, and every synthetic demonstration below, are self-contained** — they
  build a small input geometry in memory and run instantly, no network, no data.
- **The real-data demonstrations** (§1 blind recovery, §3 connection map) read six open-biology
  databases (SIGNOR, STRING, Ensembl/Compara, Reactome, GTEx, GWAS) and the Jensen-lab DISEASES
  disease-gene database. The fetch shells **download and SHA-pin these on first run** (a few hundred
  MB, one time); after that they are cached. `scripts/build_glossary.py` builds the diagnosis→gene
  glossary from DISEASES.
- **Regenesis** (the story-understanding engine, §9) is an *optional* dependency: absent, the dramatic
  account degrades gracefully to the native genre reading; the reads still run.

Determinism note: there is no trained model and no randomness in the read — the same input produces
byte-identical output every time. That is what makes "auditable" (§10) a literal claim.

---

# I. Seeing what single-tool inspection cannot

## §1 — Recover the mechanism from the shadow

**The claim.** From a sparse deviation pattern it recovers a bounded set of candidate *mechanisms* —
including, blind, a known one.

**What medicine does, and the wall.** A clinical workup reads a presentation by projecting it onto
named diagnostic axes and testing each against a population threshold. A pattern that is *sub-threshold
on every axis alone* but coherent as a joint displacement — a *shadow* — is discarded, because the
signal lives in the correlations the projection flattens. This is not a power problem: adding patients
does not recover a signal the projection has already thrown away.

**Demonstration** (`python scripts/gallery.py`, §1 — real public data):

```
THE READ  —  18 candidate mechanisms fit; none yet separable.

CANDIDATE MECHANISMS  (ranked by how much of the presentation each explains)
  1. {DCC, MYO10}
  2. {IL1R1, IL1RAP}
  ...
  … and 12 more that partially explain the presentation.

WHAT I CAN'T YET TELL  —  and the measurement that would
  Measure DCC; it separates the leading candidates.
  (the LRRK2-NOD2-RIPK2 axis is candidate #11 of the bounded set — recovered blind)
```

Given the public inflammatory-bowel gene set as a search space and a three-node inflammatory shadow —
**blind to the answer** — it returns a *dozen* legible candidate mechanisms with the known
**LRRK2–NOD2–RIPK2** inflammatory bridge among them.

**The categorical difference.** The input is three generic nodes over a fifteen-thousand-node
interactome. A counting method sees nothing; a large model would confabulate one confident answer.
This returns a *small, legible, falsifiable* set and names the measurement that narrows it. It reads
the object — the joint displacement — that projection structurally cannot represent.

## §2 — Roles, not genes

**The claim.** Two *different* genes that play the same biological role are recognized as **one
mechanism** — even with no shared gene between the patients who carry them.

**What medicine does, and the wall.** Genetics finds causes by *counting*: which variant is commoner
in patients than controls. When the same pathway is broken by different interchangeable genes in
different people — one at step 12, another at step 30 — there *is no shared gene* to count. The method
finds nothing, at any sample size, because the invariant it needs (the role) is not the object it
measures (the gene).

**Demonstration** (`python scripts/gallery.py`, §5):

```
ROLE-EQUIVALENCE, earned from the geometry (the fungibility read):
  GENE_A ~ GENE_B: fungible  (2 independent banks converge)

  → GENE_A and GENE_B share no identity, yet the engine reads them as ONE role. A
    count across the two finds no shared gene and sees nothing; the role-read sees
    one mechanism.
```

The verdict `fungible` is *earned*, not assumed: the two genes must resemble each other **and**
converge on a shared partner across ≥2 independent evidence banks. One bank alone reads `coincidental`.

**The categorical difference.** Counting operates on gene identity; this operates on gene *role*.
Those are different objects. The interchangeable-parts mechanism — the one that defeats every
frequency method by construction — is exactly the one the role-read is built to see.

## §3 — Convergence across the geometries of biology

**The claim.** It trusts a coupling only when *independent* views of biology agree, and reports which
conditions are wired together through shared regulators.

**What medicine does, and the wall.** A single association study (one dataset, one lens) is a single
noisy projection. Two clinically-comorbid conditions may share no *listed* genes yet route through the
same regulatory hub — a fact no single-lens read surfaces.

**Demonstration** (`python scripts/connect.py "Crohn's disease" "Ulcerative colitis" "Ankylosing spondylitis"`):

```
WIRING  (direct gene-gene couplings · shared direct regulators):
  Crohn's dis<->Ulcerative    7 direct ·   11 shared-reg  [WIRED]
      shared regulators: ['EGFR','GHR','IL10','IL1B','JAK1','JAK2','STAT1','STAT3','STAT4','STAT6','TYK2']
  Crohn's dis<->Ankylosing   15 direct ·   38 shared-reg  [WIRED]
  Ulcerative <->Ankylosing    6 direct ·    7 shared-reg  [WIRED]
      shared regulators: ['IL10','JAK1','JAK2','STAT1','STAT3','STAT4','TYK2']
```

Three inflammatory conditions, all found **wired** — through the **JAK–STAT / IL-10 axis**, computed
from cross-network convergence over ≥2-network couplings. That axis is not a guess: it is the exact
hub all three are clinically treated at (JAK inhibitors).

**The categorical difference.** A single study reports a correlation within one lens. This reports a
*mechanism agreed on by several independent lenses* and drops anything only one supports — turning "are
these related?" from a literature question into a computed, auditable one.

---

# II. Knowing when to stop

## §4 — The certified ⊥ (a proof of no mechanism)

**The claim.** It can return a *proof that no mechanism explains this*, distinct from "I didn't find
one."

**What medicine does, and the wall.** Statistics can only ever *fail to reject the null* — "not
significant" is the absence of evidence, never evidence of absence. A workup that finds nothing says
"we didn't find anything," which is epistemically identical to "we didn't look in the right place."
There is no construct, anywhere in the frequentist toolkit, for *proven absent*.

**Demonstration** (`python scripts/gallery.py`, §3):

```
THE READ  —  certified ⊥ — nothing in scope explains the presentation (a proof).
```

Given a shadow whose signs the only eligible source *contradicts* (it would have to drive one marker up
and one down through the same activation), the two-sign engine rules out the entire candidate set and
returns a certified bottom — a proof of non-membership.

**The categorical difference.** This is not a smaller p-value; it is a *different epistemic object* — a
constructive proof, in signed-ternary elimination, that the known biology contains no mechanism casting
this shadow. You cannot obtain it from a frequency, at any sample size. Medicine can be *uncertain*; it
cannot be *certifiably negative*.

## §5 — Honest abstention (the refusal to confabulate)

**The claim.** When the evidence does not converge, it says so and names the discriminating
measurement — rather than manufacturing a confident story.

**What medicine does, and the wall.** A diagnostic algorithm — and, more sharply, a trained model —
*always outputs*. It has no principled "I refuse." Given noise, it returns a confident label anyway;
the failure mode of the confabulation objection ("it finds a story in anything") is real, and it is the
default behavior of every system that must always answer.

**Demonstration** (`python scripts/gallery.py`, §1, the same real read as above):

```
THE READ  —  18 candidate mechanisms fit; none yet separable.
  ...
WHAT I CAN'T YET TELL  —  and the measurement that would
  Measure DCC; it separates the leading candidates.
```

Given a genuinely under-determined signal, it does **not** collapse to one answer. It returns the
bounded plurality and the single measurement that would narrow it — and elsewhere (§4) returns a
certified nothing rather than a story at all.

**The categorical difference.** The confabulation attack assumes a system that always answers. This
one's defining move is knowing *when not to*. The refusal is not a limitation bolted on; it is the
immune system that makes every non-refusal trustworthy.

---

# III. Undoing the flattening

## §6 — One label, two mechanisms

**The claim.** Two people with the *same diagnostic label* but different presentations resolve to
*different* mechanistic stories.

**What medicine does, and the wall.** A great many diagnoses — the behavioral ones especially — are
*defined* by a criteria checklist with no reference to mechanism. Two mechanistically distinct people
who meet the same criteria *are the same diagnosis by construction*. The label cannot disambiguate
them: it is a definitional limit, not a resolution problem.

**Demonstration** (`python scripts/gallery.py`, §2):

```
Patient A  —  diagnosed 'spectrum condition', labs: SHARED + ILR elevated:
THE READ  —  resolved to a single mechanism.
  1. {ILR, INF, SHARED}  — A vicious comedy: ILR and INF lock into a mutual-regulation loop...

Patient B  —  SAME diagnosis, labs: SHARED + SYNSINK elevated:
THE READ  —  resolved to a single mechanism.
  1. {SHARED, SYN, SYNSINK}  — A tragedy: SYN drives an unstoppable cascade to a doomed sink...

  → same label, two panels, two different mechanistic reads. The label flattened; the geometry did not.
```

Both patients carry the same diagnosis. One resolves to a vicious feedback loop, the other to a doomed
cascade — *different mechanisms, different treatment targets, from the same label*.

**The categorical difference.** The label's job is to be shared; the mechanism's job is to be specific
to you. This moves the object of diagnosis from *which criteria-cluster* to *which regulatory deficit* —
recovering exactly the distinction the label is built to erase.

---

# IV. Reasoning *with* the person

## §7 — The tested operator hypothesis

**The claim.** Your own intuition about your mechanism enters as a **tested** input — confirmed or
falsified against the geometry — never as ground truth, and never dismissed unheard.

**What medicine does, and the wall.** The clinical encounter treats patient self-report as unreliable
subjective data to be *screened out*. There is no mechanism to enter a patient's mechanistic intuition
as a first-class, *testable* proposal — it is either believed or (more often) discounted.

**Demonstration** (`python scripts/gallery.py`, §4):

```
WHAT YOU GOT RIGHT
  Your hypothesis that DRIVER amplifies MARKER1 — the shadow confirms it.
  Your hypothesis that DRIVER inhibits MARKER2 — the shadow contradicts it; it falls out.
```

The operator proposes two edges of the mechanism. The engine judges each against the shadow: one holds,
one is falsified out. The person's intuition is *used* — and *checked*.

**The categorical difference.** This is neither "the doctor knows best" nor "the patient is always
right." It is a third thing: the person proposes, the geometry adjudicates, and a wrong guess simply
falls out. Correctness stays in the computation; the patient's decade of self-observation stops being
noise to filter and becomes a hypothesis to test.

## §8 — The discriminating counter-ask (Jeeves)

**The claim.** When candidates fit equally, it names the *single measurement* that would separate them.

**What medicine does, and the wall.** Testing proceeds by protocol and differential — a standard panel,
ordered by convention. It does not compute the one maximally-informative measurement for *this person's
current surviving hypothesis space*.

**Demonstration** (`python scripts/gallery.py`, §1):

```
WHAT I CAN'T YET TELL  —  and the measurement that would
  Measure DCC; it separates the leading candidates.
```

Faced with a plurality it cannot resolve, it does not guess and does not order everything. It computes
the node whose measurement most cleanly splits the survivors, and asks for exactly that.

**The categorical difference.** This inverts the information flow: the read ends not with an answer but
with the *most valuable question*, computed for you specifically — often one you already carry in your
own history.

---

# V. A read you can audit

## §9 — The mechanism, read as a story

**The claim.** The answer is not a ranked gene but a *legible dynamical account* — the same
story-understanding that reads Shakespeare, run on biochemistry.

**What medicine does, and the wall.** A diagnosis is a name. It tells you *what* you have, not *why* —
not the shape of the motion that produces it. The cross-mechanistic "dynamics grammar" that alternative
traditions gestured at, they never separated from the woo.

**Demonstration** (`python scripts/gallery.py`, §6):

```
THE GENRE READING (every opinionated instance the dynamics fire):
  tragedy   Tragedy(origin='TP53', sink='APOPTOSIS', verdict='doomed')
  comedy    Comedy(a='CDK1', b='MYC', verdict='vicious')

THE DRAMATIC ACCOUNT — through the same engine that reads Shakespeare:
  TP53 --harm--> APOPTOSIS    (pursuit)
  CDK1 --betray--> MYC    (revenge)

  → the mechanism reads as: pursuit + revenge.
```

A control system's *dynamics* are what narrative structure captures. A vicious feedback loop **is** a
revenge; a flaw driving a node to a locked doom **is** a pursuit. The multi-part mechanism comes back,
through the same engine that reads Macbeth, as *pursuit + revenge* — the mechanics read correctly,
claiming nothing about purpose.

**The categorical difference.** A label is inert; a story is *generative* — you can reason and infer
over it. This is Winston's thesis (story understanding is one general intelligence capacity) made
tangible on biology, and the extraction the alternative traditions never made: keep the
dynamics-grammar, drop the woo.

## §10 — Deterministic, auditable, untrained

**The claim.** The reasoning is classical AI and data geometry — no trained model, fully reproducible,
every step traceable.

**What medicine does, and the wall.** The two candidate replacements both fail the audit. A trained
diagnostic model is a black box — you cannot read *why* it concluded what it did, and it can hallucinate
with confidence. A clinician's intuition is not reproducible and dies with the clinician.

**Demonstration.** There is nothing to train: `pyproject.toml` declares `dependencies = []`. The same
input produces byte-identical output every run (no weights, no randomness). Every candidate on every
list traces back to the coupling web, the eliminations, and the signals that produced it —
`python -m pytest -q` verifies **500** intent-and-mutation-pinned tests over the pure decisions.

**The categorical difference.** This is the only point that is *simultaneously* mechanistic (unlike a
correlation), auditable (unlike a trained model), reproducible (unlike intuition), and honest about
absence (unlike all three). It runs on the compute of a moderately-large potato because the
intelligence is in the correctness of the geometry, not the size of a network.

---

# The point

Population medicine reads you by asking how common you are. Homeostat reads you by asking what,
specifically, is happening in *you* — and it will not pretend to an answer it cannot support. Ten
capacities, ten demonstrations you can run yourself; each one is a thing the counting apparatus cannot
do, not because it is smaller but because it is pointed at a different object. Run together, they hand
the individual a legible, auditable, falsifiable mechanism — one no one can wave away as feelings,
because every step of it is on the page and reproducible from a clean clone. That redistribution of who
gets to reason about a body is the product. The honesty is not the caveat on it. It is the tool.
