---
layout: default
title: W&B Weave 경쟁사 인텔리전스 보고서
---

# Competitor Intel Bot

[상세 비교](./comparison) · [제품 상세](./competitor-detail) · [경쟁 인텔리전스 (내부)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 최신 보고서

<!-- LATEST_REPORT_START -->

[📋 최신 보고서 (2026-02-11)](./reports/2026-02-11.md)


- LangSmith는 'LangGraph Cloud'를 통해 수동적 관측성(observability)에서 능동적 런타임 관리로 공격적으로 이동하고 있으며, Weave가 데이터를 캡처하기 전에 전체 에이전트 라이프사이클을 선점하려 위협하고 있습니다.
- Braintrust는 IDE(Cursor)에 직접 통합하고 Weave가 현재 소홀히 하고 있는 백엔드 언어(Java, Go, C#)를 지원함으로써 '엔터프라이즈 엔지니어링' 측면에서 성공적으로 측면 공격을 수행하고 있습니다.
- Humanloop의 인수 및 서비스 종료는 이탈한 고객을 확보할 수 있는 즉각적인 전술적 기회를 창출하지만, Langfuse의 우수한 Prompt CMS는 이 마이그레이션에서 강력한 경쟁자가 될 것입니다.
- Arize Phoenix와 Langfuse는 강력한 '로컬 우선(Local-First)' 및 셀프 호스팅 스토리를 통해 바텀업 채택 퍼널을 압박하고 있으며, 이는 SaaS 도입을 주저하는 보안 중심 엔지니어들에게 어필하고 있습니다.
- Logfire는 Pydantic과의 깊은 통합을 통해 '풀스택' 트레이스(데이터베이스 + API + LLM)를 소유할 수 있게 되었으며, 이는 비 LLM 인프라 구성 요소에 대한 Weave의 가시성 부족을 드러냅니다.
- 에이전트 관측성이 주요 격전지가 되고 있습니다. LangSmith와 Langfuse는 현재 순환 워크플로우(cyclic workflows)에 대해 Weave의 표준 트레이스 뷰보다 뛰어난 전용 그래프/추론 시각화 기능을 출시했습니다.

> Weave는 모델 훈련에서 프로덕션에 이르는 리니지(lineage)에서 해자를 유지하고 있지만, 에이전트 오케스트레이션에서는 LangSmith로부터, 엔터프라이즈 개발자 워크플로우에서는 Braintrust로부터 심각한 압박을 받고 있습니다.


<!-- LATEST_REPORT_END -->

## 신규 기능 (최근 30일)

### LangSmith

- **트레이스 미리보기 사용자 정의**: 사용자가 트레이스 테이블에 직접 표시될 입력 및 출력의 일부를 구성할 수 있게 되어, 맞춤형 데이터 구조의 사용성이 개선되었습니다. (2026-02-06)
- **LangSmith 셀프 호스팅 v0.13**: 'Insights' 및 성능 개선을 포함하여 클라우드 버전과 기능 패리티를 확장한 셀프 호스팅 고객용 주요 릴리스입니다. (2026-01-16)
- **SDK v0.7.1**: 최신 LangChain 버전과의 호환성 보장 및 안정성이 향상된 Python/JS 클라이언트 라이브러리 업데이트입니다. (2026-02-10)

### Arize Phoenix

- **Claude Opus 4.6 지원**: 나란히 비교하기(side-by-side comparison)를 위해 Playground에 Claude Opus 4.6 지원이 추가되었습니다. (2026-02-09)
- **도구 선택 평가기(Tool Selection Evaluator)**: 에이전트의 도구 선택 로직 정확도를 측정하기 위해 특별히 설계된 새로운 평가기입니다. (2026-02-06)
- **FaithfulnessEvaluator**: 더 정교한 RAG 검사를 위해 새로운 FaithfulnessEvaluator가 도입되었습니다(HallucinationEvaluator는 지원 중단). (2026-02-02)
- **도구 호출 정확도 지표**: 에이전트가 도구를 얼마나 정확하게 호출하는지 추적하기 위한 특정 지표가 추가되었습니다. (2026-01-27)

### Braintrust

- **트레이스 기원 탐색**: 트레이스를 생성한 특정 프롬프트 버전이나 데이터셋 행으로 다시 연결하는 기능입니다. (2026-02)
- **트레이스 레벨 스코어러(Scorers)**: 커스텀 스코어러가 전체 실행 트레이스에 액세스하여 다단계 워크플로우와 에이전트 동작을 평가할 수 있습니다. (2026-02)
- **LangSmith 통합**: LangSmith 트레이싱 및 평가 호출을 Braintrust로 병렬 또는 독점적으로 라우팅하는 래퍼(Wrapper)입니다. (2026-02)
- **Cursor 통합**: 자연어를 통해 로그를 쿼리하고 실험 결과를 가져올 수 있는 Cursor 에디터용 Braintrust 확장 프로그램입니다. (2026-02)
- **자동 인스트루멘테이션 (Python/Ruby/Go)**: 주요 언어에 대한 코드 없는(Zero-code) 트레이싱 지원으로 초기 설정을 간소화했습니다. (2026-01)

### Langfuse

- **트레이스 수정 출력(Corrected Outputs)**: 파인튜닝 데이터셋 구축을 위해 트레이스 뷰에서 직접 개선된 버전의 LLM 출력을 캡처합니다. (2026-01-14)
- **관측 I/O 인라인 주석**: 트레이스 입력 및 출력 내의 특정 텍스트 선택 영역에 주석을 고정할 수 있습니다. (2026-01-07)

### Logfire

- **멀티 토큰 프로젝트 마이그레이션**: 여러 토큰을 사용하는 프로젝트의 마이그레이션 지원이 추가되었습니다. (2026-02-04)
- **OTel Gen AI 시맨틱 컨벤션**: OpenTelemetry Gen AI 시맨틱 컨벤션 스칼라 속성에 대한 지원이 추가되었습니다. (2026-01-28)
- **Pytest 통합**: pytest 실행 트레이싱을 위한 네이티브 통합이 추가되었습니다. (2026-01-26)
- **DSPy 통합**: DSPy 프레임워크에 대한 인스트루멘테이션 지원이 추가되었습니다. (2026-01-16)
- **Claude SDK 인스트루멘테이션**: Anthropic Claude SDK를 위한 전용 인스트루멘테이션이 추가되었습니다. (2026-01-12)


## 보고서 아카이브

<!-- REPORT_ARCHIVE_START -->

| 날짜 | 보고서 |
|------|--------|
| 2026-02-11 | [보고서 보기](./reports/2026-02-11.md) |
| 2026-02-10 | [보고서 보기](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)