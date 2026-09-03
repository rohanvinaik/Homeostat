# Run record — §3.2 study-bias control: SURVIVES (2026-08-30)

**Verdict under the preregistration: the §3.2 pleiotropy enrichment SURVIVES the
study-bias control. Matching candidates to background genes of the same study
intensity (PubMed tertile), degree, AND PBS, the enrichment is essentially
unchanged and remains at the permutation floor. Study bias is real but explains
only a sliver of the signal.**

## The confound, confirmed and controlled
Candidate bridges average **381 PubMed citations vs 191 for background** (~2× more
studied) — the named confound is real. Adding "same PubMed tertile" (cuts at 47 and
125 citations) as a third matching stratum controls it directly. Only **6/628**
candidates drop for lack of a 3-way match (calibrated pre-run).

## Result (degree + PBS + PubMed-tertile matched, 10,000 permutations)
| test | observed | null | p | vs 2-way null |
|---|---|---|---|---|
| **primary (622 evaluable)** | 34.70 | **25.43** | **<1e-4** | null rose 23.85 → 25.43 |
| top-100 | 54.06 | 26.82 | <1e-4 | — |
| top-300 | 42.48 | 25.26 | <1e-4 | — |
| leave-LRRK2-out (621) | 34.67 | 25.43 | <1e-4 | — |

The matched-null mean rises from 23.85 (degree+PBS only) to 25.43 (adding study
tertile) — so study intensity accounts for ~1.6 of the ~11-point gap between
candidates (34.7) and background. The remaining ~9.3-point elevation is enrichment
beyond study bias, at the permutation floor (0/10,000 null draws reached observed).
Dose-response (top-100 ≫ top-300 ≫ 628) and robustness to LRRK2 removal both hold
under the tighter matching.

## Reading
The pleiotropy the candidate bridges recover is not merely an artifact of their
being better-studied genes. Even against genes matched on graph degree, population
differentiation, AND coarse literature intensity, the candidates are markedly more
pleiotropic. §3.2 — the program's primary falsifier — stands after its named
residual confound is controlled.

## Honest bounds (unchanged)
- PubMed count is a proxy and tertiles are coarse; pleiotropy itself partly drives
  citations. The claim is "enrichment beyond what degree, PBS, and coarse study
  strata jointly explain" — a strong control, not proof of mechanism.
- Aggregate falsifier: validates the pile, not any single gene (§12.6 still forbids
  eyeballing names). Still §12.4-bounded (no dynamics; hypotheses, not mechanism).

## Where this leaves step 2 (hardening the two named confounds)
- **§8.4 selection-enrichment: did NOT survive LD correction** (LD-thin p=0.985) —
  retired as a passing validator; its per-variant p was pseudoreplication.
- **§3.2 annotation-recovery: SURVIVES study-bias control** (p<1e-4) — the primary
  falsifier is robust to its named confound.
The program's evidentiary weight now rests, honestly and after adversarial
hardening, on annotation-recovery (§3.2) + the LRRK2 positive control (§13.3), NOT
on selection enrichment.

## Output
`data/e_i_r/annotation_recovery_studybias.json`.
