from __future__ import annotations

import asyncio
from typing import Any

from agents.base_agent import BaseAgent
from core.schemas import AgentOutput, ParsedGoal
from tools.doc_generator import DocGenerator


class ExecutorAgent(BaseAgent):
    async def analyze(
        self,
        session_id: str,
        parsed_goal: ParsedGoal,
        context: list[dict[str, Any]],
    ) -> AgentOutput:
        await self.think(session_id, "Composing concrete deliverables from agent findings.")
        await asyncio.sleep(0.4)

        recommendations = [
            "Headline: Turn the current bottleneck into a measurable win in 30 days.",
            "CTA: Start the diagnostic.",
            "Email angle: Show the cost of inaction, then offer a low-friction audit.",
        ]
        content = (
            "Executor draft: create a campaign pack with one landing-page hero, a three-email recovery "
            "sequence, and a test brief. Each artifact should make the promise, mechanism, proof, and next step visible."
        )

        generator = next((tool for tool in self.tools if isinstance(tool, DocGenerator)), None)
        if generator:
            path = await generator.write_markdown(session_id, content)
            await self.think(session_id, f"Drafted deliverable artifact at {path}.")

        return AgentOutput(
            agent=self.name,
            role=self.role,
            task=self.task,
            content=content,
            confidence=0.84,
            evidence=[
                "Deliverable structure maps directly to promise, proof, mechanism, and CTA.",
                "Artifacts are scoped for fast execution rather than broad strategy theater.",
            ],
            recommendations=recommendations,
        )

