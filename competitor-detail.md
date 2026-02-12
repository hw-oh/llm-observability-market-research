---
layout: default
title: LLM Observability — Product Detail
---

# LLM Observability — Product Detail
**Date**: 2026-02-12 | **Model**: google/gemini-3-pro-preview

### LangSmith

**Overview**: A comprehensive, framework-agnostic platform designed for the entire lifecycle of LLM application development, from prototyping to production. It excels in deep tracing of complex agentic workflows, advanced evaluation with human annotation queues, and enterprise-grade monitoring.

**Strengths**:
- Deep integration with LangChain and LangGraph while remaining framework-agnostic
- Comprehensive evaluation suite with pairwise comparison and human annotation queues
- Strong enterprise readiness with self-hosted options and SOC 2 compliance
- Unified cost tracking across LLMs, tools, and retrieval components
- Advanced debugging tools like terminal-based 'Fetch' and trace replay

**Weaknesses**:
- Pricing model based on traces can become expensive for high-volume applications
- Feature density may present a steeper learning curve for simple use cases
- Memory state visualization is less explicit compared to tool and retrieval tracing

**Recent Updates**:
- Python SDK v0.7.1: Client library update for LangSmith Observability. (2026-02-10)
- Customize trace previews: Ability to customize how trace previews are displayed in the UI. (2026-02-06)
- Python SDK v0.6.9: Added pre-commit hooks and fixed sandbox async endpoint. (2026-02-05)
- Python SDK v0.6.8: Non-otel Google ADK wrapper and optional chat/completions name parameters. (2026-02-02)
- Python SDK v0.6.7: Export Google Gen AI wrapper. (2026-01-31)
- JS SDK v0.6.6: Release of JS SDK 0.4.10 and sandbox default endpoint fix. (2026-01-27)
- LangSmith Self-Hosted v0.13: Updated release for the self-hosted version of the platform. (2026-01-16)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | ●●● | Offers robust core observability with deep tracing capabilities that handle complex, hierarchical agent workflows and granular token/cost tracking. |
| Agent / RAG Observability | ●●● | Highly specialized for agent and RAG systems, providing detailed visibility into tool usage, retrieval steps, and multi-step reasoning flows. |
| Evaluation Integration | ●●● | Features a mature evaluation suite with strong support for both automated LLM-as-a-judge metrics and human-in-the-loop annotation workflows. |
| Monitoring & Metrics | ●●● | Provides comprehensive monitoring dashboards focusing on cost, latency, and errors, with specific breakdowns for different components of the LLM stack. |
| Experiment / Improvement Loop | ●●● | Strong loop for iteration, particularly in prompt engineering and dataset management, enabling systematic experimentation and improvement. |
| DevEx / Integration | ●●● | Excellent developer experience with broad framework support, robust SDKs, and tools like 'LangSmith Fetch' for terminal-based debugging. |
| Enterprise & Security | ●●● | Enterprise-ready with self-hosted options, SOC 2 compliance, and robust access controls, catering to security-conscious organizations. |


---

### Langfuse

**Overview**: Langfuse is an open-source LLM engineering platform that provides comprehensive observability, evaluation, and prompt management for LLM applications. It excels in tracing complex agentic workflows, managing datasets for evaluation, and offering robust self-hosting capabilities for enterprise security.

**Strengths**:
- Fully open-source and self-hostable, offering complete data sovereignty
- Comprehensive evaluation suite merging automated LLM-as-a-judge with human annotation queues
- Deep integration of prompt management with tracing and experiments
- Strong support for complex agentic workflows (Graphs, Tool filters, Reasoning visualization)

**Weaknesses**:
- Replay functionality is manual via Playground rather than a one-click automated regression test from trace
- Cloud region support is not explicitly detailed compared to self-hosting flexibility
- Tool success rate is a derived metric rather than a pre-built dashboard widget

