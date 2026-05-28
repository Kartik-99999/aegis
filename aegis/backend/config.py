from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "AEGIS"
    environment: str = os.getenv("AEGIS_ENV", "development")
    cors_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv(
            "AEGIS_CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    )
    mongo_url: str | None = os.getenv("MONGO_URL")
    redis_url: str | None = os.getenv("REDIS_URL")
    chroma_host: str | None = os.getenv("CHROMA_HOST")
    jwt_secret: str = os.getenv("JWT_SECRET", "aegis-local-dev-secret")
    model_name: str = os.getenv("AEGIS_MODEL", "local-simulated-agent")
    event_replay_limit: int = int(os.getenv("AEGIS_EVENT_REPLAY_LIMIT", "300"))


settings = Settings()

