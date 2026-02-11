---
layout: default
title: 홈
---

# Competitor Intel Bot

W&B Weave 경쟁사 제품 비교 리포트

[상세 비교표](./comparison) · [제품 상세분석](./competitor-detail)

## 최신 리포트

<!-- LATEST_REPORT_START -->

[📋 최신 리포트 (2026-02-11)](./reports/2026-02-11.md)


- 주요 시장 변화: Humanloop가 Anthropic에 인수됨에 따라 2025년 9월에 서비스를 종료합니다. 이는 안정적인 프롬프트 관리 및 평가 대안을 찾는 기존 기업 고객들을 Weave로 유입시킬 수 있는 즉각적이고 우선순위가 높은 기회를 창출합니다.
- '프록시 vs 비동기'의 대립: Braintrust와 Helicone과 같은 경쟁사들은 비용 제어, 캐싱, 속도 제한(Rate limiting) 측면에서 우위를 점하기 위해 게이트웨이/프록시 아키텍처에 집중하고 있습니다. 반면, Weave, LangSmith, Arize Phoenix는 개발자 편의성을 위해 비동기 로깅을 우선시하며 시장에서 뚜렷한 아키텍처적 차이를 보이고 있습니다.
- 평가 성숙도 곡선: 선두 경쟁사들(LangSmith, Braintrust)은 단순한 'LLM-as-a-Judge'를 넘어 정교한 Human-in-the-Loop(HITL) 워크플로우로 진화하고 있으며, 수동 검토를 체계화하기 위해 전용 '어노테이션 큐(Annotation Queues)'와 '쌍체 비교(Pairwise Comparison)' UI를 도입하고 있습니다.
- SQL 기반 관측성(Observability)의 부상: Logfire와 Braintrust(BTQL)는 트레이스 조회를 위해 SQL 방식의 쿼리 언어를 제공함으로써 차별화를 꾀하고 있습니다. 이는 경직된 대시보드보다 유연하고 코드 중심적인 분석을 원하는 파워 유저들에게 어필하고 있습니다.
- 에이전트 특화 도구: 시장은 일반적인 LLM 트레이싱에서 '에이전트' 관측성으로 이동하고 있습니다. LangSmith, Langfuse, Logfire는 모두 도구 호출(Tool calling), 다단계 추론 루프, 서브 에이전트 중첩을 위한 전문화된 시각화 기능을 출시했습니다.
- OpenTelemetry 표준화: Arize Phoenix, Langfuse, Logfire는 OpenTelemetry(OTel) 및 OpenInference를 표준으로 강력하게 밀어붙이고 있으며, 벤더 중립적인 인스트루멘테이션(Instrumentation)을 약속하며 독자적인 SDK에 도전하고 있습니다.
- 언어 생태계 확장: Braintrust는 Java, Go, Ruby, C#용 네이티브 SDK를 출시하며 언어 지원 측면에서 경쟁사들을 앞서고 있으며, 다양한 언어를 사용하는 기업 환경에서 최적의 선택지로 자리매김하고 있습니다.

> Weave는 전체 라이프사이클을 관리하는 ML 팀에게 여전히 최고의 선택지이지만, 비용 제어 측면에서는 프록시 기반 게이트웨이로부터, 표준화 측면에서는 OTel 네이티브 도구들로부터 거센 압박을 받고 있습니다.


<!-- LATEST_REPORT_END -->

## 리포트 아카이브

<!-- REPORT_ARCHIVE_START -->

| 날짜 | 리포트 |
|------|--------|
| 2026-02-11 | [리포트 보기](./reports/2026-02-11.md) |
| 2026-02-10 | [리포트 보기](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)