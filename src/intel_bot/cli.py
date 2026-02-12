from __future__ import annotations

import asyncio
import sys
from datetime import date
from pathlib import Path

import os

import weave
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from intel_bot.analyzer import analyze_all
from intel_bot.collectors.docs_scraper import scrape_competitor_docs
from intel_bot.collectors.feed import fetch_competitor_feeds
from intel_bot.collectors.serper import search_competitor
from intel_bot.collectors.beamer import fetch_beamer_changelog
from intel_bot.config import BEAMER_APP_ID, COMPETITORS, WEAVE_CONFIG, Settings
from intel_bot.discovery import discover
from intel_bot.models import CollectionRun, CompetitorData
from intel_bot.notify import send_slack_notification
from intel_bot.report import generate_weekly_report, save_report, update_index
from intel_bot.translator import translate_content
from intel_bot.translator import translate_all_reports
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

        # Weave 자체 데이터 수집 (경쟁사와 동일한 파이프라인 + Beamer changelog)
        task = progress.add_task(f"{WEAVE_CONFIG.name} 수집 중...", total=None)
        search_results = await search_competitor(WEAVE_CONFIG, settings.serper_dev_api)
        progress.update(task, description=f"  {WEAVE_CONFIG.name}: 검색 결과 {len(search_results)}건")
        docs_pages = await scrape_competitor_docs(WEAVE_CONFIG)
        progress.update(task, description=f"  {WEAVE_CONFIG.name}: 문서 {len(docs_pages)}건")
        feed_entries = fetch_competitor_feeds(WEAVE_CONFIG)
        beamer_entries = await fetch_beamer_changelog(BEAMER_APP_ID)
        feed_entries.extend(beamer_entries)
        progress.update(task, description=f"  {WEAVE_CONFIG.name}: 피드 {len(feed_entries)}건 (Beamer {len(beamer_entries)}건)")
        weave_data = CompetitorData(
            competitor_name=WEAVE_CONFIG.name,
            search_results=search_results,
            docs_pages=docs_pages,
            feed_entries=feed_entries,
        )
        progress.update(task, description=f"[green]  {WEAVE_CONFIG.name}: 완료")
        progress.remove_task(task)

    run = CollectionRun(date=today, mode="initial", competitors=all_competitors, weave_data=weave_data)
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
    console.print(
        f"  {weave_data.competitor_name}: "
        f"검색 {len(weave_data.search_results)}건, "
        f"문서 {len(weave_data.docs_pages)}건, "
        f"피드 {len(weave_data.feed_entries)}건"
    )


@weave.op()
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


@weave.op()
def discover_cmd() -> None:
    asyncio.run(_discover_and_save())


@weave.op()
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
    console.print(f"  카테고리: {len(run.competitors[0].categories) if run.competitors else 0}개")
    console.print(f"  종합 분석: {'완료' if run.synthesis else '없음'}")


@weave.op()
def report() -> None:
    analysis = load_latest_analysis()
    if analysis is None:
        console.print("[red]분석 데이터가 없습니다. 먼저 'analyze'를 실행하세요.")
        sys.exit(1)

    settings = Settings()
    discovery_result = load_latest_discovery()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("리포트 생성 중...", total=None)
        weekly_path, comparison_path, detail_path = save_report(analysis, discovery=discovery_result)
        progress.update(task, description="인덱스 업데이트 중...")
        update_index(analysis=analysis)
        progress.update(task, description="[green]영어 리포트 완료")
        progress.remove_task(task)

        # Translation step
        english_paths = {
            "index": Path("index.md"),
            "comparison": comparison_path,
            "detail": detail_path,
            "weekly": weekly_path,
        }

        def on_translate_progress(lang: str, key: str) -> None:
            progress.update(translate_task, description=f"번역 중... ({lang}/{key})")

        translate_task = progress.add_task("번역 중...", total=None)
        translated = translate_all_reports(settings, english_paths, on_progress=on_translate_progress)
        progress.update(translate_task, description="[green]번역 완료")
        progress.remove_task(translate_task)

    console.print()
    console.print(f"[bold green]리포트 저장:")
    console.print(f"  주간 리포트: {weekly_path}")
    console.print(f"  상세 비교표: {comparison_path}")
    console.print(f"  경쟁사 상세: {detail_path}")
    console.print(f"  경쟁사: {len(analysis.competitors)}개")
    console.print(f"  카테고리: {len(analysis.competitors[0].categories) if analysis.competitors else 0}개")
    console.print(f"  인덱스 업데이트: index.md")
    for lang, paths in translated.items():
        console.print(f"  {lang} 번역: {len(paths)}개 파일")
    if discovery_result and discovery_result.emerging_competitors:
        console.print(f"  신규 경쟁사: {len(discovery_result.emerging_competitors)}개")


