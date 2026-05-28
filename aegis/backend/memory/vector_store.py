from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class VectorStore:
    """Small local persistence adapter that mirrors the ChromaDB contract for MVP use."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(__file__).resolve().parents[1] / ".data" / "vector_store.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> dict[str, list[dict[str, Any]]]:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _write(self, data: dict[str, list[dict[str, Any]]]) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    async def store(self, collection: str, key: str, document: dict[str, Any]) -> None:
        data = self._read()
        data.setdefault(collection, []).append({"key": key, "document": document})
        self._write(data)

    async def recall(self, collection: str, query: str, limit: int = 5) -> list[dict[str, Any]]:
        data = self._read()
        items = data.get(collection, [])
        query_terms = set(query.lower().split())

        def score(item: dict[str, Any]) -> int:
            text = json.dumps(item.get("document", {})).lower()
            return sum(1 for term in query_terms if term in text)

        return sorted(items, key=score, reverse=True)[:limit]

