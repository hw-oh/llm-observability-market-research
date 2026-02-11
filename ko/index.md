---
layout: default
title: W&B Weave 경쟁사 인텔리전스 보고서
---

# 경쟁사 인텔리전스 봇 (Competitor Intel Bot)

[상세 비교](./comparison) · [제품 상세](./competitor-detail) · [경쟁 인텔리전스 (내부)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 최신 보고서

<!-- LATEST_REPORT_START -->

[📋 최신 보고서 (2026-02-11)](./reports/2026-02-11.md)


- Weave는 2026년 2월 오디오 모니터(Audio Monitors) 출시를 통해 멀티모달 기능을 차별화하고 있으며, 이는 LangSmith 및 Arize Phoenix와 같은 경쟁사들의 텍스트 중심 평가 포커스를 넘어서는 행보입니다.
- Weave Playground에 커스텀 LoRA를 통합함으로써 W&B만의 고유한 '훈련에서 추론까지(Training-to-Inference)'의 해자를 강화했습니다. 이는 Langfuse, Logfire와 같은 순수 관측성(Observability) 도구들이 따라올 수 없는 미세 조정(Fine-tuned) 모델 평가 워크플로우를 제공합니다.
- LangSmith와 Langfuse는 복잡한 워크플로우를 위한 전용 그래프 뷰를 통해 '에이전트 시각화(Agent Visualization)' 분야에서 우위를 점하고 있습니다. Weave의 선형 트레이스(Trace) 뷰는 정교한 에이전트 루프를 디버깅하기에는 다소 뒤처진 느낌을 줄 위험이 있습니다.
- Braintrust와 Langfuse는 전용 '어노테이션 큐(Annotation Queues)'와 칸반(Kanban) 뷰를 통해 인간 참여형(Human-in-the-Loop, HITL) 워크플로우를 전문화했으며, 이는 대규모 수동 라벨링 작업에서 Weave와의 격차를 만들고 있습니다.
- Arize Phoenix는 로컬 우선 기능(CLI, 노트북 지원)과 특화된 '도구 선택(Tool Selection)' 메트릭을 통해 'AI 엔지니어' 페르소나를 공격적으로 공략하며, 실험 단계에서의 Weave의 지배력에 도전하고 있습니다.
- Helicone과 Braintrust는 비용에 민감한 엔지니어링 팀을 공략하기 위해 'AI 프록시' 아키텍처(캐싱, 속도 제한)를 계속 활용하고 있으며, 이는 Weave의 SDK 기반 접근 방식으로는 해결하지 못하는 기능입니다.

> Weave는 독보적인 LoRA 및 멀티모달 기능을 통해 '훈련에서 추론까지' 이어지는 플라이휠에서 앞서 나가고 있으나, 에이전트 시각화 및 인간 참여형 어노테이션 워크플로우 측면에서는 LangSmith와 Langfuse로부터 거센 압박을 받고 있습니다.


<!-- LATEST_REPORT_END -->

## 신규 기능 (최근 30일)

### [Weave](https://app.getbeamer.com/weave/en)

- **오디오 모니터 (Audio monitors)**: LLM 심사위원을 사용하여 오디오 출력(MP3/WAV)을 평가하는 기능을 지원하여 보이스 에이전트에 대한 관측성을 확보했습니다. (2026-02-01) [[문서]](https://wandb.ai/onlineinference/genai-research/reports/A-guide-to-LLM-debugging-tracing-and-monitoring--VmlldzoxMzk1MjAyOQ)
- **동적 리더보드 (Dynamic Leaderboards)**: 지속적인 필터링 및 커스터마이징 옵션을 갖춘 평가 기반 자동 생성 리더보드입니다. (2026-01-29) [[문서]](https://wandb.ai/onlineinference/genai-research/reports/A-guide-to-LLM-debugging-tracing-and-monitoring--VmlldzoxMzk1MjAyOQ)
- **Playground 내 커스텀 LoRA**: Weave Playground에서 직접 미세 조정된 커스텀 LoRA 가중치를 로드하고 테스트할 수 있는 기능입니다. (2026-01-16) [[문서]](https://wandb.ai/onlineinference/genai-research/reports/A-guide-to-LLM-debugging-tracing-and-monitoring--VmlldzoxMzk1MjAyOQ)

### [LangSmith](https://changelog.langchain.com/feed.rss)

- **트레이스 미리보기 커스터마이징**: UI에서 트레이스가 미리 보이는 방식을 사용자 정의할 수 있는 기능입니다. (2026-02-06)
- **LangSmith 셀프 호스팅 v0.13**: 셀프 호스팅 엔터프라이즈 버전 업데이트입니다. (2026-01-16)
- **클라이언트 라이브러리 v0.7.1**: 안정성 향상 및 OIDC 지원을 위한 JS/Python SDK 업데이트입니다. (2026-02-10)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 지원**: Playground에서 Anthropic의 Claude Opus 4.6 모델 지원 및 자동 비용 추적 기능을 추가했습니다. (2026-02-09) [[문서]](https://arize.com/docs/phoenix/release-notes)
- **도구 선택 및 호출 평가기 (Tool Selection & Invocation Evaluators)**: 에이전트가 올바른 도구를 선택했는지, 유효한 파라미터로 호출했는지 판단하는 새로운 특화 평가기입니다. (2026-01-31) [[문서]](https://arize.com/docs/phoenix/release-notes)
- **구성 가능한 이메일 추출 (OAuth2)**: Azure AD/Entra ID 통합을 위한 커스텀 이메일 추출 경로(예: preferred_username) 지원입니다. (2026-01-28) [[문서]](https://arize.com/docs/phoenix/release-notes)
- **프롬프트/데이터셋용 CLI 명령어**: 프롬프트와 데이터셋을 나열, 조회 및 파이핑할 수 있는 새로운 CLI 명령어를 통해 터미널 기반 워크플로우를 지원합니다. (2026-01-22) [[문서]](https://arize.com/docs/phoenix/release-notes)
- **스팬 연관 데이터셋 생성**: 원본 소스 스팬(Span)과의 양방향 링크를 유지하면서 트레이스로부터 데이터셋을 생성하는 기능입니다. (2026-01-21) [[문서]](https://arize.com/docs/phoenix/release-notes)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **트레이스 레벨 스코어러 (Trace-level scorers)**: 커스텀 코드 스코어러가 전체 실행 트레이스에 접근하여 다단계 워크플로우와 에이전트 동작을 평가할 수 있습니다. (2026-02) [[문서]](https://braintrust.dev/docs/changelog)
- **LangSmith 통합**: LangSmith 트레이스를 Braintrust로 라우팅하여 병행 사용이나 마이그레이션을 지원하는 실험적 래퍼입니다. (2026-02) [[문서]](https://braintrust.dev/docs/changelog)
- **자동 인스트루멘테이션 (Python/Ruby/Go)**: Python, Ruby, Go SDK에서 대부분의 제공자에 대해 코드 수정 없는 트레이싱을 지원합니다. (2026-01) [[문서]](https://braintrust.dev/docs/changelog)
- **Temporal 통합**: Temporal 워크플로우 및 액티비티 자동 트레이싱을 통해 워커 간 분산 트레이스를 캡처합니다. (2026-01) [[문서]](https://braintrust.dev/docs/changelog)
- **리뷰용 칸반 레이아웃**: 드래그 앤 드롭 카드를 통해 플래그가 지정된 스팬의 상태를 관리하는 새로운 UI입니다. (2026-01) [[문서]](https://braintrust.dev/docs/changelog)

### [Langfuse](https://langfuse.com/changelog)

- **트레이스용 수정된 출력 (Corrected Outputs)**: 트레이스 뷰에서 직접 개선된 버전의 LLM 출력을 캡처하여 미세 조정 데이터셋을 구축합니다. (2026-01-14) [[문서]](https://langfuse.com/changelog)
- **추론/생각 트레이스 지원**: 트레이스 상세 정보에서 생각/추론 프로세스를 렌더링하며(v3.148.0), DeepSeek과 같은 모델을 지원합니다. (2026-01-27) [[문서]](https://github.com/langfuse/langfuse/pull/11615)
- **단일 관측 평가 (Single Observation Evals)**: 단일 관측 단위에 대해 평가를 실행하는 기능을 지원합니다(v3.150.0). (2026-02-09) [[문서]](https://github.com/langfuse/langfuse/pull/11547)

### [Logfire](https://logfire.pydantic.dev/docs/release-notes)

- **프로젝트 마이그레이션을 위한 멀티 토큰 지원**: 프로젝트 마이그레이션 워크플로우를 용이하게 하기 위해 여러 토큰 사용 기능을 추가했습니다. (2026-02-04) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **OTel Gen AI 시맨틱 컨벤션**: OpenTelemetry Gen AI 시맨틱 컨벤션 스칼라 속성에 대한 지원을 추가했습니다. (2026-01-28) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **Pytest 통합**: 테스트 실행 트레이싱을 위한 pytest 네이티브 통합입니다. (2026-01-26) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **DSPy 통합**: DSPy 프레임워크에 대한 인스트루멘테이션 지원을 추가했습니다. (2026-01-16) [[문서]](https://logfire.pydantic.dev/docs/release-notes)


## 보고서 아카이브

<!-- REPORT_ARCHIVE_START -->

| 날짜 | 보고서 |
|------|--------|
| 2026-02-11 | [보고서 보기](./reports/2026-02-11.md) |
| 2026-02-10 | [보고서 보기](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)