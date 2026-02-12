---
layout: default
title: LLM Observability — Product Detail
---

# LLM Observability — Product Detail
**Date**: 2026-02-12 | **Model**: google/gemini-3-pro-preview

### W&B Weave

**Overview**: W&B Weave is a developer-centric observability and evaluation platform that integrates deeply with the broader Weights & Biases ecosystem to track the full lineage of prompts, models, and datasets. It excels in the iterative improvement loop, offering robust tools for trace-based evaluation, dynamic leaderboards, and multi-modal monitoring, supported by flexible enterprise deployment options.

**Strengths**:
- Deep integration with W&B ecosystem for full lineage tracking of models and datasets
- Strong evaluation workflows including LLM-as-a-judge and new Dynamic Leaderboards
- Flexible deployment options including secure On-prem and VPC environments
- Multi-modal support with the recent addition of Audio Monitors
- Comprehensive SDK support with automatic patching for major frameworks

**Weaknesses**:
- Lack of visual DAG or workflow graph visualizations for complex agent flows
- No explicit support for tracing conversational memory state
- Limited details on automated regression detection beyond manual evaluation runs
- Infrastructure-as-code and CLI tooling specific to Weave is not well documented

**Recent Updates**:
- Audio Monitors: Support for creating monitors that observe and judge audio outputs (MP3/WAV) alongside text using LLM judges. (2026-02-01)
- Dynamic Leaderboards: Auto-generated leaderboards from evaluations with filtering, customization, and CSV export capabilities. (2026-01-29)
- Custom LoRAs in Playground: Serverless LoRA Inference allows using custom fine-tuned LoRA weights directly in the Weave Playground. (2026-01-16)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | Weave offers a robust core observability suite that excels in automated tracking of LLM inputs, outputs, and token-based costs. Its hierarchical trace tree and interactive plots provide deep visibility into nested function calls and performance metrics. |
| Agent / RAG Observability | △ | Weave provides robust tracing for RAG and agentic workflows, specifically excelling in capturing function calls and document retrieval steps. While it effectively visualizes multi-step reasoning, it lacks specialized memory tracking or DAG-based workflow visualizations. |
| Evaluation Integration | O | Weave offers a robust evaluation suite bridging production monitoring and systematic testing through trace-to-dataset workflows. It provides high flexibility for automated scoring via LLM-as-a-judge, dynamic leaderboards, and integrated human feedback interfaces. |
| Monitoring & Metrics | O | Weave offers a robust monitoring suite focused on cost, token usage, and performance tracking. It excels in providing customizable dashboards and granular visibility, though some advanced statistical alerting features are less explicitly documented. |
| Experiment / Improvement Loop | O | Weave provides a robust ecosystem for the experiment loop, offering deep integration between prompt management, model versioning, and evaluation comparisons. It excels at tracking the iterative development process from fine-tuning to performance analysis. |
| DevEx / Integration | O | Weave offers a strong developer experience with comprehensive SDKs and deep integrations across major LLM frameworks. Its flexible tracing decorators and REST API provide programmatic control, though infrastructure-specific tooling is not detailed. |
| Enterprise & Security | O | Weave offers a robust enterprise suite with flexible deployment options including self-hosted VPC and on-premise. It provides strong security controls through SDK-level PII redaction and audit logging, supported by multi-region availability. |


---

### LangSmith

**Overview**: LangSmith is a comprehensive observability and evaluation platform deeply integrated with the LangChain and LangGraph ecosystems, excelling in tracing complex agentic workflows. It bridges the gap between prototype and production by offering robust tools for dataset creation, LLM-as-a-judge evaluation, and prompt versioning.

**Strengths**:
- Deep integration with LangGraph for tracing complex, multi-step agent workflows.
- Comprehensive evaluation suite supporting LLM-as-a-judge and human feedback loops.
- Strong prompt and dataset versioning capabilities that facilitate iterative improvement.
- Robust self-hosting options and data residency support for enterprise compliance.
- Seamless conversion of production traces into evaluation datasets.

**Weaknesses**:
- Lack of explicit CLI tools or infrastructure-as-code support in the provided documentation.
- Documentation gaps regarding RBAC and audit logging features for enterprise governance.
- Limited visualization of failure states within the UI compared to successful trace flows.
- Less emphasis on model versioning compared to prompt and chain versioning.
- Tool success rate and custom metric dashboards are less developed than core cost/latency metrics.