**Recent Updates**:
- Single Observation Evals: Ability to run evaluations on single observations directly. (2026-02-01)
- Org Audit Log Viewer: New viewer for organization-level audit logs to track security and access events. (2026-01-28)
- Reasoning/Thinking Trace Rendering: Visualization support for 'thinking' or reasoning parts of model outputs in trace details. (2026-01-28)
- Corrected Outputs: Capture improved versions of LLM outputs directly in trace views for dataset creation. (2026-01-14)
- Events-based Trace Table: New events-based observation and trace table view. (2026-01-29)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | ●●● | Robust core tracing capabilities with deep visibility into nested spans and strong integration between traces and the playground. |
| Agent / RAG Observability | ●●● | Highly capable agent observability with specific features for tool calls, reasoning steps, and graph visualization. |
| Evaluation Integration | ●●● | A comprehensive evaluation suite combining automated LLM-as-a-judge, human annotation queues, and dataset management. |
| Monitoring & Metrics | ●●● | Strong monitoring capabilities with a focus on cost, latency, and token usage, supported by custom dashboards. |
| Experiment / Improvement Loop | ●●● | Excellent loop for iteration with strong prompt management, dataset versioning, and experiment tracking. |
| DevEx / Integration | ●●● | Developer-friendly with robust SDKs, broad framework support, and an API-first architecture. |
| Enterprise & Security | ●●● | Strong enterprise posture due to self-hosting capabilities, recently enhanced with audit logs and RBAC. |


---

### Braintrust

**Overview**: Braintrust is a comprehensive AI observability and evaluation platform that emphasizes a rigorous 'evals-first' workflow, integrating deeply with developer tools like Cursor and VS Code. It combines production monitoring with a strong experimentation framework, allowing teams to iterate on prompts and models using real-world data and automated scorers. The platform supports a wide range of SDKs and offers enterprise-grade features like self-hosting and granular access control.

**Strengths**:
- Unified workflow for evaluation (playgrounds/datasets) and production monitoring.
- Extensive SDK ecosystem covering Python, TS, Go, Java, Ruby, and C#.
- Powerful query capabilities with BTQL and SQL for custom analytics.
- Deep integration with developer tools like Cursor, VS Code, and Temporal.
- Strong enterprise features including self-hosting and granular RBAC.

**Weaknesses**:
- Lack of built-in orchestration for fine-tuning or RLHF training jobs.
- RAG visualizations are span-based rather than offering specialized embedding space inspectors.
- Direct PII text masking features are less explicitly detailed compared to general security controls.

**Recent Updates**:
- Trace-level scorers: Custom code scorers can now access the entire execution trace to evaluate multi-step workflows and agent behavior. (2026-02-01)
- LangSmith integration: Wrapper to send tracing and evaluation calls to both LangSmith and Braintrust, or route solely to Braintrust. (2026-02-01)
- Cursor integration: Extension to automatically configure Braintrust MCP server for querying logs and running experiments from Cursor. (2026-02-01)
- Image rendering security controls: Configurable modes (auto-load, click-to-load, block) to prevent sensitive data leaks from image URLs. (2026-02-01)
- Single span filters with aggregations: Combine single span filters with GROUP BY to aggregate traces based on span-level conditions. (2026-02-01)
- Auto-instrumentation (Python, Ruby, Go): Zero-code tracing support for Python, Ruby, and Go applications. (2026-01-20)
- Temporal integration: Automatic tracing of Temporal workflows and activities with parent-child relationship mapping. (2026-01-20)
- Kanban layout for reviews: Drag-and-drop interface for managing flagged spans and human review workflows. (2026-01-20)
- Streamlined online scoring setup: Create online scoring rules directly from logs with automatic prepopulation. (2026-01-20)
- Loop on trace pages: AI assistant 'Loop' is now available on individual trace pages for summarization and error analysis. (2026-01-20)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | ●●● | Robust core tracing capabilities with excellent visualization of complex, hierarchical execution paths and deep data inspection tools. |
| Agent / RAG Observability | ●●● | Strong support for agentic workflows, particularly with the new Temporal integration and trace-level scorers, though RAG visualization is standard span-based. |
| Evaluation Integration | ●●● | A market leader in evaluation integration, offering a seamless loop between production logs, datasets, and automated scoring. |
| Monitoring & Metrics | ●●● | Comprehensive monitoring with a flexible query engine (BTQL/SQL) that allows for deep custom analytics beyond standard dashboards. |
| Experiment / Improvement Loop | ●●● | Excellent tooling for the experimental loop, particularly for prompt engineering and dataset management, enabling rapid iteration. |
| DevEx / Integration | ●●● | Superior developer experience with a wide array of SDKs, modern tool integrations (Cursor, MCP), and auto-instrumentation. |
| Enterprise & Security | ●●● | Strong enterprise posture with self-hosting and robust access controls, suitable for security-conscious organizations. |


---

### MLflow

