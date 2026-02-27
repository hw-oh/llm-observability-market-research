"""Agent and task prompts — stored in Weave for version tracking.

Each prompt is a ``weave.StringPrompt`` with ``{variable}`` placeholders.
``load_prompts()`` fetches the latest versions from Weave (falls back to the
defaults defined here), and ``publish_prompts()`` pushes the defaults to Weave.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import weave

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default prompt values — 3-agent pipeline
# ---------------------------------------------------------------------------

UPDATE_COLLECTOR_BACKSTORY = (
    "You are a product update specialist monitoring the LLM observability "
    "and evaluation space. You track changelogs, release notes, and product "
    "announcements to identify recent feature additions, changes, and "
    "deprecations across competing products."
)

BASELINE_ANALYZER_BACKSTORY = (
    "You are a senior competitive intelligence analyst who maintains "
    "detailed product feature baselines. You meticulously compare new "
    "update information against existing baseline data to identify "
    "changes in feature availability, provision methods, and capabilities. "
    "You update every relevant field precisely and document all changes."
)

REPORT_WRITER_BACKSTORY = (
    "You are a VP-level market research analyst creating executive briefings "
    "on the LLM observability market. You compare products objectively, "
    "rate features conservatively based on evidence, and write concise "
    "commentary that highlights this week's notable changes and names "
    "specific products and capabilities."
)

UPDATE_COLLECTOR_TASK = (
    "Identify RECENT updates and changes for {product_name} in the LLM "
    "observability and evaluation space.\n\n"
    "=== Changelog / Release Notes (scraped) ===\n"
    "{changelog_content}\n"
    "=== End Changelog ===\n\n"
    "{product_desc}\n\n"
    "{changelog_filter_hint}\n\n"
    "=== Current Baseline Features (already known) ===\n"
    "{baseline_summary}\n"
    "=== End Baseline ===\n\n"
    "Instructions:\n"
    "- Focus on updates from the last 7 days relative to {date}\n"
    "- CRITICAL: The baseline above lists features we ALREADY know about. "
    "Do NOT report existing features as updates. Only report genuinely NEW "
    "capabilities, NEW integrations, or CHANGED behavior that is not yet "
    "reflected in the baseline.\n"
    "- If a changelog entry describes a feature already listed in the "
    "baseline, skip it entirely.\n"
    "- For each genuine update, provide: title, date (if available), and a "
    "concise summary of what changed\n"
    "- Include feature additions, API changes, deprecations, and "
    "significant improvements\n"
    "- Also search the web for any recent announcements, blog posts, or "
    "community discussions about new {product_name} features that may not "
    "appear in the changelog\n"
    '- product_name must be exactly "{product_name}"'
)

BASELINE_ANALYZER_TASK = (
    "Analyze the recent updates for {product_name} and update the product "
    "baseline accordingly.\n\n"
    "=== Recent Updates Found ===\n"
    "{updates_json}\n"
    "=== End Updates ===\n\n"
    "=== Current Baseline (last updated: {baseline_date}) ===\n"
    "{baseline_json}\n"
    "=== End Baseline ===\n\n"
    "{url_context}\n\n"
    "The baseline uses a sub_features structure. Each feature item has:\n"
    "- item_name: standardized name (49 items)\n"
    "- available: yes/no/partial\n"
    "- sub_features: list of {{name, provision_method, notes}}\n\n"
    "Instructions:\n"
    "- Compare each update against the existing baseline sub_features\n"
    "- A change is ONLY one of these:\n"
    "  1. A NEW sub_feature that does not exist in the baseline (record "
    "with sub_feature_name=\"NEW\", field=\"name\", before=\"\", after=new name)\n"
    "  2. available changed (e.g., \"no\" to \"yes\")\n"
    "  3. provision_method of an existing sub_feature changed\n"
    "- Do NOT record a change for:\n"
    "  - Notes wording enrichment (adding detail to existing notes)\n"
    "  - Features already present in the baseline with the same status\n"
    "  - Mere mentions of existing features in the update\n"
    "- When adding a new sub_feature, add it to the appropriate item's "
    "sub_features list in the updated_baseline\n"
    "- The updated_baseline must contain ALL {num_categories} categories "
    "with ALL feature items — not just the changed ones\n"
    "- category_name values must match EXACTLY as listed below WITHOUT "
    "numeric prefixes (e.g., use \"Core Tracing & Logging\" NOT "
    "\"1. Core Tracing & Logging\"):\n"
    "{categories_desc}\n"
    "- If no changes are found for a feature, preserve it exactly as-is\n"
    "- updated_baseline.last_updated must be {date}\n"
    '- product_name must be exactly "{product_name}"'
)

REPORT_WRITER_TASK = (
    "Produce a cross-product comparison report based on the latest baseline "
    "data and this week's changes.\n\n"
    "=== This Week's Changes ===\n"
    "{all_changesets_json}\n"
    "=== End Changes ===\n\n"
    "=== All Product Baselines ===\n"
    "{all_baselines_json}\n"
    "=== End Baselines ===\n\n"
    "Produce a ReportSynthesis output with:\n"
    "1. ai_comment: an AIComment object containing:\n"
    "   a) product_highlights: a list of ProductHighlight objects — one per "
    "product. Each has product_name (must exactly match baseline) and summary "
    "(1-2 concise sentences highlighting this product's key strengths or "
    "notable recent changes)\n"
    "   b) market_trend: a single sentence summarizing the overall market "
    "trend or competitive dynamics this week\n"
    "2. categories: for each of the {num_categories} categories below, rate "
    "every product on every feature item.\n"
    "{categories_desc}\n\n"
    "Rating scale:\n"
    '- "strong": well-supported with meaningful functionality\n'
    '- "medium": supported but with notable limitations\n'
    '- "none": not supported or no evidence found\n\n'
    "Rules:\n"
    "- Each baseline feature item has sub_features — rate based on the "
    "overall capability represented by ALL sub_features combined\n"
    "- Base ALL ratings on the baseline data (which reflects the latest state)\n"
    "- Every product must appear in every FeatureComparison.ratings list\n"
    "- Product names must exactly match the baselines\n"
    "- category_name values must match EXACTLY as listed above WITHOUT "
    "numeric prefixes (e.g., use \"Core Tracing & Logging\" NOT "
    "\"1. Core Tracing & Logging\")\n"
    "- If a product has no changes this week, still rate it based on "
    "its baseline data"
)


# ---------------------------------------------------------------------------
# Prompt name constants (used as Weave object names)
# ---------------------------------------------------------------------------

PROMPT_NAMES = {
    "update_collector_backstory": UPDATE_COLLECTOR_BACKSTORY,
    "baseline_analyzer_backstory": BASELINE_ANALYZER_BACKSTORY,
    "report_writer_backstory": REPORT_WRITER_BACKSTORY,
    "update_collector_task": UPDATE_COLLECTOR_TASK,
    "baseline_analyzer_task": BASELINE_ANALYZER_TASK,
    "report_writer_task": REPORT_WRITER_TASK,
}


@dataclass
class PromptSet:
    """All prompts used by the 3-agent pipeline."""
    update_collector_backstory: str = UPDATE_COLLECTOR_BACKSTORY
    baseline_analyzer_backstory: str = BASELINE_ANALYZER_BACKSTORY
    report_writer_backstory: str = REPORT_WRITER_BACKSTORY
    update_collector_task: str = UPDATE_COLLECTOR_TASK
    baseline_analyzer_task: str = BASELINE_ANALYZER_TASK
    report_writer_task: str = REPORT_WRITER_TASK


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def publish_prompts() -> None:
    """Publish all default prompts to Weave for version tracking."""
    for name, text in PROMPT_NAMES.items():
        prompt = weave.StringPrompt(text)
        weave.publish(prompt, name=name)
        logger.info("Published prompt: %s", name)


def load_prompts() -> PromptSet:
    """Load prompts from Weave, falling back to code defaults."""
    ps = PromptSet()
    for name in PROMPT_NAMES:
        try:
            obj = weave.ref(name).get()
            value = obj.format() if hasattr(obj, "format") else str(obj)
            if value:
                setattr(ps, name, value)
                logger.debug("Loaded prompt from Weave: %s", name)
        except Exception:
            logger.debug("Using default prompt: %s", name)
    return ps
