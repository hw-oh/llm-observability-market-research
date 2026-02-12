---
layout: default
title: LLM Observability — 상세 기능 비교
---

# LLM Observability — 상세 기능 비교
**날짜**: 2026-02-12 | **모델**: google/gemini-3-pro-preview

> O(강력) / △(보통) / X(없음 또는 해당 없음)

## 핵심 Tracing & Logging

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Nested Span Tracing | 부모-자식 관계를 가진 중첩된 함수/LLM 호출 Span Tracing | O | O | O | O | O | O |
| Auto-Instrumentation | 한 줄의 코드로 자동 Trace 수집 (데코레이터, autolog 등) | O | O | O | O | O | O |
| Prompt & Response Logging | LLM 입력 Prompt와 출력 Response 자동 캡처 | O | O | O | O | O | O |
| Token Usage Tracking | 입력/출력/캐시/추론 Token 사용량 추적 | O | O | O | O | O | O |
| Latency Measurement | Span별 및 엔드투엔드 Latency 측정 | O | O | O | O | O | O |
| Cost Estimation | Token 사용량 기반 자동 비용 추정 | O | O | X | O | X | O |
| Streaming Trace | Streaming LLM 응답의 실시간 Tracing | △ | O | △ | △ | △ | △ |
| Metadata & Tags | Trace에 커스텀 메타데이터 및 태그 첨부 | O | O | O | O | O | O |
| OpenTelemetry Compatibility | OTEL 표준 Trace 내보내기/가져오기 지원 | O | O | O | O | O | O |

## Agent & RAG Observability

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Tool/Function Call Tracing | 에이전트 도구 호출 입력 및 출력 자동 Tracing | O | O | O | O | O | O |
| Retrieval (RAG) Tracing | 리트리버 쿼리 및 반환된 문서 로깅 | O | O | O | O | △ | O |
| Multi-step Reasoning Trace | 멀티턴 에이전트 추론 체인 시각화 | O | O | O | O | O | O |
| Workflow Graph View | 에이전트 워크플로우의 DAG/그래프 시각화 | O | △ | O | △ | X | △ |
| MCP/A2A Protocol Tracing | Model Context Protocol 및 Agent2Agent 프로토콜 Trace 지원 | △ | X | X | X | X | △ |
| Failed Step Highlighting | Trace 내 실패한 단계 자동 강조 | △ | O | △ | △ | O | △ |
| Session/Conversation Grouping | 세션 또는 대화별 Trace 그룹화 | △ | O | O | O | △ | O |

## Evaluation & Quality

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| LLM-as-Judge | 내장된 LLM 기반 자동 Eval Scoring | O | O | O | O | O | O |
| Custom Eval Scorers | 사용자 정의 Eval 함수 작성 및 실행 | O | O | O | O | O | O |
| Human Feedback / Annotation UI | UI 기반 사람의 평가, 주석 및 레이블링 | X | O | O | O | O | △ |
| Evaluation Dataset Management | Eval 데이터셋 생성, 버전 관리 및 저장 | O | O | O | O | O | O |
| Trace → Eval Dataset | 프로덕션 Trace를 Eval 데이터셋으로 직접 변환 | △ | O | △ | O | O | △ |
| Regression Detection | 모델/Prompt 변경 시 자동 품질 저하 감지 | △ | O | O | O | △ | △ |
| Side-by-side Model Comparison | 모델/Prompt 출력 결과의 병렬 비교 | O | O | O | O | O | O |
| Evaluation Leaderboard | 여러 모델/Prompt Eval 결과의 순위표 | O | △ | △ | △ | △ | X |
| CI/CD Eval Integration | CI/CD 파이프라인(GitHub Actions 등)에 내장된 Eval | X | △ | △ | O | △ | X |
| Online Evaluation (Monitors) | 프로덕션 Trace에 대한 실시간 자동 Eval | △ | O | O | O | O | △ |

## Guardrails & Safety

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Built-in Guardrails | 내장 Guardrails (독성, PII, 환각 등) | O | △ | X | △ | X | X |
| Custom Guardrails | 사용자 정의 Guardrail Scorer 작성 | O | O | O | O | △ | △ |
| Pre/Post Response Hooks | LLM 응답 전후의 안전성 검사 훅 | O | △ | △ | O | △ | △ |
| PII Detection & Masking | 개인정보(PII) 자동 감지 및 마스킹 | △ | △ | X | X | X | △ |

