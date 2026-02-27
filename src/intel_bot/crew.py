"""crewAI-based 3-agent analysis pipeline.

Per product (parallel):  Step 1 — changelog scraping + UpdateCollector → ProductUpdates
Per product (parallel):  Step 2 — BaselineAnalyzer + baseline → ProductChangeset (+ save)
All products:            Step 3 — ReportWriter → ReportSynthesis
"""

from __future__ import annotations

import contextvars
import json
import logging
import re
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta

import requests
import weave
from bs4 import BeautifulSoup
from crewai import Crew, Process, Task

from intel_bot.agents import (
    create_baseline_analyzer,
    create_report_writer,
    create_update_collector,
)
from intel_bot.config import COMPARISON_CATEGORIES, CompetitorConfig, Settings, get_active_products
from intel_bot.models import (
    AnalysisRun,
    ProductBaseline,
    ProductChangeset,
    ProductUpdates,
    ReportSynthesis,
)
from intel_bot.prompts import PromptSet, load_prompts
from intel_bot.storage import load_baseline, save_baseline

logger = logging.getLogger(__name__)


_SCRAPE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
_MAX_CHARS_PER_URL = 8_000
_MAX_CHARS_TOTAL = 30_000
_MIN_CONTENT_LENGTH = 500


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_categories_description() -> str:
    lines: list[str] = []
    for i, cat in enumerate(COMPARISON_CATEGORIES, 1):
        lines.append(f"\n{i}. {cat.name}:")
        for item_name, item_desc in cat.items:
            lines.append(f"   - {item_name}: {item_desc}")
    return "\n".join(lines)


def _build_baseline_summary(baseline: ProductBaseline | None) -> str:
    """Build a compact summary of known features for the UpdateCollector."""
    if not baseline or not baseline.categories:
        return "(No baseline available)"
    lines: list[str] = []
    for cat in baseline.categories:
        for feat in cat.features:
            subs = ", ".join(sf.name for sf in feat.sub_features) if feat.sub_features else "N/A"
            lines.append(f"- {feat.item_name} [{feat.available}]: {subs}")
    return "\n".join(lines)


_DATE_RE = re.compile(
    r"(January|February|March|April|May|June|July|August|September"
    r"|October|November|December)\s+\d{1,2},\s+\d{4}"
)
_ENTRY_SEPARATOR = "Thanks for your feedback"
_MAX_SCROLLS = 10
_SCROLL_WAIT_MS = 1500


def _parse_oldest_date(text: str) -> datetime | None:
    """Extract the oldest date found in text (English month format)."""
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
    """Split text by entry separator and keep only entries matching tags."""
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
    """Scrape a JS-rendered page using Playwright headless Chromium.

    Scrolls `.container` until entries older than `scroll_for_days` are loaded,
    then optionally filters entries by category tags.
    """
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


@weave.op()
def _scrape_urls(
    urls: list[str],
    include_tags: list[str] | None = None,
) -> str:
    """Scrape URLs directly — no LLM reasoning needed.

    Falls back to Playwright for JS-rendered pages when the initial
    requests+BeautifulSoup result is too short. ``include_tags`` is
    forwarded to the Playwright scraper for entry-level filtering.
    """
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
# Step 1: Collect updates
# ---------------------------------------------------------------------------

