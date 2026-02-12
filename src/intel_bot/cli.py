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
from intel_bot.collectors.docs_scraper import scrape_docs
from intel_bot.collectors.feed import fetch_competitor_feeds
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


def _publish_wb_report_and_alert(
    weekly_path: Path,
    comparison_path: Path,
    detail_path: Path,
    report_date: str,
) -> None:
    """W&B Report 발행 + Alert (WANDB_API_KEY가 있을 때만)."""
    if not os.environ.get("WANDB_API_KEY"):
        return

    from intel_bot.wb_report import publish_wb_report

    weekly_en = weekly_path.read_text(encoding="utf-8")
    comparison_en = comparison_path.read_text(encoding="utf-8")
    detail_en = detail_path.read_text(encoding="utf-8")

    weekly_ko = (Path("ko") / weekly_path).read_text(encoding="utf-8")
    weekly_ja = (Path("ja") / weekly_path).read_text(encoding="utf-8")
    comparison_ko = (Path("ko") / comparison_path).read_text(encoding="utf-8")
    comparison_ja = (Path("ja") / comparison_path).read_text(encoding="utf-8")
    detail_ko = (Path("ko") / detail_path).read_text(encoding="utf-8")
    detail_ja = (Path("ja") / detail_path).read_text(encoding="utf-8")

    report_url = publish_wb_report(
        weekly_en, weekly_ko, weekly_ja,
        comparison_en, comparison_ko, comparison_ja,
        detail_en, detail_ko, detail_ja,
        report_date=report_date,
    )
    console.print(f"  W&B Report: {report_url}")

    import wandb

    wandb.alert(
        title=f"Market Research Report — {report_date}",
        text=f"Weekly report published: {report_url}",
    )
    console.print("  W&B Alert 전송 완료")


async def _collect_product(comp, progress):
    """피드 + extra_docs 수집. (카테고리 검색은 Sonar가 분석 시 수행)"""
    from intel_bot.models import DocsPage

    task = progress.add_task(f"{comp.name} 수집 중...", total=None)

    # Feed 수집
    feed_entries = fetch_competitor_feeds(comp)
    progress.update(task, description=f"  {comp.name}: 피드 {len(feed_entries)}건")

    # extra_docs만 스크래핑
    docs_pages: list[DocsPage] = []
    if comp.extra_docs_urls:
        for url in comp.extra_docs_urls:
            try:
                page = await scrape_docs(url)
                docs_pages.append(page)
            except Exception as e:
                print(f"  [warn] Scraping failed for {url}: {e}")
    progress.update(task, description=f"  {comp.name}: 문서 {len(docs_pages)}건")

    progress.update(task, description=f"[green]  {comp.name}: 완료")
    progress.remove_task(task)

    return CompetitorData(
        competitor_name=comp.name,
        product_description=comp.product_description,
        product_context=comp.product_context,
        docs_pages=docs_pages,
        feed_entries=feed_entries,
    )


async def _collect() -> None:
    today = date.today().isoformat()

    all_competitors: list[CompetitorData] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for comp in COMPETITORS:
            comp_data = await _collect_product(comp, progress)
            all_competitors.append(comp_data)

        # Weave 자체 데이터 수집 (경쟁사와 동일한 파이프라인 + Beamer changelog)
        weave_data = await _collect_product(WEAVE_CONFIG, progress)
        beamer_entries = await fetch_beamer_changelog(BEAMER_APP_ID)
        weave_data.feed_entries.extend(beamer_entries)

    run = CollectionRun(date=today, mode="initial", competitors=all_competitors, weave_data=weave_data)
    path = save_collection(run)

    console.print()
    console.print(f"[bold green]수집 완료: {path}")
    console.print()
    for comp_data in all_competitors:
        console.print(
            f"  {comp_data.competitor_name}: "
            f"문서 {len(comp_data.docs_pages)}건, "
            f"피드 {len(comp_data.feed_entries)}건"
        )
    console.print(
        f"  {weave_data.competitor_name}: "
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

    try:
        _publish_wb_report_and_alert(weekly_path, comparison_path, detail_path, analysis.date)
    except Exception as exc:
        console.print(f"[yellow]W&B Report 발행 실패: {exc}")


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

    try:
        _publish_wb_report_and_alert(weekly_path, comparison_path, detail_path, analysis.date)
    except Exception as exc:
        console.print(f"[yellow]W&B Report 발행 실패: {exc}")


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
    import wandb as _wandb

    if os.environ.get("WANDB_API_KEY"):
        today = date.today().isoformat()
        _wandb.init(
            entity="wandb-smle",
            project="llm-observability-market-research",
            name=f"report-{today}",
        )
        weave.init("wandb-smle/llm-observability-market-research")

    try:
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
            publish_prompts()
            console.print("[bold green]프롬프트 발행 완료")
        else:
            console.print(f"[red]알 수 없는 명령: {args[0]}")
            console.print("사용법: python -m intel_bot [collect|analyze|report|discover|run|preview|publish-prompts]")
            sys.exit(1)
    finally:
        if _wandb.run is not None:
            _wandb.finish()
