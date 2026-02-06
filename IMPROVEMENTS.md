# Research-Engineering-OS 改进建议

**目的**：基于读者反馈和实际使用，收集让书更好的改进想法

**原则**：先不改原文，统一收集后再批量处理

---

## 📋 待改进清单

### 高优先级 (High Priority)

#### 1. 第一章开场：增加生动案例引起共鸣

**当前问题**：
- 第一章 "为什么总是最后翻车" 开场比较抽象
- 直接讲"三种债务"，读者可能没有直观感受
- 缺少"这就是我！"的共鸣时刻

**建议改进**：
在第一章开头（三种债务定义之前）加入具体场景描写：

```markdown
## 你是否经历过这样的场景？

### 场景一：文件命名的噩梦

截止日期前三天，你打开项目文件夹：

\`\`\`
model_test.py
model_final.py
model_final_v2.py
model_backup2.py
model_backup_backup.py
model_real_final.py
model_final_fixed.py
\`\`\`

你盯着这些文件名，陷入沉思：

- 论文 Figure 3 的结果是哪个版本生成的？
- `backup2` 是在 `backup_backup` 之前还是之后？
- 为什么有两个 `final`？

你打开 Git 历史寻找线索：

\`\`\`
commit a3f5e8d "test"
commit b72c91a "fix"  
commit c8d4f2e "update"
commit d9e1a3b "final version"
commit e2f4b7c "real final this time"
\`\`\`

Git 也帮不了你。

### 场景二："昨天还能跑"

三个月后，审稿人要求补充实验。你充满信心地运行代码：

\`\`\`bash
$ python train.py
Error: module 'numpy' has no attribute 'int'
\`\`\`

什么？三个月前明明可以的！你开始排查：

- ❌ Conda 环境被更新了（什么时候？为什么？）
- ❌ 数据预处理脚本"临时修改"过，但没提交
- ❌ 随机种子？好像没记录...
- ❌ 配置文件有三个版本：`config_backup.json`、`config_backup_old.json`、`config_final.json`

两周过去了，rebuttal 截止日期已过。

### 场景三：方向错了

你花了两周实现一个复杂的图神经网络：
- 3000+ 行自定义代码
- 精心设计的注意力机制
- 完整的训练 pipeline

第三周，你终于跑完整个实验：

\`\`\`
Our GNN:      78.3% accuracy
Baseline (LR): 82.1% accuracy
\`\`\`

什么？还不如 logistic regression？

更糟的是：如果在第一天花 30 分钟做个快速原型测试，就能发现这个方向行不通。现在，两周的工作全部作废。

---

**如果以上场景你经历过任何一个，那这本书就是为你写的。**
\`\`\`

**预期效果**：
- ✅ 读者立即产生共鸣："这说的就是我！"
- ✅ 建立情感连接，愿意继续读下去
- ✅ 自然过渡到"三种技术债"的理论框架

---

#### 2. Git 章节：增加"坏的 commit message"对比

**当前状态**：
- 第四章 "Git 作为证明" 讲了如何写好 commit
- 但没有展示"坏例子" vs "好例子"的对比

**建议改进**：
加入对比示例：

| 坏的 commit | 好的 commit |
|------------|------------|
| `"test"` | `"test: verify baseline model converges on toy dataset"` |
| `"fix bug"` | `"fix: correct data normalization in preprocessing (std was 0)"` |
| `"update"` | `"exp: add dropout=0.3 to reduce overfitting (run_23 → run_24)"` |
| `"final version"` | `"paper: freeze model weights for camera-ready (commit for Figure 3)"` |

---

### 中优先级 (Medium Priority)

#### 3. 增加"10分钟行动"的可操作性

**当前问题**：
- 每章结尾有"10分钟行动"
- 但有些还是偏抽象

**建议**：
加入"复制粘贴即用"的模板，比如：

```markdown
## 10分钟行动

### 步骤1：创建实验日志模板 (2分钟)

复制这段代码到 `experiments/template.md`：

\`\`\`markdown
# Run ID: {run_id}
Date: {date}
Commit: {git_commit}

## Hypothesis
[你在测试什么假设？]

## Configuration
- Model: 
- Data: 
- Key params: 

## Results
[结果截图或数字]

## Next Steps
[下一步做什么？]
\`\`\`

### 步骤2：运行一次实验并记录 (5分钟)
### 步骤3：提交到 Git (3分钟)
```

---

#### 4. 漫画版与文本版的互相引用

**建议**：
- 文本版每章开头加："🎨 想看漫画版？点击这里"
- 漫画版每章结尾加："📖 想了解技术细节？查看文本版"

---

### 低优先级 (Low Priority)

#### 5. 增加"常见问题"章节

收集读者常问的问题：
- "我的项目太小，需要这么复杂吗？"
- "团队不配合怎么办？"
- "我已经用了 MLflow，还需要 REOS 吗？"

---

## 📝 反馈来源

- [ ] 读者评论/Issues
- [ ] 实际使用案例
- [ ] Workshop/讲座反馈
- [x] 论文写作过程中的思考（2026-02-06）

---

## ✅ 已处理的改进

（暂无）

---

## 🚫 不采纳的建议

（记录为什么某些建议不适合，避免重复讨论）

---

**维护说明**：
- 新增建议时标注日期和来源
- 定期 review，决定哪些进入实施
- 实施后移到"已处理"区域

---

## 🔴 紧急/结构性改进

### 图片存储优化：消除重复副本

**当前问题**：
- 三个语言版本各自保存一份相同的图片
- `src/images/` - 235MB
- `src_en/images/` - 235MB  
- `src_ja/images/` - 235MB
- **总计：705MB 重复数据！**

**建议改进**：

```
text-book/
├── images/          # 共享图片（只保存一份）
├── src/             # 中文版 markdown
├── src_en/          # 英文版 markdown
└── src_ja/          # 日文版 markdown
```

所有 markdown 引用统一为 `../images/xxx.png`

**优点**：
- ✅ 节省 470MB 空间
- ✅ 图片维护更简单（改一次，三版本同步）
- ✅ Git 仓库更小，clone/push 更快
- ✅ 符合 DRY 原则

**实施步骤**：
1. 创建 `text-book/images/` 目录
2. 移动 `src/images/` 到 `text-book/images/`
3. 删除 `src_en/images/` 和 `src_ja/images/`
4. 批量修改所有 markdown 中的图片路径
5. 测试构建

**风险评估**：
- 需要修改所有 markdown 文件的图片引用
- 需要仔细测试三个语言版本的构建
- 建议在独立分支进行，测试通过后合并

**优先级**：高（节省空间，改善维护性）

---

## ✅ 已处理的改进

### 2026-02-06：图片存储优化

**实施时间**：2026-02-06 14:53

**完成内容**：
- ✅ 创建 `text-book/images/` 共享目录
- ✅ 移动 `src/images/` → `text-book/images/`
- ✅ 删除 `src_en/images/` 和 `src_ja/images/`
- ✅ 批量修改所有 markdown 图片路径为 `../images/`
- ✅ 测试三语言构建：全部通过
- ✅ Git commit: 6238986

**效果**：
- 之前：705MB（235MB × 3）
- 现在：235MB（1 份）
- **节省：470MB（67%）**

---
