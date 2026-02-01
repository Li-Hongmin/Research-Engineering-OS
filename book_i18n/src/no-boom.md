# 让最后阶段不爆炸的 3 个提前动作

![插图](images/09_quality_shield.png)


## 故事引入：离 deadline 只剩一周的噩梦

周一早上，你查看日历，心里一沉——论文截稿倒计时：**7 天**。

你原本计划这周只是"最后润色"：把实验结果整理成图表，写好相关工作，检查一遍格式。应该很轻松，对吧？

但当你开始准备论文时，问题像雪崩一样涌来：

### 周一：发现主实验无法复现

你想重新跑一次主实验，确认数字没记错。但运行脚本后，结果和三周前不一样——准确率从 94.3% 降到了 92.1%。

你慌了。开始排查：

- 是代码变了吗？Git 历史一片混乱，你不确定当时用的哪个版本。

- 是数据变了吗？数据目录里有 v1、v2、v3，记不清了。

- 是环境变了吗？某个依赖库自动升级了？

你花了一整天也没找到原因。

#### 周二：发现 baseline 不公平

审稿人肯定会关注你和 baseline 的对比。你仔细检查，发现一个致命问题：你的方法用的是最新的数据预处理，但 baseline 用的是旧版本。评估口径根本不一致。

你需要重新跑 baseline——但这需要 6 小时训练时间。

#### 周三：发现缺少关键的消融实验

导师看了你的初稿，指出："你的方法包含三个改进（A、B、C），但你没有说明每个改进贡献了多少。审稿人肯定会问。"

你意识到缺少消融实验（ablation study）。你需要跑：

- baseline

- baseline + A

- baseline + B

- baseline + C

- baseline + A + B

- baseline + A + C

- baseline + B + C

- baseline + A + B + C（完整方法）

每个实验 2 小时，8 个实验 = 16 小时。但你只有 4 天了。

#### 周四：发现图表数据找不到

你想生成论文图表，但发现关键实验的输出文件找不到了——可能被你不小心删了，或者在某次清理时弄丢了。你只记得"结果很好"，但原始数据没了。

你不得不重新跑那些实验。

#### 周五：开始怀疑人生

你已经三天没睡好觉了。实验还在跑，论文还没开始写，图表还没做完。你开始怀疑**："为什么我总是在最后阶段爆炸？"**

**答案很简单：因为你没有提前做三件事。**

## 为什么"最后阶段爆炸"几乎是必然

回顾本书第一章，我们说过研究中有三种债务：

- **探索债**：代码混乱、输出散乱、路径不清

- **验证债**：baseline 不强、消融缺失、对比不公平

- **复现债**：环境不固定、配置不全、版本不明

如果这些债务在日常积累，最后阶段就是**集中偿还期**。而deadline 的压力会放大一切问题：

- 平时可以慢慢调试的问题，现在必须立刻解决

- 平时可以重跑的实验，现在没时间了

- 平时可以请教的问题，现在别人也忙

**最残酷的真相：如果你在最后一周才发现问题，大概率已经来不及修复了。**

那怎么办？答案是**：提前暴露问题，提前解决，或者至少提前知道有问题。**

## 提前动作 1：每周一次"可复现性自查"（15 分钟）

### 为什么重要

**核心理念**：你不能等到论文截稿前才发现结果无法复现。必须在日常就持续验证可复现性。

如果每周都做一次自查，问题会在出现的当周被发现，而不是累积到最后。

### 自查清单（15 分钟完成）

#### 第 1 项：检查本周最重要的实验能否复现（5 分钟）

    # 找到本周最好/最重要的实验
    RUN_ID="本周最好的 run_id"

    # 检查记录完整性
    [ ] outputs/$RUN_ID/run.json 存在
    [ ] run.json 里有 git commit
    [ ] run.json 里有 config 路径
    [ ] run.json 里有 seed
    [ ] run.json 里有数据版本
    [ ] run.json 里有环境信息

    # 如果任何一项缺失，立刻补救

#### 第 2 项：尝试快速复现（5 分钟）

不需要完整重跑（太慢），但要验证**流程能跑通**：

    # 用小数据集快速测试
    python train.py \
        --config outputs/$RUN_ID/config.yaml \
        --data_subset 100 \
        --epochs 2 \
        --seed 42

    # 检查：
    [ ] 能正常启动
    [ ] 数据加载正确
    [ ] 模型前向传播正确
    [ ] 损失计算正常
    [ ] 评估流程正确

如果这 2 分钟的测试都跑不通，说明完整复现肯定有问题。**现在修复还来得及。**

