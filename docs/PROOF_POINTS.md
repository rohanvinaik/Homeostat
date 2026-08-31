# Proof Points — what it would take to earn "generalizable mechanistic advance"

The LRRK2–NOD2–RIPK2 recovery is one green cell in the table below. It proves the
*instrument runs and recovers a known mechanism from free data with no gene names told
to it*. It does **not**, on its own, earn the headline claim. This document enumerates the
full set of stress tests, negative controls, benchmarks, and demonstrations that would —
each tied to the specific sub-claim it discharges, with an explicit pass bar and an honest
status. Nothing here is "done" except where marked.

The intent is that a skeptic (a geneticist, a methods reviewer, the author six months from
now) can read one row, run it, and see for themselves whether the cell goes green. If a row
cannot be run yet — because the data is gated — that is stated, not hidden.

---

## The claim, decomposed

The sentence "a generalizable mechanistic advance" is three separable claims, and they fail
in different ways:

- **Mechanistic** — the output is real regulatory mechanism, not a re-description of
  correlation structure the geometry already contained. Fails if the roles are artifacts of
  hub degree, expression abundance, or the seed choice.
- **Advance** — it recovers mechanism that the standard toolkit (single-locus GWAS/PRS,
  network propagation, pathway enrichment, colocalization) structurally cannot. Fails if a
  HotNet2/GSEA baseline recovers the same thing for free.
- **Generalizable** — it is an instrument, not a pipeline hand-fitted to inflammation. Fails
  if moving to a new disease family requires touching anything but the domain's role
  vocabulary.

The proof points are grouped by which of these they earn. **C, D, and E are the
make-or-break tier** — A and B are table stakes that a rigged demo could also pass, so they
come first but they are not where the claim lives.

---

## A · Instrument validity — "it is a real instrument, not a rigged demo"

| # | Demonstrates | Method | Pass bar | Status |
|---|---|---|---|---|
| **A1** | Recovers more than one known mechanism | A panel of ≥8 independently-documented compositional mechanisms (NOD signaling, complement cascade, a DNA-repair complex, a metabolic channel, a mitophagy module…), each run blind to gene identity | Core members surface above censored hubs in ≥8/8, graded by convergence | **◐ PARTIAL** — `validation/a1_panel.py`: 8 mechanisms run blind; hub censoring **100%**, but member recovery is bounded because the method is differentiation-gated (recovers the population-differential subset) and GTEx-median co-expression is a coarse proxy. The clean form needs real co-expression + variant-level Fst. The *finding* is measuring which layer is the bottleneck (lens data, not reasoning) |
| **A2** | Abstains on nothing | Null inputs: random gene sets matched for degree + expression, a shuffled seed, a hub-only set, a non-mechanism | No `core`/`deep_core` emitted from null input; false-positive rate quantified | **✅ PASS** (reasoning layer) — `validation/a2_abstention.py`: 0/15 false-positive archetypes (incl. promiscuous hubs with every qualifying fact) reach mechanism, 6/6 controls promote, 20/20 random subsets match the spec. Genome-sampled form pending Fst infra |
| **A3** | Same input → same answer | Re-run the full stack across runs and machines | Bit-identical role ledger | **✅ PASS** — `validation/a3_determinism.py`: byte-identical fact-text across 3 distinct `PYTHONHASHSEED` (sha `faab482d`); guards the `sorted()` fix |

A-tier is necessary and unglamorous. A demo that *only* passes A is still just a demo — a
sufficiently lucky hard-coding could pass all three. The discriminating work is below.

---

## B · Discrimination — "it separates mechanism from noise, quantitatively"

| # | Demonstrates | Method | Pass bar | Status |
|---|---|---|---|---|
| **B1** | Quantitative separation, not eyeballing | Hold out known members; measure recovery. ROC / precision-recall of core-vs-background across the A1 panel | AUC beats a role-shuffled baseline at a **preregistered** threshold | **not started** |
| **B2** | Needle in a haystack, not 8 hand-picked genes | Run on the full ~289-gene cloud, then a genome-scale slice | Core stays top-ranked and stable as the crowd grows | **not started** — current runs are hand-scoped |
| **B3** | Convergence carries it, no single lens does | Leave-one-lens-out; measure each lens's marginal contribution | No single lens is load-bearing; result degrades gracefully, not catastrophically | **✅ PASS** — `validation/b3_ablation.py`: dropping co-expression changes nothing; binding/wiring drops are localized and graceful; the censor holds the 1021-trait hub out; differentiation is a necessary gate **by design** (on-thesis) |

---

## C · The novel claim — cross-population fungibility (**make-or-break**)

This is the load-bearing tier. It is the thing the README says the method does that nothing
else does, and it is currently *argued*, not *shown*.