**Overview**: MLflow is a comprehensive, open-source platform managing the entire GenAI lifecycle, from experimentation to production. It features robust observability with OpenTelemetry-compatible tracing, advanced evaluation capabilities including a Judge Builder and continuous monitoring, and strong agent management tools.

**Strengths**:
- Comprehensive end-to-end platform covering tracking, tracing, evaluation, and deployment
- Vendor-neutral and OpenTelemetry-compatible, preventing lock-in
- Advanced evaluation features including Judge Builder and MemAlign optimizer
- Strong integration ecosystem with support for 30+ frameworks and libraries
- Robust enterprise features with new multi-workspace organization support

**Weaknesses**:
- Self-hosting requires managing infrastructure (DB, artifact store) compared to SaaS-only alternatives
- Advanced features like MemAlign may require specific model provider configurations
- UI Telemetry collection (opt-out) introduced in recent versions may concern privacy-focused users
- Replay functionality focuses on configuration reproducibility rather than instant trace re-execution

**Recent Updates**:
- Organization Support: Support for multi-workspace environments to organize experiments and resources. (2026-02-12)
- MLflow Assistant: In-product chatbot powered by Claude Code to help debug apps and agents. (2026-01-29)
- Agent Performance Dashboards: Pre-built charts for monitoring agent latency, request counts, and quality scores. (2026-01-29)
- MemAlign Judge Optimizer: Algorithm that learns evaluation guidelines from past feedback to improve judge accuracy. (2026-01-29)
- Judge Builder UI: Visual interface to create, test, and export custom LLM judge prompts. (2026-01-29)
- Continuous Online Monitoring: Automatically run LLM judges on incoming traces in production. (2026-01-29)
- Distributed Tracing: Track requests across multiple services with context propagation. (2026-01-29)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | ●●● | Robust core observability built on OpenTelemetry, offering deep visibility into distributed GenAI applications with detailed span hierarchies and performance metrics. |
| Agent / RAG Observability | ●●● | Strong support for agentic workflows with dedicated features for tool and retrieval tracing, backed by specialized scorers for efficiency and correctness. |
| Evaluation Integration | ●●● | Industry-leading evaluation suite featuring a no-code Judge Builder, continuous online monitoring, and the MemAlign algorithm for optimizing judges. |
| Monitoring & Metrics | ●●● | Comprehensive monitoring dashboards provide real-time visibility into agent performance, costs, and quality metrics with minimal configuration. |
| Experiment / Improvement Loop | ●●● | A complete loop for iteration, connecting prompt management, experiment tracking, and continuous evaluation to drive systematic improvement. |
| DevEx / Integration | ●●● | Excellent developer experience with broad framework support, robust SDKs, and tools like the MLflow Assistant to accelerate debugging and integration. |
| Enterprise & Security | ●●● | Enterprise-ready with support for multi-workspace organizations, secure deployment options, and flexible infrastructure compatibility. |


---

### Arize Phoenix

**Overview**: Arize Phoenix is an open-source AI observability and evaluation platform designed for engineering teams to debug, evaluate, and iterate on LLM applications. It combines OpenTelemetry-based tracing with a robust evaluation suite, prompt management, and experimentation tools, supporting both Python and TypeScript ecosystems.

**Strengths**:
- Comprehensive Developer Experience (CLI, SDKs, VS Code friendly)
- Robust Evaluation Framework (LLM-as-Judge, Tool Evals, Dataset management)
- Deep OpenTelemetry Integration with auto-instrumentation
- Strong Self-Hosting and Enterprise features (RBAC, OAuth2)
- Integrated Playground for prompt engineering and side-by-side comparison

**Weaknesses**:
- Lack of explicit PII masking or data redaction features in documentation
- No dedicated 'Workflow Graph' visualization for complex agent DAGs (relies on trace timeline)
- Memory tracing is limited to conversation history rather than state inspection
- Audit logging features are not explicitly detailed

