from __future__ import annotations

import asyncio
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from dependencies import orchestrator, session_store

router = APIRouter(prefix="/session", tags=["session"])


class SessionStartRequest(BaseModel):
    goal: str = Field(..., min_length=8, max_length=4000)


@router.post("/start")
async def start_session(payload: SessionStartRequest) -> dict[str, str]:
    session_id = uuid.uuid4().hex[:8]
    await session_store.create(session_id=session_id, goal=payload.goal)

    async def run_orchestrator() -> None:
        try:
            await orchestrator.run(payload.goal, session_id)
        except Exception:
            return

    asyncio.create_task(run_orchestrator())
    return {"session_id": session_id, "status": "queued"}


@router.get("/{session_id}")
async def get_session(session_id: str) -> dict:
    session = await session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
