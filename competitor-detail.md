---
layout: default
title: LLM Observability — Product Detail
---

# LLM Observability — Product Detail
**Date**: 2026-02-12 | **Model**: google/gemini-3-pro-preview

### W&B Weave

**Overview**: W&B Weave is a comprehensive observability and evaluation platform integrated into the broader Weights & Biases ecosystem, designed to track, evaluate, and improve LLM applications. It excels in experiment tracking, multi-modal evaluation (including audio), and seamless integration with model registries and training workflows.

**Strengths**:
- Deep integration with W&B training and model registry (e.g., Custom LoRAs)
- Multi-modal evaluation support including Audio Monitors
- Strong experiment tracking and versioning heritage
- Dynamic Leaderboards for automated model comparison
- Flexible deployment options including on-prem/dedicated

**Weaknesses**:
- Lack of explicit PII masking and data compliance features in documentation
- Streaming tracing capabilities not explicitly detailed
- Memory tracing for agents is not explicitly highlighted
- Pricing model based on usage/credits can be complex

**Recent Updates**:
- Audio Monitors: Monitors that observe and judge audio outputs (MP3/WAV) alongside text using LLM judges. (2026-02-01)
- Dynamic Leaderboards: Auto-generated leaderboards from evaluations with persistent customization and CSV export. (2026-01-29)
- Custom LoRAs in Playground: Ability to load and test custom fine-tuned LoRA weights directly in the Weave Playground. (2026-01-16)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | Strong core tracing capabilities with automatic capture of nested spans, inputs, outputs, and performance metrics via a simple decorator. |
| Agent / RAG Observability | O | Robust support for RAG and agentic workflows, with specific features for evaluating retrieval quality and tracing complex tool interactions. |
| Evaluation Integration | O | A standout category with advanced features like Audio Monitors, Dynamic Leaderboards, and deep integration of LLM-as-a-judge for multi-modal outputs. |
| Monitoring & Metrics | O | Comprehensive monitoring of cost, latency, and quality metrics, with the ability to run online monitors for continuous evaluation. |
| Experiment / Improvement Loop | O | Excellent loop capabilities, leveraging W&B's mature versioning and experiment tracking infrastructure to link observability with training and fine-tuning. |
| DevEx / Integration | O | Strong developer experience with multi-language SDKs and unique capabilities like testing custom LoRA adapters directly in the Playground. |
| Enterprise & Security | △ | Enterprise deployment options (SaaS, Dedicated, On-prem) are strong, though specific compliance features like PII masking and audit logs are not detailed in the public snippets. |


---

### LangSmith

**Overview**: LangSmith is a comprehensive framework-agnostic platform for developing, debugging, and deploying AI agents, with deep roots in the LangChain ecosystem. It offers end-to-end visibility through robust tracing, evaluation, and monitoring capabilities, supporting both cloud and self-hosted deployments for enterprise needs.

**Strengths**:
- Deep integration with LangChain and LangGraph frameworks
- Comprehensive human-in-the-loop annotation and evaluation queues
- Robust self-hosted and enterprise security options
- Unified cost and performance tracking across LLMs, tools, and retrieval

**Weaknesses**:
- Pricing model based on seats and traces can become expensive at scale
- Strong association with LangChain may deter users of other frameworks despite agnostic capabilities
- Feature set is vast, potentially creating a steeper learning curve for simple use cases

**Recent Updates**:
- Customize trace previews: Ability to customize how traces are previewed in the UI. (2026-02-06)
- Google Gen AI Wrapper: New wrapper support for Google's Gen AI models. (2026-01-31)
- LangSmith Self-Hosted v0.13: Updated self-hosted version for enterprise deployments. (2026-01-16)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | LangSmith provides top-tier core observability with detailed hierarchical tracing and integrated playground features for debugging. |
| Agent / RAG Observability | O | The platform excels in agent and RAG observability, offering specialized views for tools, retrieval, and complex reasoning chains. |
| Evaluation Integration | O | Evaluation is a core pillar, featuring robust tools for automated testing, human annotation, and dataset management. |
| Monitoring & Metrics | O | Comprehensive monitoring suite covering cost, latency, and errors with real-time alerting and granular analytics. |
| Experiment / Improvement Loop | O | Strong support for the improvement loop with integrated prompt engineering, versioning, and experiment tracking. |
| DevEx / Integration | O | Excellent developer experience with broad framework support, SDKs, and CLI tools for seamless integration. |
| Enterprise & Security | O | Enterprise-ready with self-hosted options, robust security compliance (SOC 2, HIPAA), and granular access controls. |


