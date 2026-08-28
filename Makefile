PY := PYTHONPATH=src python3

.PHONY: run status lint test enrich

run:      ## run/resume the §13.1 pipeline (idempotent; safe after any crash)
	$(PY) -m homeostat.pipeline

enrich:   ## run the §13.2 selection-signature enrichment (idempotent)
	$(PY) -m homeostat.enrich

bridge:   ## run the §13.3 blind bridge recovery + preregistered LRRK2 control
	$(PY) -m homeostat.bridge

status:   ## pull progress (add JSON=1 for machine-readable)
	$(PY) -m homeostat.status $(if $(JSON),--json,)

lint:
	ruff check src tests && ruff format --check src tests

test:
	$(PY) -m pytest -q tests