@weave.op(call_display_name=lambda call: f"collect_updates({call.inputs['config'].name})")
def collect_updates(
    config: CompetitorConfig,
    settings: Settings,
    prompts: PromptSet,
    baseline: ProductBaseline | None = None,
) -> ProductUpdates:
    """Scrape changelog + UpdateCollector Agent → ProductUpdates."""
    collector = create_update_collector(settings, prompts)

    changelog_urls = []
    if config.changelog_url:
        changelog_urls.append(config.changelog_url)
    changelog_content = _scrape_urls(
        changelog_urls,
        include_tags=config.changelog_include_tags or None,
    ) or "(No changelog content available)"

    product_desc = ""
    if config.product_description:
        product_desc = f"Product context: {config.product_description}"

    filter_hint = ""
    if config.changelog_filter_hint:
        filter_hint = f"IMPORTANT — Changelog Filtering:\n{config.changelog_filter_hint}"

    baseline_summary = _build_baseline_summary(baseline)

    task = Task(
        description=prompts.update_collector_task.format(
            product_name=config.name,
            changelog_content=changelog_content,
            product_desc=product_desc,
            changelog_filter_hint=filter_hint,
            baseline_summary=baseline_summary,
            date=date.today().isoformat(),
        ),
        expected_output=(
            f"A ProductUpdates result for {config.name} with a list of "
            f"recent updates (title, date, summary for each)."
        ),
        agent=collector,
        output_pydantic=ProductUpdates,
    )

    crew = Crew(
        agents=[collector],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
        cache=True,
    )

    result = crew.kickoff()
    if result.pydantic:
        return result.pydantic
    raise ValueError(f"UpdateCollector failed for {config.name}")


# ---------------------------------------------------------------------------
# Step 2: Analyze baseline
# ---------------------------------------------------------------------------

@weave.op(call_display_name=lambda call: f"analyze_baseline({call.inputs['config'].name})")
def analyze_baseline(
    config: CompetitorConfig,
    settings: Settings,
    prompts: PromptSet,
    updates: ProductUpdates,
    baseline: ProductBaseline,
) -> ProductChangeset:
    """BaselineAnalyzer Agent → ProductChangeset (updated baseline + changes)."""
    analyzer = create_baseline_analyzer(settings, prompts)

    categories_desc = _build_categories_description()
    num_categories = len(COMPARISON_CATEGORIES)

    updates_json = json.dumps(updates.model_dump(), ensure_ascii=False, indent=2)
    baseline_json = json.dumps(baseline.model_dump(), ensure_ascii=False, indent=2)

    product_ctx = config.product_context or ""
    url_context = ""
    if product_ctx:
        url_context = f"\n=== Internal Product Context ===\n{product_ctx}\n=== End Internal Context ==="

    task = Task(
        description=prompts.baseline_analyzer_task.format(
            product_name=config.name,
            updates_json=updates_json,
            baseline_date=baseline.last_updated,
            baseline_json=baseline_json,
            url_context=url_context,
            num_categories=num_categories,
            categories_desc=categories_desc,
            date=date.today().isoformat(),
        ),
        expected_output=(
            f"A ProductChangeset for {config.name} with a list of changes "
            f"(before/after for each changed field) and a complete "
            f"updated_baseline with all {num_categories} categories."
        ),
        agent=analyzer,
        output_pydantic=ProductChangeset,
    )

    crew = Crew(
        agents=[analyzer],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
        cache=True,
    )

    result = crew.kickoff()
    if result.pydantic:
        return result.pydantic
    raise ValueError(f"BaselineAnalyzer failed for {config.name}")


# ---------------------------------------------------------------------------
# Step 3: Write report
# ---------------------------------------------------------------------------

