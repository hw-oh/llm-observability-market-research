"""Report generation — single weekly markdown report with 4 sections.

1. AI Comment (per-product highlights + market trend)
2. Recent Updates (per product)
3. Feature Comparison Summary (8 categories)
4. Detailed Feature Comparison (49 items)
"""

from __future__ import annotations

import re
from pathlib import Path

from intel_bot.config import COMPARISON_CATEGORIES, get_active_products
from intel_bot.models import AnalysisRun

REPORTS_DIR = Path("reports")

RATING_SYMBOL: dict[str, str] = {
    "strong": "O",
    "medium": "\u25b3",
    "none": "X",
}


def _changelog_url_map() -> dict[str, str]:
    return {c.name: c.changelog_link for c in get_active_products() if c.changelog_link}


def _sym(rating: str) -> str:
    return RATING_SYMBOL.get(rating, "-")


def _normalize_cat(name: str) -> str:
    """Strip numeric prefix like '1. ' from category names."""
    return re.sub(r"^\d+\.\s*", "", name)


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _section_ai_comment(run: AnalysisRun) -> list[str]:
    lines = ["## 1. AI Comment", ""]
    if run.synthesis and run.synthesis.ai_comment:
        ai = run.synthesis.ai_comment
        lines.append("### Product Highlights")
        lines.append("")
        for ph in ai.product_highlights:
            lines.append(f"- **{ph.product_name}**: {ph.summary}")
        lines.append("")
        lines.append("### Market Trend")
        lines.append("")
        lines.append(ai.market_trend)
    else:
        lines.append("*No commentary available*")
    lines.append("")
    return lines


def _section_recent_updates(run: AnalysisRun) -> list[str]:
    lines = ["## 2. Recent Updates", ""]
    products_with_changes = {
        cs.product_name for cs in run.changesets if cs.changes
    }
    has_any = False
    for pu in run.updates:
        if not pu.updates:
            continue
        if pu.product_name not in products_with_changes:
            continue
        has_any = True
        cl_url = _changelog_url_map().get(pu.product_name)
        if cl_url:
            lines.append(f"### [{pu.product_name}]({cl_url})")
        else:
            lines.append(f"### {pu.product_name}")
        for upd in pu.updates:
            date_part = f" ({upd.date})" if upd.date else ""
            lines.append(f"- **{upd.title}**{date_part} — {upd.summary}")
        lines.append("")
    if not has_any:
        lines.append("*No significant updates were detected this week. All products remain unchanged from the current baseline.*")
        lines.append("")
    return lines


def _section_summary_table(run: AnalysisRun) -> list[str]:
    """8-category summary table: rating symbol + strong count."""
    if not run.synthesis:
        return ["## 3. Feature Comparison (Summary)", "", "*No synthesis data*", ""]

    product_names = [cs.product_name for cs in run.changesets]
    lines = ["## 3. Feature Comparison (Summary)", ""]
    lines.append("> O(Strong) / \u25b3(Medium) / X(None)")
    lines.append("")

    header = f"| Category | {' | '.join(product_names)} |"
    sep = "|---|" + "---|" * len(product_names)
    lines.append(header)
    lines.append(sep)

    for cat_def in COMPARISON_CATEGORIES:
        cat_data = next(
            (c for c in run.synthesis.categories
             if _normalize_cat(c.category_name) == cat_def.name),
            None,
        )
        cells: list[str] = []
        for pname in product_names:
            if not cat_data:
                cells.append("-")
                continue
            strong = 0
            total = len(cat_data.features)
            for feat in cat_data.features:
                pr = next((r for r in feat.ratings if r.product_name == pname), None)
                if pr and pr.rating == "strong":
                    strong += 1
            avg = strong / total if total else 0
            if avg >= 0.6:
                sym = "O"
            elif avg >= 0.2:
                sym = "\u25b3"
            else:
                sym = "X"
            cells.append(f"{sym} ({strong}/{total})")
        lines.append(f"| {cat_def.name} | {' | '.join(cells)} |")

    lines.append("")
    return lines


