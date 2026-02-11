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

logger = logging.getLogger(__name__)

_DOC_CONTENT_LIMIT = 30_000
_TOTAL_CONTEXT_LIMIT = 80_000

_MAX_ATTEMPTS = 3
_BACKOFF_BASE_SECONDS = 5

SYSTEM_PROMPT = """\
You are a competitive intelligence analyst for the W&B Weave team.
Weave is an LLM observability and evaluation platform.

You analyze competitors using a 7-category framework:
1. Core Observability: Trace Depth, Hierarchical Spans, Prompt/Response Logging, Token Tracking, Latency Analysis, Replay
2. Agent / RAG Observability: Tool Call Tracing, Retrieval Tracing, Memory Tracing, Multi-step Reasoning, Workflow Graph, Failure Visualization
3. Evaluation Integration: Trace→Dataset, LLM-as-Judge, Custom Eval Metrics, Regression Detection, Model Comparison, Human Feedback
4. Monitoring & Metrics: Cost Dashboard, Token Analytics, Latency Monitoring, Error Tracking, Tool Success Rate, Custom Metrics
5. Experiment / Improvement Loop: Prompt/Model/Dataset Versioning, Experiment Tracking, Continuous Eval, RL/Fine-tuning
6. DevEx / Integration: SDK Support, Framework Integration, Custom Model Support, API Access, Streaming Tracing, CLI/Infra
7. Enterprise & Security: On-prem/VPC, RBAC, PII Masking, Audit Logs, Data Retention, Region Support

Rating scale:
- "strong": Feature is robust and mature (●●●)
- "medium": Basic support with some limitations (●●)
- "weak": Minimal support or beta (●)
- "none": Not supported or not applicable (-)

Analyze based on facts and cite specific feature names and capabilities.

Tone guidelines:
- Be balanced: acknowledge Weave's strengths honestly, then state competitive threats directly
- Always name specific competitors when discussing threats (e.g., "facing pressure from LangSmith on X")
- Use a "maintains lead in X, but faces pressure from Y on Z" structure for verdicts
- Write as a strategist briefing the executive team — candid, not defensive or promotional
- NEVER use phrases like "industry standard", "de facto standard", "gold standard", or "market standard" to describe any competitor (except W&B/Weave). Describe specific capabilities instead.

Respond in English.\
"""


