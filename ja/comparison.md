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
| Trace Depth | ネストされた関数呼び出しのTracing深度 | O | O | O | O | O | O |
| Hierarchical Spans | 親子関係を持つスパン構造 | O | O | O | O | O | O |
| Prompt Logging | LLMプロンプトの自動キャプチャ | O | O | O | O | O | O |
| Response Logging | LLMレスポンスの自動キャプチャ | O | O | O | O | O | O |
| Token Tracking | 入出力のトークン使用量カウント | O | O | O | O | O | O |
| Latency Analysis | スパンごとおよびエンドツーエンドのレイテンシ測定 | O | O | O | O | O | O |
| Replay | UI上でのステップバイステップのトレース再生 | △ | △ | O | △ | X | △ |

## Agent / RAG Observability

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Tool Call Tracing | ツール/関数呼び出しの入出力キャプチャ | O | O | O | O | O | O |
| Retrieval Tracing | リトリーバーのクエリと返されたドキュメントのロギング | O | O | O | O | O | O |
| Memory Tracing | 会話メモリーの読み書きのトラッキング | X | △ | X | X | X | X |
| Multi-step Reasoning | マルチターンAgentの推論チェーンの可視化 | O | O | O | O | O | O |
| Workflow Graph | AgentワークフローのDAGまたはグラフ表示 | X | O | O | X | X | O |
| Failure Visualization | トレース内での失敗ステップのハイライト | △ | X | O | △ | △ | △ |

## Evaluation Integration

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Trace→Dataset | 本番環境のトレースをEvalデータセットに変換 | O | O | O | O | O | △ |
| LLM-as-Judge | 組み込みLLMによるEval Scoring | O | O | O | O | O | O |
| Custom Eval Metrics | ユーザー定義の評価関数 | O | O | O | O | O | O |
| Regression Detection | 品質の劣化（リグレッション）を自動検出 | △ | O | △ | O | △ | △ |
| Model Comparison | モデル出力のサイドバイサイド比較 | O | O | O | △ | O | X |
| Human Feedback UI | 人間によるアノテーションとラベル付け用UI | O | O | O | O | O | O |

## Monitoring & Metrics

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Dashboard | リアルタイムのLLMコスト追跡Dashboard | O | O | O | O | X | O |
| Token Analytics | トークン使用量の内訳とトレンド | O | O | O | O | O | O |
| Latency Monitoring | レイテンシのパーセンタイル表示とアラート | △ | O | △ | O | △ | O |
| Error Tracking | エラー率のモニタリングとアラート | O | O | △ | O | △ | O |
| Tool Success Rate | ツール呼び出しの成功/失敗率 | △ | △ | O | O | O | △ |
| Custom Metrics | ユーザー定義のカスタムメトリクス追跡 | O | △ | O | O | O | O |

## Experiment / Improvement Loop

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Versioning | プロンプトテンプレートのバージョン管理 | O | O | O | O | O | O |
| Model Versioning | モデルバージョンと設定のトラッキング | O | △ | X | △ | O | X |
| Experiment Tracking | A/Bテストと実験の管理 | O | O | O | O | O | O |
| Dataset Versioning | Evalおよびトレーニングデータセットのバージョン管理 | O | O | O | O | O | △ |
| Continuous Eval | スケジュールまたはトリガーによる継続的Eval実行 | △ | △ | △ | O | △ | O |
| RL/Fine-tuning Link | Fine-tuningパイプラインとの連携 | O | O | △ | X | O | △ |

## DevEx / Integration

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK Support | Python, JS/TSなどの公式SDK | O | O | O | O | O | O |
| Framework Integration | LangChain, LlamaIndexなどの組み込みサポート | O | O | O | O | O | O |
| Custom Model Support | 非標準またはセルフホストモデルのTracing | O | O | O | O | O | O |
| API Access | プログラムからアクセス可能なRESTまたはGraphQL API | O | O | O | O | O | X |
| Streaming Tracing | LLMのStreamingレスポンスのTracing | O | O | O | O | X | △ |
| CLI/Infra Integration | CLIツールおよびInfrastructure-as-Codeのサポート | X | X | X | △ | X | X |

## Enterprise & Security

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| On-prem/VPC | セルフホストまたはVPCデプロイオプション | O | O | O | O | O | O |
| RBAC | ロールベースのアクセス制御 | △ | X | O | O | △ | O |
| PII Masking | 個人情報（PII）の自動検出とマスキング | O | O | O | O | O | △ |
| Audit Logs | ユーザーおよびシステムアクションの監査ログ | O | X | O | O | △ | O |
| Data Retention | 設定可能なデータ保持ポリシー | △ | O | O | O | X | O |
| Region Support | マルチリージョンまたはデータレジデンシ対応 | O | O | O | O | △ | △ |