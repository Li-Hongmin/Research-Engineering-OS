# Git 不是用来"保存代码"，是用来"证明历史"

![插图](images/04_git_timeline.png)


## 故事引入：审稿意见要求复现，你却找不回当时的代码

论文提交三个月后，审稿意见回来了。其中一条写得很直接："请提供代码和数据，我们想要复现表3的结果。"

你心里一紧------赶紧打开代码仓库。但眼前的景象让你后背发凉：

- Git 历史只有寥寥几次提交："initial commit"、"update"、"fix bug"、"final version"；

- 论文里的结果是三个月前跑的，你已经记不清用的是哪个版本的代码；

- 代码目录里有多个版本的实验脚本：`train.py`、`train_v2.py`、`train_final.py`，你不确定用的是哪个；

- 更糟的是，你发现最近为了新实验已经大改了模型代码，现在的版本跑不出论文里的数字。

你只能硬着头皮回复："我们正在整理代码，会尽快提供。"然后开始痛苦的"考古工作"------试图从记忆、聊天记录、实验笔记里拼凑出当时的代码状态。

**这个场景你熟悉吗？**

## 为什么"随手 commit"救不了你

很多人以为自己在用 Git，但实际上只是把 Git 当成了"云盘"：

- 改了一堆代码，最后一起 commit，message 随便写个"update"；

- 从不用分支，所有改动都在 main 上叠加；

- 实验跑完了才想起来 commit，这时候代码已经又改了；

- commit 历史里找不到"哪个版本对应哪个实验结果"。

这种用法的问题在于：**你失去了 Git 最核心的价值------作为"历史证明工具"的能力。**

在工程开发中，Git 的主要作用是协作和回滚。但在研究中，Git 的核心价值是**证明：**

- 证明这个结果是用哪个版本的代码跑出来的；

- 证明论文里的每个实验都有对应的代码版本；

- 证明你可以回到任意历史版本，重新跑出相同的结果。

## 研究中的 Git 使用陷阱

### 陷阱 1：commit 粒度太大，找不到关键改动

**症状：**一个 commit 包含了十几个文件的改动，涉及数据处理、模型结构、训练流程等多个方面。commit message 只写了"improve model"。

**后果：**

- 无法定位某个指标变化是由哪个改动引起的；

- 想要回滚某个错误改动，却发现无法单独撤销；

- 几个月后再看，完全想不起来这个 commit 做了什么。

**正确做法：**

- 每个 commit 只包含**一个逻辑改动**；

- commit message 写清楚"改了什么"和"为什么改"；

- 遵循"原子性原则"：每个 commit 都应该让代码保持可运行状态。

### 陷阱 2：实验和代码改动时间错位

**症状：**先改代码跑实验，结果不错，过了两天才 commit；或者 commit 之后又临时改了几个参数重跑。

**后果：**

- 产生了结果的代码版本（commit）其实对不上；

- 别人（包括未来的你）拿着 commit hash 复现，结果对不上；

- 审稿人要求复现时，你根本找不到准确的代码版本。

**正确做法：**

- **先 commit，再跑实验**；

- 每次实验的 run.json 记录当时的 commit hash 和 dirty 状态；

- 如果临时改了代码，要么重新 commit，要么在 run 记录里注明 dirty 修改内容。

### 陷阱 3：分支使用不当，主线混乱

**症状：**所有实验都在 main 分支上做，各种尝试性改动和稳定代码混在一起；或者创建了很多分支但从不清理，分支之间关系混乱。

**后果：**

- main 分支不稳定，充斥着各种试验性代码；

- 想要找到"论文复现版本"时，不知道该用哪个分支；

- 分支太多导致团队成员不知道该基于哪个分支开展新工作。

## 适合研究的 Git 分支策略

与工程项目不同，研究项目的分支策略需要平衡两个需求：

- **稳定性：**论文结果必须有一个干净、稳定的代码版本支撑；

- **探索性**：新想法需要快速试错，不能被流程束缚。

