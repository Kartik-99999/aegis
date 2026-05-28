from __future__ import annotations

from core.event_bus import EventBus
from core.orchestrator import Orchestrator
from memory.session_store import SessionStore


event_bus = EventBus()
session_store = SessionStore()
orchestrator = Orchestrator(event_bus=event_bus, session_store=session_store)

