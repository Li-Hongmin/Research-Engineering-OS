# REOS Project Architecture

**Created**: 2026-02-07 22:05 JST  
**Purpose**: 阐明项目结构、设计决策和技术栈，帮助贡献者快速理解项目架构

---

## 🏗️ 项目概览

**Research-Engineering-OS (REOS)** 是一个三语言（中文、英文、日文）的研究工程实践指南，使用 mdBook 构建，采用"文字书 + 漫画书"双轨道设计。

**核心理念**：
- **可追溯性**：每个决策都可追溯到具体来源（文件、commit、脚本）
- **自动化优先**：能脚本化的绝不手动，减少人为错误
- **小步快跑**：每次改进都是小而可验证的增量
- **多语言友好**：三语言内容保持同步，单一来源构建多个目标

---

## 📂 目录结构

```
Research-Engineering-OS-/
│
├── 📚 text-book/               # 文字书（主内容）
│   ├── src/                    # 中文源文件
│   ├── src_en/                 # 英文源文件
│   ├── src_ja/                 # 日文源文件
│   ├── book.toml               # mdBook 配置（动态修改支持三语言）
│   └── build_all.sh            # 三语言构建脚本（动态切换 src 目录）
│
├── 📖 manga-book/              # 漫画书（图文版）
│   ├── src/                    # 中文源文件
│   ├── src_en/                 # 英文源文件
│   ├── src_ja/                 # 日文源文件
│   ├── images/                 # 漫画图片资源（共享）
│   ├── book.toml               # 构建配置
│   └── (build via mdbook build)
│
├── 🔧 自动化脚本/               # 质量保证与维护
│   ├── check_health.sh         # 综合健康检查（git、构建、依赖）
│   ├── check_links.sh          # 链接有效性检查
│   ├── check_translation_sync.sh # 三语言同步检查
│   ├── check_manga_images.sh   # 漫画图片完整性检查
│   ├── check_content_consistency.sh # 内容一致性检查
│   ├── check_markdown_lint.sh  # Markdown 质量检查
│   ├── project_stats.sh        # 项目统计信息
│   └── translate_*.py          # 翻译自动化工具
│
├── 📋 项目文档/                 # 元文档与指南
│   ├── README.md               # 项目入口（核心介绍）
│   ├── QUICKSTART.md           # 快速上手指南
│   ├── CONTRIBUTING.md         # 贡献者指南
│   ├── CODE_OF_CONDUCT.md      # 行为准则
│   ├── TODO.md                 # 待办事项（结构化追踪）
│   ├── STATUS.md               # 项目状态（实时更新）
│   ├── CHANGELOG.md            # 变更日志
│   ├── IMPROVEMENTS.md         # 改进建议
│   ├── GLOSSARY.md             # 术语表
│   ├── DOCS_INDEX.md           # 文档索引
│   ├── LICENSE_GUIDE.md        # 许可证选择指南
│   ├── CONTENT_REVIEW_CHECKLIST.md # 内容审查清单
│   ├── CLAUDE.md               # AI 辅助工作流说明
│   └── ARCHITECTURE.md         # 本文件（架构文档）
│
├── 🎨 共享资源/
│   └── shared/                 # 跨书籍共享的资源（CSS、模板等）
│
├── 🗄️ 归档/
│   └── archive/                # 旧版本、废弃文件
│
├── ⚙️ 配置文件/
│   ├── .editorconfig           # 编辑器统一配置
│   ├── .gitattributes          # Git 文件处理规则
│   ├── .gitignore              # Git 忽略规则
│   ├── Makefile                # 统一任务入口点
│   └── .github/                # GitHub 配置
│       └── workflows/          # CI/CD 流程
│           ├── deploy.yml      # 自动部署到 GitHub Pages
│           └── health-check.yml # 自动健康检查
│
└── 🐍 Python 环境/
    ├── .venv/                  # 主虚拟环境
    └── .venv_translate/        # 翻译工具专用环境
```

---

## 🧩 技术栈

