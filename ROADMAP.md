# Roadmap

## 기술 스택

- **검색**: Serper.dev (무료 2,500회/월)
- **LLM**: OpenRouter + OpenAI SDK (기본 모델: `google/gemini-3-pro-preview`)
- **스크래핑**: httpx + BeautifulSoup4
- **피드**: feedparser (GitHub Atom + PyPI RSS)
- **설정**: pydantic-settings (.env 로딩)
- **CLI**: rich (터미널 출력)
- **출력**: Markdown → GitHub Pages

## 수집 전략

- **첫 실행 (initial)**: docs 전체 읽기 → 비교 축별 기능 정리
- **이후 실행 (update)**: changelog/피드로 변경 감지 → 변경된 경쟁사만 docs 재확인

## 비교 대상 경쟁사 & 데이터 소스

| 경쟁사 | Docs URL | Changelog | GitHub Repo | PyPI |
|--------|----------|-----------|-------------|------|
| LangSmith | docs.smith.langchain.com | changelog.langchain.com | langchain-ai/langsmith-sdk | langsmith |
| Arize Phoenix | docs.arize.com/phoenix | GitHub releases | Arize-ai/phoenix | arize-phoenix |
| Braintrust | braintrust.dev/docs | braintrust.dev/docs/changelog | braintrustdata/braintrust-sdk | braintrust |
| Langfuse | langfuse.com/docs | langfuse.com/changelog | langfuse/langfuse | langfuse |
| Humanloop | humanloop.com/docs | humanloop.com/docs/changelog | (없음) | humanloop |
| Logfire | logfire.pydantic.dev/docs | logfire.pydantic.dev/docs/release-notes | pydantic/logfire | logfire |

## 프로젝트 구조

```
llm-observability-market-research/
├── src/intel_bot/
│   ├── __init__.py
│   ├── config.py             # Settings(.env) + 경쟁사 정의(COMPETITORS)
│   ├── models.py             # Pydantic 데이터 모델
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── serper.py         # Serper.dev 검색
│   │   ├── docs_scraper.py   # 공식 docs 스크래핑 (httpx + bs4)
│   │   └── feed.py           # GitHub Atom + PyPI RSS (feedparser)
│   ├── analyzer.py           # LLM 분석 (Phase 2)
│   ├── report.py             # Markdown 리포트 생성 (Phase 3)
│   ├── storage.py            # JSON 파일 저장/로드
│   └── cli.py                # CLI 진입점
├── data/
│   ├── raw/{날짜}/           # 수집된 원시 데이터 (git-ignored)
│   └── analyzed/{날짜}/      # 분석 결과 (git-ignored)
├── reports/                  # 생성된 Markdown 리포트 (git-tracked)
├── .env                      # API 키 (git-ignored)
├── .env.example
├── .gitignore
└── pyproject.toml
```

## CLI 흐름

```
python -m intel_bot collect   # Phase 1: 데이터 수집 → data/raw/
python -m intel_bot analyze   # Phase 2: LLM 분석 → data/analyzed/
python -m intel_bot report    # Phase 3: Markdown 생성 → reports/
python -m intel_bot run       # Phase 4: collect → analyze → report 전체 실행
```

---

## Phase 1: 프로젝트 셋업 및 데이터 수집

- [ ] `.gitignore` 생성 (.env, data/, __pycache__ 보호)
- [ ] `pyproject.toml` 생성 + 가상환경 + 의존성 설치
- [ ] 설정 및 데이터 모델 (`config.py`, `models.py`)
- [ ] Serper.dev 검색 클라이언트 (`collectors/serper.py`)
- [ ] 공식 docs 스크래핑 (`collectors/docs_scraper.py`)
- [ ] GitHub Atom + PyPI RSS 피드 수집 (`collectors/feed.py`)
- [ ] JSON 파일 저장 및 이전 데이터 비교 (`storage.py`)
- [ ] CLI 진입점 (`cli.py` — `python -m intel_bot collect`)
- [ ] `.env.example` 생성

## Phase 2: LLM 분석 파이프라인

`analyzer.py` — 수집 데이터(`data/raw/`)를 읽어 구조화된 비교 결과(`data/analyzed/`)를 생성

- [ ] OpenRouter 클라이언트 설정 (OpenAI SDK 호환, `config.py` 설정 활용)
- [ ] 비교 축별 분석 프롬프트 설계
- [ ] 경쟁사별 기능 요약 생성 → JSON 저장
- [ ] Weave 대비 강점/약점 판별 로직
- [ ] CLI에 `analyze` 커맨드 추가

## Phase 3: Markdown 리포트 생성

`report.py` — 분석 결과(`data/analyzed/`)를 읽어 Markdown 리포트(`reports/`)를 생성

- [ ] 비교표 Markdown 템플릿 설계
- [ ] Weave 대비 강점/약점 하이라이트 포맷
- [ ] 주차별 리포트 파일 생성 (`reports/YYYY-MM-DD.md`)
- [ ] CLI에 `report` 커맨드 추가

## Phase 4: 자동화 및 배포

- [ ] CLI에 `run` 커맨드 추가 (collect → analyze → report 파이프라인)
- [ ] GitHub Actions 주간 스케줄러 (기존 `pages.yml` 확장)
- [ ] 이전 주 리포트 대비 변경사항 diff 표시
- [ ] 리포트 자동 커밋 + GitHub Pages 배포
- [ ] 실행 결과 알림 (Slack 또는 이메일)

## Phase 5: 고도화

- [ ] 경쟁사 가격 변동 추적 (수집 데이터 히스토리 비교)
- [ ] 신규 경쟁사 자동 탐지 (Serper.dev 주기적 검색)
- [ ] 히스토리 대시보드 (주차별 트렌드 시각화)
