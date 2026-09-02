# The Story Layer — Regenesis generate-wide over the multi-network web

**Status:** design record, 2026-09-02, settled Socratically with the founder. Governs the Regenesis
generate-wide half of the read (SYSTEM_DESIGN §10 step 2; THESIS ch. 9). Grounded in the narrative-meaning
theory (`~/Projects/rohan-vinaik.github.io/papers/Core Documents/New_Work/NARRATIVE_MEANING.md`), the
Regenesis capabilities/authoring contract (read live from `mcp__Regenesis__*`), and the L2→L3 bridge
(`docs/ETIOLOGY_ENGINE.md` §3–4).

## 0. The load-bearing frame: not a port, the same engine

The story layer is **not** a new frame library and **not** Regenesis "applied to biology." It is the *same*
narrative-meaning engine, pointed at genes. Term for term:

- the disease-**shadow** IS the sacrifice frame **M3** (sub-threshold signals pointless alone, significant
  only through concerted devotion to the transcendent phenotype);
- multi-network **convergence** IS **H3** (truth = orthogonal wrongs that *sum*; the measured 12.8% / 29.4%
  network orthogonality is H3 with a number on it);
- the **certified-⊥** IS **H4** (abstention — "sometimes it's just autoimmune");
- tracing unexpected sub-threshold interactions IS the **Baymax** mis-fit read;
- generate-wide / resolve-narrow IS **H2** (Dr. House: abduce boldly, run the differential that kills).

So the build is a *pointing* plus authoring the domain's Forms — never an invention. See THESIS ch. 9.

## 1. The input path: L2 events → L3 sentences → understand()

`prior_web.all_events()` renders the four networks into `list[Event]` (network, verb, subject, target, sign).
Regenesis reads subject-verb-object EVENT SENTENCES, not a frozen graph, so the bridge (ETIOLOGY §3):

- **L2 → L3.** Each event → one fixed SVO sentence with the network VERB and **opaque gene tokens**
  (`Gene17 amplifies Gene42`), plus a sidecar `Gene17 → RIPK2` map kept OUTSIDE the reasoning. The opacity IS
  the token→role trick: a Form fires on the verb-class, so `Gene17 amplifies …` and `Gene42 amplifies …` both
  receive the amplifier role — fungibility by construction — and the real genes are read back afterward.
- Feed as `kind='text'` (raw SVO prose → GSE emit, NO Wikipedia pull) or `kind='contracts'` (GSE
  contract-JSONL). `understand_batch` mass-fires (memory-bounded, no JVM).
- **Every fact transitive** (verb + object, never bare); **reserve verbs** (a generic verb is floored). The
  network verbs (amplifies/inhibits/binds/resembles/co-metabolizes) are the reserved triggers.

## 2. The two artifacts (Regenesis's own two knobs)

Regenesis's front door takes `genres_index` AND `archetypes_index`. The mapping is exact:

- **`archetypes.index` — the ROLES (the characters).** Already exists (`universes/mechanism/`, old-lens era)
  and must be RE-ANCHORED: the trigger column holds the NETWORK VERBS as class centroids (mined from real
  vocabulary, NEVER padded synonyms, NEVER gene names). Roles: amplifier · inhibitor · sensor · transducer ·
  binder · component · bridge · fungible-filler. `if x amplifies signaling then x becomes amplifier`.
- **`genres.index` — the MEANING-MECHANISMS (the plots).** Authored fresh, each carrying its semantic core
  (the M/H principle), not just a shape.

## 3. The genre suite — each a topology AND its meaning-mechanism

| genre | relational signature (what it fires on) | meaning-mechanism it carries |
|---|---|---|
| **Tragedy** (dysregulatory cascade) | a directed chain from a sub-threshold origin into a locked absorbing state | M3/M4 — the fatal flaw serves the doom; deficit → inevitable meta-stable state |
| **Ironic comedy** (vicious cycle) | a reinforcing feedback loop (A worsens B worsens A) | the compensation that compounds; the fix IS the harm |
| **Allegory** (fungibility) | two subgraphs isomorphic in role-structure, disjoint in genes | M1 — meaning ≠ tokens; `common_frame` recovers the invariant cast |
| **Epic quest** (indirect cure) | resolution via a distant BRIDGE, not the phenotype-adjacent node | the κ-super-additive bridge; the roundabout intervention (stimulants→inflammation) |
| **Detective** (the resolve) | two-sign candidate-elimination itself | H2 resolve-narrow; certified-⊥ = "no crime here" |
| **Grail quest** (the read) | the derivation trajectory; the journey is the value | σ_sem>0 drives the search; reaching the phenotype is immaterial to the meaning |

