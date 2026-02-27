from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    perplexity_api_key: SecretStr
    openrouter_api_key: SecretStr
    openrouter_model: str = "google/gemini-3.1-pro-preview"
    url_reference_model: str = "google/gemini-3-flash-preview"
    translation_model: str = "google/gemini-3-flash-preview"
    perplexity_model: str = "sonar"
    slack_webhook_url: SecretStr | None = None


SUPPORTED_LANGS = ["ko", "ja"]
LANGUAGE_NAMES = {"ko": "Korean", "ja": "Japanese"}


@dataclass
class CompetitorConfig:
    name: str
    docs_url: str
    changelog_url: str | None        # 수집용 (RSS/HTML)
    changelog_display_url: str | None = None  # 사람용 (브라우저 링크). None이면 changelog_url 사용
    reference_urls: list[str] = field(default_factory=list)
    product_description: str = ""
    product_context: str = ""
    changelog_filter_hint: str = ""
    changelog_include_tags: list[str] = field(default_factory=list)
    enabled: bool = True

    @property
    def changelog_link(self) -> str | None:
        """리포트에 표시할 changelog URL."""
        return self.changelog_display_url or self.changelog_url


COMPETITORS: list[CompetitorConfig] = [
    CompetitorConfig(
        name="LangSmith",
        enabled=True,
        docs_url="https://docs.smith.langchain.com",
        changelog_url="https://changelog.langchain.com",
        changelog_display_url="https://changelog.langchain.com",
        reference_urls=[
            "https://docs.smith.langchain.com/observability",
            "https://docs.smith.langchain.com/evaluation",
            "https://docs.smith.langchain.com/administration",
        ],
    ),
    CompetitorConfig(
        name="Langfuse",
        enabled=True,
        docs_url="https://langfuse.com/docs",
        changelog_url="https://langfuse.com/changelog",
        reference_urls=[
            "https://langfuse.com/docs/tracing",
            "https://langfuse.com/docs/scores/overview",
            "https://langfuse.com/docs/security/overview",
        ],
    ),
    CompetitorConfig(
        name="Braintrust",
        enabled=True,
        docs_url="https://braintrust.dev/docs",
        changelog_url="https://braintrust.dev/docs/changelog",
        reference_urls=[
            "https://braintrust.dev/docs/guides/tracing",
            "https://braintrust.dev/docs/guides/evals",
        ],
    ),
    CompetitorConfig(
        name="MLflow",
        enabled=True,
        docs_url="https://mlflow.org/docs/latest/genai",
        changelog_url="https://mlflow.org/releases",
        changelog_filter_hint=(
            "MLflow's LLM observability product is called 'MLflow GenAI' (mlflow.genai). "
            "The changelog covers ALL of MLflow (tracking, models, recipes, etc.). "
            "ONLY extract updates related to GenAI/LLM observability features: "
            "tracing, evaluation, scoring, prompt engineering, LLM deployment, "
            "and the mlflow.genai module. Ignore MLflow Tracking, MLflow Models, "
            "MLflow Recipes, and other non-GenAI features."
        ),
        reference_urls=[
            "https://mlflow.org/docs/latest/genai/tracing/index.html",
            "https://mlflow.org/docs/latest/genai/eval/index.html",
        ],
    ),
    CompetitorConfig(
        name="Arize Phoenix",
        enabled=True,
        docs_url="https://docs.arize.com/phoenix",
        changelog_url="https://arize.com/docs/phoenix/release-notes",
        reference_urls=[
            "https://docs.arize.com/phoenix/tracing/overview",
            "https://docs.arize.com/phoenix/evaluation/overview",
        ],
    ),
]

