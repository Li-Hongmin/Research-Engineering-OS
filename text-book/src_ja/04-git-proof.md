# Gitは「コードの保存」のためではなく、「履歴の証明」のためにある

![插图](../images/04_git_timeline.png)


## ストーリー：査読コメントで再現を求められたが、当時のコードが見つからない

![04 04 reviewer crisis](../images/comics/04_04_reviewer_crisis.png)

![Git侦探](../images/comics/04_git_detective.png)

論文の投稿から3ヶ月後、査読結果が返ってきました。そのうちの一つのコメントにはこう書かれていました：「コードとデータを提供してください。表3の結果を再現したいと考えています。」

あなたは嫌な予感がして、慌ててコードリポジトリを開きました。しかし、目の前の光景に背筋が凍りつきました：

- Gitの履歴には数えるほどのコミットしかありません："initial commit", "update", "fix bug", "final version"。
- 論文の結果は3ヶ月前に出したもので、どのバージョンのコードを使ったかもう覚えていません。
- コードディレクトリには複数のバージョンの実験スクリプトが混在しています：`train.py`, `train_v2.py`, `train_final.py`……どれを使ったのか確信が持てません。
- さらに悪いことに、最近の新しい実験のためにモデルのコードを大幅に変更しており、現在のバージョンでは論文の数字が出せないことに気づきました。

あなたは苦渋の決断でこう返信するしかありませんでした：「現在コードを整理中です。できるだけ早く提供します。」そして、記憶、チャットログ、実験ノートから当時のコードの状態をつなぎ合わせるという、苦痛に満ちた「考古学作業」を始めることになったのです。

**この光景に見覚えはありませんか？**

## なぜ「とりあえずコミット」ではあなたを救えないのか

多くの人がGitを使っているつもりになっていますが、実際にはGitを単なる「クラウドストレージ」として扱っています：

- 大量のコードを変更し、最後にまとめてコミットし、メッセージには適当に "update" と書く。
- ブランチを一度も使わず、すべての変更を main に積み上げる。
- 実験が終わってからコミットを思い出すが、その時にはすでにコードをさらに変更してしまっている。
- コミット履歴から「どのバージョンがどの実験結果に対応しているか」が分からない。

このような使い方の問題点は、**Gitの最も核心的な価値である「履歴の証明ツール」としての能力を失っていること**にあります。

エンジニアリング開発において、Gitの主な役割はコラボレーションとロールバックです。しかし研究において、Gitの核心的な価値は**証明**にあります：

- その結果がどのバージョンのコードで実行されたかを証明する。
- 論文の各実験に、対応するコードバージョンが存在することを証明する。
- 任意の履歴バージョンに戻り、同じ結果を再作成できることを証明する。

## 研究におけるGit使用の罠

### 罠1：コミットの粒度が大きすぎて、重要な変更が見つからない

![04 05 commit too big](../images/comics/04_05_commit_too_big.png)

**症状**：1つのコミットに10個以上のファイルの変更が含まれており、データ処理、モデル構造、トレーニングプロセスなど多岐にわたる変更が含まれている。コミットメッセージには単に "improve model" とだけ書かれている。

**結果**：
- 指標の変化がどの変更によって引き起こされたのか特定できない。
- 特定の誤った変更だけをロールバックしたいと思っても、個別に修正を取り消せない。
- 数ヶ月後、そのコミットが何をしたものか全く思い出せない。

**正しい方法**：
- 各コミットには**1つの論理的な変更**のみを含める。
- コミットメッセージには「何を変更したか」だけでなく「なぜ変更したか」を明確に書く。
- 「アトミック性の原則」に従う：各コミットは常にコードが動作する状態であるべき。

### 罠2：実験とコード変更のタイミングのズレ

![04 06 experiment time mismatch](../images/comics/04_06_experiment_time_mismatch.png)

**症状**：先にコードを変更して実験を行い、結果が良かったので2日後にコミットする。あるいは、コミットした後に一時的にパラメータを変更して再実行する。

