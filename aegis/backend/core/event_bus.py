from __future__ import annotations

import asyncio
from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Any

from config import settings


class EventBus:
    """Async in-process event bus with replay history for late WebSocket joins."""

    def __init__(self) -> None:
        self._subscribers: dict[str, set[asyncio.Queue[dict[str, Any]]]] = defaultdict(set)
        self._history: dict[str, deque[dict[str, Any]]] = defaultdict(
            lambda: deque(maxlen=settings.event_replay_limit)
        )
        self._lock = asyncio.Lock()

    async def emit(self, session_id: str, event: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **event,
        }

        async with self._lock:
            self._history[session_id].append(payload)
            subscribers = list(self._subscribers[session_id])

        for queue in subscribers:
            await queue.put(payload)

        return payload

    async def subscribe(
        self, session_id: str
    ) -> tuple[asyncio.Queue[dict[str, Any]], list[dict[str, Any]]]:
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        async with self._lock:
            self._subscribers[session_id].add(queue)
            history = list(self._history[session_id])
        return queue, history

    async def unsubscribe(
        self, session_id: str, queue: asyncio.Queue[dict[str, Any]]
    ) -> None:
        async with self._lock:
            self._subscribers[session_id].discard(queue)

    def history(self, session_id: str) -> list[dict[str, Any]]:
        return list(self._history[session_id])

