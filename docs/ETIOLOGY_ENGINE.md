# The Etiology Engine — mechanism-role recovery over data-geometry signals

### Deriving a proper etiology for an illness/phenotype **without statistical swamping**, robust to highly fungible gene substitution

**Status:** Design specification, 2026-08-31. Self-contained — written to be reconstructed cold, by a
reader with no prior context. It over-specifies deliberately. Companion canon (formal substrate, not
required for this read): `docs/REGULATORY_DEFICIT_PROGRAM.md` and `docs/THEORY_OF_THE_CASE.md`. The
reasoning engine is **Regenesis** (`mcp__Regenesis__*`), the author's deterministic, provenance-carrying
port of Winston's Genesis story-understanding system.

---

## 0. The one-paragraph version

An illness or phenotype is produced by a **combination** of many weak, sub-threshold signals. Standard
genetics tests one gene at a time, so the loud, already-known signals **swamp** the quiet etiologies
that only matter in combination. Worse, the combination is **fungible**: the same mechanism is realized
by one pool of genes in one group of people and a *different* pool in another (a founder isolate, a
caste, a phenotypic sub-population), because the genes are just whatever that population's deck had to
fill the roles. So a gene-identity lookup ("is *LRRK2* significant?") is a **token match at the wrong
level** — it will always miss the sub-population that solved the same problem with a different token.
The Etiology Engine recovers the **mechanism as a structure of ROLES** and reads out *which genes fill
each role, whoever they are*. It has two layers: **(1)** Peitho-style **data geometry** computes the
relational signals (the lenses); **(2)** the **Regenesis reasoning stack** runs *on top of and using*
those signals to recover the role-structure — recognizing a gene by the **role it plays**, never its
name.

---

## 1. The thesis — why not statistics

- **The effect does not exist at any single locus; it exists in the composition.** Control over a
  regulatory pathway is distributed (metabolic-control summation theorem); most heritability is in the
  long sub-threshold tail (the omnigenic model). An element-by-element association test is *structurally*
  blind to a mechanism carried by the collective, at any sample size.
- **Statistics is not the villain — it is priorless and honest, but too weak** for this shape: the
  contributing elements are weakly associated *and* **fungible** (no single one necessary; an equivalent
  substitutes), and the mechanism lives one level up, as a coherent collective state. Statistics tests
  the element; the mechanism is the pattern the elements hold together.
- **Statistical swamping, named:** any read of population statistics — or a thin slice of signals — is
  silently asserting an *individual* mechanism from a *population* average. Differential outcomes for the
  same clinical presentation across populations are the audit-log of that error's body count. The Engine
  refuses that substitution; that refusal is what makes it *more* rigorous, not less.
- **Fungibility is the crux, and it is why this needs reasoning, not matching.** Because the same
  mechanism is spelled with different genes in different people/populations, the invariant is the
  **role-structure**, and the genes are interchangeable fillers. You cannot recover an invariant by
  matching the variable part. You recover it by recognizing the roles and letting the fillers vary.

---

## 2. The two-layer architecture

**Layer 1 — data geometry (Peitho-style): compute the relational signals.** The author's other work
(Peitho: search a bounded state space for the most parsimonious configuration reaching a goal state,
read with a signed-ternary decision core) supplies the signal layer. Each signal is a **lens** — a
partly-orthogonal, lossy shadow of the truth we cannot buy directly:
- **Differentiation** across *any legitimately-isolatable group* — ancestry at any resolution
  (continent → sub-continent → founder/caste isolate), a phenotypic sub-section, an exposure. The
  partition is a **free, searched variable**, not a hardcoded axis; the read is differentiation
  *magnitude*, direction-free (e.g. max pairwise Fst).
- **Co-expression** across people (GTEx), **co-travel** of variants across populations (1000G/gnomAD),
  **trait-wiring** (the GWAS catalog).
