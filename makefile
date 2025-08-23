.PHONY: start run migrate migration stop delete logs

start:
	docker compose -f ./docker-compose.yaml up -d --build ${svc}


run:
	uv run -m src


migrate:
	uv run alembic upgrade head


migration:
	cd template/infra/persistence
	uv run alembic revision --autogenerate -m "${msg}"


stop:
	docker compose -f ./docker-compose.yaml stop


delete: stop
	docker compose -f ./docker-compose.yaml rm -f -v
	docker volume rm psql_data


logs:
	docker compose -f ./docker-compose.yaml logs
