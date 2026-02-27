---
layout: default
title: LLM Observability — 詳細機能比較
---

# LLM Observability — 詳細機能比較
**日付**: 2026-02-25 | **モデル**: google/gemini-3-pro-preview

> O(強力) / △(中程度) / X(なし、または該当なし)

## Core Tracing & Logging

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| フルリクエスト/レスポンス Tracing | LLMの入力プロンプト、出力レスポンス、パラメータの完全なキャプチャ | O | O | O | O | O | O |
| ネストされた Span & ツリービュー | 親子ツリー視覚化による階層的な Span Tracing | O | O | O | O | O | O |
| Streaming サポート | ストリーミング LLM レスポンスのリアルタイム Tracing | △ | O | △ | O | △ | △ |
| マルチモーダル Tracing | 画像、音声、その他の非テキスト入力/出力の Tracing とレンダリング | O | △ | △ | △ | △ | X |
| Auto-Instrumentation | 1行のコードによる自動トレース収集（デコレータ、autologなど） | O | O | O | O | O | O |
| メタデータ & タグフィルタリング | カスタムメタデータとタグの付与、および検索・フィルタリング | O | O | O | O | O | O |
| トークンカウント & 推定 | トークナイザーごとの正確な入力/出力/キャッシュトークン数のカウント | O | O | O | O | O | △ |
| OpenTelemetry 標準 | OTEL標準のトレースエクスポート/インポート互換性 | O | O | O | O | O | O |

## Agent & RAG Specifics

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| RAG Retrieval Visualizer | 取得されたドキュメントチャンクの内容と関連性スコアのUI表示 | O | O | △ | △ | △ | O |
| Tool/Function Call レンダリング | ツール/関数呼び出しの入力と戻り値のパース済み表示 | O | O | O | O | O | O |
| Agent 実行グラフ | ループや分岐を含む Agent ワークフローの DAG/グラフ視覚化 | O | O | O | O | △ | O |
| 中間ステップの状態 | Agent の中間的な推論過程（Chain-of-Thought）の保存と表示 | O | O | O | O | O | O |
| セッション/スレッドリプレイ | ユーザーセッションや会話スレッドを一連の流れとして再生 | X | O | O | △ | O | △ |
| 失敗ステップのハイライト | Agent トレース内での失敗したステップの自動ハイライト | △ | O | O | O | O | O |
| MCP 統合 | Model Context Protocol サーバー/クライアントの統合と Tracing | O | O | O | X | X | O |

## Evaluation & Quality

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| LLM-as-a-Judge ウィザード | コード不要の GUI ベース LLM Judge ビルダー | O | O | O | O | O | △ |
| カスタム Eval Scorers | ユーザー定義のコードベース評価関数の作成と実行 | O | O | O | O | O | O |
| データセット管理 & キュレーション | Eval データセットの作成、バージョニング、トレースからデータセットへの変換 | X | O | O | X | O | O |
| プロンプト最適化 / DSPy サポート | 自動プロンプト最適化または候補の提案（DSPy 統合など） | X | △ | △ | X | O | O |
| 回帰テスト | モデル/プロンプト変更時の自動的な品質低下（回帰）検知 | O | O | O | O | △ | O |
| 比較ビュー (Side-by-side) | モデル/プロンプト出力の横並び比較 | X | O | O | X | O | O |
| アノテーションキュー | キュー管理とレビュー担当者割り当てによるチームベースのアノテーションワークフロー | △ | O | O | △ | △ | X |
| オンライン Eval | 本番環境のライブトラフィックに対するリアルタイム自動評価 | O | O | O | O | O | O |

## Guardrails & Safety

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| PII/機密データマスキング | PII（個人情報）および機密データの自動検知とマスキング | X | △ | O | X | O | X |
| ハルシネーション検知 | ハルシネーション（幻覚）コンテンツを検知するための専用 Guardrail | O | O | △ | △ | O | O |
| トピック/ジェイルブレイク Guardrails | 禁止トピックのブロックおよびジェイルブレイク試行の検知 | O | O | △ | X | X | X |
| Policy Management as Code | コードとして定義・管理される Guardrail ルール | O | X | △ | X | △ | X |

## Analytics & Dashboard

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| コスト分析 & アトリビューション | ユーザー/チーム/プロジェクトごとのコスト追跡と割り当て | O | O | O | O | X | △ |
| トークン使用量分析 | 入力/出力トークン使用量の内訳とトレンド | O | O | O | O | O | O |
| レイテンシヒートマップ & P99 | パーセンタイル監視を伴うレイテンシ分布の視覚化 | O | O | O | X | O | O |
| エラー率モニタリング | エラー率の追跡とアラート通知 | O | O | O | O | O | O |
| Embedding 空間の視覚化 | UMAP/t-SNE による埋め込みベクトルのクラスタリングと視覚化 | X | X | X | X | X | O |
| カスタムメトリクス & Dashboard | ユーザー定義のカスタムメトリクス追跡とダッシュボードウィジェット | O | O | O | O | O | O |

## Development Lifecycle

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| プロンプト管理 (CMS) | 非エンジニアでも編集・デプロイ可能なプロンプトのバージョニング | O | O | O | O | O | O |
| Playground & サンドボックス | インタラクティブなプロンプトとパラメータのテスト環境 | O | O | O | O | △ | O |
| 実験トラッキング | ハイパーパラメータのログ記録を伴う A/B テストと実験管理 | O | O | O | O | O | O |
| Fine-tuning 統合 | Fine-tuning 用データの書き出しとパイプライン統合 | O | △ | △ | X | △ | X |
| バージョン管理 & ロールバック | プロンプトとモデルのバージョン管理とロールバック機能 | O | O | O | O | O | △ |

## Integration & DX

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| SDK サポート (Py/JS/Go) | Python、JavaScript/TypeScript、Go における公式 SDK サポート | X | O | O | X | △ | O |
| Gateway/Proxy モード | SDK インストール不要のプロキシベース Tracing（URL変更のみ） | X | X | X | O | O | X |
| 主要フレームワーク対応 | LangChain, LlamaIndex, AutoGen, CrewAI などの組み込みサポート | O | O | O | O | O | O |
| API & Webhooks | 外部システム連携のための REST/GraphQL API と Webhook 統合 | O | O | O | O | △ | O |
| CI/CD 統合 | 自動 Eval とデプロイのための CI/CD パイプライン（GitHub Actionsなど）との統合 | O | O | O | O | △ | △ |

## Enterprise & Infrastructure

| 機能 | 説明 | Weave | LangSmith | Langfuse | Braintrust | MLflow | Arize Phoenix |
|---|---|---|---|---|---|---|---|
| デプロイオプション | マルチテナント SaaS、専用 SaaS、セルフホスト/VPC デプロイの選択肢 | O | O | O | O | O | O |
| オープンソース | オープンソースコードの公開とコミュニティ | △ | X | O | X | O | O |
| データ主権 & コンプライアンス | データリージョン選択と SOC 2/HIPAA/GDPR コンプライアンス | X | △ | O | △ | O | O |
| RBAC & SSO | SSO/SAML 認証を伴うロールベースのアクセス制御 | O | O | O | △ | △ | O |
| 監査ログ | ユーザーおよびシステムの操作履歴（監査トレール） | O | △ | O | △ | △ | X |
| データウェアハウス・エクスポート | Snowflake, BigQuery, S3 などへの自動エクスポート | O | △ | O | O | O | △ |