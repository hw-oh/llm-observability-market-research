---
layout: default
title: Competitor intelligence reports for W&B Weave
---

# Competitor Intel Bot

[Detailed Comparison](./comparison) · [Product Detail](./competitor-detail) · [Competitive Intelligence (Internal)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## Latest Report

<!-- LATEST_REPORT_START -->

[📋 Latest Report (2026-02-11)](./reports/2026-02-11.md)


- LangSmith and Langfuse are establishing a lead in 'Agent Visualization', offering dedicated graph views and state debuggers (e.g., LangGraph Studio) that provide better intelligibility for complex looping agents than Weave's linear trace trees.
- Braintrust and Helicone are successfully differentiating with 'Gateway' features (caching, rate-limiting, proxies), pushing observability into the infrastructure layer—a capability Weave currently lacks.
- Weave's integration with W&B Training remains its strongest competitive moat, offering a unique 'Production-to-Fine-tuning' workflow that standalone competitors like Arize Phoenix and LangSmith cannot replicate natively.
- Logfire is rapidly capturing the Python/Pydantic developer segment with 'magic' auto-instrumentation, threatening Weave's adoption among code-first engineering teams who prefer standard library integration over vendor SDKs.
- LangSmith and Braintrust have matured their 'Human-in-the-Loop' workflows (annotation queues, kanban reviews) significantly, creating a gap for Weave in manual evaluation and data curation use cases.
- The market is bifurcating into 'Infrastructure/Gateway' providers (Helicone, Braintrust) and 'Workflow/Agent' platforms (LangSmith, Langfuse); Weave must clarify its position as the 'Model Improvement' platform to avoid being squeezed.

> Weave leads in the **fine-tuning feedback loop** via the W&B ecosystem, but faces increasing pressure from **LangSmith** on **agentic workflow visualization** and **Braintrust** on **enterprise gateway infrastructure**.


<!-- LATEST_REPORT_END -->

## New Features (Last 30 Days)

### Weave

- **Stats Clickhouse Query Layer**: Backend improvements to the query layer for handling statistical data, likely improving dashboard performance. (2026-01-20)
- **OTel Export Improvements**: Moved OpenTelemetry export off async inserts to improve reliability and standard compliance. (2026-01-08)

### LangSmith

- **Customize trace previews**: Users can now configure which parts of a trace’s inputs and outputs appear directly in the tracing table, improving usability for custom data structures. (2026-02-06)
- **LangSmith Self-Hosted v0.13**: Major release for self-hosted customers improving feature parity with Cloud, performance, and operational control. (2026-01-16)

### Arize Phoenix

- **Claude Opus 4.6 Support**: Added support for Claude Opus 4.6 model in the Playground. (2026-02-09)
- **Tool Selection Evaluator**: New evaluator specifically for assessing tool selection logic. (2026-02-06)
- **Faithfulness Evaluator**: Added FaithfulnessEvaluator and deprecated HallucinationEvaluator for better RAG assessment. (2026-02-02)
- **Tool Invocation Accuracy Metric**: New metric to track the accuracy of tool calls within traces. (2026-02-02)
- **Custom Metric Cursor Rules**: UI update allowing creation of new built-in metrics (LLM classification) via cursor rules. (2026-01-21)

### Braintrust

- **Trace-level Scorers**: Custom code scorers can now access the entire execution trace to evaluate multi-step workflows and agent behavior. (2026-02)
- **LangSmith Integration**: Wrapper to route LangSmith traces to Braintrust, enabling parallel usage or migration. (2026-02)
- **Cursor & MCP Integration**: Integration with Cursor editor and Model Context Protocol for querying logs and running evals from the IDE. (2026-02)
- **Auto-instrumentation (Python/Ruby/Go)**: Zero-code tracing for major providers in Python, Ruby, and Go SDKs. (2026-01)
- **Temporal Integration**: Automatic tracing of Temporal workflows and activities for distributed agent observability. (2026-01)

### Langfuse

- **Corrected Outputs for Traces**: Capture improved versions of LLM outputs directly in trace views to build fine-tuning datasets. (2026-01-14)
- **Single Observation Evals**: Support for running evaluations on individual observations within a trace. (2026-02-09)
- **Thinking / Reasoning Rendering**: Visual rendering for 'thinking' or reasoning parts of model outputs in trace details. (2026-02-09)
- **Org Audit Log Viewer**: New viewer for organization-level audit logs to track security and access events. (2026-02-09)

### Logfire

- **Multi-token support for project migration**: Added support for handling multiple tokens during project migration workflows. (2026-02-04)
- **OTel Gen AI semantic conventions**: Added support for OpenTelemetry Gen AI semantic convention scalar attributes. (2026-01-28)
- **pytest integration**: Native integration with pytest for capturing test execution traces. (2026-01-26)
- **DSPy integration**: Added instrumentation support for the DSPy framework. (2026-01-16)
- **Claude SDK instrumentation**: Added dedicated instrumentation for the Anthropic Claude SDK. (2026-01-12)


## Report Archive

<!-- REPORT_ARCHIVE_START -->

| Date | Report |
|------|--------|
| 2026-02-11 | [View Report](./reports/2026-02-11.md) |
| 2026-02-10 | [View Report](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)
