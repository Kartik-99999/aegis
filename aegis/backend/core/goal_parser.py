from __future__ import annotations

import asyncio
import re

from core.schemas import ParsedGoal


class GoalParser:
    async def parse(self, goal: str) -> ParsedGoal:
        await asyncio.sleep(0.15)
        lowered = goal.lower()
        domain = self._detect_domain(lowered)
        objective = self._detect_objective(goal)
        sub_tasks = self._detect_subtasks(lowered)
        signals = {
            "mentions_revenue": any(term in lowered for term in ["revenue", "sales", "arr", "mrr"]),
            "mentions_growth": any(term in lowered for term in ["growth", "scale", "acquisition"]),
            "mentions_customers": any(term in lowered for term in ["customer", "user", "buyer"]),
        }
        return ParsedGoal(goal, domain, objective, sub_tasks, signals)

    def _detect_domain(self, lowered_goal: str) -> str:
        if any(term in lowered_goal for term in ["e-commerce", "shopify", "cart", "checkout"]):
            return "e-commerce"
        if any(term in lowered_goal for term in ["saas", "subscription", "mrr", "arr"]):
            return "saas"
        if any(term in lowered_goal for term in ["course", "creator", "newsletter"]):
            return "creator business"
        if any(term in lowered_goal for term in ["restaurant", "local", "clinic", "salon"]):
            return "local services"
        return "general business"

    def _detect_objective(self, goal: str) -> str:
        percent = re.search(r"(\d+)\s*%", goal)
        if percent:
            return f"Improve target metric by {percent.group(1)}%"
        lowered = goal.lower()
        if "revenue" in lowered:
            return "Increase revenue"
        if "launch" in lowered:
            return "Launch a new initiative"
        if "reduce" in lowered:
            return "Reduce friction or cost"
        return "Solve the stated business goal"

    def _detect_subtasks(self, lowered_goal: str) -> list[str]:
        tasks = ["market_analysis", "user_psychology", "growth_plan", "deliverable_execution"]
        if any(term in lowered_goal for term in ["risk", "validate", "confidence"]):
            tasks.append("critique")
        return tasks

