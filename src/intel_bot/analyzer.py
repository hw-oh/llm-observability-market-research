from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable
from datetime import date

import weave
from openai import OpenAI

from intel_bot.config import COMPARISON_CATEGORIES, CategoryDef, Settings
from intel_bot.models import (
    AnalysisRun,
    CategoryAnalysis,
    CollectionRun,
    CompetitorAnalysis,
    CompetitorData,
    DocsPage,
    FeedEntry,
    SearchResult,
    SynthesisResult,
)
from intel_bot.prompts import (
    load_analysis_prompt,
    load_category_analysis_prompt,
    load_exec_summary_prompt,
    load_synthesis_prompt,
)

logger = logging.getLogger(__name__)

_DOC_CONTENT_LIMIT = 30_000

_MAX_ATTEMPTS = 3
_BACKOFF_BASE_SECONDS = 5


def _build_categories_schema() -> str:
    """Build JSON schema for categories dynamically from config."""
    categories = []
    for cat in COMPARISON_CATEGORIES:
        features = []
        for item_name, _ in cat.items:
            features.append(
                f'        {{"item_name": "{item_name}", "rating": "strong|medium|none", "note": "brief note"}}'
            )
        features_str = ",\n".join(features)
        categories.append(
            f'    {{\n'
            f'      "category_name": "{cat.name}",\n'
            f'      "features": [\n{features_str}\n      ],\n'
            f'      "summary": "2-3 sentence summary for this category"\n'
            f'    }}'
        )
    return ",\n".join(categories)


def _create_client(settings: Settings) -> OpenAI:
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key,
    )


def _strip_markdown_fences(raw: str) -> str:
    """Remove markdown code fences from LLM response."""
    text = raw.strip()
    if text.startswith("```"):
        first_newline = text.index("\n")
        text = text[first_newline + 1:]
    if text.endswith("```"):
        text = text[:text.rfind("```")]
    return text.strip()


def _build_search_context(search_results: list[SearchResult]) -> str:
    """Build search context string from search results."""
    lines: list[str] = []
    for sr in search_results:
        lines.append(f"[Query: {sr.query}] Title: {sr.title}")
        lines.append(f"  Snippet: {sr.snippet}")
        if sr.link:
            lines.append(f"  URL: {sr.link}")
        lines.append("")
    return "\n".join(lines)


def _build_items_schema(category: CategoryDef) -> str:
    """Build items schema for category analysis prompt."""
    lines: list[str] = []
    for item_name, description in category.items:
        lines.append(f"- {item_name}: {description}")
    return "\n".join(lines)


def _build_feed_context(feed_entries: list[FeedEntry]) -> str:
    """Build feed context string from feed entries."""
    if not feed_entries:
        return "(no recent updates)"
    lines: list[str] = []
    for entry in feed_entries:
        parts = [f"[{entry.source}]"]
        parts.append(entry.title)
        if entry.published:
            parts.append(f"({entry.published})")
        if entry.summary:
            parts.append(f"- {entry.summary}")
        lines.append(" ".join(parts))
    return "\n".join(lines)


def _build_category_summaries(category_results: list[CategoryAnalysis]) -> str:
    """Serialize Flash category results for Pro prompt."""
    summaries = []
    for cat in category_results:
        summaries.append(cat.model_dump())
    return json.dumps(summaries, ensure_ascii=False, indent=2)


def _parse_response(raw: str) -> CompetitorAnalysis:
    text = _strip_markdown_fences(raw)
    data = json.loads(text)
    return CompetitorAnalysis.model_validate(data)


def _parse_category_response(raw: str) -> CategoryAnalysis:
    text = _strip_markdown_fences(raw)
    data = json.loads(text)
    return CategoryAnalysis.model_validate(data)


def _parse_synthesis_response(raw: str) -> SynthesisResult:
    text = _strip_markdown_fences(raw)
    data = json.loads(text)
    return SynthesisResult.model_validate(data)


# ---- Stage 1: Flash — Category-level analysis ----

@weave.op()
def analyze_category(
    client: OpenAI,
    model: str,
    competitor_name: str,
    category: CategoryDef,
    search_results: list[SearchResult],
    extra_docs: list[DocsPage] | None = None,
) -> CategoryAnalysis:
    """Flash 모델로 단일 카테고리 분석."""
    search_context = _build_search_context(search_results)

    # Append extra docs if provided (e.g., Weave Enterprise docs)
    if extra_docs:
        doc_lines = ["\n=== Additional Documentation ==="]
        for doc in extra_docs:
            content = doc.content[:_DOC_CONTENT_LIMIT]
            doc_lines.append(f"--- {doc.title} ({doc.url}) ---")
            doc_lines.append(content)
            doc_lines.append("")
        search_context += "\n".join(doc_lines)

    items_schema = _build_items_schema(category)

    prompt = load_category_analysis_prompt()
    messages = prompt.format(
        competitor_name=competitor_name,
        category_name=category.name,
        items_schema=items_schema,
        search_context=search_context,
    )

    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.0,
                max_tokens=4096,
            )
            raw = response.choices[0].message.content or ""
            return _parse_category_response(raw)

        except Exception as e:
            last_error = e
            logger.warning(
                "Category %s attempt %d/%d for %s failed: %s",
                category.name,
                attempt,
                _MAX_ATTEMPTS,
                competitor_name,
                e,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_BASE_SECONDS * attempt)

    raise RuntimeError(
        f"Failed to analyze {competitor_name}/{category.name} after {_MAX_ATTEMPTS} attempts: {last_error}"
    )


