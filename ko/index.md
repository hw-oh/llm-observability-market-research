---
layout: default
title: W&B Weave 경쟁사 인텔리전스 보고서
---

# Competitor Intel Bot

[상세 비교](./comparison) · [제품 세부 정보](./competitor-detail) · [경쟁 인텔리전스 (내부)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 최신 보고서

<!-- LATEST_REPORT_START -->

[📋 최신 보고서 (2026-02-11)](./reports/2026-02-11.md)


- LangSmith와 Langfuse는 '에이전트 시각화' 분야에서 우위를 점하고 있으며, 전용 그래프 뷰와 상태 디버거(예: LangGraph Studio)를 제공하여 Weave의 선형 트레이스 트리보다 복잡한 루핑 에이전트에 대해 더 나은 이해도를 제공합니다.
- Braintrust와 Helicone은 '게이트웨이' 기능(캐싱, 속도 제한, 프록시)으로 성공적인 차별화를 꾀하며 관측성을 인프라 계층으로 확장하고 있습니다. 이는 현재 Weave에 부족한 기능입니다.
- Weave와 W&B Training의 통합은 여전히 가장 강력한 경쟁 우위로 남아 있으며, Arize Phoenix나 LangSmith와 같은 독립형 경쟁사가 기본적으로 복제할 수 없는 고유한 '프로덕션-투-파인튜닝(Production-to-Fine-tuning)' 워크플로우를 제공합니다.
- Logfire는 '매직' 자동 계측(auto-instrumentation)을 통해 Python/Pydantic 개발자 세그먼트를 빠르게 점유하고 있으며, 벤더 SDK보다 표준 라이브러리 통합을 선호하는 코드 우선 엔지니어링 팀들 사이에서 Weave의 채택을 위협하고 있습니다.
- LangSmith와 Braintrust는 '휴먼 인 더 루프(Human-in-the-Loop)' 워크플로우(주석 큐, 칸반 리뷰)를 크게 성숙시켰으며, 이는 수동 평가 및 데이터 큐레이션 사용 사례에서 Weave와의 격차를 만들고 있습니다.
- 시장은 '인프라/게이트웨이' 제공업체(Helicone, Braintrust)와 '워크플로우/에이전트' 플랫폼(LangSmith, Langfuse)으로 양분되고 있습니다. Weave는 샌드위치 압박을 피하기 위해 '모델 개선(Model Improvement)' 플랫폼으로서의 입지를 명확히 해야 합니다.

> Weave는 W&B 에코시스템을 통한 **파인튜닝 피드백 루프**에서 앞서 나가고 있지만, **에이전트 워크플로우 시각화** 측면에서는 **LangSmith**, **엔터프라이즈 게이트웨이 인프라** 측면에서는 **Braintrust**로부터 거센 압박을 받고 있습니다.


<!-- LATEST_REPORT_END -->

## 신규 기능 (최근 30일)

### Weave

- **Stats Clickhouse 쿼리 레이어**: 통계 데이터 처리를 위한 백엔드 쿼리 레이어 개선으로 대시보드 성능이 향상될 것으로 보입니다. (2026-01-20)
- **OTel 내보내기 개선**: 안정성 및 표준 준수를 위해 OpenTelemetry 내보내기를 비동기 삽입(async inserts) 방식에서 변경했습니다. (2026-01-08)

### LangSmith

- **트레이스 미리보기 커스텀**: 사용자가 트레이스 테이블에 직접 표시될 입력 및 출력의 일부를 구성할 수 있게 되어, 커스텀 데이터 구조의 사용성이 개선되었습니다. (2026-02-06)
- **LangSmith 셀프 호스팅 v0.13**: 클라우드 버전과의 기능 동등성, 성능 및 운영 제어 능력을 향상시킨 셀프 호스팅 고객용 주요 릴리스입니다. (2026-01-16)

### Arize Phoenix

- **Claude Opus 4.6 지원**: Playground에서 Claude Opus 4.6 모델 지원을 추가했습니다. (2026-02-09)
- **도구 선택 평가기(Tool Selection Evaluator)**: 도구 선택 로직을 평가하기 위한 전용 평가기가 새로 추가되었습니다. (2026-02-06)
- **충실도 평가기(Faithfulness Evaluator)**: 더 나은 RAG 평가를 위해 FaithfulnessEvaluator를 추가하고 HallucinationEvaluator를 지원 중단했습니다. (2026-02-02)
- **도구 호출 정확도 지표**: 트레이스 내 도구 호출의 정확도를 추적하는 새로운 지표가 추가되었습니다. (2026-02-02)
- **커스텀 메트릭 커서 규칙**: 커서 규칙을 통해 새로운 내장 지표(LLM 분류)를 생성할 수 있는 UI 업데이트가 진행되었습니다. (2026-01-21)

### Braintrust

- **트레이스 레벨 스코어러**: 커스텀 코드 스코어러가 이제 전체 실행 트레이스에 접근하여 다단계 워크플로우와 에이전트 동작을 평가할 수 있습니다. (2026-02)
- **LangSmith 통합**: LangSmith 트레이스를 Braintrust로 라우팅하는 래퍼를 제공하여 병행 사용 또는 마이그레이션을 지원합니다. (2026-02)
- **Cursor 및 MCP 통합**: Cursor 에디터 및 Model Context Protocol과의 통합을 통해 IDE에서 로그를 쿼리하고 평가(evals)를 실행할 수 있습니다. (2026-02)
- **자동 계측 (Python/Ruby/Go)**: Python, Ruby, Go SDK에서 주요 제공업체에 대한 코드 없는 트레이싱을 지원합니다. (2026-01)
- **Temporal 통합**: 분산 에이전트 관측성을 위해 Temporal 워크플로우 및 액티비티의 자동 트레이싱을 지원합니다. (2026-01)

### Langfuse

- **트레이스 출력 수정**: 파인튜닝 데이터셋 구축을 위해 트레이스 뷰에서 직접 개선된 버전의 LLM 출력을 캡처합니다. (2026-01-14)
- **단일 관찰 평가**: 트레이스 내 개별 관찰(observation)에 대해 평가를 실행하는 기능을 지원합니다. (2026-02-09)
- **생각 / 추론 렌더링**: 트레이스 상세 정보에서 모델 출력의 '생각(thinking)' 또는 추론 부분을 시각적으로 렌더링합니다. (2026-02-09)
- **조직 감사 로그 뷰어**: 보안 및 액세스 이벤트를 추적하기 위한 조직 수준의 감사 로그 뷰어가 새로 추가되었습니다. (2026-02-09)

### Logfire

- **프로젝트 마이그레이션을 위한 멀티 토큰 지원**: 프로젝트 마이그레이션 워크플로우 중 여러 토큰을 처리하는 기능을 추가했습니다. (2026-02-04)
- **OTel Gen AI 시맨틱 컨벤션**: OpenTelemetry Gen AI 시맨틱 컨벤션 스칼라 속성에 대한 지원을 추가했습니다. (2026-01-28)
- **pytest 통합**: 테스트 실행 트레이스 캡처를 위한 pytest 기본 통합을 지원합니다. (2026-01-26)
- **DSPy 통합**: DSPy 프레임워크에 대한 계측 지원을 추가했습니다. (2026-01-16)
- **Claude SDK 계측**: Anthropic Claude SDK를 위한 전용 계측 기능을 추가했습니다. (2026-01-12)


## 보고서 아카이브

<!-- REPORT_ARCHIVE_START -->

| 날짜 | 보고서 |
|------|--------|
| 2026-02-11 | [보고서 보기](./reports/2026-02-11.md) |
| 2026-02-10 | [보고서 보기](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)