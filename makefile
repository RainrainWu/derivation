# Virtual Environment
POETRY_RUN		:= poetry run

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: lint
lint:
	$(POETRY_RUN) black .
	$(POETRY_RUN) isort .

.PHONY: test
test:
	$(POETRY_RUN) pytest --cov=derivation

.PHONY: build
build:
	poetry build
