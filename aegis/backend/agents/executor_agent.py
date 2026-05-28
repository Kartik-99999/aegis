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
        await self.think(session_id, "Composing concrete deliverables from agent findings.")[cite: 10]
        await asyncio.sleep(0.4)[cite: 10]

        if parsed_goal.domain in ["digital media", "defense technology"]:
            recommendations = [
                "Deliverable 1: Draft a 1,200-word deep dive into specific fleet assets like INS Sahyadri.",
                "Deliverable 2: Create a high-density Twitter/X thread summarizing key UAV tech specs.",
                "Deliverable 3: Set up a dedicated newsletter opt-in for 'Weekly Naval Intelligence'.",
            ]
            content = "Executor draft: Create an editorial sprint focusing on one major naval upgrade and one UAV teardown, repurposing long-form content into highly shareable social threads."
        else:
            recommendations = [
                "Headline: Turn the current bottleneck into a measurable win in 30 days.",[cite: 10]
                "CTA: Start the diagnostic.",[cite: 10]
                "Email angle: Show the cost of inaction, then offer a low-friction audit.",[cite: 10]
            ]
            content = (
                "Executor draft: create a campaign pack with one landing-page hero, a three-email recovery "
                "sequence, and a test brief."
            )[cite: 10]

        generator = next((tool for tool in self.tools if isinstance(tool, DocGenerator)), None)[cite: 10]
        if generator:[cite: 10]
            path = await generator.write_markdown(session_id, content)[cite: 10]
            await self.think(session_id, f"Drafted deliverable artifact at {path}.")[cite: 10]

        return AgentOutput(
            agent=self.name,[cite: 10]
            role=self.role,[cite: 10]
            task=self.task,[cite: 10]
            content=content,[cite: 10]
            confidence=0.84,[cite: 10]
            evidence=[
                "Deliverable structure maps directly to audience retention and newsletter growth."
            ],
            recommendations=recommendations,[cite: 10]
        )