**Recent Updates**:
- Customize Trace Previews: Allows users to customize how traces are previewed in the LangSmith UI. (2026-02-06)
- Non-Otel Google Vertex AI (ADK) Wrapper: Added a non-OpenTelemetry wrapper for Google Vertex AI (ADK) in the Python SDK. (2026-02-02)
- LangSmith Self-Hosted v0.13: Released version 0.13 of the self-hosted platform. (2026-01-16)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | LangSmith provides a robust core observability suite that automatically captures deep nested traces, hierarchical spans, and detailed LLM metadata. It excels in performance monitoring through latency analysis and offers specialized local replay capabilities for LangGraph-based workflows. |
| Agent / RAG Observability | O | LangSmith provides robust observability for agents and RAG through deep integration with LangGraph, enabling detailed tracing of tool calls, retrieval steps, and multi-step reasoning. It excels at capturing the orchestration of complex, stateful workflows. |
| Evaluation Integration | O | LangSmith offers a comprehensive evaluation suite that bridges production monitoring and development testing. It excels in converting real-world traces into test sets and provides robust tools for both automated LLM-based scoring and human-in-the-loop annotation. |
| Monitoring & Metrics | O | LangSmith offers a robust monitoring suite centered on cost, token usage, and performance health. Its alerting system is particularly strong, allowing teams to proactively manage latency spikes and error rates in production environments. |
| Experiment / Improvement Loop | O | LangSmith offers a robust suite for the improvement loop, characterized by strong prompt and dataset versioning capabilities. It excels in experiment tracking and provides clear pathways for fine-tuning by converting production traces into training data. |
| DevEx / Integration | O | LangSmith offers a robust developer experience with official SDKs for major languages and broad compatibility across popular AI frameworks and custom models. It provides flexible programmatic access via a REST API and specialized support for tracing streaming LLM responses. |
| Enterprise & Security | △ | LangSmith offers robust enterprise infrastructure options through self-hosted deployments and regional data residency. While it provides strong PII masking and data retention controls, the provided documentation does not detail RBAC or audit logging capabilities. |


---

### Langfuse

**Overview**: Langfuse is an open-source LLM engineering platform that combines deep observability with robust evaluation and prompt management workflows. It excels in tracing complex agentic behaviors and RAG pipelines while providing strong self-hosting capabilities for enterprise security and compliance.

**Strengths**:
- Strong self-hosting and data privacy capabilities suitable for enterprise compliance.
- Deep integration with agent frameworks (LangGraph, LlamaIndex) and complex trace visualization.
- Integrated evaluation suite combining LLM-as-a-judge, human annotation, and dataset management.
- Robust prompt management and versioning system.

**Weaknesses**:
- Lack of explicit model version registry distinct from prompt versioning.
- Limited native infrastructure management tools (CLI/IaC).
- Potential performance bottlenecks with very large datasets or complex latency queries.

**Recent Updates**:
- Single Observation Evals: Added support for running evaluations on single observations. (2026-02-09)
- Reasoning/Thinking Rendering: Added support to render thinking/reasoning parts in trace details (e.g., for reasoning models). (2026-02-06)
- Org Audit Log Viewer: New UI for viewing organization-level audit logs. (2026-02-06)
- Inline Trace Comments: Allows adding comments inline on fractions of IO data within traces. (2026-01-27)
- Corrections in Trace Preview: Added ability to view and manage corrections directly in trace and observation previews. (2026-01-13)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | Langfuse provides a robust core observability suite that excels in hierarchical tracing and automated data capture. It offers comprehensive tracking of prompts, responses, tokens, and latency, with specialized features for session-based replays and nested function call stacks. |
| Agent / RAG Observability | O | Langfuse provides a robust suite for agent and RAG observability, featuring dedicated support for tool calls, retrieval steps, and complex workflow visualizations. Its 'Agent Graphs' and deep integration with frameworks like LangGraph allow for detailed tracing of multi-step reasoning and nested agent operations. |
| Evaluation Integration | O | Langfuse offers a robust evaluation suite that bridges production observability with systematic testing through trace-to-dataset conversion and built-in LLM-as-a-judge capabilities. The platform excels in human-in-the-loop workflows, providing comprehensive UI tools for manual annotation and side-by-side model comparisons. |
| Monitoring & Metrics | O | Langfuse offers a robust suite for monitoring LLM applications, with particularly strong capabilities in cost tracking, token analytics, and tool performance. While it provides essential latency and error visibility, some documentation suggests potential performance bottlenecks with complex latency percentile queries. |
| Experiment / Improvement Loop | △ | Langfuse provides a robust environment for prompt and dataset management, featuring strong version control and side-by-side experiment comparisons. While it facilitates the creation of fine-tuning datasets through corrected outputs, it lacks explicit documentation for dedicated model versioning within the provided search results. |
| DevEx / Integration | O | Langfuse provides a robust developer experience with comprehensive SDKs for Python and JS/TS, alongside deep integrations for popular frameworks like LangChain and LlamaIndex. Its open API and OpenTelemetry support ensure high extensibility for custom model tracing and programmatic data access. |
| Enterprise & Security | O | Langfuse provides a robust enterprise security suite featuring flexible self-hosting options and comprehensive data management tools. It supports critical compliance requirements through configurable data retention, multi-region residency, and automated audit logging. |


