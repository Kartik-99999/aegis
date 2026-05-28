from __future__ import annotations

import asyncio

from core.schemas import AgentOutput


class CriticAgent:
    name = "Critic Agent"
    role = "Attacks outputs, tests assumptions, and assigns confidence scores."

    async def attack(self, outputs: list[AgentOutput]) -> dict[str, str]:
        await asyncio.sleep(0.25)
        critiques: dict[str, str] = {}
        for output in outputs:
            if len(output.evidence) < 2:
                critique = "Evidence base is thin. Add proof or narrow the recommendation."
            elif output.confidence > 0.86:
                critique = "Confidence may be inflated unless the claim is supported by fresh external data."
            else:
                critique = "Good direction, but quantify the expected impact and define a failure threshold."
            critiques[output.agent] = critique
        return critiques

    def score(self, output: AgentOutput, defense: str) -> float:
        output_quality = output.confidence
        evidence_strength = min(0.95, 0.55 + (len(output.evidence) * 0.1))
        defense_quality = 0.82 if "narrow" in defense.lower() or "supports" in defense.lower() else 0.72
        return round(
            (output_quality * 0.4)
            + (evidence_strength * 0.35)
            + (defense_quality * 0.25),
            2,
        )