def _build_categories_schema() -> str:
    """Build JSON schema for categories dynamically from config."""
    categories = []
    for cat in COMPARISON_CATEGORIES:
        features = []
        for item in cat.items:
            features.append(
                f'        {{"item_name": "{item}", "weave_rating": "strong|medium|weak|none", '
                f'"competitor_rating": "strong|medium|weak|none", "note": "brief note"}}'
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


_USER_PROMPT_TEMPLATE = """\
Analyze the following competitor: {competitor_name}

=== Collected Data ===
{context}
=== End of Data ===

Return a JSON object that exactly matches the schema below (no markdown fences, pure JSON only):
{{
  "competitor_name": "{competitor_name}",
  "overall_summary": "2-3 sentence summary of the product",
  "categories": [
{categories_schema}
  ],
  "new_features": [
    {{
      "feature_name": "Feature name",
      "description": "Feature description",
      "release_date": "YYYY-MM-DD or YYYY-MM",
      "category": "Category English name"
    }}
  ],
  "positioning": {{
    "current_position": "Current positioning in one sentence",
    "moving_toward": "Direction of movement in one sentence",
    "signal": "Supporting signal"
  }},
  "strengths_vs_weave": ["Strength 1", "Strength 2", ...],
  "weaknesses_vs_weave": ["Weakness 1", "Weakness 2", ...]
}}

Rules:
- "categories" array must contain exactly 7 items (in the schema order above)
- Each category's "features" must include all sub-items for that category
- "item_name" must use the exact names specified in the schema
- Ratings must be one of "strong", "medium", "weak", "none"
- "new_features": 0-5 items (product updates released within the last 30 days ONLY based on today's date {today}. Exclude anything older. Empty array if none.)
- "strengths_vs_weave": 3-5 items
- "weaknesses_vs_weave": 3-5 items
- All text must be written in English
- Pure JSON output only, no markdown code fences\
"""

_SYNTHESIS_SYSTEM_PROMPT = """\
You are a senior competitive intelligence analyst for the W&B Weave team.
You synthesize multiple competitor analyses to derive cross-cutting insights.

Tone guidelines:
- Be balanced: acknowledge Weave's strengths honestly, then state competitive threats directly
- Always name specific competitors when discussing threats (e.g., "facing pressure from LangSmith on X")
- Write as a strategist briefing the executive team — candid, not defensive or promotional
- NEVER use phrases like "industry standard", "de facto standard", "gold standard", or "market standard" to describe any competitor (except W&B/Weave). Describe specific capabilities instead.

Respond in English.\
"""

_SYNTHESIS_USER_PROMPT_TEMPLATE = """\
{weave_data_section}\
Below are the individual analysis results for all competitors analyzed this week:

{all_analyses_json}

Synthesize the above data and return a JSON object matching the schema below (no markdown fences, pure JSON only):
{{
  "weave_summary": "2-3 sentence comprehensive summary of Weave. Explain Weave's positioning and core value vs competitors.",
  "weave_strengths": [
    "Strength a sales engineer could highlight about Weave 1",
    "Strength 2",
    ...3-5 items...
  ],
  "weave_weaknesses": [
    "Area where competitors lead over Weave 1",
    "Weakness 2",
    ...3-5 items...
  ],
  "weave_positioning": {{
    "current_position": "Weave's current market positioning",
    "moving_toward": "Direction Weave is moving toward",
    "signal": "Supporting signal"
  }},
  "weave_new_features": [
    {{
      "feature_name": "Recent Weave feature/update name",
      "description": "Description",
      "release_date": "YYYY-MM-DD or YYYY-MM",
      "category": "Category English name",
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
    ...include all competitors...
  ],
  "enterprise_signals": [
    "Enterprise-related signal 1",
    ...3-5 items...
  ]
}}

Rules:
- "weave_summary": Summarize product positioning from a Weave sales engineer's perspective
- "weave_strengths": 3-5 items (Weave's differentiating strengths derived from competitor analysis)
- "weave_weaknesses": 3-5 items (areas where competitors lead, honest assessment)
- "weave_positioning": Weave's own market positioning shift
- "weave_new_features": 0-5 items (Weave updates from the last 30 days ONLY based on today's date {today}. Empty array if none.)
- "vendor_ratings" must include Weave and all analyzed vendors
- "enterprise_signals": 3-5 items
- Ratings must be one of "strong", "medium", "weak", "none"
- All text must be written in English
- Pure JSON output only, no markdown code fences\
"""

_EXEC_SUMMARY_SYSTEM_PROMPT = """\
You are a senior competitive intelligence strategist writing a weekly briefing \
for the W&B Weave executive team.

Your audience: VP of Product and Engineering leadership who need to make \
strategic decisions this week. They have 2 minutes to read this summary.

Tone:
- Direct and confident, not hedging
- Name names, not "some competitors"
- Honest about gaps — leadership respects candor over cheerleading
- NEVER call any competitor an "industry standard" or "de facto standard" (W&B/Weave is OK)

Respond in English.\
"""

_EXEC_SUMMARY_USER_PROMPT_TEMPLATE = """\
Below is the full synthesis data from this week's competitive analysis:

=== Synthesis Data ===
{synthesis_json}
=== End of Synthesis Data ===

{weave_context_section}\
Write an executive summary as a JSON object (no markdown fences, pure JSON only):
{{
  "executive_summary": ["bullet 1", "bullet 2", ...],
  "one_line_verdict": "single sentence verdict"
}}

Rules for executive_summary (5-7 bullets):
- Lead with the MOST IMPORTANT competitive shift this week — what changed?
- Each bullet must name at least one specific competitor and one specific capability
- Prioritize NEW information: recent releases, positioning shifts, emerging threats
- Include at least 1 bullet on Weave's advantage and 1 on Weave's biggest gap
- Be specific: "Braintrust shipped Java SDK support" not "competitors are expanding"
- Quantify when possible: version numbers, dates, counts
- End with a forward-looking bullet: what should the team watch or act on next?

Rules for one_line_verdict:
- Structure: "Weave [leads/maintains edge/is competitive] in [specific area], \
but faces [specific threat] from [named competitor] on [specific area]"
- Must be actionable — the reader should know what matters most

Pure JSON output only, no markdown code fences.\
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
        today=date.today().isoformat(),
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


@weave.op()
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


@weave.op()
def synthesize(
    client: OpenAI,
    model: str,
    competitors: list[CompetitorAnalysis],
    weave_context: str = "",
) -> SynthesisResult:
    all_analyses = [c.model_dump() for c in competitors]
    all_analyses_json = json.dumps(all_analyses, ensure_ascii=False, indent=2)

    weave_data_section = ""
    if weave_context:
        weave_data_section = (
            "=== Weave Own Data (changelog, releases, docs) ===\n"
            f"{weave_context}\n"
            "=== End of Weave Data ===\n\n"
        )

    user_prompt = _SYNTHESIS_USER_PROMPT_TEMPLATE.format(
        all_analyses_json=all_analyses_json,
        today=date.today().isoformat(),
        weave_data_section=weave_data_section,
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


@weave.op()
def generate_executive_summary(
    client: OpenAI,
    model: str,
    synthesis: SynthesisResult,
    weave_context: str = "",
) -> tuple[list[str], str]:
    """Generate executive summary in a dedicated LLM call for higher quality."""
    synthesis_json = json.dumps(synthesis.model_dump(), ensure_ascii=False, indent=2)

    weave_context_section = ""
    if weave_context:
        weave_context_section = (
            "=== Weave Recent Changes ===\n"
            f"{weave_context}\n"
            "=== End of Weave Changes ===\n\n"
        )

    user_prompt = _EXEC_SUMMARY_USER_PROMPT_TEMPLATE.format(
        synthesis_json=synthesis_json,
        weave_context_section=weave_context_section,
    )

    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _EXEC_SUMMARY_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
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
            return data["executive_summary"], data["one_line_verdict"]

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

    weave_context = ""
    if collection.weave_data:
        weave_context = _build_context(collection.weave_data)

    run.synthesis = synthesize(client, model, run.competitors, weave_context=weave_context)

    if on_progress:
        on_progress("종합 분석", "done")

    # Step 3: Executive Summary (dedicated LLM call)
    if run.synthesis:
        if on_progress:
            on_progress("Executive Summary", "analyzing")

        exec_summary, verdict = generate_executive_summary(
            client, model, run.synthesis, weave_context=weave_context,
        )
        run.synthesis.executive_summary = exec_summary
        run.synthesis.one_line_verdict = verdict

        if on_progress:
            on_progress("Executive Summary", "done")

    return run
