"""Weave prompt management for LLM analysis prompts.

Prompts are stored as Weave MessagesPrompt objects and versioned automatically.
At runtime, prompts are loaded from Weave if available, with fallback to
hardcoded defaults when WANDB_API_KEY is not set.
"""

from __future__ import annotations

import logging

import weave

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt names (used as Weave object names)
# ---------------------------------------------------------------------------

ANALYSIS_PROMPT_NAME = "analysis-prompt"
SYNTHESIS_PROMPT_NAME = "synthesis-prompt"
EXEC_SUMMARY_PROMPT_NAME = "exec-summary-prompt"

# ---------------------------------------------------------------------------
# Default prompt contents (hardcoded fallbacks)
# ---------------------------------------------------------------------------

_ANALYSIS_SYSTEM = """\
You are a market research analyst covering the LLM observability and evaluation space.

You analyze products using a 7-category framework:
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

Analyze based ONLY on facts found in the provided data. Cite specific feature names and capabilities.
Do NOT infer, speculate, or add information beyond what is in the data.

Respond in English.\
"""

_ANALYSIS_USER = """\
Analyze the following product: {competitor_name}

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
  "strengths": ["Strength 1", "Strength 2", ...],
  "weaknesses": ["Weakness 1", "Weakness 2", ...]
}}

Rules:
- Rate THIS PRODUCT only based on the provided data
- "categories" array must contain exactly 7 items (in the schema order above)
- Each category's "features" must include all sub-items for that category
- "item_name" must use the exact names specified in the schema
- Ratings must be one of "strong", "medium", "weak", "none"
- "new_features": 0-10 items (product updates released within the last 30 days ONLY based on today's date {today}. Exclude anything older. Empty array if none. Include ALL qualifying updates.)
- "strengths": 3-5 notable product strengths
- "weaknesses": 3-5 product weaknesses or gaps
- All text must be written in English
- Pure JSON output only, no markdown code fences\
"""

_SYNTHESIS_SYSTEM = """\
You are a senior market research analyst covering the LLM observability space.
You synthesize multiple product analyses into a market landscape overview.

Respond in English.\
"""

_SYNTHESIS_USER = """\
Below are the individual analysis results for all products analyzed this week:

{all_analyses_json}

Synthesize the above data and return a JSON object matching the schema below (no markdown fences, pure JSON only):
{{
  "market_summary": "2-3 sentence overview of the LLM observability market landscape this week.",
  "product_ratings": [
    {{
      "product_name": "ProductName",
      "trace_depth": "strong|medium|weak|none",
      "trace_depth_note": "one-sentence reason for this rating",
      "eval": "strong|medium|weak|none",
      "eval_note": "one-sentence reason",
      "agent_observability": "strong|medium|weak|none",
      "agent_observability_note": "one-sentence reason",
      "cost_tracking": "strong|medium|weak|none",
      "cost_tracking_note": "one-sentence reason",
      "enterprise_ready": "strong|medium|weak|none",
      "enterprise_ready_note": "one-sentence reason",
      "overall": "strong|medium|weak|none",
      "overall_note": "one-sentence reason"
    }},
    ...include ALL analyzed products...
  ],
  "enterprise_signals": [
    "Enterprise-related signal 1",
    ...3-5 items...
  ]
}}

Rules:
- "market_summary": Factual overview of key market movements this week
- "product_ratings" must include ALL analyzed products
- Each "*_note" field: one factual sentence justifying the rating (cite a specific feature or gap)
- "enterprise_signals": 3-5 items (factual enterprise-related developments from the data)
- Ratings must be one of "strong", "medium", "weak", "none"
- Base ALL conclusions on the provided data only — do not speculate
- All text must be written in English
- Pure JSON output only, no markdown code fences\
"""

_EXEC_SUMMARY_SYSTEM = """\
You are a senior market research analyst writing a weekly briefing \
on the LLM observability market.

Your audience: product and engineering leaders evaluating tools in this space.

Tone:
- Direct and factual
- Name specific products and capabilities
- Do NOT write prescriptive statements (e.g. "X must...", "teams should...")

Respond in English.\
"""

