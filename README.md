# LLM Observability Market Research

[한국어](./README_ko.md)

Automated competitive intelligence bot for W&B Weave. Periodically researches competitor products and generates feature comparison reports.

## Report Generation Workflow

```
python -m intel_bot run
```

A single command runs the full 6-step pipeline sequentially.

### Step 1. Collect

Gathers feeds and extra docs for each competitor + Weave. Changelogs and release feeds are the primary data sources.

| Source | Module | What it captures |
|--------|--------|------------------|
| Changelog | `collectors/docs_scraper.py` / `feed.py` | Release notes — new features, version history (HTML or RSS) |
| GitHub/PyPI | `collectors/feed.py` | Release tags and package versions |
| Extra Docs | `collectors/docs_scraper.py` | Additional documentation pages (e.g. Weave enterprise docs) |
| Beamer | `collectors/beamer.py` | Weave only — W&B changelog via Beamer API |

Docs/changelog URLs are configured per competitor in `config.py`. Results are saved to `data/collections/YYYY-MM-DD.json`.

### Step 2. Discover

Searches the web (via Serper) for new LLM observability products not yet tracked. LLM extracts emerging competitors from search results. Pipeline continues even if this step fails.

### Step 3. Analyze — Per-Category (Perplexity Sonar)

Perplexity Sonar performs web search + analysis in a single call for each category per product. 8 categories per product, 6 products (5 competitors + Weave).

```
6 products x 8 categories x 1 Sonar call = 48 calls
```

Output: per-category ratings and summaries with web citations

### Step 4. Analyze — Per-Competitor Synthesis (Gemini Pro)

One Gemini Pro call per product synthesizes the 8 category results + feed data into a comprehensive analysis.

```
6 products x 1 Pro call = 6 calls
```

Output: overall summary, category ratings, new features, strengths/weaknesses, positioning

### Step 5. Analyze — Synthesis + Executive Summary (Gemini Pro)

Two additional Pro calls: one aggregates all product analyses into a market landscape, another generates an executive summary targeting VP/Engineering leadership.

Output: vendor comparison, enterprise signals, 5-7 key insight bullets, market insights

### Step 6. Report & Translate

Renders analysis results into Markdown files and translates to Korean/Japanese.

| File | Content |
|------|---------|
| `index.md` | Home — Executive Summary + Report Archive |
| `comparison.md` | Detailed comparison across 8 categories |
| `competitor-detail.md` | Per-product deep dive |
| `reports/YYYY-MM-DD.md` | Full weekly report |
| `ko/`, `ja/` | Translated versions |

## Pipeline Diagram

```
┌──────────────────────────────────────────────────────────┐
│  python -m intel_bot run                                 │
│                                                          │
│  ┌───────────┐  ┌──────────┐  ┌───────────────────────┐ │
│  │ 1. Collect │─▶│2. Discover│─▶│ 3. Category Analysis │ │
│  │           │  │          │  │   Sonar x48           │ │
│  │ feeds     │  │ Serper + │  │   (search + analyze)  │ │
│  │ docs      │  │ LLM call │  └──────────┬────────────┘ │
│  │ beamer    │  └──────────┘             │              │
│  └───────────┘                           ▼              │
│                               ┌───────────────────────┐ │
│                               │ 4. Product Synthesis  │ │
│                               │   Pro x6              │ │
│                               └──────────┬────────────┘ │
│                                          │              │
│                                          ▼              │
│                               ┌───────────────────────┐ │
│                               │ 5. Synthesis + Exec   │ │
│                               │   Pro x2              │ │
│                               └──────────┬────────────┘ │
│                                          │              │
│                                          ▼              │
│                               ┌───────────────────────┐ │
│                               │ 6. Report + Translate │ │
│                               │   LLM x8 (translate)  │ │
│                               └───────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

## Competitors

| Product | Docs | Changelog |
|---------|------|-----------|
| LangSmith | [docs.smith.langchain.com](https://docs.smith.langchain.com) | [changelog.langchain.com](https://changelog.langchain.com) |
| Langfuse | [langfuse.com/docs](https://langfuse.com/docs) | [langfuse.com/changelog](https://langfuse.com/changelog) |
| Braintrust | [braintrust.dev/docs](https://braintrust.dev/docs) | [braintrust.dev/docs/changelog](https://braintrust.dev/docs/changelog) |
| MLflow | [mlflow.org/docs/latest/genai](https://mlflow.org/docs/latest/genai) | [mlflow.org/releases](https://mlflow.org/releases) |
| Arize Phoenix | [docs.arize.com/phoenix](https://docs.arize.com/phoenix) | [arize.com/docs/phoenix/release-notes](https://arize.com/docs/phoenix/release-notes) |

## 8-Category Framework (49 items)

1. **Core Tracing & Logging** (8) — Full Request/Response Tracing, Nested Span & Tree View, Streaming, Multimodal Tracing, Auto-Instrumentation, Metadata & Tags, Token Counting, OpenTelemetry
2. **Agent & RAG Specifics** (7) — RAG Retrieval Visualizer, Tool/Function Call Rendering, Agent Execution Graph, Intermediate Step State, Session/Thread Replay, Failed Step Highlighting, MCP Integration
3. **Evaluation & Quality** (8) — LLM-as-a-Judge Wizard, Custom Eval Scorers, Dataset Management & Curation, Prompt Optimization/DSPy, Regression Testing, Side-by-side Comparison, Annotation Queues, Online Evaluation
4. **Guardrails & Safety** (4) — PII/Sensitive Data Masking, Hallucination Detection, Topic/Jailbreak Guardrails, Policy Management as Code
5. **Analytics & Dashboard** (6) — Cost Analysis & Attribution, Token Usage Analytics, Latency Heatmap & P99, Error Rate Monitoring, Embedding Space Visualization, Custom Metrics & Dashboard
6. **Development Lifecycle** (5) — Prompt Management (CMS), Playground & Sandbox, Experiment Tracking, Fine-tuning Integration, Version Control & Rollback
7. **Integration & DX** (5) — SDK Support (Py/JS/Go), Gateway/Proxy Mode, Popular Frameworks, API & Webhooks, CI/CD Integration
8. **Enterprise & Infrastructure** (6) — Deployment Options (SaaS/Dedicated/Self-Host), Open Source, Data Sovereignty & Compliance, RBAC & SSO, Audit Logs, Data Warehouse Export

## Setup

```bash
pip install -e .
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PERPLEXITY_API_KEY` | Yes | Perplexity Sonar API key (category analysis with web search) |
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key (Gemini Pro for synthesis) |
| `SERPER_DEV_API` | No | Serper.dev API key (used only for competitor discovery) |
| `SLACK_WEBHOOK_URL` | No | Slack notification webhook |
| `WANDB_API_KEY` | No | W&B Weave tracing |

### CLI Commands

```bash
python -m intel_bot collect    # Data collection only
python -m intel_bot discover   # Competitor discovery only
python -m intel_bot analyze    # Analysis only (requires collected data)
python -m intel_bot report     # Report generation only (requires analysis data)
python -m intel_bot run        # Full pipeline
python -m intel_bot preview    # Analyze + Korean preview from existing collection
```

## CI/CD

GitHub Actions (`weekly-report.yml`) runs automatically every Monday at 09:00 UTC.
Manual trigger: Actions → Weekly Competitor Report → Run workflow

Generated reports are automatically deployed via GitHub Pages.
