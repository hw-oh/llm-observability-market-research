---
layout: default
title: LLM Observability — 機能詳細比較
---

# LLM Observability — 機能詳細比較
**日付**: 2026-02-12 | **モデル**: google/gemini-3-pro-preview

> O(強力) / △(中程度) / X(なし、または該当なし)

## Core Tracing & Logging

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Nested Span Tracing | 親子関係を持つネストされた関数/LLMコールのSpan Tracing | O | O | O | O | O | O |
| Auto-Instrumentation | 1行のコードによる自動トレース収集（デコレータ、autologなど） | O | O | O | O | O | O |
| Prompt & Response Logging | LLMの入力Promptと出力Responseの自動キャプチャ | O | O | O | O | O | O |
| Token Usage Tracking | 入力/出力/キャッシュ/Reasoningトークンの使用量追跡 | O | O | O | O | O | O |
| Latency Measurement | Span単位およびエンドツーエンドのレイテンシ測定 | O | O | O | O | O | O |
| Cost Estimation | トークン使用量に基づく自動コスト推定 | △ | X | O | O | X | O |
| Streaming Trace | ストリーミングLLMレスポンスのリアルタイムTracing | △ | O | △ | △ | △ | △ |
| Metadata & Tags | トレースへのカスタムメタデータおよびタグの付与 | △ | O | O | O | O | O |
| OpenTelemetry Compatibility | OTEL標準のトレースエクスポート/インポート対応 | O | O | O | O | O | O |

## Agent & RAG Observability

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Tool/Function Call Tracing | エージェントのツール呼び出し入力・出力の自動Tracing | O | O | O | O | O | O |
| Retrieval (RAG) Tracing | リトリーバーのクエリと返されたドキュメントのLogging | O | O | O | O | △ | O |
| Multi-step Reasoning Trace | マルチターン・エージェントのReasoningチェーンの可視化 | O | O | O | O | O | O |
| Workflow Graph View | エージェントワークフローのDAG/グラフ可視化 | O | △ | O | △ | X | △ |
| MCP/A2A Protocol Tracing | Model Context ProtocolおよびAgent2Agentプロトコルのトレース対応 | △ | X | X | X | X | △ |
| Failed Step Highlighting | トレース内の失敗したステップの自動ハイライト | △ | O | △ | △ | O | △ |
| Session/Conversation Grouping | セッションまたは会話ごとのトレースのグルーピング | △ | O | O | O | △ | O |

## Evaluation & Quality

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| LLM-as-Judge | 組み込みLLMによる自動Eval Scoring | O | O | O | O | O | O |
| Custom Eval Scorers | ユーザー定義の評価関数の作成と実行 | O | O | O | O | O | O |
| Human Feedback / Annotation UI | UIベースの人間による評価、アノテーション、ラベリング | △ | O | O | O | O | O |
| Evaluation Dataset Management | 評価用データセットの作成、バージョニング、保存 | O | O | O | O | O | △ |
| Trace → Eval Dataset | 本番環境のトレースから評価用データセットへの直接変換 | O | O | △ | O | O | △ |
| Regression Detection | モデル/Prompt変更時の自動品質劣化（Regression）検知 | △ | O | O | O | △ | △ |
| Side-by-side Model Comparison | モデル/Prompt出力の横並び比較 | O | △ | O | O | O | O |
| Evaluation Leaderboard | 複数のモデル/Prompt評価結果のランキング表示 | O | △ | △ | △ | △ | X |
| CI/CD Eval Integration | CI/CDパイプライン（GitHub Actions等）へのEval組み込み | X | O | △ | O | △ | X |
| Online Evaluation (Monitors) | 本番トレースに対するリアルタイム自動Eval | △ | O | O | O | O | O |

## Guardrails & Safety

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Built-in Guardrails | 組み込みガードレール（有害性、PII、ハルシネーション等） | O | △ | X | X | X | △ |
| Custom Guardrails | ユーザー定義のガードレールScorer作成 | O | O | △ | △ | △ | O |
| Pre/Post Response Hooks | LLMレスポンス前後のセーフティチェック用フック | O | △ | O | △ | △ | O |
| PII Detection & Masking | 自動PII（個人情報）検知およびマスキング | △ | △ | △ | X | X | △ |

