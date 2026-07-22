# AEGIS

**Adaptive Emergent General Intelligence System** — a multi-agent orchestration
platform, scaffolded as a runnable MVP.

A FastAPI backend parses goals, plans agents, streams agent work over WebSockets,
runs a critic debate pass, synthesizes a final output, and stores reflection/playbook
notes. A React command center consumes those events live and renders the agent graph,
thought stream, debate arena, confidence scores, and final synthesis.

> 📁 The application lives in the [`aegis/`](./aegis) directory. See
> [`aegis/README.md`](./aegis/README.md) for full setup, API reference, and
> architecture notes.

## Quick start

```bash
# Backend
cd aegis/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (in a second terminal)
cd aegis/frontend
npm install && npm run dev   # http://localhost:5173
```

Or with Docker:

```bash
cd aegis/docker
docker compose up --build
```

## Structure

```text
aegis/
├── backend/     FastAPI API, agents, orchestration, memory, tools
├── frontend/    Vite + React command center
├── docker/      Backend, sandbox, and local-service compose files
└── README.md    Full documentation
```

## Highlights

- Specialist agents: market analyst, growth, psych, executor, critic
- Core engine: goal parser, agent planner, orchestrator, debate + reflection engines,
  event bus
- Memory: session store, agent memory, vector store (with clean adapter boundaries
  for Redis / MongoDB / ChromaDB)
- Live WebSocket event stream with replay support