- **Generate, do not calculate.** A lens is a *kill-opportunity / a vote*, never an estimator.
  Convergence across independent lenses is the signal; disagreement kills. Imperfect orthogonality is
  fine here and fatal in a statistical stack, because there is no estimate to bias — only rivals to
  eliminate. (Partial orthogonality → strictly between n and 2n bits: always net-additive.)

**Layer 2 — reasoning (Regenesis): recover the role-structure from the signals.** The story engine
takes the signal-facts and derives **what they imply but never state** — the role each gene plays and
the mechanism they compose — each inference carrying provenance, **abstaining** where nothing follows
(abstention is a result, never fabrication). This is the AI stack reasoning *on top of* the
data-geometry signals: the signals are the evidence; the reasoning is the etiology.

---

## 2b. The substrate — seed known mechanisms, grow the novel composite

The object (the composite etiology) is **grown, never guessed** — but it is grown *over a substrate of
known biology, not from nothing.* This distinction keeps the program honest without making it purist:

- **Authoring known allopathic mechanisms is legitimate — they are the vocabulary, not the answer.** The
  established mechanisms of Western medicine (the NOD2→RIP2 signaling axis, a clearance pathway, a
  resolution cascade) are hand-authored as role-Forms. This is the μ-oracle / the Form library, and it is
  *not* the forbidden move — the forbidden move is seeding the **object** from **guesses** (SDIS's vibed
  edges, a population-differentiation pile). Known mechanisms are established, not guessed. There is no
  need to discard a century of medical research for academic purity; that research **is** the substrate.
- **The novelty is produced by the engine's generative layer, over that substrate.** Three native
  capacities, each measured in the §8 proof or the significance-weighting work:
  - **Auto-written rules (induction).** The engine writes new rules combining the authored Forms (the
    `learned` output — a rule the read wrote itself, seen firing in the §8 proof). Combination is
    computed, not hand-listed.
  - **Significance / surprise.** The improbable-and-coherent composite leads (κ / the significance
    bracket): a chain of known mechanisms that is improbable by idle coincidence yet coherent is exactly a
    candidate **novel** etiology — the sub-threshold combination no single known mechanism names.
  - **Holographic composition** (Wayfinder-style impute + significance-weighting chaining): chain and
    compose the known mechanisms into the multi-hop composite no single one contains — the holographic
    projection at the *mechanism* level (the same move `measuring_agi` calls behavioral holography, §3b).
- **The workflow, in one line: author the known (the substrate), compute the novel (the composite).** This
  is compute-not-guess at the level of *composition*, grounded in real medical knowledge rather than
  discarding it.

---

## 3. The signal→story translation (L2 → L3)

