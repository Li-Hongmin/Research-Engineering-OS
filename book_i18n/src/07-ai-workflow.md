# AI 编码助手加入后，工作流必须升级

![插图](images/07_ai_collaboration.png)


## 故事引入：当 AI 从提速器变成地雷制造机

你用了一个月时间，在 Copilot 的帮助下快速搭建了一个复杂的多模态学习框架。代码生成速度惊人------以前一天能写 200 行，现在半天就能写 500 行。你觉得自己的生产力翻了几倍。

但在准备论文的前一周，问题开始集中爆发：

#### 问题 1：隐藏的 Bug

你在测试一个边界情况时，发现模型输出了 NaN。追溯代码，发现是一个数据预处理函数有问题------它在某些罕见情况下会除以零。这个函数是 Copilot 生成的，你当时只检查了"能跑"，没有仔细审查边界条件。

#### 问题 2：不一致的实现

你发现数据增强在训练和评估时的实现不一致：训练用的是 Copilot 生成的版本 A，评估用的是你后来手写的版本 B，两者在归一化方式上有微妙差异。这导致训练和测试的分布不匹配，性能受到影响。

#### 问题 3：过度复杂的架构

为了"优雅"，你让 Copilot 帮你设计了一个高度抽象的架构，有很多层抽象类和工厂模式。现在你需要快速修改一个功能，却发现要改动 5 个文件，因为逻辑分散在各个抽象层里。

#### 问题 4：缺失的验证

你意识到很多 Copilot 生成的代码都没有测试覆盖。你一直依赖"跑通就行"，从没系统验证过边界情况、错误处理、数据一致性。现在想补测试，却发现代码耦合度太高，难以单独测试。

#### 悔悟时刻

你不得不停下所有新功能开发，花了一周时间：

- 审查所有 AI 生成的代码，找出隐藏问题；

- 统一不一致的实现；

- 简化过度设计的架构；

- 补充缺失的测试和验证。

你意识到：**AI 编码助手不是问题，问题是你的工作流没有跟上。**

在 AI 加入之前，你的代码量少，错误少，可以靠记忆和经验把控质量。但现在代码量暴增，而你的验证机制还停留在"手工审查"阶段，这个缺口会越来越大。

## AI 编码的三大陷阱

### 陷阱 1：生成速度超过验证能力

**症状：**AI 一分钟生成 100 行代码，你觉得"看起来没问题"就接受了。但你其实没有仔细检查边界条件、错误处理、性能影响。

**后果：**

- 埋下大量隐藏 bug，在关键时刻暴露；

- 代码库充斥着"能跑但不健壮"的实现；

- 重构成本远超一开始就做对的成本。

**本质问题：**验证机制没有升级，还停留在"手工审查"阶段。

### 陷阱 2：重复生成导致不一致

**症状：**你需要类似功能时，让 AI 重新生成，而不是复用现有代码。结果项目里有多个"类似但不完全相同"的实现。

**后果：**

- 修改一个逻辑需要改多处，容易遗漏；

- 不同实现可能有微妙差异，导致结果不一致；

- 代码库膨胀，维护成本暴增。

**本质问题：**没有区分"核心库代码"和"一次性胶水代码"（回顾第3章）。

### 陷阱 3：过度依赖"顺手改一下"

**症状：**在让 AI 实现一个功能时，你顺便让它"把这个也改了"、"把那个也优化了"。一个 commit 包含了十几个文件的改动。

**后果：**

- 无法定位哪个改动引起了问题；

- 想要回滚时发现"牵一发动全身"；

- 代码历史混乱，无法追溯逻辑演进。

**本质问题：**改动不再是"可验证的最小单元"（回顾第1章）。

## 升级后的工作流：把 AI 当成"快速试错的初级程序员"

**核心理念：**AI 是助手，不是替代品。它的优势是快速生成初稿，你的责任是验证、整合、把关。

把 AI 编码看作两阶段过程：

1.  **生成阶段：**AI 快速产出初稿（快速、粗糙、允许有问题）；

