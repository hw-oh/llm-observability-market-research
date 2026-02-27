from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

Rating = Literal["strong", "medium", "none"]
Availability = Literal["yes", "no", "partial"]


# ---------------------------------------------------------------------------
# Baseline — per-product feature snapshot (source of truth)
# ---------------------------------------------------------------------------

class SubFeature(BaseModel):
    name: str               # 제품이 실제로 부르는 기능명
    provision_method: str   # 제공 방식
    notes: str              # 비고


class FeatureBaseline(BaseModel):
    item_name: str                      # 작은 카테고리 (49개 표준 항목명)
    available: Availability
    sub_features: list[SubFeature] = []


class CategoryBaseline(BaseModel):
    category_name: str        # 큰 카테고리 (8개)
    features: list[FeatureBaseline]


class ProductBaseline(BaseModel):
    product_name: str
    last_updated: str
    categories: list[CategoryBaseline]


# ---------------------------------------------------------------------------
# Step 1 output — UpdateCollector: recent updates per product
# ---------------------------------------------------------------------------

class RecentUpdate(BaseModel):
    title: str
    date: str = ""
    summary: str


class ProductUpdates(BaseModel):
    product_name: str
    updates: list[RecentUpdate] = []


# ---------------------------------------------------------------------------
# Step 2 output — BaselineAnalyzer: changeset + updated baseline
# ---------------------------------------------------------------------------

class FeatureChange(BaseModel):
    item_name: str
    sub_feature_name: str = ""  # 변경된 sub_feature name ("NEW" = 신규 추가)
    field: str                  # "available", "name", "provision_method", "notes"
    before: str
    after: str


class ProductChangeset(BaseModel):
    product_name: str
    changes: list[FeatureChange] = []
    updated_baseline: ProductBaseline


# ---------------------------------------------------------------------------
# Step 3 output — ReportWriter: cross-product comparison + commentary
# ---------------------------------------------------------------------------

class ProductFeatureRating(BaseModel):
    product_name: str
    rating: Rating
    note: str = ""


class FeatureComparison(BaseModel):
    item_name: str
    ratings: list[ProductFeatureRating]


class CategoryComparison(BaseModel):
    category_name: str
    features: list[FeatureComparison]


class ProductHighlight(BaseModel):
    product_name: str
    summary: str


class AIComment(BaseModel):
    product_highlights: list[ProductHighlight]
    market_trend: str


class ReportSynthesis(BaseModel):
    ai_comment: AIComment
    categories: list[CategoryComparison]


# ---------------------------------------------------------------------------
# Top-level run record
# ---------------------------------------------------------------------------

class AnalysisRun(BaseModel):
    date: str
    model: str
    updates: list[ProductUpdates] = []
    changesets: list[ProductChangeset] = []
    synthesis: ReportSynthesis | None = None