---

### Langfuse

**Overview**: Langfuse is an open-source, developer-centric LLM engineering platform that unifies observability, prompt management, and evaluation. It distinguishes itself with strong self-hosting capabilities, deep agentic tracing (including graphs and tool calls), and a comprehensive suite for running experiments and managing datasets.

**Strengths**:
- Fully open-source and self-hostable, offering maximum data control
- Unified platform combining observability, prompt management, and evaluation
- Advanced agent tracing with graph views and reasoning step visualization
- Robust evaluation suite including LLM-as-a-judge and human annotation queues
- Accurate cost tracking with support for complex model pricing tiers

**Weaknesses**:
- Replay functionality is manual via Playground rather than a one-click instant trace replay
- Self-hosting at scale requires managing complex infrastructure (ClickHouse)
- Native fine-tuning orchestration is absent (relies on data export)

**Recent Updates**:
- Run Experiments on Versioned Datasets: Fetch datasets at specific version timestamps and run experiments on historical versions for reproducibility. (2026-02-11)
- Org Audit Log Viewer: New viewer for organization-level audit logs to track security and access events. (2026-02-09)
- Render Thinking/Reasoning: Trace detail view now renders thinking and reasoning parts of LLM responses separately. (2026-02-09)
- Single Observation Evals: Support for running evaluations on single observations directly. (2026-02-09)
- Corrected Outputs for Traces: Capture improved versions of LLM outputs directly in trace views to build fine-tuning datasets. (2026-01-14)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | Delivers comprehensive tracing capabilities with deep visibility into nested spans and accurate token/cost tracking, supported by a robust timeline view. |
| Agent / RAG Observability | O | Highly capable in agent and RAG monitoring, featuring specialized visualizations for graphs, tool usage, and multi-step reasoning processes. |
| Evaluation Integration | O | Provides a complete evaluation loop with LLM-as-a-judge, human annotation queues, and dataset management integrated directly into the workflow. |
| Monitoring & Metrics | O | Strong monitoring capabilities with a focus on accurate cost calculation (including pricing tiers) and flexible custom dashboards. |
| Experiment / Improvement Loop | O | Excellent support for the engineering lifecycle, enabling rigorous testing through versioned datasets, prompt management, and systematic experiments. |
| DevEx / Integration | O | Developer-first design with robust SDKs, OpenTelemetry compatibility, and a flexible API-first architecture. |
| Enterprise & Security | O | Enterprise-ready with strong security features, including RBAC, audit logs, and the ability to self-host for complete data sovereignty. |


---

### Braintrust

**Overview**: Braintrust is a developer-centric AI observability and evaluation platform that tightly integrates with coding workflows through tools like Cursor and MCP. It offers comprehensive tracing across six programming languages, robust evaluation capabilities with trace-level scorers, and enterprise-grade features like self-hosting and RBAC.

**Strengths**:
- Extensive SDK ecosystem covering Python, TS, Go, Java, Ruby, and C#.
- Deep integration with developer tools like Cursor and VS Code via MCP.
- Unified evaluation workflow connecting datasets, experiments, and production monitoring.
- Flexible data querying capabilities using both SQL and BTQL.
- Strong enterprise deployment options including self-hosting and VPC.

**Weaknesses**:
- Lack of specialized visualization widgets for RAG retrieval quality (e.g., chunk heatmaps).
- No built-in managed service for fine-tuning or RLHF (relies on data export).
- Limited out-of-the-box visualizations for complex memory state changes.
- PII masking features are less explicitly detailed compared to competitors.
- Region support documentation is limited.

