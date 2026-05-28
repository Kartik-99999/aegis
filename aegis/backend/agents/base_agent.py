from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Any

from core.event_bus import EventBus
from core.schemas import AgentOutput, ParsedGoal
from memory.agent_memory import AgentMemory
from memory.session_store import SessionStore


class BaseAgent(ABC):
    def __init__(
        self,
        name: str,
        role: str,
        task: str,
        tools: list[Any],
        event_bus: EventBus,
        session_store: SessionStore,
    ) -> None:
        self.name = name
        self.role = role
        self.task = task
        self.tools = tools
        self.event_bus = event_bus
        self.session_store = session_store
        self.memory = AgentMemory(namespace=f"agent_memory_{self.name.lower().replace(' ', '_')}")

    async def run(self, session_id: str, parsed_goal: ParsedGoal) -> AgentOutput:
        await self.session_store.update_agent(
            session_id,
            self.name,
            {"name": self.name, "role": self.role, "task": self.task, "status": "thinking"},
        )
        await self.think(session_id, f"Starting task: {self.task}")
        context = await self.memory.recall(self.task)
        await asyncio.sleep(0.2)

        output = await self.analyze(session_id, parsed_goal, context)
        await self.memory.store(self.task, output.to_dict())

        await self.session_store.update_agent(
            session_id,
            self.name,
            {"status": "complete", "score": output.confidence},
        )
        await self.think(session_id, f"Submitted output with {round(output.confidence * 100)}% confidence.")
        return output

    async def think(self, session_id: str, text: str) -> None:
        event = await self.event_bus.emit(
            session_id,
            {
                "type": "thought",
                "agent": self.name,
                "text": text,
            },
        )
        await self.session_store.append_log(session_id, event)

    async def defend(self, session_id: str, critique: str) -> str:
        await self.session_store.update_agent(session_id, self.name, {"status": "defending"})
        await self.think(session_id, "Reviewing critic attack and tightening the claim.")
        await asyncio.sleep(0.35)
        defense = (
            f"{self.name} accepts the constraint, narrows the claim, and keeps the recommendation "
            f"only where evidence supports it. Response to critique: {critique}"
        )
        await self.session_store.update_agent(session_id, self.name, {"status": "debated"})
        return defense

    @abstractmethod
    async def analyze(
        self,
        session_id: str,
        parsed_goal: ParsedGoal,
        context: list[dict[str, Any]],
    ) -> AgentOutput:
        raise NotImplementedError

