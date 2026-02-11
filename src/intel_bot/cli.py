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
            task = progress.add_task(f"{comp.name} 수집 중...", total=None)

            # Serper search
            search_results = await search_competitor(comp, settings.serper_dev_api)
            progress.update(task, description=f"  {comp.name}: 검색 결과 {len(search_results)}건")

            # Docs scraping
            docs_pages = await scrape_competitor_docs(comp)
            progress.update(task, description=f"  {comp.name}: 문서 {len(docs_pages)}건")

            # Feed collection
            feed_entries = fetch_competitor_feeds(comp)
            progress.update(task, description=f"  {comp.name}: 피드 {len(feed_entries)}건")

            all_competitors.append(
                CompetitorData(
                    competitor_name=comp.name,
                    search_results=search_results,
                    docs_pages=docs_pages,
                    feed_entries=feed_entries,
                )
            )

            progress.update(task, description=f"[green]  {comp.name}: 완료")
            progress.remove_task(task)

    run = CollectionRun(date=today, mode="initial", competitors=all_competitors)
    path = save_collection(run)

    console.print()
    console.print(f"[bold green]수집 완료: {path}")
    console.print()
    for comp_data in all_competitors:
        console.print(
            f"  {comp_data.competitor_name}: "
            f"검색 {len(comp_data.search_results)}건, "
            f"문서 {len(comp_data.docs_pages)}건, "
            f"피드 {len(comp_data.feed_entries)}건"
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
        task = progress.add_task("신규 경쟁사 탐색 중...", total=None)
        result = await discover(settings)
        progress.update(task, description="[green]탐색 완료")
        progress.remove_task(task)

    path = save_discovery(result)

    console.print()
    console.print(f"[bold green]탐색 결과 저장: {path}")
    console.print(f"  쿼리: {len(result.queries)}개")
    console.print(f"  검색 결과: {result.search_results_count}건")
    console.print(f"  신규 경쟁사: {len(result.emerging_competitors)}개")
    for ec in result.emerging_competitors:
        console.print(f"    - {ec.name}: {ec.description}")


def discover_cmd() -> None:
    asyncio.run(_discover_and_save())


def analyze() -> None:
    settings = Settings()
    collection = load_latest_collection()
    if collection is None:
        console.print("[red]수집 데이터가 없습니다. 먼저 'collect'를 실행하세요.")
        sys.exit(1)

    console.print(f"{collection.date} 수집 데이터 분석 중 (경쟁사 {len(collection.competitors)}개)")
    console.print()

    tasks: dict[str, int] = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        def on_progress(name: str, status: str) -> None:
            if status == "analyzing":
                tasks[name] = progress.add_task(f"{name} 분석 중...", total=None)
            elif status == "done" and name in tasks:
                progress.update(tasks[name], description=f"[green]  {name}: 완료")
                progress.remove_task(tasks[name])

        run = analyze_all(collection, settings, on_progress=on_progress)

    path = save_analysis(run)

    console.print()
    console.print(f"[bold green]분석 완료: {path}")
    console.print()
    for comp in run.competitors:
        stronger = sum(1 for a in comp.axes if a.weave_comparison == "stronger")
        weaker = sum(1 for a in comp.axes if a.weave_comparison == "weaker")
        comparable = sum(1 for a in comp.axes if a.weave_comparison == "comparable")
        console.print(
            f"  {comp.competitor_name}: "
            f"[red]경쟁사 우위 {stronger}[/red], "
            f"[yellow]유사 {comparable}[/yellow], "
            f"[green]Weave 우위 {weaker}[/green]"
        )


def report() -> None:
    analysis = load_latest_analysis()
    if analysis is None:
        console.print("[red]분석 데이터가 없습니다. 먼저 'analyze'를 실행하세요.")
        sys.exit(1)

    discovery_result = load_latest_discovery()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("리포트 생성 중...", total=None)
        path = save_report(analysis, discovery=discovery_result)
        progress.update(task, description="인덱스 업데이트 중...")
        update_index()
        progress.update(task, description="[green]완료")
        progress.remove_task(task)

    console.print()
    console.print(f"[bold green]리포트 저장: {path}")
    console.print(f"  경쟁사: {len(analysis.competitors)}개")
    console.print(f"  비교 축: {len(analysis.competitors[0].axes) if analysis.competitors else 0}개")
    console.print(f"  인덱스 업데이트: index.md")
    if discovery_result and discovery_result.emerging_competitors:
        console.print(f"  신규 경쟁사: {len(discovery_result.emerging_competitors)}개")


def run() -> None:
    collect()

    # Discovery (failure does not block pipeline)
    discovery_result = None
    try:
        asyncio.run(_discover_and_save())
        discovery_result = load_latest_discovery()
    except Exception as exc:
        console.print(f"[yellow]탐색 실패 (비차단): {exc}")

    analyze()

    analysis = load_latest_analysis()

    if discovery_result is None:
        discovery_result = load_latest_discovery()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("리포트 생성 중...", total=None)
        path = save_report(analysis, discovery_result)
        progress.update(task, description="인덱스 업데이트 중...")
        update_index()
        progress.update(task, description="[green]완료")
        progress.remove_task(task)

    console.print()
    console.print(f"[bold green]리포트 저장: {path}")
    if discovery_result and discovery_result.emerging_competitors:
        console.print(f"  신규 경쟁사: {len(discovery_result.emerging_competitors)}개")

    settings = Settings()
    if settings.slack_webhook_url:
        try:
            send_slack_notification(settings.slack_webhook_url, analysis, path)
        except Exception as exc:
            console.print(f"[yellow]Slack 알림 실패: {exc}")


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
        console.print(f"[red]알 수 없는 명령: {args[0]}")
        console.print("사용법: python -m intel_bot [collect|analyze|report|discover|run]")
        sys.exit(1)
