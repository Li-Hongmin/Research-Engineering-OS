# Content Review Checklist

**Purpose**: 系统化的内容质量审查指南（用于 text-book 和 manga-book）  
**Created**: 2026-02-07 00:06 JST  
**Maintainer**: REOS Team

---

## 📋 使用方法

1. 每次发布前运行完整检查
2. 日常改进时根据需要选择性检查
3. 新增内容时至少检查相关章节
4. 复制本 checklist 到 GitHub Issue/PR 作为审查模板

---

## 🔤 术语一致性检查

### 核心概念术语
- [ ] **Research Engineering** - 中文译法统一（研究工程 / 科研工程）
- [ ] **Reproducibility** - 中文译法统一（可重现性 / 可复现性）
- [ ] **Computational Thinking** - 计算思维（三语言一致）
- [ ] **Version Control** - 版本控制（不使用"版本管理"）
- [ ] **Continuous Integration** - 持续集成（CI，不译作"连续集成"）

### 工具名称
- [ ] Git/GitHub/GitLab - 保持英文，不翻译
- [ ] Docker/Kubernetes - 保持英文
- [ ] Python/R/Julia - 保持英文
- [ ] Markdown/LaTeX - 保持英文

### 人物名称
- [ ] 小研（Xiao Yan）- manga-book 主角
- [ ] 导师（Professor/Advisor）- 称呼统一
- [ ] 同学/同事 - 配角命名一致

### 检查方法
```bash
# 搜索可能不一致的术语
cd text-book
grep -rn "研究工程\|科研工程" src*/
grep -rn "可重现\|可复现" src*/
```

---

## 💻 代码示例检查

### 可运行性
- [ ] 所有代码示例可以复制粘贴运行
- [ ] 依赖包版本明确（或使用最新稳定版）
- [ ] 文件路径使用相对路径或占位符
- [ ] 环境变量和配置有说明

### 语法正确性
- [ ] Python 代码符合 PEP 8 风格
- [ ] Shell 脚本可在 Bash 4+ 运行
- [ ] YAML/JSON 格式正确（可用 linter 验证）

### 注释和说明
- [ ] 关键步骤有中文注释（中文版）
- [ ] 关键步骤有英文注释（英文版）
- [ ] 复杂算法有伪代码或流程图
- [ ] 输出示例准确（不过时）

### 检查工具
```bash
# Python 代码检查
find text-book/src -name "*.md" -exec grep -l "```python" {} \; | \
  xargs -I {} sh -c 'echo "Checking {}"; grep -A 20 "```python" {}'

# Shell 脚本检查
shellcheck script.sh
```

---

## 📚 引用与参考

### 学术引用
- [ ] 论文引用格式统一（APA / IEEE / Nature）
- [ ] DOI 链接有效
- [ ] 作者名拼写正确
- [ ] 年份和期刊信息准确

### 网络资源
- [ ] 外部链接有效（不是 404）
- [ ] 官方文档链接指向最新版本
- [ ] GitHub 仓库链接指向正确分支/tag
- [ ] 避免使用短链接（bit.ly 等）

### 引用格式示例
```markdown
<!-- 学术论文 -->
[1] Smith, J. et al. (2024). "Title". *Nature*, 123(4), 567-589. DOI: 10.1038/xxx

<!-- 在线文档 -->
[Git Documentation](https://git-scm.com/doc) (访问日期: 2026-02-07)

<!-- GitHub 项目 -->
[Project Name](https://github.com/user/repo/tree/v1.0.0) (v1.0.0)
```

### 检查工具
```bash
# 使用已有的链接检查脚本
bash check_links.sh --fast  # 快速模式（跳过外部链接）
bash check_links.sh         # 完整模式（检查外部链接）
```

---

## 🖼️ 图片与多媒体

### 图片质量
- [ ] 分辨率适合网页显示（宽度 800-1200px）
- [ ] 文件大小合理（< 500KB per image）
- [ ] 格式选择合理（PNG for diagrams, JPG for photos）
- [ ] 无水印或版权问题

### Alt Text 和标题
- [ ] 所有图片有 alt text（accessibility）
- [ ] Alt text 描述图片内容（不是"图片"或"image"）
- [ ] 重要图表有详细说明

### 路径和组织
- [ ] 图片路径使用相对路径
- [ ] 图片按章节组织（`images/01-intro/`, `images/02-git/`）
- [ ] 文件命名规范（`01_workflow_diagram.png`，不是`屏幕快照.png`）

