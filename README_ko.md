# Competitor Intel Bot

[English](./README.md)

W&B Weave의 경쟁사 제품을 주기적으로 조사하여 기능 비교 리포트를 자동 생성하는 봇.

## 리포트 생성 워크플로우

```
python -m intel_bot run
```

하나의 명령으로 아래 6단계 파이프라인이 순차 실행됩니다.

### Step 1. Collect (데이터 수집)

각 경쟁사 + Weave에 대해 여러 소스에서 데이터를 수집합니다. 공식 문서와 changelog가 기능 정확도의 1차 소스이며, 웹 검색은 시장 컨텍스트를 보충합니다.

| 소스 | 모듈 | 수집 내용 |
|------|------|----------|
| 공식 문서 | `collectors/docs_scraper.py` | 제품 문서 페이지 — 기능 상세, API 레퍼런스 |
| Changelog | `collectors/docs_scraper.py` / `feed.py` | 릴리스 노트 — 신기능, 버전 이력 (HTML 또는 RSS) |
| 웹 검색 | `collectors/serper.py` | 뉴스, 블로그, 커뮤니티 토론 (Serper.dev API) |
| GitHub/PyPI | `collectors/feed.py` | Release 태그 및 패키지 버전 |
| Beamer | `collectors/beamer.py` | Weave 전용 — W&B changelog (Beamer API) |

경쟁사별 docs/changelog URL은 `config.py`에 설정되어 있습니다. 수집 결과는 `data/collections/YYYY-MM-DD.json`에 저장됩니다.

### Step 2. Discover (신규 경쟁사 탐색)

웹 검색으로 아직 추적하지 않는 신규 LLM observability 제품을 탐색합니다.
LLM이 검색 결과에서 emerging competitor를 추출합니다. 실패해도 파이프라인은 계속 진행됩니다.

### Step 3. Analyze — 개별 분석 (LLM)

경쟁사별로 LLM 호출 1회씩, 7개 카테고리 프레임워크로 분석합니다.

```
경쟁사 5개 × LLM 호출 1회 = 5회
```

출력: 카테고리별 rating, 신기능, 강점/약점, 포지셔닝

### Step 4. Analyze — 종합 분석 (LLM)

5개 개별 분석 결과를 하나로 모아 LLM 호출 1회로 종합합니다.

출력: vendor ratings 비교표, Weave 강점/약점, 포지셔닝, enterprise signals

### Step 5. Analyze — Executive Summary (LLM)

종합 분석 결과를 입력으로 **별도 LLM 호출**로 executive summary를 생성합니다.
전용 프롬프트를 사용하여 VP/Engineering 리더십 대상 브리핑 품질로 작성됩니다.

출력: 5-7개 핵심 인사이트 불릿 + one-line verdict

### Step 6. Report & Translate (리포트 생성 + 번역)

분석 결과를 Markdown 파일로 렌더링하고, 한국어/일본어로 번역합니다.

| 파일 | 내용 |
|------|------|
| `index.md` | 홈 — Executive Summary + Report Archive |
| `comparison.md` | 7개 카테고리 상세 비교표 |
| `competitor-detail.md` | 제품별 상세 분석 |
| `reports/YYYY-MM-DD.md` | 주간 리포트 전문 |
| `ko/`, `ja/` | 번역본 |

## 파이프라인 다이어그램

```
┌─────────────────────────────────────────────────────────┐
│  python -m intel_bot run                                │
│                                                         │
│  ┌───────────┐   ┌──────────┐   ┌────────────────────┐ │
│  │ 1. Collect │──▶│2. Discover│──▶│ 3. Analyze (×5)   │ │
│  │           │   │          │   │   개별 경쟁사 분석  │ │
│  │ serper    │   │ LLM call │   │   LLM call ×5      │ │
│  │ docs      │   └──────────┘   └─────────┬──────────┘ │
│  │ feeds     │                            │            │
│  │ beamer    │                            ▼            │
│  └───────────┘                  ┌────────────────────┐ │
│                                 │ 4. Synthesize      │ │
│                                 │   종합 분석         │ │
│                                 │   LLM call ×1      │ │
│                                 └─────────┬──────────┘ │
│                                           │            │
│                                           ▼            │
│                                 ┌────────────────────┐ │
│                                 │ 5. Exec Summary    │ │
│                                 │   전용 LLM call ×1 │ │
│                                 └─────────┬──────────┘ │
│                                           │            │
│                                           ▼            │
│                                 ┌────────────────────┐ │
│                                 │ 6. Report          │ │
│                                 │   MD 생성 + 번역   │ │
│                                 │   LLM call ×8      │ │
│                                 └────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 경쟁사 목록

| 제품 | Docs | Changelog |
|------|------|-----------|
| LangSmith | [docs.smith.langchain.com](https://docs.smith.langchain.com) | [changelog.langchain.com](https://changelog.langchain.com) |
| Langfuse | [langfuse.com/docs](https://langfuse.com/docs) | [langfuse.com/changelog](https://langfuse.com/changelog) |
| Braintrust | [braintrust.dev/docs](https://braintrust.dev/docs) | [braintrust.dev/docs/changelog](https://braintrust.dev/docs/changelog) |
| MLflow | [mlflow.org/docs/latest/genai](https://mlflow.org/docs/latest/genai) | [mlflow.org/releases](https://mlflow.org/releases) |
| Arize Phoenix | [docs.arize.com/phoenix](https://docs.arize.com/phoenix) | [arize.com/docs/phoenix/release-notes](https://arize.com/docs/phoenix/release-notes) |

## 7-Category 분석 프레임워크

1. **Core Observability** — Trace Depth, Hierarchical Spans, Prompt/Response Logging, Token Tracking, Latency Analysis, Replay
2. **Agent / RAG Observability** — Tool Call Tracing, Retrieval Tracing, Memory Tracing, Multi-step Reasoning, Workflow Graph, Failure Visualization
3. **Evaluation Integration** — Trace→Dataset, LLM-as-Judge, Custom Eval Metrics, Regression Detection, Model Comparison, Human Feedback
4. **Monitoring & Metrics** — Cost Dashboard, Token Analytics, Latency Monitoring, Error Tracking, Tool Success Rate, Custom Metrics
5. **Experiment / Improvement Loop** — Prompt/Model/Dataset Versioning, Experiment Tracking, Continuous Eval, RL/Fine-tuning
6. **DevEx / Integration** — SDK Support, Framework Integration, Custom Model Support, API Access, Streaming Tracing, CLI/Infra
7. **Enterprise & Security** — On-prem/VPC, RBAC, PII Masking, Audit Logs, Data Retention, Region Support

## 설치

```bash
pip install -e .
```

### 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `SERPER_DEV_API` | Yes | Serper.dev API key |
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key |
| `SLACK_WEBHOOK_URL` | No | Slack 알림 webhook |
| `WANDB_API_KEY` | No | W&B Weave tracing |

### CLI 명령어

```bash
python -m intel_bot collect    # 데이터 수집만
python -m intel_bot discover   # 신규 경쟁사 탐색만
python -m intel_bot analyze    # 분석만 (수집 데이터 필요)
python -m intel_bot report     # 리포트 생성만 (분석 데이터 필요)
python -m intel_bot run        # 전체 파이프라인
```

## CI/CD

GitHub Actions (`weekly-report.yml`)가 매주 월요일 09:00 UTC에 자동 실행됩니다.
수동 실행: Actions → Weekly Competitor Report → Run workflow

생성된 리포트는 GitHub Pages로 자동 배포됩니다.
