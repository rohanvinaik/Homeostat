# Homeostat

**A machine for reading the mechanism under a set of symptoms — the coupled cause that connects them —
and for saying, just as carefully, when there is no mechanism it can honestly find.** Named for Ashby's
homeostat, the machine that finds its own equilibrium, because the thing under study is regulation.

> Homeostat generates *hypotheses to interrogate*, not diagnoses. It is a research instrument, not a
> clinician. **Nothing here is medical advice.** And see *Where it actually is* at the bottom — the
> reasoning engine is built and proven; the data plumbing that would feed it from open biology is
> designed but not yet wired, so it does not yet read a real person end to end.

---

## The person it is built for

Someone arrives with a cluster of conditions that span several body systems and refuse to line up with
any one clinic. Each specialist tunnels into their own organ and returns an exotic, poor-fitting label —
or, more often, a shrug. The person is usually the one who says the true thing first:

> *"I KNOW these are connected. I can feel how one feeds into the other — how treating a part of one makes
> another mysteriously vanish. I don't have the words for why, but I know they're not separate accidents.
> I need a mechanism to interrogate. Like Dr. House, without the needless cruelty."*

They are almost always right, and the medical system almost always cannot help — not out of malice, but
because of how its main instrument works. Modern genetics largely finds causes by **counting**: which
variant appears more often in patients than in healthy people. For a clean single-gene disease that
works. For most of chronic, multi-system illness it quietly fails, and it fails hardest on exactly the
people who are already hardest to believe.

## Why the counting fails — and it is not fixable with more data

The mechanism these people are feeling is real, but it is a **shadow**: a coherent state that many weak,
individually-unremarkable signals cast *in concert*, stored in no single one of them. Three things make
it invisible to a counting instrument, and each is structural, not a matter of sample size:

- **Control is distributed.** A symptom sits at the end of a long, redundant pathway, and no single step
  holds enough of the control for its failure to register on its own.
- **The parts are interchangeable.** One person breaks the pathway at step 12; another at step 30 with a
  different gene doing the same job; a third has a spare covering for the first. *Same mechanism every
  time, no shared gene* — so the count, which looks for a shared gene, finds nothing.
- **The state is dynamic.** The mechanism is a meta-stable balance that holds until enough of the coupling
  shifts and it tips — which is exactly why "treating one part makes another vanish."

A shadow cannot be found by inspecting light sources one at a time, at any sample size. That is the whole
problem in one sentence — and it is why a fragmented system of single-specialty reads is *structurally*
positioned never to see the thing the patient is reporting.

## What Homeostat does instead

It stops counting and recovers the **mechanism**, by four moves that no other tool combines:

1. **It reads roles, not genes.** The gene is the interchangeable part; the *role it plays* is the
   invariant. Two different genes filling the same role, in two different people, are recognized as the
   same mechanism.
2. **It triangulates across the geometries of biology.** No single free dataset shows a mechanism, so it
   reads several — how genes are related by evolution, by structure, by regulation, by development, by the
   life a person has lived — and trusts only what several independent views *agree* on. Convergence is the
   signal; a claim only one view supports is dropped.
3. **It reasons in two signs.** It weighs not only what *could* explain the presentation but what is
   *ruled out* — and it can return a **certified "there is no mechanism here," with a proof**, which is a
   categorically different thing from "I didn't find one." Most systems have no way to say this at all.
4. **It abstains when it should.** Where the evidence does not converge, it says so and points at the one
   measurement that would resolve it — rather than confabulating a confident story to fill the silence.

The reasoning is **classical AI and data geometry — not statistics, not a machine-learning model.** It
derives what the evidence implies but never states, and stops where nothing follows. There is no model to
train, and that is deliberate: the intelligence is in the correctness of the geometry, not the size of a
network.

## What a reading looks like

Give it the cluster, and — once its data senses are wired (see below) — it returns one of four honest
verdicts, never a label:

- **A mechanism to interrogate** — the coupled cause the symptoms imply, with the *load-bearing* part
  named (the connector whose loss would collapse the cascade — which is usually the treatment target), and
  the provenance of every step. Not "you have disease X"; rather "here is the mechanism, here is what holds
  it together, here is how sure I am."
- **The next question** — *Jeeves mode.* When two mechanisms fit equally, it does not guess. It asks for
  the single measurement that would separate them: *"Do you also have allergies? Is there a persistent
  tachycardia? Does one drug resolve several of these at once?"* The last is the most powerful input it
  has — and it is one you already carry in your own history.
- **A certified nothing** — "no mechanism the known biology can resolve explains this," with the proof.
  Honest, and rare.
- **An honest abstention** — "I cannot separate these without a measurement you don't have."

It will rank and connect and name the mechanism; it will not decide *why* your life led there — imputing
purpose is the human's job, and it is careful to say so.

## Why nothing else does this

Not because the pieces are secret, but because the field's dominant instrument is pointed the other way.
Counting-based genetics is built to find frequent single causes and is structurally blind to fungible,
sub-threshold, coherence-borne mechanisms — the ones that only exist in combination. Statistical and
machine-learning pipelines inherit that blindness and add their own: they estimate rather than eliminate,
they cannot certify a negative, and they will always return *something*. Homeostat is the inverse on every
axis — mechanism not frequency, roles not genes, elimination not estimation, two signs not one, honest
abstention not a forced answer. It is an instrument built specifically for the case everything else was
built to miss, and it rests on a decade of the author's own formal work on what *understanding* is,
turned back onto the domain where understanding first evolved.

## Where it actually is (the honest status)

This matters, so it is plain: **the brain is built and proven; the senses are not yet wired.**

- **Built and pinned** — the full reasoning engine: two-sign elimination with certified-⊥, the per-person
  signed-ternary positioning, the discrimination-dimension (Jeeves) selector, and the encoding layer that
  turns biological evidence into what the engine reads. Every *pure decision* is verified to a
  mutation-complete specification, and the whole is covered by hand-written intent tests; 133 pass. The
  complete theory is written out in full.
- **Designed but not yet built** — the *renderers*: the plumbing that reads open biological databases
  (Reactome, UniProt, Pfam, GO, BLAST) and the person's own history and turns them into the evidence the
  engine consumes. Until those are wired, Homeostat cannot read a real person from real data end to end.

So today it is a complete design with a working, proven engine, at the point where the remaining work is
the biology-data plumbing. It is honest about being there, the same way it is honest about everything
else — that discipline is the product, not a caveat on it.

The other honest limit is deeper than code: the data that would *settle* these questions — each person's
genes and symptoms together, watched over time as a mechanism moves — is gated behind institutions and
money. Homeostat is built to work from the free shadows of that data, so its output is a testable
hypothesis, never a proven mechanism and never a diagnosis. That is a fact about what data is purchasable,
not a flaw in the method — and the whole system is built to keep telling you which is which.

## Read further

- [`docs/THESIS.md`](docs/THESIS.md) — the full theory: what understanding is, and why it comes home to
  biology. Start here if you want the *why*.
- [`docs/SYSTEM_DESIGN.md`](docs/SYSTEM_DESIGN.md) — the engineering design and the current build state.
- [`docs/REGULATORY_DEFICIT_PROGRAM.md`](docs/REGULATORY_DEFICIT_PROGRAM.md) — the founding canon.

The reasoning engine is **Regenesis** (deterministic, provenance-carrying story-understanding). The
formal substrate it rests on — specification complexity, negative specification, significance-weighting,
orthogonal ternary projection — is the author's own work, referenced from the design docs.
