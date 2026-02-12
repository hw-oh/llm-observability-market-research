---
layout: default
title: LLM Observability — 製品詳細
---

# LLM Observability — 製品詳細
**日付**: 2026-02-12 | **モデル**: google/gemini-3-pro-preview

### W&B Weave

**概要**: W&B Weaveは、Weights & Biasesのエコシステムに統合された包括的なObservabilityおよびEvalプラットフォームであり、LLMアプリケーションの追跡、評価、改善を行うために設計されています。実験のトラッキング、マルチモーダル評価（オーディオを含む）、モデルレジストリやトレーニングワークフローとのシームレスな連携に優れています。

**強み**:
- W&Bのトレーニングおよびモデルレジストリとの深い統合（例：カスタムLoRA）
- オーディオモニターを含むマルチモーダル評価のサポート
- 実験トラッキングとバージョニングにおける強力な実績
- 自動化されたモデル比較のためのDynamic Leaderboards
- オンプレミス/専用環境を含む柔軟なデプロイオプション

**弱み**:
- ドキュメント内に明示的なPIIマスキングやデータコンプライアンス機能の記載がない
- StreamingのTracing機能の詳細が明示されていない
- エージェント向けのメモリTracingが明示的に強調されていない
- 使用量/クレジットに基づく料金体系が複雑になる可能性がある

**最新のアップデート**:
- Audio Monitors: LLM judgeを使用して、テキストと共にオーディオ出力（MP3/WAV）を監視・判定するモニター。(2026-02-01)
- Dynamic Leaderboards: 評価から自動生成されるリーダーボード。永続的なカスタマイズとCSVエクスポートが可能。(2026-01-29)
- Custom LoRAs in Playground: Weave PlaygroundでカスタムFine-tuningされたLoRAの重みを直接ロードしてテストする機能。(2026-01-16)

| カテゴリ | 評価 | サマリー |
|---|---|---|
| Core Observability | ●●● | シンプルなデコレータを介して、ネストされたスパン、入力、出力、パフォーマンスメトリクスを自動キャプチャする強力なコアTracing機能。 |
| Agent / RAG Observability | ●●● | RAGおよびエージェントワークフローを強力にサポート。検索品質の評価や複雑なツールインタラクションのTracingに特化した機能を備える。 |
| Evaluation Integration | ●●● | Audio Monitors、Dynamic Leaderboards、マルチモーダル出力向けのLLM-as-a-judgeの深い統合など、高度な機能を備えた際立ったカテゴリ。 |
| Monitoring & Metrics | ●●● | コスト、レイテンシ、品質メトリクスの包括的なモニタリング。継続的な評価のためのオンラインモニターの実行が可能。 |
| Experiment / Improvement Loop | ●●● | W&Bの成熟したバージョニングと実験トラッキングのインフラを活用し、ObservabilityをトレーニングやFine-tuningに結びつける優れたループ機能。 |
| DevEx / Integration | ●●● | マルチ言語SDKと、PlaygroundでカスタムLoRAアダプタを直接テストできる独自の機能を備えた強力な開発者体験。 |
| Enterprise & Security | ●●○ | エンタープライズ向けのデプロイオプション（SaaS、専用、オンプレミス）は強力だが、PIIマスキングや監査ログなどの特定のコンプライアンス機能は公開情報に詳細がない。 |


---

### LangSmith

**概要**: LangSmithは、LangChainエコシステムに深く根ざした、AIエージェントの開発、デバッグ、デプロイのためのフレームワークに依存しない包括的なプラットフォームです。堅牢なTracing、Eval、モニタリング機能を通じてエンドツーエンドの可視性を提供し、エンタープライズニーズに合わせてクラウドとセルフホストの両方のデプロイをサポートします。

**強み**:
- LangChainおよびLangGraphフレームワークとの深い統合
- 包括的なHuman-in-the-loopのアノテーションおよび評価キュー
- 堅牢なセルフホストおよびエンタープライズセキュリティオプション
- LLM、ツール、検索にわたる統合されたコストとパフォーマンスの追跡

**弱み**:
- シート数とトレース数に基づく料金体系は、大規模運用で高額になる可能性がある
- フレームワークに依存しない機能があるものの、LangChainとの強い結びつきが他のフレームワーク利用者を遠ざける可能性がある
- 機能セットが膨大であるため、単純なユースケースでは学習曲線が急になる可能性がある

