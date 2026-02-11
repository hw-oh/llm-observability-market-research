from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable
from datetime import date

from openai import OpenAI

from intel_bot.config import COMPARISON_CATEGORIES, Settings
from intel_bot.models import (
    AnalysisRun,
    CollectionRun,
    CompetitorAnalysis,
    CompetitorData,
    SynthesisResult,
)

logger = logging.getLogger(__name__)

_DOC_CONTENT_LIMIT = 30_000
_TOTAL_CONTEXT_LIMIT = 80_000

_MAX_ATTEMPTS = 3
_BACKOFF_BASE_SECONDS = 5

SYSTEM_PROMPT = """\
당신은 W&B Weave 팀의 경쟁사 인텔리전스 분석가입니다.
Weave는 LLM 옵저버빌리티 및 평가 플랫폼입니다.

7개 카테고리 프레임워크로 경쟁사를 분석합니다:
1. Core Observability (핵심 옵저버빌리티): Trace 깊이, 계층적 스팬, 프롬프트/응답 로깅, 토큰 추적, 레이턴시 분석, 리플레이
2. Agent / RAG Observability (에이전트/RAG 옵저버빌리티): 도구 호출 추적, 검색 추적, 메모리 추적, 다단계 추론, 워크플로우 그래프, 실패 시각화
3. Evaluation Integration (평가 통합): Trace→데이터셋, LLM-as-Judge, 커스텀 메트릭, 회귀 감지, 모델 비교, 휴먼 피드백
4. Monitoring & Metrics (모니터링 & 메트릭): 비용 대시보드, 토큰 분석, 레이턴시 모니터링, 에러 추적, 도구 성공률, 커스텀 메트릭
5. Experiment / Improvement Loop (실험/개선 루프): 프롬프트/모델/데이터셋 버전 관리, 실험 추적, 지속적 평가, RL/파인튜닝
6. DevEx / Integration (개발자 경험/통합): SDK 지원, 프레임워크 통합, 커스텀 모델, API, 스트리밍, CLI/인프라
7. Enterprise & Security (엔터프라이즈 & 보안): 온프레미스/VPC, RBAC, PII 마스킹, 감사 로그, 데이터 보존, 리전

등급 체계:
- "strong": 해당 기능이 강력하고 성숙함 (●●●)
- "medium": 기본 지원, 일부 제한 (●●)
- "weak": 최소한의 지원 또는 베타 (●)
- "none": 미지원 또는 해당 없음 (-)

사실에 기반하여 구체적으로 분석하세요. 구체적인 기능명과 역량을 인용하세요.
한국어로 응답하세요.\
"""


def _build_categories_schema() -> str:
    """Build JSON schema for categories dynamically from config."""
    categories = []
    for cat in COMPARISON_CATEGORIES:
        features = []
        for item in cat.items:
            features.append(
                f'        {{"item_name": "{item}", "weave_rating": "strong|medium|weak|none", '
                f'"competitor_rating": "strong|medium|weak|none", "note": "간단한 비고"}}'
            )
        features_str = ",\n".join(features)
        categories.append(
            f'    {{\n'
            f'      "category_name": "{cat.name}",\n'
            f'      "features": [\n{features_str}\n      ],\n'
            f'      "summary": "이 카테고리에 대한 2-3문장 요약 (한국어)"\n'
            f'    }}'
        )
    return ",\n".join(categories)


_USER_PROMPT_TEMPLATE = """\
다음 경쟁사를 분석하세요: {competitor_name}

=== 수집된 데이터 ===
{context}
=== 데이터 끝 ===

아래 스키마와 정확히 일치하는 JSON 객체를 반환하세요 (마크다운 펜스 없이, 순수 JSON만):
{{
  "competitor_name": "{competitor_name}",
  "overall_summary": "제품에 대한 2-3문장 요약 (한국어)",
  "categories": [
{categories_schema}
  ],
  "new_features": [
    {{
      "feature_name": "기능명 (한국어)",
      "description": "기능 설명 (한국어)",
      "release_date": "YYYY-MM-DD 또는 YYYY-MM",
      "category": "해당 카테고리 영문명"
    }}
  ],
  "positioning": {{
    "current_position": "현재 포지셔닝 한 문장 (한국어)",
    "moving_toward": "이동 방향 한 문장 (한국어)",
    "signal": "근거가 되는 시그널 (한국어)"
  }},
  "strengths_vs_weave": ["강점 1", "강점 2", ...],
  "weaknesses_vs_weave": ["약점 1", "약점 2", ...]
}}

규칙:
- "categories" 배열은 정확히 7개 항목을 포함해야 합니다 (위 스키마 순서대로)
- 각 카테고리의 "features"는 해당 카테고리의 모든 서브항목을 포함해야 합니다
- "item_name"은 스키마에 지정된 이름을 정확히 사용하세요
- 등급은 "strong", "medium", "weak", "none" 중 하나여야 합니다
- "new_features"는 0-5개 항목 (최근 제품 업데이트만, 없으면 빈 배열)
- "strengths_vs_weave"는 3-5개 항목
- "weaknesses_vs_weave"는 3-5개 항목
- 모든 텍스트는 한국어로 작성하세요
- 순수 JSON만 출력, 마크다운 코드 펜스 없음\
"""

_SYNTHESIS_SYSTEM_PROMPT = """\
당신은 W&B Weave 팀의 시니어 경쟁사 인텔리전스 분석가입니다.
여러 경쟁사 분석 결과를 종합하여 cross-cutting 인사이트를 도출합니다.
한국어로 응답하세요.\
"""

