# Regulatory-Deficit Medicine

### A research program for annotation-blind mechanism discovery: imputing coherence from weak, fungible, sub-threshold signals

**Author of record:** Rohan Vinaik
**Document type:** Reconstruction checkpoint — self-contained
**Status:** Ground-zero specification, regenerated 2026-08-30. Parts formalized, parts designed, parts conjectured. The ledger is §15. This regeneration corrects the *conception and method* of an earlier draft that had mislocated the program as a population-statistics pipeline; the formal substrate (§4–§5, §6.12–§6.17), the population-genetics literature (§8), and the LRRK2 biology (§9) are carried forward unchanged. The one thing this document deliberately does **not** specify — the concrete constraint object — is named in §0 and left to the design conversation.

---

## 0. How to read this document

This document exists so that the epistemic state it encodes can be reconstructed cold, without the conversation that produced it. It is written to be handed to an agent or collaborator with no prior context. It over-specifies deliberately.

**Three warnings before anything else, because they are the most likely failure modes of a reader.**

**Warning 1 — this is not a heterodox-medicine document.** It contains no claim that traditional medicine outperforms biomedicine, no claim that a suppressed truth is being recovered, and no appeal to ancient wisdom. Ayurveda enters this program in §6 for one narrow and technical reason: it is a *causally independent source of candidate constraints* on which sub-threshold things combine. Nothing in the program depends on any Ayurvedic claim being true. A reader who classifies this document by surface features — traditional medicine, consumer genetics, an n=1 case, an unfamiliar formalism — and then processes everything downstream as evidence about that classification will reproduce, precisely, the failure this program is about. See §12.6 and Appendix C.

**Warning 2 — the individual case in §11 is not evidence.** It is a sampling-frame specification. Reading it as the argument inverts the structure of the program.

**Warning 3 — statistics is not the enemy, and the method is not a statistic.** The program's critique of standard genetics is not that statistics is biased — statistics is *priorless*, which is honest. The critique is that a priorless, element-by-element significance test is *structurally too weak* to see a mechanism carried by many weak, interchangeable sub-threshold signals holding a collective coherent state (§2). The method that replaces it is **data geometry and classical AI — constraint-driven coherence detection with honest abstention** — not a better statistic. A statistic (PBS, a selection scan, a frequency) is at most a cheap *search-order prior*. A reader who reintroduces a statistic as the method, the significance, or the object of study has left the program (§12.12, Appendix C).

**The one thing left unspecified, named up front.** The program's instrument is only as good as the **constraint object** it runs over — the mechanistic structure that says *which sub-threshold signals must lock together in a coherent mechanism*. In the closest existing biological instance (proteomics-metadata harmonization), that object is a curated cell-line fact table; the analogue for regulatory disease is **not specified in this document and must not be invented from it.** It is the design conversation, seeded by the author's own **SDIS grounding document** (their attempt to sketch a mechanism-with-a-prior). Every "what is the object" question below is deliberately open.

**Reading order.** §1–§3 are the thesis and the instrument argument. §4–§5 are the formal machinery; they are load-bearing and cannot be skipped, but a reader who wants the empirical program first can read §7–§10 and return. §10–§12 are validation and failure modes. §13 is what to actually build.

---

## 1. The claim

### 1.1 Statement

**Allopathic medicine has no per-individual reference-establishment step. It scores an individual against a population-derived reference distribution. This failure is structurally invisible for lesional disease and structurally maximal for regulatory disease.**

A tumor is a tumor against any reference. A lesion is detectable regardless of what baseline you compare it to, because its signal is a discontinuity in kind, not a deviation in degree. A regulatory deviation is detectable *only* against the correct baseline, because its signal *is* a deviation in degree.

The diagnostic apparatus of allopathic medicine — reference ranges, thresholds, cutoffs, ICD categories — is built on population-normalized comparison. There is no stage at which an individual's own setpoint is established before deviation from it is read. There is not even a representation for "this axis has no opinion about this individual." Every lab value returns in-range or out-of-range against a distribution derived from a reference population, and the reference population is overwhelmingly European-ancestry.

### 1.2 What the claim predicts

The claim is not an observation generalized. It is mechanistic, and it therefore *predicts by mechanism* which conditions will be underserved, before looking:

- Conditions whose pathology is regulatory rather than lesional.
- Conditions presenting across multiple organ systems, because the organ-system partition is the axis along which the diagnostic apparatus is organized, and a regulatory failure does not respect it.
- Conditions produced by many weakly-contributing, partially-interchangeable factors, whose effect exists only in their combination.
- Conditions in individuals whose ancestry is distant from the reference population used to calibrate the ranges.

The prediction is confirmed by the residual categories of clinical medicine: idiopathic, atypical, functional, diagnosis of exclusion, medically unexplained. These are not a list of hard problems. They are the shape of a specific instrument's blind spot, and the instrument's blind spot is derivable from its construction.

### 1.3 Illustration: inflammation, and why no single axis is privileged

Inflammation is a useful worked domain, precisely because both its **initiation** and its **resolution** are worth studying and neither is the program's "axis." (An earlier draft leaned on an initiation-vs-termination dichotomy; that framing is withdrawn. There is no privileged carving — initiation is as worth studying as resolution, and the point of the program is combinatorial mechanism, not a favored axis.)

The reason inflammation illustrates the thesis is that its regulation is *distributed and multi-factorial*. Resolution, for instance, is an active, mediated process governed by specialized pro-resolving mediators (SPMs) — lipoxins, resolvins, protectins, maresins — that promote clearance of apoptotic cells (efferocytosis) without compromising host defense; failure to resolve underpins chronic inflammatory disease. Human trials exist but are early (a topical lipoxin A4 analog in infantile eczema; a lipoxin-mimetic oral rinse reducing gingival inflammation; an RvE1-derived ocular agent), and the principal therapeutic limitation is that these mediators are metabolically unstable. The relevant point for the program: whether the population-specific variation is in initiation machinery *or* resolution machinery *or* both, the phenotype it produces will not clear single-variant significance if the variation is distributed across many weak, interchangeable contributors — which is exactly §2.

---

## 2. Why the standard instrument cannot detect it

This section establishes that single-variant statistical genetics *must* fail on this class of phenotype. The argument is structural, not an appeal to statistical power in the ordinary sense.

### 2.1 The summation theorem

Metabolic control analysis (Kacser and Burns) establishes that **flux control coefficients across a pathway sum to one**. Control over pathway flux is distributed by default. In any pathway with more than a few steps, no single enzyme holds enough control for its perturbation to produce a detectable flux effect.

This is a theorem about control topology, not an empirical observation about sample sizes. It says single-variant association studies must fail on flux phenotypes, and it says *why*: the effect being sought does not exist at the locus being tested. It exists in the composition.

### 2.2 Control coefficients redistribute under load

Control coefficients are not invariant. Under increasing load they redistribute toward whichever step is nearest saturation. A pathway that appears robustly distributed at baseline can have a single step acquire near-total control under stress, then relinquish it.

**Consequences:**

- Threshold behavior and stressor-triggered cascade become properties of the control topology rather than narrative constructions.
- The same genotype produces nothing for years and then produces everything at once, which is otherwise difficult to explain. **This is the signature of a meta-stable state (§2.4): a locally-stable configuration that holds until enough of the load shifts and it tips.**
- Any measurement taken at baseline systematically underestimates the control held by the step that matters under load. The instrument is least sensitive exactly where the mechanism lives.

### 2.3 The omnigenic model

The sub-threshold compounding claim has a name in the literature: the omnigenic model (Boyle, Li and Pritchard, 2017). Core genes plus a long tail of peripheral variants acting through regulatory networks, with most heritability residing in the tail.

**Cite it. Do not re-derive it.** A reviewer who supplies it is a reviewer who has decided the program is naive.

### 2.4 The consequence for method — and the correct diagnosis of why statistics fails

The compound conclusion of §2.1–§2.3: for regulatory phenotypes, the effect is distributed, load-dependent, and concentrated in composition rather than in loci. A method that propagates a single causative element at a time, assumes mechanistic certainty at each step, and tests each locus in isolation is a method mismatch — not an underpowered version of the right method.

**Locate the failure correctly.** The standard statistical approach is *priorless*: it looks for significance without deciding in advance what it wants to find. Priorless is honest, and the significance engine is not biased. The failure is that it is too weak for a phenotype with this exact shape:

- the contributing elements are **weakly associated** individually, and
- they are **fungible** — no single one is necessary; a different-but-equivalent element substitutes for it in a given individual, so each element looks weak-or-absent on its own while the mechanism is present in all of them, and
- the mechanism itself exists as a **meta-stable state of coherence** among those elements: a collectively-locked configuration (§2.2) that is the thing to be detected.

An element-by-element association test is structurally blind to this at any sample size, because the object it tests (the element) is not where the mechanism lives. The mechanism is one level up, in the collective state. This is the precise, mechanistic statement of why the program does not use statistics as its method — and why the replacement (§3) is a coherence detector, not a better test.

---

## 3. The methodological inversion

### 3.1 Direction of inference

**Standard:** does variant X associate with phenotype Y, given annotation of X's function?

**This program:** recover the coupling structure that holds a set of sub-threshold signals in a coherent state, *with annotation held out*; then check whether known gene function falls out of the recovered structure as a consequence.

### 3.2 The falsifier

**Recovery of known annotation without having used it.** If the recovered coherence structure reproduces well-established gene function that was never supplied to the recovery procedure, the recovered mechanism is probably real. If it does not, it is not.

This is the program's primary falsification criterion and it is preregistered here. The recovery must be read *through the coherence structure*, not through a frequency proxy for it (a pleiotropy count is a frequency proxy; see §12 and the pathology in §15).