### manga-book 特定检查
- [ ] 所有漫画图片存在（`check_manga_images.sh`）
- [ ] 图片顺序正确（`00_001.png` → `00_002.png` ...）
- [ ] 三语言版本使用相同图片（路径统一）

### 检查工具
```bash
# 检查漫画图片完整性
bash check_manga_images.sh

# 检查图片文件大小
find manga-book/images -name "*.png" -size +500k

# 检查缺失 alt text
grep -rn "!\[\](" text-book/src*/
```

---

## 🌐 多语言一致性

### 章节结构
- [ ] 三语言版本章节数量相同
- [ ] SUMMARY.md 结构一致
- [ ] 章节标题翻译准确

### 内容完整性
- [ ] 关键段落不缺失
- [ ] 代码示例三语言都存在
- [ ] 图片引用三语言一致

### 翻译质量
- [ ] 术语翻译一致（见上方术语表）
- [ ] 语句通顺自然
- [ ] 无机器翻译痕迹（如"的话"过多）
- [ ] 文化适配（举例、比喻符合目标语言习惯）

### 检查工具
```bash
# 使用翻译同步检查脚本
bash check_translation_sync.sh

# 对比章节数量
ls text-book/src/*.md | wc -l
ls text-book/src_en/*.md | wc -l
ls text-book/src_ja/*.md | wc -l
```

---

## 📖 叙事与故事连贯性（manga-book 专用）

### 故事结构
- [ ] 开头引人入胜（00-preface 设定清晰）
- [ ] 情节推进自然（章节之间有过渡）
- [ ] 高潮和冲突合理（不突兀）
- [ ] 结尾有启发性（不虎头蛇尾）

### 角色发展
- [ ] 小研的成长弧线清晰
- [ ] 导师/同学的性格一致
- [ ] 对话符合角色设定
- [ ] 情绪变化有铺垫

### 技术与故事平衡
- [ ] 技术点融入剧情（不是教科书式灌输）
- [ ] 对话自然（不是"老师讲课"）
- [ ] 幽默和情感恰当

---

## ✅ Markdown 格式与风格

### 标题层级
- [ ] 使用正确的标题层级（# → ## → ###）
- [ ] 避免跳级（# 后直接 ###）
- [ ] 标题简洁有力（5-10 字为佳）

### 列表和格式
- [ ] 列表项使用统一符号（`-` 或 `*`，不混用）
- [ ] 代码块指定语言（```python，不是```）
- [ ] 强调使用 **粗体** 或 *斜体*（不过度使用）

### 链接和交叉引用
- [ ] 内部链接使用相对路径
- [ ] 章节引用清晰（"见第 3 章"）
- [ ] 避免"点击这里"式链接

### 检查工具
```bash
# 使用 Markdown lint 检查
bash check_markdown_lint.sh

# 检查未闭合的 HTML 标签
grep -rn "<[a-z]" text-book/src*/ | grep -v "<http"
```

---

## 🎯 用户体验

### 可读性
- [ ] 段落长度适中（3-5 句）
- [ ] 避免长句（超过 30 字拆分）
- [ ] 技术术语首次出现时有解释

### 导航和结构
- [ ] 每章开头有简介
- [ ] 每章结尾有小结
- [ ] 交叉引用清晰

### 示例和练习
- [ ] 每章至少一个实战示例
- [ ] 练习题难度适中
- [ ] 有参考答案或提示

---

## 🔄 CI/CD 集成检查

### 自动化测试
- [ ] Health Check workflow 通过
- [ ] Markdown lint 通过
- [ ] GitHub Pages 部署成功

### 预发布检查
- [ ] 本地 `mdbook build` 无警告
- [ ] 所有 checklist 项目已检查
- [ ] Git commit message 清晰

---

## 📝 使用示例

### 发布前完整检查
```bash
cd /path/to/Research-Engineering-OS-

# 1. 运行健康检查
bash check_health.sh

# 2. 检查 Markdown 格式
bash check_markdown_lint.sh

# 3. 检查链接有效性
bash check_links.sh --fast

# 4. 检查翻译同步
bash check_translation_sync.sh

# 5. 检查漫画图片
bash check_manga_images.sh

# 6. 手动检查本 checklist 其他项目
```

### 日常改进时
- 修改单个章节 → 检查该章节相关项
- 添加新图片 → 检查图片质量和 alt text
- 翻译新内容 → 检查多语言一致性

---

## 🔖 参考资源

- [mdBook Documentation](https://rust-lang.github.io/mdBook/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG21/quickref/)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)

---

**维护记录**:
- 2026-02-07 00:06 - 初始创建
