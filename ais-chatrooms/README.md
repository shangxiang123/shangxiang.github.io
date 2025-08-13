# AIS Chatrooms

A ChatGPT-like multi-agent chatrooms application where rooms can include multiple AI agents that auto-dialogue with each other and humans can join/interrupt the conversation.

- Backend: Python, Flask, SQLAlchemy, PostgreSQL
- Realtime: SSE for streaming tokens (WS optional later)
- Queue (optional, later): Celery + Redis
- Infra/IaC: Terraform (AWS target), Docker, ECS/ECR (EKS later)
- Frontend: Simple static UI placeholder (React planned)

## Features (MVP)
- Rooms with agents (AI personas) and humans
- Human sends message, AI streams response (SSE)
- Basic JWT-ready structure (placeholder), CORS, health endpoints
- Postgres schema for users/rooms/messages/agents (initial minimal)

## Repo structure

```
ais-chatrooms/
  apps/
    api/             # Flask API service
    web/             # Web static placeholder (can be upgraded to React)
  docs/
    requirements.md  # Living requirements spec (kept up-to-date)
  infra/
    docker/          # Docker compose/dev nginx
    terraform/       # Terraform modules & envs (AWS)
  .github/workflows/ # CI (lint/build/scan skeleton)
  Makefile
```

## Quickstart (local)

Requirements: Docker, Docker Compose

- Start services:
```
make dev-up
```
- Open web UI: http://localhost:8080
- API health: http://localhost:8080/healthz (proxied) or http://localhost:8081/healthz

Stop services:
```
make dev-down
```

## Environment (dev)
- API uses defaults via environment variables set in docker-compose (see `infra/docker/docker-compose.yml`).
- Database: Postgres (db service). Migrations will be added (Alembic) in subsequent iterations.

## Deployment (high-level)
- Terraform under `infra/terraform` will provision AWS resources (VPC, RDS, ECS, ECR, ALB, Secrets). Files include placeholders and variables; apply requires AWS credentials configured.
- CI/CD via GitHub Actions (skeleton `ci.yml`).

## Roadmap
- Replace static web with React + TypeScript app
- Add Celery workers and Redis for agent-run orchestration (auto dialogue)
- JWT auth, RBAC per room, rate limiting, metrics (/metrics)
- pgvector and RAG for later knowledge-grounded agents
- E2E tests (Playwright), load tests (k6)

## License
MIT