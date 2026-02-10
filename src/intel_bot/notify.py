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
            f":large_green_circle: {weaker} stronger  "
            f":large_yellow_circle: {comparable} comparable  "
            f":red_circle: {stronger} competitor stronger"
        )

    competitor_summary = "\n".join(summary_lines)
    axes_count = len(run.competitors[0].axes) if run.competitors else 0

    payload = {
        "text": (
            f":bar_chart: *Competitor Intel Report — {run.date}*\n"
            f"Analyzed *{len(run.competitors)} competitors* across *{axes_count} axes*.\n\n"
            f"{competitor_summary}\n\n"
            f"Report: `{report_path}`"
        ),
    }

    try:
        resp = httpx.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        console.print("[green]Slack notification sent.")
    except Exception as exc:
        console.print(f"[yellow]Slack notification failed: {exc}")
