# AGENT.md

Instructions for AI coding agents working on this repository.

## Project Overview

Automated bot that researches LLM Observability competitors weekly and generates feature comparison reports. Uses a crewAI 3-agent pipeline (Perplexity Sonar + Gemini Pro) to analyze products, then produces Markdown reports deployed via GitHub Pages.

## Pipeline

```
collect_updates → analyze_baseline → write_report → translate(ko/ja) → deploy(GitHub Pages)
```

## Analysis Architecture (crewAI 3-Agent)

**Per product (runs in parallel via ThreadPoolExecutor):**

Step 1 — Update Collection:
- Scrape changelog URLs (requests + BeautifulSoup; Playwright for JS pages)
- UpdateCollector agent (Perplexity Sonar): changelog + web search → `ProductUpdates`
- Receives baseline summary to avoid reporting already-known features

Step 2 — Baseline Analysis:
- BaselineAnalyzer agent (Gemini Pro): updates + existing baseline → `ProductChangeset`
- Only records genuine changes (new sub_features, available status changes, provision_method changes)
- Auto-saves updated baseline to `data/{product}/{date}.json`

**All products:**

Step 3 — Report Writing:
- ReportWriter agent (Gemini Pro): all changesets + baselines → `ReportSynthesis`
- Produces feature comparison ratings + AI comment (product highlights + market trend)

## Data Model

Baseline uses a **sub_features** structure:
- `FeatureBaseline`: item_name (49 standard items), available (yes/no/partial), sub_features list
- `SubFeature`: name (product's own feature name), provision_method, notes
- One standard item can map to multiple product-specific sub_features

## Module Structure

- `agents/`: crewAI agent factories (UpdateCollector, BaselineAnalyzer, ReportWriter)
- `crew.py`: crewAI orchestration (collect_updates, analyze_baseline, write_report, analyze_all)
- `analyzer.py`: re-exports analyze_all from crew.py (public API)
- `prompts.py`: Weave-integrated prompt management (load_prompts / publish_prompts)
- `cli.py`: CLI entry point (run / analyze / report / publish-prompts)
- `config.py`: product configs, categories, settings (single source of truth)
- `models.py`: Pydantic models (ProductUpdates, ProductChangeset, ProductBaseline, SubFeature, ReportSynthesis, AnalysisRun)
- `report.py`: Markdown report generation (4 sections)
- `translator.py`: ko/ja translation via OpenRouter
- `storage.py`: baseline and analysis result save/load
- `notify.py`: Slack notification (optional)
- `wb_report.py`: W&B Report publishing (optional)

## Key Configuration

- `config.py`: product list, URLs, 8 categories / 49 items, reference_urls
- `PERPLEXITY_API_KEY` (required): UpdateCollector — Sonar web search
- `OPENROUTER_API_KEY` (required): BaselineAnalyzer, ReportWriter

## Baseline Data

- `data/{product}/{date}.json`: versioned product baselines (49 items with sub_features)
- `data/analyzed/{date}/analysis.json`: analysis run results
- Initial generation: `python scripts/generate_baseline.py` (standalone script)
- Weekly update: BaselineAnalyzer auto-updates during pipeline run

## Report Format (4 Sections)

1. AI Comment — product highlights (1-2 lines each) + market trend (1 line)
2. Recent Updates — only products with detected changes
3. Feature Comparison (Summary) — 8-category O/△/X table
4. Detailed Feature Comparison — full 49-item table

## Prompt Management

Agent/task prompts are defined in `prompts.py` with defaults, versioned via `weave.StringPrompt`. Upload defaults to Weave with `python -m intel_bot publish-prompts`.

## 8-Category Framework (49 Items)

1. Core Tracing & Logging (8)
2. Agent & RAG Specifics (7)
3. Evaluation & Quality (8)
4. Guardrails & Safety (4)
5. Analytics & Dashboard (6)
6. Development Lifecycle (5)
7. Integration & DX (5)
8. Enterprise & Infrastructure (6)
