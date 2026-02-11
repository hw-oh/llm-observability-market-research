# Competitor Intel Bot

[한국어](./README_ko.md)

Automated competitive intelligence bot for W&B Weave. Periodically researches competitor products and generates feature comparison reports.

## Report Generation Workflow

```
python -m intel_bot run
```

A single command runs the full 6-step pipeline sequentially.

### Step 1. Collect

Gathers data from multiple sources for each competitor + Weave. Official docs and changelogs are primary sources for feature accuracy; web search supplements with broader market context.

| Source | Module | What it captures |
|--------|--------|------------------|
| Official Docs | `collectors/docs_scraper.py` | Product documentation pages — feature details, API references |
| Changelog | `collectors/docs_scraper.py` / `feed.py` | Release notes — new features, version history (HTML or RSS) |
| Web Search | `collectors/serper.py` | News, blogs, community discussions via Serper.dev API |
| GitHub/PyPI | `collectors/feed.py` | Release tags and package versions |
| Beamer | `collectors/beamer.py` | Weave only — W&B changelog via Beamer API |

Docs/changelog URLs are configured per competitor in `config.py`. Results are saved to `data/collections/YYYY-MM-DD.json`.

### Step 2. Discover

Searches the web for new LLM observability products not yet tracked. LLM extracts emerging competitors from search results. Pipeline continues even if this step fails.

### Step 3. Analyze — Per-Competitor (LLM)

One LLM call per competitor, analyzing across a 7-category framework.

```
5 competitors x 1 LLM call = 5 calls
```

Output: per-category ratings, new features, strengths/weaknesses, positioning

### Step 4. Analyze — Synthesis (LLM)

Aggregates all 5 individual analyses into a single LLM call.

Output: vendor ratings comparison, Weave strengths/weaknesses, positioning, enterprise signals

### Step 5. Analyze — Executive Summary (LLM)

A **dedicated LLM call** generates the executive summary from synthesis results. Uses a specialized prompt targeting VP/Engineering leadership briefing quality.

Output: 5-7 key insight bullets + one-line verdict

### Step 6. Report & Translate

Renders analysis results into Markdown files and translates to Korean/Japanese.

| File | Content |
|------|---------|
| `index.md` | Home — Executive Summary + Report Archive |
| `comparison.md` | Detailed comparison across 7 categories |
| `competitor-detail.md` | Per-product deep dive |
| `reports/YYYY-MM-DD.md` | Full weekly report |
| `ko/`, `ja/` | Translated versions |

## Pipeline Diagram

```
┌─────────────────────────────────────────────────────────┐
│  python -m intel_bot run                                │
│                                                         │
│  ┌───────────┐   ┌──────────┐   ┌────────────────────┐ │
│  │ 1. Collect │──▶│2. Discover│──▶│ 3. Analyze (x5)   │ │
│  │           │   │          │   │   Per-competitor    │ │
│  │ serper    │   │ LLM call │   │   LLM call x5      │ │
│  │ docs      │   └──────────┘   └─────────┬──────────┘ │
│  │ feeds     │                            │            │
│  │ beamer    │                            ▼            │
│  └───────────┘                  ┌────────────────────┐ │
│                                 │ 4. Synthesize      │ │
│                                 │   Cross-cutting    │ │
│                                 │   LLM call x1      │ │
│                                 └─────────┬──────────┘ │
│                                           │            │
│                                           ▼            │
│                                 ┌────────────────────┐ │
│                                 │ 5. Exec Summary    │ │
│                                 │   Dedicated LLM x1 │ │
│                                 └─────────┬──────────┘ │
│                                           │            │
│                                           ▼            │
│                                 ┌────────────────────┐ │
│                                 │ 6. Report          │ │
│                                 │   MD + Translate    │ │
│                                 │   LLM call x8      │ │
│                                 └────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Competitors

| Product | Docs | Changelog |
|---------|------|-----------|
| LangSmith | [docs.smith.langchain.com](https://docs.smith.langchain.com) | [changelog.langchain.com](https://changelog.langchain.com) |
| Langfuse | [langfuse.com/docs](https://langfuse.com/docs) | [langfuse.com/changelog](https://langfuse.com/changelog) |
| Braintrust | [braintrust.dev/docs](https://braintrust.dev/docs) | [braintrust.dev/docs/changelog](https://braintrust.dev/docs/changelog) |
| MLflow | [mlflow.org/docs/latest/genai](https://mlflow.org/docs/latest/genai) | [mlflow.org/releases](https://mlflow.org/releases) |
| Arize Phoenix | [docs.arize.com/phoenix](https://docs.arize.com/phoenix) | [arize.com/docs/phoenix/release-notes](https://arize.com/docs/phoenix/release-notes) |

## 7-Category Framework

1. **Core Observability** — Trace Depth, Hierarchical Spans, Prompt/Response Logging, Token Tracking, Latency Analysis, Replay
2. **Agent / RAG Observability** — Tool Call Tracing, Retrieval Tracing, Memory Tracing, Multi-step Reasoning, Workflow Graph, Failure Visualization
3. **Evaluation Integration** — Trace→Dataset, LLM-as-Judge, Custom Eval Metrics, Regression Detection, Model Comparison, Human Feedback
4. **Monitoring & Metrics** — Cost Dashboard, Token Analytics, Latency Monitoring, Error Tracking, Tool Success Rate, Custom Metrics
5. **Experiment / Improvement Loop** — Prompt/Model/Dataset Versioning, Experiment Tracking, Continuous Eval, RL/Fine-tuning
6. **DevEx / Integration** — SDK Support, Framework Integration, Custom Model Support, API Access, Streaming Tracing, CLI/Infra
7. **Enterprise & Security** — On-prem/VPC, RBAC, PII Masking, Audit Logs, Data Retention, Region Support

## Setup

```bash
pip install -e .
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SERPER_DEV_API` | Yes | Serper.dev API key |
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key |
| `SLACK_WEBHOOK_URL` | No | Slack notification webhook |
| `WANDB_API_KEY` | No | W&B Weave tracing |

### CLI Commands

```bash
python -m intel_bot collect    # Data collection only
python -m intel_bot discover   # Competitor discovery only
python -m intel_bot analyze    # Analysis only (requires collected data)
python -m intel_bot report     # Report generation only (requires analysis data)
python -m intel_bot run        # Full pipeline
```

## CI/CD

GitHub Actions (`weekly-report.yml`) runs automatically every Monday at 09:00 UTC.
Manual trigger: Actions → Weekly Competitor Report → Run workflow

Generated reports are automatically deployed via GitHub Pages.
