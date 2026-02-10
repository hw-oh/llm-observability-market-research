from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


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


class AxisAnalysis(BaseModel):
    axis: str
    summary: str
    key_features: list[str]
    weave_comparison: str  # "stronger" | "comparable" | "weaker" | "unknown"
    weave_comparison_reason: str


class CompetitorAnalysis(BaseModel):
    competitor_name: str
    overall_summary: str
    axes: list[AxisAnalysis]
    strengths_vs_weave: list[str]
    weaknesses_vs_weave: list[str]
    notable_updates: list[str]


class AnalysisRun(BaseModel):
    date: str
    model: str
    collection_date: str
    competitors: list[CompetitorAnalysis] = []


class EmergingCompetitor(BaseModel):
    name: str
    description: str
    source_url: str


class DiscoveryResult(BaseModel):
    date: str
    queries: list[str] = []
    search_results_count: int = 0
    emerging_competitors: list[EmergingCompetitor] = []
