---
layout: default
title: LLM Observability — 상세 기능 비교
---

# LLM Observability — 상세 기능 비교
**날짜**: 2026-02-12 | **모델**: google/gemini-3-pro-preview

> O(강점) / △(보통) / X(없음 또는 해당 없음)

## Core Tracing & Logging

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Full Request/Response Tracing | LLM 입력 프롬프트, 출력 응답 및 파라미터의 완전한 캡처 | O | O | O | O | O | O |
| Nested Span & Tree View | 부모-자식 트리 시각화를 포함한 계층적 Span Tracing | O | O | O | O | O | O |
| Streaming Support | 스트리밍 LLM 응답의 실시간 Tracing | △ | O | O | △ | △ | △ |
| Multimodal Tracing | 이미지, 오디오 및 기타 비텍스트 입력/출력의 Tracing 및 렌더링 | O | X | X | O | X | X |
| Auto-Instrumentation | 한 줄의 코드로 자동 Trace 수집 (decorators, autolog 등) | O | O | O | O | O | O |
| Metadata & Tags Filtering | 검색 및 필터링을 위한 커스텀 메타데이터 및 태그 첨부 | O | △ | O | O | O | O |
| Token Counting & Estimation | 토크나이저별 정확한 Input/Output/Cached 토큰 카운팅 | O | △ | O | O | △ | O |
| OpenTelemetry Standard | OTEL 표준 Trace 내보내기/가져오기 호환성 | O | O | O | △ | O | O |

## Agent & RAG Specifics

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| RAG Retrieval Visualizer | 검색된 문서 청크의 내용 및 관련성 Scoring UI 표시 | △ | O | O | △ | △ | O |
| Tool/Function Call Rendering | Tool/Function Call 입력 및 반환 값의 파싱된 뷰 | O | O | △ | O | X | O |
| Agent Execution Graph | 루프와 분기가 포함된 에이전트 워크플로우의 DAG/그래프 시각화 | △ | O | X | X | X | △ |
| Intermediate Step State | 에이전트 중간 추론 과정(Chain-of-Thought)의 저장 및 표시 | O | O | O | △ | △ | O |
| Session/Thread Replay | 사용자 세션 또는 대화 스레드를 전체 흐름으로 재생 | O | △ | O | △ | X | O |
| Failed Step Highlighting | 에이전트 Trace에서 실패한 단계의 자동 하이라이트 | △ | O | △ | O | X | △ |
| MCP Integration | Model Context Protocol 서버/클라이언트 통합 및 Tracing | O | X | X | X | X | X |

## Evaluation & Quality

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| LLM-as-a-Judge Wizard | 코드 없이 GUI 기반으로 LLM Judge 빌드 | O | △ | △ | O | O | X |
| Custom Eval Scorers | 사용자 정의 코드 기반 Eval 함수 작성 및 실행 | O | O | O | O | O | O |
| Dataset Management & Curation | Eval 데이터셋 생성, 버전 관리 및 Trace의 데이터셋 변환 | O | O | O | O | O | O |
| Prompt Optimization / DSPy Support | 자동 프롬프트 최적화 또는 후보 제안 (예: DSPy 연동) | X | △ | X | O | X | O |
| Regression Testing | 모델/프롬프트 변경 시 자동 품질 저하(Regression) 감지 | △ | O | △ | O | O | O |
| Comparison View (Side-by-side) | 모델/프롬프트 출력 결과의 병렬 비교 | O | O | X | O | O | O |
| Annotation Queues | 큐 관리 및 검토자 할당을 포함한 팀 기반 어노테이션 워크플로우 | △ | O | O | △ | △ | △ |
| Online Evaluation | 실제 프로덕션 트래픽에 대한 실시간 자동 Eval | O | O | O | O | O | △ |

## Guardrails & Safety

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| PII/Sensitive Data Masking | 개인정보(PII) 및 민감 데이터 자동 감지 및 마스킹 | O | △ | △ | X | X | O |
| Hallucination Detection | 환각(Hallucination) 콘텐츠 감지를 위한 전용 Guardrail | O | X | △ | △ | X | △ |
| Topic/Jailbreak Guardrails | 금지된 주제 차단 및 탈옥(Jailbreak) 시도 감지 | O | X | △ | △ | △ | O |
| Policy Management as Code | 코드로 정의되고 관리되는 Guardrail 규칙 | O | X | X | △ | △ | O |

## Analytics & Dashboard

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Analysis & Attribution | 사용자/팀/프로젝트별 비용 추적 및 할당 | O | △ | O | △ | X | X |
| Token Usage Analytics | Input/Output 토큰 사용량 분석 및 트렌드 | O | O | O | O | O | O |
| Latency Heatmap & P99 | 백분위수 모니터링을 포함한 Latency 분포 시각화 | △ | △ | O | △ | △ | △ |
| Error Rate Monitoring | 에러율 추적 및 알림 | △ | O | △ | △ | O | △ |
| Embedding Space Visualization | UMAP/t-SNE 임베딩 클러스터링 및 시각화 | X | X | X | X | X | X |
| Custom Metrics & Dashboard | Dashboard 위젯을 통한 사용자 정의 지표 추적 | O | O | O | O | O | O |

## Development Lifecycle

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Management (CMS) | 비개발자 수정 및 배포가 가능한 프롬프트 버전 관리 | △ | O | O | O | O | △ |
| Playground & Sandbox | 대화형 프롬프트 및 파라미터 테스트 환경 | O | △ | O | O | X | O |
| Experiment Tracking | 하이퍼파라미터 로깅을 포함한 A/B 테스트 및 실험 관리 | O | O | O | △ | O | O |
| Fine-tuning Integration | Fine-tuning 데이터 내보내기 및 파이프라인 통합 | △ | △ | X | △ | △ | X |
| Version Control & Rollback | 롤백 기능이 포함된 프롬프트 및 모델 버전 관리 | O | O | O | O | O | △ |

## Integration & DX

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK Support (Py/JS/Go) | Python, JavaScript/TypeScript, Go 공식 SDK 지원 | O | △ | △ | O | △ | △ |
| Gateway/Proxy Mode | SDK 설치 없이 프록시 기반 Tracing (URL 변경만으로 가능) | X | X | X | X | O | X |
| Popular Frameworks | LangChain, LlamaIndex, AutoGen, CrewAI 등 기본 지원 | O | O | O | △ | △ | O |
| API & Webhooks | 외부 시스템 연동을 위한 REST/GraphQL API 및 Webhook | O | △ | O | O | O | O |
| CI/CD Integration | 자동화된 Eval 및 배포를 위한 CI/CD 파이프라인 연동 | O | X | X | △ | X | △ |

## Enterprise & Infrastructure

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Deployment Options | Multi-tenant SaaS, Dedicated SaaS, Self-hosted/VPC 배포 옵션 | O | O | O | O | O | O |
| Open Source | 오픈소스 코드 공개 여부 및 커뮤니티 활성도 | △ | X | O | X | O | O |
| Data Sovereignty & Compliance | 데이터 지역 선택 및 SOC 2/HIPAA/GDPR 준수 | O | O | O | △ | △ | △ |
| RBAC & SSO | SSO/SAML 인증을 포함한 역할 기반 액세스 제어 | O | △ | O | O | △ | △ |
| Audit Logs | 사용자 및 시스템 작업 감사 추적 | O | O | O | X | △ | X |
| Data Warehouse Export | Snowflake, BigQuery, S3 등으로의 자동 데이터 내보내기 | O | O | O | X | X | X |