_EXEC_SUMMARY_USER = """\
Below is the full synthesis data from this week's market analysis:

=== Synthesis Data ===
{synthesis_json}
=== End of Synthesis Data ===

Write an executive summary as a JSON object (no markdown fences, pure JSON only):
{{
  "executive_summary": ["bullet 1", "bullet 2", ...],
  "market_insights": ["insight 1", "insight 2", "insight 3"]
}}

Rules for executive_summary (5-7 bullets):
- Summarize WHAT HAPPENED this week in the market — factual, not interpretive
- Each bullet must name at least one specific product and one specific capability
- IMPORTANT: Every analyzed product must be mentioned at least once across all bullets
- Prioritize NEW information: recent releases, positioning shifts
- Be specific: "Braintrust shipped Java SDK support" not "competitors are expanding"
- Quantify when possible: version numbers, dates, counts
- Do NOT add insights, opinions, or recommendations — just report the facts

Rules for market_insights (exactly 3 items):
- Write from Weave's competitive perspective
- Each insight must identify what this means for Weave specifically
  (e.g. "LangSmith's new eval pipeline narrows Weave's lead in evaluation integration")
- Each must name at least one competing product and relate it to Weave
- Keep each to one sentence

Pure JSON output only, no markdown code fences.\
"""

# ---------------------------------------------------------------------------
# Default message lists (used when Weave is not available)
# ---------------------------------------------------------------------------

DEFAULT_ANALYSIS_MESSAGES = [
    {"role": "system", "content": _ANALYSIS_SYSTEM},
    {"role": "user", "content": _ANALYSIS_USER},
]

DEFAULT_SYNTHESIS_MESSAGES = [
    {"role": "system", "content": _SYNTHESIS_SYSTEM},
    {"role": "user", "content": _SYNTHESIS_USER},
]

DEFAULT_EXEC_SUMMARY_MESSAGES = [
    {"role": "system", "content": _EXEC_SUMMARY_SYSTEM},
    {"role": "user", "content": _EXEC_SUMMARY_USER},
]


# ---------------------------------------------------------------------------
# Publish prompts to Weave (run once or when prompts change)
# ---------------------------------------------------------------------------

def publish_prompts() -> None:
    """Publish all prompts to Weave for versioning."""
    analysis_prompt = weave.MessagesPrompt(messages=DEFAULT_ANALYSIS_MESSAGES)
    weave.publish(analysis_prompt, name=ANALYSIS_PROMPT_NAME)
    logger.info("Published %s", ANALYSIS_PROMPT_NAME)

    synthesis_prompt = weave.MessagesPrompt(messages=DEFAULT_SYNTHESIS_MESSAGES)
    weave.publish(synthesis_prompt, name=SYNTHESIS_PROMPT_NAME)
    logger.info("Published %s", SYNTHESIS_PROMPT_NAME)

    exec_summary_prompt = weave.MessagesPrompt(messages=DEFAULT_EXEC_SUMMARY_MESSAGES)
    weave.publish(exec_summary_prompt, name=EXEC_SUMMARY_PROMPT_NAME)
    logger.info("Published %s", EXEC_SUMMARY_PROMPT_NAME)


# ---------------------------------------------------------------------------
# Load prompts at runtime
# ---------------------------------------------------------------------------

def _load_prompt(name: str, default_messages: list[dict]) -> weave.MessagesPrompt:
    """Load a prompt from Weave, falling back to hardcoded default."""
    try:
        prompt = weave.ref(name).get()
        if isinstance(prompt, weave.MessagesPrompt):
            return prompt
        # Handle WeaveObject returned from ref().get()
        return weave.MessagesPrompt.from_obj(prompt)
    except Exception:
        logger.debug("Could not load prompt '%s' from Weave, using default", name)
        return weave.MessagesPrompt(messages=default_messages)


def _is_weave_active() -> bool:
    """Check if Weave has been initialized."""
    try:
        return weave.get_client() is not None
    except Exception:
        return False


def load_analysis_prompt() -> weave.MessagesPrompt:
    if _is_weave_active():
        return _load_prompt(ANALYSIS_PROMPT_NAME, DEFAULT_ANALYSIS_MESSAGES)
    return weave.MessagesPrompt(messages=DEFAULT_ANALYSIS_MESSAGES)


def load_synthesis_prompt() -> weave.MessagesPrompt:
    if _is_weave_active():
        return _load_prompt(SYNTHESIS_PROMPT_NAME, DEFAULT_SYNTHESIS_MESSAGES)
    return weave.MessagesPrompt(messages=DEFAULT_SYNTHESIS_MESSAGES)


def load_exec_summary_prompt() -> weave.MessagesPrompt:
    if _is_weave_active():
        return _load_prompt(EXEC_SUMMARY_PROMPT_NAME, DEFAULT_EXEC_SUMMARY_MESSAGES)
    return weave.MessagesPrompt(messages=DEFAULT_EXEC_SUMMARY_MESSAGES)
