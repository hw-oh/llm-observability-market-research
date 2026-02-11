from __future__ import annotations

import json
import logging
import time
from datetime import date, datetime

import weave
from openai import OpenAI

from intel_bot.collectors.serper import search
from intel_bot.config import COMPETITORS, Settings
from intel_bot.models import DiscoveryResult, EmergingCompetitor, SearchResult

logger = logging.getLogger(__name__)

_MAX_ATTEMPTS = 3
_BACKOFF_BASE_SECONDS = 5

_KNOWN_NAMES = {c.name.lower() for c in COMPETITORS}
# Also add common short forms to avoid false negatives
_KNOWN_NAMES |= {"weave", "w&b", "wandb", "weights & biases", "weights and biases"}


def _build_discovery_queries() -> list[str]:
    year = datetime.now().year
    return [
        f"LLM observability platform {year}",
        f"LLM evaluation tool startup {year}",
        f"AI agent tracing monitoring tool {year}",
    ]


async def search_emerging(api_key: str) -> tuple[list[str], list[SearchResult]]:
    queries = _build_discovery_queries()
    all_results: list[SearchResult] = []
    for query in queries:
        try:
            results = await search(query, api_key)
            all_results.extend(results)
        except Exception as e:
            logger.warning("Discovery search failed for '%s': %s", query, e)
    return queries, all_results


def _build_extraction_prompt(results: list[SearchResult]) -> str:
    known_list = ", ".join(c.name for c in COMPETITORS)
    context_lines: list[str] = []
    for r in results:
        context_lines.append(f"Title: {r.title}")
        context_lines.append(f"  Snippet: {r.snippet}")
        context_lines.append(f"  URL: {r.link}")
        context_lines.append("")

    context = "\n".join(context_lines)

    return f"""\
Extract new LLM observability, evaluation, or tracing products/platforms from the search results below.

Important: Do NOT include competitors already being tracked: {known_list}, W&B Weave, Weights & Biases.
Also exclude general-purpose tools that are not LLM observability/evaluation platforms (e.g., generic APM tools, cloud providers, basic logging).

=== Search Results ===
{context}
=== End ===

Return a JSON array that exactly matches the schema below (no markdown fences, pure JSON only):
[
  {{
    "name": "Product name",
    "description": "One-sentence description of what this product does",
    "source_url": "https://example.com"
  }}
]

If there are no new products, return an empty array: []
Pure JSON output only, no markdown code fences."""


@weave.op()
def extract_emerging_competitors(
    client: OpenAI,
    model: str,
    results: list[SearchResult],
) -> list[EmergingCompetitor]:
    if not results:
        return []

    prompt = _build_extraction_prompt(results)
    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a competitive intelligence analyst. "
                            "Extract new LLM observability/evaluation products from search results. "
                            "Respond in English."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=2048,
            )
            raw = response.choices[0].message.content or "[]"

            # Strip markdown fences if present
            text = raw.strip()
            if text.startswith("```"):
                first_newline = text.index("\n")
                text = text[first_newline + 1 :]
            if text.endswith("```"):
                text = text[: text.rfind("```")]
            text = text.strip()

            data = json.loads(text)
            candidates = [EmergingCompetitor.model_validate(item) for item in data]

            # Second-pass filter: remove any known competitors by name
            filtered = [
                c for c in candidates if c.name.lower() not in _KNOWN_NAMES
            ]
            return filtered

        except Exception as e:
            last_error = e
            logger.warning(
                "Discovery extraction attempt %d/%d failed: %s",
                attempt,
                _MAX_ATTEMPTS,
                e,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_BASE_SECONDS * attempt)

    logger.error("Discovery extraction failed after %d attempts: %s", _MAX_ATTEMPTS, last_error)
    return []


async def discover(settings: Settings) -> DiscoveryResult:
    today = date.today().isoformat()

    queries, search_results = await search_emerging(settings.serper_dev_api)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key,
    )

    emerging = extract_emerging_competitors(
        client, settings.openrouter_model, search_results
    )

    return DiscoveryResult(
        date=today,
        queries=queries,
        search_results_count=len(search_results),
        emerging_competitors=emerging,
    )
