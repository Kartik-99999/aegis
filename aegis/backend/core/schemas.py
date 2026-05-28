from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ParsedGoal:
    raw_goal: str
    domain: str
    objective: str
    sub_tasks: list[str]
    signals: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentPlan:
    name: str
    role: str
    agent_type: str
    task: str
    tools: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentOutput:
    agent: str
    role: str
    task: str
    content: str
    confidence: float
    evidence: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DebateResult:
    scores: dict[str, float]
    transcript: list[dict[str, Any]]
    winner_logic: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

