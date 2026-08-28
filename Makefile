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

status:   ## pull progress (add JSON=1 for machine-readable)
	$(PY) -m homeostat.status $(if $(JSON),--json,)

lint:
	ruff check src tests && ruff format --check src tests

test:
	$(PY) -m pytest -q tests
