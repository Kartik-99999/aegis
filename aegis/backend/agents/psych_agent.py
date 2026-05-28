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
        await self.think(session_id, "Mapping buyer motivation, anxiety, and decision friction.")[cite: 11]
        await asyncio.sleep(0.45)[cite: 11]

        if parsed_goal.domain in ["digital media", "defense technology"]:
            await self.think(session_id, "Mapping reader psychology for specialized defense intelligence.")
            recommendations = [
                "Address reader skepticism by citing primary defense sources rather than secondary news outlets.",
                "Frame UAV and fleet upgrade content around strategic geopolitical impact to engage serious defense enthusiasts.",
                "Use segmentation: separate highly technical deep-dives from accessible weekly roundups.",
            ]
            content = "Psychology read: Defense readers crave authority and hate fluff. The strongest trigger is providing insider-level clarity on complex military technology."
        else:
            await self.think(session_id, "Separating emotional triggers from rational proof points.")[cite: 11]
            recommendations = [
                "Lead with the buyer's desired state, then immediately prove credibility.",[cite: 11]
                "Reduce uncertainty with specific timelines, transparent tradeoffs, and visible guarantees.",[cite: 11]
                "Use segmentation by intent: urgent buyers need proof; curious buyers need low-risk entry.",[cite: 11]
            ]
            content = (
                "Customer psychology read: the goal needs a message architecture that turns broad ambition "
                "into a concrete, believable next step."
            )[cite: 11]

        return AgentOutput(
            agent=self.name,[cite: 11]
            role=self.role,[cite: 11]
            task=self.task,[cite: 11]
            content=content,[cite: 11]
            confidence=0.81,[cite: 11]
            evidence=["High-intent readers respond to primary sources and deep technical accuracy."],
            recommendations=recommendations,[cite: 11]
        )