**最新のアップデート**:
- Customize trace previews: UIでのトレースのプレビュー方法をカスタマイズする機能。(2026-02-06)
- Google Gen AI Wrapper: GoogleのGen AIモデル向けの新しいラッパーサポート。(2026-01-31)
- LangSmith Self-Hosted v0.13: エンタープライズデプロイ向けの更新されたセルフホスト版。(2026-01-16)

| カテゴリ | 評価 | サマリー |
|---|---|---|
| Core Observability | ●●● | 詳細な階層的Tracingと、デバッグ用の統合Playground機能を備えたトップクラスのコアObservabilityを提供。 |
| Agent / RAG Observability | ●●● | エージェントおよびRAGのObservabilityに優れ、ツール、検索、複雑な推論チェーン専用のビューを提供。 |
| Evaluation Integration | ●●● | 評価は主要な柱であり、自動テスト、人間によるアノテーション、データセット管理のための堅牢なツールを備える。 |
| Monitoring & Metrics | ●●● | リアルタイムのアラートと詳細な分析により、コスト、レイテンシ、エラーをカバーする包括的なモニタリングスイート。 |
| Experiment / Improvement Loop | ●●● | 統合されたプロンプトエンジニアリング、バージョニング、実験トラッキングにより、改善ループを強力にサポート。 |
| DevEx / Integration | ●●● | 幅広いフレームワークサポート、SDK、シームレスな統合のためのCLIツールを備えた優れた開発者体験。 |
| Enterprise & Security | ●●● | セルフホストオプション、堅牢なセキュリティコンプライアンス（SOC 2、HIPAA）、きめ細かなアクセス制御を備えたエンタープライズ対応。 |


---

### Langfuse

**概要**: Langfuseは、Observability、プロンプト管理、Evalを統合した、オープンソースで開発者中心のLLMエンジニアリングプラットフォームです。強力なセルフホスティング機能、深いエージェントTracing（グラフやツール呼び出しを含む）、実験の実行とデータセット管理のための包括的なスイートによって差別化されています。

**強み**:
- 完全にオープンソースでセルフホスト可能であり、最大限のデータ制御を提供
- Observability、プロンプト管理、Evalを組み合わせた統合プラットフォーム
- グラフビューと推論ステップの可視化を備えた高度なエージェントTracing
- LLM-as-a-judgeや人間によるアノテーションキューを含む堅牢な評価スイート
- 複雑なモデル料金体系をサポートする正確なコスト追跡

**弱み**:
- リプレイ機能が、ワンクリックのインスタントトレースリプレイではなく、Playgroundを介した手動操作である
- 大規模なセルフホスティングには、複雑なインフラ（ClickHouse）の管理が必要
- ネイティブなFine-tuningのオーケストレーションが欠如している（データエクスポートに依存）

**最新のアップデート**:
- Run Experiments on Versioned Datasets: 特定のバージョンのタイムスタンプでデータセットを取得し、再現性のために過去のバージョンで実験を実行。(2026-02-11)
- Org Audit Log Viewer: セキュリティおよびアクセスイベントを追跡するための組織レベルの監査ログビューア。(2026-02-09)
- Render Thinking/Reasoning: トレース詳細ビューで、LLMレスポンスの思考・推論部分を個別にレンダリング。(2026-02-09)
- Single Observation Evals: 単一のオブザベーションに対して直接評価を実行する機能のサポート。(2026-02-09)
- Corrected Outputs for Traces: Fine-tuningデータセットを構築するために、トレースビューでLLM出力の改善版を直接キャプチャ。(2026-01-14)