**結果**：
- 結果を生み出したコードバージョン（コミット）が、実際には一致していない。
- 他の人（未来の自分を含む）がコミットハッシュを使って再現しようとしても、結果が一致しない。
- 査読者に再現を求められた際、正確なコードバージョンが見つからない。

**正しい方法**：
- **先にコミットし、その後に実験を実行する。**
- 各実験の run.json に、その時のコミットハッシュと dirty 状態を記録する。
- 一時的にコードを変更した場合は、改めてコミットするか、run 記録に変更内容（dirty）を注記する。

### 罠3：不適切なブランチ利用によるメインラインの混乱

![04 07 branch chaos](../images/comics/04_07_branch_chaos.png)

**症状**：すべての実験を main ブランチで行い、試行錯誤的な変更と安定したコードが混在している。あるいは、大量のブランチを作成したが一度も整理せず、ブランチ間の関係が混乱している。

**結果**：
- main ブランチが不安定になり、試行錯誤的なコードで溢れる。
- 「論文再現バージョン」を見つけようとしたとき、どのブランチを使えばいいか分からない。
- ブランチが多すぎて、チームメンバーがどのブランチを基に新しい作業を始めるべきか分からない。

## 研究に適したGitブランチ戦略

![分支策略](../images/comics/04_branch_strategy.png)

エンジニアリングプロジェクトとは異なり、研究プロジェクトのブランチ戦略には二つのニーズのバランスが必要です：

- **安定性**：論文の結果は、清潔で安定したコードバージョンによって支えられている必要がある。
- **探索性**：新しいアイデアは素早く試行錯誤する必要があり、プロセスに縛られてはならない。

### 推奨されるブランチ構造

    main (または stable)：
      - 検証済みの変更のみを受け入れる
      - 各マージは必ずDoDチェック（第5章参照）を通過させる
      - 常に論文結果を再現できる状態を維持する

    exp/<hypothesis-name>：
      - 実験仮説ごとに1つのブランチを作成
      - 命名を明確にする：exp/attention-ablation, exp/data-augmentation
      - 短命なブランチ：検証が終わればマージするか削除する
      - 「汚い」状態での素早いイテレーションを許容する

    archive/<paper-version>：
      - 論文投稿、発表などの重要な節目のアーカイブ用ブランチ
      - main ブランチから作成し、二度とマージし戻さない
      - 永久に保持し、追跡可能性を確保する

### 典型的なワークフロー

#### シナリオ1：新しい仮説の検証

1.  main から新しいブランチを作成：`git checkout -b exp/new-loss-function`
2.  ブランチ上で素早くイテレーションし、試行錯誤する（コミットは適当でも良い）。
3.  有望な結果が得られたら、コードを整理する。
4.  規範的な実験記録（config + run.json）を作成する。
5.  main へマージする：`git checkout main && git merge exp/new-loss-function`
6.  実験ブランチを削除する：`git branch -d exp/new-loss-function`

#### シナリオ2：論文投稿

1.  main ブランチのすべての論文実験が再現可能であることを確認する。
2.  アーカイブ用ブランチを作成：`git checkout -b archive/icml2026-v1`
3.  main 上でタグを打つ：`git tag -a paper-icml2026-v1 -m "ICML 2026 submission version"`
4.  タグをプッシュする：`git push origin paper-icml2026-v1`

#### シナリオ3：複数の方向を並行して探索

1.  同時に複数の実験ブランチを作成：
    - `exp/architecture-search`
    - `exp/data-augmentation`
    - `exp/loss-function`
2.  各ブランチを独立して進め、互いに干渉しないようにする。
3.  各ブランチの実験産物は独立した run_id で管理する。
4.  価値のある変更を一つずつ main へマージする。
5.  価値のないブランチはそのまま削除する。

## タグでマイルストーンを記録する：論文の結果を永久に追跡可能にする

![04 08 tag milestone](../images/comics/04_08_tag_milestone.png)

タグ（Tag）はGitの中で過小評価されている機能の一つです。研究プロジェクトにおいて、タグの価値は以下の点にあります：