@weave.op(call_display_name=lambda call: f"write_report({len(call.inputs['baselines'])} products)")
def write_report(
    changesets: list[ProductChangeset],
    baselines: list[ProductBaseline],
    settings: Settings,
    prompts: PromptSet,
) -> ReportSynthesis:
    """ReportWriter Agent → ReportSynthesis (ratings + AI comment with highlights)."""
    writer = create_report_writer(settings, prompts)

    categories_desc = _build_categories_description()
    num_categories = len(COMPARISON_CATEGORIES)

    all_changesets_json = json.dumps(
        [cs.model_dump(exclude={"updated_baseline"}) for cs in changesets],
        ensure_ascii=False,
        indent=2,
    )
    all_baselines_json = json.dumps(
        [bl.model_dump() for bl in baselines],
        ensure_ascii=False,
        indent=2,
    )

    task = Task(
        description=prompts.report_writer_task.format(
            all_changesets_json=all_changesets_json,
            all_baselines_json=all_baselines_json,
            num_categories=num_categories,
            categories_desc=categories_desc,
        ),
        expected_output=(
            "A complete ReportSynthesis with ai_comment (an AIComment with "
            "product_highlights for each product and a market_trend sentence) "
            f"and categories ({num_categories} entries, each with rated "
            "features for all products)."
        ),
        agent=writer,
        output_pydantic=ReportSynthesis,
    )

    crew = Crew(
        agents=[writer],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    if result.pydantic:
        return result.pydantic
    raise ValueError("ReportWriter failed to produce ReportSynthesis")


# ---------------------------------------------------------------------------
# Per-product pipeline (parallelizable unit)
# ---------------------------------------------------------------------------

def _process_product(
    config: CompetitorConfig,
    settings: Settings,
    prompts: PromptSet,
    on_progress: Callable[[str, str], None] | None = None,
) -> tuple[ProductUpdates | None, ProductChangeset | None, ProductBaseline | None]:
    """Run Step 1 + Step 2 for a single product. Thread-safe."""
    try:
        baseline = load_baseline(config.name)

        if on_progress:
            on_progress(config.name, "collecting updates")

        updates = collect_updates(config, settings, prompts, baseline=baseline)

        if on_progress:
            on_progress(config.name, "analyzing baseline")

        if baseline is None:
            logger.warning("No baseline found for %s — skipping baseline analysis", config.name)
            empty_bl = ProductBaseline(product_name=config.name, last_updated="", categories=[])
            if on_progress:
                on_progress(config.name, "done (no baseline)")
            return updates, None, empty_bl

        changeset = analyze_baseline(config, settings, prompts, updates, baseline)
        save_baseline(changeset.updated_baseline)

        if on_progress:
            on_progress(config.name, "done")
        return updates, changeset, changeset.updated_baseline

    except Exception as exc:
        logger.error("Pipeline failed for %s: %s", config.name, exc)
        if on_progress:
            on_progress(config.name, f"failed: {exc}")
        bl = load_baseline(config.name)
        return None, None, bl


# ---------------------------------------------------------------------------
# Top-level orchestrator (public API)
# ---------------------------------------------------------------------------

@weave.op()
def analyze_all(
    settings: Settings,
    on_progress: Callable[[str, str], None] | None = None,
) -> AnalysisRun:
    """Run the full 3-agent pipeline.

    Step 1+2: Per-product UpdateCollector + BaselineAnalyzer (parallel)
    Step 3:   ReportWriter across all products → ReportSynthesis
    """
    prompts = load_prompts()

    run = AnalysisRun(
        date=date.today().isoformat(),
        model=settings.openrouter_model,
    )

    all_configs = get_active_products()
    all_baselines: list[ProductBaseline] = []

    with ThreadPoolExecutor(max_workers=len(all_configs)) as executor:
        futures = {}
        for config in all_configs:
            ctx = contextvars.copy_context()
            futures[executor.submit(ctx.run, _process_product, config, settings, prompts, on_progress)] = config

        for future in as_completed(futures):
            config = futures[future]
            try:
                updates, changeset, bl = future.result()
            except Exception as exc:
                logger.error("Unexpected error for %s: %s", config.name, exc)
                if on_progress:
                    on_progress(config.name, f"failed: {exc}")
                bl = load_baseline(config.name)
                updates, changeset = None, None

            if updates:
                run.updates.append(updates)
            if changeset:
                run.changesets.append(changeset)
            if bl:
                all_baselines.append(bl)

    # Step 3: Write report
    if on_progress:
        on_progress("레포트 작성", "analyzing")

    run.synthesis = write_report(run.changesets, all_baselines, settings, prompts)

    if on_progress:
        on_progress("레포트 작성", "done")

    return run