| カテゴリ | 評価 | サマリー |
|---|---|---|
| Core Observability | ●●● | ネストされたスパンへの深い可視性と正確なトークン/コスト追跡を、堅牢なタイムラインビューで提供。 |
| Agent / RAG Observability | ●●● | エージェントおよびRAGのモニタリングに非常に長けており、グラフ、ツール使用、多段階の推論プロセスの専用の可視化機能を備える。 |
| Evaluation Integration | ●●● | LLM-as-a-judge、人間によるアノテーションキュー、ワークフローに直接統合されたデータセット管理により、完全な評価ループを提供。 |
| Monitoring & Metrics | ●●● | 正確なコスト計算（料金体系を含む）と柔軟なカスタムDashboardに焦点を当てた強力なモニタリング機能。 |
| Experiment / Improvement Loop | ●●● | バージョン管理されたデータセット、プロンプト管理、体系的な実験を通じて、厳格なテストを可能にするエンジニアリングライフサイクルの優れたサポート。 |
| DevEx / Integration | ●●● | 堅牢なSDK、OpenTelemetry互換性、柔軟なAPIファーストのアーキテクチャを備えた開発者優先の設計。 |
| Enterprise & Security | ●●● | RBAC、監査ログ、完全なデータ主権のためのセルフホスト機能など、強力なセキュリティ機能を備えたエンタープライズ対応。 |


---

### Braintrust

**概要**: Braintrustは、CursorやMCPなどのツールを通じてコーディングワークフローと密接に統合された、開発者中心のAI ObservabilityおよびEvalプラットフォームです。6つのプログラミング言語にわたる包括的なTracing、トレースレベルのScoringを備えた堅牢な評価機能、セルフホスティングやRBACなどのエンタープライズグレードの機能を提供します。

**強み**:
- Python、TS、Go、Java、Ruby、C#をカバーする広範なSDKエコシステム
- MCPを介したCursorやVS Codeなどの開発者ツールとの深い統合
- データセット、実験、本番モニタリングを接続する統合された評価ワークフロー
- SQLとBTQLの両方を使用した柔軟なデータクエリ機能
- セルフホスティングやVPCを含む強力なエンタープライズデプロイオプション

**弱み**:
- RAGの検索品質に関する専用の可視化ウィジェット（例：チャンクのヒートマップ）の欠如
- Fine-tuningやRLHFのための組み込みマネージドサービスがない（データエクスポートに依存）
- 複雑なメモリ状態の変化に関する標準の可視化機能が限定的
- PIIマスキング機能の詳細が競合他社に比べて明示されていない
- リージョンサポートのドキュメントが限定的

**最新のアップデート**:
- Render attachments in custom views: カスタムトレースビューで画像、動画、オーディオを直接レンダリング可能に。(2026-02-01)
- Navigate to trace origins: ログ内のトレースから、その発生元となったプロンプトやデータセットの行へ戻るナビゲーション。(2026-02-01)
- Trace-level scorers: カスタムコードScoringが、多段階評価のために実行トレース全体にアクセス可能に。(2026-02-01)
- LangSmith integration: Tracingおよび評価の呼び出しをLangSmithとBraintrustの両方に送信するラッパー。(2026-02-01)
- Cursor integration: Cursorエディタ内でBraintrust MCPサーバーを自動構成する拡張機能。(2026-02-01)
- Image rendering security controls: ログ内の外部画像に対する構成可能なモード（自動ロード、クリックしてロード、ブロック）。(2026-02-01)
- Single span filters with aggregations: 単一スパンフィルタとGROUP BYを組み合わせた集計トレース分析。(2026-02-01)
- Auto-instrumentation for Python, Ruby, Go: 主要言語向けのコード改変不要なTracingサポート。(2026-01-29)
- Temporal integration: Temporalのワークフローとアクティビティの自動Tracing。(2026-01-21)
- Kanban layout for reviews: フラグが立てられたスパンやレビューを管理するためのドラッグ＆ドロップインターフェース。(2026-01-21)

| カテゴリ | 評価 | サマリー |
|---|---|---|
| Core Observability | ●●● | 階層的な実行への深い可視性、生データ検査の強力なサポート、統合されたPlaygroundリプレイ機能を備えた堅牢なコアTracingを提供。 |
| Agent / RAG Observability | ●●● | 最近のMCPやTemporalとの統合により、エージェントワークフローとツール使用を強力にサポート。ただし、専用のRAG可視化はそれほど目立たない。 |
| Evaluation Integration | ●●● | Tracing、データセット、Scoringの間のシームレスなループを提供し、トレースレベルのScoringなどの高度な機能を備えた評価統合のマーケットリーダー。 |
| Monitoring & Metrics | ●●● | SQLやBTQLを使用してカスタムメトリクスを定義できる柔軟性を備えた、包括的なモニタリングDashboardを提供。 |
| Experiment / Improvement Loop | ●●● | プロンプトエンジニアリングやデータセット管理において実験ループを強力にサポート。ただし、マネージドなモデルトレーニングまではカバーしていない。 |
| DevEx / Integration | ●●● | 幅広いSDKカバー率、独自のIDE統合（Cursor）、最新のエージェントフレームワークのサポートを備えたクラス最高の開発者体験。 |
| Enterprise & Security | ●●● | セルフホスティングときめ細かなアクセス制御を備えた強力なエンタープライズ向け製品で、セキュリティを重視する組織に適している。 |