### 3.3 What the inversion buys

Once mechanism is recovered independently of annotation:

1. **Participation in unannotated mechanisms becomes readable.** A gene's role in a pathway nobody has characterized is visible in the coherence structure whether or not anyone has named it.
2. **Sub-threshold functional clusters become visible.** Gene groups whose contribution exists only in composition — and therefore never clears single-variant significance in isolation — appear as coherence.
3. **Purposivistic role assignment is dropped as a premise.** Treating annotation as ground truth requires genetics to be a closed system that is knowably complete and correct. It is neither. §9 gives the existence proof.

### 3.4 The method: a σ-trajectory search with node birth/death (confirmed architecture, 2026-08-30)

The signal is the **coherence of a combination**: sub-threshold elements locked together by the mechanism's structure, so that observing part of the pattern lets you impute the coherent whole, and *the coherence itself is the evidence of mechanism* — improbable-and-coherent, never frequent. The confirmed instantiation of that:

**It is Peitho with automated node birth/death.** Peitho searches a limited state space for the most parsimonious configuration that reaches a defined goal state; here the goal state is *a parsimonious mechanistic etiology for a symptom presentation*. The **search is the σ-trajectory** (§4, §5): drive **H = log₂(surviving candidate mechanisms) → 0** by candidate-elimination, each "test" being a **data-geometry constraint** — a population **co-variation** (signals that lock together across genomes) or a symptom **co-presentation** (symptoms that cluster across people); the mechanism is where the two geometries lock. **The coherence measure is σ** (§4): the minimum constraints to pin a unique mechanism (SC=1), a Blum measure equal to the teaching dimension — *not a frequency*. The **bulk/tail phase transition** (§5.4) is the collective-state / parsimony signal Kuramoto/metastability (§2.4) names in shape.

**The one piece beyond Peitho is node birth/death** — because the mechanism's shape is unknown a priori, the search grows and prunes the state space: **birth** = induction on a residual (a recurring cross-population dyad posits a node); **death** = negative learning on a near-miss (a population/presentation that breaks the coupling — withdraw before it fires, §5.9-adjacent); **consolidation** = safe-forget a κ=0 node (§5.11). The object is therefore **grown by the search, never authored or seeded** (§12.14).

**Two laws keep it honest.** The **σ_sem > 0 falsifiability guard** (§5.9): a frame that makes every observation confirm it reports σ_sem = 0 — memorization, not resolution (`self_confirming_cannot_certify`); never collapse to a self-confirming single mechanism, keep plurality, learn at the residual. And **early stopping at the κ-knee** (§5.5, §10.4; pabkit process-not-endpoint, Appendix B): grow while the bulk amplifies, stop at κ→0; past the knee is memorizing the presentation.

The primary built substrate this assembles (Appendix B): **Peitho** (the mined-zero + signed-ternary elimination decision shell), **harmonizing** (constraint propagation over a domain structure), **genomevault/orthogonal-validators** (committee collective-state + all-zero-margin abstention), **κ** (§5, coverage over a graph — usable *only* over the mechanism-derivation graph, never a generic network, §12.13), and **gse/HDC** (the ternary substrate).

### 3.5 Existing tools in the same direction

Not equivalent to the program, but the nearest existing machinery, and worth using rather than rebuilding:

- **Convergent cross mapping / empirical dynamic modeling** (Sugihara): recovers causal coupling from time series without a mechanistic model; specifically handles the case where correlation fails because variables are dynamically entangled.
- **Transfer entropy**: the information-theoretic formulation of directed coupling.
- **Latent factor decomposition** (ICA/NMF) over multi-omic data: annotation-blind module recovery. Inspecting what loads on each factor *afterward* is the §3.2 validation step, subject to the contamination caveat in §10.

---

## 4. Formal substrate I — σ, specification complexity

Source: *Specification Complexity: Reframing Mutation Testing as a Program Complexity Measure* (Vinaik). ~10,000 lines Lean 4 + Mathlib.

### 4.1 Definition

σ(P, μ) is the **minimum number of tests required to achieve complete specification of program P under mutation policy μ**.

The reframing: a surviving mutant is not evidence of a lazy tester. It is a *behavioral degree of freedom the program's structure leaves unconstrained* — a direction in which behavior could change without any test noticing. The set of surviving mutants maps exactly those dimensions along which behavior is unspecified.

Unlike the mutation score, which is a property of a test suite, σ is a property of the **program**. It measures how many independent constraints are needed to pin down computational identity.

### 4.2 The results that matter here

- **Blum axioms** (Thm 2.5): σ satisfies totality and decidability — trivially for finite domains, substantively for partial programs over infinite domains via an obstruction-package construction. This places σ inside abstract complexity theory where hierarchy and gap theorems apply.
- **Independence from Kolmogorov complexity** (Thm 2.4): there exist programs with K(P) = O(log n) and σ = Ω(2ⁿ/n), and programs with K(P) = Ω(2ⁿ) and σ ≤ 1. Witnesses: a pseudorandom function (short to describe, expensive to distinguish from mutants) and a lookup table with a single distinguishing input (long to write, one test identifies it). **σ measures not how much information a program contains but how much of it is externally observable through testing.** The two notions are orthogonal in a precise sense.
- **Representation independence** (Thm 2.3, machine-checked): σ is invariant under any transformation preserving mutation structure. The whole space of structures with the same kill-profile is one you may move within freely.
- **Redundancy characterization** (Thm 3.11, machine-checked): a constraint is redundant iff it contributes zero information gain — distinguishes no alternative the rest already distinguish.
- **Five-field identification**: σ equals the teaching dimension (Goldman and Mathias 1996), the query complexity of identity testing (Blais et al. 2012), the local testability parameter from coding theory, certificate size from combinatorial complexity, and a parameter governing membership in SpecP.
- **Composition gap**: σ(A∘B) ≤ σ(A) + σ(B) + γ(A,B), with γ bounded by the number of interface mutants and vanishing for independent components.
- **Statistical → exact transition** (Thm 3.4): the bulk→tail phase transition. σ is a candidate formal measure of the gap between statistical and exact learning, connecting to György et al. (2025).
- **Greedy specification is variational inference** (Thm 3.10).

### 4.3 The parameter that governs everything

**The theory is explicitly parameterized by μ.** Different mutation policies yield different σ for the same program. All equivalences are with respect to the concept class induced by μ and an oracle model of observability.

**This is the whole ballgame for the medical application.** μ is the oracle. σ is only as good as the policy against which it is resolved. Everything in §6 exists because of this parameterization, and it is not a weakness of the theory — it is the theory correctly identifying where the unformalizable judgment lives.

### 4.4 Transport to biology

The transport of nouns (following the pattern SSL uses):

| formal | biological |
|---|---|
| program P | a mechanism |
| mutant | a candidate perturbation of that mechanism |
| killing test | an observation that distinguishes it |
| σ(P,μ) | how many independent constraints pin the mechanism down |
| surviving mutant | an unconstrained degree of freedom in the mechanistic account |
| μ | the oracle: which mechanistic alternatives are considered at all |

**σ orthogonal to K is why this transport is worth making.** A mechanism can be compact to state and hard to specify (compact description generating entangled behavior — exactly a regulatory network), or sprawling and easy to specify (few behavioral degrees of freedom). Descriptive parsimony is not the relevant criterion for mechanistic accounts, and σ is the quantity that says so formally.

---

## 5. Formal substrate II — κ, significance weighting, and multi-hop tractability

Source: *Significance-weighting* (Vinaik / Regenesis `regenesis/significance.py`). Part I built and measured; Part II design + conjecture.

This is the answer to: **how do you compose sub-threshold effects across steps without error compounding faster than signal?** It is a candidate coherence measure for the instrument of §3.4 — with the standing caution of §5.12.

### 5.1 Significance is not depth

Scoring derivations flat means a clean 3-hop chain and a deeply composed multi-hop read count the same. The significance weight asks instead: **how improbable is this N-hop reconstruction chain by idle coincidence?** — because improbable-AND-coherent is the interesting case. This is `surprise = −log P` turned *inward* on the engine's own derivations.

Significance is **depth weighted by the branching freedom the universe afforded**. Information content depends on the alphabet. A long string from a low-entropy source carries little information.

### 5.2 The bracket — the answer to error compounding

The prior-free maximum improbability of an N-hop chain with free branching is the **ceiling** ∏(i·C) = Cᴺ·N! ≈ (N·C)ᴺ, where C is the **maximum** out-degree per hop (never an average, or the ceiling leaks). The constant-branching **floor** is bᴺ, b the mean out-degree. True improbability lives in [bᴺ, Cᴺ·N!], and which it is is **read off the real rule graph, never asserted** (compute-not-impose).

Emitted in **log space**, with the **error bar being the bracket width, which grows with N**.

**This is the answer to the compounding problem and it is a refusal, not a solution.** The error does compound. You do not propagate a point estimate through N hops and pretend the deep estimate is as good as the shallow one. You carry the widening bracket explicitly: *the estimate is worst exactly where it is load-bearing, and the honest output carries that.* Ranking survives where magnitude does not, because ordering needs only relative position.

### 5.3 The closed-set finding and the inversion

Measured on the current library: **b ≈ 0.46–0.56** against **C = 9–12**, re-convergence ≈ 1.6, cycles present. b < 1 means most derivable states are terminal. In a **closed** rule set this means bᴺ *shrinks* with depth: a deep chain was nearly forced, therefore unsurprising. This is correct behavior — the instrument reporting that the library is shallow-branching, and correctly abstaining from manufacturing significance it does not have.

