---
layout: default
title: LLM Observability — 機能詳細比較
---

# LLM Observability — 機能詳細比較
**日付**: 2026-02-12 | **モデル**: google/gemini-3-pro-preview

> O(強力) / △(弱い) / X(なし)

## Core Observability

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace Depth | ネストされた関数呼び出しの Tracing 深度 | O | O | O | O | O | O |
| Hierarchical Spans | 親子関係を持つ Span の構造化 | O | O | O | O | O | O |
| Prompt Logging | LLM Prompt の自動キャプチャ | O | O | O | O | O | O |
| Response Logging | LLM レスポンスの自動キャプチャ | O | O | O | O | O | O |
| Token Tracking | 入出力のトークン使用量のカウント | O | O | O | O | O | O |
| Latency Analysis | Span ごとおよびエンドツーエンドの Latency 測定 | O | O | O | O | O | O |
| Replay | UI 上でのステップバイステップの Trace 再生 | △ | O | △ | O | △ | O |

## Agent / RAG Observability

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Tool Call Tracing | ツール/関数呼び出しの入出力キャプチャ | O | O | O | O | O | O |
| Retrieval Tracing | Retriever のクエリと返されたドキュメントのログ記録 | O | O | O | △ | O | O |
| Memory Tracing | 会話 Memory の読み書きの追跡 | X | O | O | △ | O | △ |
| Multi-step Reasoning | マルチターン Agent の推論チェーンの可視化 | O | O | O | O | O | O |
| Workflow Graph | Agent ワークフローの DAG またはグラフ表示 | △ | O | O | O | O | O |
| Failure Visualization | Trace 内の失敗したステップのハイライト表示 | O | O | O | △ | O | O |

## Evaluation Integration

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace→Dataset | 本番環境の Trace を Eval データセットに変換 | O | O | O | O | O | O |
| LLM-as-Judge | 組み込み LLM による Eval Scoring | O | O | O | O | O | O |
| Custom Eval Metrics | ユーザー定義の Eval 関数 | O | O | O | O | O | O |
| Regression Detection | 品質の低下（Regression）を自動検出 | O | O | O | O | O | O |
| Model Comparison | モデル出力のサイドバイサイド比較 | O | O | O | O | O | O |
| Human Feedback UI | 人間によるアノテーションとラベル付け用 UI | O | O | O | O | O | O |

## Monitoring & Metrics

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Dashboard | リアルタイムの LLM コスト追跡 Dashboard | O | O | O | O | O | O |
| Token Analytics | トークン使用量の内訳とトレンド分析 | O | O | O | O | O | O |
| Latency Monitoring | Latency のパーセンタイル表示とアラート | O | O | O | O | O | O |
| Error Tracking | エラー率のモニタリングとアラート | O | O | O | O | O | O |
| Tool Success Rate | ツール呼び出しの成功/失敗率 | △ | O | O | △ | O | O |
| Custom Metrics | ユーザー定義のカスタムメトリクス追跡 | O | O | O | O | O | O |

## Experiment / Improvement Loop

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Versioning | Prompt テンプレートのバージョン管理 | O | O | O | O | O | O |
| Model Versioning | モデルバージョンと設定の追跡 | O | △ | O | △ | O | △ |
| Experiment Tracking | A/B テストと実験の管理 | O | O | O | O | O | O |
| Dataset Versioning | バージョン管理された Eval および学習データセット | O | O | O | O | O | O |
| Continuous Eval | スケジュール実行またはトリガーによる Eval 実行 | O | O | O | O | O | O |
| RL/Fine-tuning Link | Fine-tuning パイプラインとの連携 | O | △ | △ | △ | △ | △ |

## DevEx / Integration

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK Support | Python, JS/TS 等の公式 SDK | O | O | O | O | O | O |
| Framework Integration | LangChain, LlamaIndex 等の組み込みサポート | O | O | O | O | O | O |
| Custom Model Support | 非標準またはセルフホストモデルの Tracing | O | O | O | O | O | O |
| API Access | プログラムアクセス用の REST または GraphQL API | O | O | O | O | O | O |
| Streaming Tracing | LLM の Streaming レスポンスの Tracing | X | O | O | O | O | O |
| CLI/Infra Integration | CLI ツールと Infrastructure-as-Code のサポート | O | O | O | O | O | O |

## Enterprise & Security

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| On-prem/VPC | セルフホストまたは VPC デプロイオプション | O | O | O | O | O | O |
| RBAC | ロールベースのアクセス制御 | △ | O | O | O | O | O |
| PII Masking | 個人情報（PII）の自動検出とマスキング | X | △ | O | △ | △ | X |
| Audit Logs | ユーザーおよびシステム操作の監査ログ | X | O | O | △ | △ | X |
| Data Retention | 設定可能なデータ保持ポリシー | X | O | O | O | △ | O |
| Region Support | マルチリージョンまたはデータレジデンシ対応 | X | O | O | △ | O | △ |