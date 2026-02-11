---
layout: default
title: W&B Weave 경쟁사 인텔리전스 보고서
---

# Competitor Intel Bot

[상세 비교](./comparison) · [제품 세부 정보](./competitor-detail) · [경쟁 인텔리전스 (내부)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 최신 보고서

<!-- LATEST_REPORT_START -->

[📋 최신 보고서 (2026-02-11)](./reports/2026-02-11.md)


- Weave는 멀티모달 지원(Audio Monitors)으로 차별화하고 있는 반면, 경쟁사들은 여전히 텍스트/도구 중심에 머물러 있어 보이스 에이전트 관측성(observability) 분야에서 우위를 점하고 있습니다.
- LangSmith와 Langfuse는 추론 단계 및 순환 그래프를 위한 특화된 시각화를 통해 '에이전틱 관측성(Agentic Observability)'을 공격적으로 심화하며 Weave의 트레이스 뷰를 압박하고 있습니다.
- Braintrust와 LangSmith는 전용 어노테이션 큐(Annotation Queues)를 통해 '휴먼 인 더 루프(Human-in-the-Loop)' 담론을 주도하고 있으며, 이는 Weave가 현재 덜 직접적으로 다루고 있는 워크플로우 기능입니다.
- Weave의 '다이내믹 리더보드(Dynamic Leaderboards)' 릴리스는 모델 비교를 자동화함으로써 Braintrust의 평가 성숙도에 대응하며, 엔터프라이즈 모델 선택의 핵심 니즈를 해결합니다.
- '오픈 표준'의 위협이 커지고 있으며, Arize Phoenix와 Logfire는 OpenTelemetry(OTLP)를 활용하여 특정 벤더에 종속되지 않는 인스트루멘테이션을 선호하는 팀들을 공략하고 있습니다.
- Weave는 W&B Training/Artifacts와의 깊은 통합을 통해 독보적인 방어적 해자를 유지하고 있으며, 경쟁사들이 내보내기(export)를 통해서만 지원할 수 있는 '파인튜닝을 통한 개선(Fix-by-Fine-tuning)' 루프를 네이티브로 제공합니다.
- LangSmith가 LangGraph Platform을 'Deployment'로 리브랜딩한 것은 런타임 레이어 점유로의 전환을 의미하며, 이는 순수 관측성 플레이어들을 범용화(commoditize)할 위협이 됩니다.

> Weave는 멀티모달 관측성 및 학습 통합 분야를 선도하고 있으나, 에이전트 시각화 측면에서는 LangSmith, 엔터프라이즈 평가 워크플로우 측면에서는 Braintrust로부터 구체적인 압박을 받고 있습니다.


<!-- LATEST_REPORT_END -->

## 신규 기능 (최근 30일)

### [Weave](https://app.getbeamer.com/weave/en)

- **Audio Monitors**: 텍스트와 함께 오디오 출력을 관찰하고 판단하는 모니터 생성 지원으로 보이스 에이전트 평가 가능. (2026-02-01)
- **Dynamic Leaderboards**: 지속적인 커스터마이징 및 CSV 내보내기가 가능한 평가 기반 자동 생성 리더보드. (2026-01-29)
- **Custom LoRAs in Playground**: W&B Artifacts의 커스텀 파인튜닝된 LoRA 가중치를 Weave Playground에서 직접 사용 가능. (2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **트레이스 미리보기 커스텀**: UI에서 트레이스가 미리 보이는 방식을 커스터마이징하여 분류(triage) 속도 향상. (2026-02-06) [[문서]](https://docs.smith.langchain.com/observability)
- **LangSmith Self-Hosted v0.13**: 안정성 개선 및 신규 기능이 포함된 셀프 호스팅 릴리스 업데이트. (2026-01-16) [[문서]](https://docs.smith.langchain.com/self_hosting)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 지원**: Playground에서 Anthropic의 Claude Opus 4.6 모델 지원 및 자동 비용 추적 추가. (2026-02-09) [[문서]](https://docs.arize.com/phoenix/release-notes)
- **도구 선택 및 호출 평가기**: 에이전트가 올바른 도구를 선택하고 유효한 파라미터로 호출했는지 평가하는 신규 특화 평가기. (2026-01-31) [[문서]](https://docs.arize.com/phoenix/release-notes)
- **프롬프트 및 데이터셋용 CLI**: 프롬프트/데이터셋의 목록 조회, 보기, 파이프 연결을 위한 CLI 명령어로 AI 코딩 어시스턴트와의 통합 지원. (2026-01-22) [[문서]](https://docs.arize.com/phoenix/release-notes)
- **트레이스 기반 데이터셋 생성**: 소스 스팬(span)과의 양방향 링크를 유지하면서 트레이스에서 직접 데이터셋을 생성하는 기능. (2026-01-21) [[문서]](https://docs.arize.com/phoenix/release-notes)
- **트레이스와 함께 어노테이션 내보내기**: 오프라인 분석을 위해 트레이스와 함께 인간 피드백 및 어노테이션을 내보내는 CLI 지원. (2026-01-19) [[문서]](https://docs.arize.com/phoenix/release-notes)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **트레이스 레벨 스코어러**: 커스텀 코드 스코어러가 전체 실행 트레이스에 접근하여 다단계 워크플로우 및 에이전트 동작을 평가 가능. (2026-02) [[문서]](https://braintrust.dev/docs/changelog)
- **LangSmith 통합 (실험적)**: LangSmith 트레이싱 및 평가 호출을 Braintrust로 라우팅하여 이중 로깅 또는 마이그레이션 지원. (2026-02) [[문서]](https://braintrust.dev/docs/changelog)
- **자동 인스트루멘테이션 (Python, Ruby, Go)**: Python, Ruby, Go SDK에서 대부분의 제공자에 대해 코드 수정 없는 트레이싱 지원. (2026-01) [[문서]](https://braintrust.dev/docs/changelog)
- **Temporal 통합**: Temporal 워크플로우 및 액티비티 자동 트레이싱으로 실행 스팬 및 분산 트레이스 캡처. (2026-01) [[문서]](https://braintrust.dev/docs/changelog)
- **트레이스 기원 탐색**: 로그의 트레이스에서 기원이 된 프롬프트나 데이터셋 행으로 연결하여 신속한 반복 작업 지원. (2026-02) [[문서]](https://braintrust.dev/docs/changelog)

### [Langfuse](https://langfuse.com/changelog)

- **생각 / 추론 렌더링**: 트레이스 상세 정보에서 생각의 사슬(CoT) 및 추론 부분을 명시적으로 렌더링 (v3.148.0). (2026-02-01)
- **단일 관찰 평가**: 전체 트레이스가 아닌 단일 관찰(observation) 단위로 평가 실행 지원 (v3.150.0). (2026-02-05)
- **트레이스용 수정된 출력**: 파인튜닝 데이터셋 구축을 위해 트레이스 뷰에서 직접 개선된 LLM 출력 버전을 캡처. (2026-01-14) [[문서]](https://langfuse.com/docs/observability/features/corrections)

### [Logfire](https://logfire.pydantic.dev/docs/release-notes)

- **프로젝트 마이그레이션을 위한 멀티 토큰 지원**: 프로젝트 마이그레이션을 용이하게 하기 위해 여러 토큰 사용 지원 추가. (2026-02-04) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **OTel Gen AI 시맨틱 컨벤션**: OpenTelemetry Gen AI 시맨틱 컨벤션 스칼라 속성 지원 추가. (2026-01-28) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **pytest 통합**: pytest 실행 내에서 관측성을 지원하는 신규 통합. (2026-01-26) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **DSPy 통합**: DSPy 프레임워크에 대한 네이티브 인스트루멘테이션 지원 추가. (2026-01-16) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **Claude SDK 인스트루멘테이션**: Anthropic Claude SDK를 위한 특정 인스트루멘테이션 추가. (2026-01-12) [[문서]](https://logfire.pydantic.dev/docs/release-notes)


## 보고서 아카이브

<!-- REPORT_ARCHIVE_START -->

| 날짜 | 보고서 |
|------|--------|
| 2026-02-11 | [보고서 보기](./reports/2026-02-11.md) |
| 2026-02-10 | [보고서 보기](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)