---

### Braintrust

**Overview**: Braintrust is an enterprise-grade LLMops platform that tightly integrates production observability with evaluation-driven development. It distinguishes itself with a self-hosted data plane architecture for security and deep support for complex, nested tracing of agents and RAG workflows.

**Strengths**:
- Strong 'evals-first' workflow connecting production traces directly to datasets for regression testing.
- Enterprise security model with a self-hosted data plane (AWS/Terraform) ensuring data stays in user VPCs.
- Deep support for nested and hierarchical tracing suitable for complex agents and RAG.
- Broad framework integration including LangChain, LlamaIndex, and Vercel AI SDK.

**Weaknesses**:
- Lack of visual workflow graph builders or topology views compared to competitors like LangSmith.
- No explicit memory or state tracking features for long-running conversational agents.
- Limited direct integration with fine-tuning or RLHF pipelines for model improvement.

**Recent Updates**:
- Sub-agent nesting for Claude Agent: Added support for sub-agent nesting within the Claude Agent SDK wrapper to improve hierarchical observability. (2026-02-05)
- Review Span Type: Introduced a new 'review' span type to the SDK, likely to support manual or automated review steps in traces. (2026-02-05)
- Classifications Field: Added a classifications field to the SDK, enhancing data labeling and categorization capabilities. (2026-01-31)
- Trace Scoring Candidate: Updates to Python trace scoring capabilities to refine automated evaluation logic. (2026-01-21)
- Workflows Renaming: Renamed 'agents' to 'workflows' in the SDK to better reflect broader orchestration capabilities. (2026-01-15)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | Braintrust provides a robust core observability suite with deep support for nested tracing, hierarchical spans, and comprehensive metric tracking including tokens and latency. Its ability to wrap existing SDKs and integrate via OpenTelemetry ensures automatic capture of prompts, responses, and detailed execution timing. |
| Agent / RAG Observability | △ | Braintrust offers robust observability for RAG and agentic workflows, specifically excelling in tool call and retrieval tracing. While it provides detailed multi-step trace analysis, it lacks explicit mentions of specialized workflow graph visualizations or dedicated memory tracking. |
| Evaluation Integration | O | Braintrust provides a comprehensive evaluation suite that bridges production monitoring and testing by allowing users to convert traces into datasets and automate regression testing via CI/CD. It features robust support for both automated LLM-as-a-judge metrics and structured human annotation workflows. |
| Monitoring & Metrics | O | Braintrust offers a comprehensive monitoring suite that integrates production logs with experimental data. It provides robust real-time alerting and dashboarding capabilities for core LLM performance indicators including cost, latency percentiles, and tool execution success. |
| Experiment / Improvement Loop | O | Braintrust offers a robust environment for the LLM improvement loop, specifically excelling in prompt management, dataset-centric evaluations, and side-by-side experiment tracking. Its platform integrates evaluation directly into the prompt lifecycle, allowing for continuous monitoring and regression testing in production. |
| DevEx / Integration | O | Braintrust offers a robust developer experience with comprehensive SDK support for Python and TypeScript and deep integrations with major AI frameworks like LangChain and LlamaIndex. The platform is highly flexible, supporting custom model providers, full REST API access, and native streaming tracing. |
| Enterprise & Security | O | Braintrust provides a robust enterprise security suite centered around a self-hosted data plane architecture that ensures data residency and sovereignty. It complements this with standard enterprise requirements including SSO, RBAC, audit logging, and configurable data retention. |


---

### MLflow

**Overview**: MLflow is a mature, open-source MLOps platform that has successfully expanded into GenAI with robust tracing, evaluation, and prompt engineering capabilities. It excels in experiment tracking and version control for LLM artifacts, though it currently relies on integrations or custom implementations for some advanced production monitoring and cost analysis features.

**Strengths**:
- Comprehensive versioning system for Prompts, Models, and Datasets.
- Deep integration with popular GenAI frameworks like LangChain and LlamaIndex.
- Robust evaluation suite including LLM-as-a-Judge and human feedback loops.
- Flexible deployment options including self-hosted and air-gapped environments.
- Strong community support and extensive API surface for custom integrations.

**Weaknesses**:
- Lack of native, built-in cost management and dashboarding.
- Limited visualization capabilities for complex agent workflow graphs (DAGs).
- Absence of detailed percentile-based alerting for latency monitoring.
- Enterprise features like RBAC often require managed services or external integration.
- No explicit support for tracing streaming responses detailed in current documentation.

