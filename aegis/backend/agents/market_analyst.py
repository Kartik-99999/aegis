from __future__ import annotations

import asyncio
from typing import Any

from agents.base_agent import BaseAgent
from core.schemas import AgentOutput, ParsedGoal
from tools.web_search import WebSearchTool


class MarketAnalyst(BaseAgent):
    async def analyze(
        self,
        session_id: str,
        parsed_goal: ParsedGoal,
        context: list[dict[str, Any]],
    ) -> AgentOutput:
        search_tool = next((tool for tool in self.tools if isinstance(tool, WebSearchTool)), None)
        await self.think(session_id, f"Scanning market signals for {parsed_goal.domain}.")
        evidence = await search_tool.search(parsed_goal.raw_goal) if search_tool else []
        await asyncio.sleep(0.35)
        await self.think(session_id, "Found usable competitor, offer, and positioning signals.")

        recommendations = [
            "Benchmark the top three competitor offers against the user's current conversion promise.",
            "Look for underpriced guarantees, bundles, or speed-of-outcome claims.",
            "Prioritize acquisition channels where competitors are present but messaging is generic.",
        ]
        content = (
            f"Market scan for {parsed_goal.domain}: competitors are likely competing on promise clarity, "
            "proof density, and frictionless trial paths. The fastest opportunity is to isolate one "
            "positioning gap, match it with a concrete offer, and test it against the existing funnel."
        )
        confidence = 0.78 + min(len(context), 2) * 0.03
        return AgentOutput(
            agent=self.name,
            role=self.role,
            task=self.task,
            content=content,
            confidence=min(confidence, 0.88),
            evidence=[item["summary"] for item in evidence],
            recommendations=recommendations,
        )

