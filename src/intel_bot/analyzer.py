from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable
from datetime import date

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
You are a competitive intelligence analyst for the W&B Weave team.
Weave is an LLM observability and evaluation platform. Its core capabilities by axis:

- Tracing/Observability: Auto-traces LLM calls, tool calls, agent steps; nested span UI; async support
- Evaluation Pipeline: `weave.Evaluation` runs datasets through models with scorers; diffing across evals
- Dataset Management: First-class `weave.Dataset` objects versioned in W&B; edit via UI or SDK
- Prompt Management: `weave.StringPrompt` / `weave.MessagesPrompt` versioned objects; playground editing
- Scoring: Built-in scorers (hallucination, summarization, SQL); custom Python scorers; LLM-as-judge
- LLM/Framework Integration: OpenAI, Anthropic, LiteLLM, LangChain, LlamaIndex, CrewAI, DSPy auto-patching
- Pricing: Free tier included with W&B; usage-based for Teams/Enterprise
- Self-hosting: W&B Server (on-prem/private cloud) includes Weave; Docker or K8s deployment

Analyze the competitor data provided and compare against Weave on each axis.
Be factual and specific. Cite concrete feature names and capabilities.
Respond in English only.\
"""

_USER_PROMPT_TEMPLATE = """\
Analyze the following competitor: {competitor_name}

=== COLLECTED DATA ===
{context}
=== END COLLECTED DATA ===

Return a JSON object with this exact schema (no markdown fences, raw JSON only):
{{
  "competitor_name": "{competitor_name}",
  "overall_summary": "2-3 sentence summary of the product",
  "axes": [
    {{
      "axis": "<axis name>",
      "summary": "3-5 sentence capability summary for this axis",
      "key_features": ["specific feature 1", "specific feature 2", ...],
      "weave_comparison": "stronger|comparable|weaker|unknown",
      "weave_comparison_reason": "1-2 sentence justification"
    }}
  ],
  "strengths_vs_weave": ["strength 1", "strength 2", ...],
  "weaknesses_vs_weave": ["weakness 1", "weakness 2", ...],
  "notable_updates": ["recent update 1", ...]
}}

Rules:
- "axes" array must contain exactly 8 items, one per axis in this order: {axes_list}
- "weave_comparison" must be one of: "stronger", "comparable", "weaker", "unknown"
  (from the competitor's perspective — "stronger" means the competitor is stronger than Weave)
- "key_features" should list concrete, specific feature names
- "strengths_vs_weave" should have 3-5 items
- "weaknesses_vs_weave" should have 3-5 items
- "notable_updates" should have 0-5 items (recent product updates only)
- Output raw JSON only, no markdown code fences\
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
        run.competitors.append(analysis)

        if on_progress:
            on_progress(competitor.competitor_name, "done")

    return run