#### 第 3 项：检查依赖是否漂移（3 分钟）

    # 保存当前依赖
    pip freeze > requirements_$(date +%Y%m%d).txt

    # 对比上周的依赖
    diff requirements_上周日期.txt requirements_$(date +%Y%m%d).txt

    # 如果有变化，记录到 CHANGELOG.md

依赖变化是复现问题的常见原因。每周记录可以在问题出现时快速定位。

#### 第 4 项：检查输出是否有标记（2 分钟）

    # 检查本周输出是否都有 run_id
    ls outputs/

    # 检查是否有"unnamed"、"temp"、"test"这类临时目录
    # 如果有，要么删除，要么给它们起正式名字

无名输出是"未来的坑"——你现在知道它是什么，但一个月后就忘了。

### 自查频率与时机

**推荐时间**：每周五下午最后 15 分钟

**为什么是周五？**

- 一周工作结束，可以全面回顾

- 周末不工作的话，可以安心休息（知道项目状态可控）

- 如果发现问题，下周一可以立刻处理

**特殊情况**：

- 出现"看起来不错"的结果时：立刻做自查，不要拖到周五

- 改了核心代码后：当天就做自查

- 切换数据版本后：立刻做自查

### 常见陷阱

#### 陷阱 1："反正都记得，不用检查"

**现实**：两周后你就会忘记细节。记忆不可靠，记录才可靠。

#### 陷阱 2："这次只是测试，不用记录"

**现实**：很多"只是测试"的实验后来成了论文主结果，但当时没记录，最后追悔莫及。

#### 陷阱 3："反正能跑，应该能复现"

**现实**："能跑"和"能在另一台机器/另一个环境/两个月后复现"是完全不同的事。

## 提前动作 2：每月一次"债务盘点"（30 分钟）

### 为什么重要

周自查解决的是"最近的实验能否复现"，但还有更深层的问题：

- 整个项目有多少探索债？

- 有多少验证债？

- 有多少复现债？

每月盘点就是**强制你抬头看全局**，而不是一直埋头做实验。

### 盘点清单（30 分钟完成）

#### 探索债盘点（10 分钟）

    # 1. 统计代码混乱度
    git ls-files | wc -l                    # 总文件数
    git ls-files | grep "test\|tmp" | wc -l  # 临时文件数
    git log --oneline | head -20            # 最近 20 次 commit

    # 2. 统计输出混乱度
    du -sh outputs/                         # 总大小
    ls outputs/ | wc -l                     # 目录数
    find outputs/ -name "run.json" | wc -l  # 有记录的实验数

    # 3. 计算探索债指标
    有记录实验 / 总目录数 = 记录覆盖率

**健康标准**：

- 记录覆盖率 \>80%：良好

- 记录覆盖率 60-80%：警戒

- 记录覆盖率 \<60%：危险（需要立刻清理）

#### 验证债盘点（10 分钟）

    # 检查验证完整性

    论文候选结果清单：
    [ ] 主实验（Table 2）→ run_id: __________
    [ ] Baseline 对比（Table 3）→ run_id: __________
    [ ] 消融实验（Table 4）→ run_id: __________
    [ ] 失败案例分析（Figure 5）→ run_id: __________

    对于每个结果：
    [ ] 有完整 run.json
    [ ] 有 baseline 对比（公平评估）
    [ ] 有多次运行（不是偶然）
    [ ] 有测试覆盖（smoke test 通过）

**健康标准**：

- 所有论文候选结果都有 run_id：良好

- 缺少 1-2 个：警戒（下月补齐）

- 缺少 3 个以上：危险（论文写不了）

#### 复现债盘点（10 分钟）

    # 找到最重要的 3 个实验
    TOP_3_RUNS="..."

    # 对每个实验做复现测试
    for run_id in $TOP_3_RUNS; do
        echo "Testing $run_id..."

        # 检查记录
        [ -f outputs/$run_id/run.json ] || echo "❌ 缺少 run.json"

        # 快速复现测试（小数据）
        python train.py \
            --config outputs/$run_id/config.yaml \
            --data_subset 100 --epochs 2 \
            || echo "❌ 快速复现失败"

        # 依赖检查
        pip install -r outputs/$run_id/requirements.txt \
            || echo "⚠️  依赖可能有变化"
    done

**健康标准**：

- 3 个都能快速复现：良好

- 2 个能复现：警戒

- 1 个或 0 个能复现：危险（需要紧急修复）

### 债务可视化

建议维护一个"债务趋势图"：

    # debt_tracking.csv
    月份,探索债(记录覆盖率),验证债(候选结果完整性),复现债(可复现比例)
    2026-01,50%,60%,33%
    2026-02,70%,80%,67%
    2026-03,85%,100%,100%

