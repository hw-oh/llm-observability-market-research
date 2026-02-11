---
layout: default
title: Competitor intelligence reports for W&B Weave
---

# Competitor Intel Bot

[Detailed Comparison](./comparison) · [Product Detail](./competitor-detail) · [Competitive Intelligence (Internal)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## Latest Report

<!-- LATEST_REPORT_START -->

[📋 Latest Report (2026-02-11)](./reports/2026-02-11.md)


- Weave secures a critical differentiator in the Voice Agent market with the release of Audio Monitors (Feb 2026), distancing itself from text-centric competitors like Langfuse and LangSmith.
- LangSmith's strategic pivot to 'Deployment' (infrastructure) and Braintrust's 'AI Proxy' threaten to relegate Weave to a passive observer role, as competitors move to control the traffic path.
- Arize Phoenix and Braintrust are raising the bar for Agent Evaluation with specialized 'Tool Selection' metrics and 'Trace-level scorers', challenging Weave's generic scorer framework.
- Weave's 'Dynamic Leaderboards' provide a strong counter-narrative to the static dashboards of Langfuse, offering superior flexibility for model comparison.
- Logfire's deep Pydantic integration and SQL-based analytics continue to erode Weave's share among Python-native engineering teams who prefer code-first debugging over UI-first workflows.
- Braintrust's new Cursor IDE integration signals a shift toward 'In-Editor Observability', potentially bypassing Weave's notebook-centric developer loop.

> Weave leads in multimodal (audio) observability and model training integration, but faces increasing pressure from LangSmith on agent infrastructure and Braintrust on enterprise proxy capabilities.


<!-- LATEST_REPORT_END -->

## New Features (Last 30 Days)

### [Weave](https://app.getbeamer.com/weave/en)

- **Audio monitors**: Support for creating monitors that observe and judge audio outputs alongside text, enabling evaluation of voice agents. (2026-02-01)
- **Dynamic Leaderboards**: Auto-generated leaderboards from evaluations with customizable filters and rich visualization options. (2026-01-29)
- **Custom LoRAs in Playground**: Ability to use custom fine-tuned LoRA weights from W&B Artifacts directly in the Weave Playground. (2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **Customize trace previews**: Ability to customize the trace preview pane to show relevant metadata or inputs/outputs at a glance. (2026-02-06)
- **Google Gen AI Wrapper**: New SDK wrapper for tracing Google Gen AI models without manual instrumentation. (2026-01-31)
- **LangSmith Self-Hosted v0.13**: Updated self-hosted release with stability improvements and new features from the cloud version. (2026-01-16)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 Support**: Playground support for Anthropic's latest model with extended thinking parameters and accurate cost tracking. (2026-02-09) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **Tool Selection & Invocation Evaluators**: New specialized evaluators to assess if agents selected the correct tool and invoked it with valid parameters. (2026-01-31) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **CLI Commands for Prompts/Datasets**: Comprehensive CLI support to list, view, and pipe prompts to AI assistants, and manage datasets/experiments from the terminal. (2026-01-22) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **Trace-to-Dataset with Span Links**: Ability to create curated datasets from production traces while maintaining bidirectional links to the original source spans. (2026-01-21) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **Export Annotations with Traces**: CLI support to export traces along with their manual labels and evaluation scores for offline analysis. (2026-01-19) [[docs]](https://docs.arize.com/phoenix/release-notes)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **Trace-level scorers**: Custom code scorers can now access the entire execution trace to evaluate multi-step workflows and agent behavior. (2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **LangSmith integration**: Wrapper to route traces to both LangSmith and Braintrust in parallel, or migrate solely to Braintrust. (2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **Cursor integration**: Braintrust extension for Cursor editor to query logs and run experiments via natural language. (2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **Auto-instrumentation (Python, Ruby, Go)**: Zero-code tracing support for Python, Ruby, and Go applications. (2026-01) [[docs]](https://braintrust.dev/docs/changelog)
- **Temporal integration**: Automatic tracing of Temporal workflows and activities with parent-child relationship mapping. (2026-01) [[docs]](https://braintrust.dev/docs/changelog)

### [Langfuse](https://langfuse.com/changelog)

- **Corrected Outputs for Traces**: Capture improved versions of LLM outputs directly in trace views to build fine-tuning datasets. (2026-01-14) [[docs]](https://langfuse.com/docs/observability/corrections)

### [Logfire](https://logfire.pydantic.dev/docs/release-notes)

- **Multi-token support for project migration**: Added support for handling multiple tokens to facilitate smoother project migrations. (2026-02-04) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **OTel Gen AI semantic conventions**: Added support for OpenTelemetry Gen AI semantic convention scalar attributes. (2026-01-28) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **Pytest integration**: New integration allowing seamless tracing and observability within pytest test runs. (2026-01-26) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **DSPy integration**: Official integration to trace and monitor DSPy applications. (2026-01-16) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
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
