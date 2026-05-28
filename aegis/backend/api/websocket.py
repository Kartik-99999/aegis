from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from dependencies import event_bus

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/{session_id}")
async def session_stream(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    queue, history = await event_bus.subscribe(session_id)
    try:
        terminal_seen = False
        for event in history:
            await websocket.send_json({**event, "replay": True})
            terminal_seen = event["type"] in {"session_complete", "session_error"}

        if terminal_seen:
            return

        while True:
            event = await queue.get()
            await websocket.send_json(event)
            if event["type"] in {"session_complete", "session_error"}:
                return
    except WebSocketDisconnect:
        return
    finally:
        await event_bus.unsubscribe(session_id, queue)

