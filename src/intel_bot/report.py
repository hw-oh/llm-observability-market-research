from __future__ import annotations

import re
from pathlib import Path

from intel_bot.config import COMPARISON_AXES
from intel_bot.models import AnalysisRun, CompetitorAnalysis, DiscoveryResult

CHANGE_EMOJI = {
    "upgraded": "⬆️",
    "downgraded": "⬇️",
}

REPORTS_DIR = Path("reports")

COMPARISON_EMOJI = {
    "stronger": "\U0001f534",
    "comparable": "\U0001f7e1",
    "weaker": "\U0001f7e2",
    "unknown": "\u26aa",
}

COMPARISON_LABEL = {
    "stronger": "\U0001f534 Stronger",
    "comparable": "\U0001f7e1 Comparable",
    "weaker": "\U0001f7e2 Weaker",
    "unknown": "\u26aa Unknown",
}


def _build_header(run: AnalysisRun) -> str:
    return (
        "---\n"
        "layout: default\n"
        f"title: Competitor Intel Report - {run.date}\n"
        "---\n"
        "\n"
        "# W&B Weave — Competitor Intelligence Report\n"
        f"**Date**: {run.date} | **Model**: {run.model} | **Data collected**: {run.collection_date}\n"
    )


def _build_executive_summary(run: AnalysisRun) -> str:
    lines = [
        "## Executive Summary",
        "",
        f"Analyzed **{len(run.competitors)} competitors** across **{len(COMPARISON_AXES)} axes**.",
        "",
        "| Competitor | \U0001f7e2 Weave Stronger | \U0001f7e1 Comparable | \U0001f534 Competitor Stronger |",
        "|---|---|---|---|",
    ]
    for comp in run.competitors:
        stronger = sum(1 for a in comp.axes if a.weave_comparison == "stronger")
        comparable = sum(1 for a in comp.axes if a.weave_comparison == "comparable")
        weaker = sum(1 for a in comp.axes if a.weave_comparison == "weaker")
        lines.append(f"| {comp.competitor_name} | {weaker} | {comparable} | {stronger} |")
    return "\n".join(lines) + "\n"


def _build_changes_section(current: AnalysisRun, previous: AnalysisRun) -> str:
    # Build lookup: {(competitor, axis): weave_comparison} for previous
    prev_map: dict[tuple[str, str], str] = {}
    for comp in previous.competitors:
        for a in comp.axes:
            prev_map[(comp.competitor_name, a.axis)] = a.weave_comparison

    # Detect changes
    SEVERITY = {"weaker": 0, "unknown": 1, "comparable": 2, "stronger": 3}
    changes: list[tuple[str, str, str, str, str]] = []
    for comp in current.competitors:
        for a in comp.axes:
            prev_val = prev_map.get((comp.competitor_name, a.axis))
            if prev_val is not None and prev_val != a.weave_comparison:
                prev_sev = SEVERITY.get(prev_val, 1)
                curr_sev = SEVERITY.get(a.weave_comparison, 1)
                arrow = CHANGE_EMOJI["upgraded"] if curr_sev > prev_sev else CHANGE_EMOJI["downgraded"]
                changes.append((
                    comp.competitor_name,
                    a.axis,
                    COMPARISON_LABEL.get(prev_val, prev_val),
                    COMPARISON_LABEL.get(a.weave_comparison, a.weave_comparison),
                    arrow,
                ))

    lines = [f"## Changes Since Last Report ({previous.date})", ""]

    if not changes:
        lines.append(f"No changes in competitive positioning since {previous.date}.")
    else:
        lines.append("| Competitor | Axis | Previous | Current | Change |")
        lines.append("|---|---|---|---|---|")
        for comp_name, axis, prev_label, curr_label, arrow in changes:
            lines.append(f"| {comp_name} | {axis} | {prev_label} | {curr_label} | {arrow} |")

    return "\n".join(lines) + "\n"


