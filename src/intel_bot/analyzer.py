from __future__ import annotations

import asyncio
import json
import logging
import time
from collections.abc import Callable
from datetime import date

import httpx
from openai import OpenAI

from intel_bot.config import COMPARISON_AXES, Settings
from intel_bot.models import (
    AnalysisRun,
    CollectionRun,
    CompetitorAnalysis,
    CompetitorData,
)

logger = logging.getLogger(__name__)

_DOC_CONTENT_LIMIT = 30_000
_TOTAL_CONTEXT_LIMIT = 80_000

_MAX_ATTEMPTS = 3
_BACKOFF_BASE_SECONDS = 5

SYSTEM_PROMPT = """\
당신은 W&B Weave 팀의 경쟁사 인텔리전스 분석가입니다.
Weave는 LLM 옵저버빌리티 및 평가 플랫폼입니다. 축별 핵심 역량:

- 트레이싱/옵저버빌리티: LLM 호출, 도구 호출, 에이전트 스텝 자동 트레이싱; 중첩 스팬 UI; 비동기 지원
- 평가 파이프라인: `weave.Evaluation`으로 데이터셋 기반 모델 평가 + 스코어러; 평가 간 비교
- 데이터셋 관리: W&B에서 버전 관리되는 `weave.Dataset` 객체; UI 및 SDK로 편집
- 프롬프트 관리: `weave.StringPrompt` / `weave.MessagesPrompt` 버전 관리 객체; 플레이그라운드 편집
- 스코어링: 내장 스코어러(환각, 요약, SQL); 커스텀 Python 스코어러; LLM-as-judge
- LLM/프레임워크 통합: OpenAI, Anthropic, LiteLLM, LangChain, LlamaIndex, CrewAI, DSPy 자동 패칭
- 가격: W&B 포함 무료 티어; Teams/Enterprise 사용량 기반 과금
- 셀프호스팅: W&B Server(온프레미스/프라이빗 클라우드)에 Weave 포함; Docker 또는 K8s 배포

경쟁사 데이터를 분석하고 각 축에서 Weave와 비교하세요.
사실에 기반하여 구체적으로 분석하세요. 구체적인 기능명과 역량을 인용하세요.
한국어로 응답하세요.\
"""

_USER_PROMPT_TEMPLATE = """\
다음 경쟁사를 분석하세요: {competitor_name}

=== 수집된 데이터 ===
{context}
=== 데이터 끝 ===

아래 스키마와 정확히 일치하는 JSON 객체를 반환하세요 (마크다운 펜스 없이, 순수 JSON만):
{{
  "competitor_name": "{competitor_name}",
  "overall_summary": "제품에 대한 2-3문장 요약 (한국어)",
  "axes": [
    {{
      "axis": "<축 이름>",
      "summary": "이 축에 대한 3-5문장 역량 요약 (한국어)",
      "features": [
        {{
          "feature_name": "기능 일반명 (한국어, 예: 자동 트레이싱)",
          "competitor_supported": true,
          "competitor_feature_name": "경쟁사 기능명 (예: LangSmith Traces)",
          "competitor_feature_url": "해당 기능 공식 문서/페이지 URL",
          "weave_supported": true,
          "weave_feature_name": "Weave 기능명 (예: Weave Tracing)",
          "weave_feature_url": "Weave 해당 기능 공식 문서/페이지 URL"
        }}
      ],
      "weave_comparison": "stronger|comparable|weaker|unknown",
      "weave_comparison_reason": "1-2문장 판정 근거 (한국어)"
    }}
  ],
  "strengths_vs_weave": ["강점 1", "강점 2", ...],
  "weaknesses_vs_weave": ["약점 1", "약점 2", ...],
  "notable_updates": ["최근 업데이트 1", ...]
}}

규칙:
- "axes" 배열은 정확히 8개 항목을 포함해야 합니다. 순서: {axes_list}
- "weave_comparison"은 "stronger", "comparable", "weaker", "unknown" 중 하나여야 합니다
  (경쟁사 관점 — "stronger"는 경쟁사가 Weave보다 강함을 의미)
- 각 축에 "features"는 5-8개의 구체적 기능을 포함해야 합니다
- 각 feature에 competitor_feature_url과 weave_feature_url은 해당 기능의 실제 공식 문서 URL이어야 합니다
- URL을 모르면 빈 문자열("")로 남기세요. 절대 추측하지 마세요
- "strengths_vs_weave"는 3-5개 항목
- "weaknesses_vs_weave"는 3-5개 항목
- "notable_updates"는 0-5개 항목 (최근 제품 업데이트만)
- 모든 텍스트는 한국어로 작성하세요
- 순수 JSON만 출력, 마크다운 코드 펜스 없음\
"""


