# 术语对照表 (Glossary)

本文档记录项目中关键术语的标准译法，确保三语版本的一致性。

## 核心概念 | Core Concepts | 核心概念

| 中文 | English | 日本語 | 说明 |
|------|---------|---------|------|
| 实验 | experiment | 実験 | 研究工作的基本单元 |
| 探索债务 | exploration debt | 探索債務 | 未整理的探索路径 |
| 验证债务 | validation debt | 検証債務 | 缺失的验证步骤 |
| 复现债务 | reproducibility debt | 再現債務 | 无法复现的实验 |
| 完成定义 | Definition of Done | 完了定義 | 实验完成的标准 |
| DoD | DoD | DoD | "完成定义"的缩写 |

## Git 相关 | Git Terms | Git 用語

| 中文 | English | 日本語 | 说明 |
|------|---------|---------|------|
| 提交 | commit | コミット | Git commit |
| 分支 | branch | ブランチ | Git branch |
| 标签 | tag | タグ | Git tag |
| 合并 | merge | マージ | Git merge |

## 实验管理 | Experiment Management | 実験管理

| 中文 | English | 日本語 | 说明 |
|------|---------|---------|------|
| run_id | run_id | run_id | 实验运行标识符 |
| 路径 | path | パス | 实验探索路径 |
| 基线 | baseline | ベースライン | 对比基准 |
| 可复现 | reproducible | 再現可能 | 实验可重复性 |
| 可追溯 | traceable | 追跡可能 | 历史可追溯性 |

## 争议术语 | Ambiguous Terms | 曖昧な用語

以下术语可能有多种合理译法，需要根据上下文选择：

### "翻车"
- **推荐**：blows up at the end (英) / 最後に失敗する (日)
- 其他选项：fails, crashes, goes off the rails
- 说明：表示项目最后阶段的突然崩溃

### "路径"（实验探索路径）
- **推荐**：path (英) / パス (日)
- 其他选项：branch (当指代 Git 分支时)
- 说明：区分"实验路径"(path) 和 "Git 分支"(branch)

### "清理"
- **推荐**：cleanup (名词), clean up (动词)
- 其他选项：organize
- 说明：清理实验产物或代码

## 📐 写作规范

### 标题系统

本书使用**两级标题系统**：

1. **目录标题**（SUMMARY.md）：简洁、便于浏览
   - 例：`为什么总是最后翻车`
   
2. **文章标题**（.md 文件首行）：详细、说明性强
   - 例：`你为什么总在最后推翻（探索债 / 验证债 / 复现债）`

**规则**：
- ✅ 允许两级标题不完全相同
- ✅ 核心术语在两级标题中必须一致
- ❌ 禁止：同一概念在不同章节用不同术语

**示例**：
```markdown
# SUMMARY.md
- [为什么总是最后翻车](./01-why-flip.md)

# 01-why-flip.md
# 你为什么总在最后推翻（探索债 / 验证债 / 复现债）
```

### Definition of Done (DoD)

**英文规范**：
- ✅ 首次出现：**Definition of Done (DoD)**
- ✅ 后续提及：DoD
- ✅ 章节标题：Definition of Done
- ❌ 避免：definition of done (小写，除非在句中)

**日文规范**：
- ✅ 首次出现：**完了定義 (DoD)**
- ✅ 后续提及：DoD
- ✅ 章节标题：完了定義
- ❌ 避免：完了の定義（带助词"の"）

---

*最后更新：2026-02-06*
*维护者：Li Hongmin*