2.  **验证阶段：**人类审查、测试、重构（慢速、严格、确保质量）。

**关键原则：**生成可以快，但上线必须慢。

### 原则 1：每次只做一个可验证的改动

**操作建议：**

- 每次让 AI 生成的代码不超过 200 行 diff；

- 每次改动只涉及一个逻辑功能（如"添加数据增强"、"修复 NaN bug"）；

- 改动必须能独立验证（有对应的测试或实验）。

**实践案例：**

反例：

    # 一次改动包含：
- 修改数据加载逻辑
- 添加新的模型层
- 调整训练超参数
- 重构评估代码
- 更新配置文件

结果：如果实验结果变差，你无法确定是哪个改动导致的。

正例：

    # 改动 1（独立 commit）：
- 修改数据加载逻辑
- 测试：数据加载测试通过，输出 shape 正确

    # 改动 2（独立 commit）：
- 添加新的模型层
- 测试：模型前向传播测试通过

    # 改动 3（独立 commit）：
- 运行实验，对比新模型和 baseline
- 记录：run_id, metrics, 结论

### 原则 2：每次改动附带"如何验证"

**操作建议：**

在让 AI 生成代码时，同时要求它生成验证代码。

示例提示词：

    请实现数据增强功能，包括：
1. 实现代码
2. 单元测试（至少覆盖正常情况和边界情况）
3. 使用示例
4. 可能的风险点

**验证清单（每次改动后检查）：**

- 代码能运行（不崩溃）

- 输出符合预期（shape、数值范围、数据类型）

- 边界情况处理正确（空输入、极端值、错误输入）

- 不影响现有功能（回归测试通过）

- 有测试覆盖（至少 smoke test）

### 原则 3：禁止"顺手重构一大片"

**症状识别：**

危险信号：

- AI 提议："我顺便帮你重构一下这部分代码，让它更优雅"

- 你想："反正都要改，不如一起做了"

- 结果：一个 PR 包含功能添加 + 重构 + bug 修复

**正确做法：**

1.  **先实现功能，后重构：**

          # Step 1: 实现功能（允许粗糙）
          git commit -m "feat: add data augmentation (rough version)"

          # Step 2: 验证功能正确
          pytest tests/test_data_aug.py

          # Step 3: 独立重构（不改功能）
          git commit -m "refactor: clean up data augmentation code"

          # Step 4: 验证重构没有破坏功能
          pytest tests/test_data_aug.py

2.  **重构与功能分离：**

- 功能改动：commit message 用 "feat:" 或 "fix:"

- 重构改动：commit message 用 "refactor:"

- 绝不混在一起

### 原则 4：核心逻辑必须人工审查

**定义"核心逻辑"：**

以下代码不能盲目接受 AI 生成的版本，必须人工仔细审查：

- **数据处理：**数据加载、预处理、划分、增强

- **模型核心：**损失函数、关键模块（注意力、归一化等）

- **评估逻辑：**指标计算、后处理、阈值选择

- **随机性控制：**随机种子设置、随机采样逻辑

- **超参数：**学习率调度、权重衰减、dropout 率

**审查清单：**

- 逻辑正确性（算法实现对吗？）

- 边界条件（空数据、极端值会怎样？）

- 数据一致性（训练和测试逻辑一致吗？）

- 随机性（种子设置正确吗？可复现吗？）

- 性能影响（会不会特别慢？内存会爆吗？）

### 原则 5：先补最小测试，再改核心逻辑

**反面模式：**

    你：Copilot，帮我重构这个数据加载函数
    Copilot：[生成 150 行代码]
    你：看起来不错，接受！
    [一周后发现数据加载有问题，但已经运行了很多实验]

