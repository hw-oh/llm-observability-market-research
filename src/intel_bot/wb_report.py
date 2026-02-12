"""W&B Report 생성 모듈."""

from __future__ import annotations

import re

import wandb_workspaces.reports.v2 as wr


def _strip_meta(md: str) -> tuple[str, str]:
    """YAML frontmatter, H1 타이틀, Date/Model 메타라인을 제거.

    Returns (title, body) — title은 H1에서 추출, body는 나머지.
    """
    text = md

    # Strip YAML frontmatter
    text = re.sub(r"^---\n.*?\n---\n*", "", text, count=1, flags=re.DOTALL)

    # Extract and remove H1 title
    title = ""
    m = re.match(r"^# (.+)\n", text)
    if m:
        title = m.group(1).strip()
        text = text[m.end():]

    # Remove Date/Model meta line (e.g. **Date**: ... | **Model**: ...)
    text = re.sub(r"^\*\*Date\*\*:.*\n*", "", text)
    # Also handle translated variants (날짜, 日付 etc.)
    text = re.sub(r"^\*\*(날짜|日付|Date)\*\*:.*\n*", "", text)

    return title, text.lstrip("\n")


def _shift_headers(md: str) -> str:
    """본문 헤더를 H3부터 시작하도록 동적 시프트.

    본문의 최소 헤더 레벨을 찾아서 그것이 H3이 되도록 조정.
    H6 초과 시 볼드 텍스트로 변환.
    """
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
    """본문에서 메타 제거 → 헤더 시프트. Returns (title, body)."""
    title, body = _strip_meta(md)
    return title, _shift_headers(body)


def _lang_blocks(
    weekly: str, comparison: str, detail: str, first_expanded: bool = True,
) -> list:
    """한 언어의 3개 섹션 블록을 생성."""
    w_title, w_body = _prepare(weekly)
    c_title, c_body = _prepare(comparison)
    d_title, d_body = _prepare(detail)

    weekly_blocks: list = [
        wr.H2(w_title or "Latest Report"),
        wr.MarkdownBlock(text=w_body),
    ] if first_expanded else [
        wr.H2(
            w_title or "Latest Report",
            collapsed_blocks=[wr.MarkdownBlock(text=w_body)],
        ),
    ]

    return [
        *weekly_blocks,
        wr.H2(
            c_title or "Detailed Feature Comparison",
            collapsed_blocks=[wr.MarkdownBlock(text=c_body)],
        ),
        wr.H2(
            d_title or "Product Detail",
            collapsed_blocks=[wr.MarkdownBlock(text=d_body)],
        ),
    ]


def publish_wb_report(
    weekly_en: str,
    weekly_ko: str,
    weekly_ja: str,
    comparison_en: str,
    comparison_ko: str,
    comparison_ja: str,
    detail_en: str,
    detail_ko: str,
    detail_ja: str,
    report_date: str,
) -> str:
    """W&B Report 생성 후 URL 반환."""

    report = wr.Report(
        entity="wandb-smle",
        project="llm-observability-market-research",
        title=f"LLM Observability Market Research — {report_date}",
        description=f"Weekly competitor intelligence report ({report_date})",
    )

    report.blocks = [
        wr.TableOfContents(),
        wr.H1("English", collapsed_blocks=_lang_blocks(weekly_en, comparison_en, detail_en)),
        wr.H1("한국어", collapsed_blocks=_lang_blocks(weekly_ko, comparison_ko, detail_ko)),
        wr.H1("日本語", collapsed_blocks=_lang_blocks(weekly_ja, comparison_ja, detail_ja)),
    ]

    report.save()
    return report.url
