"""crewAI agent factory functions for the 3-agent pipeline.

UpdateCollector (Perplexity Sonar) → BaselineAnalyzer (Gemini Pro) → ReportWriter (Gemini Pro)
"""

from __future__ import annotations

from crewai import Agent, LLM

from intel_bot.config import Settings
from intel_bot.prompts import PromptSet


def create_update_collector(settings: Settings, prompts: PromptSet) -> Agent:
    """UpdateCollector — Perplexity Sonar (web search built-in)."""
    llm = LLM(
        model=settings.perplexity_model,
        base_url="https://api.perplexity.ai",
        api_key=settings.perplexity_api_key.get_secret_value(),
        max_tokens=4096,
    )
    return Agent(
        role="Product Update Tracker",
        goal="Monitor changelogs and web sources to identify recent product updates",
        backstory=prompts.update_collector_backstory,
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_retry_limit=3,
        max_iter=15,
        cache=True,
    )


def create_baseline_analyzer(settings: Settings, prompts: PromptSet) -> Agent:
    """BaselineAnalyzer — Gemini Pro via OpenRouter."""
    llm = LLM(
        model=f"openrouter/{settings.openrouter_model}",
        api_key=settings.openrouter_api_key.get_secret_value(),
        max_tokens=16384,
    )
    return Agent(
        role="Baseline Update Analyst",
        goal="Compare updates against product baselines and produce precise changesets",
        backstory=prompts.baseline_analyzer_backstory,
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_retry_limit=3,
        max_iter=15,
        cache=True,
    )


def create_report_writer(settings: Settings, prompts: PromptSet) -> Agent:
    """ReportWriter — Gemini Pro via OpenRouter."""
    llm = LLM(
        model=f"openrouter/{settings.openrouter_model}",
        api_key=settings.openrouter_api_key.get_secret_value(),
        max_tokens=16384,
    )
    return Agent(
        role="Senior Market Research Analyst",
        goal="Produce feature comparison ratings and commentary highlighting this week's changes",
        backstory=prompts.report_writer_backstory,
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_retry_limit=3,
        max_iter=15,
        cache=True,
    )