**正确流程：**

    # Step 1: 先为现有代码写测试
    def test_data_loader_current():
        """测试当前数据加载行为"""
        loader = DataLoader(...)
        batch = next(iter(loader))

        assert batch['image'].shape == (32, 3, 224, 224)
        assert batch['label'].shape == (32,)
        assert batch['label'].min() >= 0
        assert batch['label'].max() < num_classes

    # Step 2: 运行测试，确保通过
    pytest tests/test_data_loader.py

    # Step 3: 进行重构
    [Copilot 生成新代码]

    # Step 4: 运行测试，确保行为不变
    pytest tests/test_data_loader.py

    # Step 5: 如果测试失败，修复或回滚

**测试先行的好处：**

- 明确当前行为（作为回归测试基准）

- 快速验证重构（1 分钟而不是 1 小时实验）

- 避免破坏现有功能

- 强制思考"正确的行为是什么"

## AI 规则页（CLAUDE.md）：团队协作的共识

为了在团队中统一 AI 使用规范，建议在项目根目录创建 `CLAUDE.md`（或 `AI_RULES.md`），明确 AI 编码的边界和流程。

### CLAUDE.md 模板

    # AI 编码助手使用规范

    本项目使用 AI 编码助手（如 GitHub Copilot、Claude、GPT）辅助开发。
    为确保代码质量和可维护性，所有 AI 生成的代码必须遵循以下规范。

    ## 核心原则

1. **AI 生成，人类负责：**AI 可以快速产出初稿，但人类必须
       审查、测试、把关。
2. **小步快跑：**每次改动不超过 200 行 diff，必须可独立验证。
3. **测试先行：**核心逻辑改动前，先补充测试；改动后，测试
       必须通过。
4. **禁止顺手重构：**功能改动与重构必须分开 commit。

    ## 操作规范

    ### 1. 每次改动必须附带验证方式

    在 commit message 或 PR 描述里明确：

    ```
如何验证此改动：
- [ ] 运行测试：pytest tests/test_xxx.py
- [ ] 运行实验：python train.py --config xxx
- [ ] 检查输出：输出 shape 应为 [B, C, H, W]
```

    ### 2. 每次改动必须记录风险点

    ```
潜在风险：
- 修改了数据预处理，可能影响数据分布
- 新增了随机操作，需要检查种子设置
- 改动了评估逻辑，需要重新跑 baseline 确认公平性
```

    ### 3. 每次改动必须有回滚策略

    ```bash
回滚策略：
- 如果测试失败：git checkout -- <文件>
- 如果实验结果变差：回退到 commit <hash>
- 如果影响其他功能：回滚并新建 branch 单独调试
```

    ## 禁止的行为

    [NO] **禁止 1：盲目接受大段生成代码**
      - 任何超过 50 行的 AI 生成代码都必须人工逐行审查
      - 核心逻辑（数据、模型、评估）必须特别严格审查

    [NO] **禁止 2：改动太多文件**
      - 单次 commit 不应超过 5 个文件（特殊情况除外）
      - 如果需要改很多文件，拆分成多个 commit

    [NO] **禁止 3：跳过测试直接合并**
      - 任何代码合并到 main 之前，必须通过所有测试
      - 如果没有相关测试，必须先补充测试

    [NO] **禁止 4：在 main 分支直接改动**
      - 所有 AI 生成的代码必须在实验分支上先验证
      - 验证通过后再合并到 main

    ## 必须的行为

    [YES] **必须 1：核心逻辑有测试覆盖**
      - 数据加载、模型核心、评估逻辑必须有单元测试
      - 每次修改核心逻辑后，测试必须通过

    [YES] **必须 2：实验结果可对比**
      - 任何影响结果的改动，必须运行对比实验
      - 记录改动前后的 run_id 和指标对比

    [YES] **必须 3：配置版本同步**
      - 任何影响结果的改动，必须更新对应的 config
      - Config 文件必须 commit 并打 tag

    [YES] **必须 4：文档同步更新**
      - API 改动必须更新文档
      - 新功能必须更新 README 的使用说明

    ## 验收标准（合并到 main 前）

