# Homeostat

**Tell it your symptoms. It reads the genetics underneath them from open data, works out what — if
anything — actually connects them, and tells you what that means and, just as carefully, what it
doesn't.** It is meant to be the one doctor who takes the presentation seriously, and the one who won't
invent a story to fill the silence. Named for Ashby's homeostat, the machine that finds its own
equilibrium, because the thing under study is regulation.

> Research scaffolding for mechanism discovery. It generates *hypotheses*, not diagnoses. **Nothing here
> is medical advice.**

---

## The problem it's built around

Medicine finds the genetic cause of a disease mostly by counting: which variant shows up more often in
patients than in healthy people. For a clean single-gene disease that works. For most of disease it
quietly doesn't — and it fails hardest on exactly the people who are already the hardest to believe.

A symptom usually sits at the end of a long, redundant, forgiving pathway, and a long pathway breaks in
many places. One person breaks it at step 12; another at step 30 with a different mutation doing the same
job; a third has a spare gene covering for the first. Same mechanism every time, no shared gene — so the
count finds nothing. It has taken a real, legible mechanism and smeared it across a population until, in
the precise information-theoretic sense, the signal is gone.

This bites hardest on the multi-system presentations — the constellations of symptoms that don't line up
with one organ or one clinic, and get read as "it's probably anxiety" in a seven-minute appointment. Here
is how thoroughly counting has failed them: some of these conditions are so under-studied that the entire
free research literature knows **fewer than a handful of their genes.** Not because they are rare —
because the field's dominant instrument cannot see them, so the research and the funding and the belief
all went elsewhere.

## The idea

Stop counting genes. Recover the *mechanism*, and recognize it by the **role** a gene plays rather than
its name — because the name is the interchangeable part and the role is the invariant. Then triangulate:
no single free dataset shows you a mechanism, so look through several cheap, blurry windows — how variants
differ across populations, what co-expresses, what physically binds — and trust only what several
independent windows agree on. Convergence is the signal; a gene that lights up one window and no others
is noise.

The reasoning that combines the windows is **classical AI — not statistics, not machine learning.** It
derives what the evidence implies but never states, and it abstains when nothing follows. Statistics gets
exactly one honest job, characterizing a single window; it is never allowed to be the thing that decides
what is true.

## What it does — and you can run it

```console
$ python3 validation/read.py "<four symptoms that don't obviously belong together>"

HOMEOSTAT · a reading, not a ruling.

what you handed me, and how much the open literature actually knows about each:
  symptom 1     1,856 genes
  symptom 2        83 genes
  symptom 3       647 genes
  symptom 4         5 genes   ← a data desert; the field has all but ceded this one

what connects them — the specific genes bridging your symptoms (I dropped the generic
hubs on purpose: a gene that touches everything explains nothing):
  [a short list of the specific bridge genes]

how much to trust it: 472 genes bridge them, against 659 expected purely by chance
(p=1.00). That is *not* above chance. Read the genes as 'worth a look', not 'the
mechanism' — the missing piece is the one medicine is also missing: your genes AND
your symptoms together, at scale. Holding this at 'lead' is the honest part.

▸ 'symptom 4' is nearly data-empty on its own — but its few genes belong with
  'symptom 3'. If symptom 4 is the real question, ask that pair instead.
```

That output is the whole design in miniature. The command line is not a print box; it is an **epistemic
interface**. It reports what it found *and what that finding is worth* — here, honestly, not much yet. It
refuses to dress a coincidence as a discovery. And in that last line it does something quieter and more
useful: it notices that one symptom is a data desert, sees that its few genes actually belong with
another of the symptoms, and — with a few lines of arithmetic, no language model — points you at the
question you were about to ask. It waits exactly where you'll need it.

From there, a person (or the agent) puts on the lab coat: group the genes into modules, narrate the most
coherent causal *hypothesis* they support, and say where the data stops. If you have your own genotype,
`--genotype` overlays which of the candidate genes *you* carry notable variants in — and that stays on
your machine.

## The honesty is the product

Given a hard case, most systems either dismiss it or confabulate a confident story. This one does
neither, by construction. On a real presentation it once surfaced a genuinely elegant module — a clean
molecular story tying the symptoms together, the kind of thing that reads beautifully in a case report.
Then a permutation null showed the convergence was no denser than chance, and the system deleted the
result and kept the deletion. A tool that will not hand you a beautiful lie is worth more than one that
impresses you, and that refusal is the point rather than a limitation of it. It will rank and connect; it
will not decide *why* — imputing purpose is the human's job, and it is careful to say so.

## The engine is checked on known biology

Before it reads a person, the mechanism-finder is validated on cases where the answer is known. Handed
the **LRRK2–NOD2–RIPK2** immune-signaling mechanism as anonymous tokens, from free data, with no gene
names given, it recovers the real structure — RIPK2 and NOD2 as the confirmed core, LRRK2 as a genuinely
weaker member, the promiscuous HLA hubs censored as noise — graded by how many independent windows agree.
That recovery, a determinism and adversarial-abstention suite, a held-out-annotation recovery (p=0.015),
and a transfer across sixteen mechanisms all pass with real demonstrations in
[`docs/PROOF_POINTS.md`](docs/PROOF_POINTS.md) and
[`validation/VALIDATION_RESULTS.md`](validation/VALIDATION_RESULTS.md). Where the ledger is not green, it
says so.

## Honest limits

The data that would actually settle these questions — each person's genes *and* their symptoms together,
so a mechanism can be watched to move — is gated behind institutions and money. Homeostat works from the
free shadows of it. So its output is a testable hypothesis, never a proven mechanism and never a
diagnosis. That is a fact about what data is purchasable, not a flaw in the method — and the whole system
is built to keep telling you which is which.

## Run it, or read further

```
PYTHONPATH=src python3 validation/read.py "your, symptoms, here"
```

1. [`docs/ETIOLOGY_ENGINE.md`](docs/ETIOLOGY_ENGINE.md) — the design of the whole stack. Start here.
2. [`docs/PROOF_POINTS.md`](docs/PROOF_POINTS.md) — the validation ladder, honestly scored.
3. [`docs/REGULATORY_DEFICIT_PROGRAM.md`](docs/REGULATORY_DEFICIT_PROGRAM.md) — the founding canon.

The reasoning engine is **Regenesis**. The data-geometry signal layer and the formal substrate it rests
on are the author's own work, referenced from the design docs.