---

### MLflow

**概要**: 機械学習ライフサイクルのためのオープンソースのエンドツーエンドプラットフォームであり、GenAIのObservabilityおよびEvalへと大幅に拡張されました。包括的なTracing、エージェントモニタリングDashboard、ビジュアルビルダーや最適化アルゴリズムを含む高度な「LLM-as-a-Judge」機能を提供します。

**強み**:
- 従来のMLとGenAI（エージェント、LLM）のための統合プラットフォーム
- MemAlignオプティマイザとJudge Builder UIを備えた強力な「LLM-as-a-Judge」エコシステム
- 完全なOpenTelemetry互換性を備えたオープンソースかつベンダーニュートラルな設計
- 広範なフレームワーク統合（LangChain, LlamaIndex, DSPy, CrewAI）
- マルチワークスペースのエンタープライズ管理のための新しい「Organization Support」

**弱み**:
- SaaS専用の競合他社と比較して、セルフホスティングにはインフラ（データベース、サーバー）の管理が必要
- UIテレメトリの収集がデフォルトで有効になっている（オプトアウト可能）
- 複雑なエージェントトレースに対する直接的な「リプレイ」機能が、特化型ツールほど明示的ではない

**最新のアップデート**:
- Organization Support: 実験やリソースを整理するためのマルチワークスペース環境のサポート。(2026-02-12)
- MLflow Assistant: エージェントのデバッグや問題解決を支援する、Claude Codeを搭載した製品内チャットボット。(2026-01-29)
- Agent Performance Dashboards: レイテンシ、リクエスト数、品質スコアを監視するための構築済みチャート。(2026-01-29)
- MemAlign Judge Optimizer: フィードバックから評価ガイドラインを学習し、judgeの精度を向上させるアルゴリズム。(2026-01-29)
- Judge Builder UI: カスタムLLM judgeプロンプトを作成、テスト、エクスポートするためのビジュアルインターフェース。(2026-01-29)
- Continuous Online Monitoring: 本番環境の入力トレースに対してLLM judgeを自動的に実行。(2026-01-29)
- Distributed Tracing: コンテキスト伝播を使用して、複数のサービスにわたるリクエストを追跡。(2026-01-29)

| カテゴリ | 評価 | サマリー |
|---|---|---|
| Core Observability | ●●● | 分散システムや複雑なエージェント実行への深い可視性を備えた、堅牢でOpenTelemetry互換のTracingを提供。 |
| Agent / RAG Observability | ●●● | セッション、ツール使用、多段階の推論専用のビューを備えた、エージェントワークフローの強力なサポート。 |
| Evaluation Integration | ●●● | ビジュアルJudge Builder、自動最適化（MemAlign）、継続的なオンラインモニタリングを備えた包括的な評価スイート。 |
| Monitoring & Metrics | ●●● | エージェントのパフォーマンス、コスト、品質のための構築済み自動Dashboardと、リアルタイムモニタリング機能を提供。 |
| Experiment / Improvement Loop | ●●● | プロンプト、モデル、データセットの強力なバージョニングに加え、本番環境での継続的な評価を備えた優れた実験ループ。 |
| DevEx / Integration | ●●● | 幅広いフレームワークサポート、AIコーディングアシスタント、PythonおよびTypeScript向けの堅牢なSDKを備えた、非常に開発者フレンドリーな設計。 |
| Enterprise & Security | ●●● | 新しいマルチワークスペース組織サポートを備えたエンタープライズ対応。ただし、セルフホスティングにはインフラ管理が必要。 |


---

### Arize Phoenix