- [ ] 改动不超过 200 行（或经过充分讨论）
- [ ] 所有测试通过
- [ ] 核心逻辑经过人工审查
- [ ] 有清晰的 commit message
- [ ] 附带验证方式、风险点、回滚策略
- [ ] 如影响实验结果，附带对比实验记录

    ## 示例：好的 AI 辅助流程

    ```bash
    # 1. 创建实验分支
    git checkout -b exp/add-mixup

    # 2. 让 AI 生成初稿
    # [Copilot 生成 mixup 数据增强代码]

    # 3. 人工审查和修改
    # - 检查边界条件
    # - 添加类型注解
    # - 确认随机种子处理正确

    # 4. 补充测试
    pytest tests/test_mixup.py

    # 5. 运行对比实验
    make train CONFIG=configs/baseline.yaml  # baseline
    make train CONFIG=configs/mixup.yaml      # with mixup

    # 6. 记录结果
    # outputs/2026-02-01_1030_baseline/run.json
    # outputs/2026-02-01_1100_mixup/run.json

    # 7. 如果结果改进，合并到 main
    git checkout main
    git merge exp/add-mixup

    # 8. 清理实验分支
    git branch -d exp/add-mixup
    ```

    ## 参考资源

- 仓库结构规范：见 README.md "项目结构" 章节
- DoD 清单：见 DoD.md
- 实验记录规范：见 LOGGING.md

---

    **原则总结：AI 让你更快，但不能让你更马虎。**

## 实战案例：AI 辅助的正确打开方式

### 案例 1：添加新模型组件

#### 错误方式：

    你：Copilot，帮我实现一个多头注意力模块
    Copilot：[生成 200 行代码]
    你：看起来不错，接受！直接用在训练里
    [训练崩溃，发现注意力计算有 bug]

#### 正确方式：

    # Step 1: 生成初稿
    你：Copilot，帮我实现一个多头注意力模块，包括：
        - 实现代码
        - 单元测试
        - 使用示例

    # Step 2: 人工审查
- 检查 softmax 前是否有除以 sqrt(d_k)
- 检查 mask 的实现是否正确
- 检查输出 shape 是否符合预期

    # Step 3: 写测试
    def test_multi_head_attention():
        attn = MultiHeadAttention(d_model=512, n_heads=8)
        x = torch.randn(32, 100, 512)  # (batch, seq, dim)
        out, weights = attn(x, x, x)

        assert out.shape == (32, 100, 512)
        assert weights.shape == (32, 8, 100, 100)
        assert torch.allclose(weights.sum(dim=-1),
                              torch.ones_like(weights.sum(dim=-1)))

    # Step 4: 独立测试模块
    pytest tests/test_attention.py -v

    # Step 5: 在小数据上测试集成
    python train.py --config configs/test_attention.yaml \
                    --data_subset 100 --epochs 2

    # Step 6: 确认没问题后，正式训练
    python train.py --config configs/attention.yaml

### 案例 2：重构数据加载

#### 错误方式：

    你：这个数据加载代码太乱了，Copilot 帮我重构
    Copilot：[重写了整个 DataLoader 类]
    你：好，用新版本！
    [重新跑实验，结果和之前不一致，不知道哪里出错了]

#### 正确方式：

    # Step 1: 为旧版本写行为测试
    def test_old_data_loader_behavior():
        """记录旧版本的行为作为基准"""
        loader = OldDataLoader(...)
        batch = next(iter(loader))

        # 记录关键行为
        assert batch['image'].shape == (32, 3, 224, 224)
        assert batch['image'].dtype == torch.float32
        assert batch['image'].min() >= -1.0
        assert batch['image'].max() <= 1.0
        # ... 更多断言

    # Step 2: 运行测试，确保通过
    pytest tests/test_data_loader.py::test_old_behavior -v

    # Step 3: 让 AI 重构
    Copilot：[生成新的 DataLoader]

    # Step 4: 为新版本写相同的测试
    def test_new_data_loader_behavior():
        """确保新版本行为一致"""
        loader = NewDataLoader(...)
        batch = next(iter(loader))

        # 相同的断言
        assert batch['image'].shape == (32, 3, 224, 224)
        # ...

    # Step 5: 对比两个版本的输出
    def test_output_consistency():
        """直接对比新旧版本输出"""
        old_loader = OldDataLoader(seed=42)
        new_loader = NewDataLoader(seed=42)

        old_batch = next(iter(old_loader))
        new_batch = next(iter(new_loader))

        torch.testing.assert_close(old_batch['image'],
                                   new_batch['image'])

    # Step 6: 如果一致，再运行完整实验验证
    make reproduce RUN=baseline  # 用旧版本
    make train CONFIG=configs/baseline_new_loader.yaml  # 用新版本
    # 对比结果