### 核心工具
- **[mdBook](https://rust-lang.github.io/mdBook/)** (Rust): Markdown → HTML 静态站点生成器
  - 版本: 最新稳定版
  - 特性: 快速、轻量、支持多语言、搜索、主题定制
  
- **[GitHub Pages](https://pages.github.com/)**: 免费托管
  - 自动部署通过 `.github/workflows/deploy.yml`
  - 四个端点: 主站、英文站、日文站、漫画站

### 自动化与质量保证
- **Bash Shell**: 所有检查脚本（health、lint、links 等）
- **Python 3.x**: 翻译自动化、内容处理
  - 依赖管理: `pip` (requirements.txt 或按需安装)
  - Azure 翻译 API: 批量翻译、术语一致性
- **GNU Make**: 统一任务入口（`make help` 查看所有命令）
- **Git Hooks**: Pre-commit 自动运行健康检查

### CI/CD
- **GitHub Actions**: 自动化工作流
  - `deploy.yml`: 推送到 main → 自动构建 → 部署到 Pages
  - `health-check.yml`: 定期运行健康检查（检测 broken links、构建失败等）

---

## 🎨 设计决策

### 为什么双轨道（text-book + manga-book）？
**问题**: 不同读者有不同偏好  
- 学术/技术读者偏好纯文字
- 初学者/视觉学习者偏好图文并茂

**解决方案**: 两本书共享核心内容，但呈现方式不同  
- **text-book**: 传统技术书籍风格，深度内容，适合精读
- **manga-book**: 漫画形式，轻松易懂，适合快速入门

**技术实现**: 两个独立 mdBook 项目，共享 `shared/` 资源

---

### 为什么三语言？
**目标**: 让更多人受益（中国、日本、国际研究者）

**挑战**: 手动维护三份内容容易失步

**解决方案**:
1. **单一来源原则**: 中文为主源，英文/日文通过翻译工具生成初稿
2. **自动同步检查**: `check_translation_sync.sh` 定期检查三语言章节完整性
3. **术语表**: `GLOSSARY.md` 保证关键术语翻译一致
4. **独立构建配置**: 每种语言有独立 `book.toml`，支持本地化（语言选择器、搜索等）

**文件命名约定**:
- 中文: `src/` (默认)
- 英文: `src_en/`
- 日文: `src_ja/`

---

### 为什么选择 mdBook？
**对比**: Jekyll (Ruby)、Hugo (Go)、Docusaurus (React)、VuePress (Vue)

**mdBook 优势**:
- ✅ **专为技术书籍设计**: 导航、搜索、打印友好
- ✅ **极快构建速度**: Rust 实现，秒级构建
- ✅ **简单配置**: 单个 `book.toml` 文件
- ✅ **离线优先**: 生成的 HTML 可完全离线使用
- ✅ **无需运行时**: 纯静态 HTML，无 JavaScript 框架依赖
- ✅ **多语言友好**: 简单复制 `src/` → `src_en/` 即可

**权衡**:
- ❌ 不如 Docusaurus/VuePress 灵活（但我们不需要复杂交互）
- ❌ 插件生态较小（但核心功能已足够）

---

### 为什么用 Makefile？
**问题**: 多个脚本散落在项目中，新贡献者不知道如何操作

**解决方案**: 单一入口点 `make help`  
```bash
make health          # 健康检查
make build           # 构建所有版本
make test            # 运行所有测试
make commit          # 交互式提交（含预检查）
```

**好处**:
- 降低学习成本（不需要记忆脚本路径）
- 标准化工作流（团队协作一致）
- 自文档化（`make help` 即文档）

---

### 自动化脚本设计理念

#### 可组合性
每个脚本专注单一职责，可独立运行也可组合使用：
```bash
./check_health.sh      # 综合检查（调用下面所有脚本）
./check_links.sh       # 仅检查链接
./check_translation_sync.sh  # 仅检查翻译同步
```

#### 快速反馈
- **Fast mode**: 默认跳过耗时检查（如外部链接验证）
- **Full mode**: 完整检查（CI 使用）
```bash
./check_links.sh --fast    # 秒级反馈
./check_links.sh           # 分钟级完整检查
```

#### 可追溯性
所有脚本输出详细日志：
- ✅ 通过项显示绿色 `✓`
- ❌ 失败项显示红色 `✗` + 文件路径 + 行号
- 📊 生成总结报告（通过/失败/警告数量）

#### 幂等性
多次运行同一脚本结果相同（不产生副作用）

---

## 🔄 工作流

### 日常开发流程
1. **拉取最新代码**: `git pull` 或 `make sync`
2. **编辑内容**: 修改 `text-book/src/*.md` 或 `manga-book/src/*.md`
3. **本地预览**: `make serve-text` (http://localhost:8000)
4. **质量检查**: `make test` (运行所有检查)
5. **提交代码**: `git add .` → `git commit -m "..."` → `git push`
   - Pre-commit hook 自动运行健康检查
6. **自动部署**: GitHub Actions 检测到推送 → 构建 → 部署

### 添加新章节（三语言）
1. 编辑 `text-book/src/SUMMARY.md` 添加章节链接
2. 创建 `text-book/src/xx-new-chapter.md` (中文内容)
3. 翻译:
   ```bash
   python3 translate_manga_azure.py \
     --input text-book/src/xx-new-chapter.md \
     --output-en text-book/src_en/xx-new-chapter.md \
     --output-ja text-book/src_ja/xx-new-chapter.md
   ```
4. 手动校对翻译稿
5. 更新 `SUMMARY.md` (英文和日文版本)
6. 运行 `make check-translation` 验证同步性
7. 构建测试: `make build`
8. 提交

### 紧急修复流程
1. 识别问题: 通过 CI 失败、用户反馈、或定期检查
2. 创建 issue (可选，重大问题建议创建)
3. 修复问题
4. 验证修复: `make test`
5. 更新 `CHANGELOG.md` (如果是用户可见的变更)
6. 提交并推送

---

## 🧪 测试与验证

### 本地测试
```bash
make test          # 运行所有质量检查
make build         # 验证构建成功
```

### CI 测试
- **触发条件**: 推送到 `main` 分支
- **检查项**:
  - Git 状态
  - mdBook 构建（三语言）
  - 链接有效性
  - Markdown lint
  - 翻译同步性
  - 内容一致性

### 手动审查
使用 `CONTENT_REVIEW_CHECKLIST.md` 进行内容审查：
- 技术准确性
- 语言流畅性
- 图片质量
- 链接有效性
- 格式一致性

---

## 🚀 部署架构

### GitHub Pages 配置
- **主站**: https://username.github.io/Research-Engineering-OS-/
- **英文站**: https://username.github.io/Research-Engineering-OS-/en/
- **日文站**: https://username.github.io/Research-Engineering-OS-/ja/
- **漫画站**: https://username.github.io/Research-Engineering-OS-/manga/

### 部署流程
1. GitHub Actions 触发（推送到 main）
2. 运行健康检查（失败则终止部署）
3. 构建所有版本:
   - `cd text-book && ./build_all.sh`
   - `cd manga-book && mdbook build`
4. 复制构建产物到 `gh-pages` 分支
5. GitHub Pages 自动更新站点

### 回滚机制
- 构建失败 → 保留上一个成功版本
- Git 历史完整 → 可回退到任意 commit 重新部署

---

## 🔒 质量保证机制

### 多层检查
1. **Pre-commit hook**: 提交前自动检查
2. **CI/CD**: 推送后完整检查
3. **定期检查**: 每日运行健康检查（检测外部链接失效等）

### 失败快速原则
- 发现问题立即报告（不继续运行后续检查）
- 清晰的错误信息（文件路径 + 行号 + 问题描述）

### 可追溯性
- 每次检查记录时间戳
- 每个脚本输出标准化格式
- 所有变更通过 Git 追踪

---

## 🎯 设计原则总结

| 原则 | 实践 | 工具 |
|------|------|------|
| **可追溯性** | 所有决策记录在文档/commit | Git, STATUS.md, CHANGELOG.md |
| **自动化优先** | 脚本化所有重复任务 | Bash, Python, Makefile, GitHub Actions |
| **小步快跑** | 每次提交小而可验证 | Pre-commit hooks, CI 快速反馈 |
| **多语言友好** | 独立源文件 + 自动同步检查 | mdBook 多配置, check_translation_sync.sh |
| **质量保证** | 多层检查机制 | 7+ 检查脚本, CI/CD |
| **易于贡献** | 清晰文档 + 统一入口 | README, CONTRIBUTING, Makefile |

---

## 📚 延伸阅读

- **mdBook 官方文档**: https://rust-lang.github.io/mdBook/
- **GitHub Pages 文档**: https://docs.github.com/pages
- **GitHub Actions 文档**: https://docs.github.com/actions
- **项目贡献指南**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **快速上手**: [QUICKSTART.md](QUICKSTART.md)
- **项目文档索引**: [DOCS_INDEX.md](DOCS_INDEX.md)

---

## 🤝 贡献者注意事项

### 修改架构前请考虑
1. **是否符合 REOS 设计原则**？
2. **是否增加不必要的复杂度**？
3. **是否影响现有工作流**？
4. **是否有更简单的替代方案**？

### 重大架构变更流程
1. 在 GitHub Discussions 提出讨论
2. 创建设计文档（RFC 风格）
3. 获得核心贡献者共识
4. 小步实施（避免大爆炸式重构）
5. 更新本文档

---

**维护者**: REOS 项目团队  
**最后更新**: 2026-02-07 22:05 JST  
**反馈**: 发现问题？请提交 Issue 或 PR
