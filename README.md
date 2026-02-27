# LLM Observability Market Research

[한국어](./README_ko.md)

An automated bot that researches LLM Observability competitors weekly and generates feature comparison reports using a crewAI multi-agent pipeline.

**[View Live Reports →](https://hw-oh.github.io/llm-observability-market-research/)**

## Quick Start

```bash
pip install -e .
python -m intel_bot run
```

## Architecture

The pipeline uses a **3-agent crewAI system** with baseline-driven change detection:

```
┌──────────────────────────────────────────────────────────────────┐
│  python -m intel_bot run                                         │
│                                                                  │
│  Per product (parallel):                                         │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐  │
│  │ 1. UpdateCollector   │───▶│ 2. BaselineAnalyzer             │  │
│  │    (Perplexity Sonar)│    │    (Gemini Pro)                 │  │
│  │    Changelog scrape  │    │    Compare updates vs baseline  │  │
│  │    + web search      │    │    → ProductChangeset           │  │
│  └─────────────────────┘    └─────────────────────────────────┘  │
│                                                                  │
│  All products:                                                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ 3. ReportWriter (Gemini Pro)                                │  │
│  │    Cross-product comparison → ReportSynthesis               │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                         ▼                                        │
│  Report (EN) → Translate (ko/ja) → GitHub Pages + W&B            │
└──────────────────────────────────────────────────────────────────┘
```

| Agent | Model | Role |
|-------|-------|------|
| **UpdateCollector** | Perplexity Sonar | Scrape changelogs + web search for recent updates |
| **BaselineAnalyzer** | Gemini Pro | Compare updates against baseline, produce changesets |
| **ReportWriter** | Gemini Pro | Cross-product feature ratings + AI commentary |

## Baseline Data

Each product has a **baseline JSON** (`data/{product}/{date}.json`) containing 49 feature items across 8 categories with sub-features. The baseline is the source of truth for change detection.

- **Initial generation**: `python scripts/generate_baseline.py` (standalone deep research)
- **Weekly update**: BaselineAnalyzer auto-updates after each analysis run

## Report Format (4 Sections)

1. **AI Comment** — Per-product highlights + market trend
2. **Recent Updates** — Only products with detected changes
3. **Feature Comparison (Summary)** — 8-category rating table
4. **Detailed Feature Comparison** — Full 49-item comparison

## Products Tracked

| Product | Docs | Changelog |
|---------|------|-----------|
| LangSmith | [docs.smith.langchain.com](https://docs.smith.langchain.com) | [changelog.langchain.com](https://changelog.langchain.com) |
| Langfuse | [langfuse.com/docs](https://langfuse.com/docs) | [langfuse.com/changelog](https://langfuse.com/changelog) |
| Braintrust | [braintrust.dev/docs](https://braintrust.dev/docs) | [braintrust.dev/docs/changelog](https://braintrust.dev/docs/changelog) |
| MLflow | [mlflow.org/docs/latest/genai](https://mlflow.org/docs/latest/genai) | [mlflow.org/releases](https://mlflow.org/releases) |
| Arize Phoenix | [docs.arize.com/phoenix](https://docs.arize.com/phoenix) | [arize.com/docs/phoenix/release-notes](https://arize.com/docs/phoenix/release-notes) |
| W&B Weave | [wandb.me/weave](https://wandb.me/weave) | [app.getbeamer.com/wandb/en](https://app.getbeamer.com/wandb/en) |

## 8-Category Framework (49 Items)

1. **Core Tracing & Logging** (8) — Request/Response Tracing, Nested Spans, Streaming, Multimodal, Auto-Instrumentation, Metadata, Token Counting, OpenTelemetry
2. **Agent & RAG Specifics** (7) — RAG Visualizer, Tool Call Rendering, Agent Graph, Step State, Session Replay, Failed Highlighting, MCP
3. **Evaluation & Quality** (8) — LLM-as-a-Judge, Custom Scorers, Datasets, Prompt Optimization, Regression Testing, Side-by-side, Annotation Queues, Online Eval
4. **Guardrails & Safety** (4) — PII Masking, Hallucination Detection, Jailbreak Guardrails, Policy as Code
5. **Analytics & Dashboard** (6) — Cost Analysis, Token Analytics, Latency P99, Error Monitoring, Embedding Viz, Custom Dashboards
6. **Development Lifecycle** (5) — Prompt CMS, Playground, Experiment Tracking, Fine-tuning, Version Control
7. **Integration & DX** (5) — SDK (Py/JS/Go), Gateway/Proxy, Frameworks, API/Webhooks, CI/CD
8. **Enterprise & Infrastructure** (6) — Deployment Options, Open Source, Compliance, RBAC/SSO, Audit Logs, Data Export

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PERPLEXITY_API_KEY` | Yes | UpdateCollector — Sonar web search |
| `OPENROUTER_API_KEY` | Yes | BaselineAnalyzer, ReportWriter — via OpenRouter |
| `WANDB_API_KEY` | No | Weave tracing + W&B Report publishing |
| `SLACK_WEBHOOK_URL` | No | Slack notification on completion |

### CLI Commands

```bash
python -m intel_bot run              # Full pipeline (primary)
python -m intel_bot analyze          # Analysis only
python -m intel_bot report           # Report generation only (needs analysis data)
python -m intel_bot publish-prompts  # Upload prompts to Weave
python scripts/generate_baseline.py  # One-time baseline generation
```

## Outputs

| Path | Content |
|------|---------|
| `reports/YYYY-MM-DD.md` | Weekly report (English) |
| `ko/reports/`, `ja/reports/` | Translated reports |
| `data/{product}/{date}.json` | Product baseline snapshots |
| `data/analyzed/{date}/analysis.json` | Analysis run results |
| `index.md` | Home — Summary + Report Archive |
| `comparison.md` | Feature comparison table |
| `competitor-detail.md` | Per-product detail |

## Optional Plugins

These run only when the corresponding env var is set. Failures do not block the pipeline.

- **Slack**: Completion notification (`SLACK_WEBHOOK_URL`)
- **W&B Report**: Interactive report + HTML logging + Alert (`WANDB_API_KEY`)

## CI/CD

GitHub Actions (`weekly-report.yml`) runs every Monday at 09:00 UTC.
Manual trigger: Actions → Weekly Competitor Report → Run workflow.

Reports are auto-committed and deployed to GitHub Pages.
