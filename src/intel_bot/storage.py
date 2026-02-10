from __future__ import annotations

import json
from pathlib import Path

from intel_bot.models import AnalysisRun, CollectionRun, CompetitorData, DiscoveryResult


def save_collection(run: CollectionRun, base_dir: str = "data/raw") -> Path:
    dir_path = Path(base_dir) / run.date
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / "collection.json"
    file_path.write_text(
        json.dumps(run.model_dump(), ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    return file_path


def load_latest_collection(base_dir: str = "data/raw") -> CollectionRun | None:
    base = Path(base_dir)
    if not base.exists():
        return None

    dirs = sorted(
        [d for d in base.iterdir() if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )
    if not dirs:
        return None

    latest_file = dirs[0] / "collection.json"
    if not latest_file.exists():
        return None

    data = json.loads(latest_file.read_text(encoding="utf-8"))
    return CollectionRun.model_validate(data)


def save_analysis(run: AnalysisRun, base_dir: str = "data/analyzed") -> Path:
    dir_path = Path(base_dir) / run.date
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / "analysis.json"
    file_path.write_text(
        json.dumps(run.model_dump(), ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    return file_path


def load_latest_analysis(base_dir: str = "data/analyzed") -> AnalysisRun | None:
    base = Path(base_dir)
    if not base.exists():
        return None

    dirs = sorted(
        [d for d in base.iterdir() if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )
    if not dirs:
        return None

    latest_file = dirs[0] / "analysis.json"
    if not latest_file.exists():
        return None

    data = json.loads(latest_file.read_text(encoding="utf-8"))
    return AnalysisRun.model_validate(data)


def load_previous_analysis(base_dir: str = "data/analyzed") -> AnalysisRun | None:
    base = Path(base_dir)
    if not base.exists():
        return None

    dirs = sorted(
        [d for d in base.iterdir() if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )
    if len(dirs) < 2:
        return None

    prev_file = dirs[1] / "analysis.json"
    if not prev_file.exists():
        return None

    data = json.loads(prev_file.read_text(encoding="utf-8"))
    return AnalysisRun.model_validate(data)


def save_discovery(result: DiscoveryResult, base_dir: str = "data/raw") -> Path:
    dir_path = Path(base_dir) / result.date
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / "discovery.json"
    file_path.write_text(
        json.dumps(result.model_dump(), ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    return file_path


def load_latest_discovery(base_dir: str = "data/raw") -> DiscoveryResult | None:
    base = Path(base_dir)
    if not base.exists():
        return None

    dirs = sorted(
        [d for d in base.iterdir() if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )
    if not dirs:
        return None

    latest_file = dirs[0] / "discovery.json"
    if not latest_file.exists():
        return None

    data = json.loads(latest_file.read_text(encoding="utf-8"))
    return DiscoveryResult.model_validate(data)


def has_changes(current: CompetitorData, previous: CompetitorData) -> bool:
    current_links = {e.link for e in current.feed_entries}
    previous_links = {e.link for e in previous.feed_entries}
    return bool(current_links - previous_links)
