from __future__ import annotations


class EmailTool:
    name = "email"

    async def draft(self, subject: str, body: str) -> dict[str, str]:
        return {"subject": subject, "body": body, "status": "drafted"}

