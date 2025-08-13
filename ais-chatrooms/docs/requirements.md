# AIS Chatrooms — Requirements (Living Document)

Status: Draft (MVP in progress)
Owner: You (candidate) + AIS project maintainer
Update policy: Update this file on each requirement change; keep Change Log at bottom.

## 1. Vision
A web chatrooms application that supports multiple AI agents per room. Agents can auto-dialogue with each other (AI↔AI), and humans can join/interrupt at any time. The product demonstrates full‑stack, cloud, security, and data engineering capabilities aligned with AIS Senior Software Engineer role.

## 2. Goals & Non‑Goals
- In scope (MVP):
  - Create/join room, list agents, create/edit agent persona (name, system prompt, model, temperature)
  - Human message → AI streams response (SSE)
  - Auto mode: agents take turns to speak (simple round-robin selector)
  - Room timeline with Markdown/Code blocks rendering (frontend placeholder acceptable)
  - Health endpoints, structured logs, basic metrics stub
  - Docker Compose local run; Terraform skeleton for AWS
- Out of scope (MVP; planned later):
  - OAuth login, RBAC per room, rate limiting
  - Vector search (RAG), file uploads
  - Multi-cloud deployment, Kubernetes/EKS

## 3. Actors & Roles
- Guest user: anonymous access to a public demo room (read/send, configurable)
- Registered user: owns rooms and agents (later; placeholder in MVP)
- AI agent: chat participant with persona and model settings
- System/Worker: background runner deciding next speaker and generating messages

## 4. Key Concepts
- Room: container of participants and messages; mode: manual/auto
- Agent: an AI persona (system prompt, model, temperature, tools)
- Message: event in timeline (human/agent/system), supports streaming deltas
- Run: one auto-dialogue session with limits (max steps/time/tokens)

## 5. User Stories (MVP)
- As a user, I can create a room and add two agents with different personas.
- As a user, I can send a message and see the AI stream back the reply.
- As a user, I can toggle Auto mode so that agents alternate talking for up to N turns.
- As a user, I can stop the auto run and inject my own message.
- As a user, I can refresh the page and reload recent messages in the room.

Acceptance (MVP):
- Given two agents in Auto mode, they will alternate and produce at most `max_steps` messages within `max_seconds`, and the UI receives tokens via SSE without disconnects.

## 6. Non‑Functional Requirements
- Availability (dev/demo): single AZ, acceptable occasional restarts
- Performance: initial P95 latency under 2s for first token on simple prompts
- Security: HTTPS in cloud, secrets in SSM/Secrets Manager, CORS restricted
- Observability: structured JSON logs, health endpoints; metrics endpoint stub
- Cost: minimal dev footprint; scalable via ECS/EKS later

## 7. API (Draft)
- GET /healthz → 200 OK
- POST /api/rooms → {id, name, mode}
- GET /api/rooms/:id/messages?cursor= → [{...}]
- POST /api/rooms/:id/messages → {message}
- GET /api/rooms/:id/stream (SSE) → events: message.new, message.delta, run.status
- GET /api/rooms/:id/agents → [{...}]
- POST /api/rooms/:id/agents → {id, name, model, system_prompt}
- POST /api/rooms/:id/auto/start {max_steps, max_seconds} → {run_id}
- POST /api/rooms/:id/auto/stop → {status}

Note: SSE requires Bearer token or cookie (MVP allows anonymous for demo room).

## 8. Data Model (Initial)
- users(id, email, name, password_hash, created_at)
- rooms(id, name, owner_id, mode, created_at)
- room_members(id, room_id, user_id, role)
- agents(id, room_id, name, model, temperature, system_prompt, is_active)
- runs(id, room_id, status, max_steps, max_seconds, budget_tokens, started_at, stopped_at, stop_reason)
- messages(id, room_id, sender_type, sender_id, content, tokens_in, tokens_out, latency_ms, run_id, created_at)
- usage_events(id, room_id, agent_id, provider, model, input_tokens, output_tokens, cost, created_at)

Indexes: messages(room_id, created_at), runs(room_id, started_at), agents(room_id, is_active)

## 9. Turn Selection (MVP)
- Strategy: round-robin across active agents, skip the one who spoke last; enforce per-agent cooldown.
- Stop conditions: reached max_steps or max_seconds; or user stop; or budget exceeded.

## 10. Flows
- Human message:
  1) POST /messages → persist → emit SSE message.new → if Auto=on, enqueue next step
- Auto step:
  1) Worker selects next agent → stream tokens → persist deltas → SSE message.delta → finalize message → check stop → enqueue next
- Stop:
  - Update run.status=stopped; revoke background task

## 11. Architecture & Deployment
- Local: Docker Compose (api, db, redis, nginx web)
- Cloud (next): AWS via Terraform (VPC, RDS, Redis, ECS, ECR, ALB, S3+CF)
- CI/CD: GitHub Actions (lint/test/build/scan; terraform plan/apply with approval)

## 12. Risks & Mitigations
- SSE disconnects → auto-retry with Last-Event-ID
- Token cost overruns → budget in runs + per-room limits (later)
- Infinite loops in auto → cooldown + step/time caps

## 13. Open Questions
- Auth mode for demo (anonymous vs magic link)
- Which LLM provider first (OpenAI/Azure/Qwen)
- Need RAG in MVP?

## 14. Acceptance Criteria (MVP)
- Start local stack and chat with agents; auto mode runs and can be stopped.
- Health endpoint, basic logs, documented run steps.

---

## Change Log
- v0.2: Added Agents API (list/create) endpoints to MVP; wired into API.
- v0.1 (init): Defined MVP scope, API draft, data model, flows, and deployment approach.