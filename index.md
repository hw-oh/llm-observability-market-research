---
layout: default
title: Competitor intelligence reports for W&B Weave
---

# Competitor Intel Bot

[Detailed Comparison](./comparison) · [Product Detail](./competitor-detail) · [Competitive Intelligence (Internal)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## Latest Report

<!-- LATEST_REPORT_START -->

[📋 Latest Report (2026-02-11)](./reports/2026-02-11.md)


- Weave has established a first-mover advantage in multimodal observability with the release of Audio Monitors (Feb 2026), differentiating against text-centric competitors like LangSmith and Langfuse.
- LangSmith remains the primary threat for complex agentic workflows, offering superior visualization for cyclic graphs and state machines that Weave's current trace tree views cannot yet match.
- Braintrust is successfully flanking on the enterprise side with its 'Data Plane' architecture and broad SDK support (Java, Go, C#), capturing backend engineering teams that Weave's Python/TS-focused SDKs miss.
- The 'Human-in-the-Loop' gap is widening; LangSmith, Langfuse, and Braintrust have all shipped dedicated 'Annotation Queues' or Kanban workflows, whereas Weave relies on more generic Board/Table interfaces for review.
- MLflow (v3.9) has aggressively closed the evaluation gap with 'Judge Builder' and 'MemAlign', threatening Weave's dominance in the evaluation-driven development loop for Databricks-native teams.
- Arize Phoenix's release of specialized 'Tool Selection Evaluators' signals a market shift toward granular agent component testing, an area Weave should prioritize to maintain parity in agent reliability.

> Weave leads in multimodal support and training-to-inference continuity, but faces significant pressure from LangSmith on agentic workflow visualization and Braintrust on enterprise data privacy architectures.


<!-- LATEST_REPORT_END -->

## New Features (Last 30 Days)

### [Weave](https://app.getbeamer.com/wandb/en)

- **Audio Monitors**: Support for creating monitors that observe and judge audio outputs alongside text, using audio-capable LLM judges. (2026-02-01)
- **Dynamic Leaderboards**: Auto-generated leaderboards in Evaluations that populate instantly based on model/eval filters. (2026-01-29)
- **Custom LoRAs in Playground**: Ability to load and test custom fine-tuned LoRA weights from W&B Artifacts directly in the Weave Playground. (2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **Customize Trace Previews**: UI update allowing users to configure how trace data is previewed in the list view. (2026-02-06)
- **SDK v0.7.1**: Client library update for connecting to the LangSmith Observability and Evaluation Platform. (2026-02-10)

### [Langfuse](https://langfuse.com/changelog)

- **Corrected Outputs for Traces**: Capture improved versions of LLM outputs directly in trace views to build fine-tuning datasets. (2026-01-14)
- **Inline Comments on Observation I/O**: Anchor comments to specific text selections within trace inputs and outputs. (2026-01-07)
- **Reasoning/Thinking Rendering**: Specialized UI rendering for 'thinking' parts of reasoning models (e.g., O1, R1) in traces. (2026-02-01)
- **Org Audit Log Viewer**: New UI for viewing organization-level audit logs for security and compliance. (2026-02-01)
- **Single Observation Evals**: Ability to run evaluations on individual observations rather than full traces. (2026-02-01)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **Trace-level Scorers**: Custom code scorers can now access the entire execution trace to evaluate multi-step workflows and agent behavior. (2026-02)
- **LangSmith Integration**: Wrapper to route traces to both LangSmith and Braintrust, or migrate traffic entirely. (2026-02)
- **Cursor Integration**: Extension to configure Braintrust MCP server, enabling log querying and experiment fetching directly from the Cursor IDE. (2026-02)
- **Auto-instrumentation (Python/Ruby/Go)**: Zero-code tracing support added for Python, Ruby, and Go SDKs. (2026-01)
- **Temporal Integration**: Automatic tracing of Temporal workflows and activities, capturing distributed traces across workers. (2026-01)

### [MLflow](https://mlflow.org/releases)

- **MLflow Assistant**: In-product chatbot powered by Claude Code to diagnose issues and suggest fixes within the UI. (2026-01-29)
- **Agent Performance Dashboards**: Pre-built charts for monitoring agent latency, request counts, and quality scores. (2026-01-29)
- **MemAlign Judge Optimizer**: Algorithm that learns evaluation guidelines from past feedback to improve judge accuracy. (2026-01-29)
- **Judge Builder UI**: Visual interface to create, test, and validate custom LLM judge prompts without code. (2026-01-29)
- **Continuous Online Monitoring**: Automatically runs LLM judges on incoming production traces to detect quality issues in real-time. (2026-01-29)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 Support**: Added support for Anthropic's Claude Opus 4.6 model in the Playground with accurate cost tracking. (2026-02-09)
- **Tool Selection & Invocation Evaluators**: New specialized evaluators to assess if agents selected the correct tool and invoked it with valid parameters. (2026-01-31)
- **Phoenix CLI Expansion**: Comprehensive CLI commands to manage prompts, datasets, and experiments directly from the terminal. (2026-01-22)
- **Trace-to-Dataset with Span Links**: Ability to create datasets from traces while maintaining bidirectional links to the source spans for lineage. (2026-01-21)
- **Export Annotations with Traces**: CLI support to export human and AI annotations alongside traces for offline analysis. (2026-01-19)


## Report Archive

<!-- REPORT_ARCHIVE_START -->

| Date | Report |
|------|--------|
| 2026-02-11 | [View Report](./reports/2026-02-11.md) |
| 2026-02-10 | [View Report](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)
