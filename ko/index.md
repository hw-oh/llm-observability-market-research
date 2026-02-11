---
layout: default
title: W&B Weave 경쟁사 인텔리전스 보고서
---

# Competitor Intel Bot

[상세 비교](./comparison) · [제품 세부 정보](./competitor-detail) · [경쟁 인텔리전스 (내부)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 최신 보고서

<!-- LATEST_REPORT_START -->

[📋 최신 보고서 (2026-02-11)](./reports/2026-02-11.md)


- Weave의 Audio Monitors 도입(2026년 2월)은 LangSmith 및 Langfuse와 같은 경쟁사들이 여전히 텍스트/도구 중심에 머물러 있는 것과 대조적으로 뚜렷한 멀티모달 우위를 점하게 합니다.
- MLflow의 'Continuous Online Monitoring' 및 'Judge Builder' 출시(2026년 1월)는 프로덕션-평가 루프를 공격적으로 공략하며, Databricks 고객들에게 '기본' 솔루션을 제공함으로써 Weave의 자동화 역량에 도전하고 있습니다.
- LangSmith는 네이티브 LangGraph 통합을 통해 에이전트 시각화 분야를 계속해서 주도하고 있습니다. Weave의 선형 트레이스 뷰는 LangSmith의 순환 그래프 뷰와 Arize Phoenix의 새로운 도구 전용 평가기들로부터 압박을 받고 있습니다.
- Braintrust는 '범용' 엔터프라이즈 지원(Java, Go, C# SDK)과 깊은 IDE 통합(Cursor)을 통해 성공적으로 차별화하고 있으며, 이는 대규모 다국어 엔지니어링 조직 내에서 Weave의 입지를 위협하고 있습니다.
- Langfuse의 'Prompt CMS'와 세분화된 비용 분석(ClickHouse 기반)은 비기술적 이해관계자와 비용에 민감한 팀을 지원하는 측면에서 Weave를 계속해서 앞서고 있습니다.
- Weave의 Playground 내 커스텀 LoRA 통합(2026년 1월)은 '학습에서 추론까지' 이어지는 독보적인 해자를 강화하며, 이는 순수 관측성 벤더(LangSmith, Arize Phoenix)들이 따라올 수 없는 역량입니다.

> Weave는 멀티모달 평가 및 학습-추론 워크플로우에서 앞서 나가고 있으나, 에이전트 시각화 측면에서는 LangSmith로부터, 자동화된 프로덕션 모니터링 측면에서는 MLflow로부터 거센 압박을 받고 있습니다.


<!-- LATEST_REPORT_END -->

## 신규 기능 (최근 30일)

### [Weave](https://app.getbeamer.com/wandb/en)

- **Audio Monitors**: 오디오 지원 LLM을 사용하여 텍스트와 함께 오디오 출력을 관찰하고 판단하는 모니터 생성 기능 지원. (2026-02-01)
- **Dynamic Leaderboards**: 영구적인 커스터마이징 및 CSV 내보내기 기능이 포함된 평가 기반 자동 생성 리더보드. (2026-01-29)
- **Custom LoRAs in Playground**: W&B Artifacts에서 미세 조정된 커스텀 LoRA 가중치를 Weave Playground로 직접 로드하여 추론하는 기능. (2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **Customize trace previews**: 대시보드에서 트레이스 미리보기가 표시되는 방식을 사용자가 커스터마이징할 수 있는 UI 업데이트. (2026-02-06)
- **LangSmith Self-Hosted v0.13**: 셀프 호스팅 엔터프라이즈 인프라 구성 요소 업데이트. (2026-01-16)

### [Langfuse](https://langfuse.com/changelog)

- **Corrected Outputs for Traces**: 미세 조정 데이터셋 구축을 위해 트레이스 뷰에서 직접 개선된 버전의 LLM 출력을 캡처. (2026-01-14)
- **Reasoning/Thinking Rendering**: 트레이스 상세 정보에서 모델 출력의 '사고(thinking)' 또는 '추론(reasoning)' 부분을 렌더링하는 새로운 UI 지원 (v3.148). (2026-01-20)
- **Org Audit Log Viewer**: 보안 및 컴플라이언스 가시성 향상을 위한 조직 수준의 감사 로그 뷰어 추가. (2026-01-20)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **Trace-level Scorers**: 커스텀 코드 스코어러가 전체 실행 트레이스에 접근하여 다단계 워크플로우 및 에이전트 동작을 평가할 수 있음. (2026-02)
- **LangSmith Integration**: 트레이싱 및 평가 호출을 LangSmith와 Braintrust에 병렬로 전송하거나 Braintrust로만 라우팅하는 래퍼(Wrapper). (2026-02)
- **Cursor Integration**: MCP를 통해 Cursor 에디터와 통합하여 자연어로 로그를 쿼리하고 실험 결과를 가져옴. (2026-02)
- **Auto-instrumentation (Py/Ruby/Go)**: Python, Ruby, Go 애플리케이션을 위한 제로 코드 트레이싱 지원 추가. (2026-01)
- **Temporal Integration**: 부모-자식 관계 매핑을 통한 Temporal 워크플로우 및 액티비티 자동 트레이싱. (2026-01)

### [MLflow](https://mlflow.org/releases)

- **Continuous Online Monitoring**: 유입되는 프로덕션 트레이스에 LLM judge를 자동으로 실행하여 품질 문제를 실시간으로 감지. (2026-01-29)
- **Dashboards for Agent Performance**: 에이전트 지연 시간, 요청 수, 도구 사용 요약을 모니터링하기 위한 사전 구축된 시각화 탭. (2026-01-29)
- **Judge Builder UI**: 배포 전 커스텀 LLM judge를 생성, 테스트 및 검증할 수 있는 노코드 인터페이스. (2026-01-29)
- **MemAlign Judge Optimizer**: 과거의 인간 피드백으로부터 평가 가이드라인을 학습하여 judge의 정확도를 향상시키는 알고리즘. (2026-01-29)
- **MLflow Assistant**: 트레이스 디버깅을 돕고 수정을 제안하는 Claude Code 기반의 제품 내 AI 챗봇. (2026-01-29)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 Support**: 확장된 사고 파라미터 지원 및 비용 추적 기능이 포함된 Anthropic의 최신 모델 지원 추가. (2026-02-09)
- **Tool Selection & Invocation Evaluators**: 에이전트가 올바른 도구를 선택하고 유효한 파라미터로 호출했는지 판단하는 전문 평가기. (2026-01-31)
- **CLI for Prompts & Datasets**: AI 코딩 어시스턴트에 최적화된, 터미널에서 프롬프트, 데이터셋, 실험을 직접 관리하는 새로운 CLI 명령. (2026-01-22)
- **Trace-to-Dataset with Span Links**: 원본 소스 스팬(span)에 대한 양방향 링크를 유지하면서 프로덕션 트레이스로부터 데이터셋을 생성하는 기능. (2026-01-21)
- **Export Annotations with Traces**: 오프라인 분석을 위해 트레이스와 함께 인간 및 LLM 주석을 내보내는 CLI 지원. (2026-01-19)


## 보고서 아카이브

<!-- REPORT_ARCHIVE_START -->

| 날짜 | 보고서 |
|------|--------|
| 2026-02-11 | [보고서 보기](./reports/2026-02-11.md) |
| 2026-02-10 | [보고서 보기](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)