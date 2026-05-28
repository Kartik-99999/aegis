from __future__ import annotations

import asyncio
from typing import Any

from agents.base_agent import BaseAgent
from core.schemas import AgentOutput, ParsedGoal
from tools.code_executor import CodeExecutor


class GrowthAgent(BaseAgent):
    async def analyze(
        self,
        session_id: str,
        parsed_goal: ParsedGoal,
        context: list[dict[str, Any]],
    ) -> AgentOutput:
        await self.think(session_id, "Generating experiments and ranking by speed, cost, and upside.")
        executor = next((tool for tool in self.tools if isinstance(tool, CodeExecutor)), None)
        roi_signal = "0.74"
        if executor:
            result = await executor.run_python("print(round((0.42 * 0.6) + (0.28 * 0.8) + 0.26, 2))")
            roi_signal = result["stdout"].strip() or roi_signal
        await asyncio.sleep(0.35)

        if parsed_goal.domain in ["digital media", "defense technology"]:
            await self.think(session_id, f"Calculated audience growth ROI signal: {roi_signal}.")
            recommendations = [
                "Seed the technical articles in specialized defense forums and niche subreddits.",
                "Launch a newsletter pop-up targeted specifically at readers who finish >70% of a UAV or naval fleet article.",
                "Collaborate with niche defense YouTubers or OSINT accounts for backlink building.",
            ]
            content = "Growth plan: Prioritize organic distribution in high-trust defense communities before utilizing paid acquisition."
        else:
            await self.think(session_id, f"Calculated first-pass ROI priority score: {roi_signal}.")
            recommendations = [
                "Run a seven-day offer clarity A/B test on the highest-intent page.",
                "Launch a lifecycle sequence for users who abandon after viewing proof or pricing.",
                "Create one referral or expansion loop tied to the moment users see value.",
            ]
            content = "Growth plan: prioritize experiments that shorten time-to-proof before expanding channels."

        return AgentOutput(
            agent=self.name,
            role=self.role,
            task=self.task,
            content=content,
            confidence=0.76,
            evidence=[f"Computed ROI priority signal: {roi_signal}."],
            recommendations=recommendations,
        )
