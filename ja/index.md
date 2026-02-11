---
layout: default
title: W&B Weave 競合インテリジェンスレポート
---

# 競合インテリジェンスボット

[詳細比較](./comparison) · [製品詳細](./competitor-detail) · [競合インテリジェンス (社内用)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 最新レポート

<!-- LATEST_REPORT_START -->

[📋 最新レポート (2026-02-11)](./reports/2026-02-11.md)


- Weave は、Audio Monitors（2026年2月）のリリースにより、ボイスエージェント市場において重要な差別化要因を確保し、Langfuse や LangSmith といったテキスト中心の競合他社との差を広げました。
- LangSmith の「デプロイメント」（インフラ）への戦略的転換と Braintrust の「AI Proxy」は、競合がトラフィックパスの制御に動く中で、Weave を受動的なオブザーバーの役割に追いやる脅威となっています。
- Arize Phoenix と Braintrust は、特化型の「ツール選択」メトリクスや「トレースレベルのスコアラー」によってエージェント評価の基準を引き上げており、Weave の汎用的なスコアラーフレームワークに挑戦しています。
- Weave の「Dynamic Leaderboards」は、Langfuse の静的なダッシュボードに対する強力な対抗軸となり、モデル比較において優れた柔軟性を提供しています。
- Logfire の深い Pydantic 統合と SQL ベースのアナリティクスは、UI 重視のワークフローよりもコード優先のデバッグを好む Python ネイティブなエンジニアリングチームの間で、Weave のシェアを侵食し続けています。
- Braintrust の新しい Cursor IDE 統合は、「エディタ内オブザーバビリティ」へのシフトを示唆しており、Weave のノートブック中心の開発ループをバイパスする可能性があります。

> Weave はマルチモーダル（音声）オブザーバビリティとモデルトレーニング統合においてリードしていますが、エージェントインフラに関しては LangSmith から、エンタープライズプロキシ機能に関しては Braintrust からの圧力が高まっています。


<!-- LATEST_REPORT_END -->

## 新機能 (直近30日間)

### [Weave](https://app.getbeamer.com/weave/en)

- **Audio monitors**: テキストと並行して音声出力を監視・判定するモニターの作成をサポートし、ボイスエージェントの評価を可能にしました。(2026-02-01)
- **Dynamic Leaderboards**: カスタマイズ可能なフィルターと豊富な可視化オプションを備えた、評価結果からのリーダーボード自動生成機能。(2026-01-29)
- **Custom LoRAs in Playground**: W&B Artifacts からカスタム微調整された LoRA 重みを Weave Playground で直接使用できる機能。(2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **Customize trace previews**: トレースプレビューペインをカスタマイズして、関連するメタデータや入出力を一目で確認できる機能。(2026-02-06)
- **Google Gen AI Wrapper**: 手動のインスツルメンテーションなしで Google Gen AI モデルをトレースするための新しい SDK ラッパー。(2026-01-31)
- **LangSmith Self-Hosted v0.13**: 安定性の向上とクラウド版の新機能を取り込んだセルフホスト版のアップデート。(2026-01-16)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 Support**: 拡張思考パラメータと正確なコスト追跡を備えた Anthropic の最新モデルの Playground サポート。(2026-02-09) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **Tool Selection & Invocation Evaluators**: エージェントが正しいツールを選択し、有効なパラメータで呼び出したかを評価する新しい特化型エバリュエーター。(2026-01-31) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **CLI Commands for Prompts/Datasets**: プロンプトのリスト表示、閲覧、AI アシスタントへのパイプ処理、およびターミナルからのデータセット/実験管理のための包括的な CLI サポート。(2026-01-22) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **Trace-to-Dataset with Span Links**: 元のソーススパンへの双方向リンクを維持したまま、本番トレースから厳選されたデータセットを作成する機能。(2026-01-21) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **Export Annotations with Traces**: オフライン分析のために、トレースを手動ラベルや評価スコアと共にエクスポートする CLI サポート。(2026-01-19) [[docs]](https://docs.arize.com/phoenix/release-notes)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **Trace-level scorers**: カスタムコードスコアラーが実行トレース全体にアクセスできるようになり、マルチステップのワークフローやエージェントの動作を評価可能に。(2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **LangSmith integration**: トレースを LangSmith と Braintrust の両方に並行してルーティング、または Braintrust へ完全に移行するためのラッパー。(2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **Cursor integration**: 自然言語を介してログの照会や実験の実行を行うための Cursor エディタ用 Braintrust 拡張機能。(2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **Auto-instrumentation (Python, Ruby, Go)**: Python、Ruby、Go アプリケーション向けのコード記述不要なトレースサポート。(2026-01) [[docs]](https://braintrust.dev/docs/changelog)
- **Temporal integration**: Temporal のワークフローとアクティビティを、親子関係のマッピングと共に自動トレース。(2026-01) [[docs]](https://braintrust.dev/docs/changelog)

### [Langfuse](https://langfuse.com/changelog)

- **Corrected Outputs for Traces**: トレースビューで LLM 出力の改善版を直接キャプチャし、微調整用データセットを構築する機能。(2026-01-14) [[docs]](https://langfuse.com/docs/observability/corrections)

### [Logfire](https://logfire.pydantic.dev/docs/release-notes)

- **Multi-token support for project migration**: プロジェクト移行をよりスムーズにするための複数トークン処理のサポートを追加。(2026-02-04) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **OTel Gen AI semantic conventions**: OpenTelemetry Gen AI セマンティックコンベンションのスカラー属性のサポートを追加。(2026-01-28) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **Pytest integration**: pytest のテスト実行内でシームレスなトレースとオブザーバビリティを可能にする新しい統合。(2026-01-26) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **DSPy integration**: DSPy アプリケーションをトレースおよび監視するための公式統合。(2026-01-16) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **Claude SDK instrumentation**: Anthropic Claude SDK 専用のインスツルメンテーションを追加。(2026-01-12) [[docs]](https://logfire.pydantic.dev/docs/release-notes)


## レポートアーカイブ

<!-- REPORT_ARCHIVE_START -->

| 日付 | レポート |
|------|--------|
| 2026-02-11 | [レポートを表示](./reports/2026-02-11.md) |
| 2026-02-10 | [レポートを表示](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)