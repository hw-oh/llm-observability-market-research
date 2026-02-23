---
layout: default
title: LLM Observability — 機能詳細比較
---

# LLM Observability — 機能詳細比較
**日付**: 2026-02-23 | **モデル**: google/gemini-3-pro-preview

> O(強力) / △(中程度) / X(なし、または該当なし)

## Core Tracing & Logging

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Full Request/Response Tracing | LLMの入力プロンプト、出力レスポンス、パラメータの完全なキャプチャ | O | O | O | O | O | O |
| Nested Span & Tree View | 親子ツリー構造による階層的なスパンTracingの可視化 | O | O | O | O | O | O |
| Streaming Support | ストリーミング形式のLLMレスポンスのリアルタイムTracing | △ | O | O | △ | X | △ |
| Multimodal Tracing | 画像、音声、その他の非テキスト入出力のTracingとレンダリング | O | X | X | O | X | △ |
| Auto-Instrumentation | 1行のコード（デコレータ、autologなど）による自動トレース収集 | O | O | O | O | O | O |
| Metadata & Tags Filtering | カスタムメタデータやタグの付与、およびそれらによる検索・フィルタリング | O | O | O | O | O | O |
| Token Counting & Estimation | トークナイザーごとの正確な入力/出力/キャッシュトークン数のカウント | △ | O | O | O | △ | O |
| OpenTelemetry Standard | OTEL標準のトレースエクスポート/インポート互換性 | O | O | O | △ | O | O |

## Agent & RAG Specifics

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| RAG Retrieval Visualizer | 取得されたドキュメントチャンクの内容と関連性ScoringのUI表示 | △ | O | O | △ | △ | O |
| Tool/Function Call Rendering | ツール/関数呼び出しの入力と戻り値のパース済みビュー | O | O | △ | O | △ | O |
| Agent Execution Graph | ループや分岐を含むエージェントワークフローのDAG/グラフ可視化 | O | O | X | X | X | O |
| Intermediate Step State | エージェントの中間思考プロセス（Chain-of-Thought）の保存と表示 | O | O | O | △ | △ | O |
| Session/Thread Replay | ユーザーセッションや会話スレッドを一連の流れとして再生 | △ | O | O | △ | X | O |
| Failed Step Highlighting | エージェントトレース内の失敗したステップの自動ハイライト | O | O | △ | O | X | △ |
| MCP Integration | Model Context Protocol サーバー/クライアントの統合とTracing | O | X | X | △ | X | X |

## Evaluation & Quality

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| LLM-as-a-Judge Wizard | コード不要でGUIベースのLLM Judgeを構築 | O | O | O | △ | X | △ |
| Custom Eval Scorers | ユーザー定義のコードベース評価関数の作成と実行 | O | O | O | O | O | O |
| Dataset Management & Curation | Eval用データセットの作成、バージョニング、トレースからのデータセット変換 | O | O | △ | O | O | O |
| Prompt Optimization / DSPy Support | プロンプトの自動最適化または候補の提案（DSPy連携など） | X | △ | X | X | X | △ |
| Regression Testing | モデルやプロンプトの変更時における品質低下（リグレッション）の自動検知 | △ | O | O | O | O | O |
| Comparison View (Side-by-side) | モデルやプロンプトの出力を横並びで比較 | O | O | △ | O | △ | O |
| Annotation Queues | キュー管理とレビュー担当者割り当てによるチームベースのアノテーションワークフロー | X | O | △ | X | X | X |
| Online Evaluation | 本番環境のライブトラフィックに対するリアルタイムの自動Eval | O | O | O | △ | O | O |

## Guardrails & Safety

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| PII/Sensitive Data Masking | PII（個人情報）や機密データの自動検知とマスキング | O | X | X | X | △ | △ |
| Hallucination Detection | ハルシネーション（幻覚）検知専用のガードレール | O | X | △ | △ | X | X |
| Topic/Jailbreak Guardrails | 禁止トピックのブロックおよびジェイルブレイク試行の検知 | △ | X | △ | X | X | O |
| Policy Management as Code | コードとして定義・管理されるガードレールルール | O | X | O | △ | X | O |

## Analytics & Dashboard

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Analysis & Attribution | ユーザー/チーム/プロジェクトごとのコスト追跡と割り当て | O | △ | O | △ | △ | X |
| Token Usage Analytics | 入出力トークン使用量の内訳とトレンド分析 | O | O | O | O | O | O |
| Latency Heatmap & P99 | パーセンタイル監視を含むレイテンシ分布の可視化 | △ | O | △ | △ | △ | △ |
| Error Rate Monitoring | エラー率の追跡とアラート通知 | △ | O | △ | O | O | △ |
| Embedding Space Visualization | UMAP/t-SNEによる埋め込みベクトルのクラスタリングと可視化 | X | X | X | X | X | X |
| Custom Metrics & Dashboard | ダッシュボードウィジェットによるユーザー定義のカスタムメトリクス追跡 | O | O | O | O | O | O |

## Development Lifecycle

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Management (CMS) | 非エンジニアでも編集・デプロイ可能なプロンプトのバージョニング | △ | O | O | O | △ | △ |
| Playground & Sandbox | インタラクティブなプロンプトとパラメータのテスト環境 | O | O | O | O | △ | △ |
| Experiment Tracking | ハイパーパラメータのログ記録を含むA/Bテストと実験管理 | O | O | O | O | O | O |
| Fine-tuning Integration | Fine-tuning用データの書き出しとパイプライン連携 | △ | △ | X | X | △ | △ |
| Version Control & Rollback | ロールバック機能を備えたプロンプトとモデルのバージョン管理 | △ | O | O | △ | O | △ |

## Integration & DX

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK Support (Py/JS/Go) | Python、JavaScript/TypeScript、Goにおける公式SDKサポート | △ | O | △ | O | O | △ |
| Gateway/Proxy Mode | SDKのインストール不要、URL変更のみで利用可能なプロキシベースのTracing | X | X | X | X | X | O |
| Popular Frameworks | LangChain、LlamaIndex、AutoGen、CrewAIなどの組み込みサポート | O | △ | O | △ | O | O |
| API & Webhooks | 外部システム連携のためのREST/GraphQL APIおよびWebhook | △ | O | O | O | △ | O |
| CI/CD Integration | 自動EvalとデプロイのためのCI/CDパイプライン（GitHub Actionsなど）との連携 | △ | △ | X | △ | X | △ |

## Enterprise & Infrastructure

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Deployment Options | マルチテナントSaaS、専用SaaS、セルフホスト/VPCデプロイの選択肢 | O | O | O | O | O | O |
| Open Source | オープンソースコードの公開とコミュニティの有無 | X | X | O | X | O | O |
| Data Sovereignty & Compliance | データリージョン選択とSOC 2/HIPAA/GDPRコンプライアンス | O | O | O | O | △ | △ |
| RBAC & SSO | SSO/SAML認証を含むロールベースのアクセス制御 | O | △ | △ | O | △ | X |
| Audit Logs | ユーザーおよびシステムの操作履歴（監査ログ） | O | O | △ | X | △ | X |
| Data Warehouse Export | Snowflake、BigQuery、S3などへの自動エクスポート | △ | O | O | X | X | △ |