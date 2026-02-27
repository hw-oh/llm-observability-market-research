from __future__ import annotations

from pathlib import Path

import httpx
from rich.console import Console

from intel_bot.models import AnalysisRun

console = Console()


def send_slack_notification(webhook_url: str, run: AnalysisRun, weekly_path: Path) -> None:
    synthesis = run.synthesis

    verdict = ""
    if synthesis and synthesis.ai_comment:
        verdict = f"\n> {synthesis.ai_comment.market_trend}\n"

    product_lines = [f"  :white_circle: *{pu.product_name}*" for pu in run.updates]
    product_summary = "\n".join(product_lines)

    total_changes = sum(len(cs.changes) for cs in run.changesets)
    change_info = f"  :arrows_counterclockwise: *{total_changes} changes detected*" if total_changes else ""

    payload = {
        "text": (
            f":bar_chart: *LLM Observability Market Research — {run.date}*\n"
            f"Analyzed *{len(run.updates)} products*.\n"
            f"{verdict}\n"
            f"{product_summary}\n"
            f"{change_info}\n\n"
            f"Report: `{weekly_path}`"
        ),
    }

    try:
        resp = httpx.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        console.print("[green]Slack 알림 전송 완료.")
    except Exception as exc:
        console.print(f"[yellow]Slack 알림 실패: {exc}")
