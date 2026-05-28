from __future__ import annotations

import asyncio


class WebSearchTool:
    name = "web_search"

    async def search(self, query: str) -> list[dict[str, str]]:
        await asyncio.sleep(0.15)
        return [
            {
                "title": "Competitor pricing snapshot",
                "url": "https://example.com/market-scan",
                "summary": f"Observed demand and pricing signals related to: {query}",
            },
            {
                "title": "Customer behavior pattern",
                "url": "https://example.com/customer-research",
                "summary": "Customers respond best to concrete ROI, low-friction trials, and urgency tied to outcomes.",
            },
            {
                "title": "Growth experiment benchmark",
                "url": "https://example.com/growth-benchmark",
                "summary": "Lifecycle experiments and conversion improvements tend to compound when measured weekly.",
            },
        ]

