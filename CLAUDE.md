# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

W&B Weave의 경쟁사 제품을 주기적으로 조사하여 기능 비교표를 자동 생성하는 봇. 매주 피드/문서를 수집하고, Perplexity Sonar(웹 검색+분석)와 Gemini Pro(종합 분석)로 분석한 후 Markdown 리포트를 생성한다. GitHub Pages를 통해 결과를 웹에서 열람할 수 있다.

## 파이프라인

collect(피드+문서) → discover(신규 경쟁사) → analyze(Sonar 카테고리별 48회 + Pro 종합 8회) → report(Markdown) → translate(한/일) → deploy(GitHub Pages)

## 주요 비교 대상

LangSmith, Langfuse, Braintrust, MLflow, Arize Phoenix

## 8-Category 비교 프레임워크

1. Core Tracing & Logging
2. Agent & RAG Observability
3. Evaluation & Quality
4. Guardrails & Safety
5. Monitoring & Analytics
6. Experiment & Improvement Loop
7. Developer Experience & Integration
8. Infrastructure & Enterprise

## 핵심 설정

- `config.py`: 경쟁사 목록, URL, 카테고리 정의 (single source of truth)
- `PERPLEXITY_API_KEY` (필수): Sonar — 카테고리별 웹 검색+분석
- `OPENROUTER_API_KEY` (필수): Gemini Pro — 종합 분석
- `SERPER_DEV_API` (선택): discovery에서만 사용
