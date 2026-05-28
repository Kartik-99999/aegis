from __future__ import annotations

from fastapi import APIRouter, HTTPException

from dependencies import session_store

router = APIRouter(prefix="/result", tags=["result"])


@router.get("/{session_id}")
async def get_result(session_id: str) -> dict:
    session = await session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if not session.get("result"):
        raise HTTPException(status_code=202, detail="Result is not ready")
    return session["result"]

