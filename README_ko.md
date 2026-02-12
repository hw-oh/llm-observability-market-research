# LLM Observability Market Research

[English](./README.md)

W&B Weave의 경쟁사 제품을 주기적으로 조사하여 기능 비교 리포트를 자동 생성하는 봇.

## 리포트 생성 워크플로우

```
python -m intel_bot run
```

하나의 명령으로 아래 6단계 파이프라인이 순차 실행됩니다.

### Step 1. Collect (데이터 수집)

각 경쟁사 + Weave에 대해 피드와 추가 문서를 수집합니다. Changelog와 릴리스 피드가 주요 데이터 소스입니다.

| 소스 | 모듈 | 수집 내용 |
|------|------|----------|
| Changelog | `collectors/docs_scraper.py` / `feed.py` | 릴리스 노트 — 신기능, 버전 이력 (HTML 또는 RSS) |
| GitHub/PyPI | `collectors/feed.py` | Release 태그 및 패키지 버전 |
| 추가 문서 | `collectors/docs_scraper.py` | 추가 문서 페이지 (예: Weave enterprise docs) |
| Beamer | `collectors/beamer.py` | Weave 전용 — W&B changelog (Beamer API) |

경쟁사별 docs/changelog URL은 `config.py`에 설정되어 있습니다. 수집 결과는 `data/collections/YYYY-MM-DD.json`에 저장됩니다.

### Step 2. Discover (신규 경쟁사 탐색)

웹 검색(Serper)으로 아직 추적하지 않는 신규 LLM observability 제품을 탐색합니다.
LLM이 검색 결과에서 emerging competitor를 추출합니다. 실패해도 파이프라인은 계속 진행됩니다.

### Step 3. Analyze — 카테고리별 분석 (Perplexity Sonar)

Perplexity Sonar가 카테고리별로 웹 검색 + 분석을 한 번에 수행합니다. 제품당 8개 카테고리, 총 6개 제품 (경쟁사 5 + Weave).

```
6개 제품 × 8 카테고리 × Sonar 1회 = 48회
```

출력: 카테고리별 rating과 요약 (웹 citation 포함)

### Step 4. Analyze — 제품별 종합 분석 (Gemini Pro)

제품당 Gemini Pro 호출 1회로 8개 카테고리 결과 + 피드 데이터를 종합 분석합니다.

```
6개 제품 × Pro 1회 = 6회
```

출력: 전체 요약, 카테고리 rating, 신기능, 강점/약점, 포지셔닝

### Step 5. Analyze — 종합 분석 + Executive Summary (Gemini Pro)

Pro 호출 2회 추가: 전체 제품 분석을 시장 landscape로 종합 + VP/Engineering 리더십 대상 executive summary 생성.

출력: vendor 비교, enterprise signals, 5-7개 핵심 인사이트, market insights

### Step 6. Report & Translate (리포트 생성 + 번역)

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
┌──────────────────────────────────────────────────────────┐
│  python -m intel_bot run                                 │
│                                                          │
│  ┌───────────┐  ┌──────────┐  ┌───────────────────────┐ │
│  │ 1. Collect │─▶│2. Discover│─▶│ 3. 카테고리 분석     │ │
│  │           │  │          │  │   Sonar ×48           │ │
│  │ feeds     │  │ Serper + │  │   (검색 + 분석)       │ │
│  │ docs      │  │ LLM call │  └──────────┬────────────┘ │
│  │ beamer    │  └──────────┘             │              │
│  └───────────┘                           ▼              │
│                               ┌───────────────────────┐ │
│                               │ 4. 제품별 종합 분석   │ │
│                               │   Pro ×6              │ │
│                               └──────────┬────────────┘ │
│                                          │              │
│                                          ▼              │
│                               ┌───────────────────────┐ │
│                               │ 5. 종합 + Exec Summary│ │
│                               │   Pro ×2              │ │
│                               └──────────┬────────────┘ │
│                                          │              │
│                                          ▼              │
│                               ┌───────────────────────┐ │
│                               │ 6. 리포트 + 번역      │ │
│                               │   LLM ×8 (번역)       │ │
│                               └───────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

