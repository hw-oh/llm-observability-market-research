from __future__ import annotations

from dataclasses import dataclass

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
]

COMPARISON_AXES = [
    "트레이싱/옵저버빌리티",
    "평가 파이프라인",
    "데이터셋 관리",
    "프롬프트 관리",
    "스코어링",
    "LLM/프레임워크 통합",
    "가격",
    "셀프호스팅",
]
