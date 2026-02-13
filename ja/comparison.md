---
layout: default
title: LLM Observability — 詳細機能比較
---

# LLM Observability — 詳細機能比較
**日付**: 2026-02-13 | **モデル**: google/gemini-3-pro-preview

> O(強力) / △(中程度) / X(なし、または該当なし)

## Core Tracing & Logging

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| フルリクエスト/レスポンス Tracing | LLMの入力プロンプト、出力レスポンス、パラメータの完全なキャプチャ | O | O | O | O | O | O |
| ネストされた Span & ツリー表示 | 親子関係を持つツリー形式の階層的な Span Tracing 可視化 | O | O | O | O | O | O |
| Streaming サポート | ストリーミング形式の LLM レスポンスのリアルタイム Tracing | O | O | △ | △ | X | △ |
| マルチモーダル Tracing | 画像、音声、その他のテキスト以外の入出力の Tracing とレンダリング | O | △ | X | O | X | X |
| Auto-Instrumentation | 1行のコード（デコレータ、autologなど）による自動トレース収集 | O | O | O | O | O | O |
| メタデータ & タグフィルタリング | カスタムメタデータやタグの付与、およびそれらによる検索・フィルタリング | △ | O | O | O | O | O |
| トークンカウント & 推定 | トークナイザーごとの正確な入力/出力/キャッシュトークン数のカウント | O | O | O | O | O | O |
| OpenTelemetry 標準 | OTEL標準のトレースエクスポート/インポート互換性 | O | O | O | O | O | O |

## Agent & RAG Specifics

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| RAG Retrieval ビジュアライザー | 取得されたドキュメントチャンクの内容と関連性 Scoring のUI表示 | △ | O | O | △ | △ | O |
| Tool/Function Call レンダリング | Tool/Function Call の入力値と戻り値のパース済み表示 | O | O | △ | △ | X | O |
| Agent 実行グラフ | ループや分岐を含む Agent ワークフローの DAG/グラフ可視化 | △ | O | △ | X | X | △ |
| 中間ステップの状態 | Agent の中間的な思考プロセス（Chain-of-Thought）の保存と表示 | O | O | O | △ | △ | O |
| セッション/スレッド再生 | ユーザーセッションや会話スレッドを一連の流れとして再生 | △ | △ | O | X | X | O |
| 失敗ステップのハイライト | Agent トレース内での失敗したステップの自動ハイライト | O | O | O | △ | X | △ |
| MCP 統合 | Model Context Protocol サーバー/クライアントの統合と Tracing | O | O | X | X | X | X |

## Evaluation & Quality

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| LLM-as-a-Judge ウィザード | コード不要で GUI ベースの LLM Judge を作成 | O | △ | O | O | O | △ |
| カスタム Eval Scorers | ユーザー定義のコードベース評価関数の作成と実行 | O | O | O | O | O | O |
| データセット管理 & キュレーション | Eval データセットの作成、バージョニング、トレースからデータセットへの変換 | O | O | O | O | O | O |
| プロンプト最適化 / DSPy サポート | 自動プロンプト最適化や候補の提案（DSPy 統合など） | X | △ | X | △ | X | △ |
| 回帰テスト | モデルやプロンプトの変更時における自動的な品質低下（回帰）の検知 | △ | O | △ | O | O | O |
| 比較ビュー (Side-by-side) | モデルやプロンプトの出力を並べて比較 | O | O | X | O | O | O |
| アノテーションキュー | キュー管理とレビュー担当者割り当てによるチームベースのアノテーションワークフロー | △ | O | △ | △ | X | △ |
| オンライン Evaluation | 本番環境のライブトラフィックに対するリアルタイムの自動評価 | O | O | O | O | O | △ |

## Guardrails & Safety

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| PII/機密データマスキング | PII（個人情報）や機密データの自動検知とマスキング | O | △ | X | X | X | O |
| ハルシネーション検知 | ハルシネーション（事実誤認）コンテンツを検知するための専用 Guardrail | O | X | △ | O | X | O |
| トピック/ジェイルブレイク Guardrails | 禁止トピックのブロックおよびジェイルブレイク試行の検知 | O | X | △ | △ | △ | O |
| Policy Management as Code | コードとして定義・管理される Guardrail ルール | △ | X | O | O | △ | O |

## Analytics & Dashboard

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| コスト分析 & 属性付与 | ユーザー/チーム/プロジェクトごとのコスト追跡と属性付与 | O | O | O | △ | △ | X |
| トークン使用量分析 | 入出力トークン使用量の内訳とトレンド | O | O | O | O | O | O |
| レイテンシヒートマップ & P99 | パーセンタイル監視を含むレイテンシ分布の可視化 | △ | △ | O | △ | △ | △ |
| エラー率モニタリング | エラー率の追跡とアラート通知 | △ | O | △ | △ | O | △ |
| Embedding 空間の可視化 | UMAP/t-SNE による Embedding のクラスタリングと可視化 | X | X | X | X | X | X |
| カスタムメトリクス & Dashboard | Dashboard ウィジェットによるユーザー定義のカスタムメトリクス追跡 | O | O | O | O | O | O |

## Development Lifecycle

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| プロンプト管理 (CMS) | 非エンジニアによる編集・デプロイが可能なプロンプトのバージョニング | △ | △ | O | O | △ | X |
| Playground & Sandbox | インタラクティブなプロンプトとパラメータのテスト環境 | O | O | O | O | X | △ |
| 実験トラッキング | ハイパーパラメータのログ記録を含む A/B テストと実験管理 | O | O | O | O | O | O |
| Fine-tuning 統合 | Fine-tuning 用データの書き出しとパイプライン統合 | O | △ | X | △ | △ | X |
| バージョン管理 & ロールバック | ロールバック機能を備えたプロンプトとモデルのバージョン管理 | △ | △ | O | O | O | X |

## Integration & DX

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK サポート (Py/JS/Go) | Python, JavaScript/TypeScript, Go における公式 SDK サポート | △ | △ | △ | O | △ | △ |
| Gateway/Proxy モード | SDKのインストール不要なプロキシベースの Tracing（URL変更のみ） | X | X | X | X | X | X |
| 主要フレームワーク | LangChain, LlamaIndex, AutoGen, CrewAI 等の組み込みサポート | O | O | O | △ | O | O |
| API & Webhooks | 外部システム連携のための REST/GraphQL API と Webhook 統合 | △ | O | O | O | △ | O |
| CI/CD 統合 | 自動 Eval やデプロイのための CI/CD パイプライン（GitHub Actions等）との統合 | O | △ | X | △ | △ | △ |

## Enterprise & Infrastructure

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| デプロイオプション | マルチテナント SaaS、専用 SaaS、セルフホスト/VPC デプロイの選択肢 | O | O | O | △ | O | O |
| オープンソース | オープンソースコードの公開状況とコミュニティ | O | X | O | X | O | O |
| データ主権 & コンプライアンス | データリージョンの選択と SOC 2/HIPAA/GDPR への準拠 | O | O | △ | △ | △ | △ |
| RBAC & SSO | SSO/SAML 認証を含むロールベースのアクセス制御 | O | O | △ | O | △ | △ |
| 監査ログ | ユーザーおよびシステムの操作履歴（Audit Logs） | O | O | O | X | X | X |
| データウェアハウスへのエクスポート | Snowflake, BigQuery, S3 等への自動エクスポート | △ | △ | △ | X | X | X |