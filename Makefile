PY := PYTHONPATH=src python3

.PHONY: run status lint test enrich

run:      ## run/resume the §13.1 pipeline (idempotent; safe after any crash)
	$(PY) -m homeostat.pipeline

enrich:   ## run the §13.2 selection-signature enrichment (idempotent)
	$(PY) -m homeostat.enrich

bridge:   ## run the §13.3 blind bridge recovery + preregistered LRRK2 control
	$(PY) -m homeostat.bridge

gwas-extract: ## (re)build the §13.4 trait gene sets from the GWAS bulk file
	$(PY) -m homeostat.gwas_extract data/network/gwas-catalog-download-associations-alt-full.tsv

ensemble: ## run the §13.4 oracle-ensemble calibration (structure-derived slice)
	$(PY) -m homeostat.ensemble

sigsearch: ## run the Phase-2 deterministic verifier baseline (structural bridges)
	$(PY) -m homeostat.sigsearch

propose-verify: ## verify the frozen LLM proposal flood (firewall + selection-lift)
	$(PY) -m homeostat.propose_verify

eir-pile: ## build the cohort-scale E/I/R PBS pile from Pan-UKBB allele frequencies (§7)
	$(PY) -m homeostat.eir_cohort

gnomad-pile: ## build the E/I/R PBS pile from gnomAD v2.1.1 SAS exomes (run with HOMEOSTAT_TAG=_gnomad)
	$(PY) -m homeostat.gnomad_pile

eir-enrich: ## selection-signature enrichment on the PBS pile, MAF-matched (§8.4)
	$(PY) -m homeostat.eir_enrich

eir-enrich-block: ## §8.4 LD-block-corrected re-test (1Mb block bootstrap, preregistered)
	$(PY) -m homeostat.eir_enrich_block

eir-enrich-thin: ## §8.4 LD-thinned re-test (1 variant/1Mb window, preregistered)
	$(PY) -m homeostat.eir_enrich_ldthin

lrrk2-gate: ## §13.3 LRRK2 bridge recovery on the PBS pile, function-blind (Law 3)
	$(PY) -m homeostat.lrrk2_gate

bridge-discovery: ## §3.3 annotation-blind candidate-bridge discovery (hypotheses)
	$(PY) -m homeostat.bridge_discovery

annotation-recovery: ## §3.2 annotation-recovery validator (pleiotropy on the 628, preregistered)
	$(PY) -m homeostat.annotation_recovery

annotation-recovery-studybias: ## §3.2 study-bias control (add pubmed-tertile matching, preregistered)
	$(PY) -m homeostat.annotation_recovery_studybias

pbs-restricted: ## §7 PBS-restricted candidate set sweep (run per cohort; HOMEOSTAT_TAG=_gnomad for gnomAD)
	$(PY) -m homeostat.pbs_restricted

pbs-restricted-compare: ## cross-cohort comparison — is PBS now load-bearing?
	$(PY) -m homeostat.pbs_restricted_compare

sig-descent: ## §III selection-weighted κ (PBS as §10.3 prior); run per cohort (HOMEOSTAT_TAG=_gnomad)
	$(PY) -m homeostat.sig_descent

sig-descent-compare: ## §III cross-cohort coherence test (does the lift replicate?)
	$(PY) -m homeostat.sig_descent_compare

status:   ## pull progress (add JSON=1 for machine-readable)
	$(PY) -m homeostat.status $(if $(JSON),--json,)

lint:
	ruff check src tests && ruff format --check src tests

test:
	$(PY) -m pytest -q tests