**Recent Updates**:
- OpenAI Responses API Type Support: Support for selecting OpenAI API type (Chat Completions vs Responses) in Playground and custom providers. (2026-02-12)
- Dataset Evaluators: Attach evaluators directly to datasets for automatic server-side execution during experiments. (2026-02-12)
- Custom Providers for Playground: Centralized configuration for custom AI providers (OpenAI, Azure, Anthropic, etc.) reusable across playground and prompts. (2026-02-11)
- Claude Opus 4.6 Support: Support for Anthropic's Claude Opus 4.6 model with extended thinking parameters and cost tracking. (2026-02-09)
- Tool Selection & Invocation Evaluators: Specialized evaluators to judge agent tool selection accuracy and parameter invocation correctness. (2026-01-31)
- Configurable Email Extraction: Support for custom email extraction from OAuth2 providers using JMESPath. (2026-01-28)
- CLI Commands: New CLI commands for managing prompts, datasets, and experiments directly from the terminal. (2026-01-22)
- Trace-to-Dataset with Span Links: Convert traces to datasets while preserving bidirectional links to source spans. (2026-01-21)
- Export Annotations: CLI support for exporting annotations alongside traces for offline analysis. (2026-01-19)
- CLI Terminal Access: Enables AI coding assistants to query Phoenix data via CLI. (2026-01-17)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | ●●● | Phoenix provides a mature tracing foundation built on OpenTelemetry, offering deep visibility into execution paths, costs, and latency with replay capabilities. |
| Agent / RAG Observability | ●●● | Excellent support for agentic workflows, particularly in tool usage evaluation and multi-step tracing, though memory inspection is less specialized. |
| Evaluation Integration | ●●● | A standout category for Phoenix, offering a comprehensive loop from trace collection to dataset creation, automated evaluation, and human feedback. |
| Monitoring & Metrics | ●●● | Solid monitoring capabilities with a focus on cost, latency, and quality metrics derived from evaluations. |
| Experiment / Improvement Loop | ●●● | Strong experimentation features allow for systematic testing of prompts and models, tightly coupled with dataset management. |
| DevEx / Integration | ●●● | Exceptional developer experience with a 'code-first' approach, featuring a powerful CLI, typed SDKs, and broad framework support. |
| Enterprise & Security | ●●○ | Strong self-hosting and access control options make it suitable for enterprise deployment, though specific compliance features like PII masking are not detailed. |


---

### W&B Weave

**Overview**: W&B Weave is a comprehensive toolkit for building, evaluating, and monitoring LLM applications, leveraging Weights & Biases' deep roots in ML experiment tracking. It provides robust capabilities for tracing nested operations, managing prompts and datasets, and conducting rigorous evaluations with LLM judges and dynamic leaderboards.

**Strengths**:
- Strong integration with W&B's ML ecosystem (Training, Models, RL)
- Advanced evaluation features including Dynamic Leaderboards and Audio monitors
- Robust versioning for prompts, models, and datasets
- Support for custom LoRAs and fine-tuned models in the playground
- Flexible deployment options including on-prem/customer-managed

**Weaknesses**:
- Lack of explicit PII masking or advanced data privacy features in documentation
- No specific mention of trace replay functionality
- Streaming tracing support is not explicitly detailed
- Memory tracing for agents is not highlighted

**Recent Updates**:
- Audio monitors: Monitors that observe and judge audio outputs (MP3/WAV) alongside text using LLM judges. (2026-02-01)
- Dynamic Leaderboards: Auto-generated leaderboards from evaluations with persistent customization and CSV export. (2026-01-29)
- Custom LoRAs in Playground: Support for testing and comparing custom LoRA weights directly in the Weave Playground. (2026-01-16)

| Category | Rating | Summary |
|---|---|---|
| Core Observability | ●●○ | Weave offers strong core observability with automatic hierarchical tracing and detailed logging of inputs, outputs, and performance metrics. |
| Agent / RAG Observability | ●●○ | The platform provides robust support for agents and RAG, specifically highlighting retrieval quality measurement and nested trace visualization. |
| Evaluation Integration | ●●● | Evaluation is a standout category with features like Dynamic Leaderboards, multimodal LLM judges (audio/text), and deep dataset integration. |
| Monitoring & Metrics | ●●○ | Weave provides essential monitoring for cost, latency, and errors, with the ability to define custom metrics and visualize them effectively. |
| Experiment / Improvement Loop | ●●● | Leveraging W&B's heritage, Weave excels in the improvement loop with strong versioning, experiment tracking, and links to RL/fine-tuning workflows. |
| DevEx / Integration | ●●● | Developer experience is supported by dual SDKs (Python/TS) and tight integration with the W&B ecosystem, including custom model support. |
| Enterprise & Security | ●○○ | Enterprise support includes dedicated and customer-managed deployment options, though specific security features like PII masking are not detailed in the data. |


---

