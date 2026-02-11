---
layout: default
title: W&B Weave 경쟁사 인텔리전스 보고서
---

# Competitor Intel Bot

[상세 비교](./comparison) · [제품 세부 정보](./competitor-detail) · [경쟁 인텔리전스 (내부)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 최신 보고서

<!-- LATEST_REPORT_START -->

[📋 최신 보고서 (2026-02-11)](./reports/2026-02-11.md)


- Weave는 Audio Monitors 출시(2026년 2월)를 통해 보이스 에이전트(Voice Agent) 시장에서 핵심적인 차별화 요소를 확보하며, 텍스트 중심의 경쟁사인 Langfuse 및 LangSmith와의 격차를 벌렸습니다.
- LangSmith의 '배포(Deployment)'(인프라)로의 전략적 전환과 Braintrust의 'AI Proxy'는 경쟁사들이 트래픽 경로를 장악함에 따라 Weave를 수동적인 관찰자 역할로 전락시킬 위험이 있습니다.
- Arize Phoenix와 Braintrust는 전문화된 '도구 선택(Tool Selection)' 지표와 '트레이스 레벨 스코어러(Trace-level scorers)'를 통해 에이전트 평가의 기준을 높이고 있으며, 이는 Weave의 일반적인 스코어러 프레임워크에 도전 과제가 되고 있습니다.
- Weave의 'Dynamic Leaderboards'는 Langfuse의 정적인 대시보드에 대응하는 강력한 대안을 제공하며, 모델 비교를 위한 우수한 유연성을 보여줍니다.
- Logfire의 깊이 있는 Pydantic 통합과 SQL 기반 분석은 UI 중심 워크플로우보다 코드 중심 디버깅을 선호하는 Python 네이티브 엔지니어링 팀들 사이에서 Weave의 점유율을 지속적으로 잠식하고 있습니다.
- Braintrust의 새로운 Cursor IDE 통합은 '에디터 내 관측성(In-Editor Observability)'으로의 변화를 예고하며, Weave의 노트북 중심 개발 루프를 우회할 가능성이 있습니다.

> Weave는 멀티모달(오디오) 관측성 및 모델 학습 통합 분야에서 앞서 나가고 있으나, 에이전트 인프라 측면에서는 LangSmith, 엔터프라이즈 프록시 기능 측면에서는 Braintrust로부터 거센 압박을 받고 있습니다.


<!-- LATEST_REPORT_END -->

## 신규 기능 (최근 30일)

### [Weave](https://app.getbeamer.com/weave/en)

- **Audio monitors**: 텍스트와 함께 오디오 출력을 관찰하고 판단하는 모니터 생성 기능을 지원하여 보이스 에이전트 평가를 가능하게 함. (2026-02-01)
- **Dynamic Leaderboards**: 사용자 정의 필터와 풍부한 시각화 옵션을 갖춘 평가 결과 기반 자동 생성 리더보드. (2026-01-29)
- **Custom LoRAs in Playground**: W&B Artifacts의 사용자 정의 미세 조정 LoRA 가중치를 Weave Playground에서 직접 사용 가능. (2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **Customize trace previews**: 트레이스 미리보기 창을 커스터마이징하여 관련 메타데이터나 입출력을 한눈에 볼 수 있는 기능. (2026-02-06)
- **Google Gen AI Wrapper**: 수동 인스트루멘테이션 없이 Google Gen AI 모델을 트레이싱할 수 있는 새로운 SDK 래퍼. (2026-01-31)
- **LangSmith Self-Hosted v0.13**: 안정성 개선 및 클라우드 버전의 신규 기능이 포함된 업데이트된 셀프 호스팅 릴리스. (2026-01-16)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 지원**: 확장된 사고(thinking) 파라미터와 정확한 비용 추적을 지원하는 Anthropic 최신 모델용 Playground 지원. (2026-02-09) [[문서]](https://docs.arize.com/phoenix/release-notes)
- **Tool Selection & Invocation Evaluators**: 에이전트가 올바른 도구를 선택했는지, 유효한 파라미터로 호출했는지 평가하는 새로운 전문 평가 도구. (2026-01-31) [[문서]](https://docs.arize.com/phoenix/release-notes)
- **프롬프트/데이터셋용 CLI 명령**: 터미널에서 프롬프트 목록 조회, 보기, AI 어시스턴트로 전달 및 데이터셋/실험 관리를 지원하는 포괄적인 CLI 지원. (2026-01-22) [[문서]](https://docs.arize.com/phoenix/release-notes)
- **Span 링크를 포함한 Trace-to-Dataset**: 원본 소스 스팬과의 양방향 링크를 유지하면서 프로덕션 트레이스로부터 큐레이션된 데이터셋을 생성하는 기능. (2026-01-21) [[문서]](https://docs.arize.com/phoenix/release-notes)
- **트레이스와 함께 어노테이션 내보내기**: 오프라인 분석을 위해 수동 라벨 및 평가 점수와 함께 트레이스를 내보내는 CLI 지원. (2026-01-19) [[문서]](https://docs.arize.com/phoenix/release-notes)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **Trace-level scorers**: 커스텀 코드 스코어러가 전체 실행 트레이스에 접근하여 다단계 워크플로우와 에이전트 동작을 평가할 수 있음. (2026-02) [[문서]](https://braintrust.dev/docs/changelog)
- **LangSmith 통합**: 트레이스를 LangSmith와 Braintrust에 병렬로 전송하거나 Braintrust로 완전히 마이그레이션할 수 있는 래퍼. (2026-02) [[문서]](https://braintrust.dev/docs/changelog)
- **Cursor 통합**: 자연어를 통해 로그를 쿼리하고 실험을 실행할 수 있는 Cursor 에디터용 Braintrust 확장 프로그램. (2026-02) [[문서]](https://braintrust.dev/docs/changelog)
- **자동 인스트루멘테이션 (Python, Ruby, Go)**: Python, Ruby, Go 애플리케이션을 위한 코드 수정 없는 트레이싱 지원. (2026-01) [[문서]](https://braintrust.dev/docs/changelog)
- **Temporal 통합**: 부모-자식 관계 매핑을 통한 Temporal 워크플로우 및 액티비티 자동 트레이싱. (2026-01) [[문서]](https://braintrust.dev/docs/changelog)

### [Langfuse](https://langfuse.com/changelog)

- **Corrected Outputs for Traces**: 미세 조정 데이터셋 구축을 위해 트레이스 뷰에서 직접 개선된 버전의 LLM 출력을 캡처. (2026-01-14) [[문서]](https://langfuse.com/docs/observability/corrections)

### [Logfire](https://logfire.pydantic.dev/docs/release-notes)

- **프로젝트 마이그레이션을 위한 멀티 토큰 지원**: 원활한 프로젝트 마이그레이션을 돕기 위해 여러 토큰을 처리하는 기능 추가. (2026-02-04) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **OTel Gen AI 시맨틱 컨벤션**: OpenTelemetry Gen AI 시맨틱 컨벤션 스칼라 속성 지원 추가. (2026-01-28) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **Pytest 통합**: pytest 테스트 실행 내에서 원활한 트레이싱과 관측성을 제공하는 새로운 통합 기능. (2026-01-26) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **DSPy 통합**: DSPy 애플리케이션을 트레이싱하고 모니터링하기 위한 공식 통합. (2026-01-16) [[문서]](https://logfire.pydantic.dev/docs/release-notes)
- **Claude SDK 인스트루멘테이션**: Anthropic Claude SDK를 위한 전용 인스트루멘테이션 추가. (2026-01-12) [[문서]](https://logfire.pydantic.dev/docs/release-notes)


## 보고서 아카이브

<!-- REPORT_ARCHIVE_START -->

| 날짜 | 보고서 |
|------|--------|
| 2026-02-11 | [보고서 보기](./reports/2026-02-11.md) |
| 2026-02-10 | [보고서 보기](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)