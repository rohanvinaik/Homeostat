# Homeostat

**A mechanism-finding engine for genetics. It works out the causal mechanism under a symptom
instead of counting which gene shows up more often in sick people.** Named for Ashby's
homeostat — the machine that finds its own equilibrium — because the thing under study is
regulation.

## The problem

The standard way to find a disease gene is to count: which variant is more common in patients
than in healthy people. For a clean one-gene disease that works. For most of disease it quietly
fails, and the field half-knows it fails.

The reason is that a symptom usually sits at the end of a long, redundant pathway, and a long
pathway can break in many places. One patient breaks it at step 12; another at step 30 with a
different mutation that does the same thing; a third has a spare gene that covers the job; a
fourth spreads one broken step across three downstream genes; a fifth has a clean fallback that
compensates. Same disease, same broken mechanism every time — but line up their genomes and
count, and no single variant is *the* common one. The count goes quiet. It has smeared the
mechanism across the population and thrown the information away. You are left knowing *these
people are sick* and not *why*, even though the why is right there and is legible one patient at
a time.

Differential outcomes for the same clinical presentation across populations are the audit log of
that error. Homeostat is built to stop producing it.

## The idea

Stop counting genes. Recover the *mechanism*, and recognize it by what each gene is *doing* — the
role it plays — not by its name. The name is the interchangeable part; the role is what stays
fixed. Two moves make that work:

- **Recognize the role, not the gene.** The same mechanism is spelled with one set of genes in
  one population and a different set in a founder isolate. So the engine looks for *"something
  here is playing the amplifier role, whatever it is called"* — matched by role, never by gene
  name. That is the only way to see a mechanism that different populations build from different
  parts.
- **Triangulate across several cheap, blurry windows.** No single free dataset shows you a
  mechanism, so the engine looks through several: how a gene's variants differ across
  populations, which genes rise and fall together in tissue, which physically bind each other,
  which associate with the disease's traits. A gene counts only where independent windows agree.
  Convergence is the signal; a gene that lights up one window and no others is noise.

## Watch it work

Here is the whole idea in one run. A known immune-signaling mechanism — **LRRK2–NOD2–RIPK2**,
misfiled for years as a "Parkinson's gene" but really an inflammation bridge — is handed to the
engine as eight anonymous tokens. No names. Every signal is computed from free public data. The
engine reads the signals, works out what they imply, ranks the result by how many independent
windows agree, and only then is the name map read back:

```text
$ PYTHONPATH=src python3 probes/l2_lrrk2.py

  in:  eight genes as anonymous tokens — no names given to the reasoning
       every signal below is computed, from free public data only

  gene2   differentiates populations · co-expresses · BINDS the seed · wires traits
  gene1   differentiates populations · co-expresses · wires traits
  gene8   differentiates populations · co-expresses · wires traits
  gene3   differentiates (weakly) · co-expresses · wires traits
  gene5   co-expresses · wires traits · but associates with 1021 unrelated traits
  gene4   co-expresses · wires traits · but associates with  756 unrelated traits

  out: the engine ranks by convergence across independent windows
  gene2  ->  deep_core   4.43     confirmed by the most windows, incl. physical binding
  gene1  ->  core        3.33
  gene8  ->  core        3.33
  gene3  ->  component    2.64    real, but honestly weaker (see below)
  gene5  ->  censored              # co-expresses like a member — but wires 1021 traits.
  gene4  ->  censored              #   that is a generic hub, not a mechanism. dropped.

  map:  gene2=RIPK2  gene1=NOD2  gene8=TNFSF15  gene3=LRRK2  gene5=HLA-DQA1  gene4=HLA-DRB1
```

Read that last line back and the ranking is the real biology: **RIPK2** and **NOD2**, the core of
the pathway, on top; **TNFSF15**, an inflammatory-bowel-disease gene in the same signaling family,
promoted alongside them; **LRRK2** recovered but weaker — honestly weaker, because its effect is a
specific sub-population signal that washes out at the coarse continental level, which is exactly
why it was missed for so long. And the two promiscuous immune hubs (**HLA-DQA1** associates with
over a thousand unrelated traits) are censored out as generic noise, not counted as mechanism.

