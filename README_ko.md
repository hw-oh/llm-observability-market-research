# LLM Observability Market Research

[English](./README.md)

W&B Weave의 경쟁사 제품을 주기적으로 조사하여 기능 비교 리포트를 자동 생성하는 봇.

## 리포트 생성 워크플로우

```
python -m intel_bot run
```

하나의 명령으로 아래 파이프라인이 순차 실행됩니다.

### Step 1. Collect (데이터 수집)

각 제품에 대해 피드와 참고 URL 문서를 수집합니다.

| 소스 | 모듈 | 수집 내용 |
|------|------|----------|
| Changelog | `collectors/feed.py` | 릴리스 노트 (RSS) |
| GitHub/PyPI | `collectors/feed.py` | Release 태그 및 패키지 버전 |
| 참고 URL | `collectors/docs_scraper.py` | `config.py`의 `reference_urls`에 설정된 문서 |
| Beamer | `collectors/beamer.py` | Weave 전용 — W&B changelog |

경쟁사별 참고 URL은 `config.py`의 `reference_urls` 필드에 설정합니다.

### Step 2. Discover (신규 경쟁사 탐색, 선택)

Serper 웹 검색으로 신규 LLM observability 제품을 탐색합니다. 실패해도 파이프라인은 계속 진행됩니다.

### Step 3. Analyze — crewAI 멀티 에이전트

제품별로 3개 에이전트가 협력하여 구조화된 분석 결과를 생성합니다.

| 에이전트 | 모델 | 역할 |
|----------|------|------|
| **SearchAgent** | Perplexity Sonar | 웹 검색 기반 근거 수집 |
| **UrlReferenceAgent** | Gemini Flash | 참고 URL 문서에서 근거 추출 |
| **ExtractionAgent** | Gemini Pro | 양쪽 근거를 병합하여 구조화된 분석 생성 |

제품별 분석 후, **ReportSynthesisAgent**(Gemini Pro)가 전체 제품을 종합하여 시장 분석 + Executive Summary를 생성합니다.

### Step 4. Report & Translate (리포트 생성 + 번역)

분석 결과를 Markdown 파일로 렌더링하고, 한국어/일본어로 번역합니다.

| 파일 | 내용 |
|------|------|
| `index.md` | 홈 — Executive Summary + Report Archive |
| `comparison.md` | 8개 카테고리 상세 비교표 |
| `competitor-detail.md` | 제품별 상세 분석 |
| `reports/YYYY-MM-DD.md` | 주간 리포트 전문 |
| `ko/`, `ja/` | 번역본 |

## 파이프라인 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│  python -m intel_bot run                                    │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────────────┐│
│  │1. Collect │─▶│2. Discover│─▶│ 3. Analyze (crewAI)       ││
│  │ feeds     │  │ (선택)    │  │                            ││
│  │ ref URLs  │  │ Serper +  │  │  제품별:                   ││
│  │ beamer    │  │ LLM       │  │  SearchAgent ─┐            ││
│  └──────────┘  └──────────┘  │                ├▶ Extraction ││
│                               │  UrlRefAgent ─┘            ││
│                               │                            ││
│                               │  전체: ReportSynthesis     ││
│                               └──────────┬─────────────────┘│
│                                          │                  │
│                                          ▼                  │
│                               ┌────────────────────────────┐│
│                               │ 4. Report + 번역           ││
│                               │    + 옵션 플러그인          ││
│                               │    (Slack, W&B Report)     ││
│                               └────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 제품별 참고 URL 설정

`config.py`의 `CompetitorConfig.reference_urls`에 URL 리스트를 설정합니다:

```python
CompetitorConfig(
    name="LangSmith",
    docs_url="https://docs.smith.langchain.com",
    changelog_url="https://changelog.langchain.com/feed.rss",
    reference_urls=[
        "https://docs.smith.langchain.com/observability",
        "https://docs.smith.langchain.com/evaluation",
        "https://docs.smith.langchain.com/administration",
    ],
    ...
)
```

수집 단계에서 이 URL들을 스크래핑하고, 분석 시 UrlReferenceAgent의 입력으로 사용됩니다.

## 경쟁사 목록

