from __future__ import annotations

import json
from pathlib import Path

from intel_bot.models import AnalysisRun, ProductBaseline


def _latest_dir(base_dir: str) -> Path | None:
    base = Path(base_dir)
    if not base.exists():
        return None
    dirs = sorted(
        [d for d in base.iterdir() if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )
    return dirs[0] if dirs else None


def _save_json(data, dir_path: Path, filename: str) -> Path:
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / filename
    file_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    return file_path


def _load_json(base_dir: str, filename: str) -> dict | None:
    latest = _latest_dir(base_dir)
    if latest is None:
        return None
    file_path = latest / filename
    if not file_path.exists():
        return None
    return json.loads(file_path.read_text(encoding="utf-8"))


BASELINE_DIR = "data"


def _product_slug(name: str) -> str:
    return name.lower().replace(" ", "-").replace("&", "and")


def save_baseline(baseline: ProductBaseline, base_dir: str = BASELINE_DIR) -> Path:
    """Save baseline as data/{product_slug}/{date}.json."""
    dir_path = Path(base_dir) / _product_slug(baseline.product_name)
    dir_path.mkdir(parents=True, exist_ok=True)
    date_str = baseline.last_updated or "unknown"
    file_path = dir_path / f"{date_str}.json"
    file_path.write_text(
        json.dumps(baseline.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return file_path


def load_baseline(product_name: str, base_dir: str = BASELINE_DIR) -> ProductBaseline | None:
    """Load the latest baseline from data/{product_slug}/ (most recent date file)."""
    dir_path = Path(base_dir) / _product_slug(product_name)
    if not dir_path.exists():
        return None
    json_files = sorted(dir_path.glob("*.json"), reverse=True)
    if not json_files:
        return None
    try:
        data = json.loads(json_files[0].read_text(encoding="utf-8"))
        return ProductBaseline.model_validate(data)
    except Exception:
        return None


def load_all_baselines(base_dir: str = BASELINE_DIR) -> list[ProductBaseline]:
    """Load the latest baseline for each product under data/."""
    base = Path(base_dir)
    if not base.exists():
        return []
    baselines: list[ProductBaseline] = []
    for product_dir in sorted(base.iterdir()):
        if not product_dir.is_dir() or product_dir.name == "analyzed":
            continue
        json_files = sorted(product_dir.glob("*.json"), reverse=True)
        if not json_files:
            continue
        try:
            data = json.loads(json_files[0].read_text(encoding="utf-8"))
            baselines.append(ProductBaseline.model_validate(data))
        except Exception:
            continue
    return baselines


def save_analysis(run: AnalysisRun, base_dir: str = "data/analyzed") -> Path:
    return _save_json(run.model_dump(), Path(base_dir) / run.date, "analysis.json")


def load_latest_analysis(base_dir: str = "data/analyzed") -> AnalysisRun | None:
    data = _load_json(base_dir, "analysis.json")
    if data is None:
        return None
    try:
        return AnalysisRun.model_validate(data)
    except Exception:
        return None
