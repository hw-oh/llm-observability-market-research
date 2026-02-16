---
layout: default
title: LLM Observability — 상세 기능 비교
---

# LLM Observability — 상세 기능 비교
**날짜**: 2026-02-16 | **모델**: google/gemini-3-pro-preview

> O(강력) / △(보통) / X(없음 또는 해당 없음)

## Core Tracing & Logging

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| 전체 Request/Response Tracing | LLM 입력 프롬프트, 출력 응답 및 파라미터의 완전한 캡처 | O | O | O | O | O | O |
| 중첩 Span 및 트리 뷰 | 부모-자식 트리 시각화를 포함한 계층적 Span Tracing | O | O | O | O | O | O |
| Streaming 지원 | Streaming LLM 응답의 실시간 Tracing | △ | O | O | △ | △ | △ |
| 멀티모달 Tracing | 이미지, 오디오 및 기타 비텍스트 입력/출력의 Tracing 및 렌더링 | O | X | X | O | X | △ |
| Auto-Instrumentation | 한 줄의 코드로 자동 Trace 수집 (데코레이터, autolog 등) | O | O | O | O | O | O |
| 메타데이터 및 태그 필터링 | 커스텀 메타데이터 및 태그 첨부와 검색 및 필터링 | O | O | O | O | O | O |
| 토큰 카운팅 및 추정 | 토크나이저별 정확한 입력/출력/캐시 토큰 수 계산 | O | O | O | O | △ | △ |
| OpenTelemetry 표준 | OTEL 표준 Trace 내보내기/가져오기 호환성 | O | O | O | O | O | O |

## Agent & RAG Specifics

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| RAG Retrieval 시각화 도구 | 검색된 문서 청크의 내용과 관련성 Scoring 결과 UI 표시 | △ | O | O | △ | △ | O |
| Tool/Function Call 렌더링 | Tool/Function Call 입력 및 반환 값의 파싱된 뷰 | O | O | △ | O | △ | O |
| Agent 실행 그래프 | 루프와 분기가 포함된 Agent 워크플로우의 DAG/그래프 시각화 | △ | O | X | X | X | △ |
| 중간 단계 상태 | Agent의 중간 추론 과정(Chain-of-Thought) 저장 및 표시 | O | O | O | △ | O | O |
| 세션/스레드 재생 | 사용자 세션 또는 대화 스레드를 전체 흐름으로 재생 | O | △ | O | X | △ | △ |
| 실패 단계 하이라이트 | Agent Trace에서 실패한 단계를 자동으로 강조 표시 | △ | O | △ | △ | O | △ |
| MCP 연동 | Model Context Protocol 서버/클라이언트 통합 및 Tracing | O | △ | X | X | X | X |

## Evaluation & Quality

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| LLM-as-a-Judge 위저드 | 코드 없이 GUI 기반으로 LLM Judge 빌더 생성 | O | △ | O | O | O | X |
| 커스텀 Eval Scorers | 사용자 정의 코드 기반 Eval 함수 작성 및 실행 | O | O | O | O | O | O |
| 데이터셋 관리 및 큐레이션 | Eval 데이터셋 생성, 버전 관리 및 Trace의 데이터셋 변환 | O | O | O | O | O | △ |
| 프롬프트 최적화 / DSPy 지원 | 자동 프롬프트 최적화 또는 후보 제안 (예: DSPy 연동) | X | △ | X | △ | X | △ |
| 회귀 테스트 | 모델/프롬프트 변경 시 자동 품질 회귀 감지 | O | O | △ | O | △ | △ |
| 비교 뷰 (Side-by-side) | 모델/프롬프트 출력 결과의 병렬 비교 | O | O | △ | O | O | O |
| 어노테이션 큐 | 큐 관리 및 검토자 할당을 포함한 팀 기반 어노테이션 워크플로우 | △ | O | O | △ | O | X |
| 온라인 Evaluation | 실제 프로덕션 트래픽에 대한 실시간 자동 Eval | O | O | O | O | O | X |