WEAVE_CONFIG = CompetitorConfig(
    name="W&B Weave",
    enabled=True,
    docs_url="https://weave-docs.wandb.ai",
    changelog_url="https://app.getbeamer.com/wandb/en",
    changelog_include_tags=["WEAVE"],
    changelog_filter_hint=(
        "The W&B (Weights & Biases) changelog covers ALL W&B products: "
        "Weave (LLM observability), Models (experiment tracking, model registry), "
        "and platform features. ONLY extract updates related to Weave / LLM "
        "observability: tracing, evaluations, scorers, prompts, guardrails, "
        "datasets, playground, and LLM-specific features. Ignore updates about "
        "W&B Models, Experiments, Artifacts, Sweeps, Launch, and other non-Weave features "
        "unless they directly impact the Weave observability workflow."
    ),
    product_description=(
        "W&B Weave is the LLM observability product within the Weights & Biases (W&B) platform. "
        "It inherits ALL W&B platform-level enterprise features including RBAC (Administrator/"
        "Member/Viewer/Custom roles), SSO/SAML, audit logs, VPC/dedicated cloud deployment, "
        "SOC 2 Type II / HIPAA / GDPR compliance, configurable data retention, and multi-region support."
    ),
    product_context="""\
=== Authoritative Product Information (Internal) ===
This is verified internal data about W&B Weave. Use this to validate and correct category analysis ratings.

ENTERPRISE & INFRASTRUCTURE:
- SOC 2 Type II: Yes
- HIPAA: Yes
- GDPR: Yes (Privacy Policy + Data Processing Addendum)
- RBAC: Yes — Administrator, Member, Viewer, Custom roles (inherited from W&B platform)
- Deployment: Multi-tenant SaaS, Dedicated SaaS (single-tenant), Self-hosted (customer managed)
- Org structure: Organization > Team > Projects with scoped permissions
- Registry for artifacts (models, datasets) with versioning, aliases, lineage tracking — available to Weave+Models customers but integration is not yet seamless

TRACING:
- Full request/response tracing: Yes
- Multimodal: Yes — text, images, audio, video
- OpenTelemetry: Yes — provides OTel endpoint for recording traces
- MCP Integration: Yes — traces MCP client/server tool calls, resource access, prompt generation

EVALUATION:
- Offline evaluations: Yes (prompt + dataset + scorer), also available in Evaluations Playground UI
- Online evaluations: Yes — LLM judges on production traces with filtering and random sampling, run on W&B infrastructure
- Imperative Evaluations API: Yes
- LLM-as-a-Judge Wizard: Yes — GUI-based judge builder, added 12/2024
- Custom scorers: Yes in Python, TypeScript coming soon
- Pre-built scoring functions: Yes

HUMAN FEEDBACK:
- Human annotation: Yes — custom question forms, scores stored with scorer results
- Annotation queues: PARTIAL — annotation available but NO built-in queue management for grouping/assigning traces to reviewers
- LLM Leaderboards: Yes (based on evaluation results)

GUARDRAILS:
- Yes — prompt injection prevention, data leakage prevention, hallucination mitigation, off-topic blocking, toxicity/harmful content blocking

AGENTS:
- Agent/agentic workflow evaluation: Yes
- Native first-class agent support: Coming soon — no native agent treatment like LangGraph/LangSmith yet
- Trace tree enhancements offer greater visibility into agentic workflows

OBJECTS & PLAYGROUND:
- Prompts: Yes (created programmatically, dedicated UI section)
- Datasets: Yes (versioned)
- Models/Applications: Yes
- Prompt Playground: Yes
- Evaluations Playground: Yes

SDK & INTEGRATIONS:
- Languages: Python + TypeScript
- Framework integrations: LangChain, LlamaIndex
- Supported LLMs: All relevant LLMs
- CI/CD: Via W&B Automations/Registry (artifact-triggered workflows)

FINE-TUNING:
- Building and fine-tuning LLMs is part of W&B Experiments (platform-level feature)
=== End of Product Information ===""",
    reference_urls=[
        "https://docs.wandb.ai/weave/guides/tracking/redact-pii",
        "https://docs.wandb.ai/platform/hosting",
        "https://docs.wandb.ai/platform/access-management",
        "https://docs.wandb.ai/platform/hosting/monitoring-usage/audit-logging",
        "https://docs.wandb.ai/platform/hosting/data-retention",
    ],
)

@dataclass
class CategoryDef:
    name: str          # English name (LLM schema key)
    name_ko: str       # Korean name (report display)
    items: list[tuple[str, str]] = field(default_factory=list)  # (name, description)


