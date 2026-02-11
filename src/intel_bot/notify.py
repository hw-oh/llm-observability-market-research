from __future__ import annotations

from pathlib import Path

import httpx
from rich.console import Console

from intel_bot.models import AnalysisRun

console = Console()


def send_slack_notification(webhook_url: str, run: AnalysisRun, report_path: Path) -> None:
    summary_lines = []
    for comp in run.competitors:
        stronger = sum(1 for a in comp.axes if a.weave_comparison == "stronger")
        comparable = sum(1 for a in comp.axes if a.weave_comparison == "comparable")
        weaker = sum(1 for a in comp.axes if a.weave_comparison == "weaker")
        summary_lines.append(
            f"• *{comp.competitor_name}*: "
            f":large_green_circle: Weave 우위 {weaker}  "
            f":large_yellow_circle: 유사 {comparable}  "
            f":red_circle: 경쟁사 우위 {stronger}"
        )

    competitor_summary = "\n".join(summary_lines)
    axes_count = len(run.competitors[0].axes) if run.competitors else 0

    payload = {
        "text": (
            f":bar_chart: *경쟁사 인텔리전스 리포트 — {run.date}*\n"
            f"*{len(run.competitors)}개 경쟁사*를 *{axes_count}개 축*에서 분석했습니다.\n\n"
            f"{competitor_summary}\n\n"
            f"리포트: `{report_path}`"
        ),
    }

    try:
        resp = httpx.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        console.print("[green]Slack 알림 전송 완료.")
    except Exception as exc:
        console.print(f"[yellow]Slack 알림 실패: {exc}")