## Guardrails & Safety

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| PII/민감 데이터 마스킹 | 개인정보(PII) 및 민감 데이터 자동 감지 및 마스킹 | O | △ | O | △ | △ | △ |
| 환각(Hallucination) 감지 | 환각 콘텐츠 감지를 위한 전용 Guardrail | O | X | O | △ | X | △ |
| 주제/탈옥(Jailbreak) Guardrails | 금지된 주제 차단 및 탈옥 시도 감지 | O | △ | O | X | △ | O |
| Policy Management as Code | Guardrail 규칙을 코드로 정의하고 관리 | O | X | △ | X | X | △ |

## Analytics & Dashboard

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| 비용 분석 및 속성 할당 | 사용자/팀/프로젝트별 비용 추적 및 할당 | O | △ | O | △ | △ | X |
| 토큰 사용량 Analytics | 입력/출력 토큰 사용량 분석 및 트렌드 | O | O | △ | O | O | O |
| Latency 히트맵 및 P99 | 백분위수 모니터링을 포함한 Latency 분포 시각화 | △ | O | O | △ | △ | △ |
| 에러율 모니터링 | 에러율 추적 및 알림(Alerting) | △ | O | △ | △ | O | O |
| 임베딩 공간 시각화 | UMAP/t-SNE 임베딩 클러스터링 및 시각화 | X | X | X | X | X | X |
| 커스텀 메트릭 및 Dashboard | Dashboard 위젯을 통한 사용자 정의 메트릭 추적 | O | O | O | O | O | O |

## Development Lifecycle

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| 프롬프트 관리 (CMS) | 비개발자도 수정 및 배포 가능한 프롬프트 버전 관리 | △ | O | O | O | O | △ |
| Playground 및 샌드박스 | 대화형 프롬프트 및 파라미터 테스트 환경 | O | △ | O | O | X | △ |
| 실험 추적 (Experiment Tracking) | 하이퍼파라미터 로깅을 포함한 A/B 테스트 및 실험 관리 | O | O | O | O | O | O |
| Fine-tuning 연동 | Fine-tuning 데이터 내보내기 및 파이프라인 통합 | △ | △ | X | △ | △ | X |
| 버전 제어 및 롤백 | 롤백 기능을 포함한 프롬프트 및 모델 버전 관리 | O | O | △ | O | O | X |

## Integration & DX

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK 지원 (Py/JS/Go) | Python, JavaScript/TypeScript, Go 공식 SDK 지원 | O | △ | △ | O | △ | △ |
| Gateway/Proxy 모드 | SDK 설치 없이 Proxy 기반 Tracing (URL 변경만으로 가능) | X | X | X | X | O | O |
| 주요 프레임워크 지원 | LangChain, LlamaIndex, AutoGen, CrewAI 등 내장 지원 | O | O | O | △ | △ | O |
| API 및 Webhooks | 외부 시스템 연동을 위한 REST/GraphQL API 및 Webhook | O | O | O | △ | O | O |
| CI/CD 통합 | 자동화된 Eval 및 배포를 위한 CI/CD 파이프라인(GitHub Actions 등) 연동 | △ | △ | X | O | △ | △ |

## Enterprise & Infrastructure

| 기능 | 설명 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| 배포 옵션 | 멀티 테넌트 SaaS, 전용 SaaS, 셀프 호스팅/VPC 배포 옵션 | O | O | O | O | O | O |
| 오픈 소스 | 오픈 소스 코드 공개 여부 및 커뮤니티 | O | X | O | X | O | O |
| 데이터 주권 및 컴플라이언스 | 데이터 지역 선택 및 SOC 2/HIPAA/GDPR 준수 | O | O | O | △ | △ | △ |
| RBAC 및 SSO | SSO/SAML 인증을 포함한 역할 기반 액세스 제어 | O | △ | O | O | O | △ |
| 감사 로그 (Audit Logs) | 사용자 및 시스템 작업 감사 추적 | O | O | O | X | △ | X |
| 데이터 웨어하우스 내보내기 | Snowflake, BigQuery, S3 등으로 자동 내보내기 | △ | O | O | X | X | X |