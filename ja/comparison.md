---
layout: default
title: LLM Observability — 詳細機能比較
---

# LLM Observability — 詳細機能比較
**日付**: 2026-02-12 | **モデル**: google/gemini-3-pro-preview

> O(強力) / △(中程度) / X(なし、または該当なし)

## Core Tracing & Logging

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Nested Span Tracing | 親子関係を持つネストされた関数/LLMコールのSpan Tracing | O | O | O | O | O | O |
| Auto-Instrumentation | 1行のコードによる自動トレース収集（デコレータ、autologなど） | O | O | O | O | O | O |
| Prompt & Response Logging | LLMの入力Promptと出力Responseの自動キャプチャ | O | O | O | O | O | O |
| Token Usage Tracking | 入力/出力/キャッシュ/推論トークン使用量のトラッキング | O | O | O | O | O | O |
| Latency Measurement | Span単位およびエンドツーエンドのレイテンシ計測 | O | O | O | O | O | O |
| Cost Estimation | トークン使用量に基づく自動コスト推定 | O | O | X | O | X | O |
| Streaming Trace | ストリーミングLLMレスポンスのリアルタイムTracing | △ | O | △ | △ | △ | △ |
| Metadata & Tags | トレースへのカスタムMetadataおよびタグの付与 | O | O | O | O | O | O |
| OpenTelemetry Compatibility | OTEL標準のトレースエクスポート/インポート対応 | O | O | O | O | O | O |

## Agent & RAG Observability

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Tool/Function Call Tracing | エージェントのツールコールの入出力の自動Tracing | O | O | O | O | O | O |
| Retrieval (RAG) Tracing | リトリーバーのクエリと返されたドキュメントのロギング | O | O | O | O | △ | O |
| Multi-step Reasoning Trace | マルチターン・エージェントの推論チェーンの可視化 | O | O | O | O | O | O |
| Workflow Graph View | エージェントワークフローのDAG/グラフ可視化 | O | △ | O | △ | X | △ |
| MCP/A2A Protocol Tracing | Model Context ProtocolおよびAgent2Agentプロトコルのトレース対応 | △ | X | X | X | X | △ |
| Failed Step Highlighting | トレース内の失敗したステップの自動ハイライト | △ | O | △ | △ | O | △ |
| Session/Conversation Grouping | セッションまたは会話ごとのトレースのグルーピング | △ | O | O | O | △ | O |

## Evaluation & Quality

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| LLM-as-Judge | 組み込みLLMによる自動Eval Scoring | O | O | O | O | O | O |
| Custom Eval Scorers | ユーザー定義の評価関数の作成と実行 | O | O | O | O | O | O |
| Human Feedback / Annotation UI | UIベースの人間による評価、アノテーション、ラベリング | X | O | O | O | O | △ |
| Evaluation Dataset Management | 評価用データセットの作成、バージョニング、保存 | O | O | O | O | O | O |
| Trace → Eval Dataset | 本番環境のトレースから評価用データセットへの直接変換 | △ | O | △ | O | O | △ |
| Regression Detection | モデル/Prompt変更時の自動的な品質劣化（リグレッション）検知 | △ | O | O | O | △ | △ |
| Side-by-side Model Comparison | モデル/Prompt出力の横並び比較 | O | O | O | O | O | O |
| Evaluation Leaderboard | 複数のモデル/Prompt評価結果のランキング表示 | O | △ | △ | △ | △ | X |
| CI/CD Eval Integration | CI/CDパイプライン（GitHub Actions等）へのEvalの組み込み | X | △ | △ | O | △ | X |
| Online Evaluation (Monitors) | 本番環境のトレースに対するリアルタイム自動評価 | △ | O | O | O | O | △ |

## Guardrails & Safety

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Built-in Guardrails | 組み込みガードレール（有害性、PII、ハルシネーション等） | O | △ | X | △ | X | X |
| Custom Guardrails | ユーザー定義のガードレールScorerの作成 | O | O | O | O | △ | △ |
| Pre/Post Response Hooks | LLMレスポンス前後のセーフティチェック用フック | O | △ | △ | O | △ | △ |
| PII Detection & Masking | 自動PII検知およびマスキング | △ | △ | X | X | X | △ |