No gene names were given to the reasoning. The roles fell out of the data.

## Why it is interesting

- **It sees mechanism that single-locus genetics is structurally blind to.** An effect that lives
  in a *combination* of weak, interchangeable signals is invisible to any test that examines one
  variant at a time, at any sample size. Homeostat reads the coherence of the combination
  directly.
- **It handles the same mechanism spelled differently across populations** — the exact case that
  breaks both frequency counting and single-patient reasoning. Recognizing roles instead of gene
  names is what lets it.
- **It runs on free, public data.** No gated cohort, no institutional access — population
  genetics, expression, and interaction data that anyone can download. A person with a laptop can
  run it.
- **Nothing is hard-coded.** You never tell it "gene X is the amplifier" — that would be assuming
  the answer. The mechanism is grown from where the data converges, and the roles fall out.
- **Every cutoff is derived from the evidence,** not a textbook constant — the way a neuron sets
  its own threshold against noise rather than reading one off a rulebook.

The engine doing the reasoning is classical AI — not statistics and not machine learning. It is a
deterministic story-understanding system (a port of Patrick Winston's Genesis) that reads the
windows, derives what they *imply* but never state, ranks findings by how improbable-yet-coherent
they are, and abstains when nothing follows. Statistics gets exactly one honest seat — as a
*characterization* tool inside a single window, for instance setting a cutoff from a dataset's own
noise — never as the thing that decides significance.

## Honest limits

The gold-standard data — each person's genes *and* symptoms together, so the mechanism can be
watched to move — is gated behind institutions and money. Homeostat works from the free *shadows*
of it. So what it produces is a strong, testable **hypothesis** about mechanism, not a proven one,
until that data exists. That is a fact about what data is available, not a flaw in the method.
**This is research scaffolding, not medical advice; no output here is a clinical finding.**

The LRRK2 run above is one worked example: the instrument recovering a real mechanism, blind to
gene identity, from free data. It is not yet proof the method *generalizes*. What would earn that
stronger claim — a panel of known mechanisms, adversarial negative controls, a head-to-head
against the standard toolkit, and the cross-population case shown on real data — is laid out,
honestly and with pass bars, in [`docs/PROOF_POINTS.md`](docs/PROOF_POINTS.md).

## How confidence is computed, not fudged

The numbers above (4.43, 3.33, 2.64) are not a tuning knob. Confidence *is* structure: each
independent window that agrees adds one more link to the reasoning, and a gene ranks higher only
by being confirmed along more links, never by a weight someone chose. The whole ladder is three
rules:

```text
tracks the seed  +  differs across populations         ->  component
    + dominates that population difference               ->  core
    + physically binds the seed                          ->  deep_core
```

RIPK2 reaches `deep_core` because a fourth, independent window — physical binding — confirms it.
That is the entire scoring model: more converging evidence is literally more structure, and more
structure is what ranks higher.

## Reading order

1. [`docs/ETIOLOGY_ENGINE.md`](docs/ETIOLOGY_ENGINE.md) — the self-contained design of the whole
   stack. Start here.
2. [`docs/THEORY_OF_THE_CASE.md`](docs/THEORY_OF_THE_CASE.md) — the derived design and the project
   laws.
3. [`docs/REGULATORY_DEFICIT_PROGRAM.md`](docs/REGULATORY_DEFICIT_PROGRAM.md) — the founding canon,
   self-contained and authoritative.
4. [`docs/DENSITY_PROTOCOL.md`](docs/DENSITY_PROTOCOL.md) — the repeatable recipe for adding one
   more evidence window.
5. [`docs/PROOF_POINTS.md`](docs/PROOF_POINTS.md) — what it would take to earn the generalization
   claim, with pass bars.
6. [`docs/PROBE_STATE.md`](docs/PROBE_STATE.md) — the live state of the running experiment.

The reasoning engine is **Regenesis**. The data-geometry signal layer and the formal substrate it
rests on are the author's own work, referenced from the design docs.
