---
layout: default
title: Competitor intelligence reports for W&B Weave
---

# Competitor Intel Bot

[Detailed Comparison](./comparison) · [Product Detail](./competitor-detail) · [Competitive Intelligence (Internal)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## Latest Report

<!-- LATEST_REPORT_START -->

[📋 Latest Report (2026-02-11)](./reports/2026-02-11.md)


- Weave is differentiating through multimodal capabilities with the release of Audio Monitors (Feb 2026), moving beyond the text-centric evaluation focus of competitors like LangSmith and Arize Phoenix.
- The integration of Custom LoRAs into the Weave Playground reinforces W&B's unique 'Training-to-Inference' moat, offering a workflow for fine-tuned model evaluation that pure-play observability tools (Langfuse, Logfire) cannot match.
- LangSmith and Langfuse are establishing a lead in 'Agent Visualization' with dedicated graph views for complex workflows; Weave's linear trace views risk feeling outdated for debugging sophisticated agentic loops.
- Braintrust and Langfuse have professionalized Human-in-the-Loop (HITL) workflows with dedicated 'Annotation Queues' and Kanban views, creating a gap for Weave in large-scale manual labeling operations.
- Arize Phoenix is aggressively targeting the 'AI Engineer' persona with local-first features (CLI, Notebook support) and specialized 'Tool Selection' metrics, challenging Weave's dominance in the experimentation phase.
- Helicone and Braintrust continue to leverage 'AI Proxy' architectures (caching, rate limiting) as a wedge for cost-conscious engineering teams, a capability Weave's SDK-based approach does not address.

> Weave leads in the 'Training-to-Inference' flywheel with unique LoRA and multimodal capabilities, but faces increasing pressure from LangSmith and Langfuse on agent visualization and human-in-the-loop annotation workflows.


<!-- LATEST_REPORT_END -->

## New Features (Last 30 Days)

### [Weave](https://app.getbeamer.com/weave/en)

- **Audio monitors**: Support for evaluating audio outputs (MP3/WAV) using LLM judges, enabling observability for voice agents. (2026-02-01) [[docs]](https://wandb.ai/onlineinference/genai-research/reports/A-guide-to-LLM-debugging-tracing-and-monitoring--VmlldzoxMzk1MjAyOQ)
- **Dynamic Leaderboards**: Auto-generated leaderboards from evaluations with persistent filtering and customization options. (2026-01-29) [[docs]](https://wandb.ai/onlineinference/genai-research/reports/A-guide-to-LLM-debugging-tracing-and-monitoring--VmlldzoxMzk1MjAyOQ)
- **Custom LoRAs in Playground**: Ability to load and test custom fine-tuned LoRA weights directly in the Weave Playground. (2026-01-16) [[docs]](https://wandb.ai/onlineinference/genai-research/reports/A-guide-to-LLM-debugging-tracing-and-monitoring--VmlldzoxMzk1MjAyOQ)

### [LangSmith](https://changelog.langchain.com/feed.rss)

- **Customize trace previews**: Ability to customize how traces are previewed in the UI. (2026-02-06)
- **LangSmith Self-Hosted v0.13**: Update to the self-hosted enterprise version. (2026-01-16)
- **Client Library v0.7.1**: Updates to the JS/Python SDKs for better stability and OIDC support. (2026-02-10)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 Support**: Added support for Anthropic's Claude Opus 4.6 model in the playground with automatic cost tracking. (2026-02-09) [[docs]](https://arize.com/docs/phoenix/release-notes)
- **Tool Selection & Invocation Evaluators**: New specialized evaluators to judge if an agent chose the correct tool and invoked it with valid parameters. (2026-01-31) [[docs]](https://arize.com/docs/phoenix/release-notes)
- **Configurable Email Extraction (OAuth2)**: Support for custom email extraction paths (e.g., preferred_username) for Azure AD/Entra ID integrations. (2026-01-28) [[docs]](https://arize.com/docs/phoenix/release-notes)
- **CLI Commands for Prompts/Datasets**: New CLI commands to list, view, and pipe prompts/datasets, enabling terminal-based workflows. (2026-01-22) [[docs]](https://arize.com/docs/phoenix/release-notes)
- **Dataset Creation with Span Associations**: Ability to create datasets from traces while preserving bidirectional links to the original source spans. (2026-01-21) [[docs]](https://arize.com/docs/phoenix/release-notes)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **Trace-level scorers**: Custom code scorers can now access the entire execution trace to evaluate multi-step workflows and agent behavior. (2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **LangSmith Integration**: Experimental wrapper to route LangSmith traces to Braintrust, enabling parallel usage or migration. (2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **Auto-instrumentation (Python/Ruby/Go)**: Zero-code tracing for most providers in Python, Ruby, and Go SDKs. (2026-01) [[docs]](https://braintrust.dev/docs/changelog)
- **Temporal Integration**: Automatic tracing of Temporal workflows and activities, capturing distributed traces across workers. (2026-01) [[docs]](https://braintrust.dev/docs/changelog)
- **Kanban layout for reviews**: New UI for managing flagged spans with drag-and-drop cards for status updates. (2026-01) [[docs]](https://braintrust.dev/docs/changelog)

### [Langfuse](https://langfuse.com/changelog)

- **Corrected Outputs for Traces**: Capture improved versions of LLM outputs directly in trace views to build fine-tuning datasets. (2026-01-14) [[docs]](https://langfuse.com/changelog)
- **Reasoning/Thinking Trace Support**: Render thinking/reasoning parts in trace details (v3.148.0), supporting models like DeepSeek. (2026-01-27) [[docs]](https://github.com/langfuse/langfuse/pull/11615)
- **Single Observation Evals**: Support for running evaluations on single observations (v3.150.0). (2026-02-09) [[docs]](https://github.com/langfuse/langfuse/pull/11547)

### [Logfire](https://logfire.pydantic.dev/docs/release-notes)

- **Multi-token support for project migration**: Added support for using multiple tokens to facilitate project migration workflows. (2026-02-04) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **OTel Gen AI semantic conventions**: Added support for OpenTelemetry Gen AI semantic convention scalar attributes. (2026-01-28) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **Pytest integration**: Native integration with pytest for tracing test executions. (2026-01-26) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **DSPy integration**: Added instrumentation support for the DSPy framework. (2026-01-16) [[docs]](https://logfire.pydantic.dev/docs/release-notes)


## Report Archive

<!-- REPORT_ARCHIVE_START -->

| Date | Report |
|------|--------|
| 2026-02-11 | [View Report](./reports/2026-02-11.md) |
| 2026-02-10 | [View Report](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)
