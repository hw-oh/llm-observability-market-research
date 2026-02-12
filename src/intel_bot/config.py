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
    changelog_url: str | None        # 수집용 (RSS/HTML)
    changelog_display_url: str | None = None  # 사람용 (브라우저 링크). None이면 changelog_url 사용
    github_repo: str | None = None
    pypi_package: str | None = None
    extra_docs_urls: list[str] = field(default_factory=list)  # 추가 문서 URL

    @property
    def changelog_link(self) -> str | None:
        """리포트에 표시할 changelog URL."""
        return self.changelog_display_url or self.changelog_url


COMPETITORS: list[CompetitorConfig] = [
    CompetitorConfig(
        name="LangSmith",
        docs_url="https://docs.smith.langchain.com",
        changelog_url="https://changelog.langchain.com/feed.rss",
        changelog_display_url="https://changelog.langchain.com",
        github_repo="langchain-ai/langsmith-sdk",
        pypi_package="langsmith",
    ),
    CompetitorConfig(
        name="Langfuse",
        docs_url="https://langfuse.com/docs",
        changelog_url="https://langfuse.com/changelog",
        github_repo="langfuse/langfuse",
        pypi_package="langfuse",
    ),
    CompetitorConfig(
        name="Braintrust",
        docs_url="https://braintrust.dev/docs",
        changelog_url="https://braintrust.dev/docs/changelog",
        github_repo="braintrustdata/braintrust-sdk",
        pypi_package="braintrust",
    ),
    CompetitorConfig(
        name="MLflow",
        docs_url="https://mlflow.org/docs/latest/genai",
        changelog_url="https://mlflow.org/releases",
        github_repo="mlflow/mlflow",
        pypi_package="mlflow",
    ),
    CompetitorConfig(
        name="Arize Phoenix",
        docs_url="https://docs.arize.com/phoenix",
        changelog_url="https://arize.com/docs/phoenix/release-notes",
        github_repo="Arize-ai/phoenix",
        pypi_package="arize-phoenix",
    ),
]

WEAVE_CONFIG = CompetitorConfig(
    name="W&B Weave",
    docs_url="https://weave-docs.wandb.ai",
    changelog_url="https://app.getbeamer.com/wandb/en",
    github_repo="wandb/weave",
    pypi_package="weave",
    extra_docs_urls=[
        "https://docs.wandb.ai/weave/guides/tracking/redact-pii",
        "https://docs.wandb.ai/platform/hosting",
        "https://docs.wandb.ai/platform/access-management",
        "https://docs.wandb.ai/platform/hosting/monitoring-usage/audit-logging",
        "https://docs.wandb.ai/platform/hosting/data-retention",
    ],
)

BEAMER_APP_ID = "iTpiKrhl12143"


@dataclass
class CategoryDef:
    name: str          # English name (LLM schema key)
    name_ko: str       # Korean name (report display)
    items: list[tuple[str, str]] = field(default_factory=list)  # (name, description)
    search_queries: list[str] = field(default_factory=list)  # 검색 쿼리 템플릿 ({name} = competitor name)


