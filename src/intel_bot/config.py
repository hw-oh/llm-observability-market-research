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
    CategoryDef("Core Tracing & Logging", "핵심 트레이싱 & 로깅", [
        ("Nested Span Tracing", "Nested function/LLM call span tracing with parent-child relationships"),
        ("Auto-Instrumentation", "One-line automatic trace collection (decorators, autolog, etc.)"),
        ("Prompt & Response Logging", "Automatic capture of LLM input prompts and output responses"),
        ("Token Usage Tracking", "Input/output/cached/reasoning token usage tracking"),
        ("Latency Measurement", "Per-span and end-to-end latency measurement"),
        ("Cost Estimation", "Automatic cost estimation based on token usage"),
        ("Streaming Trace", "Real-time tracing of streaming LLM responses"),
        ("Metadata & Tags", "Custom metadata and tag attachment on traces"),
        ("OpenTelemetry Compatibility", "OTEL-standard trace export/import support"),
    ], [
        "{name} tracing nested spans auto-instrumentation",
        "{name} prompt response logging token cost tracking",
        "{name} streaming trace OpenTelemetry metadata tags",
    ]),
    CategoryDef("Agent & RAG Observability", "에이전트 & RAG 옵저버빌리티", [
        ("Tool/Function Call Tracing", "Automatic tracing of agent tool call inputs and outputs"),
        ("Retrieval (RAG) Tracing", "Logging of retriever queries and returned documents"),
        ("Multi-step Reasoning Trace", "Visualization of multi-turn agent reasoning chains"),
        ("Workflow Graph View", "DAG/graph visualization of agent workflows"),
        ("MCP/A2A Protocol Tracing", "Model Context Protocol and Agent2Agent protocol trace support"),
        ("Failed Step Highlighting", "Automatic highlighting of failed steps in traces"),
        ("Session/Conversation Grouping", "Grouping traces by session or conversation"),
    ], [
        "{name} agent tool call tracing function calls",
        "{name} RAG retrieval tracing MCP A2A protocol",
        "{name} workflow graph session grouping failed step",
    ]),
    CategoryDef("Evaluation & Quality", "평가 & 품질", [
        ("LLM-as-Judge", "Built-in LLM-based automatic evaluation scoring"),
        ("Custom Eval Scorers", "User-defined evaluation function authoring and execution"),
        ("Human Feedback / Annotation UI", "UI-based human evaluation, annotation, and labeling"),
        ("Evaluation Dataset Management", "Evaluation dataset creation, versioning, and storage"),
        ("Trace → Eval Dataset", "Direct conversion of production traces to evaluation datasets"),
        ("Regression Detection", "Automatic quality regression detection on model/prompt changes"),
        ("Side-by-side Model Comparison", "Side-by-side comparison of model/prompt outputs"),
        ("Evaluation Leaderboard", "Ranking of multiple model/prompt evaluation results"),
        ("CI/CD Eval Integration", "Evaluation embedded in CI/CD pipelines (GitHub Actions, etc.)"),
        ("Online Evaluation (Monitors)", "Real-time automatic evaluation on production traces"),
    ], [
        "{name} LLM judge evaluation scoring custom scorers",
        "{name} human feedback annotation regression detection",
        "{name} eval CI/CD pipeline online evaluation leaderboard",
    ]),
    CategoryDef("Guardrails & Safety", "가드레일 & 안전", [
        ("Built-in Guardrails", "Built-in guardrails (toxicity, PII, hallucination, etc.)"),
        ("Custom Guardrails", "User-defined guardrail scorer authoring"),
        ("Pre/Post Response Hooks", "Safety check hooks before/after LLM responses"),
        ("PII Detection & Masking", "Automatic PII detection and masking"),
    ], [
        "{name} guardrails safety toxicity hallucination detection",
        "{name} PII masking redaction custom guardrail",
        "{name} pre post response hooks content filtering",
    ]),
    CategoryDef("Monitoring & Analytics", "모니터링 & 분석", [
        ("Cost Dashboard", "Real-time LLM cost tracking dashboard"),
        ("Token Usage Analytics", "Token usage breakdown and trends"),
        ("Latency Percentiles & Alerting", "Latency percentile monitoring and alerting"),
        ("Error Rate Monitoring", "Error rate monitoring and alerting"),
        ("Custom Metrics", "User-defined custom metric tracking"),
        ("Drift Detection", "Model input/output distribution drift detection"),
        ("Embedding Clustering/Analysis", "Embedding space clustering and visualization analysis"),
    ], [
        "{name} cost dashboard token analytics monitoring",
        "{name} latency alerting error rate drift detection",
        "{name} custom metrics embedding clustering analysis",
    ]),
    CategoryDef("Experiment & Improvement Loop", "실험 & 개선 루프", [
        ("Prompt Versioning", "Version control for prompt templates"),
        ("Model Versioning", "Tracking of model versions and configs"),
        ("Experiment Tracking", "A/B test and experiment management"),
        ("Dataset Versioning", "Versioned evaluation and training datasets"),
        ("LLM Playground", "Interactive prompt testing interface"),
        ("Continuous/Scheduled Eval", "Scheduled or trigger-based automatic evaluation runs"),
        ("RL/Fine-tuning Pipeline", "Integration with fine-tuning/RL pipelines"),
        ("Training Data Generation", "Automatic training data generation from traces"),
        ("Failure Trajectory Extraction", "Extraction of failure pattern traces into datasets"),
    ], [
        "{name} prompt versioning experiment tracking playground",
        "{name} dataset versioning continuous eval fine-tuning",
        "{name} training data generation failure trajectory extraction",
    ]),
    CategoryDef("Developer Experience & Integration", "개발자 경험 & 통합", [
        ("Python SDK", "Official Python SDK"),
        ("TypeScript/JS SDK", "Official TypeScript/JavaScript SDK"),
        ("Framework Integration", "Built-in support for LangChain, LlamaIndex, DSPy, CrewAI, etc."),
        ("REST/GraphQL API", "REST or GraphQL API for programmatic access"),
        ("Custom Model Support", "Tracing for non-standard or self-hosted models"),
        ("CLI Tools", "Command-line interface tools"),
        ("Notebook Integration", "Trace visualization within Jupyter/Colab notebooks"),
    ], [
        "{name} Python SDK TypeScript JavaScript integration",
        "{name} LangChain LlamaIndex DSPy CrewAI framework",
        "{name} REST API CLI notebook Jupyter custom model",
    ]),
    CategoryDef("Infrastructure & Enterprise", "인프라 & 엔터프라이즈", [
        ("Cloud Managed (SaaS)", "Managed cloud service offering"),
        ("Self-Host / On-Prem", "Self-hosted or on-premise deployment option"),
        ("VPC Deployment", "Deployment within customer VPC"),
        ("Open Source", "Open-source code availability"),
        ("RBAC", "Role-based access control"),
        ("SSO/SAML", "SSO and SAML authentication support"),
        ("SOC 2 Certification", "SOC 2 Type II security certification"),
        ("Audit Logs", "User and system action audit trail"),
        ("Data Retention Policy", "Configurable data retention policies"),
        ("Data Warehouse Export", "Export to external data warehouses"),
        ("Multi-Region / Data Residency", "Multi-region or data residency support"),
        ("Traditional ML Experiment Integration", "Integration with traditional ML experiment tracking (W&B, MLflow, etc.)"),
        ("Databricks Native Integration", "Databricks platform native integration"),
    ], [
        "{name} self-hosted VPC on-premise open source deployment",
        "{name} RBAC SSO SAML SOC2 audit logs compliance",
        "{name} data retention warehouse export multi-region Databricks",
    ]),
]

# Section 2 summary table dimensions
SUMMARY_DIMENSIONS = ["Tracing", "Eval", "Agent Observability", "Cost Tracking", "Enterprise", "Overall"]
