---
layout: default
title: LLM Observability — 상세 기능 비교
---

# LLM Observability — 상세 기능 비교
**날짜**: 2026-02-12 | **모델**: google/gemini-3-pro-preview

> O(강력) / △(보통) / X(없음 또는 해당 없음)

## 핵심 Observability

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace Depth | 중첩된 함수 호출 Tracing 깊이 | O | O | O | O | O | O |
| Hierarchical Spans | 부모-자식 Span 관계 유지 | O | O | O | O | O | O |
| Prompt Logging | LLM Prompt 자동 캡처 | O | O | O | O | O | O |
| Response Logging | LLM 응답 자동 캡처 | O | O | O | O | O | O |
| Token Tracking | 입출력 토큰 사용량 카운팅 | O | O | O | O | O | O |
| Latency Analysis | Span별 및 End-to-end 지연 시간 측정 | O | O | O | O | O | O |
| Replay | UI 내 단계별 Trace Replay | △ | △ | O | X | X | △ |

## Agent / RAG Observability

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Tool Call Tracing | Tool/함수 호출 입력 및 출력 캡처 | O | O | O | O | O | O |
| Retrieval Tracing | Retriever 쿼리 및 반환된 문서 로깅 | O | O | O | O | O | O |
| Memory Tracing | 대화형 메모리 읽기/쓰기 추적 | X | X | X | X | X | X |
| Multi-step Reasoning | 멀티턴 Agent 추론 체인 시각화 | O | O | O | O | O | O |
| Workflow Graph | Agent 워크플로우의 DAG 또는 그래프 뷰 | X | △ | O | X | X | O |
| Failure Visualization | Trace 내 실패 단계 강조 표시 | △ | X | O | △ | X | △ |

## Evaluation 통합

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace→Dataset | 프로덕션 Trace를 Eval 데이터셋으로 변환 | O | O | O | O | O | O |
| LLM-as-Judge | 내장된 LLM 기반 Eval Scoring | O | O | O | O | O | O |
| Custom Eval Metrics | 사용자 정의 Eval 함수 | O | O | O | O | O | O |
| Regression Detection | 품질 저하(Regression) 자동 감지 | △ | O | △ | O | X | △ |
| Model Comparison | 모델 출력 결과의 Side-by-side 비교 | O | O | O | △ | O | X |
| Human Feedback UI | 사람의 어노테이션 및 레이블링을 위한 UI | O | O | O | O | O | O |

## 모니터링 및 지표 (Metrics)

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Dashboard | 실시간 LLM 비용 추적 Dashboard | O | O | O | O | X | O |
| Token Analytics | 토큰 사용량 분석 및 트렌드 | O | O | O | O | O | O |
| Latency Monitoring | 지연 시간 백분위수 및 알림 | △ | O | O | O | O | O |
| Error Tracking | 에러율 모니터링 및 알림 | O | O | △ | O | O | O |
| Tool Success Rate | Tool 호출 성공/실패율 | △ | X | O | △ | O | O |
| Custom Metrics | 사용자 정의 커스텀 지표 추적 | O | △ | O | O | O | O |

## 실험 / 개선 루프 (Experiment Loop)

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Versioning | Prompt 템플릿 버전 관리 | O | O | O | O | O | O |
| Model Versioning | 모델 버전 및 설정 추적 | O | △ | △ | △ | O | X |
| Experiment Tracking | A/B 테스트 및 실험 관리 | O | O | O | O | O | O |
| Dataset Versioning | Eval 및 학습 데이터셋 버전 관리 | O | O | O | O | O | △ |
| Continuous Eval | 예약 또는 트리거 기반 Eval 실행 | △ | △ | △ | O | △ | O |
| RL/Fine-tuning Link | Fine-tuning 파이프라인과의 연동 | O | O | △ | X | O | △ |

## DevEx / 통합

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK Support | Python, JS/TS 등 공식 SDK 지원 | O | O | O | O | O | O |
| Framework Integration | LangChain, LlamaIndex 등 내장 지원 | O | O | O | O | O | O |
| Custom Model Support | 비표준 또는 자체 호스팅 모델 Tracing | O | O | O | O | O | O |
| API Access | 프로그래밍 방식 접근을 위한 REST/GraphQL API | O | O | O | O | O | X |
| Streaming Tracing | Streaming LLM 응답 Tracing | O | X | △ | O | X | X |
| CLI/Infra Integration | CLI 도구 및 Infrastructure-as-code 지원 | △ | X | X | △ | X | X |

## 보안 및 거버넌스

| 기능 | 설명 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| On-prem/VPC | 자체 호스팅 또는 VPC 배포 옵션 | O | O | O | O | O | O |
| RBAC | 역할 기반 액세스 제어 | O | X | O | O | △ | O |
| PII Masking | 개인정보(PII) 자동 감지 및 마스킹 | O | △ | O | O | O | △ |
| Audit Logs | 사용자 및 시스템 작업 감사 로그 | O | X | O | O | △ | O |
| Data Retention | 구성 가능한 데이터 보관 정책 | △ | O | O | △ | X | O |
| Region Support | 멀티 리전 또는 데이터 레지던시 지원 | O | O | O | O | △ | X |