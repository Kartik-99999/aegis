from __future__ import annotations

import asyncio
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


class SessionStore:
    """In-memory session state. Swap this for Redis/Mongo adapters in production."""

    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def create(self, session_id: str, goal: str) -> dict[str, Any]:
        session = {
            "id": session_id,
            "goal": goal,
            "phase": "queued",
            "agents": {},
            "scores": {},
            "logs": [],
            "result": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        async with self._lock:
            self._sessions[session_id] = session
        return deepcopy(session)

    async def get(self, session_id: str) -> dict[str, Any] | None:
        async with self._lock:
            session = self._sessions.get(session_id)
            return deepcopy(session) if session else None

    async def set_phase(self, session_id: str, phase: str) -> None:
        await self.patch(session_id, {"phase": phase})

    async def update_agent(self, session_id: str, agent_name: str, payload: dict[str, Any]) -> None:
        async with self._lock:
            session = self._sessions[session_id]
            agent = session["agents"].setdefault(agent_name, {})
            agent.update(payload)
            session["updated_at"] = datetime.now(timezone.utc).isoformat()

    async def set_score(self, session_id: str, agent_name: str, score: float) -> None:
        async with self._lock:
            session = self._sessions[session_id]
            session["scores"][agent_name] = score
            if agent_name in session["agents"]:
                session["agents"][agent_name]["score"] = score
            session["updated_at"] = datetime.now(timezone.utc).isoformat()

    async def append_log(self, session_id: str, event: dict[str, Any]) -> None:
        async with self._lock:
            session = self._sessions[session_id]
            session["logs"].append(event)
            session["updated_at"] = datetime.now(timezone.utc).isoformat()

    async def save_result(self, session_id: str, result: dict[str, Any]) -> None:
        async with self._lock:
            session = self._sessions[session_id]
            session["phase"] = "complete"
            session["result"] = result
            session["updated_at"] = datetime.now(timezone.utc).isoformat()

    async def fail(self, session_id: str, error: str) -> None:
        async with self._lock:
            session = self._sessions[session_id]
            session["phase"] = "failed"
            session["result"] = {"error": error}
            session["updated_at"] = datetime.now(timezone.utc).isoformat()

    async def patch(self, session_id: str, values: dict[str, Any]) -> None:
        async with self._lock:
            session = self._sessions[session_id]
            session.update(values)
            session["updated_at"] = datetime.now(timezone.utc).isoformat()

