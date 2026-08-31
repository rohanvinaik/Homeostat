# Homeostat

**A mechanism-unearthing engine for genetics — it imputes the causal mechanism under a symptom
presentation instead of counting which gene shows up more often in sick people.** Named for Ashby's
homeostat, the device that finds its own equilibrium, because the thing being studied is regulation.

---

## The problem it exists to solve

Medicine tries to find the genetic cause of a disease by asking *"which gene shows up more in sick
people than healthy people."* That's a frequency count, and for a huge amount of disease it just
doesn't work — and everyone half-knows it doesn't.

The reason is that biology isn't a clean one-gene-one-disease machine. It's a long, redundant, noisy
pipeline. A phenotype is often the end of a 50-step pathway, and that pathway is absurdly fragile to a
frequency count. One person breaks it at step 12; another at step 30 with a totally different mutation
that does the same thing; a third has a **fungible** substitute gene covering the job; a fourth has
three downstream genes standing in for one busted upstream one; a fifth has a clean fallback that
compensates. Same disease, same broken mechanism, every time — but line up their genomes and count, and
no single gene is *the* common one. The statistic goes quiet. **It smears the real mechanism across the
population and, in the literal information-theoretic sense, throws the information away.** You're left
knowing *these people are sick* and not *why* — even though the "why" is right there, and is even
understandable one person at a time.

Differential outcomes for the *same* clinical presentation across populations are the audit log of that
error. That's what Homeostat is built to stop doing.

## The idea

Stop counting genes. Recover the **mechanism**, and recognize it by what the genes are *doing* — the
role they play — not by their names. Because the names are the fungible part; the mechanism is the
invariant.

Two moves make that work:

- **Recognize the role, not the gene.** The same mechanism is spelled with one set of genes in one
  population and a *different* set in a founder isolate. So the engine pulls out *"something here is
  playing the amplifier role, whatever it's called"* — matched by the role, never the gene token. That's
  the only way to see a mechanism that different populations realize with different genes.
- **Triangulate across many lossy windows.** No single free data source shows you the mechanism, so we
  look through several cheap, blurry ones — how a gene's variants differ across populations, which genes
  rise and fall together in tissue, which physically stick to each other, which wire to the disease's
  traits. A gene only counts where **several independent windows agree**. Convergence is the signal; a
  gene that lights up only one window is noise.

The reasoning that combines those windows is **classical AI, not statistics and not machine learning** —
a deterministic story-understanding engine (a port of Patrick Winston's Genesis) that reads the windows,
derives what they *imply* but never state, ranks findings by how improbable-yet-coherent they are, and
abstains when nothing follows. Statistics gets exactly one honest seat — as a *characterization* tool
inside a window (e.g. deriving a cutoff from a data set's own noise), never as the significance.

## Why it's interesting

- **It sees mechanism that single-locus genetics is structurally blind to.** The effect that lives in a
  *combination* of weak, interchangeable signals is invisible to any element-by-element frequency test,
  at any sample size. Homeostat reads the coherence of the combination directly.
- **It handles fungibility across populations** — the exact case that breaks gene-frequency statistics
  and n-of-1 reasoning alike. Recognizing roles instead of tokens is what lets it.
- **It runs on free, public data.** No gated cohort, no institutional affiliation — the whole thing works
  from public population genetics, expression, and interaction data. A person with a laptop can run it.
- **Nothing is hard-coded.** The mechanism is *grown* from where the data converges. You never tell it
  "gene X is the amplifier" — that would be assuming the answer. The roles fall out of the data.
- **Every threshold is derived from the evidence,** not a textbook constant — the way a neuron itself is
  a threshold tuned for noise, not a universal truth.

## What it does today (proof of concept)

Given the known **LRRK2–NOD2–RIPK2** inflammatory mechanism — a real thing, misfiled for years as a
"Parkinson's gene," actually an immune-signaling bridge — Homeostat, **from free data alone and with no
gene names told to it**, recovers the mechanism and ranks it by confidence:

- **RIPK2** rises to the top (`deep_core`) — it's confirmed by the most independent windows.
- **NOD2** lands just below (`core`).
- **LRRK2** comes in as a weaker member (`component`) — honestly weaker, because its signal is a specific
  sub-population effect that washes out at the coarse continental level (which is exactly why it was
  missed for so long).
- The **generic immune hubs** that co-express with everything (e.g. HLA-DQA1, which associates with 1000+
  unrelated traits) are **censored out** as structural noise.

That is the instrument recovering a real compositional mechanism, discriminating it from noise, with
graded confidence — computed end to end, no cheating. Adding a new evidence window is a disciplined,
repeatable step (see `docs/DENSITY_PROTOCOL.md`); done principled and forever, it scales toward the whole
gene × phenotype space.

## Honest limits

The gold-standard data — each person's genes *and* symptoms together, so you can watch the mechanism
move — is gated behind institutions and money. Homeostat works from free *shadows* of it. So what it
produces is a strong, testable **hypothesis** about mechanism, not a proven one, until that data exists.
That's a fact about available data, not a flaw in the method. **This is research scaffolding, not medical
advice; no output here is a clinical finding.**

## How it works, in order

1. **`docs/ETIOLOGY_ENGINE.md`** — the self-contained design of the whole stack (read this first).
2. **`docs/THEORY_OF_THE_CASE.md`** — the derived design + the project laws.
3. **`docs/REGULATORY_DEFICIT_PROGRAM.md`** — the founding canon (authoritative, self-contained).
4. **`docs/DENSITY_PROTOCOL.md`** — the repeatable recipe for adding one more evidence window.
5. **`docs/PROBE_STATE.md`** — the live state of the running experiment.
6. **`AGENTS.md`** / **`CLAUDE.md`** — the gate and the laws, read before proposing anything.

The reasoning engine is **Regenesis** (`mcp__Regenesis__*`); the data-geometry signal layer and the
formal substrate (specification complexity, significance-weighting, `measuring_agi` behavioral
characterization) are the author's own work, referenced from the design docs.
