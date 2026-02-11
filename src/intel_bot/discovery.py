from __future__ import annotations

import json
import logging
import time
from datetime import date, datetime

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
아래 검색 결과에서 새로운 LLM 옵저버빌리티, 평가, 또는 트레이싱 제품/플랫폼을 추출하세요.

중요: 이미 추적 중인 경쟁사는 포함하지 마세요: {known_list}, W&B Weave, Weights & Biases.
또한 LLM 옵저버빌리티/평가 플랫폼이 아닌 일반 도구는 제외하세요 (예: 일반 APM 도구, 클라우드 제공자, 기본 로깅).

=== 검색 결과 ===
{context}
=== 끝 ===

아래 스키마와 정확히 일치하는 JSON 배열을 반환하세요 (마크다운 펜스 없이, 순수 JSON만):
[
  {{
    "name": "제품명",
    "description": "이 제품이 하는 일에 대한 한 문장 설명 (한국어)",
    "source_url": "https://example.com"
  }}
]

새로운 제품이 없으면 빈 배열을 반환하세요: []
순수 JSON만 출력, 마크다운 코드 펜스 없음."""


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
                            "당신은 경쟁사 인텔리전스 분석가입니다. "
                            "검색 결과에서 새로운 LLM 옵저버빌리티/평가 제품을 추출하세요. "
                            "한국어로 응답하세요."
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