- 論文の各重要なバージョンに恒久的な印を付ける。
- main ブランチが進化し続けても、正確に過去のバージョンに戻れる。
- 引用や再現に便利な、明確なバージョン名を提供する。

### 推奨されるタグ命名規則

    # 論文バージョン
    paper-<venue>-<version>
    例：paper-icml2026-v1, paper-icml2026-revision

    # 実験グループ
    exp-<experiment-name>
    例：exp-ablation-study, exp-baseline-comparison

    # 主要な結果
    result-<result-name>
    例：result-table3-main, result-fig2-comparison

    # マイルストーン
    milestone-<description>
    例：milestone-first-sota, milestone-reproducible-baseline

### タグ使用の実践

#### 論文の各重要実験にタグを打つ：

![提交作为证据](../images/comics/04_commit_evidence.png)

    # 主要な実験が終わったらすぐにタグを打つ
    git tag -a result-main-experiment -m \
      "Main results reported in Table 2, config: configs/main.yaml"

    # タグメッセージに重要な情報を記録する
    git tag -a result-ablation-study -m \
      "Ablation study results (Table 3)
       Run IDs: 2026-02-01_1030_ablation_*
       Config: configs/ablation_*.yaml
       Key finding: attention mechanism contributes 5% improvement"

#### 再現時に直接タグに切り替える：

    # 実験関連のタグをすべて確認
    git tag -l "result-*"

    # 特定の実験バージョンに切り替え
    git checkout result-main-experiment

    # 実験を再現
    make reproduce CONFIG=configs/main.yaml

## 実験産物はGitに入れない：.gitignore でリポジトリを清潔に保つ

![04 09 gitignore clean](../images/comics/04_09_gitignore_clean.png)

**核心原則**：Gitはソースコードと設定を管理し、実験産物は管理しない。

### Gitにコミットすべきでないもの

- **モデルの重み**：通常非常に大きく（数百MBから数GB）、専用のモデル管理ツール（DVC, Git LFS）やクラウドストレージを使用します。
- **トレーニングログ**：`outputs/` 以下のすべての実行産物。run_id ごとに整理した後にアーカイブまたは削除します。
- **中間データ**：キャッシュされた特徴量、前処理結果などは、再生成可能であるべきです。
- **データセット**：元データは通常外部で管理し、`data/` には小規模なサンプルやデータポインタ（マニフェスト、ダウンロードスクリプト）のみを置きます。
- **仮想環境**：`venv/`, `.conda/` などのディレクトリ。`requirements.txt` や `environment.yaml` で代用します。

### 推奨される .gitignore テンプレート

    # Python
    __pycache__/
    *.py[cod]
    *$py.class
    *.so
    .Python

    # 仮想環境
    venv/
    env/
    .conda/

    # 実験産物
    outputs/
    runs/
    checkpoints/
    *.pt
    *.pth
    *.ckpt
    *.h5

    # データ（小規模サンプル以外）
    data/raw/
    data/processed/
    *.csv
    *.parquet

    # ログ
    *.log
    logs/
    wandb/

    # 一時ファイル
    .DS_Store
    *.swp
    *.swo
    *~

    # IDE
    .vscode/
    .idea/
    *.iml

    # 例外：小規模サンプルデータと設定は保持
    !data/samples/
    !configs/

## よくある質問と解決策

### Q1：コードをすでに大幅に変更してしまった。どう修復すればいい？

リポジトリの履歴がすでに混沌としている場合、「履歴を書き換える」ことはお勧めしません（Git rebaseに非常に精通している場合を除く）。推奨される方法は以下の通りです：

1.  **基準点を設定する**：現在の状態にタグを打ちます：`git tag baseline-before-cleanup`
2.  **今この瞬間から規範化する**：
    - すべての新しい実験で独立したブランチを使う。
    - 各コミットのアトミック性を維持する。
    - 重要な結果が出たら即座にタグを打つ。
