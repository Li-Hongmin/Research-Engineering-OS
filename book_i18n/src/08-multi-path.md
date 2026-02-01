# 多路径探索如何不变垃圾堆

![插图](images/08_exploration_branches.png)


## 故事引入：从"灵活探索"到"不敢动任何东西"

你的研究项目进行到第三个月。你是一个勤奋的研究者，尝试了很多不同的方向：

- 路径 A：改进模型架构（5 种不同的注意力机制）

- 路径 B：优化训练策略（3 种不同的学习率调度）

- 路径 C：增强数据质量（4 种预处理方式）

- 路径 D：调整损失函数（6 种不同的损失组合）

你很兴奋——这么多探索！肯定能找到有效的组合！

但当你打开项目目录，看到的是这样的景象：

    experiments/
      train_v1.py
      train_v2.py
      train_v2_fixed.py
      train_v3_final.py
      train_v3_really_final.py
      train_attention_test.py
      train_loss_ablation.py
      ...（20+ 个文件）

    outputs/
      run_0523/
      exp_new/
      test_attention/
      final_results/
      final_results_v2/
      backup_0601/
      temp/
      ...（50+ 个目录）

    configs/
      config.yaml
      config_old.yaml
      config_backup.yaml
      config_test.yaml
      ...（15+ 个文件）

**问题开始暴露**：

### 问题 1：找不到最好的结果

你记得某次实验效果很好，但你不记得是哪个配置、哪个输出目录。你开始一个一个打开目录，查看日志，试图找到那个结果。花了两个小时，还是不确定找对了没有。

#### 问题 2：不敢删除任何东西

outputs/ 已经占了 50GB 空间，但你不敢删除任何目录——万一删掉的正好是论文需要的那个实验呢？你决定"先留着，反正硬盘够大"。

#### 问题 3：无法对比不同路径

你想对比"路径 A（注意力改进）"和"路径 B（学习率优化）"的效果，但你发现：

- 它们用的 baseline 不一样（一个是三个月前的，一个是最近的）

- 评估脚本不一样（一个算的是 top-1，一个是 top-5）

- 数据划分可能也不一样（记不清了）

#### 问题 4：无法合并有效改进

你在路径 A 里发现了一个有效的改进，想把它移植到路径 B 里，但发现：

- 路径 A 和路径 B 的代码已经分化了

- 数据加载逻辑不兼容

- 合并需要大量人工工作

**你意识到：灵活探索变成了无序混乱，多路径并行变成了垃圾堆。**

## 为什么多路径探索容易失控

研究的本质就是**不确定性**：你不知道哪条路会成功，所以需要同时探索多个方向。但如果没有管理机制，探索的越多，混乱度就越高。

### 失控的三个阶段

#### 阶段 1：快速探索（第 1-4 周）

**行为**：

- 想到什么就试什么，不拘泥于规范

- 代码复制粘贴，改个名字就用

- 输出随便找个地方放，"先跑起来再说"

**感觉**：充满活力，进展快速。

#### 阶段 2：路径分化（第 5-8 周）

**行为**：

- 不同路径的代码开始分化，共同部分减少

- 每条路径有自己的数据处理、训练脚本、评估方式

- 新想法基于某个旧路径，而不是主线

**感觉**：有点乱，但还能记住大致情况。

#### 阶段 3：失控混乱（第 9 周+）

**行为**：

- 完全记不住哪个实验是哪个路径的

- 不敢删除任何东西，空间占用暴增

- 想要合并改进时发现路径已经完全不兼容

- 准备论文时重新跑实验，结果对不上记忆

**感觉**：焦虑、无力、想推倒重来。

### 根本原因：缺少"可丢弃"和"可合并"机制

多路径探索的核心挑战是：

- **不知道哪条路会成功**，所以需要并行探索多条路径

- **不能全部保留**，否则会淹没在信息海洋里

- **成功的路径需要合并回主线**，否则无法形成完整方案

如果缺少管理机制：

- 路径无法安全丢弃（怕删错）

- 路径无法轻松合并（代码分化）

- 路径无法清晰对比（条件不一致）

## 核心机制：隔离 + 可丢弃 + 可对比