def _section_detailed_table(run: AnalysisRun) -> list[str]:
    """49-item detailed comparison, grouped by category."""
    if not run.synthesis:
        return ["## 4. Detailed Feature Comparison", "", "*No synthesis data*", ""]

    product_names = [cs.product_name for cs in run.changesets]
    lines = ["## 4. Detailed Feature Comparison", ""]
    lines.append("> O(Strong) / \u25b3(Medium) / X(None)")
    lines.append("")

    for cat_def in COMPARISON_CATEGORIES:
        lines.append(f"### {cat_def.name}")
        lines.append("")

        header = f"| Feature | {' | '.join(product_names)} |"
        sep = "|---|" + "---|" * len(product_names)
        lines.append(header)
        lines.append(sep)

        cat_data = next(
            (c for c in run.synthesis.categories
             if _normalize_cat(c.category_name) == cat_def.name),
            None,
        )

        for item_name, _item_desc in cat_def.items:
            feat_data = None
            if cat_data:
                feat_data = next(
                    (f for f in cat_data.features if f.item_name == item_name),
                    None,
                )
            cells: list[str] = []
            for pname in product_names:
                if not feat_data:
                    cells.append("-")
                    continue
                pr = next((r for r in feat_data.ratings if r.product_name == pname), None)
                cells.append(_sym(pr.rating) if pr else "-")
            lines.append(f"| {item_name} | {' | '.join(cells)} |")

        lines.append("")

    return lines


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_weekly_report(run: AnalysisRun) -> str:
    lines = [
        "---",
        "layout: default",
        f"title: LLM Observability Market Research - {run.date}",
        "---",
        "",
        "# Weekly LLM Observability Market Research Report",
        f"**Date**: {run.date} | **Model**: {run.model}",
        "",
    ]
    lines.extend(_section_ai_comment(run))
    lines.extend(_section_recent_updates(run))
    lines.extend(_section_summary_table(run))
    lines.extend(_section_detailed_table(run))

    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append(
        "Data was collected via 3-agent pipeline: UpdateCollector (Perplexity Sonar) "
        "for changelog and web search, BaselineAnalyzer (Gemini Pro) for baseline "
        "comparison and update, and ReportWriter (Gemini Pro) for cross-product "
        "comparison and commentary."
    )
    lines.append("")

    return "\n".join(lines) + "\n"


def save_report(run: AnalysisRun) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    weekly_path = REPORTS_DIR / f"{run.date}.md"
    weekly_path.write_text(generate_weekly_report(run), encoding="utf-8")
    return weekly_path


def update_index(index_path: str = "index.md", analysis: AnalysisRun | None = None) -> None:
    index_file = Path(index_path)

    report_files = sorted(
        REPORTS_DIR.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"),
        key=lambda p: p.stem,
        reverse=True,
    )

    archive_lines = ["| Date | Report |", "|------|--------|"]
    for rp in report_files:
        archive_lines.append(f"| {rp.stem} | [View Report](./reports/{rp.name}) |")
    archive_content = "\n".join(archive_lines) + "\n"

    if report_files:
        latest = report_files[0]
        latest_parts = [f"[\U0001f4cb Latest Report ({latest.stem})](./reports/{latest.name})\n"]
        if analysis and analysis.synthesis and analysis.synthesis.ai_comment:
            ai = analysis.synthesis.ai_comment
            latest_parts.append("")
            for ph in ai.product_highlights:
                latest_parts.append(f"- **{ph.product_name}**: {ph.summary}")
            latest_parts.append("")
            latest_parts.append(f"> {ai.market_trend}")
            latest_parts.append("")
        latest_content = "\n".join(latest_parts) + "\n"
    else:
        latest_content = "No reports generated yet.\n"

    content = (
        "---\n"
        "layout: default\n"
        "title: LLM Observability Market Research\n"
        "---\n"
        "\n"
        "## Executive Summary\n"
        "\n"
        "<!-- LATEST_REPORT_START -->\n"
        "\n"
        f"{latest_content}"
        "\n"
        "<!-- LATEST_REPORT_END -->\n"
        "\n"
        "## Report Archive\n"
        "\n"
        "<!-- REPORT_ARCHIVE_START -->\n"
        "\n"
        f"{archive_content}"
        "\n"
        "<!-- REPORT_ARCHIVE_END -->\n"
    )
    index_file.write_text(content, encoding="utf-8")
