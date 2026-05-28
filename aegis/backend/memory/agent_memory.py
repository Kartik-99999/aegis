from __future__ import annotations

from typing import Any

from memory.vector_store import VectorStore


class AgentMemory:
    def __init__(self, namespace: str, vector_store: VectorStore | None = None) -> None:
        self.namespace = namespace
        self.vector_store = vector_store or VectorStore()

    async def recall(self, task: str) -> list[dict[str, Any]]:
        return await self.vector_store.recall(self.namespace, task)

    async def store(self, task: str, response: dict[str, Any]) -> None:
        await self.vector_store.store(self.namespace, task, response)

