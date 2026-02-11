---
layout: default
title: W&B Weave 競合インテリジェンスレポート
---

# 競合インテリジェンスボット

[詳細比較](./comparison) · [製品詳細](./competitor-detail) · [競合インテリジェンス (社内用)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 最新レポート

<!-- LATEST_REPORT_START -->

[📋 最新レポート (2026-02-11)](./reports/2026-02-11.md)


- Weave は、Audio Monitors（2026年2月）のリリースにより、マルチモーダル・オブザーバビリティにおける先行者利益を確立し、LangSmith や Langfuse といったテキスト中心の競合他社との差別化を図っています。
- LangSmith は、複雑なエージェント・ワークフローにおいて依然として主要な脅威です。Weave の現在のトレースツリー表示ではまだ対応できていない、循環グラフやステートマシンの優れた可視化機能を提供しています。
- Braintrust は、「Data Plane」アーキテクチャと幅広い SDK サポート（Java、Go、C#）により、エンタープライズ側での切り崩しに成功しており、Weave の Python/TS 中心の SDK ではカバーできていないバックエンドエンジニアリングチームを獲得しています。
- 「Human-in-the-Loop」の格差が広がっています。LangSmith、Langfuse、Braintrust はいずれも専用の「アノテーションキュー」やカンバンワークフローをリリースしていますが、Weave はレビューにおいて、より汎用的なボード/テーブルインターフェースに依存しています。
- MLflow (v3.9) は、「Judge Builder」と「MemAlign」によって評価機能の差を積極的に埋めており、Databricks ネイティブなチームにおける Weave の評価主導型開発ループの優位性を脅かしています。
- Arize Phoenix による特化型「Tool Selection Evaluators」のリリースは、市場が粒度の細かいエージェントコンポーネントテストへと移行していることを示唆しています。Weave はエージェントの信頼性において同等性を維持するために、この領域を優先すべきです。

> Weave はマルチモーダル対応とトレーニングから推論への継続性においてリードしていますが、エージェント・ワークフローの可視化では LangSmith から、エンタープライズデータプライバシーアーキテクチャでは Braintrust から大きな圧力を受けています。


<!-- LATEST_REPORT_END -->

## 新機能 (直近30日間)

### [Weave](https://app.getbeamer.com/wandb/en)

- **Audio Monitors**: オーディオ対応の LLM Judge を使用して、テキストと並行してオーディオ出力を監視・判定するモニターの作成をサポート。(2026-02-01)
- **Dynamic Leaderboards**: モデルや評価フィルターに基づいて即座にデータが入力される、評価（Evaluations）内の自動生成リーダーボード。(2026-01-29)
- **Custom LoRAs in Playground**: W&B Artifacts からカスタムファインチューニングされた LoRA 重みを直接 Weave Playground にロードしてテストする機能。(2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **Customize Trace Previews**: リストビューでのトレースデータのプレビュー方法をユーザーが設定できる UI アップデート。(2026-02-06)
- **SDK v0.7.1**: LangSmith オブザーバビリティおよび評価プラットフォームに接続するためのクライアントライブラリのアップデート。(2026-02-10)

### [Langfuse](https://langfuse.com/changelog)

- **Corrected Outputs for Traces**: ファインチューニング用データセットを構築するために、トレースビューで LLM 出力の改善版を直接キャプチャ。(2026-01-14)
- **Inline Comments on Observation I/O**: トレースの入力および出力内の特定のテキスト選択箇所にコメントを固定。(2026-01-07)
- **Reasoning/Thinking Rendering**: トレース内での推論モデル（例：O1、R1）の「思考（thinking）」部分に特化した UI レンダリング。(2026-02-01)
- **Org Audit Log Viewer**: セキュリティとコンプライアンスのための、組織レベルの監査ログを表示する新しい UI。(2026-02-01)
- **Single Observation Evals**: 完全なトレースではなく、個別のオブザベーションに対して評価を実行する機能。(2026-02-01)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **Trace-level Scorers**: カスタムコードスコーラーが実行トレース全体にアクセスし、マルチステップのワークフローやエージェントの動作を評価可能に。(2026-02)
- **LangSmith Integration**: トレースを LangSmith と Braintrust の両方にルーティング、またはトラフィックを完全に移行するためのラッパー。(2026-02)
- **Cursor Integration**: Braintrust MCP サーバーを設定するための拡張機能。Cursor IDE から直接ログのクエリや実験の取得が可能に。(2026-02)
- **Auto-instrumentation (Python/Ruby/Go)**: Python、Ruby、Go SDK 向けのコード記述不要なトレースサポートを追加。(2026-01)
- **Temporal Integration**: Temporal のワークフローとアクティビティの自動トレース。ワーカーをまたがる分散トレースをキャプチャ。(2026-01)

### [MLflow](https://mlflow.org/releases)

- **MLflow Assistant**: UI 内で問題を診断し修正を提案する、Claude Code 搭載の製品内チャットボット。(2026-01-29)
- **Agent Performance Dashboards**: エージェントのレイテンシ、リクエスト数、品質スコアを監視するための構築済みチャート。(2026-01-29)
- **MemAlign Judge Optimizer**: 過去のフィードバックから評価ガイドラインを学習し、Judge の精度を向上させるアルゴリズム。(2026-01-29)
- **Judge Builder UI**: コードなしでカスタム LLM Judge プロンプトを作成、テスト、検証するためのビジュアルインターフェース。(2026-01-29)
- **Continuous Online Monitoring**: 本番環境のトレースに対して LLM Judge を自動実行し、品質の問題をリアルタイムで検出。(2026-01-29)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 Support**: Playground において、正確なコスト追跡機能を備えた Anthropic の Claude Opus 4.6 モデルのサポートを追加。(2026-02-09)
- **Tool Selection & Invocation Evaluators**: エージェントが正しいツールを選択し、有効なパラメータで呼び出したかを評価する新しい特化型エバリュエーター。(2026-01-31)
- **Phoenix CLI Expansion**: ターミナルから直接プロンプト、データセット、実験を管理するための包括的な CLI コマンド。(2026-01-22)
- **Trace-to-Dataset with Span Links**: リネージ（系統）のためにソーススパンへの双方向リンクを維持したまま、トレースからデータセットを作成する機能。(2026-01-21)
- **Export Annotations with Traces**: オフライン分析のために、トレースと並行して人間および AI によるアノテーションをエクスポートする CLI サポート。(2026-01-19)


## レポートアーカイブ

<!-- REPORT_ARCHIVE_START -->

| 日付 | レポート |
|------|--------|
| 2026-02-11 | [レポートを表示](./reports/2026-02-11.md) |
| 2026-02-10 | [レポートを表示](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)