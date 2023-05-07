#####################
#  Install targets  #
#####################

init:
	/usr/local/bin/python3 -m venv venv
	install
	pip install -r requirements.txt

# Ready the project to start developing
install: install-dependencies pre-commit-install

# Install all the dependencies specified in requirements.txt
install-dependencies:
	pip install .[dev]

# Install the configured pre-commit git hooks
# TODO: replace by a single command that installs both pre-commit and commit-msg hooks
pre-commit-install:
	pre-commit install --config etc/config/pre-commit-config.yaml --install-hooks --overwrite


##########################
#  Code analysis targets #
##########################

pre-commit-run:
	pre-commit run --all-files --config etc/config/pre-commit-config.yaml

cq:
	black src
	mypy src
	lint-imports

test:
	pytest

coverage: coverage-run
	coverage report

coverage-html: coverage-run
	coverage html

coverage-run:
	coverage run

.PHONY: install install-dependencies pre-commit-install cq test coverage coverage-html coverage-run
