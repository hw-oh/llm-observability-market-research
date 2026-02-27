#!/usr/bin/env python3
"""Standalone baseline data generator.

Comprehensively researches each product's documentation and generates
structured ProductBaseline JSON files under data/{product}.json.

This is intentionally separate from the intel_bot analysis pipeline —
baseline generation requires deep, thorough documentation reading,
while the weekly analysis focuses on tracking incremental changes.

Usage:
    python scripts/generate_baseline.py                      # all 6 products
    python scripts/generate_baseline.py --product Langfuse   # single product
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from intel_bot.config import (
    COMPARISON_CATEGORIES,
    CompetitorConfig,
    Settings,
    get_all_products,
)
from intel_bot.models import ProductBaseline
from intel_bot.storage import save_baseline

logger = logging.getLogger(__name__)
console = Console()

# ---------------------------------------------------------------------------
# Scraping
# ---------------------------------------------------------------------------

_SCRAPE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
_MAX_CHARS_PER_URL = 8_000
_MAX_CHARS_TOTAL = 30_000
_MIN_CONTENT_LENGTH = 500

_DATE_RE = re.compile(
    r"(January|February|March|April|May|June|July|August|September"
    r"|October|November|December)\s+\d{1,2},\s+\d{4}"
)
_ENTRY_SEPARATOR = "Thanks for your feedback"
_MAX_SCROLLS = 10
_SCROLL_WAIT_MS = 1500


def _parse_oldest_date(text: str) -> datetime | None:
    matches = _DATE_RE.findall(text)
    if not matches:
        return None
    dates: list[datetime] = []
    for m in _DATE_RE.finditer(text):
        try:
            dates.append(datetime.strptime(m.group(), "%B %d, %Y"))
        except ValueError:
            continue
    return min(dates) if dates else None


def _filter_entries_by_tags(text: str, include_tags: list[str]) -> str:
    if not include_tags:
        return text
    entries = text.split(_ENTRY_SEPARATOR)
    upper_tags = {t.upper() for t in include_tags}
    kept: list[str] = []
    for entry in entries:
        lines = [ln.strip() for ln in entry.strip().splitlines() if ln.strip()]
        entry_tags = {ln for ln in lines if ln.isupper() and len(ln) < 30}
        if entry_tags & upper_tags:
            kept.append(entry.strip())
    return ("\n" + _ENTRY_SEPARATOR + "\n").join(kept)


def _scrape_with_playwright(
    url: str,
    timeout_ms: int = 30_000,
    scroll_for_days: int = 10,
    include_tags: list[str] | None = None,
) -> str:
    """Scrape a JS-rendered page using Playwright headless Chromium."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.warning("playwright not installed — cannot scrape JS page: %s", url)
        return ""

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            page.wait_for_timeout(2000)

            cutoff = datetime.now() - timedelta(days=scroll_for_days)

            for _ in range(_MAX_SCROLLS):
                text = page.inner_text("body")
                oldest = _parse_oldest_date(text)
                if oldest and oldest <= cutoff:
                    break
                prev_len = len(text)
                page.evaluate(
                    "() => { const c = document.querySelector('.container');"
                    " if (c) c.scrollTop = c.scrollHeight; }"
                )
                page.wait_for_timeout(_SCROLL_WAIT_MS)
                if len(page.inner_text("body")) == prev_len:
                    break

            text = page.inner_text("body")
            browser.close()

        text = "\n".join(ln for ln in text.splitlines() if ln.strip())

        if include_tags:
            text = _filter_entries_by_tags(text, include_tags)

        return text
    except Exception as exc:
        logger.warning("Playwright scrape failed for %s: %s", url, exc)
        return ""


def _scrape_urls(urls: list[str], include_tags: list[str] | None = None) -> str:
    if not urls:
        return ""
    chunks: list[str] = []
    total = 0
    for url in urls:
        if total >= _MAX_CHARS_TOTAL:
            break
        try:
            resp = requests.get(url, timeout=15, headers=_SCRAPE_HEADERS)
            resp.encoding = resp.apparent_encoding
            text = BeautifulSoup(resp.text, "html.parser").get_text(separator="\n")
            text = "\n".join(ln for ln in text.splitlines() if ln.strip())

            if len(text.strip()) < _MIN_CONTENT_LENGTH:
                logger.info("Static scrape too short for %s (%d chars), trying Playwright", url, len(text))
                pw_text = _scrape_with_playwright(url, include_tags=include_tags)
                if pw_text:
                    text = pw_text

            if len(text) > _MAX_CHARS_PER_URL:
                text = text[:_MAX_CHARS_PER_URL] + "\n…(truncated)"
            chunks.append(f"=== {url} ===\n{text}")
            total += len(text)
        except Exception as exc:
            logger.warning("Failed to scrape %s: %s", url, exc)
            chunks.append(f"=== {url} ===\n(scrape failed: {exc})")
    return "\n\n".join(chunks)


