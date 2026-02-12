---
layout: default
title: LLM Observability — 제품 상세 정보
---

# LLM Observability — 제품 상세 정보
**날짜**: 2026-02-12 | **모델**: google/gemini-3-pro-preview

### W&B Weave

**개요**: W&B Weave는 LLM 실험, Eval, 그리고 프로덕션 모니터링 사이의 루프를 폐쇄하도록 설계된 개발자 중심의 툴킷입니다. Weights & Biases의 강력한 실험 트래킹 인프라를 활용하여 강력한 버전 관리, 커스텀 LLM-as-a-judge Eval, 그리고 커스텀 모델 및 LoRA와의 원활한 통합을 제공합니다.

**강점**:
- W&B의 성숙한 실험 트래킹 및 모델 레지스트리 에코시스템과의 깊은 통합
- Dynamic Leaderboards 및 Audio Monitors를 포함한 고급 Eval 기능
- 커스텀 LoRA 어댑터 및 Fine-tuning된 모델 테스트를 위한 원활한 지원
- 모든 아티팩트(프롬프트, 모델, 데이터셋)에 대한 강력한 버전 관리

**약점**:
- PII 마스킹과 같은 엔터프라이즈 컴플라이언스 기능에 대한 명시적인 문서 부족
- 복잡한 에이전트 메모리 상태에 대한 시각적 디버깅 강조 부족
- 토큰 레벨 분석이 비용 및 Latency 지표에 비해 덜 상세함

**최근 업데이트**:
- Audio Monitors: LLM judge를 사용하여 오디오 출력(MP3/WAV)을 관찰하고 판별하는 모니터 생성 지원 (2026-02-01)
- Dynamic Leaderboards: 지속적인 커스터마이징 및 CSV 내보내기가 가능한 Eval 결과 기반 자동 생성 리더보드 (2026-01-29)
- Playground에서의 커스텀 LoRA: W&B Artifacts의 커스텀 Fine-tuning된 LoRA 가중치를 Weave Playground에서 직접 사용 가능 (2026-01-16)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | Weave는 입력, 출력 및 중첩된 실행 트리를 자동으로 캡처하며 W&B 에코시스템에 깊이 통합된 강력한 핵심 Tracing 기능을 제공합니다. |
| Agent / RAG Observability | ●●○ | 중첩된 Span을 통한 RAG Eval 및 일반적인 에이전트 Tracing을 강력하게 지원하지만, 에이전트 메모리나 복잡한 상태 그래프에 대한 특정 시각화는 덜 강조됩니다. |
| Evaluation Integration | ●●● | Weave의 독보적인 카테고리로, Dynamic Leaderboards, 광범위한 LLM-as-a-judge 기능(오디오 포함), 데이터셋과의 긴밀한 통합이 특징입니다. |
| Monitoring & Metrics | ●●○ | 비용, Latency, 품질 지표에 집중된 견고한 모니터링 기능을 제공하며, 온라인 Eval을 위한 커스텀 모니터 정의가 가능합니다. |
| Experiment / Improvement Loop | ●●● | 버전 관리, 실험 트래킹, Eval 결과를 모델 Fine-tuning으로 다시 연결하기 위해 성숙한 W&B 플랫폼을 활용함으로써 이 분야에서 탁월합니다. |
| DevEx / Integration | ●●● | 다국어 SDK와 Playground에서 커스텀 LoRA 어댑터를 직접 테스트하는 독특한 기능을 통해 강력한 개발자 경험을 제공합니다. |
| Enterprise & Security | ●○○ | 다양한 배포 옵션(SaaS, 전용, 온프레미스)을 제공하지만, PII 마스킹 및 감사 로그와 같은 특정 컴플라이언스 기능은 공개 릴리스 노트에 상세히 나와 있지 않습니다. |


---

### LangSmith

**개요**: LangSmith는 LLM 애플리케이션을 위한 포괄적인 DevOps 플랫폼으로, 엔드 투 엔드 Observability, Eval 및 배포 기능을 제공합니다. 복잡한 에이전트 워크플로우와 RAG 파이프라인 Tracing에 탁월하며, 도구 사용, 비용, Latency에 대한 깊은 가시성을 제공하는 동시에 관리형 및 셀프 호스팅 배포 모델을 모두 지원합니다.

