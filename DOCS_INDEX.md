# REOS 项目文档索引

**目的**：快速导航项目文档，了解每个文件的作用和使用场景

**创建时间**：2026-02-06 23:07 JST  
**维护原则**：新增重要文档时更新此索引

---

## 📋 核心项目文档

### 用户面向文档

| 文档 | 用途 | 目标读者 |
|------|------|---------|
| **README.md** | 项目概览、快速开始、内容结构 | 所有人（首次访问者） |
| **QUICKSTART.md** | 5-10 分钟快速上手指南（新贡献者） | 想快速开始贡献的新手 |
| **FAQ.md** | 常见问题解答（安装、使用、贡献、调试） | 遇到问题的用户和贡献者 |
| **text-book/README.md** | 文本版使用指南 | 想阅读多语言文本版的读者 |
| **manga-book/README.md** | 漫画版使用指南 | 想阅读漫画版的读者 |
| **GLOSSARY.md** | 术语表、关键概念定义 | 需要查找术语含义的读者 |

### 贡献者文档

| 文档 | 用途 | 目标读者 |
|------|------|---------|
| **CONTRIBUTING.md** | 贡献指南（5种贡献方式 + 完整工作流程） | 新贡献者、开发者 |
| **CODE_OF_CONDUCT.md** | 社区行为准则（Contributor Covenant 2.1） | 所有社区成员 |
| **CONTENT_REVIEW_CHECKLIST.md** | 系统化内容审查清单（8 大领域） | 内容审查者、质量保障团队 |
| **IMPROVEMENTS.md** | 改进建议收集、优先级排序 | 内容贡献者、维护者 |
| **TODO.md** | 待办任务追踪（短/中/长期） | 项目维护者、REOS 自动化 |
| **STATUS.md** | 实时项目状态、每小时工作日志 | 项目维护者、REOS 自动化 |
| **CLAUDE.md** | Claude 工作上下文和指导 | AI 助手、维护者 |

### 项目管理文档

| 文档 | 用途 | 目标读者 |
|------|------|---------|
| **ARCHITECTURE.md** | 项目架构、技术栈、设计决策、目录结构 | 新贡献者、维护者、架构师 |
| **CHANGELOG.md** | 项目变更日志（Keep a Changelog 格式） | 用户、贡献者、维护者 |
| **LICENSE_GUIDE.md** | 许可证选择指南（5种许可证对比 + 推荐） | 项目维护者、Fork 项目者 |
| **MAINTENANCE.md** | 项目维护指南（日常、周报、构建、故障排查） | 项目维护者、REOS 自动化、运维人员 |

### 技术报告文档

| 文档 | 用途 | 目标读者 |
|------|------|---------|
| **MANGA_I18N_FINAL_REPORT.md** | 漫画版多语言翻译最终报告 | 翻译团队、维护者 |
| **MANGA_I18N_REPORT.md** | 漫画版多语言翻译初步报告 | 翻译团队、维护者 |

---

## 🔧 自动化工具脚本

### 构建与命令管理

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| **Makefile** | 统一命令入口（20+ 命令：构建、检查、开发、Git） | 所有开发任务（推荐优先使用） |

### 健康检查与验证

| 脚本 | 功能 | 使用场景 |
|------|------|---------|
| **check_health.sh** | 全面项目健康检查（Git、构建、图片、文档） | 提交前、CI/CD、定期检查 |
| **check_markdown_lint.sh** | Markdown 质量检查（HTML标签、空格、图片alt） | 提交前、CI/CD |
| **check_links.sh** | 链接有效性检查（内部+外部） | 定期检查、发布前 |
| **check_manga_images.sh** | 漫画图片引用完整性检查 | manga-book 修改后 |
| **check_translation_sync.sh** | 三语言版本同步状态检查 | 翻译后、发布前 |
| **check_content_consistency.sh** | 三语言内容一致性检查（结构、章节、代码块、图片） | 发布前、定期检查 |

### 翻译工具

| 脚本 | 功能 | 使用场景 |
|------|------|---------|
| **translate_manga_azure_batch.py** | 批量翻译漫画版（Azure API） | 大规模翻译任务 |
| **translate_manga_azure.py** | 单个翻译漫画版（Azure API） | 小规模翻译任务 |
| **translate_manga_safe.py** | 安全翻译脚本（带验证） | 生产环境翻译 |
| **translate_summary.py** | 翻译摘要统计 | 翻译进度追踪 |

### 测试脚本

| 脚本 | 功能 | 使用场景 |
|------|------|---------|
| **test_azure.py** | 测试 Azure API 连接 | 调试 Azure 配置 |
| **test_translate_small.py** | 小规模翻译测试 | 翻译功能验证 |

---

## 📂 目录结构说明

### text-book/
```
text-book/
├── src/              # 中文内容（主版本）
├── src_en/           # 英文翻译内容
├── src_ja/           # 日文翻译内容
├── images/           # 共享图片资源（三语言共用）
├── manga/            # 插图生成资源
├── theme/            # mdBook 自定义主题
├── build_all.sh      # 三语言构建脚本
└── book/             # 构建输出目录（git ignored）
```