# ---------------------------------------------------------------------------
# Category description builder
# ---------------------------------------------------------------------------

def _build_categories_description() -> str:
    lines: list[str] = []
    for i, cat in enumerate(COMPARISON_CATEGORIES, 1):
        lines.append(f"\n{i}. {cat.name}:")
        for item_name, item_desc in cat.items:
            lines.append(f"   - {item_name}: {item_desc}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Prompts (self-contained — not shared with intel_bot)
# ---------------------------------------------------------------------------

SEARCH_AGENT_BACKSTORY = (
    "You are a market research specialist covering the LLM observability "
    "and evaluation space. You use web search to find up-to-date, factual "
    "information about product features, pricing, and enterprise capabilities."
)

EXTRACTION_AGENT_BACKSTORY = (
    "You are a senior competitive intelligence analyst who combines web "
    "search findings and documentation evidence into precise, structured "
    "analysis output. When sources conflict, you prefer official documentation "
    "over search results. Include only facts found in the evidence."
)

SEARCH_TASK_PROMPT = (
    "Research {product_name} COMPREHENSIVELY for the LLM observability and evaluation market.\n\n"
    "For each category and feature item below, search the web for DETAILED current capabilities:\n"
    "{categories_desc}\n\n"
    "{product_desc}\n\n"
    "For EVERY item, find:\n"
    "1. Whether the product supports it (yes / no / partial)\n"
    "2. What the product CALLS this feature (the product's own feature name)\n"
    "3. HOW it is provided (SDK, UI, API, CLI, etc.)\n"
    "4. Any relevant details, limitations, or recent changes\n\n"
    "Be thorough — this data will serve as a long-lived baseline reference."
)

EXTRACTION_TASK_PROMPT = (
    "Combine the search evidence and documentation into a structured "
    "ProductBaseline for {product_name}.\n"
    "{url_context}\n\n"
    "Rules:\n"
    "- When search and documentation evidence conflict, prefer documentation evidence\n"
    "- categories must contain exactly {num_categories} entries matching these names:\n"
    "{categories_desc}\n"
    "- Each category must list ALL feature items with these fields:\n"
    '  - item_name: the standardized name (MUST match exactly as listed above)\n'
    '  - available: "yes" (fully supported), "no" (not supported), '
    'or "partial" (exists but with notable limitations)\n'
    '  - sub_features: a list of concrete capabilities the product offers '
    'for this item. Each sub_feature has:\n'
    '    - name: the product\'s OWN name for this capability '
    '(e.g., "@weave.op()", "LangSmith Runs", "Langfuse Traces")\n'
    '    - provision_method: HOW the feature is provided '
    '(e.g., "SDK decorator", "Built-in UI", "REST API", "Auto-instrumentation")\n'
    '    - notes: additional context, limitations, or details. '
    'Keep concise but informative.\n'
    '  - If the item is not supported, set available to "no" and '
    'sub_features to an empty list []\n'
    '  - If the product supports the item through MULTIPLE distinct '
    'features/tools, list each as a separate sub_feature\n'
    '  - Example: for "MCP Integration" with available="yes":\n'
    '    sub_features: [\n'
    '      {{"name": "MCP Server", "provision_method": "npm package", '
    '"notes": "Core MCP server for log querying"}},\n'
    '      {{"name": "Cursor Extension", "provision_method": "IDE Extension", '
    '"notes": "Auto-configures MCP server in Cursor"}}\n'
    '    ]\n\n'
    '- product_name must be exactly "{product_name}"\n'
    "- last_updated must be {date}"
)


# ---------------------------------------------------------------------------
# Agent factories
# ---------------------------------------------------------------------------

def _create_search_agent(settings: Settings) -> Agent:
    llm = LLM(
        model=settings.perplexity_model,
        base_url="https://api.perplexity.ai",
        api_key=settings.perplexity_api_key.get_secret_value(),
    )
    return Agent(
        role="LLM Observability Product Researcher",
        goal="Research product capabilities using web search and return factual evidence",
        backstory=SEARCH_AGENT_BACKSTORY,
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_retry_limit=3,
        max_iter=15,
        cache=True,
    )


def _create_extraction_agent(settings: Settings) -> Agent:
    llm = LLM(
        model=f"openrouter/{settings.openrouter_model}",
        api_key=settings.openrouter_api_key.get_secret_value(),
    )
    return Agent(
        role="Competitive Intelligence Analyst",
        goal="Merge evidence into a structured ProductBaseline with feature names, availability, and provision methods",
        backstory=EXTRACTION_AGENT_BACKSTORY,
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_retry_limit=3,
        max_iter=15,
        cache=True,
    )


# ---------------------------------------------------------------------------
# Baseline generation
# ---------------------------------------------------------------------------

def generate_baseline(
    config: CompetitorConfig,
    settings: Settings,
) -> ProductBaseline:
    """Run SearchAgent + scraping -> ExtractionAgent -> ProductBaseline for one product."""
    search_agent = _create_search_agent(settings)
    extraction_agent = _create_extraction_agent(settings)

    categories_desc = _build_categories_description()
    num_categories = len(COMPARISON_CATEGORIES)

    product_desc = ""
    if config.product_description:
        product_desc = f"Product context: {config.product_description}"

    scraped_content = _scrape_urls(config.reference_urls)
    product_ctx = config.product_context or ""
    url_context = ""
    if scraped_content:
        url_context = (
            f"\n\n=== Official Documentation (scraped) ===\n"
            f"{scraped_content}\n=== End Documentation ==="
        )
    if product_ctx:
        url_context += (
            f"\n\n=== Internal Product Context ===\n"
            f"{product_ctx}\n=== End Internal Context ==="
        )

    search_task = Task(
        description=SEARCH_TASK_PROMPT.format(
            product_name=config.name,
            categories_desc=categories_desc,
            product_desc=product_desc,
        ),
        expected_output=(
            f"A comprehensive research report on {config.name} covering all "
            f"{num_categories} categories "
            f"({sum(len(c.items) for c in COMPARISON_CATEGORIES)} items total) "
            f"with feature names, availability, provision methods, and source URLs."
        ),
        agent=search_agent,
    )

    extraction_task = Task(
        description=EXTRACTION_TASK_PROMPT.format(
            product_name=config.name,
            date=date.today().isoformat(),
            num_categories=num_categories,
            categories_desc=categories_desc,
            url_context=url_context,
        ),
        expected_output=(
            f"A complete ProductBaseline for {config.name} with all "
            f"{num_categories} categories, each containing all feature items "
            f"with available status and sub_features list (name, provision_method, notes)."
        ),
        agent=extraction_agent,
        context=[search_task],
        output_pydantic=ProductBaseline,
    )

    crew = Crew(
        agents=[search_agent, extraction_agent],
        tasks=[search_task, extraction_task],
        process=Process.sequential,
        verbose=False,
        cache=True,
    )

    result = crew.kickoff()
    if result.pydantic:
        return result.pydantic
    raise ValueError(
        f"ExtractionAgent failed to produce structured ProductBaseline for {config.name}"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate baseline data for LLM observability products")
    parser.add_argument("--product", type=str, default=None, help="Generate for a specific product only")
    args = parser.parse_args()

    settings = Settings()
    all_configs = get_all_products()

    if args.product:
        all_configs = [
            c for c in all_configs
            if c.name.lower() == args.product.lower()
        ]
        if not all_configs:
            console.print(f"[red]Unknown product: {args.product}")
            console.print("Available: " + ", ".join(c.name for c in get_all_products()))
            sys.exit(1)
        console.print(f"베이스라인 생성 시작: {args.product}")
    else:
        console.print("전체 제품 베이스라인 생성 시작...")

    console.print()

    tasks: dict[str, int] = {}
    baselines: list[ProductBaseline] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for config in all_configs:
            task_id = progress.add_task(f"{config.name} 베이스라인 생성 중...", total=None)
            tasks[config.name] = task_id

            bl = generate_baseline(config, settings)
            path = save_baseline(bl)
            baselines.append(bl)

            progress.update(task_id, description=f"[green]  {config.name}: 완료 → {path}")
            progress.remove_task(task_id)

    console.print()
    console.print(f"[bold green]베이스라인 생성 완료: {len(baselines)}개 제품")
    for bl in baselines:
        n_items = sum(len(c.features) for c in bl.categories)
        n_subs = sum(len(f.sub_features) for c in bl.categories for f in c.features)
        console.print(f"  {bl.product_name}: {n_items}개 항목, {n_subs}개 sub_features")


if __name__ == "__main__":
    main()