**강점**:
- LangChain 및 LangGraph 프레임워크와의 깊은 네이티브 통합
- 휴먼 어노테이션 및 LLM-as-a-judge를 포함한 포괄적인 Eval 스위트
- 엔터프라이즈를 위한 강력한 셀프 호스팅을 포함한 유연한 배포 옵션
- 복잡한 에이전트 워크플로우 및 계층적 Tracing에 대한 강력한 지원

**약점**:
- Trace 기반의 요금 모델은 대규모 애플리케이션에서 비용이 많이 들 수 있음
- 기능 세트의 복잡성이 단순한 유스케이스에는 과할 수 있음
- LangChain과 가장 긴밀하게 통합되어 있어, 커스텀 스택의 경우 더 많은 설정이 필요할 수 있음

**최근 업데이트**:
- Client Library v0.7.1: 플랫폼 연결을 위한 Python 및 JS 클라이언트 라이브러리 업데이트 (2026-02-10)
- Customize Trace Previews: UI에서 Trace 미리보기가 표시되는 방식을 커스터마이징하는 새로운 기능 (2026-02-06)
- Google Gen AI Wrapper: SDK에서 Google Gen AI 래퍼 내보내기 및 지원 (2026-01-31)
- Self-Hosted v0.13: 셀프 호스팅 배포 옵션을 위한 새 버전 출시 (2026-01-16)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | LangSmith는 특히 계층적이고 복잡한 에이전트 워크플로우에 최적화된 깊은 Tracing 기능과 함께 강력한 핵심 Observability를 제공합니다. |
| Agent / RAG Observability | ●●● | 이 플랫폼은 에이전트 및 RAG 아키텍처에 고도로 특화되어 도구, 검색 및 다단계 추론 프로세스에 대한 상세한 가시성을 제공합니다. |
| Evaluation Integration | ●●● | Eval은 핵심 기둥으로, 데이터셋 관리, 자동화된 LLM-as-a-judge 테스트, 휴먼 어노테이션 워크플로우를 위한 광범위한 도구를 갖추고 있습니다. |
| Monitoring & Metrics | ●●● | 비용, Latency, 에러 트래킹에 중점을 둔 포괄적인 모니터링 스위트로 프로덕션 배포에 적합합니다. |
| Experiment / Improvement Loop | ●●● | 강력한 프롬프트 엔지니어링, 실험 트래킹 및 데이터셋 관리 기능을 통해 긴밀한 피드백 루프를 촉진합니다. |
| DevEx / Integration | ●●● | 광범위한 프레임워크 지원, 견고한 SDK 및 현대적인 엔지니어링 워크플로우에 적합한 도구를 통해 우수한 개발자 경험을 제공합니다. |
| Enterprise & Security | ●●● | 강력한 보안 컴플라이언스, 유연한 배포 모델(셀프 호스팅 포함) 및 관리 제어 기능을 갖춘 엔터프라이즈급 솔루션입니다. |


---

### Langfuse

**개요**: Langfuse는 Observability, 프롬프트 관리 및 Eval을 결합한 오픈 소스 올인원 LLM 엔지니어링 플랫폼입니다. 에이전트 그래프 및 추론 Trace와 같은 기능으로 복잡한 에이전트 워크플로우를 지원하며, 셀프 호스팅 및 감사 로그를 포함한 강력한 엔터프라이즈 기능을 제공합니다.

**강점**:
- 높은 보안 환경에 적합한 포괄적인 오픈 소스 및 셀프 호스팅 가능 솔루션
- Eval 워크플로우(LLM-as-Judge, 휴먼 어노테이션)를 Trace와 직접 강력하게 통합
- 그래프 뷰 및 추론 단계 시각화를 포함한 고급 에이전트 Observability 기능
- 버전 관리, Playground 및 실험 트래킹을 갖춘 견고한 프롬프트 관리 시스템

**약점**:
- 직접적인 'Trace 재생' 기능이 Trace 뷰에서의 원클릭 액션이 아닌 Playground를 통한 수동 방식임
- Fine-tuning 지원이 학습 프로세스 관리보다는 데이터셋 생성에 국한됨
- 멀티 리전 클라우드 서비스를 제공하는 경쟁사에 비해 클라우드 리전 가용성이 명시적으로 상세하지 않음

