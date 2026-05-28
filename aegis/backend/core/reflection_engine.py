from __future__ import annotations

from typing import Any

from core.agent_planner import AgentPlanner
from core.schemas import AgentOutput
from memory.vector_store import VectorStore


class ReflectionEngine:
    def __init__(
        self,
        vector_store: VectorStore | None = None,
        agent_planner: AgentPlanner | None = None,
    ) -> None:
        self.vector_store = vector_store or VectorStore()
        self.agent_planner = agent_planner or AgentPlanner()

    async def reflect(
        self,
        session_id: str,
        goal: str,
        results: list[AgentOutput],
        final_output: dict[str, Any],
    ) -> dict[str, Any]:
        best_agent = max(results, key=lambda output: output.confidence).agent if results else "n/a"
        weakest_agent = min(results, key=lambda output: output.confidence).agent if results else "n/a"
        reflection = {
            "improvements": [
                "Prefer agents with concrete deliverables when the goal asks for execution.",
                "Require fresh evidence before allowing confidence above 0.86.",
                "Keep debate critiques tied to measurable failure thresholds.",
            ],
            "agent_weights_update": {
                "executor": 1.08 if best_agent == "Executor Agent" else 1.0,
                "growth": 1.05 if "growth" in goal.lower() else 1.0,
            },
            "playbook_patch": {
                "best_agent": best_agent,
                "weakest_agent": weakest_agent,
                "next_run_hint": "Ask each agent for one measurable next action and one kill criterion.",
            },
        }
        await self.agent_planner.update_weights(reflection["agent_weights_update"])
        await self.vector_store.store("reflection_store", f"reflection:{session_id}", reflection)
        await self.vector_store.store("playbook", f"playbook:{session_id}", reflection["playbook_patch"])
        return reflection

