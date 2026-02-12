---
layout: default
title: LLM Observability — 제품 상세 정보
---

# LLM Observability — Product Detail
**날짜**: 2026-02-12 | **모델**: google/gemini-3-pro-preview

### W&B Weave

**개요**: W&B Weave는 Weights & Biases 생태계와 깊이 통합되어 있으며, 구성 가능한(composable) LLM 애플리케이션 구축을 위해 설계된 개발자 중심의 Observability 및 Eval 플랫폼입니다. 복잡한 에이전트 워크플로우의 Tracing과 LLM-as-a-judge를 사용한 체계적인 Eval에 탁월하며, 프롬프트 및 모델에 대한 강력한 버전 관리를 제공하여 실험과 프로덕션 모니터링 사이의 간극을 좁혀줍니다.

**강점**:
- 실험부터 프로덕션까지 전체 라이프사이클 관리를 위한 W&B 생태계(Models, Registry)와의 깊은 통합.
- LLM-as-a-judge, 동적 리더보드, 휴먼 피드백 UI를 포함한 강력한 Eval 기능.
- 도구 호출(tool calls) 및 검색(retrieval) 단계를 포함한 복잡한 에이전트 워크플로우에 대한 강력한 Tracing.
- 셀프 호스팅 VPC 및 강력한 리전 지원을 포함한 유연한 엔터프라이즈 배포 옵션.

**약점**:
- 직관적인 에이전트 디버깅을 위한 시각적 워크플로우 그래프 또는 DAG 시각화 부족.
- 대화형 메모리 Tracing(읽기/쓰기)에 대한 명시적 지원 없음.
- 전문 모니터링 도구에 비해 기본 제공되는 자동 회귀(regression) 알림 기능이 제한적임.

**최근 업데이트**:
- Audio Monitors: LLM judge를 사용하여 오디오 출력(MP3/WAV)을 평가하고 대화 품질을 측정하는 기능 지원. (2026-02-01)
- Dynamic Leaderboards: 지속적인 커스터마이징 및 CSV 내보내기가 가능한 Eval 결과 기반 자동 생성 리더보드. (2026-01-29)
- Playground 내 커스텀 LoRA: Weave Playground에서 직접 커스텀 Fine-tuning된 LoRA 가중치를 사용하여 추론 및 비교 가능. (2026-01-16)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | Weave는 딥 네스티드(deep nested) Tracing과 입력, 출력, 토큰 사용량의 자동 캡처를 지원하며, 대화형 시각화 도구를 갖춘 강력한 핵심 Observability 스위트를 제공합니다. |
| Agent / RAG Observability | ●●○ | 에이전트 워크플로우에서 도구 호출 및 RAG 검색 단계를 Tracing하는 강력한 기능을 지원하지만, 시각적 워크플로우 그래프와 명시적인 메모리 Tracing 기능이 부족합니다. |
| Evaluation Integration | ●●● | 프로덕션과 테스트를 잇는 포괄적인 Eval 스위트를 제공하며, 강력한 LLM-as-a-judge 지원, 휴먼 피드백 도구, 상세한 모델 비교 보고서가 특징입니다. |
| Monitoring & Metrics | ●●● | 비용 및 토큰 분석에 탁월한 강력한 모니터링 스위트를 갖추고 있으며, 강력한 에러 트래킹 및 커스텀 메트릭 기능을 제공합니다. 단, 일부 특정 알림 설정은 덜 명시적입니다. |
| Experiment / Improvement Loop | ●●● | 모든 아티팩트(프롬프트, 모델, 데이터)에 대한 강력한 버전 제어와 Fine-tuning으로 이어지는 명확한 경로를 통해 개선 루프를 훌륭하게 지원합니다. |
| DevEx / Integration | ●●● | 광범위한 프레임워크 지원, 공식 SDK, Streaming 기능을 통해 우수한 개발자 경험을 제공하며 다양한 워크플로우에 높은 적응성을 보입니다. |
| Security & Governance | ●●● | 유연한 배포 옵션(VPC/On-prem), 강력한 PII 보호 및 포괄적인 감사 로그를 갖춘 엔터프라이즈급 보안을 제공합니다. |


