from __future__ import annotations

import asyncio
from typing import Any

from agents.base_agent import BaseAgent
from agents.critic_agent import CriticAgent
from core.event_bus import EventBus
from core.schemas import AgentOutput, DebateResult
from memory.session_store import SessionStore


class DebateEngine:
    def __init__(self, event_bus: EventBus, session_store: SessionStore) -> None:
        self.event_bus = event_bus
        self.session_store = session_store
        self.critic = CriticAgent()

    async def run(
        self,
        session_id: str,
        agents: list[BaseAgent],
        outputs: list[AgentOutput],
    ) -> DebateResult:
        await self.session_store.set_phase(session_id, "debating")
        await self.session_store.update_agent(
            session_id,
            self.critic.name,
            {"name": self.critic.name, "role": self.critic.role, "status": "attacking"},
        )
        await self.event_bus.emit(
            session_id,
            {
                "type": "agent_spawned",
                "agent": self.critic.name,
                "role": self.critic.role,
                "task": "Stress-test every agent output.",
            },
        )
        await self.event_bus.emit(session_id, {"type": "phase_update", "phase": "debating"})

        critiques = await self.critic.attack(outputs)
        transcript: list[dict[str, Any]] = []
        for output in outputs:
            attack = {
                "type": "debate_attack",
                "from": self.critic.name,
                "target": output.agent,
                "text": critiques[output.agent],
            }
            transcript.append(attack)
            await self.event_bus.emit(session_id, attack)

        defenses = await asyncio.gather(
            *[agent.defend(session_id, critiques[agent.name]) for agent in agents]
        )

        scores: dict[str, float] = {}
        for output, defense in zip(outputs, defenses):
            defense_event = {
                "type": "debate_defense",
                "from": output.agent,
                "text": defense,
            }
            transcript.append(defense_event)
            await self.event_bus.emit(session_id, defense_event)

            score = self.critic.score(output, defense)
            scores[output.agent] = score
            await self.session_store.set_score(session_id, output.agent, score)
            await self.event_bus.emit(
                session_id,
                {"type": "score_update", "agent": output.agent, "score": score},
            )

        overall = round(sum(scores.values()) / max(len(scores), 1), 2)
        await self.session_store.set_score(session_id, "Overall", overall)
        await self.event_bus.emit(
            session_id,
            {"type": "score_update", "agent": "Overall", "score": overall},
        )
        await self.session_store.update_agent(session_id, self.critic.name, {"status": "complete"})

        winner = max(scores, key=scores.get)
        return DebateResult(
            scores=scores | {"Overall": overall},
            transcript=transcript,
            winner_logic=f"{winner} carried the strongest combination of output quality, evidence, and defense.",
        )