**概要**: Arize Phoenixは、LLMアプリケーションの実験、トラブルシューティング、継続的な改善のために設計された、オープンソースのAI ObservabilityおよびEvalプラットフォームです。OpenTelemetry/OpenInferenceを介した堅牢なTracing、包括的なLLM-as-a-judge評価機能、本番トレースと評価データセット間のシームレスなデータ移行ワークフローを提供します。

**強み**:
- 柔軟なセルフホストオプション（Docker/K8s）を備えた強力なオープンソース基盤
- 特化型エージェント評価（ツール選択/呼び出し）を含む包括的な評価スイート
- CLIやAIコーディングアシスタントのサポートを通じた深い開発者ワークフロー統合
- 本番トレースを評価データセットに変換するシームレスなワークフロー
- 最新のLLMフレームワーク（LlamaIndex, LangChain, DSPy）およびプロバイダーへの幅広いサポート

**弱み**:
- 提供されたドキュメント内に明示的なPIIマスキングや墨消し機能の記載がない
- 監査ログ機能の詳細が、他のエンタープライズ機能に比べて明示されていない
- メモリTracingは会話履歴を通じてサポートされているが、ツールTracingに比べて専用の状態可視化が欠けている

**最新のアップデート**:
- OpenAI Responses API Type Support: PlaygroundおよびカスタムプロバイダーでのOpenAI APIタイプ（Chat Completions vs Responses）の選択をサポート。(2026-02-12)
- Dataset Evaluators: 実験中にサーバー側で自動実行するために、評価器をデータセットに直接アタッチ。(2026-02-12)
- Custom Providers for Playground: Playgroundやプロンプトで再利用可能な、カスタムAIプロバイダー（OpenAI, Azure, Anthropicなど）の集中構成。(2026-02-11)
- Claude Opus 4.6 Support: 拡張思考パラメータをサポートしたAnthropicのClaude Opus 4.6モデルのサポートを追加。(2026-02-09)
- Tool Selection & Invocation Evaluators: エージェントが正しいツールを選択し、有効なパラメータで呼び出したかを評価する新しい評価器。(2026-01-31)
- Configurable Email Extraction: JMESPathを使用したOAuth2プロバイダーからのカスタムメール抽出のサポート。(2026-01-28)
- CLI Commands for Prompts/Datasets: プロンプト、データセット、実験を管理するためのCLIサポート（AIアシスタントへのパイプ渡しを含む）。(2026-01-22)
- Dataset Creation from Traces: 双方向リンクのためのスパンの関連付けを維持したまま、本番トレースをデータセットに変換。(2026-01-21)
- Export Annotations with Traces: 手動ラベルや評価スコアを含むトレースをエクスポートするためのCLIサポート。(2026-01-19)
- CLI Terminal Access for AI Assistants: AIコーディングアシスタント（Cursor, Windsurf）がPhoenixのデータをクエリできるように設計されたCLI機能。(2026-01-17)

| カテゴリ | 評価 | サマリー |
|---|---|---|
| Core Observability | ●●● | OpenInferenceに基づいて構築された包括的なTracingスイートを提供し、ネイティブなリプレイ機能を備え、実行フロー、レイテンシ、コストへの深い可視性を提供。 |
| Agent / RAG Observability | ●●● | ツール選択と呼び出しのための特定の評価器を備え、エージェントのObservabilityに優れる。また、RAG検索Tracingや多段階推論分析も強力にサポート。 |
| Evaluation Integration | ●●● | トレースとデータセットの間の密接なループ、広範なLLM-as-a-judgeサポート、自動および人間による評価の両方のツールを備えた主要な柱。 |
| Monitoring & Metrics | ●●● | コスト、レイテンシ、エラーに関する不可欠なモニタリングDashboardを提供。ツール使用の正確性など、エージェントの行動に関する特化型メトリクスも備える。 |
| Experiment / Improvement Loop | ●●● | プロンプトのバージョニング、実験トラッキング、テストのために本番トラフィックからデータセットを直接キュレートする機能により、強力な改善ループを促進。 |
| DevEx / Integration | ●●● | 機能豊富なCLI、幅広いSDKサポート、人気のLLMフレームワークやオーケストレーションツールとの深い統合を備えた優れた開発者体験。 |
| Enterprise & Security | ●●○ | エンタープライズデプロイに適した強力なセルフホスティングとアクセス制御機能を備えているが、PIIマスキングや監査ログなどの特定のコンプライアンス機能は詳細がない。 |


---