---

### LangSmith

**개요**: LangSmith는 LangChain 생태계와 깊이 통합된 포괄적인 Observability 및 Eval 플랫폼으로, 프로토타이핑부터 프로덕션까지 LLM 애플리케이션의 전체 라이프사이클을 지원하도록 설계되었습니다. 계층적 Tracing, 자동화된 Eval 워크플로우, 데이터셋 관리에 탁월하여 복잡한 에이전트 또는 RAG 기반 애플리케이션을 구축하는 팀에게 강력한 선택지입니다.

**강점**:
- 복잡한 체인의 원활한 Tracing을 위한 LangChain 및 LangGraph와의 깊은 통합.
- LLM-as-a-judge 및 휴먼 어노테이션 큐를 포함한 포괄적인 Eval 스위트.
- 반복적인 개선 루프를 위한 강력한 데이터셋 관리 및 버전 관리.
- 규정 준수를 위한 강력한 셀프 호스팅 및 리전별 배포 옵션.

**약점**:
- 내장된 역할 기반 액세스 제어(RBAC) 및 감사 로그에 대한 문서화가 제한적임.
- Observability UI 내에서 명시적인 시각적 워크플로우 DAG 부족 (LangGraph 통합 외부).
- 도구 호출 성공률을 즉시 추적하기 위한 특정 메트릭이나 Dashboard 부재.
- Streaming 응답 Tracing 기능이 제공된 문서에 명시적으로 상세히 설명되어 있지 않음.

**최근 업데이트**:
- Client SDK v0.7.1: OIDC 수정 및 종속성 업데이트를 포함한 Python 및 JS 클라이언트 라이브러리 업데이트. (2026-02-10)
- Trace 미리보기 커스터마이징: UI에서 Trace 미리보기가 렌더링되는 방식을 커스터마이징하는 새로운 기능. (2026-02-06)
- LangSmith Self-Hosted v0.13: 셀프 호스팅 배포 옵션을 위한 새 버전 출시. (2026-01-16)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | LangSmith는 딥 네스팅 기능과 프롬프트, 응답, 토큰 메트릭의 자동 로깅을 갖춘 강력한 핵심 Observability 스위트를 제공합니다. 지연 시간 분석을 위한 워터폴 그래프와 같은 고급 시각화 도구는 복잡한 LLM 체인 디버깅을 위한 포괄적인 솔루션을 제공합니다. |
| Agent / RAG Observability | ●●○ | 도구 호출, 모델 상호작용, 문서 검색의 상세 Trace를 캡처하여 RAG 및 에이전트 워크플로우에 대한 강력한 Observability를 제공합니다. 특히 LangGraph 오케스트레이터와 통합될 때 복잡한 추론 체인의 순차적 단계를 로깅하는 데 탁월합니다. |
| Evaluation Integration | ●●● | Trace-to-dataset 워크플로우와 강력한 Human-in-the-loop 기능을 통해 프로덕션 Observability와 테스트를 원활하게 연결하는 포괄적인 Eval 스위트를 제공합니다. LLM 기반 Scoring과 상세한 회귀 추적, 모델 간 비교를 결합하여 자동화된 품질 보증에 탁월합니다. |
| Monitoring & Metrics | ●●● | 통합 알림 기능을 갖추고 비용, 토큰 사용량, 지연 시간, 에러 트래킹에 집중한 강력한 모니터링 스위트를 제공합니다. 핵심 운영 메트릭에는 탁월하지만, 전문화된 도구 성공률 및 고급 커스텀 메트릭 시각화 지원은 상대적으로 덜 발달된 것으로 보입니다. |
| Experiment / Improvement Loop | ●●● | Eval 워크플로우에 직접 통합되는 강력한 데이터셋 및 프롬프트 버전 관리 기능을 특징으로 하는 개선 루프용 스위트를 제공합니다. 실험 결과 비교와 프로덕션 Trace와 Fine-tuning 파이프라인 간의 간극을 메우는 데 탁월합니다. |
| DevEx / Integration | ●●○ | 공식 Python 및 JS/TS SDK와 LangChain, LlamaIndex와 같은 주요 LLM 프레임워크와의 깊은 통합을 통해 강력한 개발자 경험을 제공합니다. API를 통한 유연한 프로그래밍 방식의 접근을 제공하고 커스텀 모델 Tracing을 지원하지만, CLI 도구 및 Streaming 전용 Tracing에 대한 문서는 확인되지 않았습니다. |
| Security & Governance | ●●○ | 셀프 호스팅 VPC 옵션과 전용 EU 호스팅을 포함한 강력한 데이터 레지던시 지원을 통해 배포 유연성을 제공합니다. 구성 가능한 데이터 보존 및 SDK 수준의 PII 마스킹을 제공하지만, 내부 RBAC 및 감사 로그 기능에 대한 상세 정보가 부족합니다. |


