from __future__ import annotations

import asyncio
import sys
from datetime import date

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from intel_bot.analyzer import analyze_all
from intel_bot.collectors.docs_scraper import scrape_competitor_docs
from intel_bot.collectors.feed import fetch_competitor_feeds
from intel_bot.collectors.serper import search_competitor
from intel_bot.config import COMPETITORS, Settings
from intel_bot.discovery import discover
from intel_bot.models import CollectionRun, CompetitorData
from intel_bot.notify import send_slack_notification
from intel_bot.report import save_report, update_index
from intel_bot.storage import (
    load_latest_analysis,
    load_latest_collection,
    load_latest_discovery,
    load_previous_analysis,
    save_analysis,
    save_collection,
    save_discovery,
)

console = Console()


async def _collect() -> None:
    settings = Settings()
    today = date.today().isoformat()

    all_competitors: list[CompetitorData] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for comp in COMPETITORS:
            task = progress.add_task(f"Collecting {comp.name}...", total=None)

            # Serper search
            search_results = await search_competitor(comp, settings.serper_dev_api)
            progress.update(task, description=f"  {comp.name}: {len(search_results)} search results")

            # Docs scraping
            docs_pages = await scrape_competitor_docs(comp)
            progress.update(task, description=f"  {comp.name}: {len(docs_pages)} docs pages")

            # Feed collection
            feed_entries = fetch_competitor_feeds(comp)
            progress.update(task, description=f"  {comp.name}: {len(feed_entries)} feed entries")

            all_competitors.append(
                CompetitorData(
                    competitor_name=comp.name,
                    search_results=search_results,
                    docs_pages=docs_pages,
                    feed_entries=feed_entries,
                )
            )

            progress.update(task, description=f"[green]  {comp.name}: done")
            progress.remove_task(task)

    run = CollectionRun(date=today, mode="initial", competitors=all_competitors)
    path = save_collection(run)

    console.print()
    console.print(f"[bold green]Collection saved to {path}")
    console.print()
    for comp_data in all_competitors:
        console.print(
            f"  {comp_data.competitor_name}: "
            f"{len(comp_data.search_results)} searches, "
            f"{len(comp_data.docs_pages)} docs, "
            f"{len(comp_data.feed_entries)} feeds"
        )


def collect() -> None:
    asyncio.run(_collect())


async def _discover_and_save() -> None:
    settings = Settings()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Discovering emerging competitors...", total=None)
        result = await discover(settings)
        progress.update(task, description="[green]Discovery done")
        progress.remove_task(task)

    path = save_discovery(result)

    console.print()
    console.print(f"[bold green]Discovery saved to {path}")
    console.print(f"  Queries: {len(result.queries)}")
    console.print(f"  Search results: {result.search_results_count}")
    console.print(f"  Emerging competitors: {len(result.emerging_competitors)}")
    for ec in result.emerging_competitors:
        console.print(f"    - {ec.name}: {ec.description}")


def discover_cmd() -> None:
    asyncio.run(_discover_and_save())


def analyze() -> None:
    settings = Settings()
    collection = load_latest_collection()
    if collection is None:
        console.print("[red]No collection data found. Run 'collect' first.")
        sys.exit(1)

    console.print(f"Analyzing collection from {collection.date} ({len(collection.competitors)} competitors)")
    console.print()

    tasks: dict[str, int] = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        def on_progress(name: str, status: str) -> None:
            if status == "analyzing":
                tasks[name] = progress.add_task(f"Analyzing {name}...", total=None)
            elif status == "done" and name in tasks:
                progress.update(tasks[name], description=f"[green]  {name}: done")
                progress.remove_task(tasks[name])

        run = analyze_all(collection, settings, on_progress=on_progress)

    path = save_analysis(run)

    console.print()
    console.print(f"[bold green]Analysis saved to {path}")
    console.print()
    for comp in run.competitors:
        stronger = sum(1 for a in comp.axes if a.weave_comparison == "stronger")
        weaker = sum(1 for a in comp.axes if a.weave_comparison == "weaker")
        comparable = sum(1 for a in comp.axes if a.weave_comparison == "comparable")
        console.print(
            f"  {comp.competitor_name}: "
            f"[red]{stronger} stronger[/red], "
            f"[yellow]{comparable} comparable[/yellow], "
            f"[green]{weaker} weaker[/green]"
        )


def report() -> None:
    analysis = load_latest_analysis()
    if analysis is None:
        console.print("[red]No analysis data found. Run 'analyze' first.")
        sys.exit(1)

    discovery_result = load_latest_discovery()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating report...", total=None)
        path = save_report(analysis, discovery=discovery_result)
        progress.update(task, description="Updating index...")
        update_index()
        progress.update(task, description="[green]Done")
        progress.remove_task(task)

    console.print()
    console.print(f"[bold green]Report saved to {path}")
    console.print(f"  Competitors: {len(analysis.competitors)}")
    console.print(f"  Axes: {len(analysis.competitors[0].axes) if analysis.competitors else 0}")
    console.print(f"  Index updated: index.md")
    if discovery_result and discovery_result.emerging_competitors:
        console.print(f"  Emerging competitors: {len(discovery_result.emerging_competitors)}")


def run() -> None:
    collect()

    # Discovery (failure does not block pipeline)
    discovery_result = None
    try:
        asyncio.run(_discover_and_save())
        discovery_result = load_latest_discovery()
    except Exception as exc:
        console.print(f"[yellow]Discovery failed (non-blocking): {exc}")

    analyze()

    analysis = load_latest_analysis()
    previous = load_previous_analysis()

    if discovery_result is None:
        discovery_result = load_latest_discovery()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating report...", total=None)
        path = save_report(analysis, previous, discovery_result)
        progress.update(task, description="Updating index...")
        update_index()
        progress.update(task, description="[green]Done")
        progress.remove_task(task)

    console.print()
    console.print(f"[bold green]Report saved to {path}")
    if previous:
        console.print(f"  Diff included (vs {previous.date})")
    if discovery_result and discovery_result.emerging_competitors:
        console.print(f"  Emerging competitors: {len(discovery_result.emerging_competitors)}")

    settings = Settings()
    if settings.slack_webhook_url:
        try:
            send_slack_notification(settings.slack_webhook_url, analysis, path)
        except Exception as exc:
            console.print(f"[yellow]Slack notification failed: {exc}")


def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] == "collect":
        collect()
    elif args[0] == "analyze":
        analyze()
    elif args[0] == "report":
        report()
    elif args[0] == "discover":
        discover_cmd()
    elif args[0] == "run":
        run()
    else:
        console.print(f"[red]Unknown command: {args[0]}")
        console.print("Usage: python -m intel_bot [collect|analyze|report|discover|run]")
        sys.exit(1)