## Monitoring & Analytics

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Dashboard | リアルタイムLLMコスト追跡Dashboard | O | O | O | O | X | X |
| Token Usage Analytics | トークン使用量の内訳とトレンド分析 | O | O | O | O | O | O |
| Latency Percentiles & Alerting | レイテンシのパーセンタイル監視とアラート | O | O | △ | △ | △ | O |
| Error Rate Monitoring | エラー率の監視とアラート | O | O | △ | △ | △ | △ |
| Custom Metrics | ユーザー定義のカスタムメトリクス追跡 | △ | O | O | O | O | △ |
| Drift Detection | モデル入出力分布のドリフト検知 | X | X | X | △ | X | O |
| Embedding Clustering/Analysis | Embedding空間のクラスタリングと可視化分析 | X | △ | X | X | X | △ |

## Experiment & Improvement Loop

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Versioning | Promptテンプレートのバージョン管理 | △ | O | O | O | O | O |
| Model Versioning | モデルバージョンと設定の追跡 | O | O | △ | △ | O | △ |
| Experiment Tracking | A/Bテストおよび実験管理 | O | O | O | O | O | O |
| Dataset Versioning | バージョン管理された評価・学習用データセット | X | △ | X | O | O | O |
| LLM Playground | インタラクティブなPromptテストインターフェース | O | O | O | O | X | △ |
| Continuous/Scheduled Eval | 定期実行またはトリガーベースの自動Eval実行 | △ | △ | X | △ | △ | △ |
| RL/Fine-tuning Pipeline | Fine-tuning/RLパイプラインとの連携 | O | X | △ | △ | X | △ |
| Training Data Generation | トレースからの学習データ自動生成 | △ | O | △ | O | △ | △ |
| Failure Trajectory Extraction | 失敗パターンのトレースをデータセットとして抽出 | O | O | O | O | △ | O |

## Developer Experience & Integration

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Python SDK | 公式Python SDK | O | O | O | O | O | O |
| TypeScript/JS SDK | 公式TypeScript/JavaScript SDK | O | O | O | O | O | △ |
| Framework Integration | LangChain, LlamaIndex, DSPy, CrewAI等の組み込みサポート | O | O | △ | X | O | △ |
| REST/GraphQL API | プログラムアクセス用のRESTまたはGraphQL API | △ | O | O | X | O | O |
| Custom Model Support | 非標準またはセルフホストモデルのTracing | O | △ | O | O | O | △ |
| CLI Tools | コマンドラインインターフェースツール | X | O | X | X | O | X |
| Notebook Integration | Jupyter/Colabノートブック内でのトレース可視化 | △ | X | X | X | △ | △ |

## Infrastructure & Enterprise

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cloud Managed (SaaS) | マネージドクラウドサービスの提供 | O | O | O | O | O | O |
| Self-Host / On-Prem | セルフホストまたはオンプレミスへのデプロイオプション | O | O | O | △ | O | O |
| VPC Deployment | 顧客のVPC内へのデプロイ | O | △ | O | X | △ | O |
| Open Source | オープンソースコードの公開 | △ | X | O | X | O | O |
| RBAC | ロールベースのアクセス制御 | O | X | O | O | △ | X |
| SSO/SAML | SSOおよびSAML認証対応 | O | X | △ | O | X | △ |
| SOC 2 Certification | SOC 2 Type II セキュリティ認証 | O | X | △ | O | X | X |
| Audit Logs | ユーザーおよびシステムの操作ログ（監査ログ） | O | X | O | △ | △ | X |
| Data Retention Policy | 設定可能なデータ保持ポリシー | O | X | O | △ | X | X |
| Data Warehouse Export | 外部データウェアハウスへのエクスポート | O | X | O | X | △ | △ |
| Multi-Region / Data Residency | マルチリージョンまたはデータレジデンシ対応 | O | O | △ | △ | △ | △ |
| Traditional ML Experiment Integration | 従来のML実験追跡（W&B, MLflow等）との統合 | O | X | X | X | O | X |
| Databricks Native Integration | Databricksプラットフォームとのネイティブ統合 | X | X | X | X | O | X |