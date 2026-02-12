---
layout: default
title: LLM Observability — 상세 기능 비교
---

# LLM Observability — 상세 기능 비교
**날짜**: 2026-02-12 | **모델**: google/gemini-3-pro-preview

> ●●●(강력) / ●●○(보통) / ●○○(약함) / ○○○(없음)

## 핵심 Observability

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace Depth | 중첩된 함수 호출 Tracing 깊이 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Hierarchical Spans | 부모-자식 Span 관계 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Prompt Logging | LLM Prompt 자동 캡처 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Response Logging | LLM 응답 자동 캡처 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Token Tracking | 입력/출력 토큰 사용량 카운팅 | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |
| Latency Analysis | Span별 및 엔드투엔드 지연 시간 측정 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Replay | Dashboard UI에서 단계별 Tracing 재생 | ●●○ | ●●● | ●●○ | ●●● | ●●○ | ●●● |

## Agent / RAG Observability

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Tool Call Tracing | 도구/함수 호출 입력 및 출력 캡처 | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |
| Retrieval Tracing | Retriever 쿼리 및 반환된 문서 로깅 | ●●● | ●●● | ●●● | ●●○ | ●●● | ●●● |
| Memory Tracing | 대화형 메모리 읽기/쓰기 추적 | ○○○ | ●●○ | ●●● | ●○○ | ●●○ | ●●○ |
| Multi-step Reasoning | 멀티턴 에이전트 추론 체인 시각화 | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |
| Workflow Graph | 에이전트 워크플로우의 DAG 또는 그래프 뷰 | ●●○ | ●●● | ●●● | ●●○ | ●●○ | ●●○ |
| Failure Visualization | Tracing 내 실패한 단계 강조 표시 | ●●○ | ●●● | ●●○ | ●●○ | ●●● | ●●● |

## Evaluation 통합

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace→Dataset | 프로덕션 Tracing을 Eval 데이터셋으로 변환 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| LLM-as-Judge | 내장된 LLM 기반 Eval Scoring | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Custom Eval Metrics | 사용자 정의 Eval 함수 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Regression Detection | 품질 저하(Regression) 자동 감지 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Model Comparison | 모델 출력 결과의 병렬 비교 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Human Feedback UI | 인간 어노테이션 및 레이블링을 위한 UI | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |

## Monitoring & Metrics

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Dashboard | 실시간 LLM 비용 추적 Dashboard | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Token Analytics | 토큰 사용량 상세 분석 및 트렌드 | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |
| Latency Monitoring | 지연 시간 백분위수 및 알림 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Error Tracking | 에러율 모니터링 및 알림 | ●●○ | ●●● | ●●○ | ●●● | ●●● | ●●● |
| Tool Success Rate | 도구 호출 성공/실패율 | ○○○ | ●●○ | ●●● | ●●○ | ●●● | ●●● |
| Custom Metrics | 사용자 정의 커스텀 지표 추적 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |

## 실험 / 개선 루프

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Versioning | 프롬프트 템플릿 버전 관리 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Model Versioning | 모델 버전 및 설정 추적 | ●●● | ●●○ | ●●○ | ●●● | ●●● | ●●○ |
| Experiment Tracking | A/B 테스트 및 실험 관리 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Dataset Versioning | Eval 및 학습 데이터셋 버전 관리 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Continuous Eval | 예약된 또는 트리거 기반 Eval 실행 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| RL/Fine-tuning Link | Fine-tuning 파이프라인과의 연동 | ●●● | ●●○ | ●●○ | ●○○ | ●●● | ●●○ |

## DevEx / 통합

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK Support | Python, JS/TS 등 공식 SDK 지원 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Framework Integration | LangChain, LlamaIndex 등 내장 지원 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Custom Model Support | 비표준 또는 자체 호스팅 모델 Tracing | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| API Access | 프로그래밍 방식 접근을 위한 REST 또는 GraphQL API | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Streaming Tracing | Streaming LLM 응답 Tracing | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●○ |
| CLI/Infra Integration | CLI 도구 및 Infrastructure-as-code 지원 | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |

## 엔터프라이즈 및 보안

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| On-prem/VPC | 자체 호스팅 또는 VPC 배포 옵션 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| RBAC | 역할 기반 액세스 제어 | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |
| PII Masking | 개인정보(PII) 자동 감지 및 마스킹 | ○○○ | ●●○ | ●●● | ●●○ | ●●○ | ○○○ |
| Audit Logs | 사용자 및 시스템 작업 감사 로그 | ○○○ | ●●● | ●●● | ●●○ | ●●○ | ○○○ |
| Data Retention | 구성 가능한 데이터 보존 정책 | ○○○ | ●●● | ●●● | ●●● | ●●○ | ●●○ |
| Region Support | 멀티 리전 또는 데이터 레지던시 지원 | ○○○ | ●●● | ●●○ | ●○○ | ●●● | ●●○ |