**최근 업데이트**:
- 버전 관리된 데이터셋에서 실험 실행: 특정 타임스탬프의 데이터셋을 가져오고 재현성을 위해 과거 버전에서 실험 실행 (2026-02-11)
- Single Observation Evals: 개별 Observation에 직접 Eval을 추가하는 기능 (2026-02-05)
- Thinking / Reasoning 파트 렌더링: Trace 상세 정보에서 Chain-of-thought/추론 단계 시각화 (2026-01-30)
- 조직 감사 로그 뷰어: 조직 수준의 감사 로그를 보기 위한 UI (2026-01-30)
- Trace를 위한 수정된 출력: Fine-tuning 데이터셋 구축을 위해 Trace 뷰에서 개선된 버전의 LLM 출력을 캡처 (2026-01-14)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | OpenTelemetry를 기반으로 구축된 강력한 핵심 Tracing 기능으로, 복잡한 데이터에 특화된 뷰와 함께 실행 흐름, 비용, Latency에 대한 깊은 가시성을 제공합니다. |
| Agent / RAG Observability | ●●● | 에이전트 그래프, 도구 사용 및 내부 추론 단계를 시각화하는 특정 기능을 갖춘 고성능 에이전트 Observability를 제공합니다. |
| Evaluation Integration | ●●● | 자동화된 LLM judge, 휴먼 어노테이션 워크플로우 및 실험을 통한 체계적인 회귀 테스트를 지원하는 포괄적인 Eval 스위트입니다. |
| Monitoring & Metrics | ●●● | 커스터마이징 가능한 Dashboard와 비용 제어 및 토큰 사용량에 특화된 강력한 분석 기능을 제공합니다. |
| Experiment / Improvement Loop | ●●● | 견고한 프롬프트 관리, 데이터셋 버전 관리 및 모델 개선을 위한 수정 사항 캡처 도구를 특징으로 하는 우수한 반복 루프를 제공합니다. |
| DevEx / Integration | ●●● | 광범위한 SDK/프레임워크 지원과 기존 인프라에 잘 맞는 API 우선 아키텍처로 개발자 친화적입니다. |
| Enterprise & Security | ●●● | 오픈 소스 셀프 호스팅 옵션, RBAC 및 감사 로깅 기능을 통해 강력한 엔터프라이즈 태세를 갖추고 있습니다. |


---

### Braintrust

**개요**: Braintrust는 여러 언어에 걸친 강력한 SDK 지원과 함께 코드 우선, 개발자 중심 워크플로우를 강조하는 포괄적인 AI Observability 및 Eval 플랫폼입니다. Tracing, Eval(LLM-as-a-judge) 및 데이터셋 관리를 긴밀하게 통합하여 팀이 Playground 및 'Loop' AI 어시스턴트와 같은 기능을 사용하여 프롬프트와 모델을 신속하게 반복할 수 있도록 합니다.