_SYNTHESIS_USER_PROMPT_TEMPLATE = """\
아래는 이번 주 분석된 모든 경쟁사의 개별 분석 결과입니다:

{all_analyses_json}

위 데이터를 종합하여 아래 스키마의 JSON 객체를 반환하세요 (마크다운 펜스 없이, 순수 JSON만):
{{
  "executive_summary": [
    "핵심 인사이트 1 (한국어)",
    "핵심 인사이트 2",
    "핵심 인사이트 3",
    "핵심 인사이트 4",
    "핵심 인사이트 5"
  ],
  "one_line_verdict": "이번 주 Weave의 경쟁 포지션에 대한 한줄 총평 (한국어)",
  "weave_summary": "Weave 제품에 대한 2-3문장 종합 요약. 경쟁사 대비 Weave의 포지셔닝과 핵심 가치 설명 (한국어)",
  "weave_strengths": [
    "Weave를 셀링하는 엔지니어가 강조할 수 있는 강점 1 (한국어)",
    "강점 2",
    ...3-5개...
  ],
  "weave_weaknesses": [
    "경쟁사 대비 Weave가 개선해야 할 영역 1 (한국어)",
    "약점 2",
    ...3-5개...
  ],
  "weave_positioning": {{
    "current_position": "Weave의 현재 시장 포지셔닝 (한국어)",
    "moving_toward": "Weave가 나아가는 방향 (한국어)",
    "signal": "근거가 되는 시그널 (한국어)"
  }},
  "weave_new_features": [
    {{
      "feature_name": "Weave 최근 기능/업데이트명 (한국어)",
      "description": "설명 (한국어)",
      "release_date": "YYYY-MM-DD 또는 YYYY-MM",
      "category": "해당 카테고리 영문명"
    }}
  ],
  "vendor_ratings": [
    {{
      "vendor_name": "Weave",
      "trace_depth": "strong|medium|weak|none",
      "eval": "strong|medium|weak|none",
      "agent_observability": "strong|medium|weak|none",
      "cost_tracking": "strong|medium|weak|none",
      "enterprise_ready": "strong|medium|weak|none",
      "overall": "strong|medium|weak|none"
    }},
    {{
      "vendor_name": "LangSmith",
      ...
    }},
    ...각 경쟁사 포함...
  ],
  "enterprise_signals": [
    "엔터프라이즈 관련 시그널 1 (한국어)",
    ...3-5개...
  ],
  "insights": [
    {{
      "title": "인사이트 제목 (한국어)",
      "body": "2-3문장 설명 (한국어)"
    }},
    ...정확히 3개...
  ],
  "watchlist": [
    "다음 주 주시 항목 1 (한국어)",
    ...3-5개...
  ]
}}

규칙:
- "executive_summary"는 정확히 5개 bullet
- "weave_summary"는 Weave 셀링 엔지니어 관점에서 제품 포지셔닝 요약
- "weave_strengths"는 3-5개 (경쟁사 분석에서 도출한 Weave의 차별화 강점)
- "weave_weaknesses"는 3-5개 (경쟁사가 앞서는 영역, 솔직한 평가)
- "weave_positioning"은 Weave 자체의 시장 포지셔닝 변화
- "weave_new_features"는 0-5개 (경쟁사 데이터에서 언급된 Weave 최신 업데이트. 없으면 빈 배열)
- "vendor_ratings"는 Weave를 포함하여 모든 분석 대상 벤더를 포함해야 합니다
- "enterprise_signals"는 3-5개
- "insights"는 정확히 3개
- "watchlist"는 3-5개
- 등급은 "strong", "medium", "weak", "none" 중 하나
- 모든 텍스트는 한국어로 작성
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
    categories_schema = _build_categories_schema()
    return _USER_PROMPT_TEMPLATE.format(
        competitor_name=name,
        context=context,
        categories_schema=categories_schema,
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


def _parse_synthesis_response(raw: str) -> SynthesisResult:
    text = raw.strip()
    if text.startswith("```"):
        first_newline = text.index("\n")
        text = text[first_newline + 1 :]
    if text.endswith("```"):
        text = text[: text.rfind("```")]
    text = text.strip()

    data = json.loads(text)
    return SynthesisResult.model_validate(data)


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


def synthesize(
    client: OpenAI,
    model: str,
    competitors: list[CompetitorAnalysis],
) -> SynthesisResult:
    all_analyses = [c.model_dump() for c in competitors]
    all_analyses_json = json.dumps(all_analyses, ensure_ascii=False, indent=2)

    user_prompt = _SYNTHESIS_USER_PROMPT_TEMPLATE.format(
        all_analyses_json=all_analyses_json,
    )

    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _SYNTHESIS_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=16384,
            )
            raw = response.choices[0].message.content or ""
            return _parse_synthesis_response(raw)

        except Exception as e:
            last_error = e
            logger.warning(
                "Synthesis attempt %d/%d failed: %s",
                attempt,
                _MAX_ATTEMPTS,
                e,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_BASE_SECONDS * attempt)

    raise RuntimeError(
        f"Failed to synthesize after {_MAX_ATTEMPTS} attempts: {last_error}"
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
        run.competitors.append(analysis)

        if on_progress:
            on_progress(competitor.competitor_name, "done")

    # Step 2: Synthesis
    if on_progress:
        on_progress("종합 분석", "analyzing")

    run.synthesis = synthesize(client, model, run.competitors)

    if on_progress:
        on_progress("종합 분석", "done")

    return run