---

### Langfuse

**개요**: Langfuse는 고정밀 Tracing과 강력한 Eval 및 비용 관리 도구를 결합한 오픈 소스 LLM 엔지니어링 플랫폼입니다. 복잡한 에이전트 애플리케이션을 구축하는 개발자를 대상으로 하며, LangChain과 같은 프레임워크와의 깊은 통합과 보안에 민감한 기업을 위한 강력한 셀프 호스팅 기능을 제공합니다.

**강점**:
- 보안 수준이 높은 환경에 적합한 강력한 오픈 소스 셀프 호스팅 기능.
- 에이전트 워크플로우를 위한 전문화된 시각화를 포함한 깊은 계층적 Tracing.
- Tracing 워크플로우에 직접 통합된 포괄적인 Eval 스위트.
- 세분화된 추적이 가능한 강력한 비용 및 토큰 분석.

**약점**:
- 명시적인 메모리 Tracing 기능 부족.
- CLI 또는 Infrastructure-as-Code 도구 부재.
- 명시적인 선제적 알림 기능이 없는 사후 대응적 에러 트래킹(Dashboard).

**최근 업데이트**:
- Single Observation Evals: 단일 관측치(observation)에 대해 Eval을 실행하는 기능 추가. (2026-02-12)
- Events-based Trace Table: 이벤트/관측치 기반의 새로운 Trace 테이블 UI 뷰. (2026-02-12)
- Reasoning Trace Rendering: 추론 모델 등을 위해 Trace 상세 정보에서 생각/추론(thinking/reasoning) 부분을 렌더링하는 기능 지원. (2026-02-12)
- Org Audit Log Viewer: 조직 수준의 감사 로그를 위한 새로운 뷰어. (2026-02-12)
- Inline Trace Comments: Trace 내 IO 데이터의 일부에 인라인으로 주석을 추가하는 기능. (2026-02-12)
- Corrections in Trace Preview: Trace 및 관측치 미리보기에서 직접 수정 사항을 확인하고 관리하는 기능 추가. (2026-02-12)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | Langfuse는 계층적 Tracing과 비용 관리에 탁월한 강력한 핵심 Observability 스위트를 제공합니다. 데코레이터를 통한 딥 네스팅 지원과 엔드 투 엔드 상호작용 분석을 위한 포괄적인 세션 리플레이가 특징입니다. |
| Agent / RAG Observability | ●●● | 도구 호출 및 검색 단계를 위한 전용 데이터 모델을 갖춘 에이전트 및 RAG용 강력한 스위트를 제공합니다. 에이전트 그래프 기능과 오케스트레이션 프레임워크 통합을 통해 다단계 추론 과정을 매핑하는 데 탁월합니다. |
| Evaluation Integration | ●●● | 강력한 데이터셋 관리와 다중 방식 Scoring을 통해 프로덕션 Observability와 체계적인 테스트를 연결합니다. LLM-as-a-judge, 휴먼 어노테이션, 모델 간 비교를 위한 통합 워크플로우에 탁월합니다. |
| Monitoring & Metrics | ●●● | 모니터링 스위트가 비용, 토큰 사용량, 지연 시간 분석과 깊이 통합되어 있습니다. 도구 호출 추적 및 API를 통한 커스텀 메트릭에는 탁월하지만, 에러에 대한 선제적 알림 메커니즘은 덜 두드러집니다. |
| Experiment / Improvement Loop | ●●● | 프롬프트 관리, 데이터셋 버전 관리, 실험 간 비교에 탁월합니다. 수정된 출력을 통해 Fine-tuning을 위한 토대를 제공하며, 주로 프롬프트 반복의 체계적인 추적에 집중합니다. |
| DevEx / Integration | ●●● | 포괄적인 SDK와 깊은 프레임워크 통합을 통해 강력한 개발자 경험을 제공합니다. 오픈 API와 OpenTelemetry 지원으로 높은 확장성을 보장하지만, 인프라 전용 도구는 현재 부재합니다. |
| Security & Governance | ●●● | 유연한 셀프 호스팅 옵션과 포괄적인 관리 제어 기능을 갖춘 강력한 보안 스위트를 제공합니다. PII 마스킹, 구성 가능한 데이터 보존, 상세 감사 로그와 같은 필수 엔터프라이즈 기능을 포함합니다. |