### 机制 1：每条路径必须隔离

**隔离的三要素**：

1.  **独立的 Git 分支**

          exp/path-A-attention      # 路径 A：注意力改进
          exp/path-B-lr-schedule    # 路径 B：学习率优化
          exp/path-C-data-aug       # 路径 C：数据增强
          exp/path-D-loss-combo     # 路径 D：损失组合

    好处：

- 代码改动相互独立，不会冲突

- 可以随时切换、对比、合并

- Git 历史清晰记录每条路径的演进

2.  **独立的配置文件**

          configs/
            baseline.yaml              # 公共基准
            path_A_attention.yaml      # 路径 A 的配置
            path_B_lr_schedule.yaml    # 路径 B 的配置
            path_C_data_aug.yaml       # 路径 C 的配置
            path_D_loss_combo.yaml     # 路径 D 的配置

    配置里明确继承关系：

          # path_A_attention.yaml
          base: baseline.yaml  # 继承基准配置

          # 只列出差异
          model:
            attention_type: "multi_head"  # 改动点
            num_heads: 8

          experiment:
            name: "path_A_attention"
            hypothesis: "多头注意力比单头更有效"

3.  **独立的输出目录**

          outputs/
            path_A/
              2026-02-01_1030_baseline/
              2026-02-01_1500_multi_head_attn/
              2026-02-02_0900_improved_attn/
            path_B/
              2026-02-01_1100_baseline/
              2026-02-01_1600_cosine_schedule/
              2026-02-02_1000_warmup_schedule/
            path_C/
              ...

    好处：

- 每条路径的实验结果清晰分组

- 删除整个路径时，只需删除对应目录

- 归档时可以按路径打包

### 机制 2：明确的生命周期管理

每条探索路径都应该有明确的生命周期：

    创建 → 探索 → 评估 → 决策（保留/归档/删除）

#### 创建阶段

    # 1. 创建分支
    git checkout main
    git checkout -b exp/path-E-new-idea

    # 2. 创建配置
    cp configs/baseline.yaml configs/path_E_new_idea.yaml
    # 编辑配置，记录假设

    # 3. 创建输出目录
    mkdir -p outputs/path_E/

    # 4. 记录路径信息
    cat > outputs/path_E/README.md <<EOF
    # 路径 E：新想法探索

    ## 假设
    [这条路径要验证什么假设？]

    ## 基准对比
    对比基准：outputs/baseline/2026-02-01_1030_baseline
    预期改进：[预期能提升多少？]

    ## 关键改动
- [改动 1]
- [改动 2]

    ## 开始时间
    2026-02-05

    ## 状态
    探索中
    EOF

#### 探索阶段

在分支上自由迭代，记录每次实验：

    # 运行实验
    python train.py --config configs/path_E_new_idea.yaml \
                    --output outputs/path_E/2026-02-05_1030_try1/

    # 记录结果（run.json 自动生成，run.md 手写）
    # 见第6章

    # 继续迭代
    # 每次实验用新的 run_id，不覆盖之前的

#### 评估阶段

定期（如每周）评估路径价值：

    # 评估清单

    ## 效果评估
- 最好结果：[指标]
- 对比基准：[改进幅度]
- 稳定性：[多次运行的方差]

    ## 成本评估
- 时间成本：[训练时间增加了多少？]
- 计算成本：[需要更多资源吗？]
- 复杂度成本：[代码复杂度增加了多少？]

    ## 洞察收获
- 发现了什么？[即使没成功，有什么学到的？]
- 失败原因：[为什么没达到预期？]
- 副产品：[有没有意外收获？]

    ## 决策
    [ ] 继续探索（值得深入）
    [ ] 合并到主线（成功）
    [ ] 归档（有价值但不是当前重点）
    [ ] 删除（无价值）

#### 决策阶段

根据评估结果，做出清晰决策：