### 推荐的分支结构

    main (或 stable)：
      - 只接受验证通过的改动
      - 每个 merge 必须经过 DoD 检查（见第5章）
      - 确保任何时候都可以复现论文结果

    exp/<hypothesis-name>：
      - 每个实验假设一条分支
      - 命名要清晰：exp/attention-ablation, exp/data-augmentation
      - 短命分支：验证完就合并或删除
      - 允许"脏"的快速迭代

    archive/<paper-version>：
      - 论文提交、发表等重要节点的存档分支
      - 从 main 分支创建，不再合并回去
      - 永久保留，确保可追溯

### 典型工作流程

#### 场景 1：验证新假设

1.  从 main 创建新分支：`git checkout -b exp/new-loss-function`

2.  在分支上快速迭代、试错，commit 可以随意

3.  跑出有希望的结果后，整理代码

4.  创建规范的实验记录（config + run.json）

5.  合并回 main：`git checkout main && git merge exp/new-loss-function`

6.  删除实验分支：`git branch -d exp/new-loss-function`

#### 场景 2：论文提交

1.  确保 main 分支所有论文实验都可复现

2.  创建存档分支：`git checkout -b archive/icml2026-v1`

3.  在 main 上打 tag：`git tag -a paper-icml2026-v1 -m "ICML 2026 submission version"`

4.  推送 tag：`git push origin paper-icml2026-v1`

#### 场景 3：并行探索多个方向

1.  同时创建多个实验分支：

- `exp/architecture-search`

- `exp/data-augmentation`

- `exp/loss-function`

2.  各分支独立推进，互不干扰

3.  每个分支的实验产物用独立的 run_id 管理

4.  有价值的改动逐个合并回 main

5.  无价值的分支直接删除

## 用 Tag 标记里程碑：让论文结果永久可追溯

Tag 是 Git 中被严重低估的功能。对于研究项目，tag 的价值在于：

- 为论文的每个关键版本打上永久标记；

- 即使 main 分支继续演进，也能精确回到历史版本；

- 提供清晰的版本命名，便于引用和复现。

### 推荐的 Tag 命名规范

    # 论文版本
    paper-<venue>-<version>
    例如：paper-icml2026-v1, paper-icml2026-revision

    # 实验组
    exp-<experiment-name>
    例如：exp-ablation-study, exp-baseline-comparison

    # 主要结果
    result-<result-name>
    例如：result-table3-main, result-fig2-comparison

    # 里程碑
    milestone-<description>
    例如：milestone-first-sota, milestone-reproducible-baseline

### Tag 使用实践

#### 为论文的每个重要实验打 tag：

    # 跑完主实验后立即打 tag
    git tag -a result-main-experiment -m \
      "Main results reported in Table 2, config: configs/main.yaml"

    # 记录关键信息在 tag message 里
    git tag -a result-ablation-study -m \
      "Ablation study results (Table 3)
       Run IDs: 2026-02-01_1030_ablation_*
       Config: configs/ablation_*.yaml
       Key finding: attention mechanism contributes 5% improvement"

#### 复现时直接切换到 tag：

    # 查看所有实验相关的 tag
    git tag -l "result-*"

    # 切换到特定实验版本
    git checkout result-main-experiment

    # 复现实验
    make reproduce CONFIG=configs/main.yaml

## 实验产物不进 Git：用 .gitignore 保持仓库干净

**核心原则：**Git 管理源代码和配置，不管理实验产物。

### 什么不应该提交到 Git

- **模型权重：**通常很大（几百 MB 到几 GB），用专门的模型管理工具（如 DVC、Git LFS、或云存储）。

- **训练日志：**outputs/ 下的所有运行产物，按 run_id 组织后归档或清理。

- **中间数据：**缓存的特征、预处理结果等，应该可重新生成。

- **数据集：**原始数据通常由外部管理，只在 data/ 里放小样本或数据指针（清单、下载脚本）。