| # | Demonstrates | Method | Pass bar | Status |
|---|---|---|---|---|
| **C1** | The same mechanism, different genes, one recovered frame | Find/construct a real case where a mechanism is realized by **disjoint filler sets** in two populations (a founder isolate, a caste-stratified subpopulation vs. a continental group). Run `common_frame` across both | The invariant **role-frame** is recovered while the gene fillers differ by population | **not started** — the synthetic proof exists; the real-data case does not |
| **C2** | It recovers what the standard toolkit misses | On the C1 case, run single-locus GWAS/PRS, network propagation (HotNet2-style), pathway enrichment (GSEA), colocalization | The token-bound methods return null/inconsistent across populations exactly where fillers differ; Homeostat returns the shared frame | **not started** |

C2 is the whole argument in one experiment: the standard methods are token-bound, so they
*must* fail where the fillers differ, and that is precisely the case Homeostat is built for.
If C1+C2 land on real data, "advance" stops being a claim and becomes a result.

---

## D · Novel-mechanism recovery — "it finds biology, not just re-finds it"

| # | Demonstrates | Method | Pass bar | Status |
|---|---|---|---|---|
| **D1** | Known biology falls out of structure that didn't use it | The §3.2 annotation-recovery falsifier through the *full* pipeline: on candidates whose mechanism was withheld, test whether independently-known annotations enrich in the recovered frame vs. matched background — **preregistered** | Significant held-out-annotation recovery | **not started** |
| **D2** | It proposes something new that checks out | Emit a novel mechanistic hypothesis; confirm against a source **not used** in the derivation (a later-published finding, an orthogonal database, a wet-lab collaborator) | ≥1 novel hypothesis externally confirmed | **not started** — the hardest and most valuable row |

D2 is where a methods paper becomes a discovery. It is open-ended by nature and the one row
that most benefits from a domain collaborator.

---

## E · Generalizability — "an instrument, not a one-off"

| # | Demonstrates | Method | Pass bar | Status |
|---|---|---|---|---|
| **E1** | Zero-tuning transfer to a new disease family | Run the whole pipeline on a metabolic / neuro / cardiac mechanism, changing **only** the domain's role anchors in its universe `.index` (the one registration step) — no engine, no probe, no threshold touched | Recovers a known mechanism in the new domain with no code change | **✅ PASS** — `validation/a1_panel.py` runs the identical pipeline over 8 domains (inflammation, DNA-repair, complement, coagulation, lipid, mitophagy, inflammasome, interferon) changing only the seed+member list; every domain produces a ledger, none abstains |
| **E2** | New roles register without touching the engine | Add a role the current vocabulary lacks; confirm it fires from `.index` rows alone | New role works via vocabulary registration only | **not started** |

E1 is the direct, checkable form of "generalizable": if a new domain costs one `.index`
edit and nothing else, the instrument claim is earned. If it costs a code change, it isn't.

---

## F · Claim discipline (an enforcement, not a test)

Not a cell that goes green — a rule that governs how every result above is reported.

- **The static-data ceiling.** Every output is labeled a **hypothesis**, because the data
  that would confirm mechanism — each person's genotype *and* phenotype together, so the
  mechanism can be watched to move — is gated. The dynamic-data test (canon §12.4) is the
  ceiling that upgrades hypothesis → finding. Until it runs, no row above produces a clinical
  claim, and the README, any talk, and any collaborator hand-off must say so in those words.

---

## Priority order (what to build first, and why)

1. **A2 + A3** — cheap, and they protect every later claim from the "it never actually
   abstains / it isn't deterministic" objection. Pin them as regression tests.
2. **C1 + C2** — the headline. Everything else is preamble to the cross-population case. This
   is where to spend the scarce resource (a real disjoint-filler dataset), and where a
   geneticist's input is worth the most.
3. **E1** — one clean cross-domain transfer converts "works on inflammation" into "is an
   instrument," for the price of one `.index` registration.
4. **B1 + A1 panel** — the quantitative backbone a methods write-up needs.
5. **D1 → D2** — annotation-recovery first (self-contained), then the prospective
   novel-hypothesis confirmation that turns method into discovery.

**Green so far:** the LRRK2 recovery (A1, 1/8), plus **A2**, **A3**, and **B3** fully closed with
real-engine demonstrations (see `validation/VALIDATION_RESULTS.md`). The instrument is shown
deterministic, adversarially abstaining, and carried by convergence rather than any single lens. The
remaining gap is the panel (A1/B1/B2), the cross-population headline (C1/C2), cross-domain transfer
(E1/E2), and novel recovery (D1/D2) — most needing a disjoint-filler dataset or a domain
collaborator, not more code.