**决策 1：合并到主线**（路径成功）

    # 1. 整理代码
    # 确保改动最小、干净、可测试

    # 2. 运行完整验证
    make test
    make reproduce RUN=path_E/best_result

    # 3. 合并
    git checkout main
    git merge exp/path-E-new-idea

    # 4. 打 tag
    git tag -a milestone-E-success -m \
      "路径 E 成功：新想法将 baseline 性能从 X 提升到 Y"

    # 5. 更新 baseline
    cp outputs/path_E/best_result outputs/baseline/

    # 6. 删除实验分支
    git branch -d exp/path-E-new-idea

    # 7. 更新路径状态
    echo "Status: Merged to main (2026-02-12)" >> outputs/path_E/README.md

**决策 2：归档**（有价值但非当前重点）

    # 1. 打 tag 保存分支状态
    git tag -a archive/path-E-v1 -m \
      "路径 E 归档：初步有效但需要更多时间验证"

    # 2. 整理产物
    mkdir -p archives/path_E/
    cp -r outputs/path_E/ archives/path_E/
    cp configs/path_E_*.yaml archives/path_E/

    # 3. 写总结
    cat > archives/path_E/SUMMARY.md <<EOF
    # 路径 E 归档总结

    ## 主要发现
    [总结关键发现]

    ## 为什么归档
    [解释为什么现在不继续，但值得保留]

    ## 未来重启条件
    [什么情况下值得重新探索？]

    ## 参考资料
- 代码版本：git tag archive/path-E-v1
- 最好结果：outputs/path_E/2026-02-10_1500_best/
- 相关论文：[外部参考]
    EOF

    # 4. 删除实验分支（保留 tag）
    git branch -d exp/path-E-new-idea

    # 5. 删除 outputs（已归档）
    rm -rf outputs/path_E/

**决策 3：删除**（无价值）

    # 1. 最后确认
    # 检查是否有任何有价值的发现或代码

    # 2. 删除输出
    rm -rf outputs/path_E/

    # 3. 删除配置
    rm configs/path_E_*.yaml

    # 4. 删除分支
    git branch -D exp/path-E-new-idea  # -D 强制删除

    # 5. 记录删除原因（可选但推荐）
    cat >> docs/EXPLORATION_LOG.md <<EOF
    ## 路径 E（已删除，2026-02-12）
- 假设：[原始假设]
- 结果：[为什么失败]
- 教训：[学到了什么]
    EOF

### 机制 3：公平对比的基准线

所有路径对比时，必须使用**同一基准**：

#### 建立基准实验

    # 1. 在 main 分支跑基准实验
    git checkout main
    python train.py --config configs/baseline.yaml \
                    --output outputs/baseline/2026-02-01_1030_baseline/

    # 2. 验证基准可复现
    make reproduce RUN=baseline/2026-02-01_1030_baseline

    # 3. 打 tag
    git tag -a baseline-v1 -m "Common baseline for all paths"

    # 4. 记录基准信息
    cat > outputs/baseline/INFO.md <<EOF
    # 基准实验信息

    ## 配置
- Config: configs/baseline.yaml
- Commit: $(git rev-parse HEAD)
- Tag: baseline-v1

    ## 结果
- Val accuracy: 0.920
- Test accuracy: 0.915
- Training time: 2.5 hours

    ## 用途
    所有路径（A-Z）的对比基准。
    任何路径的改进都应该相对这个基准来报告。

    ## 复现
    make reproduce RUN=baseline/2026-02-01_1030_baseline
    EOF

#### 路径对比标准化

    # 对比脚本示例
    # compare_paths.py

    import json
    from pathlib import Path

    def compare_to_baseline(path_name):
        """对比某条路径和基准的结果"""
        baseline = load_best_run("outputs/baseline")
        path = load_best_run(f"outputs/{path_name}")

        print(f"\n{'='*60**")
        print(f"路径对比：{path_name} vs Baseline")
        print(f"{'='*60**\n")

        # 对比配置差异
        print("配置差异：")
        diff_configs(baseline["config"], path["config"])

        # 对比指标
        print("\n指标对比：")
        compare_metrics(baseline["metrics"], path["metrics"])

        # 对比成本
        print("\n成本对比：")
        compare_cost(baseline, path)

        # 结论
        print("\n结论：")
        if is_improvement(path["metrics"], baseline["metrics"]):
            print(f"[OK] 路径 {path_name} 成功改进 baseline")
            print(f"   建议：合并到主线")
        else:
            print(f"[NO] 路径 {path_name} 未能改进 baseline")
            print(f"   建议：归档或删除")

    if __name__ == "__main__":
        import sys
        compare_to_baseline(sys.argv[1])

