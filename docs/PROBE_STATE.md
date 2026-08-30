# PROBE STATE — the multi-lens LRRK2 positive control (pre-compact, 2026-08-30)

*Live-experiment handoff. The docs (`THEORY_OF_THE_CASE.md`, `REGULATORY_DEFICIT_PROGRAM.md`,
auto-loaded `CLAUDE.md`/`AGENTS.md`) are the confirmed architecture and source of truth — read them
first. This file is ONLY the state of the running LRRK2 experiment. Ground on git + the probe files,
not this summary.*

## Where we are
The object-agnostic engine is BUILT + pinned (`src/homeostat/`: otp, signal, search, nodes, loop; 74
tests). The first real data run is the **multi-lens LRRK2 positive control** (canon §13.3) — probes in
`probes/lrrk2_slice{1..5}.py`, each a lens, run after each so we WATCH triangulation, not assert it.

**The recurring, thesis-confirming finding: no single lens recovers LRRK2** (it is the compositional,
sub-threshold, regulatory bridge). Measured:
- **Slice 1** (GWAS trait-wiring): recovers the both-cluster HLA hubs; kills LRRK2 (gut-only) & RIPK2
  (leprosy-only) — the mechanism is a SET, not a gene. NOD2 survives (in both clusters) = the seed.
- **Slice 2** (STRING co-occurrence, node-birth from NOD2): @700 → clean 25-gene signaling core
  {NOD2, RIPK2, …}, zero hubs, but LRRK2 missing (regulatory, not a physical bind). @400 → 289 genes,
  all 3 triad BUT hubs+junk. Precision/recall trade-off of one lens = the multi-lens argument.
- **Slice 3** (spine floor = promiscuity, sig-weighting §6): kills the worst generic hubs (HLA-DQA1 =
  1021 traits!); triad survives (RIPK2=2, NOD2=19, LRRK2=40, rank 142/289 — mid). Promiscuity alone
  can't isolate LRRK2 without keeping junk or risking it.
- **Slice 4** (CONVERGENCE over 3 lenses: STRING-700, specificity, GTEx co-expression): NOD2 & RIPK2
  converge (1,1,1)=3 → born; hubs killed (triad survival 67% vs hub 20%). **LRRK2 = (0,1,0)=1, NOT
  born** — fails STRING-700 (not high-conf physical) AND co-expression (broadly expressed, doesn't
  track NOD2's immune profile). Diagnostic: LRRK2's relationship is GENETIC, so it needs a genetic lens.

## THE ONE NEXT ACTION (imperative)
**Get Slice 5's result (the GENETIC lens) and report the convergence.**
1. Check the cache: `wc -l /tmp/gnomad_cloud_af.tsv`. If missing/empty (a bg scan `bgywlk3js` was
   running at compaction; `/tmp` may be wiped), RE-RUN the one-pass gnomAD scan (matched by rsID —
   gnomAD carries rsIDs, dodging the GRCh37/38 build mismatch):
   ```
   cd ~/Projects/Homeostat && PYTHONPATH=src python3 probes/lrrk2_slice5.py rsids > /tmp/cloud_rsids.txt \
   && gzip -dc data/gnomad/gnomad.exomes.r2.1.1.sites.vcf.bgz \
   | awk -F'\t' 'NR==FNR{t[$1]=1;next} !/^#/ && ($3 in t){info=$8;sas="";nfe="";n=split(info,a,";");for(i=1;i<=n;i++){if(a[i]~/^AF_sas=/)sas=substr(a[i],8);else if(a[i]~/^AF_nfe=/)nfe=substr(a[i],8)}if(sas!=""&&nfe!="")print $3"\t"sas"\t"nfe}' /tmp/cloud_rsids.txt - > /tmp/gnomad_cloud_af.tsv
   ```
   (~59 GB, a few minutes — run in the background.)
2. Then: `PYTHONPATH=src python3 probes/lrrk2_slice5.py` — the 4-lens convergence (adds vote_genetic =
   SA-shift, AF_sas > AF_nfe).
3. **Report honestly, DO NOT presume the outcome:**
   - LRRK2 → support 2 (specificity + genetic) → born → the third piece CLICKS; free triangulation
     recovers the whole NOD2–RIPK2–LRRK2 bridge while hubs stay dead. OR
   - LRRK2 stays at support 1 (it's a shared variant with SA-specific *penetrance*, not frequency —
     §7.4) → the §12.4 result, shown lens-by-lens: the regulatory modulator is invisible to every free
     MARGINAL lens and needs the gated joint genotype×phenotype data. Either is a real, publishable answer.

## FORBIDDEN / discipline (do not drift)
- Statistics is TACTICAL only: a lens/candidate-constraint (a proposed kill), NEVER the significance.
  The significance is σ / convergence; the guard is structural. Reading one map's *shape* (STRING
  participation) as the answer is the Act-2 death.
- Convergence across INDEPENDENT lenses is the signal (§6.9); imperfect orthogonality is fine because
  we GENERATE (eliminate), not CALCULATE (estimate) — κ is marginal, so overlap is redundant not wrong.
- **Do NOT tune thresholds to make LRRK2 survive.** Report the vote table transparently; an honest
  negative (LRRK2 stays out) is the §12.4 finding, not a failure to fix.
- `data/e_i_r/*` are the OLD statistical pipeline's outputs (the pathology) — build only from RAW data.

## Pointers
`git log --oneline` (this session: 5f3de08 dump … fcfcdfd Slice 1). Probes: `probes/lrrk2_slice{1..5}.py`.
Engine: `src/homeostat/{otp,signal,search,nodes,loop}.py`. Memory: the refreshed
`reference_homeostat-location.md`. The founder IS the n=1 index case; SDIS is a characterization target,
not the object.