---

### Braintrust

**개요**: Braintrust는 LLM Observability와 Eval을 긴밀하게 통합한 엔터프라이즈급 플랫폼으로, 프로덕션 Trace와 테스트 데이터셋 사이의 피드백 루프를 완성하는 데 중점을 둡니다. 강력한 SDK를 통해 복잡하고 중첩된 에이전트 워크플로우를 처리하는 데 탁월하며, 셀프 호스팅 데이터 플레인과 같은 강력한 보안 기능을 제공합니다. 다만 현재 시각적 워크플로우 그래프 빌더와 네이티브 Fine-tuning 파이프라인은 부족합니다.

**강점**:
- 프로덕션 Trace를 Eval 데이터셋으로 원활하게 통합 (Trace-to-Dataset).
- 셀프 호스팅 데이터 플레인 옵션을 갖춘 강력한 엔터프라이즈 보안 모델.
- 복잡하고 중첩된 에이전트 워크플로우 및 커스텀 모델을 위한 강력한 SDK 지원.
- LLM-as-a-judge 및 휴먼 리뷰 UI를 포함한 포괄적인 Eval 스위트.

**약점**:
- 경쟁사 대비 시각적 워크플로우/에이전트 그래프 빌더 부족.
- RLHF 또는 Fine-tuning 파이프라인에 대한 네이티브 지원 없음.
- UI에서 Trace 실행 단계를 따라가는 시각적 '리플레이' 기능 부재.