**The b < 1 reading holds only while the set is closed.** Induction opens the set, and opening it flips the layer from a passive ranking lens into an **active selection pressure toward long chains**.

### 5.4 Why long chains do not explode

**Re-convergence is submodularity.** Dense, overlapping, cyclic re-entry is submodular saturation of overlapping coverage. Consequences: marginal coverage κ is antitone; greedy hub-first descent is (1−1/e)-optimal; the bulk is bounded. Measured on the dense NLP-WSD graph: knee at ~3% of curriculum (≈91% of H₀ resolved), ≈28× bulk→tail drop, scale-stable across a 4× pool, L(NLP) = 0.528.

Deep chains live in an amplified, saturating **BULK** that converges fast; only the independent **TAIL** is PAC-limited and must be taught. Traversal is **elimination via the informational zero** — the empty banks *are* the signal — turning O(nᵏ) enumeration into O(k·log n) guided descent on a potential field. **You never enumerate the Cᴺ chains.**

### 5.5 Weight by κ, not raw bᴺ

κ = marginal coverage = hub-score = genealogy PageRank over the rule/frame IS-A graph. This resolves the depth paradox:

- deep chain collapsing a cluster of readings (**high κ, bulk**) → high significance → **propose it as a rule**
- deep chain of independent hops (**low κ, tail**) → low significance → **abstain**

In MDL/Levin terms, the rule worth learning is the one that most compresses the improbable-by-chance coherent chain: `surprise = ΔL = log₂[p_H / p_naive]`. A high-κ deep chain *is* a rule-shaped compression.

**Stopping rule: κ → 0.** The bulk/tail knee is the principled halting condition, not an arbitrary depth cap. Significance-weighting is not a detour before induction; it *is* the induction prior.

### 5.6 The spine floor

Two kinds of cruft, two layers. Terminal dead-ends score ~0 under significance. But **reflexive parse junk and generic ungrounded subjects are structurally identical to signal at the chain level** — no κ composition separates them. The fundamental meaning-vs-noise resolution is **intrinsic to the spine** (reflexivity / low-content floor), not derivable from corpus statistics. Corpus statistics are an external, outside-in read and never the fundamental resolution.

**Delivered ranking: the spine floor sinks structural noise; chain_significance orders the survivors; nothing is dropped** (each fact carries a flag). Ranking-only throughout — never a firing gate, so the audit stays clean.

### 5.7 §13 — THE CRUX: submodularity fails at bridges

**The load-bearing finding, and it is negative.**

The easy argument: coverage is submodular ⇒ greedy is (1−1/e)-optimal ⇒ the fixpoint is tractable. **That argument is wrong.** SSL's machine-checked submodularity results rest on coverage over a **fixed** ground structure. In the corpus loop, cover(·) is **not static**: promoting a rule adds an edge to the graph κ is read from. The ground structure is a function of the chosen set.

**The bridge counterexample.** Cluster A reaches node x via rule r′; cluster B is disconnected from A; r is a bridge x → B.
- With S = ∅: adding r′ covers x plus A's small downstream. Marginal gain **small**.
- With T = {r} ⊇ S: adding r′ now reaches x → B, all of B. Marginal gain **large**.

f(T∪{r′}) − f(T) > f(S∪{r′}) − f(S) for S ⊆ T: **diminishing returns fails.** The gain is super-additive. r and r′ are **complementary**, not redundant.

**And this is not an edge case — it is the target.** Every deep inference worth having is a bridge between previously-separate clusters. **The interesting cases are precisely the ones that violate submodularity.** A theory assuming submodularity would be a theory of the boring cases.

**The real object is bounded curvature / bounded supermodular degree** (Feige–Izsak): a function submodular except for a controlled amount of complementarity retains a degraded greedy guarantee, degrading in the supermodular degree *d*.

> **Conjecture (bounded-bridge greedy).** Rule-graph coverage under promotion is monotone with supermodular degree *d* bounded by the number of promotions connecting previously-disjoint components. Greedy max-κ promotion retains an approximation guarantee degrading in *d*; at *d* = 0 it recovers (1−1/e).

### 5.8 §13 transported to biology — the central structural result

**A bridge in biology is a pleiotropic gene joining two previously-separate mechanism clusters.**

A biological pathway graph is the sparse regime, not the dense one: most variants are terminal and propagate nothing; a few are connectors. So §13 is not a caveat about a text-reasoning engine. It is a **prediction about which genes carry the mechanism**:

**The genes where the search guarantee is weakest are the same genes that will never clear single-variant significance.** Bridges are simultaneously the target and the obstruction, in both domains, for the same structural reason — their effect exists only in composition.

This also fixes the form of the biological claim: **quantitative, not binary.** The guarantee degrades in *d*, and *d* is the number of pleiotropic connectors admitted to the candidate set. §7 is the mechanism for bounding *d*.

### 5.9 §14 — the self-confirmation guard is a well-definedness condition

Confirmation must come from the **stated spine**, never from the engine's own derivations. A rule confirmed by its own output reduces H *by construction* while carrying **zero information**: the descent looks fast and means nothing, and L_ind → 1 vacuously. **Without the guard the central quantity is not merely unsafe — it is undefined.**

In Regenesis this is structural, not disciplinary: ANTICIPATED is computed as a DERIVED fact whose corroboration key lies in stated_keys, built from the stated spine by construction. The engine *cannot* confirm from its own output; the shape forbids it. The admissibility test is SSL §4.3's design law, already machine-checked (`self_confirming_cannot_certify`, `falsifiability_pivot`).

**Transported: the confirmation channel must not have been used in the derivation.** This is the exact criterion that decides which validators in §10 are legitimate.

### 5.10 The self-teaching completeness equation

SSL's descent dH/dt = −(N + C(H)) prices external facts N plus intra-text structural amplification C(H). It is a theory of *being taught*. The corpus loop makes teaching endogenous:

**dH/dt = −(N_ext + N_ind(H) + C(H))**

where N_ind(H) is the rate of admissible promotions at entropy H. N_ind and C are coupled: a promoted rule is an edge, so it raises coverage, so it feeds C. C(H) is amplification *within* a text; N_ind(H) is amplification *across* the population.

**The induction split:** I_solve(D) = I_ind(D) + I_ext(D), with **L_ind = I_ind / I_solve**, the self-teaching fraction. The completeness map becomes three-region:

| region | quantity | who resolves it |
|---|---|---|
| known-knowns | L(D) | structure, free (intra-text) |
| **unknown-knowns** | **L_ind(D)** | **the corpus, by induction (inter-text)** |
| known-unknowns | I_ext(D) | a teacher, irreducibly |

I_ind is latent in the corpus and unreachable per read: story A alone does not support the law; A…N together do. It is information carried by co-occurrence across the population.

**Biological transport:** I_ind is the mechanism latent across the cohort that no single genome supports. This is the formal statement of why n=1 cannot carry the argument and why the population must.

### 5.11 Safe forgetting

