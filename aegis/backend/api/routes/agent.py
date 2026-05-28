from __future__ import annotations

from fastapi import APIRouter, HTTPException

from dependencies import session_store

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/{session_id}/list")
async def list_agents(session_id: str) -> list[dict]:
    session = await session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return list(session["agents"].values())


@router.get("/{session_id}/{agent_name}/log")
async def agent_log(session_id: str, agent_name: str) -> list[dict]:
    session = await session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return [event for event in session["logs"] if event.get("agent") == agent_name]

