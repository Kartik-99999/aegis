# AEGIS

Adaptive Emergent General Intelligence System, scaffolded as a runnable hackathon MVP.

The current build includes a FastAPI backend that parses goals, plans agents, streams simulated agent work over WebSockets, runs a critic debate pass, synthesizes a final output, and stores reflection/playbook notes locally. The React command center consumes those events live and renders the agent graph, thought stream, debate arena, scores, and final synthesis.

## Quick Start

Run the backend:

```bash
cd aegis/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Optional production adapters live in `backend/requirements-optional.txt`.

Run the frontend:

```bash
cd aegis/frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Docker

```bash
cd aegis/docker
docker compose up --build
```

The backend runs on [http://localhost:8000](http://localhost:8000), and the frontend runs on [http://localhost:5173](http://localhost:5173).

## API

```http
POST /session/start
GET  /session/{id}
GET  /agents/{session_id}/list
GET  /agents/{session_id}/{agent_name}/log
GET  /result/{session_id}
WS   /ws/{session_id}
```

Example:

```bash
curl -X POST http://localhost:8000/session/start \
  -H "Content-Type: application/json" \
  -d '{"goal":"Increase e-commerce revenue by 20% without raising ad spend."}'
```

## MVP Notes

- Redis, MongoDB, ChromaDB, Playwright, email, and document generation are represented by clean adapter boundaries.
- The demo works immediately with in-memory session state and local JSON reflection storage.
- The WebSocket event stream supports replay, so the dashboard can connect after a session has already started.
- Agent reasoning is deterministic and simulated for hackathon reliability. Replace the specialist `analyze` methods with real model/tool calls when production credentials are available.

## Project Structure

```text
aegis/
├── backend/        FastAPI API, agents, orchestration, memory, tools
├── frontend/       Vite React command center
├── docker/         Backend, sandbox, and local service compose files
└── README.md
```
