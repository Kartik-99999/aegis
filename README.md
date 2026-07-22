# AEGIS — Adaptive Emergent General Intelligence System

A multi-agent orchestration platform that turns a single business goal into a live,
observable "war room" of specialist AI agents. AEGIS parses the goal, plans a team of
agents, runs them concurrently, subjects their output to an adversarial critic debate,
synthesizes a final strategy, and reflects on the run to improve future planning — all
streamed to a React command center in real time over WebSockets.

> 📁 The application lives in the [`aegis/`](./aegis) directory. This root README is the
> canonical overview; deeper notes also live in [`aegis/README.md`](./aegis/README.md).

---

## How it works

A session flows through the [`Orchestrator`](./aegis/backend/core/orchestrator.py),
which drives seven phases and emits an event at every transition so the UI can render
progress live:

```
parsing_goal → planning_agents → running_agents → debating → synthesizing → complete
```

1. **Goal parsing** — [`GoalParser`](./aegis/backend/core/goal_parser.py) classifies the
   goal into a domain (e-commerce, SaaS, creator business, local services, digital media,
   defense technology, …), extracts an objective and sub-tasks, and flags signals
   (revenue / growth / customer intent) via keyword heuristics.
2. **Agent planning** — [`AgentPlanner`](./aegis/backend/core/agent_planner.py) builds a
   team of four specialists and tailors their tasks to the parsed goal. It also keeps
   tunable per-agent weights that the reflection engine updates over time.
3. **Concurrent execution** — every agent runs in parallel (`asyncio.gather`), recalls
   relevant context from its own memory namespace, produces an `AgentOutput` (content,
   confidence, evidence, recommendations), and streams its "thoughts" as it works.
4. **Adversarial debate** — the [`DebateEngine`](./aegis/backend/core/debate_engine.py)
   spawns a [`CriticAgent`](./aegis/backend/agents/critic_agent.py) that stress-tests
   every output; each agent then defends and narrows its claim, producing a scored
   transcript.
5. **Synthesis** — the orchestrator ranks recommendations by confidence, builds a
   concrete action plan, and writes a domain-aware strategy narrative.
6. **Reflection** — the [`ReflectionEngine`](./aegis/backend/core/reflection_engine.py)
   identifies the best/weakest agents, patches a reusable "playbook," and adjusts agent
   weights for the next run. Reflections and playbooks are persisted to a local vector
   store.

### The agents

| Agent | Role | Tools |
|-------|------|-------|
| **Market Analyst** | Competitor research, market sizing, positioning gaps | web search, scraper |
| **Psych Agent** | Customer behavior, objections, emotional triggers | web search, doc reader |
| **Growth Agent** | Experiment generation, ROI ranking, metrics design | web search, code executor |
| **Executor Agent** | Deliverables, copy, briefs, implementation-ready assets | doc generator, email, code executor |
| **Critic Agent** | Adversarial stress-testing of every output | — |

All agents extend [`BaseAgent`](./aegis/backend/agents/base_agent.py), which provides the
shared `run → think → analyze → store` lifecycle, per-agent memory, and the `defend`
step used during debate.

---

## Architecture

```text
aegis/
├── backend/                    FastAPI service (Python 3.11+)
│   ├── main.py                 App factory, CORS, health check, router wiring
│   ├── config.py               Env-driven settings (dataclass)
│   ├── dependencies.py         Singleton event bus, session store, orchestrator
│   ├── core/                   Orchestration engine
│   │   ├── orchestrator.py     End-to-end session pipeline
│   │   ├── goal_parser.py      Goal → domain / objective / sub-tasks
│   │   ├── agent_planner.py    Builds the agent team + weight tuning
│   │   ├── debate_engine.py    Critic attack → defense → scoring
│   │   ├── reflection_engine.py Post-run learning + playbook patches
│   │   ├── event_bus.py        In-process pub/sub with replay history
│   │   └── schemas.py          Dataclasses: ParsedGoal, AgentPlan, AgentOutput, …
│   ├── agents/                 Specialist + critic agents
│   ├── api/                    REST routes (session, agent, result) + WebSocket
│   ├── memory/                 Session store, per-agent memory, vector store
│   └── tools/                  web_search, scraper, code_executor, doc_generator, email
├── frontend/                   Vite + React command center
│   ├── src/components/         AgentGraph, ThoughtStream, DebateArena, ResultPanel, …
│   └── src/hooks/              useAegisSession, useWebSocket
└── docker/                     Backend, sandbox, and compose (Redis / Mongo / Chroma)
```

