from __future__ import annotations

from datetime import datetime

import httpx
import weave

from intel_bot.config import CompetitorConfig
from intel_bot.models import SearchResult

SERPER_URL = "https://google.serper.dev/search"


def _build_queries(competitor: CompetitorConfig) -> list[str]:
    year = datetime.now().year
    name = competitor.name
    return [
        f"{name} LLM observability features {year}",
        f"{name} pricing plans {year}",
    ]


@weave.op()
async def search(
    query: str, api_key: str, num_results: int = 10
) -> list[SearchResult]:
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    payload = {"q": query, "num": num_results}

    async with httpx.AsyncClient() as client:
        resp = await client.post(SERPER_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

    results: list[SearchResult] = []
    for item in data.get("organic", []):
        results.append(
            SearchResult(
                query=query,
                title=item.get("title", ""),
                link=item.get("link", ""),
                snippet=item.get("snippet", ""),
                date=item.get("date"),
            )
        )
    return results


async def search_competitor(
    competitor: CompetitorConfig, api_key: str
) -> list[SearchResult]:
    all_results: list[SearchResult] = []
    for query in _build_queries(competitor):
        try:
            results = await search(query, api_key)
            all_results.extend(results)
        except httpx.HTTPError as e:
            print(f"  [warn] Search failed for '{query}': {e}")
    return all_results
