---
layout: default
title: LLM Observability — 상세 기능 비교
---

# LLM Observability — 상세 기능 비교
**날짜**: 2026-02-12 | **모델**: google/gemini-3-pro-preview

> O(강점) / △(약점) / X(없음)

## 핵심 Observability

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace Depth | 중첩된 함수 호출 Tracing 깊이 | O | O | O | O | O | O |
| Hierarchical Spans | 부모-자식 Span 관계 유지 | O | O | O | O | O | O |
| Prompt Logging | LLM Prompt 자동 캡처 | O | O | O | O | O | O |
| Response Logging | LLM 응답 자동 캡처 | O | O | O | O | O | O |
| Token Tracking | 입력/출력 토큰 사용량 카운팅 | O | O | O | O | O | O |
| Latency Analysis | Span별 및 엔드투엔드 지연 시간 측정 | O | O | O | O | O | O |
| Replay | UI에서 단계별 Trace 재생 | △ | O | O | O | △ | O |

## Agent / RAG Observability

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Tool Call Tracing | 도구/함수 호출 입력 및 출력 캡처 | O | O | O | O | O | O |
| Retrieval Tracing | Retriever 쿼리 및 반환된 문서 로깅 | O | O | O | △ | O | O |
| Memory Tracing | 대화형 메모리 읽기/쓰기 추적 | △ | O | O | X | O | △ |
| Multi-step Reasoning | 멀티턴 에이전트 추론 체인 시각화 | O | O | O | O | O | O |
| Workflow Graph | 에이전트 워크플로우의 DAG 또는 그래프 뷰 | O | O | O | O | O | △ |
| Failure Visualization | Trace 내 실패한 단계 하이라이트 | O | O | O | O | O | O |

## Eval 통합

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace→Dataset | 프로덕션 Trace를 Eval 데이터셋으로 변환 | O | O | O | O | O | O |
| LLM-as-Judge | 내장된 LLM 기반 Eval Scoring | O | O | O | O | O | O |
| Custom Eval Metrics | 사용자 정의 Eval 함수 | O | O | O | O | O | O |
| Regression Detection | 품질 저하(Regression) 자동 감지 | O | O | O | O | O | O |
| Model Comparison | 모델 출력 결과의 병렬 비교 | O | O | O | O | O | O |
| Human Feedback UI | 인간의 어노테이션 및 레이블링을 위한 UI | O | O | O | O | O | O |

## 모니터링 및 지표 (Metrics)

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Dashboard | 실시간 LLM 비용 추적 Dashboard | O | O | O | O | O | O |
| Token Analytics | 토큰 사용량 분석 및 트렌드 | O | O | O | O | O | O |
| Latency Monitoring | 지연 시간 백분위수 및 알림 | O | O | O | O | O | O |
| Error Tracking | 에러율 모니터링 및 알림 | O | O | O | O | O | O |
| Tool Success Rate | 도구 호출 성공/실패율 | △ | O | O | △ | O | O |
| Custom Metrics | 사용자 정의 커스텀 지표 추적 | O | O | O | O | O | O |

## 실험 / 개선 루프

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Versioning | Prompt 템플릿 버전 관리 | O | O | O | O | O | O |
| Model Versioning | 모델 버전 및 설정 추적 | O | △ | O | △ | O | △ |
| Experiment Tracking | A/B 테스트 및 실험 관리 | O | O | O | O | O | O |
| Dataset Versioning | 버전 관리되는 Eval 및 학습 데이터셋 | O | O | O | O | O | O |
| Continuous Eval | 예약 또는 트리거 기반 Eval 실행 | O | O | O | O | O | O |
| RL/Fine-tuning Link | Fine-tuning 파이프라인과의 연동 | O | △ | △ | X | O | △ |

## DevEx / 통합

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK Support | Python, JS/TS 등 공식 SDK 지원 | O | O | O | O | O | O |
| Framework Integration | LangChain, LlamaIndex 등 내장 지원 | O | O | O | O | O | O |
| Custom Model Support | 비표준 또는 자체 호스팅 모델 Tracing | O | O | O | O | O | O |
| API Access | 프로그래밍 방식 접근을 위한 REST/GraphQL API | O | O | O | O | O | O |
| Streaming Tracing | Streaming LLM 응답 Tracing | △ | O | O | O | O | O |
| CLI/Infra Integration | CLI 도구 및 Infrastructure-as-code 지원 | O | O | O | O | O | O |

## 엔터프라이즈 및 보안

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| On-prem/VPC | 자체 호스팅 또는 VPC 배포 옵션 | O | O | O | O | O | O |
| RBAC | 역할 기반 액세스 제어 | O | O | O | O | O | O |
| PII Masking | 개인정보(PII) 자동 감지 및 마스킹 | △ | O | O | △ | X | X |
| Audit Logs | 사용자 및 시스템 작업 감사 로그 | △ | O | O | X | X | X |
| Data Retention | 구성 가능한 데이터 보존 정책 | △ | O | O | O | △ | O |
| Region Support | 멀티 리전 또는 데이터 레지던시 지원 | △ | O | O | X | △ | △ |