**최근 업데이트**:
- OpenAI Agents 통합: OpenAI 에이전트 통합을 위해 모든 span 유형을 처리하도록 SDK 업데이트. (2026-02-05)
- Sub-agent Nesting: Claude Agent SDK 래퍼를 위한 서브 에이전트 네스팅 지원 추가. (2026-02-05)
- Review Span Type: Trace에서 직접 휴먼 리뷰 워크플로우를 지원하기 위한 새로운 'review' span 유형 도입. (2026-02-05)
- Classifications 필드: 구조화된 데이터 캡처를 강화하기 위해 SDK에 classifications 필드 추가. (2026-01-31)
- Eval Cache Control: Eval 도중 및 span 내보내기 후 캐싱을 끌 수 있는 옵션 추가. (2026-01-29)
- Python Trace Scoring: Python SDK 내에서 Trace Scoring을 위한 후보(candidate) 지원 도입. (2026-01-21)
- Workflow 명칭 변경: 일반적인 실행 그래프를 더 잘 반영하기 위해 SDK에서 'agents'를 'workflows'로 변경. (2026-01-15)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | Braintrust는 계층적 Tracing과 토큰 사용량, 지연 시간과 같은 상세 성능 메트릭에 탁월한 강력한 핵심 Observability 스위트를 제공합니다. SDK는 에이전트 AI 시스템에서 흔히 발생하는 복잡하고 중첩된 실행 흐름을 처리하도록 특별히 제작되었습니다. |
| Agent / RAG Observability | ●●○ | 도구 호출 및 문서 검색 단계 Tracing을 강력하게 지원하여 RAG 및 에이전트 워크플로우에 대한 강력한 Observability를 제공합니다. 상세한 다단계 실행 데이터 캡처에는 탁월하지만, 전문화된 워크플로우 그래프 시각화나 전용 메모리 추적에 대한 명시적 언급은 부족합니다. |
| Evaluation Integration | ●●● | 프로덕션 모니터링과 오프라인 테스트를 긴밀하게 통합하는 포괄적인 Eval 스위트를 제공합니다. 프로덕션 Trace를 테스트 데이터셋으로 변환하고 자동화된 LLM 기반 Scoring과 수동 휴먼 어노테이션을 위한 강력한 도구를 제공하여 피드백 루프를 완성하는 데 탁월합니다. |
| Monitoring & Metrics | ●●● | 실시간 비용, 토큰, 지연 시간 추적을 커스터마이징 가능한 Dashboard에 통합한 포괄적인 모니터링 스위트를 제공합니다. 특히 알림 기능이 강력하여 팀이 지연 시간 백분위수 및 에러율 전반에서 SLO 위반을 모니터링할 수 있습니다. |
| Experiment / Improvement Loop | ●●● | 프롬프트 관리, 데이터셋 중심 Eval, 사이드 바이 사이드 A/B 테스트에 특히 탁월한 강력한 LLM 개선 루프 환경을 제공합니다. 버전 관리되는 프롬프트, 데이터셋, scorer를 긴밀하게 통합하여 지속적인 모니터링과 회귀 테스트를 용이하게 합니다. |
| DevEx / Integration | ●●● | Python 및 JS/TS를 위한 포괄적인 SDK와 LangChain, LlamaIndex와 같은 주요 AI 프레임워크와의 깊은 통합을 통해 강력한 개발자 경험을 제공합니다. 커스텀 모델 제공자 지원 및 실시간 LLM 응답을 위한 네이티브 Streaming Tracing을 통해 유연성 면에서 탁월합니다. |
| Security & Governance | ●●● | 민감한 정보가 고객의 VPC 내에 머물도록 보장하는 셀프 호스팅 데이터 플레인을 중심으로 강력한 보안 프레임워크를 제공합니다. 엄격한 규제 요구 사항을 충족하기 위해 RBAC, SSO 통합, PII 마스킹, 감사 로그와 같은 필수 엔터프라이즈 기능을 포함합니다. |


---

### MLflow

**개요**: MLflow는 성숙한 오픈 소스 MLOps 플랫폼으로, 강력한 Tracing, Eval, 실험 추적 기능을 통해 LLM Observability 분야로 성공적으로 확장했습니다. 프롬프트 엔지니어링부터 모델 버전 관리까지 전체 라이프사이클 관리에 탁월하지만, 고급 엔터프라이즈 거버넌스를 위해 통합 솔루션에 의존하며 워크플로우 그래프와 같은 일부 전문화된 에이전트 시각화 기능이 부족합니다.

**강점**:
- 프롬프트, 모델, 데이터셋을 아우르는 포괄적인 라이프사이클 관리.
- 커스텀 메트릭을 지원하는 강력한 'LLM-as-a-Judge' 및 Eval 프레임워크.
- LangChain 및 LlamaIndex와 같은 주요 LLM 프레임워크와의 깊은 통합.
- 강력한 셀프 호스팅 및 PII 마스킹 기능을 갖춘 오픈 소스의 유연성.

**약점**:
- 복잡한 에이전트 실행을 위한 시각적 워크플로우 그래프 부족.
- 네이티브 비용 Dashboard 부재 (커스텀 구현 필요).
- 매니지드 서비스 없이는 제한적인 네이티브 거버넌스(RBAC/감사).
- Trace에 대한 단계별 리플레이 기능 누락.