## 경쟁사 목록

| 제품 | Docs | Changelog |
|------|------|-----------|
| LangSmith | [docs.smith.langchain.com](https://docs.smith.langchain.com) | [changelog.langchain.com](https://changelog.langchain.com) |
| Langfuse | [langfuse.com/docs](https://langfuse.com/docs) | [langfuse.com/changelog](https://langfuse.com/changelog) |
| Braintrust | [braintrust.dev/docs](https://braintrust.dev/docs) | [braintrust.dev/docs/changelog](https://braintrust.dev/docs/changelog) |
| MLflow | [mlflow.org/docs/latest/genai](https://mlflow.org/docs/latest/genai) | [mlflow.org/releases](https://mlflow.org/releases) |
| Arize Phoenix | [docs.arize.com/phoenix](https://docs.arize.com/phoenix) | [arize.com/docs/phoenix/release-notes](https://arize.com/docs/phoenix/release-notes) |

## 8-Category 분석 프레임워크

1. **Core Tracing & Logging** — Nested Spans, Auto-Instrumentation, Prompt/Response Logging, Token Usage, Latency, Cost Estimation, Streaming, Metadata, OpenTelemetry
2. **Agent & RAG Observability** — Tool Call Tracing, Retrieval Tracing, Multi-step Reasoning, Workflow Graph, MCP/A2A Protocol, Failed Step Highlighting, Session Grouping
3. **Evaluation & Quality** — LLM-as-Judge, Custom Scorers, Human Feedback, Dataset Management, Trace-to-Eval, Regression Detection, Model Comparison, Leaderboard, CI/CD Eval, Online Evaluation
4. **Guardrails & Safety** — Built-in Guardrails, Custom Guardrails, Pre/Post Hooks, PII Detection & Masking
5. **Monitoring & Analytics** — Cost Dashboard, Token Analytics, Latency Alerting, Error Rate, Custom Metrics, Drift Detection, Embedding Analysis
6. **Experiment & Improvement Loop** — Prompt/Model/Dataset Versioning, Experiment Tracking, Playground, Continuous Eval, RL/Fine-tuning, Training Data Generation, Failure Trajectory Extraction
7. **Developer Experience & Integration** — Python/TypeScript SDK, Framework Integration, REST/GraphQL API, Custom Model Support, CLI, Notebook Integration
8. **Infrastructure & Enterprise** — SaaS, Self-Host, VPC, Open Source, RBAC, SSO/SAML, SOC 2, Audit Logs, Data Retention, Data Warehouse Export, Multi-Region, ML Experiment Integration, Databricks

## 설치

```bash
pip install -e .
```

### 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `PERPLEXITY_API_KEY` | Yes | Perplexity Sonar API key (웹 검색 + 카테고리 분석) |
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key (Gemini Pro 종합 분석) |
| `SERPER_DEV_API` | No | Serper.dev API key (신규 경쟁사 탐색에만 사용) |
| `SLACK_WEBHOOK_URL` | No | Slack 알림 webhook |
| `WANDB_API_KEY` | No | W&B Weave tracing |

### CLI 명령어

```bash
python -m intel_bot collect    # 데이터 수집만
python -m intel_bot discover   # 신규 경쟁사 탐색만
python -m intel_bot analyze    # 분석만 (수집 데이터 필요)
python -m intel_bot report     # 리포트 생성만 (분석 데이터 필요)
python -m intel_bot run        # 전체 파이프라인
python -m intel_bot preview    # 분석 + 한국어 프리뷰 (기존 수집 데이터 사용)
```

## CI/CD

GitHub Actions (`weekly-report.yml`)가 매주 월요일 09:00 UTC에 자동 실행됩니다.
수동 실행: Actions → Weekly Competitor Report → Run workflow

생성된 리포트는 GitHub Pages로 자동 배포됩니다.
