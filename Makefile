#####################
#  Install targets  #
#####################

# Ready the project to start developing
install: install-dependencies pre-commit-install

venv:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate

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
	black core
	mypy core
	lint-imports

test:
	pytest

coverage: coverage-run
	coverage report

coverage-html: coverage-run
	coverage html

coverage-run:
	coverage run

##########################
#         Build          #
##########################
build: install
	@python ./etc/scripts/build.py
	make install

##########################
#         Hasura         #
##########################
start:
	docker compose down -t 0
	docker compose up -d
	sleep 5
	docker exec -ti pynances-graphql-engine-1 bash -c "cd /home/hasura && hasura metadata apply && hasura migrate apply --database-name pynances && hasura metadata reload"

export:
	docker exec -ti pynances-graphql-engine-1 bash -c "cd /home/hasura && hasura metadata export"

create-migration:
	docker exec -ti pynances-graphql-engine-1 bash -c "hasura migrate create '$(migration)' --database-name Postgres"

.PHONY: install install-dependencies pre-commit-install cq test coverage coverage-html coverage-run build venv start export create-migration