**Recent Updates**:
- Render attachments in custom views: Custom trace views now support rendering images, videos, and audio directly. (2026-02-01)
- Navigate to trace origins: Navigate from traces in logs back to their originating prompt or dataset row. (2026-02-01)
- Trace-level scorers: Custom code scorers can now access the entire execution trace for multi-step evaluation. (2026-02-01)
- LangSmith integration: Wrapper to send tracing and evaluation calls to both LangSmith and Braintrust. (2026-02-01)
- Cursor integration: Extension to automatically configure Braintrust MCP server within Cursor editor. (2026-02-01)
- Image rendering security controls: Configurable modes (auto-load, click-to-load, block) for external images in logs. (2026-02-01)
- Single span filters with aggregations: Combine single span filters with GROUP BY for aggregated trace analysis. (2026-02-01)
- Auto-instrumentation for Python, Ruby, Go: Zero-code tracing support for major languages. (2026-01-29)
- Temporal integration: Automatic tracing of Temporal workflows and activities. (2026-01-21)
- Kanban layout for reviews: Drag-and-drop interface for managing flagged spans and reviews. (2026-01-21)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | Delivers robust core tracing with deep visibility into hierarchical execution, strong support for raw data inspection, and integrated playground replay capabilities. |
| Agent / RAG Observability | O | Strong support for agentic workflows and tool usage, particularly with recent MCP and Temporal integrations, though specialized RAG visualizations are less prominent. |
| Evaluation Integration | O | A market leader in evaluation integration, offering a seamless loop between tracing, datasets, and scoring with advanced features like trace-level scorers. |
| Monitoring & Metrics | O | Provides comprehensive monitoring dashboards with the flexibility to define custom metrics using SQL and BTQL. |
| Experiment / Improvement Loop | O | Excellent support for the experimental loop, particularly in prompt engineering and dataset management, though it stops short of managed model training. |
| DevEx / Integration | O | Best-in-class developer experience with broad SDK coverage, unique IDE integrations (Cursor), and support for modern agent frameworks. |
| Enterprise & Security | O | Strong enterprise offering with self-hosting and robust access controls, suitable for security-conscious organizations. |


---

### MLflow

**Overview**: An open-source, end-to-end platform for the machine learning lifecycle that has expanded significantly into GenAI observability and evaluation. It offers comprehensive tracing, agent monitoring dashboards, and advanced "LLM-as-a-Judge" capabilities including a visual builder and optimization algorithms.

**Strengths**:
- Unified platform for traditional ML and GenAI (Agents, LLMs)
- Strong "LLM-as-a-Judge" ecosystem with MemAlign optimizer and Judge Builder UI
- Open-source and vendor-neutral with full OpenTelemetry compatibility
- Extensive framework integrations (LangChain, LlamaIndex, DSPy, CrewAI)
- New "Organization Support" for multi-workspace enterprise management

**Weaknesses**:
- Self-hosting requires managing infrastructure (database, server) compared to SaaS-only competitors
- UI telemetry collection is enabled by default (opt-out available)
- Direct "Replay" functionality for complex agent traces is less explicit than in specialized tools

**Recent Updates**:
- Organization Support: Support for multi-workspace environments to organize experiments and resources. (2026-02-12)
- MLflow Assistant: In-product chatbot powered by Claude Code to help debug agents and fix issues. (2026-01-29)
- Agent Performance Dashboards: Pre-built charts for monitoring latency, request counts, and quality scores. (2026-01-29)
- MemAlign Judge Optimizer: Algorithm that learns evaluation guidelines from feedback to improve judge accuracy. (2026-01-29)
- Judge Builder UI: Visual interface to create, test, and export custom LLM judge prompts. (2026-01-29)
- Continuous Online Monitoring: Automatically run LLM judges on incoming traces in production. (2026-01-29)
- Distributed Tracing: Track requests across multiple services with context propagation. (2026-01-29)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | Delivers robust, OpenTelemetry-compatible tracing with deep visibility into distributed systems and complex agent executions. |
| Agent / RAG Observability | O | Strong support for agentic workflows with specialized views for sessions, tool usage, and multi-step reasoning. |
| Evaluation Integration | O | A comprehensive evaluation suite featuring a visual Judge Builder, automated optimization (MemAlign), and continuous online monitoring. |
| Monitoring & Metrics | O | Provides pre-built, automated dashboards for agent performance, cost, and quality, with real-time monitoring capabilities. |
| Experiment / Improvement Loop | O | Excellent loop for experimentation with strong versioning for prompts, models, and datasets, plus continuous evaluation in production. |
| DevEx / Integration | O | Highly developer-friendly with broad framework support, an AI coding assistant, and robust SDKs for Python and TypeScript. |
| Enterprise & Security | O | Enterprise-ready with new multi-workspace organization support, though self-hosting requires infrastructure management. |


