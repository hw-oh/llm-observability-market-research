from __future__ import annotations

import os
import sys
import threading
from datetime import date
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from intel_bot.analyzer import analyze_all
from intel_bot.config import Settings
from intel_bot.models import AnalysisRun
from intel_bot.report import save_report, update_index
from intel_bot.translator import translate_all_reports
from intel_bot.storage import load_latest_analysis, save_analysis

console = Console()


# ---------------------------------------------------------------------------
# Shared pipeline components
# ---------------------------------------------------------------------------

def _generate_report_and_translate(
    analysis: AnalysisRun,
    settings: Settings,
) -> Path:
    """리포트 생성 + 번역."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("리포트 생성 중...", total=None)
        weekly_path = save_report(analysis)
        progress.update(task, description="인덱스 업데이트 중...")
        update_index(analysis=analysis)
        progress.update(task, description="[green]영어 리포트 완료")
        progress.remove_task(task)

        english_paths = {"weekly": weekly_path}

        def on_translate_progress(lang: str, key: str) -> None:
            progress.update(translate_task, description=f"번역 중... ({lang}/{key})")

        translate_task = progress.add_task("번역 중...", total=None)
        translated = translate_all_reports(settings, english_paths, on_progress=on_translate_progress)
        progress.update(translate_task, description="[green]번역 완료")
        progress.remove_task(translate_task)

    console.print()
    console.print("[bold green]리포트 저장:")
    console.print(f"  주간 리포트: {weekly_path}")
    for lang, paths in translated.items():
        console.print(f"  {lang} 번역: {len(paths)}개 파일")

    return weekly_path


def _run_optional_plugins(
    settings: Settings,
    analysis: AnalysisRun,
    weekly_path: Path,
) -> None:
    """비차단 옵션 플러그인: Slack + W&B Report."""
    if settings.slack_webhook_url:
        try:
            from intel_bot.notify import send_slack_notification
            send_slack_notification(settings.slack_webhook_url.get_secret_value(), analysis, weekly_path)
        except Exception as exc:
            console.print(f"[yellow]Slack 알림 실패: {exc}")

    if os.environ.get("WANDB_API_KEY"):
        import wandb

        weekly_en = weekly_path.read_text(encoding="utf-8")
        weekly_ko = (Path("ko") / weekly_path).read_text(encoding="utf-8")
        weekly_ja = (Path("ja") / weekly_path).read_text(encoding="utf-8")

        try:
            import markdown as md_lib

            html_en = md_lib.markdown(weekly_en, extensions=["tables", "fenced_code"])
            html_ko = md_lib.markdown(weekly_ko, extensions=["tables", "fenced_code"])
            html_ja = md_lib.markdown(weekly_ja, extensions=["tables", "fenced_code"])

            wandb.log({
                "report_en": wandb.Html(html_en),
                "report_ko": wandb.Html(html_ko),
                "report_ja": wandb.Html(html_ja),
            })
            console.print("  W&B run에 리포트 로깅 완료")
        except Exception as exc:
            console.print(f"[yellow]W&B 리포트 로깅 실패: {exc}")

        try:
            from intel_bot.wb_report import publish_wb_report

            report_url = publish_wb_report(
                weekly_en, weekly_ko, weekly_ja,
                report_date=analysis.date,
            )
            console.print(f"  W&B Report: {report_url}")

            wandb.alert(
                title=f"Market Research Report — {analysis.date}",
                text=f"Weekly report published: {report_url}",
            )
            console.print("  W&B Alert 전송 완료")
        except Exception as exc:
            console.print(f"[yellow]W&B Report 발행 실패: {exc}")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def analyze() -> None:
    settings = Settings()

    console.print("3-에이전트 파이프라인 분석 시작... (제품별 병렬 처리)")
    console.print()

    tasks: dict[str, int] = {}
    lock = threading.Lock()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        def on_progress(name: str, status: str) -> None:
            with lock:
                if "done" in status and name in tasks:
                    progress.update(tasks[name], description=f"[green]  {name}: 완료")
                elif "failed" in status and name in tasks:
                    progress.update(tasks[name], description=f"[red]  {name}: {status}")
                elif name not in tasks:
                    tasks[name] = progress.add_task(f"  {name}: {status}...", total=None)
                else:
                    progress.update(tasks[name], description=f"  {name}: {status}...")

        run = analyze_all(settings, on_progress=on_progress)

    path = save_analysis(run)

    console.print()
    console.print(f"[bold green]분석 완료: {path}")
    console.print(f"  제품: {len(run.updates)}개")
    console.print(f"  변경사항: {sum(len(cs.changes) for cs in run.changesets)}건")
    console.print(f"  종합 분석: {'완료' if run.synthesis else '없음'}")


def report() -> None:
    analysis = load_latest_analysis()
    if analysis is None:
        console.print("[red]분석 데이터가 없습니다. 먼저 'analyze'를 실행하세요.")
        sys.exit(1)

    settings = Settings()
    weekly_path = _generate_report_and_translate(analysis, settings)
    _run_optional_plugins(settings, analysis, weekly_path)


def run() -> None:
    """analyze → report → plugins."""
    analyze()

    analysis = load_latest_analysis()
    settings = Settings()

    weekly_path = _generate_report_and_translate(analysis, settings)
    _run_optional_plugins(settings, analysis, weekly_path)


def publish_prompts_cmd() -> None:
    from intel_bot.prompts import publish_prompts
    publish_prompts()
    console.print("[bold green]프롬프트 Weave에 퍼블리시 완료")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    from dotenv import load_dotenv
    load_dotenv()

    import wandb as _wandb

    if os.environ.get("WANDB_API_KEY"):
        import weave

        today = date.today().isoformat()
        prefix = "report" if os.environ.get("GITHUB_ACTIONS") else "test"
        _wandb.init(
            entity="wandb-smle",
            project="llm-observability-market-research",
            name=f"{prefix}-{today}",
        )
        weave.init("wandb-smle/llm-observability-market-research")
        # Disable crewAI autopatch due to circular-reference serialization
        # issues in some weave/crewai version combinations.
        from weave.integrations.crewai.crewai_sdk import _crewai_patcher
        if _crewai_patcher is not None:
            _crewai_patcher.undo_patch()

    try:
        args = sys.argv[1:]
        cmd = args[0] if args else "run"

        commands = {
            "analyze": analyze,
            "report": report,
            "run": run,
            "publish-prompts": publish_prompts_cmd,
        }

        if cmd in commands:
            commands[cmd]()
        else:
            console.print(f"[red]알 수 없는 명령: {cmd}")
            console.print(
                "사용법: python -m intel_bot "
                "[analyze|report|run|publish-prompts]"
            )
            sys.exit(1)
    finally:
        if _wandb.run is not None:
            _wandb.finish()
