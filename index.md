---
layout: default
title: Competitor intelligence reports for W&B Weave
---

# Competitor Intel Bot

[Detailed Comparison](./comparison) · [Product Detail](./competitor-detail) · [Competitive Intelligence (Internal)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## Latest Report

<!-- LATEST_REPORT_START -->

[📋 Latest Report (2026-02-11)](./reports/2026-02-11.md)


- Weave differentiates with multimodal support (Audio Monitors) while competitors remain text/tool-focused, opening a lead in voice-agent observability.
- LangSmith and Langfuse are aggressively deepening 'Agentic Observability' with specialized visualizations for reasoning steps and cyclic graphs, pressuring Weave's trace views.
- Braintrust and LangSmith dominate the 'Human-in-the-Loop' narrative with dedicated Annotation Queues, a workflow feature Weave currently addresses less directly.
- Weave's 'Dynamic Leaderboards' release counters Braintrust's evaluation maturity by automating model comparison, a critical need for enterprise model selection.
- The 'Open Standards' threat is growing, with Arize Phoenix and Logfire leveraging OpenTelemetry (OTLP) to appeal to teams avoiding vendor-specific instrumentation.
- Weave retains a unique defensive moat via deep integration with W&B Training/Artifacts, offering a native 'Fix-by-Fine-tuning' loop that competitors can only support via export.
- LangSmith's rebrand of LangGraph Platform to 'Deployment' signals a shift toward owning the runtime layer, threatening to commoditize pure observability players.

> Weave leads in multimodal observability and training integration, but faces specific pressure from LangSmith on agent visualization and Braintrust on enterprise evaluation workflows.


<!-- LATEST_REPORT_END -->

## New Features (Last 30 Days)

### [Weave](https://app.getbeamer.com/weave/en)

- **Audio Monitors**: Support for creating monitors that observe and judge audio outputs alongside text, enabling evaluation of voice agents. (2026-02-01)
- **Dynamic Leaderboards**: Auto-generated leaderboards from evaluations with persistent customization and CSV export. (2026-01-29)
- **Custom LoRAs in Playground**: Ability to use custom fine-tuned LoRA weights from W&B Artifacts directly in the Weave Playground. (2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **Customize trace previews**: Ability to customize how traces are previewed in the UI, improving triage speed. (2026-02-06) [[docs]](https://docs.smith.langchain.com/observability)
- **LangSmith Self-Hosted v0.13**: Updated self-hosted release with stability improvements and new features. (2026-01-16) [[docs]](https://docs.smith.langchain.com/self_hosting)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 Support**: Added support for Anthropic's Claude Opus 4.6 model in the playground with automatic cost tracking. (2026-02-09) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **Tool Selection & Invocation Evaluators**: New specialized evaluators to assess if agents selected the correct tool and invoked it with valid parameters. (2026-01-31) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **CLI for Prompts & Datasets**: CLI commands to list, view, and pipe prompts/datasets, enabling integration with AI coding assistants. (2026-01-22) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **Dataset Creation from Traces**: Ability to create datasets directly from traces while preserving bidirectional links to source spans. (2026-01-21) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **Export Annotations with Traces**: CLI support to export human feedback and annotations alongside traces for offline analysis. (2026-01-19) [[docs]](https://docs.arize.com/phoenix/release-notes)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **Trace-level scorers**: Custom code scorers can now access the entire execution trace to evaluate multi-step workflows and agent behavior. (2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **LangSmith integration (Experimental)**: Wrapper to route LangSmith tracing and evaluation calls to Braintrust, enabling dual-logging or migration. (2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **Auto-instrumentation (Python, Ruby, Go)**: Zero-code tracing for most providers in Python, Ruby, and Go SDKs. (2026-01) [[docs]](https://braintrust.dev/docs/changelog)
- **Temporal integration**: Automatic tracing of Temporal workflows and activities, capturing execution spans and distributed traces. (2026-01) [[docs]](https://braintrust.dev/docs/changelog)
- **Navigate to trace origins**: Link from traces in logs back to the originating prompt or dataset row for rapid iteration. (2026-02) [[docs]](https://braintrust.dev/docs/changelog)

### [Langfuse](https://langfuse.com/changelog)

- **Thinking / Reasoning Rendering**: Renders chain-of-thought and reasoning parts explicitly in trace details (v3.148.0). (2026-02-01)
- **Single Observation Evals**: Support for running evaluations on single observations rather than full traces (v3.150.0). (2026-02-05)
- **Corrected Outputs for Traces**: Capture improved versions of LLM outputs directly in trace views to build fine-tuning datasets. (2026-01-14) [[docs]](https://langfuse.com/docs/observability/features/corrections)

### [Logfire](https://logfire.pydantic.dev/docs/release-notes)

- **Multi-token support for project migration**: Added support for using multiple tokens to facilitate project migration. (2026-02-04) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **OTel Gen AI semantic conventions**: Added support for OpenTelemetry Gen AI semantic convention scalar attributes. (2026-01-28) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **pytest integration**: New integration to support observability within pytest executions. (2026-01-26) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **DSPy integration**: Added native instrumentation support for the DSPy framework. (2026-01-16) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **Claude SDK instrumentation**: Added specific instrumentation for the Anthropic Claude SDK. (2026-01-12) [[docs]](https://logfire.pydantic.dev/docs/release-notes)


## Report Archive

<!-- REPORT_ARCHIVE_START -->

| Date | Report |
|------|--------|
| 2026-02-11 | [View Report](./reports/2026-02-11.md) |
| 2026-02-10 | [View Report](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)