def _build_comparison_matrix(run: AnalysisRun) -> str:
    lines = [
        "## Comparison Matrix",
        "",
        "> \U0001f7e2 Weave stronger \u00b7 \U0001f7e1 Comparable \u00b7 \U0001f534 Competitor stronger \u00b7 \u26aa Unknown",
        "",
    ]

    # Header row
    header = "| Axis |"
    separator = "|---|"
    for comp in run.competitors:
        header += f" {comp.competitor_name} |"
        separator += "---|"
    lines.append(header)
    lines.append(separator)

    # Build axis lookup per competitor
    comp_axis_maps: list[dict[str, str]] = []
    for comp in run.competitors:
        axis_map = {a.axis: a.weave_comparison for a in comp.axes}
        comp_axis_maps.append(axis_map)

    # Data rows
    for axis in COMPARISON_AXES:
        row = f"| {axis} |"
        for axis_map in comp_axis_maps:
            comparison = axis_map.get(axis, "unknown")
            row += f" {COMPARISON_EMOJI.get(comparison, '\u26aa')} |"
        lines.append(row)

    return "\n".join(lines) + "\n"


def _build_competitor_detail(comp: CompetitorAnalysis) -> str:
    lines = [
        f"### {comp.competitor_name}",
        "",
        f"**Overall**: {comp.overall_summary}",
        "",
        "**Strengths vs Weave**:",
    ]

    if comp.strengths_vs_weave:
        for s in comp.strengths_vs_weave:
            lines.append(f"- {s}")
    else:
        lines.append("- *None reported*")

    lines.append("")
    lines.append("**Weaknesses vs Weave**:")

    if comp.weaknesses_vs_weave:
        for w in comp.weaknesses_vs_weave:
            lines.append(f"- {w}")
    else:
        lines.append("- *None reported*")

    lines.append("")
    lines.append("**Notable Updates**:")

    if comp.notable_updates:
        for u in comp.notable_updates:
            lines.append(f"- {u}")
    else:
        lines.append("- *None reported*")

    lines.append("")
    lines.append("| Axis | Verdict | Key Features | Summary |")
    lines.append("|---|---|---|---|")

    axis_map = {a.axis: a for a in comp.axes}
    for axis in COMPARISON_AXES:
        a = axis_map.get(axis)
        if a:
            verdict = COMPARISON_LABEL.get(a.weave_comparison, COMPARISON_LABEL["unknown"])
            features = ", ".join(a.key_features) if a.key_features else "-"
            summary = a.summary.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {axis} | {verdict} | {features} | {summary} |")
        else:
            lines.append(f"| {axis} | {COMPARISON_LABEL['unknown']} | - | - |")

    return "\n".join(lines) + "\n"


def _build_emerging_competitors(discovery: DiscoveryResult) -> str:
    lines = ["## Emerging Competitors", ""]

    if not discovery.emerging_competitors:
        lines.append("No new competitors detected this week.")
        return "\n".join(lines) + "\n"

    lines.append(
        f"*Auto-discovered on {discovery.date} from {discovery.search_results_count} "
        f"search results across {len(discovery.queries)} broad queries.*"
    )
    lines.append("")
    lines.append("| Product | Description | Source |")
    lines.append("|---------|-------------|--------|")

    for ec in discovery.emerging_competitors:
        desc = ec.description.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| **{ec.name}** | {desc} | [link]({ec.source_url}) |")

    lines.append("")
    lines.append("> *These are automatically detected and not yet tracked. To add one, update `config.py`.*")

    return "\n".join(lines) + "\n"


def _build_methodology(run: AnalysisRun) -> str:
    return (
        "## Methodology\n"
        "\n"
        f"Data collected on {run.collection_date} via Serper.dev web search, "
        "official docs scraping, and GitHub/PyPI feeds.\n"
        f"Analysis by {run.model} via OpenRouter.\n"
    )


