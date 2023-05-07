start:
	docker compose down -t 0
	docker compose up -d
	sleep 5
	docker exec -ti hasura-graphql-engine-1 bash -c "cd /home/hasura && hasura metadata apply && hasura migrate apply --database-name Postgres && hasura metadata reload"

export:
	docker exec -ti hasura-graphql-engine-1 bash -c "cd /home/hasura && hasura metadata export"

create-migration:
	docker exec -ti hasura-graphql-engine-1 bash -c "hasura migrate create '$(migration)' --database-name Postgres"

.PHONY: start export
