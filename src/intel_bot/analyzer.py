from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable
from datetime import date

import weave
from openai import OpenAI

from intel_bot.config import COMPARISON_CATEGORIES, Settings
from intel_bot.models import (
    AnalysisRun,
    CollectionRun,
    CompetitorAnalysis,
    CompetitorData,
    SynthesisResult,
)
from intel_bot.prompts import (
    load_analysis_prompt,
    load_exec_summary_prompt,
    load_synthesis_prompt,
)

logger = logging.getLogger(__name__)

_DOC_CONTENT_LIMIT = 30_000
_TOTAL_CONTEXT_LIMIT = 80_000

_MAX_ATTEMPTS = 3
_BACKOFF_BASE_SECONDS = 5


def _build_categories_schema() -> str:
    """Build JSON schema for categories dynamically from config."""
    categories = []
    for cat in COMPARISON_CATEGORIES:
        features = []
        for item_name, _ in cat.items:
            features.append(
                f'        {{"item_name": "{item_name}", "rating": "strong|medium|weak|none", "note": "brief note"}}'
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


def _build_context(competitor: CompetitorData) -> str:
    sections: list[str] = []

    # Feed entries (first — most important for new features, avoid truncation)
    if competitor.feed_entries:
        lines = ["=== RECENT UPDATES (GitHub Releases, PyPI, Changelog) ==="]
        for entry in competitor.feed_entries:
            parts = [f"[{entry.source}]"]
            parts.append(entry.title)
            if entry.published:
                parts.append(f"({entry.published})")
            if entry.summary:
                parts.append(f"- {entry.summary}")
            lines.append(" ".join(parts))
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

    # Search results (last — least critical, OK to truncate)
    if competitor.search_results:
        lines = ["=== WEB SEARCH RESULTS ==="]
        for sr in competitor.search_results:
            lines.append(f"[Query: {sr.query}] Title: {sr.title}")
            lines.append(f"  Snippet: {sr.snippet}")
            if sr.link:
                lines.append(f"  URL: {sr.link}")
            lines.append("")
        sections.append("\n".join(lines))

    full_context = "\n\n".join(sections)

    if len(full_context) > _TOTAL_CONTEXT_LIMIT:
        full_context = full_context[:_TOTAL_CONTEXT_LIMIT] + "\n... (truncated)"

    return full_context


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


@weave.op()
def analyze_competitor(
    client: OpenAI,
    model: str,
    competitor: CompetitorData,
) -> CompetitorAnalysis:
    context = _build_context(competitor)
    categories_schema = _build_categories_schema()

    prompt = load_analysis_prompt()
    messages = prompt.format(
        competitor_name=competitor.competitor_name,
        context=context,
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
                competitor.competitor_name,
                e,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_BASE_SECONDS * attempt)

    raise RuntimeError(
        f"Failed to analyze {competitor.competitor_name} after {_MAX_ATTEMPTS} attempts: {last_error}"
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
            text = raw.strip()
            if text.startswith("```"):
                text = text[text.index("\n") + 1 :]
            if text.endswith("```"):
                text = text[: text.rfind("```")]
            text = text.strip()

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
    model = settings.openrouter_model

    run = AnalysisRun(
        date=date.today().isoformat(),
        model=model,
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

        analysis = analyze_competitor(client, model, product)
        run.competitors.append(analysis)

        if on_progress:
            on_progress(product.competitor_name, "done")

    # Step 2: Synthesis
    if on_progress:
        on_progress("종합 분석", "analyzing")

    run.synthesis = synthesize(client, model, run.competitors)

    if on_progress:
        on_progress("종합 분석", "done")

    # Step 3: Executive Summary (dedicated LLM call)
    if run.synthesis:
        if on_progress:
            on_progress("Executive Summary", "analyzing")

        exec_summary, insights = generate_executive_summary(
            client, model, run.synthesis,
        )
        run.synthesis.executive_summary = exec_summary
        run.synthesis.market_insights = insights

        if on_progress:
            on_progress("Executive Summary", "done")

    return run