Tragedy / comedy / allegory / quest are MECHANISM genres (recognized in the web). Detective / Grail are
READING genres — the shape of the inquiry, and the engine we already hold (two-sign + the read itself). Author
the four mechanism genres first.

## 4. The two guards (what keeps it a reader, not a romanticism machine)

- **H4 — abstention / recover-vs-import.** Every genre-frame is REFUSABLE. A frame imposing a mechanism-story
  where the truth is a plain fact ("sometimes it's just autoimmune") is a false positive, not a deep insight.
  Recover the shadow the surface voided; never import one that isn't there. This IS the certified-⊥ /
  `not-entailed`, and it is non-negotiable — the anti-over-diagnosis immune system.
- **Baymax — mis-fit boldness (symbolic-deterministic).** Run genres that do NOT fit the presenting phenotype,
  boldly, to surface the occluded sub-threshold layer — because a symbolic mis-fit is an auditable,
  byte-identical derivation, not a hallucination. Licensed *precisely because* the engine is symbolic (a
  symbolic reasoner ENTAILS, it does not fabricate), which is why we can run mis-fit frames whole-hog where an
  LLM could not.

## 5. The pipeline (generate wide → resolve narrow)

1. `prior_web.all_events()` → L2 events (the four networks).
2. L2 → L3 SVO sentences (opaque tokens + sidecar map).
3. `understand(universe_root=universes/mechanism, …)` → recognized genres + archetype roles + the implied
   mechanism + the rules the read wrote itself (`learn`) + significance ranking (κ).
4. Read roles back → real genes via the sidecar; `common_frame` recovers fungible casts.
5. The candidate mechanisms feed the built **resolve-narrow** engine (`search.eliminate_two_sign` over the
   person's positioned deviations) → the auditable verdict / certified-⊥ / Jeeves probe.

## 6. The cardinal authoring rules (from the Regenesis contract — do not violate)

- **Two artifacts per Form: a `.rules` bundle AND its class-centroid anchors in the `.index` trigger column.**
  Miss the trigger column → silent degrade to literal-lemma matching; "0 derivations" then looks like
  abstention but is a WIRING FAILURE. NEVER pad triggers with surface synonyms (they are class centroids),
  NEVER rewrite input to hit a rule's verb, NEVER read "0 derivations" as honest abstention before confirming
  the anchors fire.
- **Markers:** `then` (deduction), `may` (backward abduction — the unstated cause), `cannot` (censor), `must`
  (presumption). Avoid authoring an arc entirely as `then` (fires unconditionally → every read the same shape
  → manufactured meaning).
- **Bridges need CONJUNCTION** `if A and B then C`, with a literal shape on both sides + distinct subject
  variables (a variable bound in antecedent 1 fails to re-match in antecedent 2's object position).
- **Mine, don't fire:** GSE decomposition (CAUSATION/IMPLIES/TEMPORAL) → candidate rules → author small
  (~2 dozen) → fire via `understand_batch` → coherence validates. Firing ASSESSES authored rules; never
  discovers them.

## 7. The build (small, by design)

A few hundred lines. What it is:

- `story.py` — the L2→L3 renderer (events → SVO sentences + the opaque-token sidecar map). Pure decisions
  Detective-pinnable.
- `universes/mechanism/archetypes.index` — re-anchored trigger column (network verbs as centroids) + the role
  `.rules` (amplifier/inhibitor/…), reconciled from the old-lens universe.
- `universes/mechanism/genres.index` — the four mechanism-genre Forms + their `.rules`, each carrying its M/H
  meaning-mechanism.
- the `understand()` wiring + the generate-wide → resolve-narrow bridge (candidates → `eliminate_two_sign`).
- the **LRRK2 positive control** (canon §13.3): recover LRRK2–NOD2–RIPK2 as coherence, blind — the acceptance
  test.

The intelligence is in the frames and the data geometry, not the code. The code is the fuel line.
