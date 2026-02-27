# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

W&B Weave의 경쟁사 제품을 주기적으로 조사하여 기능 비교표를 자동 생성하는 봇. crewAI 3-에이전트 파이프라인(Sonar + Gemini Pro)으로 분석한 후 Markdown 리포트를 생성한다. GitHub Pages를 통해 결과를 웹에서 열람할 수 있다.

## 파이프라인

collect_updates → analyze_baseline → write_report → translate(한/일) → deploy(GitHub Pages)

## 분석 아키텍처 (crewAI 3-에이전트)

제품별 Step 1 — 업데이트 수집:
- changelog URL 스크래핑 (requests+BeautifulSoup, LLM 오버헤드 없음)
- UpdateCollector (Perplexity Sonar): changelog 기반 + 웹 검색 보완으로 최근 변경사항 수집 → ProductUpdates

제품별 Step 2 — 베이스라인 분석/갱신:
- reference_urls 스크래핑 (requests+BeautifulSoup)
- BaselineAnalyzer (Gemini Pro): 업데이트 + 기존 baseline JSON 비교 → ProductChangeset (변경 전/후 + 갱신된 baseline)

전체 제품 Step 3 — 레포트 작성:
- ReportWriter (Gemini Pro): 전 제품 changeset + baseline → ReportSynthesis (비교 rating + AI 코멘트)
- AI 코멘트 첫 줄은 이번 주 변경 하이라이트 필수 포함

베이스라인 초기 생성: `scripts/generate_baseline.py` (독립 스크립트, 포괄적 문서 조사)

Weave 연동: @weave.op() 트레이싱으로 분석 과정 전체 추적

## 리포트 형식 (4섹션)

1. AI Comment — 이번 주 변경 하이라이트 + 시장 요약 3줄
2. Recent Updates — 제품별 최근 업데이트
3. Feature Comparison (Summary) — 8카테고리 요약 비교표
4. Detailed Feature Comparison — 49항목 전체 비교표

## 프롬프트 관리

에이전트/태스크 프롬프트는 `prompts.py`에 기본값이 정의되어 있고, `weave.StringPrompt`로 Weave에 저장·버전 관리된다. `python -m intel_bot publish-prompts`로 기본값을 Weave에 업로드할 수 있다.

## 주요 비교 대상

LangSmith, Langfuse, Braintrust, MLflow, Arize Phoenix

## 8-Category 비교 프레임워크 (49항목)

1. Core Tracing & Logging (8)
2. Agent & RAG Specifics (7)
3. Evaluation & Quality (8)
4. Guardrails & Safety (4)
5. Analytics & Dashboard (6)
6. Development Lifecycle (5)
7. Integration & DX (5)
8. Enterprise & Infrastructure (6)

## 핵심 설정

- `config.py`: 경쟁사 목록, URL, 카테고리 정의, reference_urls (single source of truth)
- `PERPLEXITY_API_KEY` (필수): UpdateCollector — Sonar 웹 검색
- `OPENROUTER_API_KEY` (필수): BaselineAnalyzer, ReportWriter

## 모듈 구조

- `agents/`: crewAI 에이전트 팩토리 함수 (UpdateCollector, BaselineAnalyzer, ReportWriter)
- `crew.py`: crewAI 3-에이전트 오케스트레이션 (collect_updates, analyze_baseline, write_report, analyze_all)
- `analyzer.py`: crew.py의 analyze_all을 re-export (공용 API)
- `prompts.py`: Weave 연동 프롬프트 관리 (load_prompts/publish_prompts)
- `cli.py`: run 중심 CLI (analyze/report/run/publish-prompts)
- `config.py`: 설정/경쟁사/카테고리 정의
- `models.py`: Pydantic 데이터 모델 (ProductUpdates, ProductChangeset, ProductBaseline, ReportSynthesis, AnalysisRun)
- `report.py`: Markdown 리포트 생성 (4섹션)
- `translator.py`: 번역
- `storage.py`: 분석 결과 및 베이스라인 저장/로드
- `notify.py`: Slack 알림 (옵션 플러그인)
- `wb_report.py`: W&B Report 발행 (옵션 플러그인)

## 베이스라인 데이터

- `data/{product}.json`: 제품별 기능 베이스라인 (49항목의 available, provision_method, feature_name, notes)
- 초기 생성: `python scripts/generate_baseline.py` (독립 스크립트)
- 주간 갱신: Step 2 BaselineAnalyzer가 분석 시 자동 갱신
