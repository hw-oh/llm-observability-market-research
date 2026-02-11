---
layout: default
title: W&B Weave 競合インテリジェンスレポート
---

# 競合インテリジェンスボット

[詳細比較](./comparison) · [製品詳細](./competitor-detail) · [競合インテリジェンス（内部用）](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 最新レポート

<!-- LATEST_REPORT_START -->

[📋 最新レポート (2026-02-11)](./reports/2026-02-11.md)


- Weave は、2026年2月にリリースされた Audio Monitors を通じてマルチモーダル機能での差別化を図っており、LangSmith や Arize Phoenix といった競合他社のテキスト中心の評価フォーカスを超えた進化を遂げています。
- Weave Playground へのカスタム LoRA の統合は、W&B 独自の「学習から推論まで（Training-to-Inference）」の堀（moat）を強化するものであり、純粋なオブザーバビリティツール（Langfuse、Logfire）では対応できない、ファインチューニング済みモデルの評価ワークフローを提供しています。
- LangSmith と Langfuse は、複雑なワークフロー向けの専用グラフ表示による「エージェントの可視化」でリードを広げています。Weave の線形トレース表示は、高度なエージェントのループをデバッグする際には時代遅れに感じられるリスクがあります。
- Braintrust と Langfuse は、専用の「アノテーションキュー」やカンバン表示によって Human-in-the-Loop (HITL) ワークフローをプロフェッショナル化しており、大規模な手動ラベル付け作業において Weave との間にギャップを生んでいます。
- Arize Phoenix は、ローカルファーストの機能（CLI、Notebook サポート）や特化型の「ツール選択」メトリクスにより「AI エンジニア」層を積極的にターゲットにしており、実験フェーズにおける Weave の優位性を脅かしています。
- Helicone と Braintrust は、コスト意識の高いエンジニアリングチームへの足がかりとして「AI プロキシ」アーキテクチャ（キャッシュ、レート制限）を引き続き活用していますが、これは Weave の SDK ベースのアプローチではカバーされていない機能です。

> Weave は、独自の LoRA やマルチモーダル機能によって「学習から推論まで」のフライホイールでリードしていますが、エージェントの可視化や Human-in-the-Loop のアノテーションワークフローにおいては、LangSmith や Langfuse からの激しい追い上げに直面しています。


<!-- LATEST_REPORT_END -->

## 新機能（過去30日間）

### [Weave](https://app.getbeamer.com/weave/en)

- **Audio monitors**: LLM ジャッジを使用した音声出力（MP3/WAV）の評価をサポートし、ボイスエージェントのオブザーバビリティを可能にしました。(2026-02-01) [[docs]](https://wandb.ai/onlineinference/genai-research/reports/A-guide-to-LLM-debugging-tracing-and-monitoring--VmlldzoxMzk1MjAyOQ)
- **Dynamic Leaderboards**: 評価結果から自動生成されるリーダーボード。永続的なフィルタリングやカスタマイズオプションを備えています。(2026-01-29) [[docs]](https://wandb.ai/onlineinference/genai-research/reports/A-guide-to-LLM-debugging-tracing-and-monitoring--VmlldzoxMzk1MjAyOQ)
- **Custom LoRAs in Playground**: ファインチューニングされたカスタム LoRA の重みを Weave Playground に直接ロードしてテストする機能。(2026-01-16) [[docs]](https://wandb.ai/onlineinference/genai-research/reports/A-guide-to-LLM-debugging-tracing-and-monitoring--VmlldzoxMzk1MjAyOQ)

### [LangSmith](https://changelog.langchain.com/feed.rss)

- **トレースプレビューのカスタマイズ**: UI でのトレースのプレビュー方法をカスタマイズできる機能。(2026-02-06)
- **LangSmith セルフホスト版 v0.13**: セルフホスト型エンタープライズ版のアップデート。(2026-01-16)
- **クライアントライブラリ v0.7.1**: 安定性の向上と OIDC サポートのための JS/Python SDK のアップデート。(2026-02-10)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 サポート**: プレイグラウンドで Anthropic の Claude Opus 4.6 モデルをサポートし、自動コスト追跡機能を追加。(2026-02-09) [[docs]](https://arize.com/docs/phoenix/release-notes)
- **ツール選択および呼び出しエバリュエーター**: エージェントが正しいツールを選択し、有効なパラメータで呼び出したかを判定する新しい専用エバリュエーター。(2026-01-31) [[docs]](https://arize.com/docs/phoenix/release-notes)
- **設定可能なメール抽出 (OAuth2)**: Azure AD/Entra ID 統合のためのカスタムメール抽出パス（例：preferred_username）のサポート。(2026-01-28) [[docs]](https://arize.com/docs/phoenix/release-notes)
- **プロンプト/データセット用 CLI コマンド**: プロンプトやデータセットのリスト表示、閲覧、パイプ処理を可能にする新しい CLI コマンド。ターミナルベースのワークフローを実現。(2026-01-22) [[docs]](https://arize.com/docs/phoenix/release-notes)
- **スパン関連付けによるデータセット作成**: 元のソーススパンへの双方向リンクを保持したまま、トレースからデータセットを作成する機能。(2026-01-21) [[docs]](https://arize.com/docs/phoenix/release-notes)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **トレースレベルのスコアラー**: カスタムコードスコアラーが実行トレース全体にアクセスできるようになり、マルチステップのワークフローやエージェントの挙動を評価可能に。(2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **LangSmith 統合**: LangSmith のトレースを Braintrust にルーティングする実験的なラッパー。並行利用や移行を容易にします。(2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **自動インストルメンテーション (Python/Ruby/Go)**: Python、Ruby、Go SDK において、主要なプロバイダーに対するコード改変不要のトレース機能。(2026-01) [[docs]](https://braintrust.dev/docs/changelog)
- **Temporal 統合**: Temporal のワークフローとアクティビティを自動トレースし、ワーカー間の分散トレースをキャプチャ。(2026-01) [[docs]](https://braintrust.dev/docs/changelog)
- **レビュー用カンバンレイアウト**: フラグが立てられたスパンを管理するための新しい UI。ドラッグ＆ドロップのカードでステータスを更新可能。(2026-01) [[docs]](https://braintrust.dev/docs/changelog)

### [Langfuse](https://langfuse.com/changelog)

- **トレースの修正済み出力**: トレースビューで LLM 出力の改善版を直接キャプチャし、ファインチューニング用データセットを構築。(2026-01-14) [[docs]](https://langfuse.com/changelog)
- **推論/思考プロセスのトレースサポート**: トレース詳細で思考/推論部分をレンダリング（v3.148.0）。DeepSeek などのモデルをサポート。(2026-01-27) [[docs]](https://github.com/langfuse/langfuse/pull/11615)
- **単一オブザベーションの評価**: 単一のオブザベーションに対して評価を実行する機能のサポート（v3.150.0）。(2026-02-09) [[docs]](https://github.com/langfuse/langfuse/pull/11547)

### [Logfire](https://logfire.pydantic.dev/docs/release-notes)

- **プロジェクト移行用のマルチトークンサポート**: プロジェクト移行ワークフローを容易にするため、複数のトークンの使用をサポート。(2026-02-04) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **OTel Gen AI セマンティックコンベンション**: OpenTelemetry Gen AI セマンティックコンベンションのスカラー属性のサポートを追加。(2026-01-28) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **Pytest 統合**: テスト実行をトレースするための pytest とのネイティブ統合。(2026-01-26) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **DSPy 統合**: DSPy フレームワークのインストルメンテーションサポートを追加。(2026-01-16) [[docs]](https://logfire.pydantic.dev/docs/release-notes)


## レポートアーカイブ

<!-- REPORT_ARCHIVE_START -->

| 日付 | レポート |
|------|--------|
| 2026-02-11 | [レポートを表示](./reports/2026-02-11.md) |
| 2026-02-10 | [レポートを表示](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)