## Monitoring & Analytics

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Dashboard | 실시간 LLM 비용 추적 Dashboard | O | O | O | O | O | X |
| Token Usage Analytics | Token 사용량 세부 분석 및 트렌드 | O | O | O | O | O | O |
| Latency Percentiles & Alerting | Latency 백분위수 모니터링 및 알림 | △ | △ | △ | △ | △ | O |
| Error Rate Monitoring | 에러율 모니터링 및 알림 | X | O | O | O | O | △ |
| Custom Metrics | 사용자 정의 커스텀 메트릭 추적 | O | △ | O | O | O | O |
| Drift Detection | 모델 입력/출력 분포의 Drift 감지 | X | X | X | X | X | O |
| Embedding Clustering/Analysis | 임베딩 공간 클러스터링 및 시각화 분석 | X | △ | X | X | X | O |

## Experiment & Improvement Loop

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Versioning | Prompt 템플릿 버전 관리 | O | O | O | O | O | O |
| Model Versioning | 모델 버전 및 설정 추적 | △ | O | △ | △ | O | △ |
| Experiment Tracking | A/B 테스트 및 실험 관리 | O | O | O | O | O | O |
| Dataset Versioning | 버전 관리되는 Eval 및 학습 데이터셋 | O | △ | X | O | △ | △ |
| LLM Playground | 대화형 Prompt 테스트 인터페이스 | O | O | O | O | X | △ |
| Continuous/Scheduled Eval | 예약 또는 트리거 기반 자동 Eval 실행 | △ | O | X | △ | △ | X |
| RL/Fine-tuning Pipeline | Fine-tuning/RL 파이프라인과의 통합 | △ | X | X | △ | O | X |
| Training Data Generation | Trace로부터 자동 학습 데이터 생성 | X | O | △ | O | O | △ |
| Failure Trajectory Extraction | 실패 패턴 Trace를 데이터셋으로 추출 | O | O | △ | O | O | O |

## Developer Experience & Integration

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Python SDK | 공식 Python SDK | O | O | O | O | O | O |
| TypeScript/JS SDK | 공식 TypeScript/JavaScript SDK | O | O | O | O | O | △ |
| Framework Integration | LangChain, LlamaIndex, DSPy, CrewAI 등 내장 지원 | △ | O | O | O | O | O |
| REST/GraphQL API | 프로그래밍 방식 접근을 위한 REST 또는 GraphQL API | X | O | O | X | O | O |
| Custom Model Support | 비표준 또는 자체 호스팅 모델 Tracing | O | O | O | O | △ | O |
| CLI Tools | 커맨드라인 인터페이스 도구 | X | △ | X | O | O | X |
| Notebook Integration | Jupyter/Colab 노트북 내 Trace 시각화 | X | O | △ | X | △ | △ |

## Infrastructure & Enterprise

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cloud Managed (SaaS) | 관리형 클라우드 서비스 제공 | O | O | O | O | △ | △ |
| Self-Host / On-Prem | 자체 호스팅 또는 온프레미스 배포 옵션 | O | O | O | O | O | O |
| VPC Deployment | 고객 VPC 내 배포 | △ | △ | △ | △ | O | O |
| Open Source | 오픈 소스 코드 가용성 | O | X | O | X | O | O |
| RBAC | 역할 기반 액세스 제어 | X | O | O | O | X | X |
| SSO/SAML | SSO 및 SAML 인증 지원 | O | △ | △ | O | X | △ |
| SOC 2 Certification | SOC 2 Type II 보안 인증 | O | X | X | O | X | X |
| Audit Logs | 사용자 및 시스템 작업 감사 로그 | O | O | O | △ | △ | O |
| Data Retention Policy | 구성 가능한 데이터 보관 정책 | △ | X | O | △ | X | O |
| Data Warehouse Export | 외부 데이터 웨어하우스로 내보내기 | O | X | O | X | △ | X |
| Multi-Region / Data Residency | 멀티 리전 또는 데이터 거주성 지원 | O | O | O | △ | △ | △ |
| Traditional ML Experiment Integration | 기존 ML 실험 추적(W&B, MLflow 등)과의 통합 | O | X | X | X | O | X |
| Databricks Native Integration | Databricks 플랫폼 네이티브 통합 | X | X | X | X | O | △ |