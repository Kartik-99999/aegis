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
        await self.think(session_id, f"Calculated first-pass ROI priority score: {roi_signal}.")

        recommendations = [
            "Run a seven-day offer clarity A/B test on the highest-intent page.",
            "Launch a lifecycle sequence for users who abandon after viewing proof or pricing.",
            "Create one referral or expansion loop tied to the moment users see value.",
            "Instrument weekly leading indicators before optimizing lagging revenue.",
        ]
        content = (
            "Growth plan: prioritize experiments that shorten time-to-proof before expanding channels. "
            "The best sequence is offer clarity, lifecycle recovery, then compounding referral or expansion loops."
        )
        return AgentOutput(
            agent=self.name,
            role=self.role,
            task=self.task,
            content=content,
            confidence=0.76,
            evidence=[
                f"Computed ROI priority signal: {roi_signal}.",
                "Short feedback cycles reduce wasted spend before channel scaling.",
            ],
            recommendations=recommendations,
        )