COMPARISON_CATEGORIES: list[CategoryDef] = [
    CategoryDef("Core Observability", "핵심 옵저버빌리티", [
        ("Trace Depth", "Nested function call trace depth"),
        ("Hierarchical Spans", "Parent-child span relationships"),
        ("Prompt Logging", "Automatic capture of LLM prompts"),
        ("Response Logging", "Automatic capture of LLM responses"),
        ("Token Tracking", "Input/output token usage counting"),
        ("Latency Analysis", "Per-span and end-to-end latency measurement"),
        ("Replay", "Step-by-step trace replay in UI"),
    ], [
        "{name} tracing spans nested function calls",
        "{name} prompt response logging token tracking",
        "{name} latency analysis trace replay",
    ]),
    CategoryDef("Agent / RAG Observability", "에이전트/RAG 옵저버빌리티", [
        ("Tool Call Tracing", "Capture of tool/function call inputs and outputs"),
        ("Retrieval Tracing", "Logging of retriever queries and returned documents"),
        ("Memory Tracing", "Tracking of conversational memory reads/writes"),
        ("Multi-step Reasoning", "Visualization of multi-turn agent reasoning chains"),
        ("Workflow Graph", "DAG or graph view of agent workflows"),
        ("Failure Visualization", "Highlighting of failed steps in a trace"),
    ], [
        "{name} agent tool call tracing function calls",
        "{name} RAG retrieval tracing document retriever",
        "{name} multi-step reasoning workflow graph visualization",
    ]),
    CategoryDef("Evaluation Integration", "평가 통합", [
        ("Trace→Dataset", "Convert production traces into eval datasets"),
        ("LLM-as-Judge", "Built-in LLM-based evaluation scoring"),
        ("Custom Eval Metrics", "User-defined evaluation functions"),
        ("Regression Detection", "Automatic detection of quality regressions"),
        ("Model Comparison", "Side-by-side comparison of model outputs"),
        ("Human Feedback UI", "UI for human annotation and labeling"),
    ], [
        "{name} LLM evaluation judge scoring metrics",
        "{name} trace to dataset eval pipeline regression",
        "{name} human feedback annotation model comparison",
    ]),
    CategoryDef("Monitoring & Metrics", "모니터링 & 메트릭", [
        ("Cost Dashboard", "Real-time LLM cost tracking dashboard"),
        ("Token Analytics", "Token usage breakdown and trends"),
        ("Latency Monitoring", "Latency percentiles and alerting"),
        ("Error Tracking", "Error rate monitoring and alerting"),
        ("Tool Success Rate", "Success/failure rate of tool calls"),
        ("Custom Metrics", "User-defined custom metric tracking"),
    ], [
        "{name} cost dashboard token analytics monitoring",
        "{name} latency percentiles error tracking alerting",
        "{name} custom metrics tool success rate",
    ]),
    CategoryDef("Experiment / Improvement Loop", "실험/개선 루프", [
        ("Prompt Versioning", "Version control for prompt templates"),
        ("Model Versioning", "Tracking of model versions and configs"),
        ("Experiment Tracking", "A/B test and experiment management"),
        ("Dataset Versioning", "Versioned eval and training datasets"),
        ("Continuous Eval", "Scheduled or triggered evaluation runs"),
        ("RL/Fine-tuning Link", "Integration with fine-tuning pipelines"),
    ], [
        "{name} prompt versioning template management",
        "{name} experiment tracking A/B test comparison",
        "{name} dataset versioning continuous eval fine-tuning",
    ]),
    CategoryDef("DevEx / Integration", "개발자 경험/통합", [
        ("SDK Support", "Official SDKs for Python, JS/TS, etc."),
        ("Framework Integration", "Built-in support for LangChain, LlamaIndex, etc."),
        ("Custom Model Support", "Tracing for non-standard or self-hosted models"),
        ("API Access", "REST or GraphQL API for programmatic access"),
        ("Streaming Tracing", "Tracing of streaming LLM responses"),
        ("CLI/Infra Integration", "CLI tools and infrastructure-as-code support"),
    ], [
        "{name} Python SDK JavaScript TypeScript integration",
        "{name} LangChain LlamaIndex OpenAI framework support",
        "{name} REST API streaming tracing custom model",
    ]),
    CategoryDef("Security & Governance", "보안 & 거버넌스", [
        ("On-prem/VPC", "Self-hosted or VPC deployment option"),
        ("RBAC", "Role-based access control"),
        ("PII Masking", "Automatic PII detection and redaction"),
        ("Audit Logs", "Audit trail for user and system actions"),
        ("Data Retention", "Configurable data retention policies"),
        ("Region Support", "Multi-region or data residency support"),
    ], [
        "{name} self-hosted VPC on-premise deployment",
        "{name} RBAC PII masking audit logs",
        "{name} data retention region support compliance",
    ]),
]

# Section 2 summary table dimensions
SUMMARY_DIMENSIONS = ["Trace Depth", "Eval", "Agent Observability", "Cost Tracking", "Security & Governance", "Overall"]
