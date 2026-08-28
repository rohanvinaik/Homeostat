# Decision: Homeostat is a publishable project; frame for biomedicine/comp-bio

**Date:** 2026-08-28
**Status:** accepted
**Context:** Founder direction: this is intended as a publishable project, likely with
a physician co-author (a doctor friend of the founder's; not yet confirmed — nothing is
attributed to anyone until they explicitly sign on).

## Decision

The target artifact is a paper for a medicine / biomedicine / computational-biology
audience, framed as: **a mechanism-unearthing system that imputes causal mechanisms
from sub-threshold individual signals, linking biochemistry and etiology to expressed
symptoms.**

Framing constraints (these extend, and match, THEORY_OF_THE_CASE Law 2 and the naming
decision):

1. **Lead with the method**: annotation-blind coupling recovery, the preregistered
   annotation-recovery falsifier, selection-signature validation, PBS-ranked candidate
   sets, the LRRK2 positive control. This is the paper's spine.
2. **The oracle-ensemble ingredient is presented as what it rigorously is** —
   mechanistic import of partition hypotheses from centuries of systematic
   observational medical practice, causally independent of the modern annotation
   channel, phylogeny-weighted, with Unani as the built-in negative control. It is
   pulled out cleanly and never allowed to read as a claim that any traditional system
   outperforms biomedicine (checkpoint §12.7 gives the defensible claim shape:
   search strategy over partition space, not outcomes).
3. **Sub-threshold composition is the hook**: the summation theorem + omnigenic
   framing explains *why* single-variant methods miss this class, which is the part a
   biomedical reviewer can act on.

## Consequences

- Every artifact (code, docs, results) should be written as if a skeptical biomedical
  reviewer reads it: provenance pinned, dials explicit, validators preregistered,
  abstentions visible. This is already the house style; publication makes it binding.
- Results reporting keeps the §15-style status ledger discipline (proved / measured /
  designed / conjectured) so the paper's claims tier cleanly.
- Per the founder's narrative-first workflow: the paper's story gets articulated and
  scored before drafting begins; the §13 experiments produce the evidence for it.
- Co-authorship, venue, and any use of the physician co-author's name require their
  explicit agreement — founder handles that relationship.
