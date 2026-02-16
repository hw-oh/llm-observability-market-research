---
layout: default
title: LLM Observability — 詳細機能比較
---

# LLM Observability — 詳細機能比較
**日付**: 2026-02-16 | **モデル**: google/gemini-3-pro-preview

> O(強力) / △(中程度) / X(なし、または該当なし)

## Core Tracing & Logging

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| フル Request/Response Tracing | LLMの入力プロンプト、出力レスポンス、パラメータの完全なキャプチャ | O | O | O | O | O | O |
| ネストされた Span & ツリー表示 | 親子ツリー視覚化による階層的な Span Tracing | O | O | O | O | O | O |
| Streaming サポート | ストリーミング LLM レスポンスのリアルタイム Tracing | △ | O | O | △ | △ | △ |
| マルチモーダル Tracing | 画像、音声、その他の非テキスト入力/出力の Tracing とレンダリング | O | X | X | O | X | △ |
| Auto-Instrumentation | 1行のコードによる自動トレース収集（デコレータ、autologなど） | O | O | O | O | O | O |
| メタデータ & タグフィルタリング | カスタムメタデータとタグの付与、および検索・フィルタリング | O | O | O | O | O | O |
| Token カウント & 推定 | トキナイザーごとの正確な入力/出力/キャッシュ済み Token カウント | O | O | O | O | △ | △ |
| OpenTelemetry 標準 | OTEL標準のトレースエクスポート/インポート互換性 | O | O | O | O | O | O |

## Agent & RAG Specifics

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| RAG Retrieval ビジュアライザー | 取得されたドキュメントチャンクの内容と関連性スコアのUI表示 | △ | O | O | △ | △ | O |
| Tool/Function Call レンダリング | Tool/Function Call の入力と戻り値のパース済み表示 | O | O | △ | O | △ | O |
| Agent 実行グラフ | ループや分岐を含む Agent ワークフローの DAG/グラフ視覚化 | △ | O | X | X | X | △ |
| 中間ステップの状態 | Agent の中間的な推論プロセス（Chain-of-Thought）の保存と表示 | O | O | O | △ | O | O |
| セッション/スレッド再生 | ユーザーセッションや会話スレッドを完全なフローとして再生 | O | △ | O | X | △ | △ |
| 失敗ステップのハイライト | Agent トレース内での失敗したステップの自動ハイライト | △ | O | △ | △ | O | △ |
| MCP 統合 | Model Context Protocol サーバー/クライアントの統合と Tracing | O | △ | X | X | X | X |

## Evaluation & Quality

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| LLM-as-a-Judge ウィザード | コード不要の GUI ベース LLM Judge ビルダー | O | △ | O | O | O | X |
| カスタム Eval Scorers | ユーザー定義のコードベース評価関数の作成と実行 | O | O | O | O | O | O |
| データセット管理 & キュレーション | Eval データセットの作成、バージョニング、トレースからデータセットへの変換 | O | O | O | O | O | △ |
| プロンプト最適化 / DSPy サポート | 自動プロンプト最適化または候補の提案（例：DSPy 統合） | X | △ | X | △ | X | △ |
| 回帰テスト | モデル/プロンプト変更時の自動的な品質低下（回帰）検知 | O | O | △ | O | △ | △ |
| 比較ビュー (Side-by-side) | モデル/プロンプト出力の横並び比較 | O | O | △ | O | O | O |
| アノテーションキュー | キュー管理とレビュー担当者割り当てによるチームベースのアノテーションワークフロー | △ | O | O | △ | O | X |
| オンライン Evaluation | 本番環境のライブトラフィックに対するリアルタイム自動評価 | O | O | O | O | O | X |

## Guardrails & Safety

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| PII/機密データマスキング | PII（個人情報）および機密データの自動検知とマスキング | O | △ | O | △ | △ | △ |
| ハルシネーション検知 | ハルシネーション（幻覚）コンテンツを検知するための専用 Guardrail | O | X | O | △ | X | △ |
| トピック/ジェイルブレイク Guardrails | 禁止トピックのブロックおよびジェイルブレイク試行の検知 | O | △ | O | X | △ | O |
| Policy Management as Code | コードとして定義・管理される Guardrail ルール | O | X | △ | X | X | △ |

## Analytics & Dashboard

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| コスト分析 & 属性特定 | ユーザー/チーム/プロジェクトごとのコスト追跡と属性特定 | O | △ | O | △ | △ | X |
| Token 使用量分析 | 入力/出力 Token 使用量の内訳とトレンド | O | O | △ | O | O | O |
| レイテンシヒートマップ & P99 | パーセンタイル監視を伴うレイテンシ分布の視覚化 | △ | O | O | △ | △ | △ |
| エラー率モニタリング | エラー率の追跡とアラート通知 | △ | O | △ | △ | O | O |
| Embedding 空間の視覚化 | UMAP/t-SNE による Embedding のクラスタリングと視覚化 | X | X | X | X | X | X |
| カスタムメトリクス & Dashboard | ユーザー定義のカスタムメトリクス追跡と Dashboard ウィジェット | O | O | O | O | O | O |

## Development Lifecycle

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| プロンプト管理 (CMS) | 非エンジニアによる編集・デプロイが可能なプロンプトバージョニング | △ | O | O | O | O | △ |
| Playground & サンドボックス | インタラクティブなプロンプトおよびパラメータのテスト環境 | O | △ | O | O | X | △ |
| 実験トラッキング | ハイパーパラメータのロギングを伴う A/B テストと実験管理 | O | O | O | O | O | O |
| Fine-tuning 統合 | Fine-tuning 用データの出力とパイプライン統合 | △ | △ | X | △ | △ | X |
| バージョン管理 & ロールバック | ロールバック機能を備えたプロンプトとモデルのバージョン管理 | O | O | △ | O | O | X |

## Integration & DX

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK サポート (Py/JS/Go) | Python、JavaScript/TypeScript、Go における公式 SDK サポート | O | △ | △ | O | △ | △ |
| Gateway/Proxy モード | SDK インストール不要のプロキシベース Tracing（URL変更のみ） | X | X | X | X | O | O |
| 主要フレームワーク | LangChain, LlamaIndex, AutoGen, CrewAI 等の組み込みサポート | O | O | O | △ | △ | O |
| API & Webhooks | 外部システム連携のための REST/GraphQL API と Webhook 統合 | O | O | O | △ | O | O |
| CI/CD 統合 | 自動 Eval とデプロイのための CI/CD パイプライン（GitHub Actions等）連携 | △ | △ | X | O | △ | △ |

## Enterprise & Infrastructure

| 機能 | 説明 | W&B Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| デプロイオプション | マルチテナント SaaS、専用 SaaS、セルフホスト/VPC デプロイの選択肢 | O | O | O | O | O | O |
| オープンソース | オープンソースコードの公開とコミュニティ | O | X | O | X | O | O |
| データ主権 & コンプライアンス | データリージョン選択と SOC 2/HIPAA/GDPR コンプライアンス | O | O | O | △ | △ | △ |
| RBAC & SSO | SSO/SAML 認証を備えたロールベースのアクセス制御 | O | △ | O | O | O | △ |
| 監査ログ | ユーザーおよびシステムの操作履歴（監査トレール） | O | O | O | X | △ | X |
| データウェアハウス・エクスポート | Snowflake, BigQuery, S3 等への自動エクスポート | △ | O | O | X | X | X |