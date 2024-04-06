# Usage:
# make          # setup packages and install required dependencies
# make setup    # install poetry and pre-commit hooks
# make update   # upgrade poetry dependencies
# make upgrade  # upgrade pre-commit hooks
# make clean    # remove ALL Clean out cached pre-commit files
# make tidy     # run pre-commit hooks

SHELL := /bin/bash

.PHONY: all setup install update upgrade clean tidy test

all: setup install update tidy test

setup:
	@python3 -m pip install --upgrade certifi --break-system-packages
	@curl -sSL https://install.python-poetry.org | python3 -

install:
	@poetry env use python3.12
	@poetry update
	@poetry run pre-commit install -f
	@poetry self add poetry-plugin-up

update:
	@poetry self update
	@poetry update

upgrade:
	@poetry run pre-commit autoupdate
	@poetry up --latest

clean:
	@poetry cache clear pypi --all
	@poetry run pre-commit clean
	@poetry run pre-commit gc
	@poetry run pre-commit uninstall
	@poetry env remove --all
# poetry cache clear --all .

FILES ?= --all-files
tidy: # Example: make tidy FILES="--file clickup_time_entry_prod.py"
	@SKIP=unittest poetry run pre-commit run $(FILES)

test:
	@poetry run pre-commit run unittest

test-all:
	@poetry run pre-commit run unittest --all-files