| 제품 | Docs | Changelog |
|------|------|-----------|
| LangSmith | [docs.smith.langchain.com](https://docs.smith.langchain.com) | [changelog.langchain.com](https://changelog.langchain.com) |
| Langfuse | [langfuse.com/docs](https://langfuse.com/docs) | [langfuse.com/changelog](https://langfuse.com/changelog) |
| Braintrust | [braintrust.dev/docs](https://braintrust.dev/docs) | [braintrust.dev/docs/changelog](https://braintrust.dev/docs/changelog) |
| MLflow | [mlflow.org/docs/latest/genai](https://mlflow.org/docs/latest/genai) | [mlflow.org/releases](https://mlflow.org/releases) |
| Arize Phoenix | [docs.arize.com/phoenix](https://docs.arize.com/phoenix) | [arize.com/docs/phoenix/release-notes](https://arize.com/docs/phoenix/release-notes) |

## 8-Category 분석 프레임워크 (49개 항목)

1. **Core Tracing & Logging** (8) — Full Request/Response Tracing, Nested Span & Tree View, Streaming, Multimodal Tracing, Auto-Instrumentation, Metadata & Tags, Token Counting, OpenTelemetry
2. **Agent & RAG Specifics** (7) — RAG Retrieval Visualizer, Tool/Function Call Rendering, Agent Execution Graph, Intermediate Step State, Session/Thread Replay, Failed Step Highlighting, MCP Integration
3. **Evaluation & Quality** (8) — LLM-as-a-Judge Wizard, Custom Eval Scorers, Dataset Management & Curation, Prompt Optimization/DSPy, Regression Testing, Side-by-side Comparison, Annotation Queues, Online Evaluation
4. **Guardrails & Safety** (4) — PII/Sensitive Data Masking, Hallucination Detection, Topic/Jailbreak Guardrails, Policy Management as Code
5. **Analytics & Dashboard** (6) — Cost Analysis & Attribution, Token Usage Analytics, Latency Heatmap & P99, Error Rate Monitoring, Embedding Space Visualization, Custom Metrics & Dashboard
6. **Development Lifecycle** (5) — Prompt Management (CMS), Playground & Sandbox, Experiment Tracking, Fine-tuning Integration, Version Control & Rollback
7. **Integration & DX** (5) — SDK Support (Py/JS/Go), Gateway/Proxy Mode, Popular Frameworks, API & Webhooks, CI/CD Integration
8. **Enterprise & Infrastructure** (6) — Deployment Options (SaaS/Dedicated/Self-Host), Open Source, Data Sovereignty & Compliance, RBAC & SSO, Audit Logs, Data Warehouse Export

## 설치

```bash
pip install -e .
```

### 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `PERPLEXITY_API_KEY` | Yes | Perplexity Sonar API key (SearchAgent) |
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key (UrlReferenceAgent, ExtractionAgent, 번역) |
| `SERPER_DEV_API` | No | Serper.dev API key (신규 경쟁사 탐색에만 사용) |
| `SLACK_WEBHOOK_URL` | No | Slack 알림 webhook (옵션 플러그인) |
| `WANDB_API_KEY` | No | W&B Weave tracing + W&B Report (옵션 플러그인) |

### CLI 명령어

```bash
python -m intel_bot run        # 전체 파이프라인 (기본)
python -m intel_bot collect    # 데이터 수집만 (디버깅)
python -m intel_bot analyze    # 분석만 (디버깅, 수집 데이터 필요)
python -m intel_bot report     # 리포트 생성만 (디버깅, 분석 데이터 필요)
python -m intel_bot discover   # 신규 경쟁사 탐색만 (디버깅)
```

## 옵션 플러그인

다음 기능은 해당 환경 변수가 설정된 경우에만 실행됩니다. 실패해도 핵심 파이프라인은 중단되지 않습니다.

- **Slack 알림**: `SLACK_WEBHOOK_URL` 설정 시 리포트 완료 알림
- **W&B Report**: `WANDB_API_KEY` 설정 시 W&B Report 발행 + Alert

## CI/CD

GitHub Actions (`weekly-report.yml`)가 매주 월요일 09:00 UTC에 자동 실행됩니다.
수동 실행: Actions → Weekly Competitor Report → Run workflow

생성된 리포트는 GitHub Pages로 자동 배포됩니다.
