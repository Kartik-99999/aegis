from __future__ import annotations

import asyncio


class Scraper:
    name = "scraper"

    async def scrape_summary(self, url: str) -> dict[str, str]:
        await asyncio.sleep(0.1)
        return {"url": url, "summary": "MVP scraper placeholder. Add Playwright extraction here."}