**최근 업데이트**:
- 조직 지원: MLflow Tracking Server에서 멀티 워크스페이스 환경을 지원하여 서로 다른 워크스페이스 간에 실험과 리소스를 조직화할 수 있음. (2026-02-12)
- MLflow Assistant: MLflow UI 내에서 직접 문제를 식별, 진단 및 수정할 수 있도록 돕는 Claude Code 기반의 인프로덕트 챗봇. (2026-01-29)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | MLflow는 깊은 계층적 Tracing과 지연 시간, 토큰 사용량 같은 운영 메트릭의 자동 캡처를 특징으로 하는 강력한 LLM용 핵심 Observability 프레임워크를 제공합니다. 복잡하게 중첩된 함수 호출 매핑과 프롬프트 버전 관리에 탁월하지만, 상세한 단계별 Trace 리플레이 기능은 확인되지 않았습니다. |
| Agent / RAG Observability | ●●○ | OpenAI, Anthropic, LangChain, LlamaIndex와의 깊은 통합을 통해 에이전트 및 RAG 워크플로우에 대한 강력한 Tracing을 제공합니다. 도구 호출 및 검색 span 캡처에 탁월하지만, 메모리 전용 추적 및 그래프 기반 워크플로우 시각화에 대한 언급은 부족합니다. |
| Evaluation Integration | ●●● | 프로덕션 Trace를 데이터셋으로 변환하고 포괄적인 LLM-as-a-Judge 기능을 제공하는 데 탁월한 Eval 스위트를 제공합니다. Human-in-the-loop 워크플로우와 모델 비교를 강력하게 지원하지만, 특정 자동 회귀 알림 기능은 상세히 설명되어 있지 않습니다. |
| Monitoring & Metrics | ●●● | 지연 시간, 토큰 사용량, 도구 성공률을 추적하는 Tracing 및 Agents Dashboard 기능을 통해 LLM 애플리케이션에 대한 강력한 모니터링을 제공합니다. 커스텀 메트릭 정의 및 성능 분석에는 탁월하지만, 현재 네이티브 실시간 비용 추적 Dashboard는 부족합니다. |
| Experiment / Improvement Loop | ●●● | 전용 프롬프트 레지스트리와 포괄적인 실험 추적 기능을 갖춘 강력한 개선 루프 생태계를 제공합니다. 데이터셋, 모델, 프롬프트의 버전 관리에 탁월하며 GenAI 애플리케이션을 체계적으로 개선하기 위한 Fine-tuning 워크플로우 통합 지원을 제공합니다. |
| DevEx / Integration | ●●○ | Python 및 TypeScript를 위한 강력한 SDK 지원과 LlamaIndex와 같은 인기 LLM 프레임워크와의 깊은 통합을 통해 강력한 개발자 경험을 보여줍니다. 프로그래밍 방식의 접근을 위한 포괄적인 REST API를 제공하지만, Streaming Tracing 및 인프라 수준의 CLI 도구에 대한 상세 정보는 부족합니다. |
| Security & Governance | ●●○ | 강력한 셀프 호스팅 기능과 GenAI Trace를 위한 강력한 PII 마스킹을 제공합니다. RBAC 및 규정 준수와 같은 핵심 거버넌스 기능은 Databricks와 같은 매니지드 서비스 제공업체와 밀접하게 연관되어 있지만, 플랫폼 자체적으로 보안 엔터프라이즈 배포를 위한 필요한 연결 고리를 제공합니다. |


---

### Arize Phoenix

**개요**: Arize Phoenix는 LLM 애플리케이션을 위해 설계된 오픈 소스 우선의 Observability 및 Eval 플랫폼으로, OpenTelemetry 호환 Tracing과 깊은 프레임워크 통합을 강조합니다. 강력한 프로덕션 모니터링과 LLM-as-a-judge 기능을 갖춘 강력한 Eval 스위트를 결합하여, 코드 중심의 디버깅과 지속적인 개선에 집중하는 엔지니어링 팀에 특히 적합합니다.

**강점**:
- OpenTelemetry 통합을 통해 복잡한 에이전트 워크플로우의 벤더 중립적이고 계층적인 Tracing 가능.
- 사전 구축된 평가기(신뢰성, 도구 선택 등) 라이브러리가 확장 중인 강력한 LLM-as-a-Judge 프레임워크.
- 데이터에 민감한 환경에 이상적인, 모든 기능을 동일하게 제공하는 강력한 셀프 호스팅 기능.
- Observability 루프에 직접 통합된 포괄적인 프롬프트 관리 및 실험 추적.

