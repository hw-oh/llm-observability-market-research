# LLM Observability Market Research

[English](./README.md)

LLM Observability 경쟁사를 매주 자동 조사하여 기능 비교 리포트를 생성하는 crewAI 멀티 에이전트 봇.

**[리포트 보기 →](https://hw-oh.github.io/llm-observability-market-research/)**

## 빠른 시작

```bash
pip install -e .
python -m intel_bot run
```

## 아키텍처

**3-에이전트 crewAI 파이프라인**으로 베이스라인 기반 변경 감지를 수행합니다:

```
┌──────────────────────────────────────────────────────────────────┐
│  python -m intel_bot run                                         │
│                                                                  │
│  제품별 (병렬 처리):                                              │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐  │
│  │ 1. UpdateCollector   │───▶│ 2. BaselineAnalyzer             │  │
│  │    (Perplexity Sonar)│    │    (Gemini Pro)                 │  │
│  │    체인지로그 스크래핑 │    │    업데이트 vs 베이스라인 비교   │  │
│  │    + 웹 검색          │    │    → ProductChangeset           │  │
│  └─────────────────────┘    └─────────────────────────────────┘  │
│                                                                  │
│  전체 제품:                                                       │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ 3. ReportWriter (Gemini Pro)                                │  │
│  │    전 제품 비교 → ReportSynthesis                            │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                         ▼                                        │
│  리포트 (EN) → 번역 (ko/ja) → GitHub Pages + W&B                 │
└──────────────────────────────────────────────────────────────────┘
```

| 에이전트 | 모델 | 역할 |
|----------|------|------|
| **UpdateCollector** | Perplexity Sonar | 체인지로그 스크래핑 + 웹 검색으로 최근 업데이트 수집 |
| **BaselineAnalyzer** | Gemini Pro | 업데이트를 베이스라인과 비교하여 변경사항 도출 |
| **ReportWriter** | Gemini Pro | 전 제품 기능 비교 rating + AI 코멘트 생성 |

## 베이스라인 데이터

각 제품은 `data/{product}/{date}.json`에 **베이스라인 JSON**을 가지며, 8개 카테고리 49개 항목의 sub-features를 포함합니다. 변경 감지의 기준이 됩니다.

- **초기 생성**: `python scripts/generate_baseline.py` (독립 스크립트, 포괄적 문서 조사)
- **주간 갱신**: BaselineAnalyzer가 분석 시 자동 갱신

## 리포트 형식 (4섹션)

1. **AI Comment** — 제품별 핵심 요약 + 시장 트렌드
2. **Recent Updates** — 변경사항이 감지된 제품만 표시
3. **Feature Comparison (Summary)** — 8카테고리 요약 비교표
4. **Detailed Feature Comparison** — 49항목 전체 비교표

## 비교 대상

| 제품 | Docs | Changelog |
|------|------|-----------|
| LangSmith | [docs.smith.langchain.com](https://docs.smith.langchain.com) | [changelog.langchain.com](https://changelog.langchain.com) |
| Langfuse | [langfuse.com/docs](https://langfuse.com/docs) | [langfuse.com/changelog](https://langfuse.com/changelog) |
| Braintrust | [braintrust.dev/docs](https://braintrust.dev/docs) | [braintrust.dev/docs/changelog](https://braintrust.dev/docs/changelog) |
| MLflow | [mlflow.org/docs/latest/genai](https://mlflow.org/docs/latest/genai) | [mlflow.org/releases](https://mlflow.org/releases) |
| Arize Phoenix | [docs.arize.com/phoenix](https://docs.arize.com/phoenix) | [arize.com/docs/phoenix/release-notes](https://arize.com/docs/phoenix/release-notes) |
| W&B Weave | [wandb.me/weave](https://wandb.me/weave) | [app.getbeamer.com/wandb/en](https://app.getbeamer.com/wandb/en) |

## 8-Category 프레임워크 (49항목)

1. **Core Tracing & Logging** (8) — 요청/응답 트레이싱, 중첩 스팬, 스트리밍, 멀티모달, 자동 계측, 메타데이터, 토큰 카운팅, OpenTelemetry
2. **Agent & RAG Specifics** (7) — RAG 시각화, 도구 호출 렌더링, 에이전트 그래프, 단계 상태, 세션 리플레이, 실패 하이라이팅, MCP
3. **Evaluation & Quality** (8) — LLM-as-a-Judge, 커스텀 스코어러, 데이터셋, 프롬프트 최적화, 리그레션 테스트, 비교 뷰, 어노테이션 큐, 온라인 평가
4. **Guardrails & Safety** (4) — PII 마스킹, 할루시네이션 감지, 탈옥 방지, 정책 코드화
5. **Analytics & Dashboard** (6) — 비용 분석, 토큰 분석, 레이턴시 P99, 에러 모니터링, 임베딩 시각화, 커스텀 대시보드
6. **Development Lifecycle** (5) — 프롬프트 CMS, 플레이그라운드, 실험 추적, 파인튜닝, 버전 관리
7. **Integration & DX** (5) — SDK (Py/JS/Go), 게이트웨이/프록시, 프레임워크, API/Webhooks, CI/CD
8. **Enterprise & Infrastructure** (6) — 배포 옵션, 오픈소스, 컴플라이언스, RBAC/SSO, 감사 로그, 데이터 내보내기

## 설정

### 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `PERPLEXITY_API_KEY` | Yes | UpdateCollector — Sonar 웹 검색 |
| `OPENROUTER_API_KEY` | Yes | BaselineAnalyzer, ReportWriter — OpenRouter 경유 |
| `WANDB_API_KEY` | No | Weave 트레이싱 + W&B Report 발행 |
| `SLACK_WEBHOOK_URL` | No | 완료 시 Slack 알림 |

### CLI 명령어

```bash
python -m intel_bot run              # 전체 파이프라인 (기본)
python -m intel_bot analyze          # 분석만
python -m intel_bot report           # 리포트 생성만 (분석 데이터 필요)
python -m intel_bot publish-prompts  # Weave에 프롬프트 업로드
python scripts/generate_baseline.py  # 베이스라인 초기 생성 (일회성)
```

## 출력 파일

| 경로 | 내용 |
|------|------|
| `reports/YYYY-MM-DD.md` | 주간 리포트 (영문) |
| `ko/reports/`, `ja/reports/` | 번역 리포트 |
| `data/{product}/{date}.json` | 제품별 베이스라인 스냅샷 |
| `data/analyzed/{date}/analysis.json` | 분석 실행 결과 |
| `index.md` | 홈 — 요약 + 리포트 아카이브 |
| `comparison.md` | 기능 비교표 |
| `competitor-detail.md` | 제품별 상세 |

## 옵션 플러그인

해당 환경 변수가 설정된 경우에만 실행됩니다. 실패해도 파이프라인은 중단되지 않습니다.

- **Slack**: 완료 알림 (`SLACK_WEBHOOK_URL`)
- **W&B Report**: 인터랙티브 리포트 + HTML 로깅 + Alert (`WANDB_API_KEY`)

## CI/CD

GitHub Actions (`weekly-report.yml`)가 매주 월요일 09:00 UTC에 자동 실행됩니다.
수동 실행: Actions → Weekly Competitor Report → Run workflow

리포트는 자동 커밋되어 GitHub Pages로 배포됩니다.
