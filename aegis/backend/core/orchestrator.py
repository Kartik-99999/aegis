from __future__ import annotations

import traceback
from typing import Any

from agents.base_agent import BaseAgent
from agents.executor_agent import ExecutorAgent
from agents.growth_agent import GrowthAgent
from agents.market_analyst import MarketAnalyst
from agents.psych_agent import PsychAgent
from core.agent_planner import AgentPlanner
from core.debate_engine import DebateEngine
from core.event_bus import EventBus
from core.goal_parser import GoalParser
from core.reflection_engine import ReflectionEngine
from core.schemas import AgentOutput, AgentPlan, DebateResult, ParsedGoal
from memory.session_store import SessionStore
from tools.code_executor import CodeExecutor
from tools.doc_generator import DocGenerator
from tools.email_tool import EmailTool
from tools.scraper import Scraper
from tools.web_search import WebSearchTool


class Orchestrator:
    def __init__(self, event_bus: EventBus, session_store: SessionStore) -> None:
        self.event_bus = event_bus
        self.session_store = session_store
        self.goal_parser = GoalParser()
        self.agent_planner = AgentPlanner()
        self.debate_engine = DebateEngine(event_bus, session_store)
        self.reflection_engine = ReflectionEngine(agent_planner=self.agent_planner)

    async def run(self, goal: str, session_id: str) -> dict[str, Any]:
        try:
            await self._phase(session_id, "parsing_goal")
            parsed = await self.goal_parser.parse(goal)
            await self.event_bus.emit(
                session_id,
                {"type": "goal_parsed", "parsed": parsed.to_dict()},
            )

            await self._phase(session_id, "planning_agents")
            plans = await self.agent_planner.plan(parsed)
            agents = [self.spawn_agent(plan) for plan in plans]

            await self._phase(session_id, "running_agents")
            for plan in plans:
                await self.session_store.update_agent(
                    session_id,
                    plan.name,
                    {
                        "name": plan.name,
                        "role": plan.role,
                        "task": plan.task,
                        "tools": plan.tools,
                        "status": "spawned",
                    },
                )
                await self.event_bus.emit(
                    session_id,
                    {
                        "type": "agent_spawned",
                        "agent": plan.name,
                        "role": plan.role,
                        "task": plan.task,
                        "tools": plan.tools,
                    },
                )

            results = await self._run_agents(session_id, parsed, agents)
            debate_result = await self.debate_engine.run(session_id, agents, results)

            await self._phase(session_id, "synthesizing")
            final = await self.synthesize(goal, parsed, results, debate_result)
            reflection = await self.reflection_engine.reflect(session_id, goal, results, final)
            final["reflection"] = reflection

            await self.session_store.save_result(session_id, final)
            await self.event_bus.emit(
                session_id,
                {"type": "session_complete", "result": final},
            )
            return final
        except Exception as exc:
            error = f"{exc.__class__.__name__}: {exc}"
            await self.session_store.fail(session_id, error)
            await self.event_bus.emit(
                session_id,
                {
                    "type": "session_error",
                    "error": error,
                    "trace": traceback.format_exc(limit=4),
                },
            )
            raise

    async def _phase(self, session_id: str, phase: str) -> None:
        await self.session_store.set_phase(session_id, phase)
        await self.event_bus.emit(session_id, {"type": "phase_update", "phase": phase})

    async def _run_agents(
        self,
        session_id: str,
        parsed: ParsedGoal,
        agents: list[BaseAgent],
    ) -> list[AgentOutput]:
        import asyncio

        return await asyncio.gather(*[agent.run(session_id, parsed) for agent in agents])

    def spawn_agent(self, plan: AgentPlan) -> BaseAgent:
        common = {
            "name": plan.name,
            "role": plan.role,
            "task": plan.task,
            "event_bus": self.event_bus,
            "session_store": self.session_store,
        }
        if plan.agent_type == "market":
            return MarketAnalyst(tools=[WebSearchTool(), Scraper()], **common)
        if plan.agent_type == "psych":
            return PsychAgent(tools=[WebSearchTool()], **common)
        if plan.agent_type == "growth":
            return GrowthAgent(tools=[WebSearchTool(), CodeExecutor()], **common)
        if plan.agent_type == "executor":
            return ExecutorAgent(tools=[DocGenerator(), EmailTool(), CodeExecutor()], **common)
        raise ValueError(f"Unknown agent type: {plan.agent_type}")

    async def synthesize(
        self,
        goal: str,
        parsed: ParsedGoal,
        results: list[AgentOutput],
        debate_result: DebateResult,
    ) -> dict[str, Any]:
        top_recommendations = []
        for output in sorted(results, key=lambda item: item.confidence, reverse=True):
            top_recommendations.extend(output.recommendations[:2])

        action_plan = [
            "Pick one target segment and one primary metric for the next seven days.",
            "Run the highest-confidence offer or messaging experiment first.",
            "Instrument conversion, recovery, and confidence signals before scaling spend.",
            "Use the critic's failure thresholds to decide whether to keep, revise, or kill the experiment.",
        ]

        synthesis = (
            f"AEGIS analyzed the goal '{goal}' as a {parsed.domain} objective. The strongest path is to "
            "tighten the offer around measurable proof, test it quickly with high-intent users, and convert "
            "the result into execution assets before adding channel complexity."
        )
        return {
            "goal": goal,
            "parsed_goal": parsed.to_dict(),
            "synthesis": synthesis,
            "action_plan": action_plan,
            "top_recommendations": top_recommendations[:6],
            "agent_outputs": [output.to_dict() for output in results],
            "debate_transcript": debate_result.transcript,
            "scores": debate_result.scores,
            "winner_logic": debate_result.winner_logic,
        }

