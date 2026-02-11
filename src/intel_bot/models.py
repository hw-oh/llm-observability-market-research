from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Rating = Literal["strong", "medium", "weak", "none"]


class SearchResult(BaseModel):
    query: str
    title: str
    link: str
    snippet: str
    date: str | None = None


class DocsPage(BaseModel):
    url: str
    title: str
    content: str
    fetched_at: datetime = Field(default_factory=datetime.now)


class FeedEntry(BaseModel):
    source: str  # "github" or "pypi"
    title: str
    link: str
    published: str | None = None
    summary: str = ""


class CompetitorData(BaseModel):
    competitor_name: str
    search_results: list[SearchResult] = []
    docs_pages: list[DocsPage] = []
    feed_entries: list[FeedEntry] = []


class CollectionRun(BaseModel):
    date: str
    mode: str = "initial"  # "initial" or "update"
    competitors: list[CompetitorData] = []


class FeatureRating(BaseModel):
    item_name: str          # Must match config sub-item exactly
    weave_rating: Rating
    competitor_rating: Rating
    note: str = ""


class CategoryAnalysis(BaseModel):
    category_name: str      # Must match CategoryDef.name
    features: list[FeatureRating]
    summary: str


class NewFeature(BaseModel):
    feature_name: str
    description: str
    release_date: str
    category: str


class PositioningShift(BaseModel):
    current_position: str
    moving_toward: str
    signal: str


class CompetitorAnalysis(BaseModel):
    competitor_name: str
    overall_summary: str
    categories: list[CategoryAnalysis]  # 7 categories
    new_features: list[NewFeature] = []  # 0-5
    positioning: PositioningShift
    strengths_vs_weave: list[str]
    weaknesses_vs_weave: list[str]


class VendorSummaryRating(BaseModel):
    vendor_name: str
    trace_depth: Rating
    eval: Rating
    agent_observability: Rating
    cost_tracking: Rating
    enterprise_ready: Rating
    overall: Rating


class WeeklyInsight(BaseModel):
    title: str
    body: str


class SynthesisResult(BaseModel):
    executive_summary: list[str]        # Exactly 5 items
    one_line_verdict: str
    weave_summary: str                  # Weave overall summary for detail page
    weave_strengths: list[str]          # 3-5 selling points
    weave_weaknesses: list[str]         # 3-5 areas to improve
    weave_positioning: PositioningShift  # Weave's own positioning
    weave_new_features: list[NewFeature]  # 0-5 Weave recent updates
    vendor_ratings: list[VendorSummaryRating]  # Including Weave
    enterprise_signals: list[str]       # 3-5 items
    insights: list[WeeklyInsight]       # Exactly 3
    watchlist: list[str]                # 3-5 items


class AnalysisRun(BaseModel):
    date: str
    model: str
    collection_date: str
    competitors: list[CompetitorAnalysis] = []
    synthesis: SynthesisResult | None = None


class EmergingCompetitor(BaseModel):
    name: str
    description: str
    source_url: str


class DiscoveryResult(BaseModel):
    date: str
    queries: list[str] = []
    search_results_count: int = 0
    emerging_competitors: list[EmergingCompetitor] = []
