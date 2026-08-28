PY := PYTHONPATH=src python3

.PHONY: run status lint test

run:      ## run/resume the §13.1 pipeline (idempotent; safe after any crash)
	$(PY) -m homeostat.pipeline

status:   ## pull progress (add JSON=1 for machine-readable)
	$(PY) -m homeostat.status $(if $(JSON),--json,)

lint:
	ruff check src tests && ruff format --check src tests

test:
	$(PY) -m pytest -q tests
