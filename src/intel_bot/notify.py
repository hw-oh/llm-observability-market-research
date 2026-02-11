from __future__ import annotations

from pathlib import Path

import httpx
from rich.console import Console

from intel_bot.models import AnalysisRun

console = Console()

RATING_EMOJI = {
    "strong": ":large_green_circle:",
    "medium": ":large_yellow_circle:",
    "weak": ":red_circle:",
    "none": ":white_circle:",
}


def send_slack_notification(webhook_url: str, run: AnalysisRun, weekly_path: Path) -> None:
    synthesis = run.synthesis

    # One-line verdict
    verdict = ""
    if synthesis:
        verdict = f"\n> {synthesis.one_line_verdict}\n"

    # Vendor overall ratings
    summary_lines = []
    if synthesis and synthesis.vendor_ratings:
        for vr in synthesis.vendor_ratings:
            emoji = RATING_EMOJI.get(vr.overall, ":white_circle:")
            summary_lines.append(f"  {emoji} *{vr.vendor_name}*: Overall {vr.overall}")
    else:
        for comp in run.competitors:
            summary_lines.append(f"  :white_circle: *{comp.competitor_name}*")

    competitor_summary = "\n".join(summary_lines)

    payload = {
        "text": (
            f":bar_chart: *경쟁사 인텔리전스 리포트 — {run.date}*\n"
            f"*{len(run.competitors)}개 경쟁사*를 *7개 카테고리*에서 분석했습니다.\n"
            f"{verdict}\n"
            f"{competitor_summary}\n\n"
            f"리포트: `{weekly_path}`"
        ),
    }

    try:
        resp = httpx.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        console.print("[green]Slack 알림 전송 완료.")
    except Exception as exc:
        console.print(f"[yellow]Slack 알림 실패: {exc}")
