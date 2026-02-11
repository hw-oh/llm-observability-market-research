---
layout: default
title: W&B Weave 경쟁사 인텔리전스 보고서
---

# 경쟁사 인텔리전스 봇 (Competitor Intel Bot)

[상세 비교](./comparison) · [제품 상세](./competitor-detail) · [경쟁 인텔리전스 (내부)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 최신 보고서

<!-- LATEST_REPORT_START -->

[📋 최신 보고서 (2026-02-11)](./reports/2026-02-11.md)


- Weave는 오디오 모니터(2026년 2월) 출시를 통해 멀티모달 관측성(observability) 분야에서 선점 효과를 확보했으며, LangSmith 및 Langfuse와 같은 텍스트 중심 경쟁사들과 차별화했습니다.
- LangSmith는 복잡한 에이전트 워크플로우에서 여전히 주요 위협으로 남아 있으며, Weave의 현재 트레이스 트리 뷰가 아직 따라잡지 못한 순환 그래프 및 상태 머신에 대한 우수한 시각화를 제공합니다.
- Braintrust는 '데이터 플레인(Data Plane)' 아키텍처와 광범위한 SDK 지원(Java, Go, C#)을 통해 엔터프라이즈 측면을 성공적으로 공략하며, Weave의 Python/TS 중심 SDK가 놓치고 있는 백엔드 엔지니어링 팀을 확보하고 있습니다.
- '휴먼 인 더 루프(Human-in-the-Loop)' 격차가 벌어지고 있습니다. LangSmith, Langfuse, Braintrust는 모두 전용 '어노테이션 큐(Annotation Queues)' 또는 칸반 워크플로우를 출시한 반면, Weave는 리뷰를 위해 보다 일반적인 보드/테이블 인터페이스에 의존하고 있습니다.
- MLflow(v3.9)는 '저지 빌더(Judge Builder)'와 'MemAlign'을 통해 평가 격차를 공격적으로 좁혔으며, Databricks 네이티브 팀들을 위한 평가 기반 개발 루프에서 Weave의 지배력을 위협하고 있습니다.
- Arize Phoenix의 특화된 '도구 선택 평가기(Tool Selection Evaluators)' 출시는 시장이 세분화된 에이전트 구성 요소 테스트로 이동하고 있음을 시사하며, 이는 Weave가 에이전트 신뢰성 부문에서 대등함을 유지하기 위해 우선순위를 두어야 할 분야입니다.

> Weave는 멀티모달 지원 및 학습에서 추론까지의 연속성 측면에서 앞서 나가고 있지만, 에이전트 워크플로우 시각화에서는 LangSmith로부터, 엔터프라이즈 데이터 프라이버시 아키텍처에서는 Braintrust로부터 상당한 압박을 받고 있습니다.


<!-- LATEST_REPORT_END -->

## 신규 기능 (최근 30일)

### [Weave](https://app.getbeamer.com/wandb/en)

- **오디오 모니터 (Audio Monitors)**: 오디오 지원 LLM 저지를 사용하여 텍스트와 함께 오디오 출력을 관찰하고 판단하는 모니터 생성 지원. (2026-02-01)
- **동적 리더보드 (Dynamic Leaderboards)**: 모델/평가 필터에 따라 즉시 채워지는 평가(Evaluations) 내 자동 생성 리더보드. (2026-01-29)
- **플레이그라운드 내 커스텀 LoRA**: W&B Artifacts에서 커스텀 파인튜닝된 LoRA 가중치를 Weave 플레이그라운드에 직접 로드하고 테스트하는 기능. (2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **트레이스 미리보기 커스텀**: 리스트 뷰에서 트레이스 데이터가 미리 보이는 방식을 사용자가 설정할 수 있는 UI 업데이트. (2026-02-06)
- **SDK v0.7.1**: LangSmith 관측성 및 평가 플랫폼 연결을 위한 클라이언트 라이브러리 업데이트. (2026-02-10)

### [Langfuse](https://langfuse.com/changelog)

- **트레이스 출력 수정 (Corrected Outputs)**: 파인튜닝 데이터셋 구축을 위해 트레이스 뷰에서 직접 개선된 버전의 LLM 출력을 캡처. (2026-01-14)
- **관찰 I/O 인라인 코멘트**: 트레이스 입력 및 출력 내의 특정 텍스트 선택 영역에 코멘트 고정. (2026-01-07)
- **추론/생각 렌더링**: 트레이스 내 추론 모델(예: O1, R1)의 '생각(thinking)' 부분에 대한 특화된 UI 렌더링. (2026-02-01)
- **조직 감사 로그 뷰어**: 보안 및 컴플라이언스를 위한 조직 수준의 감사 로그 확인용 신규 UI. (2026-02-01)
- **단일 관찰 평가**: 전체 트레이스가 아닌 개별 관찰(observation) 단위로 평가 실행 가능. (2026-02-01)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **트레이스 레벨 스코어러**: 커스텀 코드 스코어러가 전체 실행 트레이스에 접근하여 다단계 워크플로우 및 에이전트 동작을 평가 가능. (2026-02)
- **LangSmith 통합**: 트레이스를 LangSmith와 Braintrust 양쪽으로 라우팅하거나 트래픽을 완전히 마이그레이션하는 래퍼(Wrapper). (2026-02)
- **Cursor 통합**: Cursor IDE에서 직접 로그 쿼리 및 실험 가져오기를 가능하게 하는 Braintrust MCP 서버 설정 확장 프로그램. (2026-02)
- **자동 인스트루멘테이션 (Python/Ruby/Go)**: Python, Ruby, Go SDK에 대한 제로 코드 트레이싱 지원 추가. (2026-01)
- **Temporal 통합**: Temporal 워크플로우 및 액티비티 자동 트레이싱으로 워커 간 분산 트레이스 캡처. (2026-01)

### [MLflow](https://mlflow.org/releases)

- **MLflow 어시스턴트**: UI 내에서 문제를 진단하고 수정을 제안하는 Claude Code 기반의 인제품 챗봇. (2026-01-29)
- **에이전트 성능 대시보드**: 에이전트 지연 시간, 요청 수, 품질 점수 모니터링을 위한 사전 구축된 차트. (2026-01-29)
- **MemAlign 저지 최적화 도구**: 과거 피드백으로부터 평가 가이드라인을 학습하여 저지 정확도를 향상시키는 알고리즘. (2026-01-29)
- **저지 빌더 UI**: 코드 없이 커스텀 LLM 저지 프롬프트를 생성, 테스트 및 검증하는 시각적 인터페이스. (2026-01-29)
- **지속적 온라인 모니터링**: 유입되는 프로덕션 트레이스에 대해 LLM 저지를 자동으로 실행하여 품질 문제를 실시간으로 감지. (2026-01-29)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 지원**: 정확한 비용 추적과 함께 플레이그라운드에서 Anthropic의 Claude Opus 4.6 모델 지원 추가. (2026-02-09)
- **도구 선택 및 호출 평가기**: 에이전트가 올바른 도구를 선택하고 유효한 파라미터로 호출했는지 평가하는 신규 특화 평가기. (2026-01-31)
- **Phoenix CLI 확장**: 터미널에서 직접 프롬프트, 데이터셋, 실험을 관리할 수 있는 포괄적인 CLI 명령. (2026-01-22)
- **스팬 링크를 포함한 트레이스-데이터셋 변환**: 계보(lineage) 확인을 위해 소스 스팬에 대한 양방향 링크를 유지하면서 트레이스로부터 데이터셋 생성 가능. (2026-01-21)
- **트레이스와 함께 어노테이션 내보내기**: 오프라인 분석을 위해 트레이스와 함께 사람 및 AI 어노테이션을 내보내는 CLI 지원. (2026-01-19)


## 보고서 아카이브

<!-- REPORT_ARCHIVE_START -->

| 날짜 | 보고서 |
|------|--------|
| 2026-02-11 | [보고서 보기](./reports/2026-02-11.md) |
| 2026-02-10 | [보고서 보기](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)