σ-preserving reduction: a spine edit is safe to forget iff it preserves the significance-weighted closure — iff re-deriving after the prune leaves the σ_sem-witness unchanged. What banks zero significance-weighted coverage is, by Thm 3.11 transported, exactly what can be forgotten *with proof*. Waking is the forward greedy trajectory accumulating the bulk; sleep is redundancy-elimination back to the σ-minimal witness. (Makes rigorous Crick & Mitchison's 1983 reverse-learning conjecture: a spurious memory *is* a zero-κ derivation.)

Relevant here as the pruning operator over accumulated candidate mechanisms.

### 5.12 The standing caution on κ (do not skip)

κ is coverage / genealogy-PageRank over a **graph**. It is a data-geometry coherence measure **only when the graph is the mechanism-derivation graph** — the what-implies-what of the reconstructed combination. Read over a *generic* network (a universal interactome, STRING ∪ GTEx), κ silently becomes a **topology statistic**: a node's participation/hub-score in a pre-existing map, with no person, no phenotype, and no coherence-of-a-specific-combination in it. That substitution is precisely the pathology recorded in §15 (Act 2). A graph measure over the wrong graph is a statistic in disguise. Use κ only over the derivation graph, never the interactome.

---

## 6. The oracle problem and the ensemble

### 6.1 The problem

Everything above is bounded by the completeness of the oracle (μ) against which significance is resolved. **Idiomatic and spurious clustering is a failure of significance driven by an incomplete or over-generated oracle.** This is the unbounded part, defined by taste and intent, and the largest and most obvious scope of failure. It is not a zero-time one-hop solution like an inventory engine; it is genuine medical research.

Conventionally, oracle construction *is* the researcher's expertise — accrued through field experience or careful pre-research and self-interrogation of bias.

### 6.2 The substitution

**No funding, no affiliation, no review board, no researcher.** What is available: unlimited license to explore, and cheap mechanical ideation to flood the μ testing space. **Brute force as a substitute for expertise.**

This works because of a **generate/verify asymmetry**: constructing a good μ is hard, but checking whether a given μ yields coherent σ-structure is mechanical. Expert intuition is a search heuristic over oracle space; dense sampling removes the need for the heuristic.

### 6.3 The ensemble is the bracket

A single expert-constructed μ is a **point estimate**. The program refuses point estimates everywhere else (§5.2); it must refuse this one.

**Variance of σ across a μ-ensemble is not noise around the expert answer. It is the measurement.**

- A coherent combination surviving across widely-varying oracle definitions is **structurally real**.
- A combination appearing only under a narrow band of μ is an **artifact of that partition**.

This is the answer to *"can σ distinguish a real mechanism from an artifact of which two clusters happened to be annotated separately?"* — **Can it? Yes. Does it, automatically? No.** It does so only under an ensemble, and only if the ensemble is genuinely diverse.

### 6.4 Why LLM-generated oracles collapse

**A language model is not an independent sample.** It is trained on the literature that produced the existing partitions. Requesting N candidate carvings yields N draws correlated with consensus — the very partition whose artifacts are to be detected. The ensemble collapses toward the field's own carving, and variance **understates** true uncertainty.

**This is §5.9 one level up:** generator and annotation share a source, so the confirmation channel is contaminated and σ-stability looks better than it is.

Persona prompting (`you are an expert in <field>`) does not fix this. It re-labels draws from the same distribution.

### 6.5 The requirement

A source of non-standard mechanistic hypotheses that is:

1. **Orthogonal** to standard neuro-immunological assumptions;
2. **Non-violating** of validated off-target mechanistic assumptions held as control — no fairy magic;
3. **Principled** — following observations expressly validated in medicine;
4. Prescribing nothing **mechanistically** (not statistically) invalidated and proven unambiguously invalid.

### 6.6 Ayurveda

**Ayurveda satisfies all four, and the reason is technical, not reverential.**

**It is causally independent of the annotation channel.** Every carving in it was made by people with no access to the literature that produced the partitions under test. That is real decorrelation, not a persona drawing from the same consensus in different vocabulary.

**It is systematic rather than folkloric,** so it *spans* a hypothesis space rather than scattering across one. Its carvings can be enumerated, giving coverage rather than anecdote. This distinguishes it sharply from wives'-tale remedies, which prescribe noise nearly as often as signal. (Contrast: barley-germination fetal sex-testing turns out to track real hormonal differences in germination propensity; salt over the shoulder does not. A folk corpus mixes these with no internal principle separating them. A systematic corpus has structure to mine.)

**Its carvings are candidate constraints, not conclusions.** In the instrument of §3.4, an Ayurvedic carving enters as a *hypothesis about which sub-threshold things lock together* — a candidate edge in the constraint object — to be confirmed or eliminated by the same coherence machinery as any other. It is never an authority; it is a decorrelated way of proposing the domain-knowledge structure that §0 flags as the deferred object.

### 6.7 The carvings that are orthogonal

| Ayurvedic construct | What it is, structurally | Why it is orthogonal |
|---|---|---|
| **ama** | Clearance-failure category: accumulated unprocessed substrate when throughput is exceeded | Groups amyloid, atheromatous plaque, urate crystals, lipofuscin as **one kind of thing**. Allopathic medicine has no such category — these sit in neurology, cardiology, rheumatology, gerontology, and the partition is historical accident. **A pleiotropic connector in the §5.8 sense.** Predicts shared upstream mechanism in clearance capacity: efferocytosis, autophagic flux, resolution. |
| **dhatu sequence** | Serial dependency topology: seven tissues, each substrate for the next | Makes a **falsifiable ordering claim** — upstream failure produces downstream deficits in specified sequence. Orthogonal to organ-system carving; directly testable against expression or flux data. |
| **srotas** | Flux-topology partition: channels defined by what flows and where it obstructs | Partitions by transport and obstruction rather than by anatomy. |
| **dosha** | Regulatory-character partition | *Vata* groups neural signaling with peristalsis with circulation — a cross-cutting prediction biomedicine only half-accepted in the 1990s via the enteric nervous system. |
| **agni** | Rate/throughput partition | No allopathic equivalent at all. |
| **prakriti / vikriti** | Per-individual reference and deviation from it | **This is §1.1's missing step, present by construction — and the mined zero of the Peitho state estimator (§3.4).** Diagnosis against the individual's own baseline, not a population distribution. |
| **samanya-vishesha** | Like increases like; opposites decrease | Sign-inverted feedback — negative feedback with explicit reference tracking. |
| **snehapaka** | Lipid-vehicle preparation | Preferentially partitions lipophilic constituents into a lipid vehicle promoting lymphatic uptake, partially bypassing first-pass metabolism. A **pharmacokinetic** encoding, not a phytochemical one. |

**Ayurveda as a control system, stated formally:** prakriti/vikriti is setpoint versus current state — an error signal computed per individual. Tridosha is a signed state vector. Samanya-vishesha is sign-inverted feedback. Agni is throughput; ama is backlog when load exceeds throughput; srotas are flux paths. **Treatment is a function of the deviation vector, not of a disease name.** This is a controller with explicit reference tracking, and it is structurally the same shape as the §3.4 instrument: mine norms from the data itself, place each axis at +1/−1/0 with an explicit abstention state, and take the verdict to be whatever survives elimination.

**The abstention state is load-bearing**, and it is what allopathic diagnostics structurally lack: a lab value returns in-range or out-of-range; there is no representation for *this axis has no opinion about you*. It is the informational zero of §3.4.

### 6.8 The pharmacokinetic thread (secondary but strong)

The Western failure with curcumin and boswellia was extracting single molecules from delivery matrices and finding them bioavailability-limited (curcumin additionally being a canonical pan-assay interference compound). Read one way, a strike against traditional pharmacology. Read the other, **the tradition encoded a PK solution that reductionist extraction destroyed** — trikatu-type formulations co-administer piperine, shifting curcumin bioavailability by over an order of magnitude.

**The convergence worth noting:** the principal therapeutic limitation in resolution pharmacology is that SPMs are metabolically unstable lipid mediators (§1.3). The traditional system's characteristic move is lipid-vehicle formulation. That is a non-trivial mechanistic convergence, not a metaphor.

### 6.9 Oracle phylogeny — weighting the ensemble

**Oracle sources have descent relationships, and convergence must be scored against them.**

| source | relation to allopathic | weight |
|---|---|---|
| **Unani** | Descends through Galenic humoralism into allopathic medicine | **Zero evidential weight on agreement — it is inheritance, not convergence.** Precisely therefore a clean **negative control**. |
| **Ayurveda** | Independent development | Full weight |
| **TCM** | Limited historical contact with Ayurveda; carves differently (zang-fu, meridians, qi/blood/fluids) | Full weight; convergence with Ayurveda is strong signal |
| **Sowa Rigpa (Tibetan)** | Ayurveda-descended | Partial weight — shared descent |

**Convergence across lineages that never touched is signal. Convergence within a lineage is shared descent.** This is the E/I/R filter (§7) applied to oracle sources instead of genomes, and it is what prevents the ensemble collapsing the way an LLM-generated one does (§6.4).

### 6.10 The exclusion criterion, operationalized

The line is **mechanistically disproven** versus **dismissed by association**. The second category is enormous and is where the usable hypotheses are.

**Excluded:** specific anatomical claims contradicted by dissection; rasashastra *bhasma* preparations (heavy-metal toxicology is settled); anything requiring transmission through structures that do not exist.

**Not excluded:** dosha as a functional classification; ama as a clearance category; the dhatu dependency ordering; prakriti as a per-individual reference; srotas as flux topology. These were not falsified; they were mostly never tested as mechanistic hypotheses at all, and were discarded in the same gesture that discarded the mercury.

### 6.11 Over-flexibility is self-policing

The obvious objection — that these categories are semantically elastic enough to map onto anything — **answers itself inside the framework**. A carving that maps onto everything has low specification power, and **σ measures that directly**. An oracle admitting all partitions equally shows up as a low-σ oracle and is downweighted mechanically. The ensemble is self-policing on exactly the failure mode that would otherwise sink it.

### 6.12 Knowability discipline — what an oracle regime can certify

Source: *What a Mutation Regime Can Know About a Function* (Vinaik). Formal core machine-checked in Lean 4 / Mathlib, axiom-clean to the kernel.

§6.1–§6.11 establish *that* the oracle is the binding parameter and give a construction for diversifying it. This subsection supplies the **discipline for auditing any single carving**, including the ones proposed above. It is the reason no carving in this document may be asserted as complete.

**The footprint reduction.** For adequacy, an output operator *is* its footprint — Mov(p) = {r : p(r) ≠ r}, the set of values it changes. Whether a mutant is a non-equivalent survivor depends only on Mov(p) read against I (the reachable outputs) and O (the observed outputs). Where an operator sends the values it moves is invisible. So a regime's power is exactly a family of subsets of the return type.

**The sufficiency characterization (Thm 3.2, machine-checked).** A finite regime Π is sufficient for target class Γ, uniformly over all programs and suites, **iff every target footprint is the union of the Π-footprints it contains.** (An infinite regime obeys a finite-avoidance form, Thm 3.2b.)

**The minimal regime and its size (Cor 4.1).** On n output values the minimal absolutely-sufficient regime is the **n value guards** — "if the result is r, return something else" — of size exactly n.

**The ceiling (Thm 4.5).** A full score holds exactly when O = I: **the suite exercised every value the program can return. That is the whole of what the technique determines, and no more.**

**The cost (Thm 8.1).** The minimum certifying suite has size |f(D)| — one test per reachable value. This is the **teaching dimension**, and it is the same quantity σ identifies in §4.2's five-field result. The knowledge is not only characterized but priced.

### 6.13 The n = 2 trap — the recorded error

**Cor 4.3: the constant regime is absolutely sufficient iff n = 2.** On Booleans, `return true` / `return false` have footprints {false} / {true} — exactly the two guards. For n ≥ 3 every constant footprint has size ≥ 2, so **no constant is a guard**, and the regime is *provably deficient*, not merely underpowered.

**Any binary carving of a mechanism space is a bet that n = 2.** An initiation/termination dichotomy is such a bet, and this is exactly why §1.3 refuses to privilege it.

**Example 4.4 is that error in miniature.** R = {a, b, c}; the program reaches all three; the suite observes only {a, b}. All constants die, so the score is 1. But the fault with footprint {c} is non-equivalent (c ∈ I) and unkilled (c ∉ O). *A perfect score determines nothing about the outputs never observed.*

**Transported:** "allopathic pharmacology covers X" is a fact about **O** — which regulatory modes have agents pointed at them — not a fact about **I** — which regulatory failure modes exist. Even an exhaustive pharmacopoeia certifies only that a mode was *observed*. **n is unknown, and until it is, the space cannot be priced (Thm 8.1) and no regime over it can be called sufficient.**

### 6.14 The structural residual — what no phenotype-reading regime can reach

**Remark 4.6:** if f(x₁) = f(x₂), then p(f(x₁)) = p(f(x₂)) for every output operator. Faults separating two inputs mapped to the same output are **structurally outside the technique's reach**.

**Transported: two mechanistically distinct regulatory failures that present with the same observable phenotype cannot be separated by any regime that reads phenotype.** This is not a power problem and not fixable with more subjects. It is a wall, and it must be crossed by changing what is measured, not by measuring more. This is the formal statement of why §12.4 (missing dynamics) is the binding constraint.

### 6.15 Oracle-relativity — the part that bites hardest

Everything above relativizes to an arbitrary oracle ω : R → Ω recording what the suite's assertions actually observe. Det_ω(p) = {r : ω(p(r)) ≠ ω(r)}, with **Det_ω(p) ⊆ Mov(p)**, equality only for injective ω. Theorems 3.2, 3.2b, 4.5, 5.2, 8.1 all hold with Mov replaced by Det_ω.

**The pseudo-tested method (Prop 9.4, mixed oracle).** A mutant is pseudo-tested iff it is non-equivalent under the *exact* oracle (Mov ∩ I ≠ ∅) while surviving under the *weak* oracle (Det_ω ∩ O = ∅). The regime knows mechanically that the value changed; **what it cannot know is whether the change matters.** The gap **Mov(p) \ Det_ω(p)** is exactly the oracle weakness a human closes by writing an assertion that pins the value.

**Transported: clinical readouts are non-injective oracles.** CRP is a non-injective ω. So is flare/no-flare. A regulatory mechanism that genuinely moves the underlying state but does not move the assay reading is **a pseudo-tested method exactly** — a real effect that no assertion pins.

**The magnitude is measured, and it is large.** Across 122 covered functions in four Python libraries: **43% pseudo-tested under a value oracle, 6% under a crash-inclusive one.** The 37-point gap is pure oracle-dependence. (Only the *magnitude* carries information; the direction is tautological.)

**Consequence for this program:** the fraction of regulatory mechanisms that appear un-implicated is dominated by readout coarseness, not by biology. **A carving derived from what current assays distinguish is a carving of the oracle, not of the mechanism.** Validator strength must be characterized as an ω *before* results are read, not after.

### 6.16 Two further transports worth holding

**Program-independence (Prop 7.2), and why structure-derived oracles are formally preferable.** For output mutation, detection factors through the footprint: Det(p∘f) = f⁻¹(Mov(p)). The operator enters detection only through a **program-independent** object. Program-text mutation has no operator-only invariant. **Transported: this is the formal reason §6.4's preference for structure-derived over annotation-derived partitions is not merely hygienic** — an annotation-based carving depends on the "text" (the literature that produced it), while a structure-derived carving (expression correlation, PPI topology, selection signature) factors through the mechanism. Only the second class can support a uniform sufficiency claim.

**The honest certificate (Prop 5.1).** A partial guard regime {γ_r1 … γ_rk} is sufficient for exactly Γ_max = {g : Mov(g) ⊆ {r1 … rk}}. The usable form this program should adopt: *any regulatory failure confined to the guarded modes is caught*, **with the guarded set a named parameter**. That is a checkable certificate. "We have covered inflammation" is not.

**Where knowability is achievable at all (Cor 4.2, Thm 5.2).** Absolute sufficiency exists only on **finite** return types; deciding sufficiency is deciding footprint containment — polynomial for value tables, decidable for semilinear footprints, **undecidable in general**. The program should assume Prop 5.1's relative certificate is the only object available.

**Coupling is not entailed (Prop 6.1).** A composite's footprint can be strictly smaller than its factors' — killing first-order mutants need not kill higher-order ones. Transported: **certifying the single-step perturbations of a pathway does not certify their compositions.** This is §2.4 arriving from the other direction, and it is a theorem here rather than an observation about statistical power.

### 6.17 Provenance caution

The "evolved over millennia" premise is *not* required by this program (independence is what is required, established by the historical record of contact, not by antiquity). But if any argument leans on iteration depth, note that what is reverse-engineered is a textual tradition (Charaka, Sushruta, Vagbhata) plus heterogeneous regional folk practice plus a 20th-century institutional revival that was nationalist and openly syncretic. **Date the policy observations.** A formulation encountered today may be a 1970s pharmacopoeia product.

---

## 7. The candidate-set filter — E/I/R differential (a search-order prior, never the method)

### 7.1 Structure

Three pools:

- **E** = European-ancestry reference pool
- **I** = Indic / South Asian pool
- **R** = the index individual: genome-wide ancestry Euro-shifted (high ANI/Steppe component), phenotype Indic-typical and severe

**Filter logic:**

- Variant where **R matches E, differs from I** → **deprioritize.**
- Variant where **R matches I, differs from E** → **enrich the search order.** The index case has the phenotype; the Indic pool has it at elevated rates; the European pool does not.

### 7.2 What it is and is not

**It is admixture mapping, inverted and run at variant level on n=1.** It is a **prior over search order**, not a hypothesis test, and above all **not the object of study and not the significance.** The multi-hop coherence problem is combinatorially hopeless under uniform sampling, so what is needed at that stage is not evidence but a **ranking function that makes the search tractable** — one input to the instrument of §3.4, bounding which candidate signals enter the coherence computation.

**It bounds *d*.** By restricting which pleiotropic connectors enter the candidate set before the coherence descent runs, the supermodular degree of §5.7 is constrained *by construction*. §7 and §5.7 are the two halves: prior over search order on one side, curvature bound on the other.

### 7.3 Formalization

The "differs between E and I" step is a population-differentiation statistic. Use the **population branch statistic (PBS)** — a three-population statistic giving a **continuous per-locus ranking**. This converts pile-sorting into a scored priority queue. Per-variant F_ST is the cruder fallback. **PBS is used here and only here — as the search-order prior. It is never the candidate object, never the coherence measure, never the significance (§15, Act 1).**

### 7.4 Scaling out of n=1

ANI ancestry ranges **39–71%** across most Indian groups and runs higher in Indo-European speakers and traditionally upper-caste groups. **ANI fraction is therefore a continuous, measurable covariate across the subcontinent.** So the deconvolution is a regression, not a case study: does the inflammatory-regulation phenotype track ANI fraction, ASI fraction, or neither?

- Tracks ANI → mechanism is on the Steppe/West-Eurasian component
- Tracks ASI → mechanism is on the indigenous component
- **Tracks neither → the most interesting answer**: shared Eurasian variants with differentially penetrant *regulation*

The n=1 case specifies the design; it does not estimate the slope.

---

## 8. Population-genetic substrate

### 8.1 The representation gap, quantified

As of the GWAS Catalog, January 2024: **~78% of included individuals were of European ancestry**, ~11% Asian, ~4% all other groups combined. European-derived polygenic scores show reduced portability across populations. Measured instance: MS polygenic scores explained 4.8% of disease risk in European UK Biobank participants and performed substantially worse in a South Asian cohort.

### 8.2 The structural inversion — the hardest support for the thesis

Reich et al.: **allele-frequency differences between groups in India are larger than in Europe**, reflecting strong founder effects maintained for millennia by endogamy — with an explicit prediction of an **excess of recessive disease** that should be screenable and mappable.

Nakatsuka et al.: of 263 South Asian populations, **81 showed founder events stronger than the Finnish and Ashkenazi populations**. The strongest likely began from **100 founders or fewer** — roughly **ten times** the Finnish effect — and **14 such groups now have census sizes over one million**.

Whole-genome data from ~4,806 individuals recruited through healthcare systems in Pakistan, India and Bangladesh plus 927 from isolated populations: **rare-homozygote levels reaching 100× those in outbred populations**, and the explicit conclusion that founder effects **increase** power to associate functional variants with disease processes, making South Asia **uniquely powerful** for population-scale genetics. The **SARGAM** array and imputation panel exist, optimized for South Asian genomes.

**Put against §8.1: the population with the highest structural power for variant-to-mechanism association is among the least sampled.** A quantified misallocation, and the thesis's hardest empirical support.

### 8.3 The calibration failure, instantiated

HLA-B27 and spondyloarthropathy. Subtype distribution is population-structured:

- **B\*27:05** — the subtype on which the European disease association is calibrated
- **B\*27:04** — Chinese populations
- **B\*27:03** — predominant in Punjabis
- **B\*27:07** — predominant in Pathans
- **B\*27:06 and B\*27:09** — appear to carry **no disease association**

Meanwhile HLA-B27 frequency is **low in North Indian groups (<5%)**, correlating with observed scarcity of AS in tertiary care there. **The Western clinical test is binary presence/absence** — same gene name, different subtype distribution, different disease association, different base rate — and a diagnostic apparatus calibrated on none of it. **Use this as the worked example.** It is the thesis in one gene.

### 8.4 Selection as context (and the retired validator)

Immune loci are the most selection-scarred region of the genome, and South Asia has a distinct pathogen history — mycobacteria above all (India accounts for roughly half of new leprosy cases worldwide). A selection signature is *thematically consistent* with real mechanistic difference, and a published selection scan (iHS, XP-EHH, CLR) can serve as a weak, annotation-free contextual prior.

**But note the empirical result (2026-08-30, committed; §15, Act 3):** a **selection-signature enrichment validator** built on the E/I/R pile — testing whether the pile is enriched for selection signatures vs. matched controls — **was retired** after it failed under honest LD correction (a naïve pass at permutation p = 0.0005 collapsed to p = 0.985 once the 1 Mb window, not the variant, was made the exchangeable unit). Selection enrichment is therefore **not a legitimate validator** of the program; it is at most weak context. This corrects an earlier draft that named it "validator #1."

---

## 9. LRRK2 — the existence proof

**This gene alone establishes that purposivistic role assignment fails in exactly the way the program claims, and that the failure is population-structured.**

- Annotated as a **Parkinson's disease gene**, characterized in European familial PD cohorts. Role locked in early.
- The first leprosy GWAS found a **striking overlap between leprosy risk factors and Crohn's disease**. Extended to type-1 reactions (the excessive inflammatory episodes in leprosy), **a majority of risk variants were shared between T1R and IBD**.
- **LRRK2 modulates the strength of Nod1/2-Rip2 signaling by enhancing Rip2 phosphorylation.** LRRK2 deficiency markedly reduces macrophage cytokine production upon NOD2 activation.
- **LRRK2 and NOD2 proteins physically interact in macrophages**, the interaction strongly impacted by the NOD2 variant; joint effect produces reduced antimycobacterial response.
- The LRRK2 variants involved show **antagonistic pleiotropy**.
- In Indian cohorts, **LRRK2 rs1873613** is associated with leprosy outcome through the NOD2-mediated pathway; the minor allele/AA increases risk, the major allele/GG confers protection.
- LRRK2 also maintains mitochondrial homeostasis and regulates innate immune responses to *M. tuberculosis*.

**Why it is the whole thesis in one gene:**

1. Function misassigned because characterized in the wrong population against the wrong disease.
2. Actual mechanism is inflammatory-response regulation.
3. Recovered only because someone ran the analysis in a South Asian/East Asian pathogen environment.
4. **Antagonistic pleiotropy** makes single-role annotation *structurally* wrong.
5. It is a **pleiotropic connector** (§5.7/§5.8) joining the neurodegeneration cluster to the mycobacterial-immunity/IBD cluster.
6. Its effect is visible **only in composition** (the LRRK2×NOD2 epistatic interaction), which is why single-variant analysis stopped at "Parkinson's gene."

**Use LRRK2 as the positive control for the whole pipeline.** Any method that cannot recover the LRRK2–NOD2–RIPK2 coherence from annotation-blind data — recovered as a *coherent combination*, not as a hub in a generic graph (§15, Act 2) — is not working.

---

## 10. Validation architecture

### 10.1 The governing criterion

From §5.9: **the confirmation channel must not have been used in the derivation.** A validator sharing a source with the derivation reduces H by construction while carrying zero information. This decides which validators are legitimate.

### 10.2 Validators, ranked (corrected 2026-08-30)

| validator | independent of derivation? | verdict |
|---|---|---|
| **Recovery of known annotation** without using it (§3.2), read *through the coherence structure* | Partially contaminated | **Primary, with preregistration** — see below |
| **Cross-oracle convergence** across independent lineages (§6.9) | Yes, if phylogeny-weighted | **Legitimate** |
| Selection-signature enrichment of the candidate pile | Uses no gene annotation | **RETIRED (§8.4): failed under LD correction; not a validator.** |
| Annotation-derived confirmation of annotation-blind modules | No | **Self-licking. Excluded.** |

**Two corrections from the empirical arc (§15):**
1. Selection-signature enrichment, previously named "primary," is retired — it did not survive honest LD correction and, worse, in practice it measured the generic graph rather than any coherence of the candidate combination.
2. The annotation-recovery falsifier must be read **through the coherence structure**, not through a frequency proxy for it. A *pleiotropy count* is a frequency proxy: it "passes" by measuring the generic network's topology, not the recovered combination. Preregister exactly which annotations count as independently recovered and how coherence — not count — is read, *before* running.

### 10.3 What replaces "selection as a weighting"

An earlier draft proposed feeding the selection signal as a soft weighting into the coherence math. That was tried (feeding PBS as a κ teleportation prior) and it **demoted** the known connectors rather than lifting them (§15, Act 4). The selection/population signal is a **search-order prior (§7)** and nothing more. It does not enter the coherence measure.

### 10.4 Stopping rule

**κ → 0**, the bulk/tail knee (§5.5). Not an arbitrary depth cap, not a p-value threshold, not exhaustion. Nothing external will say when to stop; this stopping rule is the replacement and must be made binding in advance.

---

## 11. The n=1 case — proper role and hard limits

### 11.1 What it is for

The index case is an **ancestry-discordant sampling-frame specification**: genome-wide Euro-shifted, phenotype Indic-typical and severe. It identifies the informative contrast (§7) and supplies a prototype filter that can be run at population scale over the ANI/ASI cline. **A tail point specifies the design. It does not estimate the slope.**

### 11.2 What it is not for

It is not evidence for any mechanism. I_ind (§5.10) is precisely the information latent across a population and unreachable per read: one genome does not support the law; the cohort together does. **This is the formal statement of why n=1 cannot carry the argument** — from the program's own machinery, not external convention.

### 11.3 A recorded internal inconsistency

An argument in circulation holds that the *count* of already-flagged risk markers carried by the index case indicates phenotype **severity**. **This does not survive the program's own premises.** Those markers are on a consumer array because they reached significance in single-variant, predominantly European GWAS; the count is substantially a property of **panel construction**. An argument that annotation-based single-variant assignment is unreliable cannot take annotation-based single-variant hit counts as its premise. The severity claim needs an independent measure (phenotypic, biochemical, longitudinal) or should be dropped.

### 11.4 Narrative framing devices

Rare-phenotype narrative framings are legitimate *as expository devices* for the compounding argument. They carry **zero evidentiary weight** because a contested-existence trait has no definable reference class. If any such state is to enter as data, it must be characterized directly — autonomic measures, duration, trigger, refractory period — not named.

### 11.5 Data quality of the index genotype

The available genotype is a consumer **v5 array (GSA chip)**: ~600k pre-selected SNPs, screening-grade, not sequencing. Several functional pharmacogenomic loci are absent and uncallable (CYP2D6, CYP1A2, CYP2A6, COMT rs4680, SLCO1B1, VKORC1/CYP2C9, TPMT/DPYD, RYR1/BCHE). Report-layer interpretations not present in the parsed export are **not independently verifiable** and must be tiered separately. WGS is required before any variant carries clinical or analytic weight. (The array's content is itself one of the normalization failures the thesis describes — §8.3.)

---

## 12. Failure modes

Enumerated so they are not rediscovered.

**12.1 Oracle collapse (§6.4).** LLM-generated ensembles correlate with consensus; variance understates uncertainty. **Mitigation:** structure-derived partitions and genuinely independent traditions with phylogeny weighting (§6.9).

**12.2 Identifiability under free-form mapping.** Inferring an objective from an observed policy is underdetermined. **Mitigation:** the mapping must be computed by *elimination over signed axes with an abstention state* (§3.4), not fitted. Elimination and abstention both *reduce* the verdict space, so the structure cannot retrodict everything. Plus §6.11: over-flexible oracles show up as low-σ.

**12.3 Self-licking confirmation (§5.9, §10.1).** The most dangerous failure because it *looks like rigor*: objections, caveats, fast descent, zero information. **Mitigation:** the stated-spine guard, enforced structurally.

**12.4 Missing dynamics.** Deconvolution requires state transitions. A static genotype array has no time axis and no perturbation, and a meta-stable coherent state (§2.4) is a *dynamical* object. **This is the binding constraint on the full program**, and it is a data problem, not a conceptual one. Longitudinal multi-omic sampling through state changes — ideally flare-to-remission — is what the method actually needs. Everything in §13 is what can be done before that exists.

**12.5 Constant transfer across regimes.** SSL's measured constants (L = 0.528, ~3% knee, 28× drop) were measured on a **dense** IS-A graph. The rule graph and the biological pathway graph are **sparse**. Structure transfers; constants do not (§5.7).

**12.6 Classification-first reading.** A reader who sorts this program by surface features and then processes all subsequent content as evidence about the classification will produce fluent, confident output that carries zero information — §12.3 performed on the document. See Appendix C.

**12.7 Comparison-class inflation.** The defensible claim is *not* that traditional systems outperform biomedicine on outcomes. The claim is that they are **hypothesis generators with high prior density in an under-searched region of partition space** — a claim about search strategy.

**12.8 Ethnic-package framing.** Physical phenotype does not index an ancestry-linked gene package. The operationalizable variable is a **measurable ancestry component** (ANI fraction, characterized founder effects) — never a language family, folk category, or appearance.

**12.9 Asserting n.** Any binary carving is a bet that n = 2 (§6.13). No partition in this document may be described as covering a space; the honest form is Prop 5.1's relative certificate.

**12.10 Reading O as I.** A statement about which mechanisms have been observed/drugged is a statement about the observed set; treating it as the reachable set reads a passing score as a claim about I (§6.13).

**12.11 Oracle-collapsed mechanisms (pseudo-testing).** A mechanism that moves the underlying state but not the assay reading is reported un-implicated regardless of truth (§6.15). Characterize every validator as an ω *before* reading its results.

**12.12 Statistics-as-method (the recorded death — see §15).** Reaching for a statistic (frequency, association, enrichment, population-differentiation rank, network participation/hub-score, a p-value, a pleiotropy count) as the *method*, the *significance*, or the *object* — instead of a search-order prior — is the specific failure this program most recently committed. It feels like rigor. It was done four ways on 2026-08-30 and failed every way. **Mitigation:** the method is constraint-elimination coherence over the derivation graph (§3.4); a statistic is only ever the §7 prior.

**12.13 Coherence mis-imagined as a graph statistic.** A graph measure (κ, participation) over a *generic* network is a topology statistic in disguise (§5.12). Coherence must be read over the mechanism-derivation graph, and the working detector is constraint-elimination (§3.4), not coverage over a pre-existing interactome.

**12.14 Inventing the constraint object.** The domain-knowledge structure that says which sub-threshold signals lock together (§0, §3.4) is *not specified* and must not be fabricated to make the pipeline runnable. Guessing it (the PBS pile, the generic interactome) instead of building it with the author and SDIS is the root under Acts 1–2 of §15.

---

## 13. Concrete first work

All runnable with no funding, no affiliation, and no data-access committee. Ordered so the object is built before the instrument runs over it.

### 13.1 Specify the constraint object (WITH the author; SDIS-seeded, now in hand)

The first work is not a run; it is the design conversation that specifies Homeostat's analogue of harmonizing's cell-line fact table — the mechanistic structure saying which sub-threshold signals must lock together. **SDIS is now in hand** (Appendix B): its candidate constraint edges (the neuro↔immune coupling) enter as *hypotheses to confirm or eliminate by coherence*, never as the object; its **genetic summary is the concrete first signal input** (the index case's ✓/○-tiered sub-threshold set). Also admit Ayurvedic/cross-tradition carvings as *candidate constraints* (§6.6). Expect the computed coherence to differ from SDIS — likely with **no single driver** (§2.1) rather than SDIS's dopamine root. **Do not proceed to §13.3 with a guessed object (§12.14), and do not adopt SDIS as the object because it is convenient.**

### 13.2 The E/I/R filter — the search-order prior

**Inputs:** 1000 Genomes / gnomAD (SAS + EUR allele frequencies); the index export for R. **Procedure:** compute PBS per variant across E, I, R; rank. **Output:** the bounded-*d* candidate set the coherence descent runs over (§7). **Cost:** zero. This is a prior, not a validator (§8.4 corrects the earlier framing).

### 13.3 LRRK2 as positive control, read through coherence

Run the coherence instrument (§3.4) blind and check whether the LRRK2–NOD2–RIPK2 combination is recovered as a *coherent combination* without annotation input. **If it is not, the method is not working.** Do this before trusting any novel output — and verify it is recovered as coherence, not as participation in a generic graph (§15, Act 2).

### 13.4 Oracle-ensemble σ-variance on a known partition

Take a partition where the answer is known (the leprosy/Crohn's/T1R overlap). Generate carvings from Ayurveda, TCM, Unani (negative control), and structure-derived methods. Measure σ-variance across the ensemble to calibrate whether ensemble variance behaves as §6.3 predicts before it is used on unknown structure.

### 13.5 Free resources

- **1000 Genomes, gnomAD** — population allele frequencies
- **STRING, Reactome, BioGRID** — network topology (a *substrate for the derivation graph*, never the coherence object itself — §5.12)
- **OpenGWAS / IEU** — GWAS summary statistics at scale
- **GTEx** — expression across tissues
- **Genes & Health** — ~50,000 British Pakistani and Bangladeshi individuals with linked records; the right ancestry range and phenotypes. Applied-for, the target cohort.
- **NCT04698291** (Queen Mary) — profiling how genetic variants regulate SPM production in chronic inflammatory conditions, in Genes & Health, with lipid-mediator profiling, efferocytosis and T-cell assays. **The resolution axis, right population, right covariates, already collecting** — the single most relevant existing study.
- **GenomeAsia 100K, IndiGen** — South Asian reference panels; **SARGAM** — SA-optimized array/panel

---

## 14. Open problems

1. **Specify the constraint object** (§13.1). The central unbuilt piece; SDIS-seeded, author-led.
2. **Measure *d*** (§5.7). The bounded-bridge conjecture is quantitative; the supermodular degree must be measured on the actual derivation/pathway graph. Measurement precedes proof.
3. **Combination versus partition artifact** (§6.3). Resolved *in principle* by ensemble σ-variance; §13.4 is the calibration.
4. **L_ind on biological corpora** (§5.10). Defined but unmeasured outside text.
5. **Dynamics** (§12.4). No time-series substrate currently in hand — the binding constraint.
6. **Sheaf condition for biological composition.** Whether mechanism composition satisfies the sheaf condition (§4.2) determines whether γ in the composition gap is tractable.
7. **Phenotype definition.** Unresolved and consequential. Candidate anchors: CRP trajectory; SPM profile; efferocytosis capacity; time-to-resolution after standardized challenge (the most thesis-aligned, since it reads the mechanism directly).
8. **Oracle enumeration completeness.** How many carvings a systematic tradition contains, and when the space is covered. Unformalized.

---

## 15. Status ledger

**PROVED (machine-checked; cite, do not re-derive):**
- σ satisfies the Blum axioms (Thm 2.5); σ independent of Kolmogorov complexity (Thm 2.4); representation independence (Thm 2.3); redundancy = zero information gain (Thm 3.11); five-field identification; composition gap σ(A∘B) ≤ σ(A)+σ(B)+γ(A,B); statistical→exact transition (Thm 3.4); greedy specification is variational inference (Thm 3.10).
- SSL: coverage submodularity, marginal antitone, greedy bound, resolution bulk bounded — **over a static ground structure only**; `self_confirming_cannot_certify`, `falsifiability_pivot`.
- **Knowability (Lean 4/Mathlib, axiom-clean to kernel):** footprint characterization (Thm 3.2, `footprint_characterization`) and its general form (3.2b); value-guard basis (Cor 4.1, `absolute_iff_guards`); constants sufficient iff n=2 (Cor 4.3, `constants_iff_card_two`); the ceiling (Thm 4.5, `ceiling`); coupling not entailed (Prop 6.1, `coupling_fails`); subsumption = footprint containment (Prop 7.1); detection factors through footprint (Prop 7.2, `det_factors`); minimum certifying suite (Thm 8.1); pseudo-testedness under mixed oracle (Prop 9.4, `pseudo_tested_mixed_iff`).

**BUILT AND MEASURED (formal substrate):**
- Significance layer Part I (§5): κ, the bracket, depth pass, per-universe graph measurement, spine floor.
- b ≈ 0.46–0.56, C = 9–12, reconvergence ≈ 1.6 on the current library.
- SSL constants on the dense NLP-WSD graph (L = 0.528, ~3% knee, 28× drop) — **regime-bound, do not transfer.**

**BUILT AND MEASURED (the coherence instrument, in other domains — primary sources, Appendix B):**
- Constraint-propagation coherence on biological metadata (harmonizing `symbolic_healing.py`); committee collective-state with all-zero-margin abstention on 3.7M genomic positions (genomevault); domain-agnostic extraction (orthogonal-validators); per-individual mined-zero + signed-ternary elimination, mutation-pinned (Peitho). These are the reusable instrument, over an object still to be specified (§13.1).

**THE RECORDED DEATH — statistics substituted for the coherence method (2026-08-30, all preregistered and committed):**
- **Act 1 — the object was a statistic.** The E/I/R PBS pile (a population-differentiation statistic) was treated as the candidate object. PBS is a §7 search-order prior, not the object.
- **Act 2 — the "mechanism" was generic topology.** Variants were mapped to the universal interactome (STRING ∪ GTEx) and "bridges" read as community-participation. gnomAD-vs-Pan-UKBB replication: swap the whole cohort, 98.7% of participation values identical while PBS differs greatly — topology, not population signal.
- **Act 3 — the validators were statistics.** Selection-enrichment FAILED under LD correction (p 0.0005 → 0.985; §8.4, now retired); annotation-recovery used a pleiotropy count (a frequency proxy) and "passed" only by measuring the generic graph (§10.2, now corrected).
- **Act 4 — making the statistic load-bearing broke everything.** Top-K PBS restriction broke the gates (0/8 configs replicated); PBS as a soft κ prior *demoted* the known connectors (§10.3). Across four operationalizations, **no configuration where a statistic does the work AND the analysis holds.**
- **The diagnosis:** statistics is not biased — it is underpowered for a fungible, coherence-borne mechanism (§2.4); a graph measure over the wrong graph is a statistic in disguise (§5.12); and every failure quietly *guessed the object* instead of building it (§12.14). The fix is the constraint-elimination instrument (§3.4) over an author-specified object (§13.1), never another statistic.

**DESIGN + CONJECTURE (nothing proved):** bounded-bridge greedy (§5.7); N_ind(H), the split I_solve = I_ind + I_ext, L_ind (§5.10); consolidation as free-energy minimization; **the entire biological transport (§§4.4, 5.8, 6–10) — argued, not demonstrated.**

**EMPIRICALLY ESTABLISHED (external literature):** GWAS representation figures; PRS portability degradation; South Asian founder effects, ANI/ASI cline, rare-homozygote rates; HLA-B27 subtype structure; LRRK2–NOD2–RIPK2 biology and its population-structured discovery; SPM biology and early-phase trials; metabolic-control summation theorem; omnigenic model.

**NAMED RISK:** the coherence instrument may be sound while data quality, not method, remains the limiting factor. A meta-stable coherent state is dynamical; static allele frequencies may not carry it at all (§12.4, §11.5). The honest static-data deliverable is a demonstration that statistics on static frequencies over a generic network cannot recover regulatory mechanism — shown, not asserted.

---

## Appendix A — Glossary

| term | meaning |
|---|---|
| **σ (sigma)** | Specification complexity: minimum tests to completely specify P under mutation policy μ. Property of the program. |
| **μ (mu)** | Mutation policy = **the oracle**. Which alternatives are considered at all. The unformalizable parameter. |
| **κ (kappa)** | Marginal coverage / genealogy-PageRank over the rule/frame graph. A coherence measure **only over the mechanism-derivation graph** (§5.12); over a generic network it is a topology statistic. |
| **fungible signals** | Elements where no single one is necessary; an equivalent substitutes in a given individual, so each looks weak alone while the mechanism is present in all (§2.4). |
| **meta-stable coherence** | A collectively-locked state among many weak elements that holds until enough load shifts and it tips (§2.2, §2.4). The target of the instrument; Kuramoto is its conceptual shape. |
| **coherence detector** | Constraint elimination over a domain-knowledge structure, with honest abstention (§3.4). Not a frequency, not a bare order parameter, not participation over a generic network. |
| **constraint object** | The mechanistic structure saying which sub-threshold signals lock together. Homeostat's analogue of harmonizing's cell-line fact table. **Deferred; SDIS-seeded (§0, §13.1).** |
| **mined zero / informational zero** | The per-individual baseline mined from the data (= prakriti/vikriti); and the abstention state "this axis has no opinion here" — both load-bearing (§3.4, §6.7). |
| **bulk / tail** | Bulk = correlated, overlapping coverage that resolves fast. Tail = independent, PAC-limited, must be taught. |
| **pleiotropic connector** | A gene joining two previously-separate mechanism clusters; largest κ jump; the target and the obstruction (§5.7–§5.8). In §5.7 language, a bridge. |
| **spine** | The stated, external substrate. Confirmation must originate here (§5.9). |
| **abstention (0)** | An axis explicitly having no opinion. The representation allopathic diagnostics lack. |
| **ANI / ASI** | Ancestral North Indian / Ancestral South Indian. ANI 39–71% across most Indian groups. |
| **PBS** | Population branch statistic. The §7 search-order prior — never the object or the significance. |
| **SPM** | Specialized pro-resolving mediator: lipoxins, resolvins, protectins, maresins. |
| **efferocytosis** | Clearance of apoptotic cells by phagocytes; central to resolution. |
| **T1R** | Type-1 reaction: excessive inflammatory episode in leprosy. Shares most risk variants with IBD. |
| **ama / prakriti / vikriti** | Ayurvedic clearance-failure category / constitutional baseline / current deviation (§6.7). |
| **footprint Mov(p)** | The set of values an output operator changes. For adequacy, an operator *is* its footprint. |
| **ω (omega)** | Oracle: what a suite's assertions actually observe. Non-injective ω collapses distinct values into one class. |
| **pseudo-tested** | A mechanism whose perturbation genuinely changes the state while every observed output stays inside one ω-class. Real effect, no assertion pinning it. |
| **d** | Supermodular degree: how many pleiotropic connectors. Governs the degraded greedy guarantee. |

---

## Appendix B — Source documents

**Formal substrate (the author's papers) — the σ-trajectory-search machinery (§3.4):**
- `specification_complexity_paper.md` — σ, Blum axioms, Kolmogorov independence, five-field identification, composition gap, sheaf theory. ~10,000 lines Lean 4. **σ is the coherence measure.**
- **Semantic Specification Learning** (`~/Projects/rohan-vinaik.github.io/papers/Core Documents/Semantic_Specification_Learning/` — `00_CONCEPTUAL_FRAMING`, `01_PAPER_SKELETON`, and the exact-learning sibling `06_EXACT_SPECIFICATION_LEARNING`) — understanding as the σ-trajectory (drive conceptual entropy to zero by candidate-elimination); the completeness equation and the bulk/tail transition; **the σ_sem>0 falsifiability guard** (`self_confirming_cannot_certify`); node birth = induction, node death = negative-learning withdrawal. **The primary source for §3.4's architecture.**
- `SIGNIFICANCE_WEIGHTING.md` — κ, the bracket, the §5.7 bridge crux, the §5.9 guard, N_ind, safe forgetting. Part I built; Part II design.
- **pabkit** (`~/Projects/pabkit` — `docs/process_makes_perfect.md`, `docs/mathematical_formalism.md`) — Process-Aware Benchmarking: judge the learning *trajectory*, not the endpoint; **early stopping** at the loss minimum. The source for §3.4's κ-knee parsimony halt and the small-n overfitting guard (structured rule-formation vs. memorization).
- `knowability_ieee.pdf` — *What a Mutation Regime Can Know About a Function*. Footprint reduction, sufficiency, value-guard basis, ceiling, decidability spectrum, oracle-relativity, pseudo-tested method. Machine-checked Lean 4/Mathlib. **The auditing discipline for every carving in §6.**

**The coherence instrument (built, in other domains — read these as the primary sources for §3.4, not this summary):**
- **harmonizing** (`~/Projects/Kaggle_Killer/competitions/harmonizing/src/symbolic_healing.py`) — constraint propagation over a domain-physics fact table, on biological metadata. The closest existing instance of the object + instrument.
- **genomevault** clinical committee (validated on 3.7M positions) and **orthogonal-validators** — committee collective-state with all-zero-margin abstention; the domain-agnostic version.
- **Peitho** (`~/Projects/Peitho`) — per-individual mined-zero + signed-ternary elimination + informational-zero abstention, mutation-pinned. The state-estimator + decision half; retail domain is incidental, the architecture is the argument.
- **COEC** (`~/Projects/COEC-Framework`) — the theory/vocabulary: constraint-trajectory computation, metastable holding states, order parameter, residual-in-the-collective.
- Portfolio reference: `~/Projects/Kaggle_Killer/DATA_GEOMETRY_ARCHITECTURE.md` (OTP, Informational Zero, COEC, GSE, HDC).

**The deferred object (SDIS — now in hand, as a candidate carving):**
- **SDIS** — the author's hand-built, intuited version of this program's information-theoretic
  principle: a coherent multi-system mechanistic construction (the "Systemic Dopaminergic
  Insufficiency Syndrome" model) assembled by vibes rather than computed. Two files: a
  **genetic summary** (the more accurate version — the index case's sub-threshold signal set,
  tiered ✓verified / ○reported, with the informational-zero discipline built in) and the fuller
  **SDIS master report**. It is a **candidate carving and a characterization target, NOT the
  object and NOT ground truth**: dopamine-centric (the loud-signal risk incarnate — §2.4), n=1
  (a design-frame, §11), and written as a 100%-retrodiction story (the self-confirming pattern —
  §5.9, §12.3), with its "central driver" variants (DRD2 A1, COMT Val/Val, BDNF Met) only
  ○reported, not on the array. Its **value**: it is a specimen of the output type (what the
  machine should *compute*), a source of candidate constraint edges (the neuro↔immune coupling:
  D2-on-immune-cells → NF-κB, the vagal reflex, IL-23/Th17, BH4-depletion → less dopamine), and
  the index-case signal set. The machine's job is to **recover its defensible core and correct
  its over-reach** — likely finding a coherence with **no single driver** (§2.1: distributed
  control → no king). *(Files currently at the session-upload path; a durable home is TBD — do
  not copy personal genetic data into a pushable repo without the author placing it, per the
  in-place / hash-pinned pattern in `docs/REFERENCE_MANIFEST.yaml`.)*

**Data / index case:** index-case genetic material — see §11.5 for tiering discipline. **Screening-grade. Not evidence.**

---

## Appendix C — Anti-patterns for an agent picking this up cold

**Do not validate the premise for coherence.** It has been stress-tested. Objections at the level of "have you considered identifiability," "is this falsifiable," "n=1 cannot establish causation," "traditional medicine lacks outcome data" are answered in §12.2, §3.2, §11.2, §12.7. Re-raising them is §12.3.

**Do not reach for a statistic as the method.** Frequency, association, enrichment, population-differentiation rank, network participation/hub-score, p-value, pleiotropy count — every one is the drift (§12.12). A statistic is only ever the §7 search-order prior. The method is constraint-elimination coherence (§3.4).

**Do not imagine the coherence detector as a graph statistic.** κ or participation over a *generic* network is a topology statistic wearing data-geometry vocabulary (§5.12, §12.13). Coherence is read over the derivation graph, and the working detector is constraint-elimination with abstention.

**Do not invent the constraint object.** The structure saying which sub-threshold signals lock together is not specified here (§0). Guessing it (a PBS pile, a generic interactome) to make the pipeline runnable is the root of the recorded death (§15). Build it with the author, seeded by SDIS (§13.1).

**Do not score the input flat.** A deeply composed multi-hop construction and a shallow coincidence are not the same object. Rank by κ (over the right graph), not by surface familiarity.

**Do not resolve significance against the default oracle.** If the operative μ is "person with consumer genetics and a heterodox theory," low-content surface markers score as load-bearing and the actual mechanism scores zero. The weighting inverts.

**Do not confirm from your own derivations (§5.9).** Once a classification fires, every subsequent turn appears to confirm it, fluently, while carrying zero information. The check is external: is the confirmation coming from what was *stated*, or from what was *derived*?

**Do not assert completeness of any carving.** Every partition here is a candidate in an ensemble. A binary carving is a bet that n = 2 and must be argued, not assumed (§6.13).

**Do not reach for ML.** This is classical AI / data geometry. A bounded model is at most an author-placed tail on an irreducible residual, never the method, never the default (see `DATA_GEOMETRY_ARCHITECTURE.md`, Architecture-Primacy banner).

**Do offer:** extensions, formalizations, existing literature naming an independently-derived result, orthogonal validators, specific experiments, and the constraint-object design. **Do flag:** internal inconsistencies (§11.3 is the recorded example), regime-boundary violations (§12.5), contaminated confirmation channels, and any statistic that has crept in as the method. Generic epistemic hygiene is not a contribution.

---

*End of checkpoint.*