## 常见问题与解决方案

### Q1：AI 生成的代码太复杂，看不懂怎么办？

**解决方案：**

- 拒绝接受！让 AI 重新生成更简单的版本。

- 提示词：

        请实现 XXX 功能，要求：
        - 代码简单直接，避免过度抽象
        - 尽量使用标准库和常见模式
        - 添加详细注释解释每个步骤

- 记住：**你看不懂的代码，未来的你也看不懂，别人更看不懂。**

### Q2：AI 生成的代码有 bug，但改了又出现新 bug

**解决方案：**

- 不要反复让 AI 修 bug，陷入无限循环。

- 正确做法：

  1.  先写测试，复现 bug

  2.  人工修复 bug（小范围改动）

  3.  测试通过后，再考虑是否需要重构

- AI 可以提示可能的问题，但修复应该由人来做。

### Q3：团队成员不遵守 AI 使用规范怎么办？

**解决方案：**

- 在 Git pre-commit hook 里加入自动检查：

        # .git/hooks/pre-commit
        #!/bin/bash

        # 检查 commit diff 行数
        DIFF_LINES=$(git diff --cached | wc -l)
        if [ $DIFF_LINES -gt 400 ]; then
            echo "Error: commit diff too large ($DIFF_LINES lines)"
            echo "Please split into smaller commits"
            exit 1
        fi

        # 检查是否有测试
        if git diff --cached --name-only | grep -q "src/"; then
            if ! git diff --cached --name-only | grep -q "tests/"; then
                echo "Warning: you modified src/ but no test changes"
                echo "Please ensure tests are updated"
            fi
        fi

        # 运行测试
        pytest tests/ -q || {
            echo "Error: tests failed"
            exit 1
        **

- 在 CI 中强制执行（见下节）

- Code review 时严格检查

## 10 分钟动作：为下一次 AI 编码建立检查点

如果你现在只做一件事：为下一次 AI 辅助编码建立最小验证流程。

1.  **创建 CLAUDE.md**

    复制本章的模板，放到项目根目录。

2.  **写一个 smoke test**

          # tests/test_smoke.py

          def test_basic_training_loop():
              """基本训练流程能跑通"""
              config = load_config("configs/test.yaml")
              config["epochs"] = 2
              config["data_subset"] = 100

              model, metrics = train_model(config)

              assert metrics["train_loss"] > 0
              assert not math.isnan(metrics["val_loss"])

3.  **设置 pre-commit hook**

          # 简单版本：只检查测试
          echo '#!/bin/bash\npytest tests/ -q' > .git/hooks/pre-commit
          chmod +x .git/hooks/pre-commit

4.  **试一次完整流程**

          # 1. 创建实验分支
          git checkout -b exp/test-ai-workflow

          # 2. 让 AI 做一个小改动（如添加一个工具函数）
          # 3. 写对应测试
          # 4. 运行测试
          pytest tests/test_xxx.py

          # 5. Commit（会自动运行 hook）
          git add .
          git commit -m "feat: add utility function X"

          # 6. 如果 hook 通过，合并到 main
          git checkout main
          git merge exp/test-ai-workflow

从下一次使用 AI 编码开始，**默认行为**就是：生成 → 审查 → 测试 → 验证 → 合并。这个流程会成为肌肉记忆，确保 AI 始终是你的提速器，而不是地雷制造机。