如果债务在累积（数字下降），说明你在"透支未来"。如果债务在减少（数字上升），说明你在"偿还债务"。

**目标**：论文截稿前三个月，所有债务指标应该 \>90%。

## 提前动作 3：论文前三个月建立"复现基线"（1 小时）

### 为什么重要

**最大的误区**：认为"论文写作阶段"才需要考虑复现性。

**现实**：如果你等到写论文时才开始准备复现材料，会发现：

- 很多实验细节已经忘了

- 代码版本对不上

- 数据找不到了

- 环境变了

**正确做法**：在"实验阶段"就建立复现基线，论文阶段只需要验证和补充。

### 复现基线的内容

#### 最小复现包（1 小时建立）

    reproduce/
      README.md              # 复现指南
      environment.yaml       # 环境定义
      data_manifest.txt      # 数据清单
      baseline_runs.txt      # 关键实验列表
      reproduce.sh           # 一键复现脚本
      verify.py              # 验证脚本

#### README.md 模板

    # 复现指南

    ## 环境准备（10 分钟）

    ```bash
    # 创建环境
    conda env create -f environment.yaml
    conda activate research-env

    # 验证安装
    python verify.py --check-env
    ```
## 数据准备（30 分钟）
```bash
    # 下载数据（需要约 5GB 空间）
    bash scripts/download_data.sh

    # 验证数据
    python verify.py --check-data
    ```
## 复现关键实验（6 小时）
```bash
    # 复现主实验（Table 2，约 2 小时）
    make reproduce RUN=main_experiment
    # 预期结果：accuracy 94.3% ± 0.5%

    # 复现 baseline（Table 3，约 2 小时）
    make reproduce RUN=baseline
    # 预期结果：accuracy 92.0% ± 0.3%

    # 复现消融实验（Table 4，约 2 小时）
    bash scripts/reproduce_ablation.sh
    ```
## 验证结果
```bash
    # 自动验证所有结果
    python verify.py --check-results

    # 输出应该显示：
    # ✅ Main experiment: within expected range
    # ✅ Baseline: within expected range
    # ✅ Ablation: all components verified
    ```

    ## 故障排除

    见 docs/TROUBLESHOOTING.md

### verify.py 示例

    import json
    from pathlib import Path

    def verify_environment():
        """验证环境是否正确"""
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"✅ CUDA available: {torch.cuda.is_available()}")
        # 更多检查...

    def verify_data():
        """验证数据是否完整"""
        data_manifest = Path("data_manifest.txt").read_text()
        # 检查文件是否存在、哈希是否一致...
        print("✅ Data verification passed")

    def verify_results(run_id, expected_metric, tolerance=0.01):
        """验证结果是否在预期范围内"""
        run_json = Path(f"outputs/{run_id}/run.json")
        with open(run_json) as f:
            run_info = json.load(f)

        actual = run_info["metrics"]["test_acc"]
        diff = abs(actual - expected_metric)

        if diff <= tolerance:
            print(f"✅ {run_id}: {actual:.3f} "
                  f"(expected {expected_metric:.3f} ± {tolerance:.3f})")
            return True
        else:
            print(f"❌ {run_id}: {actual:.3f} "
                  f"(expected {expected_metric:.3f}, diff {diff:.3f})")
            return False

    if __name__ == "__main__":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--check-env", action="store_true")
        parser.add_argument("--check-data", action="store_true")
        parser.add_argument("--check-results", action="store_true")
        args = parser.parse_args()

        if args.check_env:
            verify_environment()
        if args.check_data:
            verify_data()
        if args.check_results:
            # 验证所有关键实验
            verify_results("main_experiment", expected_metric=0.943)
            verify_results("baseline", expected_metric=0.920)
            # ...

### 建立时机

**最佳时机**：当你有第一个"看起来能写进论文"的结果时，立刻建立复现基线。

不要等到：

- ❌ 实验都做完了

- ❌ 开始写论文了

- ❌ 准备投稿了

应该是：

- ✅ 有第一个有希望的结果（即使还不完美）

- ✅ 确定大致的技术路线

- ✅ 能回答"这个项目最终要证明什么"

**经验法则**：论文截稿前 3 个月建立复现基线。如果是会议论文（6 个月项目），则在第 3 个月建立。

## 紧急补救方案：如果已经到了最后阶段

### 如果距离 deadline 只剩 2 周

**接受现实**：你没时间"做对一切"了。必须聚焦最重要的事。

