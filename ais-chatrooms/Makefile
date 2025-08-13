SHELL := /bin/bash

.PHONY: dev-up dev-down logs api-shell fmt

dev-up:
	docker compose -f infra/docker/docker-compose.yml up -d --build

dev-down:
	docker compose -f infra/docker/docker-compose.yml down -v

logs:
	docker compose -f infra/docker/docker-compose.yml logs -f --tail=200

api-shell:
	docker compose -f infra/docker/docker-compose.yml exec api bash

fmt:
	docker compose -f infra/docker/docker-compose.yml exec api bash -lc "python -m pip install --no-cache-dir black && black app || true"