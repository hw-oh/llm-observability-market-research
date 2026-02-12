---
layout: default
title: LLM Observability — 機能詳細比較
---

# LLM Observability — 機能詳細比較
**日付**: 2026-02-12 | **モデル**: google/gemini-3-pro-preview

> O(強力) / △(中程度) / X(なし、または該当なし)

## Core Observability

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace Depth | ネストされた関数呼び出しの Tracing 深度 | O | O | O | O | O | O |
| Hierarchical Spans | 親子関係を持つ Span の構造化 | O | O | O | O | O | O |
| Prompt Logging | LLM Prompt の自動キャプチャ | O | O | O | O | O | O |
| Response Logging | LLM レスポンスの自動キャプチャ | O | O | O | O | O | O |
| Token Tracking | 入出力の Token 使用量のカウント | O | O | O | O | O | O |
| Latency Analysis | Span ごとおよびエンドツーエンドの Latency 測定 | O | O | O | O | O | O |
| Replay | UI 上でのステップバイステップの Trace 再生 | △ | △ | O | X | X | △ |

## Agent / RAG Observability

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Tool Call Tracing | ツール/関数呼び出しの入出力キャプチャ | O | O | O | O | O | O |
| Retrieval Tracing | リトリーバーのクエリと返されたドキュメントの Logging | O | O | O | O | O | O |
| Memory Tracing | 会話メモリーの読み書きのトラッキング | X | X | X | X | X | X |
| Multi-step Reasoning | マルチターンなエージェントの推論チェーンの可視化 | O | O | O | O | O | O |
| Workflow Graph | エージェントワークフローの DAG またはグラフ表示 | X | △ | O | X | X | O |
| Failure Visualization | Trace 内の失敗したステップのハイライト表示 | △ | X | O | △ | X | △ |

## Evaluation Integration

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace→Dataset | 本番環境の Trace を Eval データセットに変換 | O | O | O | O | O | O |
| LLM-as-Judge | 組み込みの LLM ベースの Eval Scoring | O | O | O | O | O | O |
| Custom Eval Metrics | ユーザー定義の Eval 関数 | O | O | O | O | O | O |
| Regression Detection | 品質の低下（リグレッション）の自動検知 | △ | O | △ | O | X | △ |
| Model Comparison | モデル出力のサイドバイサイド比較 | O | O | O | △ | O | X |
| Human Feedback UI | 人間によるアノテーションとラベリング用 UI | O | O | O | O | O | O |

## Monitoring & Metrics

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Dashboard | リアルタイムの LLM コスト追跡 Dashboard | O | O | O | O | X | O |
| Token Analytics | Token 使用量の内訳とトレンド分析 | O | O | O | O | O | O |
| Latency Monitoring | Latency のパーセンタイル表示とアラート | △ | O | O | O | O | O |
| Error Tracking | エラー率の監視とアラート | O | O | △ | O | O | O |
| Tool Success Rate | ツール呼び出しの成功/失敗率 | △ | X | O | △ | O | O |
| Custom Metrics | ユーザー定義のカスタムメトリクス追跡 | O | △ | O | O | O | O |

## Experiment / Improvement Loop

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Versioning | Prompt テンプレートのバージョン管理 | O | O | O | O | O | O |
| Model Versioning | モデルのバージョンと設定のトラッキング | O | △ | △ | △ | O | X |
| Experiment Tracking | A/B テストと実験の管理 | O | O | O | O | O | O |
| Dataset Versioning | バージョン管理された Eval および学習データセット | O | O | O | O | O | △ |
| Continuous Eval | スケジュール実行またはトリガーによる Eval 実行 | △ | △ | △ | O | △ | O |
| RL/Fine-tuning Link | Fine-tuning パイプラインとの連携 | O | O | △ | X | O | △ |

## DevEx / Integration

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK Support | Python, JS/TS などの公式 SDK | O | O | O | O | O | O |
| Framework Integration | LangChain, LlamaIndex などの組み込みサポート | O | O | O | O | O | O |
| Custom Model Support | 非標準またはセルフホストモデルの Tracing | O | O | O | O | O | O |
| API Access | プログラムからアクセスするための REST または GraphQL API | O | O | O | O | O | X |
| Streaming Tracing | LLM の Streaming レスポンスの Tracing | O | X | △ | O | X | X |
| CLI/Infra Integration | CLI ツールと Infrastructure-as-Code のサポート | △ | X | X | △ | X | X |

## Security & Governance

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| On-prem/VPC | セルフホストまたは VPC デプロイオプション | O | O | O | O | O | O |
| RBAC | ロールベースのアクセス制御 | O | X | O | O | △ | O |
| PII Masking | 個人情報（PII）の自動検知とマスキング | O | △ | O | O | O | △ |
| Audit Logs | ユーザーおよびシステムアクションの監査ログ | O | X | O | O | △ | O |
| Data Retention | 設定可能なデータ保持ポリシー | △ | O | O | △ | X | O |
| Region Support | マルチリージョンまたはデータレジデンシのサポート | O | O | O | O | △ | X |