def _create_client(settings: Settings) -> OpenAI:
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key,
    )


def _build_context(competitor: CompetitorData) -> str:
    sections: list[str] = []

    # Search results
    if competitor.search_results:
        lines = ["=== WEB SEARCH RESULTS ==="]
        for sr in competitor.search_results:
            lines.append(f"[Query: {sr.query}] Title: {sr.title}")
            lines.append(f"  Snippet: {sr.snippet}")
            if sr.link:
                lines.append(f"  URL: {sr.link}")
            lines.append("")
        sections.append("\n".join(lines))

    # Docs pages
    if competitor.docs_pages:
        lines = ["=== OFFICIAL DOCUMENTATION ==="]
        for doc in competitor.docs_pages:
            content = doc.content[:_DOC_CONTENT_LIMIT]
            lines.append(f"--- {doc.title} ({doc.url}) ---")
            lines.append(content)
            lines.append("")
        sections.append("\n".join(lines))

    # Feed entries
    if competitor.feed_entries:
        lines = ["=== RECENT UPDATES (GitHub Releases & PyPI) ==="]
        for entry in competitor.feed_entries:
            parts = [f"[{entry.source}]"]
            parts.append(entry.title)
            if entry.published:
                parts.append(f"({entry.published})")
            if entry.summary:
                parts.append(f"- {entry.summary}")
            lines.append(" ".join(parts))
        sections.append("\n".join(lines))

    full_context = "\n\n".join(sections)

    if len(full_context) > _TOTAL_CONTEXT_LIMIT:
        full_context = full_context[:_TOTAL_CONTEXT_LIMIT] + "\n... (truncated)"

    return full_context


def _build_prompt(name: str, context: str) -> str:
    axes_list = ", ".join(COMPARISON_AXES)
    return _USER_PROMPT_TEMPLATE.format(
        competitor_name=name,
        context=context,
        axes_list=axes_list,
    )


def _parse_response(raw: str) -> CompetitorAnalysis:
    text = raw.strip()
    # Remove markdown fences if present
    if text.startswith("```"):
        first_newline = text.index("\n")
        text = text[first_newline + 1 :]
    if text.endswith("```"):
        text = text[: text.rfind("```")]
    text = text.strip()

    data = json.loads(text)
    return CompetitorAnalysis.model_validate(data)


async def _verify_urls(analysis: CompetitorAnalysis) -> CompetitorAnalysis:
    """접근 불가능한 URL을 빈 문자열로 대체"""
    async with httpx.AsyncClient(timeout=5, follow_redirects=True) as client:
        for axis in analysis.axes:
            for feat in axis.features:
                for url_field in ("competitor_feature_url", "weave_feature_url"):
                    url = getattr(feat, url_field)
                    if url:
                        try:
                            resp = await client.head(url)
                            if resp.status_code >= 400:
                                setattr(feat, url_field, "")
                        except Exception:
                            setattr(feat, url_field, "")
    return analysis


def analyze_competitor(
    client: OpenAI,
    model: str,
    competitor: CompetitorData,
) -> CompetitorAnalysis:
    context = _build_context(competitor)
    user_prompt = _build_prompt(competitor.competitor_name, context)

    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=16384,
            )
            raw = response.choices[0].message.content or ""
            return _parse_response(raw)

        except Exception as e:
            last_error = e
            logger.warning(
                "Attempt %d/%d for %s failed: %s",
                attempt,
                _MAX_ATTEMPTS,
                competitor.competitor_name,
                e,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_BASE_SECONDS * attempt)

    raise RuntimeError(
        f"Failed to analyze {competitor.competitor_name} after {_MAX_ATTEMPTS} attempts: {last_error}"
    )


def analyze_all(
    collection: CollectionRun,
    settings: Settings,
    on_progress: Callable[[str, str], None] | None = None,
) -> AnalysisRun:
    client = _create_client(settings)
    model = settings.openrouter_model

    run = AnalysisRun(
        date=date.today().isoformat(),
        model=model,
        collection_date=collection.date,
    )

    for competitor in collection.competitors:
        if on_progress:
            on_progress(competitor.competitor_name, "analyzing")

        analysis = analyze_competitor(client, model, competitor)
        analysis = asyncio.run(_verify_urls(analysis))
        run.competitors.append(analysis)

        if on_progress:
            on_progress(competitor.competitor_name, "done")

    return run
