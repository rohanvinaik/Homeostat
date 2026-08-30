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

eir-enrich: ## selection-signature enrichment on the PBS pile, MAF-matched (§8.4)
	$(PY) -m homeostat.eir_enrich

lrrk2-gate: ## §13.3 LRRK2 bridge recovery on the PBS pile, function-blind (Law 3)
	$(PY) -m homeostat.lrrk2_gate

bridge-discovery: ## §3.3 annotation-blind candidate-bridge discovery (hypotheses)
	$(PY) -m homeostat.bridge_discovery

annotation-recovery: ## §3.2 annotation-recovery validator (pleiotropy on the 628, preregistered)
	$(PY) -m homeostat.annotation_recovery

status:   ## pull progress (add JSON=1 for machine-readable)
	$(PY) -m homeostat.status $(if $(JSON),--json,)

lint:
	ruff check src tests && ruff format --check src tests

test:
	$(PY) -m pytest -q tests
