# Virtual Environment
POETRY_RUN	:= poetry run

# Configuration
FILE_TOML 	:= pyproject.toml

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: lint
lint:
	$(POETRY_RUN) black .
	$(POETRY_RUN) isort .
	$(POETRY_RUN) mypy derivation

.PHONY: test
test:
	$(POETRY_RUN) pytest --cov=derivation --cov-report xml:coverage.xml --timeout=30

.PHONY: secure
secure:
	$(POETRY_RUN) safety check --cache -i 51499
	$(POETRY_RUN) bandit -q -r -iii -lll -c ${FILE_TOML} derivation

.PHONY: build
build:
	poetry build
