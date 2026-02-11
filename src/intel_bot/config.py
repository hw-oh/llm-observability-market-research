from __future__ import annotations

from dataclasses import dataclass, field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    serper_dev_api: str
    openrouter_api_key: str
    openrouter_model: str = "google/gemini-3-pro-preview"
    translation_model: str = "google/gemini-3-flash-preview"
    slack_webhook_url: str | None = None


SUPPORTED_LANGS = ["ko", "ja"]
LANGUAGE_NAMES = {"ko": "Korean", "ja": "Japanese"}


@dataclass
class CompetitorConfig:
    name: str
    docs_url: str
    changelog_url: str | None
    github_repo: str | None
    pypi_package: str | None


COMPETITORS: list[CompetitorConfig] = [
    CompetitorConfig(
        name="LangSmith",
        docs_url="https://docs.smith.langchain.com",
        changelog_url="https://changelog.langchain.com",
        github_repo="langchain-ai/langsmith-sdk",
        pypi_package="langsmith",
    ),
    CompetitorConfig(
        name="Arize Phoenix",
        docs_url="https://docs.arize.com/phoenix",
        changelog_url=None,
        github_repo="Arize-ai/phoenix",
        pypi_package="arize-phoenix",
    ),
    CompetitorConfig(
        name="Braintrust",
        docs_url="https://braintrust.dev/docs",
        changelog_url="https://braintrust.dev/docs/changelog",
        github_repo="braintrustdata/braintrust-sdk",
        pypi_package="braintrust",
    ),
    CompetitorConfig(
        name="Langfuse",
        docs_url="https://langfuse.com/docs",
        changelog_url="https://langfuse.com/changelog",
        github_repo="langfuse/langfuse",
        pypi_package="langfuse",
    ),
    CompetitorConfig(
        name="Humanloop",
        docs_url="https://humanloop.com/docs",
        changelog_url="https://humanloop.com/docs/changelog",
        github_repo=None,
        pypi_package="humanloop",
    ),
    CompetitorConfig(
        name="Logfire",
        docs_url="https://logfire.pydantic.dev/docs",
        changelog_url="https://logfire.pydantic.dev/docs/release-notes",
        github_repo="pydantic/logfire",
        pypi_package="logfire",
    ),
    CompetitorConfig(
        name="Helicone",
        docs_url="https://docs.helicone.ai",
        changelog_url="https://docs.helicone.ai/changelog",
        github_repo="Helicone/helicone",
        pypi_package="helicone",
    ),
]


@dataclass
class CategoryDef:
    name: str          # English name (LLM schema key)
    name_ko: str       # Korean name (report display)
    items: list[str] = field(default_factory=list)  # Sub-items (English)


COMPARISON_CATEGORIES: list[CategoryDef] = [
    CategoryDef("Core Observability", "핵심 옵저버빌리티",
        ["Trace Depth", "Hierarchical Spans", "Prompt Logging", "Response Logging",
         "Token Tracking", "Latency Analysis", "Replay"]),
    CategoryDef("Agent / RAG Observability", "에이전트/RAG 옵저버빌리티",
        ["Tool Call Tracing", "Retrieval Tracing", "Memory Tracing",
         "Multi-step Reasoning", "Workflow Graph", "Failure Visualization"]),
    CategoryDef("Evaluation Integration", "평가 통합",
        ["Trace→Dataset", "LLM-as-Judge", "Custom Eval Metrics",
         "Regression Detection", "Model Comparison", "Human Feedback UI"]),
    CategoryDef("Monitoring & Metrics", "모니터링 & 메트릭",
        ["Cost Dashboard", "Token Analytics", "Latency Monitoring",
         "Error Tracking", "Tool Success Rate", "Custom Metrics"]),
    CategoryDef("Experiment / Improvement Loop", "실험/개선 루프",
        ["Prompt Versioning", "Model Versioning", "Experiment Tracking",
         "Dataset Versioning", "Continuous Eval", "RL/Fine-tuning Link"]),
    CategoryDef("DevEx / Integration", "개발자 경험/통합",
        ["SDK Support", "Framework Integration", "Custom Model Support",
         "API Access", "Streaming Tracing", "CLI/Infra Integration"]),
    CategoryDef("Enterprise & Security", "엔터프라이즈 & 보안",
        ["On-prem/VPC", "RBAC", "PII Masking", "Audit Logs",
         "Data Retention", "Region Support"]),
]

# Section 2 summary table dimensions
SUMMARY_DIMENSIONS = ["Trace Depth", "Eval", "Agent Observability", "Cost Tracking", "Enterprise Ready", "Overall"]
