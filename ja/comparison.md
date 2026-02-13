---
layout: default
title: LLM Observability — 機能詳細比較
---

# LLM Observability — 機能詳細比較
**日付**: 2026-02-13 | **モデル**: google/gemini-3-pro-preview

> O(強力) / △(中程度) / X(なし、または該当なし)

## Core Tracing & Logging

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| フル Request/Response Tracing | LLMの入力プロンプト、出力レスポンス、パラメータの完全なキャプチャ | O | O | O | O | O | O |
| Nested Span & Tree View | 親子ツリー構造による階層的なスパン Tracing 可視化 | O | O | O | O | O | O |
| Streaming Support | ストリーミング形式の LLM レスポンスのリアルタイム Tracing | △ | O | O | △ | X | X |
| Multimodal Tracing | 画像、音声、その他の非テキスト入出力の Tracing とレンダリング | O | X | X | O | X | X |
| Auto-Instrumentation | 1行のコード（デコレータ、autologなど）による自動トレース収集 | O | O | O | O | O | O |
| Metadata & Tags Filtering | カスタムメタデータとタグの付与、および検索・フィルタリング | O | O | O | O | O | O |
| Token Counting & Estimation | トークナイザーごとの正確な入力/出力/キャッシュトークン数のカウント | O | O | O | O | X | △ |
| OpenTelemetry Standard | OTEL標準のトレースエクスポート/インポート互換性 | O | O | O | △ | O | O |

## Agent & RAG Specifics

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| RAG Retrieval Visualizer | 取得されたドキュメントチャンクの内容と関連性 Scoring のUI表示 | X | O | O | △ | △ | O |
| Tool/Function Call Rendering | ツール/関数呼び出しの入力と戻り値のパース済みビュー | O | O | △ | △ | X | O |
| Agent Execution Graph | ループや分岐を含むエージェントワークフローのDAG/グラフ可視化 | △ | △ | △ | X | X | △ |
| Intermediate Step State | エージェントの中間思考プロセス（Chain-of-Thought）の保存と表示 | O | O | △ | △ | △ | O |
| Session/Thread Replay | ユーザーセッションや会話スレッドを一連の流れとして再生 | O | X | △ | O | X | △ |
| Failed Step Highlighting | エージェントトレース内での失敗ステップの自動ハイライト | △ | △ | X | △ | X | △ |
| MCP Integration | Model Context Protocol サーバー/クライアントの統合と Tracing | O | △ | X | X | X | X |

## Evaluation & Quality

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| LLM-as-a-Judge Wizard | コード不要で GUI ベースの LLM Judge を構築 | O | △ | O | △ | X | O |
| Custom Eval Scorers | ユーザー定義のコードベース評価関数の作成と実行 | O | O | O | O | O | O |
| Dataset Management & Curation | Eval 用データセットの作成、バージョニング、トレースからの変換 | △ | O | O | O | O | O |
| Prompt Optimization / DSPy Support | プロンプトの自動最適化や候補の提案（DSPy 連携など） | X | △ | X | △ | X | △ |
| Regression Testing | モデルやプロンプトの変更時における品質低下の自動検出 | △ | O | △ | O | △ | O |
| Comparison View (Side-by-side) | モデルやプロンプトの出力を横並びで比較 | O | O | △ | O | O | O |
| Annotation Queues | キュー管理とレビュー担当者割り当てによるチームベースの注釈ワークフロー | △ | O | O | O | △ | △ |
| Online Evaluation | 本番環境のライブトラフィックに対するリアルタイム自動 Eval | O | O | O | O | O | X |

## Guardrails & Safety

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| PII/Sensitive Data Masking | 個人情報（PII）や機密データの自動検出とマスキング | O | △ | △ | X | △ | △ |
| Hallucination Detection | ハルシネーション（幻覚）コンテンツ検出専用のガードレール | O | X | △ | △ | X | △ |
| Topic/Jailbreak Guardrails | 禁止トピックのブロックとジェイルブレイク試行の検出 | O | △ | △ | X | △ | O |
| Policy Management as Code | コードとして定義・管理されるガードレールルール | O | △ | X | O | △ | X |

## Analytics & Dashboard

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Cost Analysis & Attribution | ユーザー/チーム/プロジェクトごとのコスト追跡と割り当て | O | O | O | △ | X | X |
| Token Usage Analytics | 入出力トークン使用量の内訳とトレンド分析 | O | O | O | O | O | O |
| Latency Heatmap & P99 | パーセンタイル監視を含むレイテンシ分布の可視化 | △ | O | O | △ | △ | △ |
| Error Rate Monitoring | エラー率の追跡とアラート通知 | △ | O | △ | △ | O | △ |
| Embedding Space Visualization | UMAP/t-SNE による埋め込みベクトルのクラスタリングと可視化 | X | X | X | X | X | X |
| Custom Metrics & Dashboard | Dashboard ウィジェットによるユーザー定義カスタムメトリクスの追跡 | O | O | O | O | O | O |

## Development Lifecycle

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Prompt Management (CMS) | 非エンジニアでも編集・デプロイ可能なプロンプトのバージョニング | △ | O | O | O | △ | X |
| Playground & Sandbox | インタラクティブなプロンプトとパラメータのテスト環境 | O | O | O | O | X | △ |
| Experiment Tracking | ハイパーパラメータのログ記録を含む A/B テストと実験管理 | O | O | O | O | O | O |
| Fine-tuning Integration | Fine-tuning 用データの書き出しとパイプライン連携 | △ | △ | X | △ | △ | △ |
| Version Control & Rollback | ロールバック機能を備えたプロンプトとモデルのバージョン管理 | △ | O | O | O | O | X |

## Integration & DX

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK Support (Py/JS/Go) | Python、JavaScript/TypeScript、Go の公式 SDK サポート | O | △ | △ | O | △ | △ |
| Gateway/Proxy Mode | SDK 導入不要、URL 変更のみで利用可能なプロキシベースの Tracing | X | X | X | X | X | X |
| Popular Frameworks | LangChain、LlamaIndex、AutoGen、CrewAI 等の組み込みサポート | O | O | O | △ | △ | O |
| API & Webhooks | 外部システム連携のための REST/GraphQL API と Webhook | △ | O | O | △ | △ | △ |
| CI/CD Integration | 自動 Eval とデプロイのための CI/CD パイプライン（GitHub Actions等）連携 | △ | △ | X | X | X | X |

## Enterprise & Infrastructure

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| Deployment Options | マルチテナント SaaS、専用 SaaS、セルフホスト/VPC デプロイの選択肢 | O | O | O | △ | O | O |
| Open Source | オープンソースコードの公開状況とコミュニティ | O | X | O | X | O | O |
| Data Sovereignty & Compliance | データリージョン選択と SOC 2/HIPAA/GDPR コンプライアンス | O | △ | △ | △ | X | △ |
| RBAC & SSO | SSO/SAML 認証を含むロールベースのアクセス制御 | O | O | O | O | △ | △ |
| Audit Logs | ユーザーおよびシステム操作の監査ログ | O | △ | O | X | X | X |
| Data Warehouse Export | Snowflake、BigQuery、S3 等への自動エクスポート | △ | O | O | X | △ | X |