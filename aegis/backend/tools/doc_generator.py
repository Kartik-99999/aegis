from __future__ import annotations

from pathlib import Path


class DocGenerator:
    name = "doc_generator"

    async def write_markdown(self, session_id: str, content: str) -> str:
        output_dir = Path(__file__).resolve().parents[1] / ".data" / "deliverables"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{session_id}.md"
        path.write_text(content, encoding="utf-8")
        return str(path)