## Monitoring & Analytics

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Dashboard | リアルタイムLLMコストトラッキングDashboard | O | O | O | O | O | X |
| Token Usage Analytics | トークン使用量の内訳とトレンド分析 | O | O | O | O | O | O |
| Latency Percentiles & Alerting | レイテンシのパーセンタイル監視とアラート | △ | △ | △ | △ | △ | O |
| Error Rate Monitoring | エラー率の監視とアラート | X | O | O | O | O | △ |
| Custom Metrics | ユーザー定義のカスタムメトリクスのトラッキング | O | △ | O | O | O | O |
| Drift Detection | モデル入出力の分布ドリフト検知 | X | X | X | X | X | O |
| Embedding Clustering/Analysis | Embedding空間のクラスタリングと可視化分析 | X | △ | X | X | X | O |

## Experiment & Improvement Loop

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Versioning | Promptテンプレートのバージョン管理 | O | O | O | O | O | O |
| Model Versioning | モデルバージョンと設定のトラッキング | △ | O | △ | △ | O | △ |
| Experiment Tracking | A/Bテストおよび実験管理 | O | O | O | O | O | O |
| Dataset Versioning | バージョン管理された評価用および学習用データセット | O | △ | X | O | △ | △ |
| LLM Playground | インタラクティブなPromptテストインターフェース | O | O | O | O | X | △ |
| Continuous/Scheduled Eval | 定期実行またはトリガーベースの自動Eval実行 | △ | O | X | △ | △ | X |
| RL/Fine-tuning Pipeline | Fine-tuning/RLパイプラインとの統合 | △ | X | X | △ | O | X |
| Training Data Generation | トレースからの自動学習データ生成 | X | O | △ | O | O | △ |
| Failure Trajectory Extraction | 失敗パターンのトレースをデータセットとして抽出 | O | O | △ | O | O | O |

## Developer Experience & Integration

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Python SDK | 公式Python SDK | O | O | O | O | O | O |
| TypeScript/JS SDK | 公式TypeScript/JavaScript SDK | O | O | O | O | O | △ |
| Framework Integration | LangChain, LlamaIndex, DSPy, CrewAI等の組み込みサポート | △ | O | O | O | O | O |
| REST/GraphQL API | プログラムアクセス用のRESTまたはGraphQL API | X | O | O | X | O | O |
| Custom Model Support | 非標準またはセルフホストモデルのTracing | O | O | O | O | △ | O |
| CLI Tools | コマンドラインインターフェースツール | X | △ | X | O | O | X |
| Notebook Integration | Jupyter/Colabノートブック内でのトレース可視化 | X | O | △ | X | △ | △ |

## Infrastructure & Enterprise

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cloud Managed (SaaS) | マネージドクラウドサービスの提供 | O | O | O | O | △ | △ |
| Self-Host / On-Prem | セルフホストまたはオンプレミスへのデプロイオプション | O | O | O | O | O | O |
| VPC Deployment | 顧客VPC内へのデプロイ | △ | △ | △ | △ | O | O |
| Open Source | オープンソースコードの公開 | O | X | O | X | O | O |
| RBAC | ロールベースのアクセス制御 | X | O | O | O | X | X |
| SSO/SAML | SSOおよびSAML認証のサポート | O | △ | △ | O | X | △ |
| SOC 2 Certification | SOC 2 Type II セキュリティ認証 | O | X | X | O | X | X |
| Audit Logs | ユーザーおよびシステムアクションの監査ログ | O | O | O | △ | △ | O |
| Data Retention Policy | 設定可能なデータ保持ポリシー | △ | X | O | △ | X | O |
| Data Warehouse Export | 外部データウェアハウスへのエクスポート | O | X | O | X | △ | X |
| Multi-Region / Data Residency | マルチリージョンまたはデータレジデンシ対応 | O | O | O | △ | △ | △ |
| Traditional ML Experiment Integration | 従来のML実験トラッキング（W&B, MLflow等）との統合 | O | X | X | X | O | X |
| Databricks Native Integration | Databricksプラットフォームとのネイティブ統合 | X | X | X | X | O | △ |