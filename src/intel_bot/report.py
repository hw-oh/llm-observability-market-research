from __future__ import annotations

import re
from pathlib import Path

from intel_bot.config import COMPARISON_AXES
from intel_bot.models import AnalysisRun, CompetitorAnalysis, DiscoveryResult

REPORTS_DIR = Path("reports")

COMPARISON_LABEL = {
    "stronger": "경쟁사 우위",
    "comparable": "유사",
    "weaker": "Weave 우위",
    "unknown": "정보 부족",
}


def _build_header(run: AnalysisRun) -> str:
    return (
        "---\n"
        "layout: default\n"
        f"title: 경쟁사 인텔리전스 리포트 - {run.date}\n"
        "---\n"
        "\n"
        "# W&B Weave — 경쟁사 인텔리전스 리포트\n"
        f"**날짜**: {run.date} | **모델**: {run.model} | **데이터 수집일**: {run.collection_date}\n"
    )


def _format_cell(supported: bool, feature_name: str, feature_url: str) -> str:
    """O/X 셀 포맷: O면 [기능명](URL) 또는 기능명, X면 X"""
    if not supported:
        return "X"
    if feature_url:
        return f"[{feature_name}]({feature_url})"
    if feature_name:
        return feature_name
    return "O"


def _build_feature_ox_tables(run: AnalysisRun) -> str:
    lines = ["## 축별 기능 비교", ""]

    competitor_names = [c.competitor_name for c in run.competitors]

    # Build per-axis tables
    for axis in COMPARISON_AXES:
        lines.append(f"### {axis}")
        lines.append("")

        # Header row
        header = f"| 기능 | **Weave** | {' | '.join(competitor_names)} |"
        separator = "|---|---|" + "---|" * len(competitor_names)
        lines.append(header)
        lines.append(separator)

        # Collect features from all competitors for this axis
        # Use the first competitor that has features for this axis to define feature list
        all_features: dict[str, dict[str, tuple[bool, str, str]]] = {}

        for comp in run.competitors:
            axis_data = next((a for a in comp.axes if a.axis == axis), None)
            if not axis_data:
                continue
            for feat in axis_data.features:
                if feat.feature_name not in all_features:
                    all_features[feat.feature_name] = {
                        "__weave__": (feat.weave_supported, feat.weave_feature_name, feat.weave_feature_url),
                    }
                else:
                    # Update Weave info if we got better data
                    existing_weave = all_features[feat.feature_name].get("__weave__", (False, "", ""))
                    if not existing_weave[1] and feat.weave_feature_name:
                        all_features[feat.feature_name]["__weave__"] = (
                            feat.weave_supported, feat.weave_feature_name, feat.weave_feature_url,
                        )
                all_features[feat.feature_name][comp.competitor_name] = (
                    feat.competitor_supported, feat.competitor_feature_name, feat.competitor_feature_url,
                )

        # Build rows
        for feature_name, comp_data in all_features.items():
            weave_sup, weave_name, weave_url = comp_data.get("__weave__", (False, "", ""))
            weave_cell = _format_cell(weave_sup, weave_name, weave_url)

            cells = [weave_cell]
            for cname in competitor_names:
                sup, fname, furl = comp_data.get(cname, (False, "", ""))
                cells.append(_format_cell(sup, fname, furl))

            row = f"| {feature_name} | {' | '.join(cells)} |"
            lines.append(row)

        lines.append("")

    return "\n".join(lines) + "\n"


def _build_competitor_detail(comp: CompetitorAnalysis) -> str:
    lines = [
        f"### {comp.competitor_name}",
        "",
        f"**개요**: {comp.overall_summary}",
        "",
        "**Weave 대비 강점**:",
    ]

    if comp.strengths_vs_weave:
        for s in comp.strengths_vs_weave:
            lines.append(f"- {s}")
    else:
        lines.append("- *보고된 내용 없음*")

    lines.append("")
    lines.append("**Weave 대비 약점**:")

    if comp.weaknesses_vs_weave:
        for w in comp.weaknesses_vs_weave:
            lines.append(f"- {w}")
    else:
        lines.append("- *보고된 내용 없음*")

    lines.append("")
    lines.append("**주요 업데이트**:")

    if comp.notable_updates:
        for u in comp.notable_updates:
            lines.append(f"- {u}")
    else:
        lines.append("- *보고된 내용 없음*")

    lines.append("")
    lines.append("| 축 | 판정 | 요약 |")
    lines.append("|---|---|---|")

    axis_map = {a.axis: a for a in comp.axes}
    for axis in COMPARISON_AXES:
        a = axis_map.get(axis)
        if a:
            verdict = COMPARISON_LABEL.get(a.weave_comparison, COMPARISON_LABEL["unknown"])
            summary = a.summary.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {axis} | {verdict} | {summary} |")
        else:
            lines.append(f"| {axis} | {COMPARISON_LABEL['unknown']} | - |")

    return "\n".join(lines) + "\n"


def _build_emerging_competitors(discovery: DiscoveryResult) -> str:
    lines = ["## 신규 경쟁사", ""]

    if not discovery.emerging_competitors:
        lines.append("이번 주 신규 경쟁사가 발견되지 않았습니다.")
        return "\n".join(lines) + "\n"

    lines.append(
        f"*{discovery.date}에 {len(discovery.queries)}개 검색 쿼리에서 "
        f"{discovery.search_results_count}개 결과를 기반으로 자동 발견됨.*"
    )
    lines.append("")
    lines.append("| 제품 | 설명 | 출처 |")
    lines.append("|------|------|------|")

    for ec in discovery.emerging_competitors:
        desc = ec.description.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| **{ec.name}** | {desc} | [링크]({ec.source_url}) |")

    lines.append("")
    lines.append("> *자동 감지된 항목으로 아직 추적 대상이 아닙니다. 추가하려면 `config.py`를 수정하세요.*")

    return "\n".join(lines) + "\n"


def _build_methodology(run: AnalysisRun) -> str:
    return (
        "## 분석 방법론\n"
        "\n"
        f"데이터는 {run.collection_date}에 Serper.dev 웹 검색, "
        "공식 문서 스크래핑, GitHub/PyPI 피드를 통해 수집되었습니다.\n"
        f"분석은 OpenRouter를 통해 {run.model} 모델로 수행되었습니다.\n"
    )


def generate_report(
    run: AnalysisRun,
    discovery: DiscoveryResult | None = None,
) -> str:
    sections = [
        _build_header(run),
        "---\n",
        _build_feature_ox_tables(run),
        "---\n",
        "## 경쟁사 상세 분석\n",
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
    discovery: DiscoveryResult | None = None,
) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{run.date}.md"
    content = generate_report(run, discovery)
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