@weave.op()
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

    settings = Settings()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("리포트 생성 중...", total=None)
        weekly_path, comparison_path, detail_path = save_report(analysis, discovery_result)
        progress.update(task, description="인덱스 업데이트 중...")
        update_index(analysis=analysis)
        progress.update(task, description="[green]영어 리포트 완료")
        progress.remove_task(task)

        # Translation step
        english_paths = {
            "index": Path("index.md"),
            "comparison": comparison_path,
            "detail": detail_path,
            "weekly": weekly_path,
        }

        def on_translate_progress(lang: str, key: str) -> None:
            progress.update(translate_task, description=f"번역 중... ({lang}/{key})")

        translate_task = progress.add_task("번역 중...", total=None)
        translated = translate_all_reports(settings, english_paths, on_progress=on_translate_progress)
        progress.update(translate_task, description="[green]번역 완료")
        progress.remove_task(translate_task)

    console.print()
    console.print(f"[bold green]리포트 저장:")
    console.print(f"  주간 리포트: {weekly_path}")
    console.print(f"  상세 비교표: {comparison_path}")
    console.print(f"  경쟁사 상세: {detail_path}")
    for lang, paths in translated.items():
        console.print(f"  {lang} 번역: {len(paths)}개 파일")
    if discovery_result and discovery_result.emerging_competitors:
        console.print(f"  신규 경쟁사: {len(discovery_result.emerging_competitors)}개")
    if settings.slack_webhook_url:
        try:
            send_slack_notification(settings.slack_webhook_url, analysis, weekly_path)
        except Exception as exc:
            console.print(f"[yellow]Slack 알림 실패: {exc}")


def preview() -> None:
    """Analyze + generate Korean preview from existing collection data."""
    settings = Settings()
    collection = load_latest_collection()
    if collection is None:
        console.print("[red]수집 데이터가 없습니다. 먼저 'collect'를 실행하세요.")
        sys.exit(1)

    console.print(f"{collection.date} 수집 데이터로 프리뷰 생성 중...")
    console.print()

    tasks: dict[str, int] = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Analyze
        def on_progress(name: str, status: str) -> None:
            if status == "analyzing":
                tasks[name] = progress.add_task(f"{name} 분석 중...", total=None)
            elif status == "done" and name in tasks:
                progress.update(tasks[name], description=f"[green]  {name}: 완료")
                progress.remove_task(tasks[name])

        analysis = analyze_all(collection, settings, on_progress=on_progress)

        # Generate English weekly report
        task = progress.add_task("리포트 생성 중...", total=None)
        english_content = generate_weekly_report(analysis)
        progress.update(task, description="[green]영어 리포트 완료")
        progress.remove_task(task)

        # Translate to Korean
        task = progress.add_task("한국어 번역 중...", total=None)
        from openai import OpenAI

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )
        korean_content = translate_content(
            client, settings.translation_model, english_content, "ko"
        )
        progress.update(task, description="[green]한국어 번역 완료")
        progress.remove_task(task)

    preview_path = Path("preview.md")
    preview_path.write_text(korean_content, encoding="utf-8")

    console.print()
    console.print(f"[bold green]프리뷰 저장: {preview_path}")
    console.print(f"  경쟁사: {len(analysis.competitors)}개")
    console.print(f"  카테고리: {len(analysis.competitors[0].categories) if analysis.competitors else 0}개")


def main() -> None:
    if os.environ.get("WANDB_API_KEY"):
        weave.init("llm-observability-market-research")

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
    elif args[0] == "preview":
        preview()
    elif args[0] == "publish-prompts":
        from intel_bot.prompts import publish_prompts
        if not os.environ.get("WANDB_API_KEY"):
            console.print("[red]WANDB_API_KEY가 필요합니다.")
            sys.exit(1)
        if weave.get_client() is None:
            weave.init("llm-observability-market-research")
        publish_prompts()
        console.print("[bold green]프롬프트 발행 완료")
    else:
        console.print(f"[red]알 수 없는 명령: {args[0]}")
        console.print("사용법: python -m intel_bot [collect|analyze|report|discover|run|preview|publish-prompts]")
        sys.exit(1)
