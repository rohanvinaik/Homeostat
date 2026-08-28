# Run record — §13.1 E/I/R filter, first complete run (2026-08-28)

Counts and dials only; the ranked queue itself (genotype-derived) stays in
`data/e_i_r/` (gitignored) per the genotype-data policy.

## Inputs
- Index array export: 643,481 SNP rows → 606,137 usable autosomal diploid calls
  (8,501 no-calls, 4,863 indel-type calls, 23,980 non-autosomal). sha256 pinned in
  `docs/REFERENCE_MANIFEST.yaml` (`index-genotype-r-raw`).
- 1000G phase 3 v5c sites VCF (GRCh37), 1,458,224,240 bytes. NB: first download was
  size-exact but stream-corrupt in two regions (~8MB, ~188MB); repaired by ranged
  re-fetch + splice, verified by full decompression (per-member CRC). The pipeline now
  integrity-gates the download (commit "Integrity-gate the reference download").

## Scan (single stream, 22 shards, ~10 min)
- 81,271,999 VCF lines; 77,818,345 biallelic SNPs considered.
- Matched to array sites: **594,846** (98.1% of usable calls) — only 3 allele
  mismatches, confirming plus-strand build-37 orientation end to end.
- Counted skips (never silent): 416,023 multiallelic; 3,037,377 non-SNP;
  6,708 strand-ambiguous A/T–C/G pairs kept but flagged.

## Rank (dials recorded in data/e_i_r/summary.json)
- outgroup=EAS (AFR column emitted), fst_clamp=0.999999, pbs_floor=0.
- **594,846 candidates; 112,348 with priority > 0** (R carries the I-shifted allele
  at a positively-PBS-ranked site).
- Top of queue: max priority ≈ 1.17; a dense cluster of top-25 entries falls in one
  ~700kb window on chr16 (~30.4–31.1Mb) — an extended-LD block, i.e. one locus-scale
  signal expressed as many variants. **Per-variant ranking does not dedup LD**; a
  locus-collapse pass (LD clumping or window-max) is future work before any
  per-locus claims.

## Discipline notes
- Annotation-blind: no gene names attached anywhere in the pipeline or this record.
  Annotation enters only at validation time (checkpoint §3.2, §10.2, preregistered).
- This queue is a **search-order prior** (checkpoint §7.2), not findings. Law 8: no
  novel output is a finding until the §13.3 positive control passes.
- Next per checkpoint: §13.2 selection-signature enrichment on this pile;
  §13.3 blind bridge-recovery positive control.
