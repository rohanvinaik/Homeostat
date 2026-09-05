PYTHON ?= python3
RUN := PYTHONPATH=src $(PYTHON)

.DEFAULT_GOAL := help

.PHONY: help install-dev check lint format test coverage demo gallery glossary connect prior-web

help: ## show the supported development and demonstration commands
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_-]+:.*## / {printf "  %-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install-dev: ## install Homeostat and its development tools in the active environment
	$(PYTHON) -m pip install -e ".[dev]"

check: lint test ## run the complete local quality gate

lint: ## check lint and formatting without modifying files
	ruff check .
	ruff format --check .

format: ## apply Ruff's safe fixes and formatter
	ruff check --fix .
	ruff format .

test: ## run the complete test suite
	$(RUN) -m pytest -q

coverage: ## run the test suite with branch-aware coverage
	$(RUN) -m pytest -q --cov=src/homeostat --cov-branch --cov-report=term-missing

demo: ## run the five self-contained demonstrations (no downloads)
	$(RUN) scripts/gallery.py --synthetic-only

gallery: ## run the complete gallery, including the external-data acceptance probe
	$(RUN) scripts/gallery.py

glossary: ## build the sourced diagnosis-to-gene glossary
	$(RUN) scripts/build_glossary.py

connect: ## map the diagnoses supplied in ARGS over the prior web
	$(RUN) scripts/connect.py $(ARGS)

prior-web: ## fetch source data as needed and assemble the prior web
	$(RUN) -m homeostat.prior_web