**약점**:
- 네이티브 자동 PII 마스킹 부재로 인해 커스텀 span 프로세서의 수동 구성 필요.
- 프롬프트 버전 관리와 구별되는 모델 버전 관리 또는 구성 추적에 대한 명시적 지원 없음.
- 플랫폼의 프로그래밍 방식 관리를 위한 상세 API 액세스 또는 CLI 도구 부족.
- 대화형 메모리 읽기/쓰기 Tracing을 위한 특정 기능 누락.

**최근 업데이트**:
- Claude Opus 4.6 지원: Playground에 Claude Opus 4.6 모델 추가. (2026-02-09)
- Tool Selection Evaluator: 라이브러리에 누락되었던 tool_selection 평가기 추가. (2026-02-06)
- Faithfulness Evaluator: FaithfulnessEvaluator를 추가하고 HallucinationEvaluator를 지원 중단(deprecated). (2026-02-02)
- Tool Invocation Accuracy Metric: 도구 호출 정확도를 추적하기 위한 특정 메트릭 추가. (2026-01-27)
- LLM Classification Evaluators: LLM 분류를 위한 새로운 내장 메트릭 생성을 위한 cursor rule 추가. (2026-01-21)

| 카테고리 | 등급 | 요약 |
|---|---|---|
| Core Observability | ●●● | Arize Phoenix는 계층적 span, 입력, 출력 및 타이밍 데이터를 캡처하는 OpenTelemetry 호환 Tracing 중심의 강력한 핵심 Observability 프레임워크를 제공합니다. 토큰 추적 및 지연 시간 분석을 통한 성능 모니터링에 탁월하여 개발자가 복잡하게 중첩된 LLM 애플리케이션 흐름을 시각화할 수 있게 합니다. |
| Agent / RAG Observability | ●●● | 도구 호출 Tracing, 문서 검색 검사, 멀티 에이전트 궤적 시각화를 강력하게 지원하여 RAG 및 에이전트 워크플로우에 대한 강력한 Observability를 제공합니다. LangGraph 및 AutoGen과 같은 주요 프레임워크와 통합되어 복잡한 다단계 추론 체인에 대한 명확한 인사이트를 제공합니다. |
| Evaluation Integration | ●●● | LLM-as-a-judge 기능과 통합된 휴먼 어노테이션 워크플로우를 중심으로 강력한 Eval 스위트를 제공합니다. 프로덕션 Trace를 평가 가능한 데이터 포인트로 변환하는 데 탁월하며 품질 추적을 위한 광범위한 커스텀 및 사전 구축 메트릭을 지원합니다. |
| Monitoring & Metrics | ●●● | 지연 시간 분위수, 에러율, 자동화된 비용 추적을 포함한 핵심 LLM 성능 지표를 다루는 강력한 모니터링 스위트를 제공합니다. 최근 업데이트를 통해 특정 호출 정확도 메트릭으로 도구 모니터링이 강화되었습니다. |
| Experiment / Improvement Loop | ●●○ | 통합된 프롬프트 관리 및 실험 추적 기능을 통해 개선 루프를 위한 강력한 환경을 제공합니다. 지속적인 Eval 및 Fine-tuning을 위한 데이터 큐레이션에 탁월하지만, 주요 초점은 여전히 Observability 기반의 개선에 머물러 있습니다. |
| DevEx / Integration | ●●○ | 포괄적인 SDK 지원과 인기 LLM 프레임워크와의 깊은 통합을 통해 강력한 개발자 경험을 제공합니다. OpenTelemetry를 통한 벤더 중립적 Tracing에는 탁월하지만, 프로그래밍 방식의 API 액세스나 Streaming 전용 Tracing에 대한 증거는 제한적입니다. |
| Security & Governance | ●●● | 셀프 호스팅 환경을 위한 강력한 보안 프로필을 제공하며, 전체 데이터 제어, RBAC 및 구성 가능한 데이터 보존을 제공합니다. PII 마스킹은 지원되지만 커스텀 프로세서를 통한 수동 구성이 필요합니다. |


---