# ---- Stage 2: Pro — Comprehensive analysis ----

@weave.op()
def analyze_competitor(
    client: OpenAI,
    model: str,
    competitor_name: str,
    category_results: list[CategoryAnalysis],
    feed_entries: list[FeedEntry],
) -> CompetitorAnalysis:
    """Pro 모델로 종합 분석. Flash의 카테고리 결과를 바탕으로."""
    category_summaries = _build_category_summaries(category_results)
    feed_context = _build_feed_context(feed_entries)
    categories_schema = _build_categories_schema()

    prompt = load_analysis_prompt()
    messages = prompt.format(
        competitor_name=competitor_name,
        category_summaries=category_summaries,
        feed_context=feed_context,
        categories_schema=categories_schema,
        today=date.today().isoformat(),
    )

    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.0,
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
                competitor_name,
                e,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_BASE_SECONDS * attempt)

    raise RuntimeError(
        f"Failed to analyze {competitor_name} after {_MAX_ATTEMPTS} attempts: {last_error}"
    )


@weave.op()
def synthesize(
    client: OpenAI,
    model: str,
    competitors: list[CompetitorAnalysis],
) -> SynthesisResult:
    all_analyses = [c.model_dump() for c in competitors]
    all_analyses_json = json.dumps(all_analyses, ensure_ascii=False, indent=2)

    prompt = load_synthesis_prompt()
    messages = prompt.format(all_analyses_json=all_analyses_json)

    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.0,
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


@weave.op()
def generate_executive_summary(
    client: OpenAI,
    model: str,
    synthesis: SynthesisResult,
) -> tuple[list[str], list[str]]:
    """Generate executive summary in a dedicated LLM call."""
    synthesis_json = json.dumps(synthesis.model_dump(), ensure_ascii=False, indent=2)

    prompt = load_exec_summary_prompt()
    messages = prompt.format(synthesis_json=synthesis_json)

    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.0,
                max_tokens=4096,
            )
            raw = response.choices[0].message.content or ""
            text = _strip_markdown_fences(raw)

            data = json.loads(text)
            return data["executive_summary"], data["market_insights"]

        except Exception as e:
            last_error = e
            logger.warning(
                "Executive summary attempt %d/%d failed: %s",
                attempt,
                _MAX_ATTEMPTS,
                e,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_BASE_SECONDS * attempt)

    raise RuntimeError(
        f"Failed to generate executive summary after {_MAX_ATTEMPTS} attempts: {last_error}"
    )


def analyze_all(
    collection: CollectionRun,
    settings: Settings,
    on_progress: Callable[[str, str], None] | None = None,
) -> AnalysisRun:
    client = _create_client(settings)
    flash_model = settings.translation_model   # gemini-3-flash-preview (재사용)
    pro_model = settings.openrouter_model       # gemini-3-pro-preview

    run = AnalysisRun(
        date=date.today().isoformat(),
        model=pro_model,
        collection_date=collection.date,
    )

    # Analyze all products (Weave first, then competitors)
    all_products: list[CompetitorData] = []
    if collection.weave_data:
        all_products.append(collection.weave_data)
    all_products.extend(collection.competitors)

    for product in all_products:
        if on_progress:
            on_progress(product.competitor_name, "analyzing")

        # Stage 1: Flash — 카테고리별 분석 (7회)
        category_results: list[CategoryAnalysis] = []
        for cat_def in COMPARISON_CATEGORIES:
            cat_search = product.category_search_results.get(cat_def.name, [])
            extra_docs = product.docs_pages if cat_def.name == "Enterprise & Security" else None
            result = analyze_category(
                client, flash_model, product.competitor_name,
                cat_def, cat_search, extra_docs,
            )
            category_results.append(result)

        # Stage 2: Pro — 종합 분석 (1회)
        analysis = analyze_competitor(
            client, pro_model, product.competitor_name,
            category_results, product.feed_entries,
        )
        run.competitors.append(analysis)

        if on_progress:
            on_progress(product.competitor_name, "done")

    # Step 2: Synthesis
    if on_progress:
        on_progress("종합 분석", "analyzing")

    run.synthesis = synthesize(client, pro_model, run.competitors)

    if on_progress:
        on_progress("종합 분석", "done")

    # Step 3: Executive Summary (dedicated LLM call)
    if run.synthesis:
        if on_progress:
            on_progress("Executive Summary", "analyzing")

        exec_summary, insights = generate_executive_summary(
            client, pro_model, run.synthesis,
        )
        run.synthesis.executive_summary = exec_summary
        run.synthesis.market_insights = insights

        if on_progress:
            on_progress("Executive Summary", "done")

    return run
