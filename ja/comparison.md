---
layout: default
title: LLM Observability — 詳細機能比較
---

# LLM Observability — 詳細機能比較
**日付**: 2026-02-12 | **モデル**: google/gemini-3-pro-preview

> ●●●(強力) / ●●○(中) / ●○○(弱) / ○○○(なし)

## Core Observability

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace Depth | ネストされた関数呼び出しの Tracing 深度 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Hierarchical Spans | 親子関係の Span 構造 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Prompt Logging | LLM Prompt の自動キャプチャ | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Response Logging | LLM レスポンスの自動キャプチャ | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Token Tracking | 入出力のトークン使用量のカウント | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Latency Analysis | Span ごとおよびエンドツーエンドのレイテンシ測定 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Replay | Dashboard UI 上でのステップバイステップの Trace 再生 | ●●○ | ●●● | ●●○ | ●●● | ●●○ | ●●● |

## Agent / RAG Observability

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Tool Call Tracing | ツール/関数呼び出しの入出力キャプチャ | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Retrieval Tracing | Retriever のクエリと返されたドキュメントの Logging | ●●● | ●●● | ●●● | ●●○ | ●●● | ●●● |
| Memory Tracing | 会話メモリの読み書きのトラッキング | ●●○ | ●●○ | ●●● | ●●○ | ●●● | ●●○ |
| Multi-step Reasoning | マルチターン Agent の推論チェーンの可視化 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Workflow Graph | Agent ワークフローの DAG またはグラフ表示 | ●●○ | ●●● | ●●● | ●●○ | ●●○ | ●●○ |
| Failure Visualization | Trace 内の失敗したステップのハイライト表示 | ●●○ | ●●● | ●●○ | ●●● | ●●● | ●●● |

## Evaluation Integration

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace→Dataset | 本番環境の Trace を Eval データセットに変換 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| LLM-as-Judge | 組み込み LLM による Eval Scoring | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Custom Eval Metrics | ユーザー定義の Eval 関数 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Regression Detection | 品質の劣化（デグレード）を自動検出 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Model Comparison | モデル出力のサイドバイサイド比較 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Human Feedback UI | 人間によるアノテーションとラベル付け用 UI | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |

## Monitoring & Metrics

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Dashboard | リアルタイムの LLM コスト追跡 Dashboard | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Token Analytics | トークン使用量の内訳とトレンド分析 | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |
| Latency Monitoring | レイテンシのパーセンタイル表示とアラート | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Error Tracking | エラー率のモニタリングとアラート | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |
| Tool Success Rate | ツール呼び出しの成功/失敗率 | ●●○ | ●●○ | ●●● | ●●○ | ●●● | ●●● |
| Custom Metrics | ユーザー定義のカスタムメトリクス追跡 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |

## Experiment / Improvement Loop

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Versioning | Prompt テンプレートのバージョン管理 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Model Versioning | モデルバージョンと設定のトラッキング | ●●● | ●●○ | ●●○ | ●●● | ●●● | ●●● |
| Experiment Tracking | A/B テストと実験の管理 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Dataset Versioning | バージョン管理された Eval および学習データセット | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Continuous Eval | スケジュールまたはトリガーによる Eval 実行 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| RL/Fine-tuning Link | Fine-tuning パイプラインとの連携 | ●●● | ●●○ | ●●○ | ●○○ | ●●○ | ●○○ |

## DevEx / Integration

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK Support | Python, JS/TS などの公式 SDK | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Framework Integration | LangChain, LlamaIndex などの組み込みサポート | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Custom Model Support | 非標準またはセルフホストモデルの Tracing | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| API Access | プログラムからアクセス可能な REST または GraphQL API | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| Streaming Tracing | LLM の Streaming レスポンスの Tracing | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |
| CLI/Infra Integration | CLI ツールおよび Infrastructure-as-Code のサポート | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |

## Enterprise & Security

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| On-prem/VPC | セルフホストまたは VPC デプロイオプション | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● |
| RBAC | ロールベースのアクセス制御 | ●●○ | ●●● | ●●● | ●●● | ●●● | ●●● |
| PII Masking | PII（個人情報）の自動検出とマスキング | ○○○ | ●●○ | ●●● | ●●○ | ●●○ | ○○○ |
| Audit Logs | ユーザーおよびシステム操作の監査ログ | ○○○ | ●●● | ●●● | ●●○ | ●●○ | ○○○ |
| Data Retention | 設定可能なデータ保持ポリシー | ●●○ | ●●● | ●●● | ●●● | ●●○ | ●●● |
| Region Support | マルチリージョンまたはデータレジデンシ対応 | ●○○ | ●●● | ●●● | ●●○ | ●●● | ●●○ |