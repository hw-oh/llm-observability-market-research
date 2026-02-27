"""W&B Report 생성 모듈."""

from __future__ import annotations

import re

import wandb_workspaces.reports.v2 as wr


def _strip_meta(md: str) -> tuple[str, str]:
    """YAML frontmatter, H1 타이틀, Date/Model 메타라인을 제거.

    Returns (title, body) — title은 H1에서 추출, body는 나머지.
    """
    text = md
    text = re.sub(r"^---\n.*?\n---\n*", "", text, count=1, flags=re.DOTALL)

    title = ""
    m = re.match(r"^# (.+)\n", text)
    if m:
        title = m.group(1).strip()
        text = text[m.end():]

    text = re.sub(r"^\*\*Date\*\*:.*\n*", "", text)
    text = re.sub(r"^\*\*(날짜|日付|Date)\*\*:.*\n*", "", text)

    return title, text.lstrip("\n")


def _shift_headers(md: str) -> str:
    """본문 헤더를 H3부터 시작하도록 동적 시프트."""
    levels = [len(m.group(1)) for m in re.finditer(r"^(#{1,6}) ", md, re.MULTILINE)]
    if not levels:
        return md
    shift = 3 - min(levels)
    if shift == 0:
        return md

    def _replace(m: re.Match[str]) -> str:
        hashes = m.group(1)
        title = m.group(2)
        new_level = len(hashes) + shift
        if new_level <= 6:
            return f"{'#' * new_level} {title}"
        return f"**{title}**"

    return re.sub(r"^(#{1,6}) (.+)$", _replace, md, flags=re.MULTILINE)


def _prepare(md: str) -> tuple[str, str]:
    title, body = _strip_meta(md)
    return title, _shift_headers(body)


def publish_wb_report(
    weekly_en: str,
    weekly_ko: str,
    weekly_ja: str,
    report_date: str,
) -> str:
    """W&B Report 생성 후 URL 반환."""

    en_title, en_body = _prepare(weekly_en)
    ko_title, ko_body = _prepare(weekly_ko)
    ja_title, ja_body = _prepare(weekly_ja)

    report = wr.Report(
        entity="wandb-smle",
        project="llm-observability-market-research",
        title=f"LLM Observability Market Research — {report_date}",
        description=f"Weekly competitor intelligence report ({report_date})",
    )

    report.blocks = [
        wr.TableOfContents(),
        wr.H1("English", collapsed_blocks=[
            wr.H2(en_title or "Latest Report"),
            wr.MarkdownBlock(text=en_body),
        ]),
        wr.H1("한국어", collapsed_blocks=[
            wr.H2(ko_title or "최신 리포트"),
            wr.MarkdownBlock(text=ko_body),
        ]),
        wr.H1("日本語", collapsed_blocks=[
            wr.H2(ja_title or "最新レポート"),
            wr.MarkdownBlock(text=ja_body),
        ]),
    ]

    report.save()
    return report.url