### manga-book/
```
manga-book/
├── src/              # 漫画版 markdown（中文）
├── src_en/           # 漫画版英文翻译
├── src_ja/           # 漫画版日文翻译
├── images/           # 漫画图片资源（按章节组织）
├── theme/            # mdBook 自定义主题
└── book/             # 构建输出目录（git ignored）
```

### shared/
```
shared/
└── theme/            # 共享的 mdBook 主题文件
    ├── language-switcher.js
    ├── version-switcher.js
    └── ...
```

### .github/
```
.github/
└── workflows/
    ├── health-check.yml        # 健康检查 CI
    └── pages.yml               # GitHub Pages 部署
```

---

## 🔄 文档使用流程

### 新贡献者上手流程

1. **快速开始** → QUICKSTART.md（5-10 分钟上手）
2. **阅读** README.md（了解项目）
3. **查看** TODO.md（找待办任务）
4. **运行** check_health.sh（验证环境）
5. **参考** IMPROVEMENTS.md（了解改进方向）
6. **更新** STATUS.md（记录工作）

### 内容改进流程

1. **记录想法** → IMPROVEMENTS.md
2. **讨论优先级** → 标记为高/中/低
3. **排入计划** → TODO.md（短期/中期/长期）
4. **执行任务** → 修改内容文件
5. **验证质量** → 运行相关检查脚本
6. **提交修改** → Git commit（pre-commit hook 自动检查）
7. **记录完成** → STATUS.md + TODO.md

### 翻译工作流程

1. **检查同步** → check_translation_sync.sh
2. **识别缺失** → 比对三语言版本
3. **执行翻译** → translate_manga_azure_batch.py
4. **验证质量** → 手动审查 + check_markdown_lint.sh
5. **确认同步** → check_translation_sync.sh（再次验证）
6. **提交修改** → Git commit

---

## 🎯 快速查找指南

### "我想..."

- **快速上手（新手）** → QUICKSTART.md（5-10 分钟）
- **了解项目** → README.md
- **解决常见问题** → FAQ.md（安装、使用、贡献、调试）
- **开始贡献** → CONTRIBUTING.md（完整贡献指南）
- **理解术语** → GLOSSARY.md
- **提改进建议** → IMPROVEMENTS.md
- **查看项目状态** → STATUS.md
- **查看所有可用命令** → `make help`（推荐）
- **检查项目健康** → `make health`（或 `bash check_health.sh`）
- **运行所有检查** → `make check-all`
- **构建所有版本** → `make build`
- **验证翻译同步** → `make check-translation`（或 `bash check_translation_sync.sh`）
- **检查链接有效性** → `make check-links`（或 `bash check_links.sh`）
- **检查三语言一致性** → `make check-consistency`（或 `bash check_content_consistency.sh`）

### "我遇到..."

- **构建失败** → 运行 check_health.sh，查看具体错误
- **图片显示问题** → 运行 check_manga_images.sh
- **翻译不同步** → 运行 check_translation_sync.sh
- **Markdown 格式问题** → 运行 check_markdown_lint.sh
- **不知道下一步** → 查看 TODO.md 短期任务

---

## 📝 文档维护约定

### 优先级

1. **README.md** - 始终保持最新（项目门面）
2. **STATUS.md** - 每小时更新（REOS 工作日志）
3. **TODO.md** - 任务完成时更新（待办追踪）
4. **IMPROVEMENTS.md** - 收集想法时更新（改进建议）
5. **DOCS_INDEX.md** - 新增重要文档时更新（本文件）

### 命名约定

- **大写 .md** - 项目级文档（README, TODO, STATUS等）
- **小写 .sh** - 可执行脚本
- **小写 .py** - Python 工具脚本
- **小写目录** - 内容目录（text-book, manga-book, shared）

### 提交约定

- 文档修改：`docs: [description]`
- 内容修改：`content: [description]`
- 工具脚本：`tools: [description]`
- 修复问题：`fix: [description]`
- 自动化改进：`ci: [description]`

---

## 🔗 外部链接

- **GitHub 仓库**：https://github.com/li-hongmin/Research-Engineering-OS
- **在线阅读（主站）**：https://li-hongmin.github.io/Research-Engineering-OS/
- **在线阅读（英文版）**：https://li-hongmin.github.io/Research-Engineering-OS/en/
- **在线阅读（日文版）**：https://li-hongmin.github.io/Research-Engineering-OS/ja/
- **在线阅读（漫画版）**：https://li-hongmin.github.io/Research-Engineering-OS/manga/

---

**维护说明**：
- 新增重要文档时更新"核心项目文档"部分
- 新增工具脚本时更新"自动化工具脚本"部分
- 工作流程变化时更新"文档使用流程"部分
- 保持"快速查找指南"的实用性

**Last Updated**: 2026-02-09 13:06 JST  
**Version**: 2.5 - 新增 MAINTENANCE.md（项目维护指南）