- **虚拟环境**：venv/、.conda/ 等目录，用 requirements.txt 或 environment.yaml 代替。

### 推荐的 .gitignore 模板

    # Python
    __pycache__/
    *.py[cod]
    *$py.class
    *.so
    .Python

    # 虚拟环境
    venv/
    env/
    .conda/

    # 实验产物
    outputs/
    runs/
    checkpoints/
    *.pt
    *.pth
    *.ckpt
    *.h5

    # 数据（除非是小样本）
    data/raw/
    data/processed/
    *.csv
    *.parquet

    # 日志
    *.log
    logs/
    wandb/

    # 临时文件
    .DS_Store
    *.swp
    *.swo
    *~

    # IDE
    .vscode/
    .idea/
    *.iml

    # 例外：保留小样本数据和配置
    !data/samples/
    !configs/

## 常见问题与解决方案

### Q1：代码已经改了很多，怎么补救？

如果你的仓库历史已经很混乱，不要试图"重写历史"（除非你非常熟悉 Git rebase）。推荐的做法：

1.  **设定基准点：**在当前状态打一个 tag：`git tag baseline-before-cleanup`

2.  **从现在开始规范：**

- 每个新实验使用独立分支

- 每个 commit 保持原子性

- 重要结果立即打 tag

3.  **历史问题逐步修复：**

- 识别出论文关键实验对应的代码版本，补打 tag

- 在 README 或文档里记录"历史版本对应关系"

- 新实验都用规范流程，旧实验尽力追溯

### Q2：团队协作时如何统一分支策略？

- **写进 README：**把分支命名规范、tag 使用方法写进文档。

- **设定保护规则：**在 GitHub/GitLab 上设置 main 分支保护，禁止直接 push，必须通过 PR/MR。

- **Code Review：**合并到 main 前，检查是否满足 DoD（第5章），是否有完整的实验记录。

- **定期清理：**每周一次会议，集体清理无用的实验分支，归档重要的 tag。

### Q3：如何处理"dirty" 状态的实验？

有时你临时修改了代码跑实验，还没来得及 commit，这就是"dirty"状态。

**记录策略：**

- 在 run.json 里记录 `"git_dirty": true`

- 同时记录 diff：`git diff > outputs/<run_id>/changes.patch`

- 在 run.md 里注明临时改动的内容和原因

**事后补救：**

- 如果结果有价值，立即把改动 commit 并打 tag

- 如果只是临时试验，在 run.md 里记录即可，不必 commit

## 实战案例：从混乱到清晰的 Git 历史

### 重构前（反面教材）

    * a3f2d1c (HEAD -> main) update
    * f8d9e0a fix
    * 1b2c3d4 add new feature
    * 9e8d7f6 initial commit

无法从历史看出任何有用信息，所有论文实验找不到对应版本。

### 重构后（正面示例）

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

清晰的历史，每个重要节点都有标记，可以随时回溯。

## 10 分钟动作：为当前项目建立 Git 基线

如果你现在只做一件事：为你的项目建立一个清晰的 Git 基线。

1.  **检查当前状态：**

          git status
          git log --oneline -10

2.  **如果有未提交改动，决定处理方式：**

- 有价值的改动：整理后 commit，写清楚 message

- 临时试验：记录到 run.md，然后 `git stash`

- 无用改动：`git checkout .` 撤销

3.  **为当前稳定版本打基线 tag：**

          git tag -a baseline-$(date +%Y%m%d) -m \
            "Baseline before implementing git workflow"

4.  **设置规范的 .gitignore：**

          # 使用前面提供的模板
          curl -o .gitignore <模板链接>
          # 或手动创建
          git add .gitignore
          git commit -m "Add comprehensive .gitignore for research project"

5.  **写下分支命名规范**：在 README.md 里添加一节"Git Workflow"，记录：

- main 分支用途

- exp/ 分支命名规范

- tag 使用方法

从现在开始，每个新实验都按规范使用分支和 tag，让 Git 真正成为你的"历史证明工具"。