#### 优先级 1：确保主结果可复现（3 天）

    # Day 1：找到主实验的代码版本
    # - 通过 Git 历史、聊天记录、笔记回忆
    # - 找到最接近的 commit
    # - 补充 run.json（尽可能回忆参数）

    # Day 2：在干净环境重跑
    # - 新建虚拟环境
    # - 记录所有依赖
    # - 重新运行，记录结果

    # Day 3：如果无法精确复现
    # - 如果差异在 1-2% 内：可以接受，注明误差
    # - 如果差异更大：在论文里诚实说明原因
    # - 最坏情况：改用可复现的次优结果

#### 优先级 2：补最关键的验证（2 天）

只补**审稿人肯定会问**的验证：

- 如果只能选一个：补 baseline 公平对比

- 如果能选两个：再补主要的消融实验

- 其他的：可以说"due to time constraints, left for future work"

#### 优先级 3：写最小复现文档（1 天）

    # 最小复现文档包含：
1. 环境说明（Python 版本、关键库版本）
2. 数据获取方式（链接或联系方式）
3. 运行命令（哪怕只有一个）
4. 预期结果（数值范围）
5. 已知问题（诚实说明复现困难）

### 如果距离 deadline 只剩 1 周

**残酷的真相**：你已经没时间重跑实验了。只能尽力补救记录。

    # 能做的（每项 2 小时）：
    [ ] 为所有论文实验补充 run.json（尽可能回忆）
    [ ] 把现有代码打上 Git tag（保存当前状态）
    [ ] 写最简单的复现说明（README 里一节）
    [ ] 把所有输出文件打包备份（防止丢失）

    # 不要做的（没时间了）：
    [ ] 不要试图重跑所有实验
    [ ] 不要试图建立完美的复现环境
    [ ] 不要试图修复所有不一致

**心态调整**：接受不完美，但确保最低可追溯性。论文能投出去比完美复现更重要。

### 事后补救

如果论文被接收，要求提供代码：

    # 你有 2-4 周时间补救

    Week 1：回溯和记录
- 找到所有论文相关的代码版本
- 尽力复现关键结果
- 记录所有"不一致"的地方

    Week 2-3：清理和验证
- 清理代码（删除不相关部分）
- 补充文档和注释
- 确保至少 1-2 个结果能复现

    Week 4：打包和发布
- 把代码整理成可发布形式
- 写清晰的 README
- 在论文里诚实说明复现的限制

## 10 分钟动作：今天就做的自查

如果你现在只做一件事：对当前项目做一次最小自查。

1.  **找到最重要的实验**（1 分钟）

          问自己：如果只能保留一个实验结果，是哪个？
          写下它的 run_id（如果没有，现在就给它创建一个）

2.  **检查记录完整性**（3 分钟）

          [ ] 有 run.json 吗？
          [ ] 知道用的哪个 Git commit 吗？
          [ ] 知道用的哪个 config 吗？
          [ ] 知道随机种子吗？
          [ ] 知道数据版本吗？

          任何一项缺失，立刻补救（写在笔记里也行）

3.  **快速复现测试**（5 分钟）

          # 用小数据测试流程能否跑通
          python train.py \
              --config <你的config> \
              --data_subset 100 \
              --epochs 2

          如果报错，记录错误信息，下次工作时优先修复

4.  **设定下次自查时间**（1 分钟）

          在日历里加入：
          - 每周五 17:00：可复现性自查（15 分钟）
          - 每月最后一天：债务盘点（30 分钟）
          - [项目开始 + 3个月]：建立复现基线（1 小时）

完成这个 10 分钟自查后，你会得到两个重要成果：

1.  **心里有底**：你知道项目的核心成果是可追溯的

2.  **提前预警**：如果发现问题，你还有时间修复

## 本章总结：预防胜于救火

最后阶段爆炸的根本原因是：**把验证推迟到了最后才做**。

正确的心态是：

- **不要等"确定能用"才记录**——任何"看起来不错"的结果都要立刻记录

- **不要等"写论文"才验证复现性**——日常就要持续验证

- **不要等"审稿人要求"才补实验**——提前识别验证债，主动补齐

**三个提前动作是你的保险**：

1.  每周自查：确保最近的工作可追溯（15 分钟）

2.  每月盘点：确保债务不失控（30 分钟）

3.  提前建立复现基线：确保最后阶段不手忙脚乱（1 小时）

总计每月投入时间：15 分钟 × 4 + 30 分钟 + 1 小时（首次）= 2.5 小时

这 2.5 小时的投入，可以避免最后阶段的 **3 天到 3 周的救火时间**。

**记住：研究的不确定性不可避免，但最后阶段的爆炸是可以预防的。**
