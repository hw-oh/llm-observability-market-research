---
layout: default
title: W&B Weave 競合インテリジェンス・レポート
---

# Competitor Intel Bot

[詳細な比較](./comparison) · [製品詳細](./competitor-detail) · [競合インテリジェンス (内部用)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)

## 最新レポート

<!-- LATEST_REPORT_START -->

[📋 最新レポート (2026-02-11)](./reports/2026-02-11.md)


- Weave はマルチモーダル対応（Audio Monitors）で差別化を図っています。競合がテキストやツール中心に留まる中、ボイスエージェントのオブザーバビリティにおいてリードを広げています。
- LangSmith と Langfuse は「エージェンティック・オブザーバビリティ」を積極的に深掘りしており、推論ステップや循環グラフの専用ビジュアライゼーションを導入し、Weave のトレースビューに圧力をかけています。
- Braintrust と LangSmith は、専用のアノテーション・キューによって「Human-in-the-Loop」のナラティブを支配しています。これは Weave が現在、直接的にはあまり対応できていないワークフロー機能です。
- Weave の「Dynamic Leaderboards」リリースは、モデル比較を自動化することで Braintrust の評価機能の成熟度に対抗しており、企業のモデル選定における重要なニーズに応えています。
- 「オープンスタンダード」の脅威が増大しており、Arize Phoenix と Logfire は OpenTelemetry (OTLP) を活用して、ベンダー固有の計装を避けたいチームにアピールしています。
- Weave は W&B Training/Artifacts との深い統合により、独自の防御壁を維持しています。これにより、競合がエクスポート経由でしかサポートできない「ファインチューニングによる修正（Fix-by-Fine-tuning）」ループをネイティブに提供しています。
- LangSmith が LangGraph Platform を「Deployment」へとリブランドしたことは、ランタイムレイヤーの所有へのシフトを意味しており、純粋なオブザーバビリティ・プレイヤーをコモディティ化する恐れがあります。

> Weave はマルチモーダル・オブザーバビリティとトレーニング統合においてリードしていますが、エージェントの可視化については LangSmith から、エンタープライズ評価ワークフローについては Braintrust から、それぞれ特有の圧力を受けています。


<!-- LATEST_REPORT_END -->

## 新機能 (直近30日間)

### [Weave](https://app.getbeamer.com/weave/en)

- **Audio Monitors**: テキストと並行して音声出力を監視・判定するモニターの作成をサポートし、ボイスエージェントの評価を可能にしました。(2026-02-01)
- **Dynamic Leaderboards**: 評価からリーダーボードを自動生成し、永続的なカスタマイズとCSVエクスポートに対応しました。(2026-01-29)
- **Playground でのカスタム LoRA**: W&B Artifacts からカスタムのファインチューニング済み LoRA 重みを Weave Playground で直接使用できるようになりました。(2026-01-16)

### [LangSmith](https://changelog.langchain.com)

- **トレースプレビューのカスタマイズ**: UI でのトレースのプレビュー方法をカスタマイズできるようになり、トリアージの速度が向上しました。(2026-02-06) [[docs]](https://docs.smith.langchain.com/observability)
- **LangSmith セルフホスト版 v0.13**: 安定性の向上と新機能を含むセルフホスト版のアップデート。(2026-01-16) [[docs]](https://docs.smith.langchain.com/self_hosting)

### [Arize Phoenix](https://arize.com/docs/phoenix/release-notes)

- **Claude Opus 4.6 サポート**: Playground で Anthropic の Claude Opus 4.6 モデルをサポートし、自動コスト追跡に対応しました。(2026-02-09) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **ツール選択・呼び出しエバリュエーター**: エージェントが正しいツールを選択し、有効なパラメータで呼び出したかを評価する新しい専用エバリュエーター。(2026-01-31) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **プロンプト・データセット用 CLI**: プロンプトやデータセットのリスト表示、閲覧、パイプ処理を行う CLI コマンド。AI コーディングアシスタントとの統合を可能にします。(2026-01-22) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **トレースからのデータセット作成**: ソーススパンへの双方向リンクを保持したまま、トレースから直接データセットを作成する機能。(2026-01-21) [[docs]](https://docs.arize.com/phoenix/release-notes)
- **トレースと共のアノテーション・エクスポート**: オフライン分析のために、人間によるフィードバックやアノテーションをトレースと共にエクスポートする CLI サポート。(2026-01-19) [[docs]](https://docs.arize.com/phoenix/release-notes)

### [Braintrust](https://braintrust.dev/docs/changelog)

- **トレースレベル・スコアラー**: カスタムコード・スコアラーが実行トレース全体にアクセスできるようになり、マルチステップのワークフローやエージェントの挙動を評価可能になりました。(2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **LangSmith 統合 (実験的)**: LangSmith のトレースおよび評価コールを Braintrust にルーティングするラッパー。二重ログ記録や移行を可能にします。(2026-02) [[docs]](https://braintrust.dev/docs/changelog)
- **自動計装 (Python, Ruby, Go)**: Python、Ruby、Go SDK において、ほとんどのプロバイダーでコード変更なしのトレースが可能になりました。(2026-01) [[docs]](https://braintrust.dev/docs/changelog)
- **Temporal 統合**: Temporal のワークフローとアクティビティを自動トレースし、実行スパンと分散トレースをキャプチャします。(2026-01) [[docs]](https://braintrust.dev/docs/changelog)
- **トレースの起点へのナビゲート**: ログ内のトレースから、起点のプロンプトやデータセットの行へリンクし、迅速なイテレーションを可能にします。(2026-02) [[docs]](https://braintrust.dev/docs/changelog)

### [Langfuse](https://langfuse.com/changelog)

- **思考 / 推論のレンダリング**: トレース詳細において、思考の連鎖（Chain-of-thought）や推論部分を明示的にレンダリングします (v3.148.0)。(2026-02-01)
- **単一オブザベーションの評価**: フル・トレースではなく、単一のオブザベーションに対して評価を実行できるようになりました (v3.150.0)。(2026-02-05)
- **トレースの修正済み出力**: LLM 出力の改善版をトレースビューで直接キャプチャし、ファインチューニング用データセットを構築できます。(2026-01-14) [[docs]](https://langfuse.com/docs/observability/features/corrections)

### [Logfire](https://logfire.pydantic.dev/docs/release-notes)

- **プロジェクト移行用のマルチトークン対応**: プロジェクトの移行を容易にするため、複数のトークンの使用をサポートしました。(2026-02-04) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **OTel Gen AI セマンティック・コンベンション**: OpenTelemetry Gen AI セマンティック・コンベンションのスカラー属性のサポートを追加しました。(2026-01-28) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **pytest 統合**: pytest 実行時のオブザーバビリティをサポートする新しい統合。(2026-01-26) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **DSPy 統合**: DSPy フレームワークのネイティブな計装サポートを追加しました。(2026-01-16) [[docs]](https://logfire.pydantic.dev/docs/release-notes)
- **Claude SDK 計装**: Anthropic Claude SDK 専用の計装を追加しました。(2026-01-12) [[docs]](https://logfire.pydantic.dev/docs/release-notes)


## レポート・アーカイブ

<!-- REPORT_ARCHIVE_START -->

| 日付 | レポート |
|------|--------|
| 2026-02-11 | [レポートを表示](./reports/2026-02-11.md) |
| 2026-02-10 | [レポートを表示](./reports/2026-02-10.md) |

<!-- REPORT_ARCHIVE_END -->

---

[GitHub](https://github.com/hw-oh/competitor-intel-bot)