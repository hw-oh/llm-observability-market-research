# LLM Observability Market Research

[한국어](./README_ko.md)

An automated bot that periodically researches W&B Weave's competitors and generates feature comparison reports.

## Quick Start

```bash
pip install -e .
python -m intel_bot run
```

A single command runs the full pipeline: **Collect → Discover → Analyze → Report**.

## Architecture: crewAI Multi-Agent Pipeline

Analysis is powered by a crewAI-based multi-agent system:

| Agent | Model | Role |
|-------|-------|------|
| **SearchAgent** | Perplexity Sonar | Web search-based evidence gathering |
| **UrlReferenceAgent** | Gemini Flash | Extract facts from reference URL documents |
| **ExtractionAgent** | Gemini Pro | Merge evidence into structured product analysis |
| **ReportSynthesisAgent** | Gemini Pro | Cross-product synthesis and executive summary |

Per product, SearchAgent and UrlReferenceAgent run in parallel, then ExtractionAgent combines their outputs. After all products are analyzed, ReportSynthesisAgent produces the market-level report.

## Pipeline Steps

1. **Collect** — Gather feeds (GitHub/PyPI/RSS) and scrape `reference_urls` from config
2. **Discover** (optional) — Search for emerging competitors via Serper
3. **Analyze** — crewAI multi-agent analysis (per-product + synthesis)
4. **Report & Translate** — Generate Markdown reports + ko/ja translations

## Configuration

Products and reference URLs are defined in `config.py`:

```python
CompetitorConfig(
    name="LangSmith",
    docs_url="https://docs.smith.langchain.com",
    changelog_url="https://changelog.langchain.com/feed.rss",
    reference_urls=[
        "https://docs.smith.langchain.com/observability",
        "https://docs.smith.langchain.com/evaluation",
    ],
)
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PERPLEXITY_API_KEY` | Yes | Perplexity Sonar (SearchAgent) |
| `OPENROUTER_API_KEY` | Yes | OpenRouter (UrlReferenceAgent, ExtractionAgent, translation) |
| `SERPER_DEV_API` | No | Serper.dev (discovery only) |
| `SLACK_WEBHOOK_URL` | No | Slack notification (optional plugin) |
| `WANDB_API_KEY` | No | W&B Weave tracing + Report publishing (optional plugin) |

### CLI Commands

```bash
python -m intel_bot run        # Full pipeline (primary)
python -m intel_bot collect    # Data collection only (debug)
python -m intel_bot analyze    # Analysis only (debug, needs collection data)
python -m intel_bot report     # Report generation only (debug, needs analysis data)
python -m intel_bot discover   # Competitor discovery only (debug)
```

## Outputs

| File | Content |
|------|---------|
| `index.md` | Home — Executive Summary + Report Archive |
| `comparison.md` | 8-category detailed comparison table |
| `competitor-detail.md` | Per-product analysis detail |
| `reports/YYYY-MM-DD.md` | Weekly report |
| `ko/`, `ja/` | Translations |

## Optional Plugins

These features run only when the corresponding env var is set. Failures do not block the core pipeline.

- **Slack**: Notification on report completion (`SLACK_WEBHOOK_URL`)
- **W&B Report**: Publish interactive W&B Report + Alert (`WANDB_API_KEY`)

## CI/CD

GitHub Actions (`weekly-report.yml`) runs every Monday at 09:00 UTC.
Manual trigger: Actions → Weekly Competitor Report → Run workflow.

Reports are auto-deployed to GitHub Pages.