def generate_report(
    run: AnalysisRun,
    previous: AnalysisRun | None = None,
    discovery: DiscoveryResult | None = None,
) -> str:
    sections = [
        _build_header(run),
        "---\n",
        _build_executive_summary(run),
    ]

    if previous is not None:
        sections.append("---\n")
        sections.append(_build_changes_section(run, previous))

    sections += [
        "---\n",
        _build_comparison_matrix(run),
        "---\n",
        "## Competitor Details\n",
    ]

    for comp in run.competitors:
        sections.append(_build_competitor_detail(comp))
        sections.append("---\n")

    sections.append(_build_methodology(run))

    if discovery is not None and discovery.emerging_competitors:
        sections.append("\n---\n")
        sections.append(_build_emerging_competitors(discovery))

    return "\n".join(sections)


def save_report(
    run: AnalysisRun,
    previous: AnalysisRun | None = None,
    discovery: DiscoveryResult | None = None,
) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{run.date}.md"
    content = generate_report(run, previous, discovery)
    report_path.write_text(content, encoding="utf-8")
    return report_path


def update_index(index_path: str = "index.md") -> None:
    index_file = Path(index_path)

    # Discover reports
    report_files = sorted(
        REPORTS_DIR.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"),
        key=lambda p: p.stem,
        reverse=True,
    )

    # Build archive table
    archive_lines = ["| Date | Report |", "|------|--------|"]
    for rp in report_files:
        archive_lines.append(f"| {rp.stem} | [View Report](./reports/{rp.name}) |")

    archive_content = "\n".join(archive_lines) + "\n"

    # Build latest report link
    if report_files:
        latest = report_files[0]
        latest_content = f"[\U0001f4cb Latest Report ({latest.stem})](./reports/{latest.name})\n"
    else:
        latest_content = "\uc544\uc9c1 \uc0dd\uc131\ub41c \ub9ac\ud3ec\ud2b8\uac00 \uc5c6\uc2b5\ub2c8\ub2e4.\n"

    if not index_file.exists():
        _write_full_index(index_file, latest_content, archive_content)
        return

    content = index_file.read_text(encoding="utf-8")

    archive_pattern = r"<!-- REPORT_ARCHIVE_START -->\n.*?<!-- REPORT_ARCHIVE_END -->"
    latest_pattern = r"<!-- LATEST_REPORT_START -->\n.*?<!-- LATEST_REPORT_END -->"

    has_archive = "<!-- REPORT_ARCHIVE_START -->" in content
    has_latest = "<!-- LATEST_REPORT_START -->" in content

    if has_archive and has_latest:
        content = re.sub(
            archive_pattern,
            f"<!-- REPORT_ARCHIVE_START -->\n{archive_content}<!-- REPORT_ARCHIVE_END -->",
            content,
            flags=re.DOTALL,
        )
        content = re.sub(
            latest_pattern,
            f"<!-- LATEST_REPORT_START -->\n{latest_content}<!-- LATEST_REPORT_END -->",
            content,
            flags=re.DOTALL,
        )
        index_file.write_text(content, encoding="utf-8")
    else:
        _write_full_index(index_file, latest_content, archive_content)


def _write_full_index(index_file: Path, latest_content: str, archive_content: str) -> None:
    content = (
        "---\n"
        "layout: default\n"
        "title: Home\n"
        "---\n"
        "\n"
        "# Competitor Intel Bot\n"
        "\n"
        "W&B Weave \uacbd\uc7c1\uc0ac \uc81c\ud488 \ube44\uad50 \ub9ac\ud3ec\ud2b8\n"
        "\n"
        "## Latest Report\n"
        "\n"
        "<!-- LATEST_REPORT_START -->\n"
        f"{latest_content}"
        "<!-- LATEST_REPORT_END -->\n"
        "\n"
        "## Report Archive\n"
        "\n"
        "<!-- REPORT_ARCHIVE_START -->\n"
        f"{archive_content}"
        "<!-- REPORT_ARCHIVE_END -->\n"
        "\n"
        "---\n"
        "\n"
        "[ROADMAP](./ROADMAP.md) \u00b7 [GitHub](https://github.com/hw-oh/competitor-intel-bot)\n"
    )
    index_file.write_text(content, encoding="utf-8")