### Event-driven core

The [`EventBus`](./aegis/backend/core/event_bus.py) is an async in-process pub/sub with a
bounded **replay history** (default 300 events, `AEGIS_EVENT_REPLAY_LIMIT`). Because
every event is retained, a dashboard can connect *after* a session has started — or even
after it finished — and the [WebSocket endpoint](./aegis/backend/api/websocket.py) will
replay the full timeline before switching to live updates. Event types include
`goal_parsed`, `phase_update`, `agent_spawned`, `thought`, `debate_attack`,
`session_complete`, and `session_error`.

### State & memory

- [`SessionStore`](./aegis/backend/memory/session_store.py) — in-memory, lock-guarded
  session state (phase, agents, scores, logs, result).
- [`VectorStore`](./aegis/backend/memory/vector_store.py) — local JSON persistence that
  mirrors a ChromaDB-style contract for reflections and playbooks.
- Redis, MongoDB, ChromaDB, Playwright, email, and doc generation are represented by
  **clean adapter boundaries** — the MVP runs entirely on in-memory + local-JSON so it
  works with zero external services. Optional production adapters live in
  [`backend/requirements-optional.txt`](./aegis/backend/requirements-optional.txt).

> **Note:** in this build the agents' reasoning is deterministic and simulated for
> demo reliability. Each specialist's `analyze` method is the seam where you plug in real
> model/tool calls once production credentials are available.

---

## Getting started

### Prerequisites

- Python 3.11+
- Node.js 18+ (Node 22 for the Docker frontend image)
- Docker (optional, for the full stack with Redis/Mongo/Chroma)

### Backend

```bash
cd aegis/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The backend serves on <http://localhost:8000> (health check at `/health`).

### Frontend

```bash
cd aegis/frontend
cp .env.example .env      # VITE_API_URL / VITE_WS_URL
npm install
npm run dev               # http://localhost:5173
```

### Docker (full stack)

```bash
cd aegis/docker
docker compose up --build
```

Brings up the backend, the Vite dev server, and Redis + MongoDB + ChromaDB.

---

## Configuration

Backend settings ([`config.py`](./aegis/backend/config.py)) are read from the environment:

| Variable | Default | Purpose |
|----------|---------|---------|
| `AEGIS_ENV` | `development` | Environment name |
| `AEGIS_CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Allowed origins (comma-separated) |
| `AEGIS_MODEL` | `local-simulated-agent` | Model identifier |
| `AEGIS_EVENT_REPLAY_LIMIT` | `300` | Max events retained per session |
| `MONGO_URL` / `REDIS_URL` / `CHROMA_HOST` | unset | Optional production adapters |
| `JWT_SECRET` | `aegis-local-dev-secret` | Auth secret |

Frontend: `VITE_API_URL` (default `http://localhost:8000`) and `VITE_WS_URL`
(default `ws://localhost:8000`).

---

## API reference

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service health check |
| `POST` | `/session/start` | Start a session — body `{ "goal": "…" }` (8–4000 chars); returns `{ session_id, status }` and runs the orchestrator in the background |
| `GET` | `/session/{id}` | Full session state |
| `GET` | `/agents/{session_id}/list` | All agents in a session |
| `GET` | `/agents/{session_id}/{agent_name}/log` | An agent's thought log |
| `GET` | `/result/{session_id}` | Final result (`202` until ready) |
| `WS` | `/ws/{session_id}` | Live event stream with replay |

Example:

```bash
curl -X POST http://localhost:8000/session/start \
  -H "Content-Type: application/json" \
  -d '{"goal":"Increase e-commerce revenue by 20% without raising ad spend."}'
```

---

## Tech stack

**Backend:** Python, FastAPI, Uvicorn, Pydantic, asyncio, WebSockets
**Frontend:** React 18, Vite, D3, Framer Motion, Lucide
**Infra (optional):** Docker Compose, Redis, MongoDB, ChromaDB
