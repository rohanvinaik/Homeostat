# The Density Addition Protocol

### A disciplined, repeatable recipe for adding one principled analytical surface (lens) to the Etiology Engine

**What this is.** The Etiology Engine (`docs/ETIOLOGY_ENGINE.md`) grows a mechanism from CONVERGENCE
across data lenses. This protocol is how you add ONE more lens, principled, every time — invoke it
repeatedly. Run infinitely (principled) and it covers the whole ~30,000-gene × every-phenotype space;
but each addition is disciplined, and the additions COMPOUND (§ Compounding) so the system resolves
meaning *above* the literal windows. One lens at a time. Stop at the orthogonality gate (Step 3) if the
lens does not discriminate.

---

## The invariants (never violated — if an addition breaks one, it is not admitted)

1. **A lens is a WINDOW onto RECORDED EVIDENCE** — a real data surface (a public dataset, a database, an
   assay), never an agent's guess and never a hand-authored answer.
2. **Its threshold is EVIDENCE-DERIVED** — from the data's own null / distribution (a permutation null, a
   percentile of the real spread), never a conventional constant. (A neuron is itself a threshold + a
   noise-robust expectation; derive the cut from the evidence, not a textbook.)
3. **It emits TRANSITIVE role-facts with OPAQUE gene tokens** — the lens fires on what the gene DOES (the
   role-verb), never on its name. Every fact has an object or no rule can fire.
4. **NO hard-coded gene→role bindings.** The substrate authors role VOCABULARY (rules/Forms) only; the
   fillers are COMPUTED. Asserting `NOD2 amplifies signal` as input is purposivistic role-assignment
   (canon §3.3) and is forbidden. There is one correct version, and it computes the fillers.
5. **The mechanism GROWS from convergence.** A lens is a kill/vote, not an estimate; the pure decision is
   Detective-pinned; the falsifier stays live (the engine can abstain, fail to recover, or disagree).

---

## The steps (the recipe — run 1→7 per lens)

1. **NAME** the window and its evidence source. *What recorded data, what does it measure, why is it a
   real biological surface?* (e.g. STRING physical interaction; GTEx co-expression; GWAS trait-wiring;
   Reactome directed signaling; a perturbation panel à la `measuring_agi`.)
2. **DERIVE the threshold** from the data's own null/distribution — a permutation null + percentile, the
   spread of the real values — not a default. If the signal has magnitude, **tier it ORDINALLY** (GSE
   marker-on-a-base-primitive; a stronger tier stacks a marker that deepens the chain, §ETIOLOGY_ENGINE
   3b), never a continuous scalar.
3. **CHECK ORTHOGONALITY — the gate.** Does the lens *vary* across the candidate set (marginal coverage
   κ > 0)? A lens that is ~constant adds density but NO discrimination, and can actively mislead by acting
   as a free convergence partner. **A non-discriminating lens is DROPPED or re-scoped** — never credited
   as independent evidence. Greedy rule: prefer the MOST orthogonal next lens (the one that kills the most
   *new* rivals). *Worked failure (2026-08-31): `wires presentation` (GWAS) is TRUE for every gene in a
   presentation-derived cloud → κ ≈ 0 → it trivially converged with differentiation and over-promoted
   TNFSF15 to core. That promotion is an artifact of a non-orthogonal lens, not a finding. The gate
   catches it; the fix is to re-scope trait-wiring to a discriminating contrast or drop it.*
4. **ENCODE the pure decision.** Add the binned signal to `src/homeostat/l2_encoder.data_facts`
   (boolean/tier in → one transitive role-fact out, opaque token). **Detective-pin** it (`detective
   converge …::data_facts`).
5. **REGISTER in the universe** (`universes/mechanism/`):
   - a **Form** — `rules/<role>.rules`: `if x <verb>s <object> then x becomes <role>`, with its
     trigger-verb centroid in `archetypes.index` (the class centroid, NEVER padded synonyms, NEVER gene
     names);
   - a **convergence rule** in `component.rules`: `if x <verb>s <object> and x differentiates population
     then x becomes component` — OR, for a **CENSOR** (negative lens), `if x <over-fires> then x cannot
     become component`;
   - add the verb to the `component` trigger column.
6. **WIRE the shell** (`probes/l2_lrrk2.py` or the real driver): compute the real signal from the evidence
   source, pass it to `data_facts`.
7. **RUN + VERIFY.** `understand()` through the universe: confirm the lens fires, significance grades, and
   — critically — that it DISCRIMINATES (it did not merely lift everything). Run the lint/type/test gate,
   confirm the pin, commit.

---

## The two lens archetypes

- **CONVERGENCE-ADDER** (a positive surface): differentiation, co-expression, physical binding,
  trait-wiring. It deepens a gene's mechanism-membership where it converges with other lenses. *Worked:
  STRING binding sharpened RIPK2 (the one gene with a real physical partner signal).*
- **CENSOR** (near-miss / node-death — a negative surface): promiscuity/genericness, a conservation /
  no-shift signal. It VETOES a false-positive role (`cannot become …`). **This is how you kill the generic
  hubs that convergence alone lets through** — the honest limitation that permissive co-expression admits
  immune hubs is fixed by a *specificity* censor computed from the promiscuity distribution, not by a
  hand-drawn exclusion list.

---

## The compounding — why the additions exceed the sum of the windows

Each lens is a lossy shadow, individually weak and noisy. The founder's point is that they do not just
*accumulate* — the Regenesis reasoning layer does four things ON TOP that lift the combination to meaning
*above* any single window:

- **COMBINE.** Convergence conjunctions fire only where *independent* lenses agree, so a gene confirmed by
  four windows is structurally deeper than one confirmed by one (density → κ → significance).
  Information-theoretically, *n* partly-orthogonal windows yield between *n* and *2n* bits — always
  net-additive, never a stat-stack's correlated-error collapse (we generate, we don't calculate).
- **INDUCE.** From the facts, the engine WRITES ITS OWN general laws (`wire ∧ differentiate ∧ component ⇒
  …`, grounded across the corpus with a multiplicity) — rules no single lens contains. It learns the
  mechanism's *shape*, not just its members.
- **SURPRISE-TUNE.** Significance (κ over the derivation graph) ranks the improbable-and-coherent above the
  common — the deep, rare, cross-lens chain leads. Meaning is graded by how *unlikely-yet-coherent* a
  convergence is, never by frequency. (This is the "surprise" knob.)
- **EDIT / FORGET.** A lens that adds zero marginal coverage (κ = 0) is safely forgotten; a near-miss
  withdraws a node (consolidation / node-death). The graph is editable, self-pruning.

So as principled windows are added, the system resolves mechanism structure that is *above* the literal
evidence — because the reasoning layer combines, induces, weights-by-surprise, and prunes. Scaled
(principled) to the whole gene×phenotype space, every mechanism is GROWN from convergence, none authored.

---

## Invocation

> **"Run the Density Addition Protocol for lens `<X>`."** → steps 1–7, one lens. Honor the invariants;
> stop at the Step-3 orthogonality gate if `<X>` does not discriminate across the candidate set. The
> current lenses are in `src/homeostat/l2_encoder.py` + `universes/mechanism/`; the live state is
> `docs/PROBE_STATE.md`.