---

### Arize Phoenix

**Overview**: Arize Phoenix is an open-source AI observability and evaluation platform designed for experimentation, troubleshooting, and continuous improvement of LLM applications. It offers robust tracing via OpenTelemetry/OpenInference, comprehensive LLM-as-a-judge evaluation capabilities, and seamless workflows for moving data between production traces and evaluation datasets.

**Strengths**:
- Strong open-source foundation with flexible self-hosting options (Docker/K8s).
- Comprehensive evaluation suite including specialized agentic evaluators (Tool Selection/Invocation).
- Deep developer workflow integration via CLI and support for AI coding assistants.
- Seamless workflow for converting production traces into evaluation datasets.
- Broad support for modern LLM frameworks (LlamaIndex, LangChain, DSPy) and providers.

**Weaknesses**:
- Lack of explicit PII masking or redaction features in the provided documentation.
- Audit logging capabilities are not explicitly detailed compared to other enterprise features.
- Memory tracing is supported via conversation history but lacks dedicated state visualization compared to tool tracing.

**Recent Updates**:
- OpenAI Responses API Type Support: Support for selecting OpenAI API type (Chat Completions vs Responses) in Playground and custom providers. (2026-02-12)
- Dataset Evaluators: Attach evaluators directly to datasets for automatic server-side execution during experiments. (2026-02-12)
- Custom Providers for Playground: Centralized configuration for custom AI providers (OpenAI, Azure, Anthropic, etc.) reusable across playground and prompts. (2026-02-11)
- Claude Opus 4.6 Support: Added support for Anthropic's Claude Opus 4.6 model with extended thinking parameter support. (2026-02-09)
- Tool Selection & Invocation Evaluators: New evaluators to assess if agents chose the correct tool and invoked it with valid parameters. (2026-01-31)
- Configurable Email Extraction: Support for custom email extraction from OAuth2 providers using JMESPath. (2026-01-28)
- CLI Commands for Prompts/Datasets: CLI support for managing prompts, datasets, and experiments, including piping to AI assistants. (2026-01-22)
- Dataset Creation from Traces: Convert production traces into datasets while preserving span associations for bidirectional linking. (2026-01-21)
- Export Annotations with Traces: CLI support to export traces including manual labels and evaluation scores. (2026-01-19)
- CLI Terminal Access for AI Assistants: CLI features designed to allow AI coding assistants (Cursor, Windsurf) to query Phoenix data. (2026-01-17)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | O | Phoenix provides a comprehensive tracing suite built on OpenInference, offering deep visibility into execution flows, latency, and costs with native replay capabilities. |
| Agent / RAG Observability | O | The platform excels in agent observability with specific evaluators for tool selection and invocation, alongside robust support for RAG retrieval tracing and multi-step reasoning analysis. |
| Evaluation Integration | O | Evaluation is a core pillar, featuring a tight loop between traces and datasets, extensive LLM-as-a-judge support, and tools for both automated and human assessment. |
| Monitoring & Metrics | O | Provides essential monitoring dashboards for cost, latency, and errors, with specialized metrics for agentic behaviors like tool usage accuracy. |
| Experiment / Improvement Loop | O | Facilitates a strong improvement loop with prompt versioning, experiment tracking, and the ability to curate datasets directly from production traffic for testing. |
| DevEx / Integration | O | Excellent developer experience with a feature-rich CLI, broad SDK support, and deep integration with popular LLM frameworks and orchestration tools. |
| Enterprise & Security | △ | Strong self-hosting and access control capabilities suitable for enterprise deployment, though specific compliance features like PII masking and audit logs are not detailed. |


---

