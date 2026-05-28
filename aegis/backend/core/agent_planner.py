from __future__ import annotations

import asyncio

from core.schemas import AgentPlan, ParsedGoal


class AgentPlanner:
    def __init__(self) -> None:
        self.weights = {
            "market": 1.0,
            "psych": 1.0,
            "growth": 1.0,
            "executor": 1.0,
        }

    async def plan(self, parsed_goal: ParsedGoal) -> list[AgentPlan]:
        await asyncio.sleep(0.15)
        plans = [
            AgentPlan(
                name="Market Analyst",
                role="Competitor research, market sizing, and positioning gaps.",
                agent_type="market",
                task=f"Find market opportunities for: {parsed_goal.objective}",
                tools=["web_search", "scraper"],
            ),
            AgentPlan(
                name="Psych Agent",
                role="Customer behavior, objections, and emotional triggers.",
                agent_type="psych",
                task=f"Map customer psychology in {parsed_goal.domain}.",
                tools=["web_search", "doc_reader"],
            ),
            AgentPlan(
                name="Growth Agent",
                role="Experiment generation, ROI ranking, and metrics design.",
                agent_type="growth",
                task=f"Rank growth experiments for: {parsed_goal.objective}",
                tools=["web_search", "code_executor"],
            ),
            AgentPlan(
                name="Executor Agent",
                role="Produces deliverables, copy, briefs, and implementation-ready assets.",
                agent_type="executor",
                task="Turn winning strategy into concrete campaign assets.",
                tools=["doc_generator", "email", "code_executor"],
            ),
        ]

        if parsed_goal.signals.get("mentions_growth"):
            plans[2].task = f"Generate 50 hypotheses and shortlist the top 5 for {parsed_goal.domain}."

        return plans

    async def update_weights(self, updates: dict[str, float]) -> None:
        for key, value in updates.items():
            if key in self.weights:
                self.weights[key] = max(0.2, min(2.0, value))

