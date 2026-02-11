from __future__ import annotations

from dataclasses import dataclass, field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    serper_dev_api: str
    openrouter_api_key: str
    openrouter_model: str = "google/gemini-3-pro-preview"
    slack_webhook_url: str | None = None


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
    items: list[str] = field(default_factory=list)  # Sub-items (Korean)


COMPARISON_CATEGORIES: list[CategoryDef] = [
    CategoryDef("Core Observability", "핵심 옵저버빌리티",
        ["Trace 깊이", "계층적 스팬", "프롬프트 로깅", "응답 로깅", "토큰 추적", "레이턴시 분석", "리플레이"]),
    CategoryDef("Agent / RAG Observability", "에이전트/RAG 옵저버빌리티",
        ["도구 호출 추적", "검색(Retrieval) 추적", "메모리 추적", "다단계 추론", "워크플로우 그래프", "실패 시각화"]),
    CategoryDef("Evaluation Integration", "평가 통합",
        ["Trace→데이터셋 생성", "LLM-as-Judge", "커스텀 평가 메트릭", "회귀 감지", "모델 비교", "휴먼 피드백 UI"]),
    CategoryDef("Monitoring & Metrics", "모니터링 & 메트릭",
        ["비용 대시보드", "토큰 분석", "레이턴시 모니터링", "에러 추적", "도구 성공률", "커스텀 메트릭"]),
    CategoryDef("Experiment / Improvement Loop", "실험/개선 루프",
        ["프롬프트 버전 관리", "모델 버전 관리", "실험 추적", "데이터셋 버전 관리", "지속적 평가", "RL/파인튜닝 연결"]),
    CategoryDef("DevEx / Integration", "개발자 경험/통합",
        ["SDK 지원", "프레임워크 통합", "커스텀 모델 지원", "API 제공", "스트리밍 추적", "CLI/인프라 통합"]),
    CategoryDef("Enterprise & Security", "엔터프라이즈 & 보안",
        ["온프레미스/VPC", "RBAC", "PII 마스킹", "감사 로그", "데이터 보존", "리전 지원"]),
]

# Weekly report Section 4: 5 categories for deep tracking (other 2 in comparison table only)
WEEKLY_REPORT_DEEP_CATEGORIES = [
    "Core Observability",
    "Agent / RAG Observability",
    "Evaluation Integration",
    "Monitoring & Metrics",
    "Enterprise & Security",
]

# Section 2 summary table dimensions
SUMMARY_DIMENSIONS = ["Trace Depth", "Eval", "Agent Observability", "Cost Tracking", "Enterprise Ready", "Overall"]
