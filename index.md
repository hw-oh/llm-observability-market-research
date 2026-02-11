---
layout: default
title: Competitor intelligence reports for W&B Weave
---

# Competitor Intel Bot

[Detailed Comparison](./comparison) · [Product Detail](./competitor-detail) · [Competitive Intelligence (Internal)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## Latest Report

<!-- LATEST_REPORT_START -->

[📋 Latest Report (2026-02-11)](./reports/2026-02-11.md)


- LangSmith is aggressively moving from passive observability to active runtime management with 'LangGraph Cloud', threatening to lock in the entire agent lifecycle before Weave can capture data.
- Braintrust is successfully flanking on the 'Enterprise Engineering' side by integrating directly into the IDE (Cursor) and supporting backend languages (Java, Go, C#) that Weave currently neglects.
- The acquisition and shutdown of Humanloop creates an immediate tactical opportunity to capture displaced customers, though Langfuse's superior Prompt CMS makes them a strong contender for this migration.
- Arize Phoenix and Langfuse are squeezing the bottom-up adoption funnel with strong 'Local-First' and self-hosting stories, appealing to security-conscious engineers hesitant to adopt SaaS.
- Logfire's deep integration with Pydantic allows it to own the 'Full Stack' trace (Database + API + LLM), exposing Weave's lack of visibility into non-LLM infrastructure components.
- Agentic observability is becoming the primary battleground; LangSmith and Langfuse have shipped dedicated Graph/Reasoning visualizations that currently outperform Weave's standard trace views for cyclic workflows.

> Weave maintains its moat in the model training-to-production lineage, but faces acute pressure from LangSmith on agentic orchestration and Braintrust on enterprise developer workflows.


<!-- LATEST_REPORT_END -->

## New Features (Last 30 Days)

### LangSmith

- **Customize Trace Previews**: Users can now configure which parts of a trace’s inputs and outputs appear directly in the tracing table, improving usability for custom data structures. (2026-02-06)
- **LangSmith Self-Hosted v0.13**: Major release for self-hosted customers expanding feature parity with Cloud, including 'Insights' and performance improvements. (2026-01-16)
- **SDK v0.7.1**: Updates to Python/JS client libraries ensuring compatibility with latest LangChain versions and improved stability. (2026-02-10)

### Arize Phoenix

- **Claude Opus 4.6 Support**: Added support for Claude Opus 4.6 in the Playground for side-by-side comparison. (2026-02-09)
- **Tool Selection Evaluator**: New evaluator specifically designed to measure the accuracy of agent tool selection logic. (2026-02-06)
- **FaithfulnessEvaluator**: Introduction of a new FaithfulnessEvaluator (deprecating HallucinationEvaluator) for more nuanced RAG checking. (2026-02-02)
- **Tool Invocation Accuracy Metric**: Added specific metrics to track how often agents invoke tools correctly. (2026-01-27)

### Braintrust

- **Navigate to trace origins**: Ability to link traces back to the specific prompt version or dataset row that generated them. (2026-02)
- **Trace-level scorers**: Custom scorers can now access the entire execution trace to evaluate multi-step workflows and agent behavior. (2026-02)
- **LangSmith integration**: Wrapper to route LangSmith tracing and evaluation calls to Braintrust in parallel or exclusively. (2026-02)
- **Cursor integration**: Braintrust extension for Cursor editor to query logs and fetch experiment results via natural language. (2026-02)
- **Auto-instrumentation (Python/Ruby/Go)**: Zero-code tracing support for major languages, simplifying initial setup. (2026-01)

### Langfuse

- **Corrected Outputs for Traces**: Capture improved versions of LLM outputs directly in trace views to build fine-tuning datasets. (2026-01-14)
- **Inline Comments on Observation I/O**: Anchor comments to specific text selections within trace inputs and outputs. (2026-01-07)

### Logfire

- **Multi-token Project Migration**: Support for migrating projects using multiple tokens. (2026-02-04)
- **OTel Gen AI Semantic Conventions**: Added support for OpenTelemetry Gen AI semantic convention scalar attributes. (2026-01-28)
- **Pytest Integration**: Native integration for tracing pytest executions. (2026-01-26)
- **DSPy Integration**: Added instrumentation support for the DSPy framework. (2026-01-16)
- **Claude SDK Instrumentation**: Added specific instrumentation for the Anthropic Claude SDK. (2026-01-12)


## Report Archive

<!-- REPORT_ARCHIVE_START -->

| Date | Report |
|------|--------|
| 2026-02-11 | [View Report](./reports/2026-02-11.md) |
| 2026-02-10 | [View Report](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)
