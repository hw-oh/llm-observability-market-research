---
layout: default
title: Competitor intelligence reports for W&B Weave
---

# Competitor Intel Bot

[Detailed Comparison](./comparison) · [Product Detail](./competitor-detail) · [Competitive Intelligence (Internal)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## Latest Report

<!-- LATEST_REPORT_START -->

[📋 Latest Report (2026-02-11)](./reports/2026-02-11.md)


- Weave's introduction of Audio Monitors (Feb 2026) creates a distinct multimodal advantage, as competitors like LangSmith and Langfuse remain primarily text/tool-focused.
- MLflow's release of 'Continuous Online Monitoring' and 'Judge Builder' (Jan 2026) aggressively targets the production-to-evaluation loop, challenging Weave's automation capabilities with a 'default' solution for Databricks customers.
- LangSmith continues to dominate agentic visualization with native LangGraph integration; Weave's linear trace views face pressure from LangSmith's cyclic graph views and Arize Phoenix's new tool-specific evaluators.
- Braintrust is successfully differentiating via 'Universal' enterprise support (Java, Go, C# SDKs) and deep IDE integration (Cursor), threatening Weave's hold on large, polyglot engineering organizations.
- Langfuse's 'Prompt CMS' and granular cost analytics (ClickHouse-backed) continue to outperform Weave in serving non-technical stakeholders and finance-conscious teams.
- Weave's integration of Custom LoRAs into the Playground (Jan 2026) reinforces its unique 'Training-to-Inference' moat, a capability no pure-play observability vendor (LangSmith, Phoenix) can match.

> Weave leads in multimodal evaluation and training-to-inference workflows, but faces intensifying pressure from LangSmith on agentic visualization and MLflow on automated production monitoring.


<!-- LATEST_REPORT_END -->

## New Features (Last 30 Days)

### [Weave](https://app.getbeamer.com/wandb/en)

- **Audio Monitors**: Support for creating monitors that observe and judge audio outputs alongside text, using audio-capable LLMs. (2026-02-01)
- **Dynamic Leaderboards**: Auto-generated leaderboards from evaluations with persistent customization and CSV export. (2026-01-29)
- **Custom LoRAs in Playground**: Ability to load custom fine-tuned LoRA weights from W&B Artifacts directly into the Weave Playground for inference. (2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **Customize trace previews**: UI update allowing users to customize how trace previews are displayed in the dashboard. (2026-02-06)
- **LangSmith Self-Hosted v0.13**: Update to the self-hosted enterprise infrastructure components. (2026-01-16)

### [Langfuse](https://langfuse.com/changelog)

- **Corrected Outputs for Traces**: Capture improved versions of LLM outputs directly in trace views to build fine-tuning datasets. (2026-01-14)
- **Reasoning/Thinking Rendering**: New UI support to render 'thinking' or 'reasoning' parts of model outputs in trace details (v3.148). (2026-01-20)
- **Org Audit Log Viewer**: Added a viewer for organization-level audit logs to enhance security and compliance visibility. (2026-01-20)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **Trace-level Scorers**: Custom code scorers can now access the entire execution trace to evaluate multi-step workflows and agent behavior. (2026-02)
- **LangSmith Integration**: Wrapper to send tracing and evaluation calls to both LangSmith and Braintrust in parallel, or route solely to Braintrust. (2026-02)
- **Cursor Integration**: Integration with Cursor editor via MCP to query logs and fetch experiment results using natural language. (2026-02)
- **Auto-instrumentation (Py/Ruby/Go)**: Zero-code tracing support added for Python, Ruby, and Go applications. (2026-01)
- **Temporal Integration**: Automatic tracing of Temporal workflows and activities with parent-child relationship mapping. (2026-01)

### [MLflow](https://mlflow.org/releases)

- **Continuous Online Monitoring**: Automatically run LLM judges on incoming production traces to detect quality issues in real-time. (2026-01-29)
- **Dashboards for Agent Performance**: Pre-built visualization tabs for monitoring agent latency, request counts, and tool usage summaries. (2026-01-29)
- **Judge Builder UI**: No-code interface to create, test, and validate custom LLM judges before deployment. (2026-01-29)
- **MemAlign Judge Optimizer**: Algorithm that learns evaluation guidelines from past human feedback to improve judge accuracy. (2026-01-29)
- **MLflow Assistant**: In-product AI chatbot powered by Claude Code to help debug traces and suggest fixes. (2026-01-29)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 Support**: Added support for Anthropic's latest model with extended thinking parameter support and cost tracking. (2026-02-09)
- **Tool Selection & Invocation Evaluators**: Specialized evaluators to judge if an agent selected the correct tool and invoked it with valid parameters. (2026-01-31)
- **CLI for Prompts & Datasets**: New CLI commands to manage prompts, datasets, and experiments directly from the terminal, optimized for AI coding assistants. (2026-01-22)
- **Trace-to-Dataset with Span Links**: Ability to create datasets from production traces while maintaining bidirectional links to the original source spans. (2026-01-21)
- **Export Annotations with Traces**: CLI support to export human and LLM annotations alongside traces for offline analysis. (2026-01-19)


## Report Archive

<!-- REPORT_ARCHIVE_START -->

| Date | Report |
|------|--------|
| 2026-02-11 | [View Report](./reports/2026-02-11.md) |
| 2026-02-10 | [View Report](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)
