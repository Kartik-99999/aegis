from __future__ import annotations

import asyncio
from typing import Any

from agents.base_agent import BaseAgent
from core.schemas import AgentOutput, ParsedGoal


class PsychAgent(BaseAgent):
    async def analyze(
        self,
        session_id: str,
        parsed_goal: ParsedGoal,
        context: list[dict[str, Any]],
    ) -> AgentOutput:
        await self.think(session_id, "Mapping buyer motivation, anxiety, and decision friction.")
        await asyncio.sleep(0.45)
        await self.think(session_id, "Separating emotional triggers from rational proof points.")

        recommendations = [
            "Lead with the buyer's desired state, then immediately prove credibility.",
            "Reduce uncertainty with specific timelines, transparent tradeoffs, and visible guarantees.",
            "Use segmentation by intent: urgent buyers need proof; curious buyers need low-risk entry.",
        ]
        content = (
            "Customer psychology read: the goal needs a message architecture that turns broad ambition "
            "into a concrete, believable next step. The strongest trigger is relief from uncertainty, "
            "not novelty by itself."
        )
        return AgentOutput(
            agent=self.name,
            role=self.role,
            task=self.task,
            content=content,
            confidence=0.81,
            evidence=[
                "High-intent users respond to concrete outcomes and reduced decision risk.",
                "Trust increases when claims are paired with mechanism, proof, and clear next action.",
            ],
            recommendations=recommendations,
        )