**강점**:
- 포괄적인 Eval 에코시스템: Trace를 데이터셋, Playground 및 자동화된 Scoring 도구와 원활하게 연결
- 우수한 개발자 경험: 광범위한 SDK(Go, Ruby, Java, C#), 자동 Instrumentation 및 IDE 통합
- 통합 워크플로우: 프로덕션 Trace, 프롬프트 엔지니어링 및 실험 사이를 즉시 이동할 수 있는 긴밀한 통합
- 유연한 데이터 분석: 집계 및 커스텀 시각화 기능이 포함된 강력한 BTQL/SQL 쿼리
- 엔터프라이즈 준비성: 강력한 셀프 호스팅 옵션, RBAC 및 보안 제어

**약점**:
- 네이티브 Fine-tuning 부재: 엔드 투 엔드 MLOps 플랫폼에 비해 RLHF 또는 모델 Fine-tuning을 위한 내장 오케스트레이션이 부족함
- 제한된 시각적 빌더: 코드 우선 워크플로우에 집중하여 비기술 사용자를 위한 드래그 앤 드롭 프롬프트 플로우 빌더가 부족함
- 리전 지원: 최근 업데이트에서 멀티 리전 데이터 레지던시가 명시적으로 강조되지 않음
- 메모리 상태 시각화: 에이전트 Tracing은 강력하지만, 에이전트 메모리 상태에 대한 특정 시각화는 제한적임

**최근 업데이트**:
- Trace 레벨 Scoring 도구: 커스텀 코드 Scoring 도구가 이제 전체 실행 Trace에 액세스하여 다단계 워크플로우 및 에이전트 동작을 평가 가능 (2026-02-01)
- LangSmith 통합: Tracing 및 Eval 호출을 LangSmith와 Braintrust 모두에 보내거나 Braintrust로만 라우팅하는 래퍼 (2026-02-01)
- Cursor 통합: MCP 서버를 통해 Cursor IDE와 통합하여 에디터에서 직접 로그를 쿼리하고 실험 결과를 가져옴 (2026-02-01)
- 커스텀 뷰에서 첨부 파일 렌더링: 커스텀 Trace 뷰에서 이미지, 비디오 및 오디오를 직접 렌더링 지원 (2026-02-01)
- 자동 Instrumentation: Python, Ruby 및 Go 애플리케이션을 위한 제로 코드 Tracing 지원 (2026-01-29)
- Temporal 통합: 부모-자식 관계 매핑을 통한 Temporal 워크플로우 및 액티비티 자동 Tracing (2026-01-21)
- TrueFoundry 통합: OpenTelemetry를 통해 TrueFoundry AI Gateway에서 LLM Trace를 내보내는 통합 (2026-01-21)
- 리뷰를 위한 칸반 레이아웃: 플래그가 지정된 Span 및 리뷰 상태 관리를 위한 새로운 칸반 보드 뷰 (2026-01-21)
- Trace 페이지의 Loop: 분석 및 디버깅을 위해 개별 Trace 뷰에서 AI 어시스턴트 'Loop'를 직접 사용 가능 (2026-01-21)
- 원시 Trace 데이터 보기: 개별 Span 또는 Trace의 전체 JSON 표현을 보고 검색하는 기능 (2026-01-21)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | 복잡한 워크플로우 디버깅에 최적화된 깊은 계층적 Tracing 및 원시 데이터 액세스를 갖춘 강력한 핵심 Observability를 제공합니다. |
| Agent / RAG Observability | ●●○ | 도구 Tracing 및 다단계 Eval을 통해 에이전트 워크플로우를 강력하게 지원하지만, 시각화는 그래프 기반보다는 트리 기반입니다. |
| Evaluation Integration | ●●● | Trace, 데이터셋 및 자동화된 Scoring 도구 사이의 원활한 루프를 제공하는 Eval 분야의 시장 리더입니다. |
| Monitoring & Metrics | ●●● | BTQL 및 SQL을 통한 유연한 커스텀 지표와 함께 포괄적인 모니터링을 제공합니다. |
| Experiment / Improvement Loop | ●●● | 프롬프트, 데이터셋 및 실험을 일급 버전 관리 대상으로 취급하여 개선 루프를 탁월하게 지원합니다. |
| DevEx / Integration | ●●● | 광범위한 언어 지원, 자동 Instrumentation 및 IDE 통합을 통해 동급 최고의 개발자 경험을 제공합니다. |
| Enterprise & Security | ●●○ | 셀프 호스팅 및 액세스 제어를 갖춘 강력한 엔터프라이즈 기반을 갖추고 있지만, 특정 리전 지원과 같은 일부 컴플라이언스 기능은 덜 가시적입니다. |


---

### MLflow

**개요**: MLflow는 전통적인 MLOps에서 풀스택 GenAI 운영 체제로 확장된 포괄적인 오픈 소스 플랫폼으로, 엔드 투 엔드 Observability, 에이전트 Eval 및 프롬프트 엔지니어링을 특징으로 합니다. 최근 업데이트는 분산 Tracing을 사용한 에이전트 워크플로우, LLM judge를 사용한 지속적인 온라인 모니터링, AI 지원 디버깅 도구를 강조합니다.

**강점**:
- 전체 라이프사이클(Tracking, Registry, Evals, Observability)을 아우르는 통합 플랫폼
- 완전한 OpenTelemetry 호환성을 갖춘 벤더 중립적 아키텍처
- Judge Builder, MemAlign 및 지속적인 모니터링을 포함한 고급 Eval 에코시스템
- 광범위한 프레임워크 통합(LangChain, LlamaIndex 등) 및 SDK 지원
- 로컬에서 에어갭 엔터프라이즈 환경까지 이르는 유연한 배포 옵션

**약점**:
- 셀프 호스팅은 SaaS 전용 도구에 비해 상당한 인프라 관리가 필요함
- 클래식 ML과 GenAI를 모두 아우르는 광범위한 기능으로 인해 UI 복잡도가 높을 수 있음
- 대화형 '재생' 디버깅 워크플로우가 배치 Eval 및 비교에 비해 덜 강조됨
- 멀티 워크스페이스 RBAC와 같은 엔터프라이즈 기능은 매우 최근에 추가됨 (v3.10)

**최근 업데이트**:
- 조직 지원: 실험 및 리소스를 정리하기 위한 멀티 워크스페이스 환경 지원 (2026-02-12)
- MLflow Assistant: 컨텍스트 인식을 통해 문제를 디버깅하고 수정하는 Claude Code 기반의 인프로덕트 챗봇 (2026-01-29)
- 에이전트 성능 Dashboard: Latency, 요청 수, 품질 점수 및 도구 사용량을 모니터링하기 위한 사전 구축된 차트 (2026-01-29)
- MemAlign Judge Optimizer: 피드백으로부터 Eval 가이드라인을 학습하여 judge 정확도를 향상시키는 알고리즘 (2026-01-29)
- Judge Builder UI: 코드 없이 커스텀 LLM judge 프롬프트를 생성, 테스트 및 내보낼 수 있는 시각적 인터페이스 (2026-01-29)
- 지속적인 온라인 모니터링: 실시간 품질 평가를 위해 프로덕션의 유입 Trace에 대해 LLM judge를 자동으로 실행 (2026-01-29)
- 분산 Tracing: 엔드 투 엔드 가시성을 위해 컨텍스트 전파를 통해 여러 서비스에 걸친 요청을 추적 (2026-01-29)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | 입력, 출력 및 Latency에 대한 깊은 가시성을 통해 복잡하고 분산된 에이전트 워크플로우를 처리하는 강력한 OpenTelemetry 호환 Tracing 시스템입니다. |
| Agent / RAG Observability | ●●● | 도구 사용 분석, 분산 컨텍스트 전파 및 세션 레벨 트래킹을 위한 특정 기능을 통해 에이전트 시스템을 강력하게 지원합니다. |
| Evaluation Integration | ●●● | 시각적 Judge Builder, 자동화된 judge 최적화(MemAlign) 및 지속적인 프로덕션 모니터링을 특징으로 하는 업계 선도적인 Eval 기능입니다. |
| Monitoring & Metrics | ●●● | 포괄적인 모니터링 Dashboard는 수동 설정 없이 에이전트 성능, 비용 및 품질 지표에 대한 실시간 가시성을 제공합니다. |
| Experiment / Improvement Loop | ●●● | 통합된 프롬프트 관리, 지속적인 Eval 및 모델 버전 관리를 통해 Observability를 개선 루프와 원활하게 연결합니다. |
| DevEx / Integration | ●●● | 광범위한 프레임워크 지원, AI 지원 디버깅, Python 및 TypeScript를 위한 견고한 SDK를 통해 우수한 개발자 경험을 제공합니다. |
| Enterprise & Security | ●●● | 새로운 멀티 워크스페이스 조직 지원을 통해 엔터프라이즈 준비를 마쳤으나, 셀프 호스팅은 SaaS 대안보다 더 많은 인프라 관리가 필요합니다. |


---

### Arize Phoenix

**개요**: Arize Phoenix는 Tracing, 데이터셋 및 실험을 하나의 통합 워크플로우로 결합한 오픈 소스 AI Observability 및 Eval 플랫폼입니다. 엄격한 엔지니어링 루프를 강조하여 개발자가 개별 Trace 디버깅에서 프로덕션 데이터를 사용한 체계적인 Eval 및 프롬프트 반복으로 원활하게 이동할 수 있도록 합니다.

**강점**:
- 강력한 셀프 호스팅 옵션(Docker/Kubernetes)을 갖춘 강력한 오픈 소스 기반
- 프로덕션 Trace를 회귀 테스트를 위한 Eval 데이터셋으로 변환하는 원활한 워크플로우
- Playground, 버전 관리 및 Span 재생을 포함한 고급 프롬프트 엔지니어링 도구
- 에이전트를 위한 특화된 지표(도구 선택/호출)를 갖춘 포괄적인 Eval 스위트
- OpenInference 표준 및 광범위한 SDK 지원을 통한 넓은 에코시스템 통합

**약점**:
- 명시적인 내장 PII 마스킹 및 데이터 프라이버시 변환 기능 부족
- 엔터프라이즈 컴플라이언스를 위한 감사 로깅이 명시적으로 상세하지 않음
- 모델 버전 관리가 풀기능 모델 레지스트리보다는 실험 트래킹에 국한됨
- 에이전트를 위한 시각적 워크플로우 빌더나 DAG 에디터가 Trace 타임라인에 비해 덜 강조됨

**최근 업데이트**:
- OpenAI Responses API 타입 지원: Playground에서 Chat Completions와 Responses API 타입 중에서 선택할 수 있는 지원 (2026-02-12)
- 데이터셋 Evaluator: 실험 중에 서버 측에서 자동으로 실행되도록 데이터셋에 Evaluator를 직접 연결 (2026-02-12)
- Playground를 위한 커스텀 Provider: Playground 전체에서 재사용 가능한 커스텀 AI Provider(OpenAI, Azure, Anthropic 등)의 중앙 집중식 구성 (2026-02-11)
- Claude Opus 4.6 지원: 확장된 thinking 파라미터 및 비용 트래킹을 포함한 Claude Opus 4.6의 Playground 지원 (2026-02-09)
- 도구 선택 및 호출 Evaluator: 에이전트의 도구 선택 정확도 및 파라미터 호출 정확성을 판별하는 특화된 Evaluator (2026-01-31)
- Phoenix CLI 명령: 터미널에서 프롬프트, 데이터셋 및 실험을 관리하기 위한 새로운 CLI 명령 (2026-01-22)
- Span ID를 포함한 Trace의 데이터셋 변환: 소스 Span에 대한 양방향 링크를 유지하면서 Trace를 데이터셋으로 변환 (2026-01-21)
- Trace와 함께 어노테이션 내보내기: 수동 및 자동 어노테이션과 함께 Trace를 내보내기 위한 CLI 지원 (2026-01-19)
- CLI 터미널 액세스: AI 코딩 어시스턴트가 터미널 명령을 통해 Phoenix 데이터를 직접 쿼리할 수 있도록 지원 (2026-01-17)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | Phoenix는 OpenTelemetry/OpenInference를 기반으로 구축된 강력한 핵심 Observability를 제공하며, 상세한 Trace 시각화, 타임라인 분석 및 디버깅을 위한 Span 재생 기능을 갖추고 있습니다. |
| Agent / RAG Observability | ●●● | 도구 사용을 위한 특화된 Evaluator와 에이전트 프레임워크와의 깊은 통합, 표준 RAG 검색 Tracing을 통해 에이전트 워크플로우를 강력하게 지원합니다. |
| Evaluation Integration | ●●● | 플랫폼의 핵심 기둥으로, 광범위한 LLM-as-a-judge 기능과 휴먼 피드백 도구의 지원을 받아 프로덕션 Trace와 Eval 데이터셋 사이의 긴밀한 루프를 제공합니다. |
| Monitoring & Metrics | ●●● | 비용, Latency 및 품질 지표를 아우르는 포괄적인 모니터링 Dashboard를 제공하며, 최근에는 에이전트 도구 사용 성능을 타겟팅하는 기능이 추가되었습니다. |
| Experiment / Improvement Loop | ●●● | 강력한 프롬프트 엔지니어링 도구, 실험 트래킹 및 데이터셋 관리를 통해 데이터 기반의 반복을 가능하게 함으로써 견고한 개선 루프를 촉진합니다. |
| DevEx / Integration | ●●● | 광범위한 프레임워크 지원, 터미널 워크플로우를 위한 새로운 CLI, 오픈 표준을 준수하는 유연한 SDK를 통해 우수한 개발자 경험을 제공합니다. |
| Enterprise & Security | ●●○ | 엔터프라이즈 배포에 적합한 강력한 셀프 호스팅 및 액세스 제어 기능을 갖추고 있지만, PII 마스킹 및 감사 로그와 같은 특정 컴플라이언스 기능은 상세하지 않습니다. |


---