**Recent Updates**:
- Organization Support in MLflow Tracking Server: Support for multi-workspace environments, allowing organization of experiments and resources across different workspaces. (2026-02-12)
- MLflow Assistant: In-product chatbot backed by Claude Code to help identify, diagnose, and fix issues directly within the MLflow UI. (2026-01-29)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | MLflow provides a robust core observability framework, featuring deep hierarchical tracing and automatic capture of prompts, responses, and token usage, excelling at performance monitoring. |
| Agent / RAG Observability | △ | Robust observability for RAG and agentic workflows via automatic tool and retriever tracing, though it lacks dedicated workflow graph visualizations and memory tracking. |
| Evaluation Integration | O | Comprehensive evaluation suite bridging production and testing, featuring robust LLM-as-a-Judge scoring, human-in-the-loop workflows, and trace-to-dataset conversion. |
| Monitoring & Metrics | △ | Strong support for token usage and tool performance analysis via the Agent Dashboard, but currently lacks a native real-time cost dashboard and advanced alerting. |
| Experiment / Improvement Loop | O | Excellent suite for the improvement loop, centered on the Prompt Registry and comprehensive versioning for models, prompts, and datasets. |
| DevEx / Integration | △ | Strong developer experience with multi-language SDKs and deep framework integrations, though specific streaming tracing and IaC features are not detailed. |
| Enterprise & Security | △ | Robust self-hosting and PII masking make it suitable for privacy-conscious use, though RBAC and audit features often rely on external or managed integrations. |


---

### Arize Phoenix

**Overview**: Arize Phoenix is an open-source observability and evaluation platform built on OpenInference standards, designed to provide deep visibility into LLM applications, particularly RAG and agentic workflows. It combines robust hierarchical tracing with a strong 'LLM-as-a-judge' evaluation framework, offering flexible deployment options ranging from SaaS to fully self-hosted VPC environments.

**Strengths**:
- Deep integration with agentic frameworks (LangGraph, LlamaIndex) and OpenInference standard.
- Strong 'LLM-as-a-Judge' evaluation framework with pre-built and custom evaluators.
- Flexible deployment options including full self-hosting/VPC with no feature limitations.
- Comprehensive trace visualization including hierarchical spans and token usage.

**Weaknesses**:
- Lack of native model versioning and side-by-side model comparison UI.
- PII masking relies on manual Regex configuration rather than automated out-of-the-box solutions.
- No explicit support for tracing conversational memory reads/writes.
- Documentation lacks specific details on programmatic API access and CLI tools.

**Recent Updates**:
- Claude Opus 4.6 Support: Added support for Claude Opus 4.6 model to the playground. (2026-02-09)
- Tool Selection Evaluator: Added missing tool_selection evaluator to libraries. (2026-02-06)
- Faithfulness Evaluator: Added FaithfulnessEvaluator and deprecated HallucinationEvaluator. (2026-02-02)
- Tool Invocation Accuracy Metric: Added a new metric to track tool invocation accuracy. (2026-02-02)
- Configurable OAuth2 Email Extraction: Added EMAIL_ATTRIBUTE_PATH for configurable email extraction in OAuth2. (2026-01-28)
- Cursor Rule for Built-in Metrics: Added cursor rule for creating new built-in metrics (LLM classification evaluators). (2026-01-21)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | Arize Phoenix provides a robust core observability framework built on OpenInference, offering deep hierarchical tracing and detailed token usage metrics. It excels at capturing the full execution flow of LLM applications, including latency and input/output data. |
| Agent / RAG Observability | O | The platform provides robust observability for RAG and agentic workflows, featuring deep integration with frameworks like LangGraph to visualize complex reasoning chains. It excels in tool call evaluation and retrieval quality assessment. |
| Evaluation Integration | △ | Arize Phoenix offers a robust evaluation framework centered on LLM-as-a-judge capabilities and human-in-the-loop annotations. It excels at providing pre-built evaluators, though automated regression pipelines may require manual configuration. |
| Monitoring & Metrics | O | The monitoring suite covers essential LLM performance indicators including latency quantiles, error rates, and detailed cost tracking. It supports proactive management through a dedicated alerting system and flexible custom metrics. |
| Experiment / Improvement Loop | △ | Arize Phoenix offers a robust environment for prompt engineering and experimentation, featuring strong version control for prompts. It excels in continuous evaluation, though direct model versioning and automated fine-tuning pipelines are less emphasized. |
| DevEx / Integration | △ | The platform offers robust developer experience through comprehensive SDKs and deep integrations with major LLM frameworks. It excels in language-agnostic tracing, though details on programmatic API access and CLI tools are lacking. |
| Enterprise & Security | O | Arize Phoenix offers a strong enterprise security suite, particularly through flexible self-hosting and VPC deployment options. It includes RBAC, audit logging, and configurable retention, though PII masking requires manual configuration. |


---