## 每周清理仪式：实验墓地整理

**核心理念**：定期清理是避免垃圾堆的唯一方法。

### 每周五下午的清理流程（30 分钟）

#### Step 1：列出所有活跃路径（5 分钟）

    # list_active_paths.sh

    echo "活跃的探索路径："
    git branch | grep "exp/" | while read branch; do
        echo "  - $branch"
    done

    echo "\n输出目录大小："
    du -sh outputs/*/ | sort -rh

#### Step 2：逐个评估路径（15 分钟）

对每条路径问三个问题：

1.  **这周有新进展吗？**

- 有：继续保留

- 没有：是暂停还是放弃？

2.  **相比 baseline 有改进吗？**

- 有：达到合并标准了吗？

- 没有：还有继续价值吗？

3.  **占用多少资源？**

- 输出目录大小

- 代码复杂度

- 维护成本

#### Step 3：执行清理动作（10 分钟）

    # 清理脚本示例
    # weekly_cleanup.sh

    #!/bin/bash

    echo "开始每周清理..."

    # 1. 归档两周前的路径（如果有 tag）
    git tag -l "archive/*" | while read tag; do
        tag_date=$(git log -1 --format=%ai $tag | cut -d' ' -f1)
        # [归档逻辑]
    done

    # 2. 删除标记为 "to_delete" 的输出
    find outputs/ -name ".to_delete" -type f | while read marker; do
        dir=$(dirname $marker)
        echo "删除：$dir"
        rm -rf $dir
    done

    # 3. 压缩一个月前的输出（如果还有价值）
    find outputs/ -type d -mtime +30 | while read dir; do
        if [ -f "$dir/run.json" ]; then
            echo "压缩：$dir"
            tar -czf "${dir}.tar.gz" $dir
            rm -rf $dir
        fi
    done

    # 4. 报告空间释放
    echo "\n清理完成！"
    du -sh outputs/

### 清理决策树

    对于每条路径，判断：

    +-- 过去两周有活动？
        |
        +-- 是 -> 相比 baseline 有改进？
        |        |
        |        +-- 是(>5%) -> [合并到主线]
        |        +-- 是(3-5%) -> [继续观察]
        |        +-- 否(<3%) -> [考虑放弃]
        |
        +-- 否 -> 是否有归档价值？
                 |
                 +-- 是（有独特洞察）-> [归档]
                 +-- 否 -> [删除]

    特殊情况：
- 占用空间 >10GB -> 优先处理（压缩或删除）
- 有外部引用（如论文草稿）-> 暂不删除，打标记
- 代码复杂度高 -> 如无明显价值，倾向删除

## 路径合并策略：从探索到稳定主线

### 合并前检查清单

在合并路径到 main 之前，确保满足：

    [ ] 相比 baseline 有稳定改进（多次运行均有效）
    [ ] 改动最小化（只保留必要的修改）
    [ ] 代码干净可维护（通过 lint 和 review）
    [ ] 有测试覆盖（至少 smoke test）
    [ ] 配置清晰记录（可复现）
    [ ] 不破坏现有功能（回归测试通过）
    [ ] 文档已更新（README、API docs）

### 渐进式合并策略

对于复杂路径，不要一次性全部合并。推荐分步骤：

#### 示例：合并"路径 A：注意力改进"

    # 路径 A 包含三个改动：
    # 1. 新的注意力机制
    # 2. 改进的位置编码
    # 3. 调整的学习率

    # 不要一次性合并所有改动！

    # Step 1: 先合并最核心的改进（注意力）
    git checkout main
    git checkout exp/path-A-attention -- src/models/attention.py
    git commit -m "feat: add improved attention mechanism from path A"

    # 验证
    make test
    make train CONFIG=configs/main_with_new_attention.yaml

    # Step 2: 如果 Step 1 成功，再合并位置编码
    git checkout exp/path-A-attention -- src/models/position_encoding.py
    git commit -m "feat: add improved position encoding from path A"

    # 验证
    make test
    make train CONFIG=configs/main_with_attention_and_pos.yaml

    # Step 3: 最后合并超参数调整
    # [如果前两步都成功的话]

好处：

- 每一步都可独立验证

- 如果某步失败，不影响其他改进

- Git 历史清晰记录每个改进

- 便于定位问题

## 常见问题与解决方案

### Q1：路径太多了，记不住怎么办？

**解决方案**：维护一个路径追踪表。

    # docs/EXPLORATION_TRACKER.md

    # 探索路径追踪

    | 路径 | 状态 | 假设 | 最好结果 | 决策 | 更新时间 |
    |------|------|------|----------|------|----------|
    | A-attention | 进行中 | 多头注意力更有效 | 0.925 (+0.5%) | 继续 | 2026-02-10 |
    | B-lr-schedule | 归档 | Cosine 调度更好 | 0.922 (+0.2%) | 效果不显著 | 2026-02-08 |
    | C-data-aug | 进行中 | MixUp 能提升泛化 | 0.930 (+1.0%) | **考虑合并** | 2026-02-12 |
    | D-loss-combo | 删除 | 多任务损失有帮助 | 0.918 (-0.2%) | 反向效果 | 2026-02-05 |
    | E-new-idea | 刚启动 | [待验证] | - | 探索 | 2026-02-12 |

    ## 基准
    Baseline: 0.920 (outputs/baseline/2026-02-01_1030_baseline)

    ## 下周计划
- 路径 A：完成消融实验，确认每个组件贡献
- 路径 C：多跑几个 seed 验证稳定性
- 路径 E：初步实现和验证

每周更新这个表格（5 分钟），就能清晰掌控所有路径状态。

### Q2：不同路径的代码冲突怎么办？

**预防胜于治疗**：

- 路径尽量改不同的模块（如一个改数据、一个改模型）

- 共享的核心代码放在 src/，不轻易修改

- 路径特有的改动放在 experiments/ 里

**冲突发生时**：

- 不要强行合并多个路径

- 先合并一个，验证成功后，再基于新 main 重新创建其他路径

- 或者：重新评估是否真的需要合并多个路径

### Q3：删除路径后后悔了怎么办？

**预防措施**：

- 删除前打 tag：

        git tag -a deleted/path-X -m "Path X before deletion"

- 删除前写简短总结（见上文"删除决策"）

- 重要的数据先归档到便宜的存储（如云端）

**恢复方法**：

    # 如果有 tag，可以恢复代码
    git checkout deleted/path-X

    # 基于此重新创建分支
    git checkout -b exp/path-X-restored

    # 如果输出被删除了，检查归档或备份
    ls archives/path_X/

## 10 分钟动作：整理当前的探索路径

如果你现在只做一件事：清点并分类当前所有探索路径。

1.  **列出所有分支和输出**

          git branch | grep "exp/"
          ls outputs/

2.  **为每条路径快速分类**

    在笔记里写下：

          路径 A (exp/xxx): [进行中 | 归档 | 删除]
          - 假设：
          - 状态：
          - 决策：

          路径 B (exp/yyy): [进行中 | 归档 | 删除]
          - ...

3.  **执行一次清理**

          # 删除明确无价值的路径
          git branch -D exp/failed-path-X
          rm -rf outputs/path_X/

          # 归档有价值但不活跃的路径
          git tag -a archive/path-Y
          mkdir -p archives/path_Y/
          mv outputs/path_Y/ archives/path_Y/

          # 为活跃路径更新状态记录

4.  **建立追踪表**

    创建 `docs/EXPLORATION_TRACKER.md`，记录所有活跃路径。

5.  **设定下周清理时间**

    在日历里加入**：每周五 17:00 - 探索路径清理（30 分钟）**

完成这个 10 分钟动作后，你会立刻感觉到：

- 对项目状态的掌控力增强

- 知道哪些路径值得继续、哪些该放弃

- 不再担心"垃圾堆"会失控

**记住：多路径探索是研究的必要特征，但不管理的多路径探索会变成灾难。定期清理不是负担，而是保持清醒的必要仪式。**