COMPARISON_CATEGORIES: list[CategoryDef] = [
    CategoryDef("Core Tracing & Logging", "핵심 트레이싱 & 로깅", [
        ("Full Request/Response Tracing", "Complete capture of LLM input prompts, output responses, and parameters"),
        ("Nested Span & Tree View", "Hierarchical span tracing with parent-child tree visualization"),
        ("Streaming Support", "Real-time tracing of streaming LLM responses"),
        ("Multimodal Tracing", "Tracing and rendering of image, audio, and other non-text inputs/outputs"),
        ("Auto-Instrumentation", "One-line automatic trace collection (decorators, autolog, etc.)"),
        ("Metadata & Tags Filtering", "Custom metadata and tag attachment with search and filtering"),
        ("Token Counting & Estimation", "Accurate per-tokenizer input/output/cached token counting"),
        ("OpenTelemetry Standard", "OTEL-standard trace export/import compatibility"),
    ]),
    CategoryDef("Agent & RAG Specifics", "에이전트 & RAG 심화", [
        ("RAG Retrieval Visualizer", "UI display of retrieved document chunks with content and relevance scores"),
        ("Tool/Function Call Rendering", "Parsed view of tool/function call inputs and return values"),
        ("Agent Execution Graph", "DAG/graph visualization of agent workflows with loops and branches"),
        ("Intermediate Step State", "Storage and display of agent intermediate reasoning (Chain-of-Thought)"),
        ("Session/Thread Replay", "Replay of user session or conversation thread as a complete flow"),
        ("Failed Step Highlighting", "Automatic highlighting of failed steps in agent traces"),
        ("MCP Integration", "Model Context Protocol server/client integration and tracing"),
    ]),
    CategoryDef("Evaluation & Quality", "평가 & 품질", [
        ("LLM-as-a-Judge Wizard", "GUI-based LLM judge builder without requiring code"),
        ("Custom Eval Scorers", "User-defined code-based evaluation function authoring and execution"),
        ("Dataset Management & Curation", "Evaluation dataset creation, versioning, and trace-to-dataset conversion"),
        ("Prompt Optimization / DSPy Support", "Automatic prompt optimization or candidate suggestion (e.g. DSPy integration)"),
        ("Regression Testing", "Automatic quality regression detection on model/prompt changes"),
        ("Comparison View (Side-by-side)", "Side-by-side comparison of model/prompt outputs"),
        ("Annotation Queues", "Team-based annotation workflows with queue management and reviewer assignment"),
        ("Online Evaluation", "Real-time automatic evaluation on live production traffic"),
    ]),
    CategoryDef("Guardrails & Safety", "가드레일 & 안전", [
        ("PII/Sensitive Data Masking", "Automatic PII and sensitive data detection and masking"),
        ("Hallucination Detection", "Dedicated guardrail for detecting hallucinated content"),
        ("Topic/Jailbreak Guardrails", "Blocking of forbidden topics and jailbreak attempt detection"),
        ("Policy Management as Code", "Guardrail rules defined and managed as code"),
    ]),
    CategoryDef("Analytics & Dashboard", "분석 & 대시보드", [
        ("Cost Analysis & Attribution", "Cost tracking with per-user/team/project attribution"),
        ("Token Usage Analytics", "Input/output token usage breakdown and trends"),
        ("Latency Heatmap & P99", "Latency distribution visualization with percentile monitoring"),
        ("Error Rate Monitoring", "Error rate tracking and alerting"),
        ("Embedding Space Visualization", "UMAP/t-SNE embedding clustering and visualization"),
        ("Custom Metrics & Dashboard", "User-defined custom metric tracking with dashboard widgets"),
    ]),
    CategoryDef("Development Lifecycle", "개발 라이프사이클", [
        ("Prompt Management (CMS)", "Prompt versioning with non-developer editing and deployment capabilities"),
        ("Playground & Sandbox", "Interactive prompt and parameter testing environment"),
        ("Experiment Tracking", "A/B test and experiment management with hyperparameter logging"),
        ("Fine-tuning Integration", "Fine-tuning data export and pipeline integration"),
        ("Version Control & Rollback", "Prompt and model version management with rollback capability"),
    ]),
    CategoryDef("Integration & DX", "통합 & 개발 편의성", [
        ("SDK Support (Py/JS/Go)", "Official SDK support across Python, JavaScript/TypeScript, and Go"),
        ("Gateway/Proxy Mode", "Proxy-based tracing without SDK installation (URL change only)"),
        ("Popular Frameworks", "Built-in support for LangChain, LlamaIndex, AutoGen, CrewAI, etc."),
        ("API & Webhooks", "REST/GraphQL API and webhook integration for external systems"),
        ("CI/CD Integration", "Integration with CI/CD pipelines (GitHub Actions, etc.) for automated eval and deployment"),
    ]),
    CategoryDef("Enterprise & Infrastructure", "엔터프라이즈 & 인프라", [
        ("Deployment Options", "Multi-tenant SaaS, dedicated SaaS, and self-hosted/VPC deployment options"),
        ("Open Source", "Open-source code availability and community"),
        ("Data Sovereignty & Compliance", "Data region selection with SOC 2/HIPAA/GDPR compliance"),
        ("RBAC & SSO", "Role-based access control with SSO/SAML authentication"),
        ("Audit Logs", "User and system action audit trail"),
        ("Data Warehouse Export", "Automated export to Snowflake, BigQuery, S3, etc."),
    ]),
]


def get_active_products() -> list[CompetitorConfig]:
    """Return enabled products: WEAVE_CONFIG first, then enabled COMPETITORS."""
    products = []
    if WEAVE_CONFIG.enabled:
        products.append(WEAVE_CONFIG)
    products.extend(c for c in COMPETITORS if c.enabled)
    return products


def get_all_products() -> list[CompetitorConfig]:
    """Return ALL products regardless of enabled flag (for baseline generation)."""
    return [WEAVE_CONFIG, *COMPETITORS]