Regenesis reads subject-verb-object **event sentences**, not a frequency matrix. So the data geometry is
rendered in two deliberately-split stages (the pattern proven in the author's ARC_AGI_3 universe):

**L2 — a closed relational-event vocabulary** (computed from Layer 1, judgment-free structs):
| event | source signal | shape |
|---|---|---|
| `DIFFERENTIATES(gene, partition)` | the generalized differentiation lens (Fst) | gene is population-structured across an isolatable partition |
| `COEXPRESSES(gene, gene)` | GTEx correlation | co-functional |
| `COTRAVELS(gene, gene)` | 1000G/gnomAD co-variation | co-inherited |
| `WIRES(gene, trait)` | GWAS catalog | trait association |
| `AMPLIFIES` / `INHIBITS(gene, axis)` | directed pathway data (Reactome) | directional signaling role |
| `ABSENT(gene, lens)` | a lens abstaining | the informational zero (see §4) |

**L3 — the bridge: each event → one fixed SVO sentence, with OPAQUE gene tokens.** Genes are named by
opaque proper nouns (`Gene17`), with a sidecar `Gene17 → LRRK2` map kept *outside* the reasoning. This
is the whole token→role trick: the Form fires on the **verb**, so `Gene17 amplifies signaling` and
`Gene42 amplifies signaling` both receive the amplifier role — **fungibility by construction** — and we
read back which real genes filled each role afterward. Two hard dialect constraints (measured in the
author's universes):
1. **Every fact must be transitive** — a role-verb needs an object, or no rule antecedent can fire
   (`differentiates partition`, never bare `differentiates`; manufacture a mechanical object if needed).
2. **Reserve verbs; generic verbs do not fire.** A specific verb carries a specific provenance; a
   generic one (like "move") is floored by the engine.

---

## 3b. The L2 encoder — role imputation by behavioral characterization (co-localization, not prevalence)

How is a gene's role-fact (`Gene17 amplifies signal`) *derived from data*? By the author's
**`measuring_agi` method — black-box behavioral characterization**, transported from LLMs to genes. It is
the one place a statistical method belongs in the stack, and it is a **characterization tool, never the
significance, and never prevalence.**

- **Characterize the gene as a black box you cannot open.** You do not have its full causal mechanism; you
  have its **behavior under systematic perturbation** (knockouts, stresses, cell states, timepoints).
  Measure the *structure* of that behavior — the shape of its response distribution — not any single
  readout. Content is held free (baseline expression is not the signal) so **process** — the regulatory
  behavior — remains. (`measuring_agi`, verbatim: *"measure the statistical structure of a model's output
  distribution under systematic perturbation… behavioral holography — probing a black box from multiple
  angles to reconstruct its internal cognitive structure."* This is the founder's holographic-impute idea,
  already built.)
- **The role is imputed by co-localization — guilt-by-association in behavior-space.** Two relational
  signals: (a) the gene's **relative position in the cohort** responding to the *identical* perturbation
  battery — *the cohort of other genes is not the background, it is the evidence*; and (b) **where** the
  divergence concentrates — which axes/pathways the behavioral signal co-localizes onto is the mechanistic
  read. The role-class a gene fires is the fingerprint-cluster it sits in — exactly how a Regenesis
  trigger-column **class centroid** is populated from real relational geometry (fix the centroid from the
  behavior, never the input).
- **Why this is not prevalence and not a significance test.** Accuracy/frequency is deliberately held free
  (it carries zero signal — the swamping trap); the signal is the **second-order** structure
  (variance/entropy/composition under perturbation) invisible to a first-order count. The output is a
  continuous fingerprint located in a morphospace by relative geometry — a **positioning instrument**, not
  a p<0.05 verdict on a prevalence.
- **The three guardrails (identical to `measuring_agi`) that keep behavior→role honest:**
  1. **Anytime-valid stopping** (Empirical-Bernstein confidence sequences): σ = the minimum assays to
     characterize a role; you do not over-read a role from too few perturbations — the sequence says when
     it has measured enough. (The canon's σ / specification complexity, applied to assays.)
  2. **A pre-committed perturbation panel**: the assays are fixed in advance, so a role is not fished out.
  3. **External falsification**: every imputed role is a **hypothesis**, confirmed against out-of-band
     ground truth (known pathway membership, a positive-control gene), never proven from co-behavior alone
     — the program's annotation-recovery falsifier and the LRRK2 positive control, at the encoder level.

So L2 is not an open unknown: it is `measuring_agi`'s instrument pointed at genes — statistics as
*characterization*, held to external validation, feeding role-facts to the reasoning stack.

---

## 4. The Regenesis mechanism universe

A universe = a directory of `.rules` bundles + `.index` manifests. Each `.index` row is
`name | trigger-verbs | rules-file | (concepts)`; each rule is one English sentence.

- **Role-Forms (the chassis / always-on recognizer).** Each mechanistic role is a Form. The trigger
  column holds the role-action verbs as **class centroids** (mined from the relational vocabulary —
  never padded with surface synonyms, never gene names). Example shape:
  ```
  amplifier      | amplify enhance potentiate boost       | rules/amplifier.rules |
  transducer     | transduce relay propagate signal       | rules/transducer.rules |
  differentiator | differentiate stratify separate divide | rules/differentiator.rules |
  ```
  Role assignment is `... becomes <role>`: `if x amplifies signaling then x becomes amplifier`.
- **Convergence IS conjunction — the load-bearing mapping.** A Form cannot fire on one token; two
  independent classes must co-occur. That *is* multi-lens convergence, at the rule level:
  ```
  if x amplifies signaling and x differentiates partition then x becomes component
  ```
  A gene fills a role only where **independent lenses agree** — generate-not-calculate as a conjunction
  gate; the holographic combine made mechanical. (Literal objects + a single subject sidestep the
  re-binding gotcha; distinct-subject bridges — `if x becomes amplifier and y becomes transducer then
  signaling becomes active` — encode "different genes, different roles, one mechanism.")
- **The informational zero — abstain ≠ no** (the author's `zero_signal` pattern): an absence is an
  *active* assertion, not a null:
  ```
  if x is absent then x is signal
  if x is signal then x is diagnostic
  ```
  A lens abstaining on a gene (e.g. LRRK2's non-coding variants absent from an exome panel) becomes
  `diagnostic (needs a finer lens)`, **never** "this gene has no role." Fires on the copula.
- **Node-death / near-miss — the `cannot` censor twin.** Where lenses disagree, a censor refuses the
  false-positive role: `if x amplifies signaling and x conserves across partitions then x cannot become
  differentiator` (a gene that is the same everywhere is not population-structured). This is learn-at-the
  -residual: the informative move kills a rival, never confirms the leader.
- **Multi-lens = multi-index.** One `.index` per lens (`genetic`, `physical`, `expression`, `trait`),
  each stand-alone and separately loadable; they **fire and SUM** (orthogonal partials) — that is the
  triangulation.
- **Cross-population combine — the native op.** `common_frame([understand(pop_A), understand(pop_B),
  …])` returns the **invariant role-structure** that different filler-gene-sets realized in each
  population. This is the fungibility recovery, and it is a single Regenesis call.
- **Lean taxonomy.** A mature working universe runs on `then` (deduction) + `cannot` (censor) +
  conjunction gates. `may`/`must` are available but not required.

---

## 5. Authoring discipline (load-bearing; from the working universes)

- **Trigger column = class centroids, never surface synonyms, never gene names.** If a Form won't fire
  on real signal-facts, fix the centroid — **never** rewrite the input to contain a rule's verbs
  (that is the system lying). "0 derivations" is *not* honest abstention until the anchors are verified.
- **Mine, don't fire.** Rules are *found* by GSE decomposition of the signal-facts (CAUSATION/IMPLIES/
  TEMPORAL → candidate rules), then authored small (~2 dozen, not hundreds of flat deductions). Firing
  *assesses* authored rules; it never discovers them.
- **The re-binding gotcha:** a variable bound in antecedent 1 fails to re-match in the OBJECT position
  of antecedent 2 — author bridges with a **literal shape on both sides + distinct subject variables**.
- **Do not type-guard on gene identity.** GSE entity-typing is noisy/sparse on real input; key on the
  **role-verb + mood**, and let the concrete gene ride as an opaque filler.
- Every emitted fact **transitive**; **reserve verbs** by provenance; imperatives emit zero facts.

---

## 6. The honest seam and the data bound

- **The real work is Layer-1/L2 — the role encoder — but it now has a method (§3b) and a substrate
  (§2b), so it is a build, not an open unknown.** Much of the role-vocabulary is *authored* from known
  allopathic mechanisms (§2b); what must be *derived* from data is imputed by behavioral characterization
  (§3b, the `measuring_agi` instrument), held to external validation. In hand today: `DIFFERENTIATES`
  (Fst), `COEXPRESSES` (GTEx), `WIRES` (GWAS). The **directed** roles (`AMPLIFIES`/`INHIBITS`) need
  directed pathway data (Reactome) or a perturbation panel (§3b), not the undirected interaction graph —
  a data-acquisition question, not a method gap. The LRRK2 proof (§8) is feasible because the NOD2→RIP2
  signaling direction is known.
- **Static data gates the claim.** A coherent regulatory mechanism is a dynamical state; static allele
  frequencies / expression may not carry it. Every output is therefore a **hypothesis**, not established
  mechanism, until dynamic / state-resolved data exists. Do not oversell a static-data result.

---

## 7. Empirical grounding (this session, real numbers — why the design is shaped this way)

The first real-data run is the **multi-lens LRRK2 positive control** — a *known* mechanism
(LRRK2–NOD2–RIPK2, an inflammatory-signaling bridge), so it validates the *instrument*, it is not a
novel finding. Measured:
- **No single lens recovers LRRK2** (each misses it a different way — the mechanism is compositional).
- **Convergence over three non-genetic lenses** births NOD2 + RIPK2 and kills most generic hubs (triad
  67% vs hub 20%).
- The **genetic lens as a bare `SAS>EUR` binary is a ~coin flip** (44% of variants "shift") → noisy
  (153/289 born, 60% hub survival). Generalizing it to **differentiation across the five superpopulations**
  restores specificity (86/289 born, 20% hub survival) and recovers NOD2 (rank 29/242) and RIPK2 (rank
  22). **LRRK2 falls to rank 143/242 — robustly mid-pack** — because its signal is *finer than a
  continent* (the SAS average washes out the Indian-cohort founder signal). The threshold was **not**
  lowered to force it back; the mid-pack rank *is* the finding.
- **The lesson that produced this design:** LRRK2 is exactly the case where token-matching and
  coarse-partition matching fail, and **role recognition + finer/any partition** is required. The two
  generalizations — *the partition is a free variable* and *the unit is the role, not the gene* — are the
  resolution, and the Regenesis stack above is how they are computed.

---

## 8. First build — the minimal proof

The smallest thing that tests whether the role-level idea actually fires in Regenesis:
1. Hand-render the **NOD2–RIP2–LRRK2 mechanism** as L3 facts for **two contrasting partitions** (each
   partition emphasizing a different filler gene for the same role).
2. Author ~4 role-Forms + the convergence conjunction + the zero-signal rules + the censor twin.
3. Run `understand()` per partition; call `common_frame([...])` and check it recovers the **invariant
   role-structure** while the filler genes differ.

If it fires, the whole role-level thesis is real in Regenesis, and we scale the L2 encoder onto the real
lenses. If it does not, we learn where — cheaply, before investing in the encoder.

---

## 9. Provenance

The design is distilled from the author's **working** Regenesis universes (primary source, read directly):
ARC_AGI_3 (the `chassis` recognizer + per-task universes, and the L2 `render/events.py` → L3
`story/speak.py` signal→sentence split); MentalAtlas `genesis_universe` (the `then`+`cannot` marker
taxonomy, the multi-`.index` multi-lens split, `zero_signal.rules`, `compositional.rules`); and the
engine's `docs/UNIVERSE_AUTHORING.md`. The reasoning engine is **Regenesis** (`mcp__Regenesis__*`); the
signal layer is **Peitho**-style data geometry; the σ / κ / early-stopping formal substrate is the
author's Specification-Complexity, Significance-Weighting, and pabkit work (canon Appendix B). The **L2
role encoder** (§3b) is the author's **`measuring_agi`** black-box behavioral-characterization method
(`~/Projects/Kaggle_Killer/competitions/measuring_agi` — "behavioral holography": characterize a black
box by the structure of its response under systematic perturbation, role imputed by cohort-relative
co-localization; anytime-valid stopping + pre-commitment + external falsification). The **holographic
composition** of known mechanisms (§2b) draws on **Wayfinder** (`~/Projects/Wayfinder`) + the
significance-weighting chaining.