3.  **過去の問題を段階的に修復する**：
    - 論文の重要な実験に対応するコードバージョンを特定し、後からタグを打つ。
    - READMEやドキュメントに「履歴バージョンと実験の対応関係」を記録する。
    - 新しい実験には規範的なプロセスを適用し、古い実験については可能な範囲で追跡する。

### Q2：チームで協力する際、どうやってブランチ戦略を統一すればいい？

- **READMEに明記する**：ブランチの命名規則、タグの使用方法をドキュメント化します。
- **保護ルールを設定する**：GitHub/GitLabなどで main ブランチの保護を設定し、直接の push を禁止し、PR/MR を必須にします。
- **コードレビュー（Code Review）**：main へのマージ前に、DoD（第5章）を満たしているか、完全な実験記録があるかをチェックします。
- **定期的な整理**：週に一度のミーティングで、不要な実験ブランチを一斉に削除し、重要なタグをアーカイブします。

### Q3：「dirty」な状態の実験はどう扱えばいい？

一時的にコードを変更して実験を行い、コミットする時間がなかった。これが「dirty」な状態です。

**記録戦略**：
- run.json に `"git_dirty": true` と記録する。
- 同時に diff も記録する：`git diff > outputs/<run_id>/changes.patch`
- run.md に一時的な変更内容とその理由を注記する。

**事後修復**：
- 結果に価値がある場合は、直ちに変更をコミットしてタグを打つ。
- 単なる一時的な試行であれば、run.md に記録を残すだけで、無理にコミットしなくても良い。

## 実戦事例：混乱から明晰なGit履歴へ

### 重構前（反面教材）

    * a3f2d1c (HEAD -> main) update
    * f8d9e0a fix
    * 1b2c3d4 add new feature
    * 9e8d7f6 initial commit

履歴から有用な情報を何も読み取ることができず、論文の実験に対応するバージョンも見つかりません。

### 重構後（グッドサンプル）

    * d1e2f3g (tag: paper-icml2026-v1, main) Merge exp/final-ablation
    |           Paper results ready for submission
    |\
    | * c4d5e6f (exp/final-ablation) Add ablation study for attention
    | * b3c4d5e Configure ablation experiments
    |/
    * a1b2c3d (tag: result-main-experiment) Main experiment: achieve 95.2% accuracy
               Run ID: 2026-02-01_1030_main_run
               Config: configs/main_experiment.yaml
    * 9a8b7c6 (tag: milestone-baseline) Establish reproducible baseline
               All baseline experiments validated
    * 8f7e6d5 Fix data preprocessing bug in train/val split
    * 7e6d5c4 Add comprehensive smoke test
    * 6d5c4b3 Refactor data loading module

履歴が明快で、各重要な節目に記印があり、いつでも過去に遡ることができます。

## 10分アクション：現在のプロジェクトにGitのベースラインを築く

もし今すぐ一つだけ行うなら：あなたのプロジェクトに明確なGitのベースラインを築いてください。

1.  **現在の状態を確認する**：
          git status
          git log --oneline -10
2.  **未コミットの変更がある場合、処理を決定する**：
    - 価値のある変更：整理してコミットし、明確なメッセージを書く。
    - 一時的な試行：run.md に記録し、`git stash` で避ける。
    - 不要な変更：`git checkout .` で元に戻す。
3.  **現在の安定版にベースラインタグを打つ**：
          git tag -a baseline-$(date +%Y%m%d) -m \
            "Baseline before implementing git workflow"
4.  **規範的な .gitignore を設定する**：
          # 前述のテンプレートを使用
          curl -o .gitignore <テンプレートへのリンク>
          # または手動で作成
          git add .gitignore
          git commit -m "Add comprehensive .gitignore for research project"
5.  **ブランチ命名規則を書き留める**：README.md に "Git Workflow" セクションを追加し、以下を記述します：
    - main ブランチの用途
    - exp/ ブランチの命名規則
    - タグの使用方法

今この瞬間から、すべての新しい実験において、ブランチとタグを規範に従って使用し、Gitを真の「履歴の証明ツール」にしていきましょう。
