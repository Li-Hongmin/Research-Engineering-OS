# REOS 常见问题解答 (FAQ)

**目的**：快速解答新用户和贡献者的常见问题  
**创建时间**：2026-02-09 12:06 JST  
**维护原则**：收集实际用户问题后持续更新

---

## 🚀 快速上手

### Q: 我是新手，应该从哪里开始？

**A**: 推荐三步走：

1. **5 分钟快速了解**：阅读 [QUICKSTART.md](QUICKSTART.md)
2. **深入了解项目**：浏览 [README.md](README.md)
3. **开始贡献**：查看 [CONTRIBUTING.md](CONTRIBUTING.md)

如果想直接体验，运行：
```bash
cd text-book
./build_all.sh
cd book && python -m http.server 8000
```

### Q: 项目有哪些版本？有什么区别？

**A**: REOS 有两个独立的版本：

| 版本 | 特点 | 适合人群 |
|------|------|---------|
| **text-book/** | 多语言文本版（中/英/日），技术深度更高 | 喜欢系统学习的研究者 |
| **manga-book/** | 中文漫画版，以小研的故事为主线 | 视觉学习者、喜欢故事的读者 |

两个版本内容相通但独立维护，可以根据个人偏好选择。

### Q: 如何快速验证项目是否正常？

**A**: 运行健康检查命令：

```bash
make health          # 使用 Makefile（推荐）
# 或者
./check_health.sh    # 直接运行脚本
```

如果看到 `✅ Project health: EXCELLENT`，说明一切正常！

---

## 📚 阅读与使用

### Q: 如何在本地阅读电子书？

**A**: 

**方法一：构建后本地预览**
```bash
# 文本版（全部三语言）
cd text-book
./build_all.sh
cd book && python -m http.server 8000

# 漫画版
cd manga-book
mdbook build
cd book && python -m http.server 8001
```

**方法二：在线阅读**
- 主站（中文）：https://li-hongmin.github.io/Research-Engineering-OS/
- 英文版：https://li-hongmin.github.io/Research-Engineering-OS/en/
- 日文版：https://li-hongmin.github.io/Research-Engineering-OS/ja/
- 漫画版：https://li-hongmin.github.io/Research-Engineering-OS/manga/

### Q: 我只想读某一个语言版本，可以单独构建吗？

**A**: 可以！

```bash
cd text-book

# 只构建中文版
mdbook build

# 只构建英文版
cd .. && mdbook build --dest-dir book/en

# 只构建日文版
cd .. && mdbook build --dest-dir book/ja
```

不过推荐使用 `./build_all.sh`，它会自动处理所有语言版本。

### Q: mdBook 是什么？需要安装吗？

**A**: mdBook 是一个 Rust 编写的静态网站生成器，专门用于生成电子书。

**安装方法**：
```bash
# macOS/Linux
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install mdbook

# 或者使用 Homebrew (macOS)
brew install mdbook
```

详见：https://rust-lang.github.io/mdBook/guide/installation.html

---

## 🤝 贡献与开发

### Q: 我想贡献内容，但不会写代码怎么办？

**A**: 完全没问题！REOS 有 **5 种贡献方式**（详见 [CONTRIBUTING.md](CONTRIBUTING.md)）：

1. **内容贡献** - 改进文字、案例、说明（无需写代码）
2. **翻译贡献** - 帮助翻译或审校（支持自动翻译）
3. **设计贡献** - 漫画插图、主题美化
4. **质量保障** - 测试、报告问题、审查内容
5. **社区建设** - 回答问题、分享经验

你可以从 Issue 报告、文档改进开始！

### Q: 我想修改内容，如何确保不破坏项目？

**A**: REOS 有完善的自动化检查系统：

**提交前**：
```bash
make check-all    # 运行所有质量检查
make health       # 快速健康检查
```

**提交时**：
- Pre-commit hook 会自动运行健康检查
- 如果有问题会阻止提交

**提交后**：
- GitHub Actions 自动运行 CI/CD
- PR 会自动显示检查结果

**建议工作流程**：
1. 修改文件
2. `make health` 快速验证
3. `git add` + `git commit`（自动检查）
4. 如果失败，修复问题后重试

### Q: 如何添加新的翻译语言版本？

**A**: 目前支持中文、英文、日文。如果要添加新语言：

1. 在 `text-book/` 下创建新目录（如 `src_fr/` for 法语）
2. 复制 `book.toml` 并修改语言设置
3. 翻译 Markdown 文件
4. 修改 `build_all.sh` 添加新语言构建
5. 更新 GitHub Actions 部署配置

详见：[CONTRIBUTING.md - 翻译工作流程](CONTRIBUTING.md#翻译工作流程)

---

## 🔧 工具与命令

### Q: `make` 命令和直接运行脚本有什么区别？

**A**: 

- **`make` 命令**（推荐）：统一入口，易记，自动检查依赖
- **直接运行脚本**：更灵活，可传参数

**示例**：
```bash
# 等价命令
make health          <==>  ./check_health.sh
make lint            <==>  ./check_markdown_lint.sh
make check-links     <==>  ./check_links.sh --fast
```

查看所有可用命令：
```bash
make help
```

### Q: 健康检查失败了，如何调试？

**A**: 健康检查包含 7 个子检查：

1. **Git 状态** - 工作树是否干净
2. **Git 同步** - 是否与远程同步
3. **text-book 构建** - 三语言版本是否完整
4. **manga-book 构建** - 漫画版是否存在
5. **漫画图片** - 图片资源是否完整
6. **核心文档** - 重要文档是否齐全
7. **依赖安装** - Python 虚拟环境是否就绪

**调试方法**：
```bash
./check_health.sh    # 查看详细输出，定位失败项

# 单独运行特定检查
./check_links.sh
./check_manga_images.sh
./check_markdown_lint.sh
```

常见问题：
- **构建缺失** → 运行 `make build`
- **Git 不同步** → 运行 `git pull` 或 `make sync`
- **图片缺失** → 检查 `manga-book/images/` 目录

### Q: 翻译工具如何使用？

**A**: REOS 提供 Azure API 批量翻译工具：

**批量翻译**（推荐用于大规模任务）：
```bash
python translate_manga_azure_batch.py \
  --source src/ \
  --target src_en/ \
  --lang en
```

**单个翻译**（用于小规模任务）：
```bash
python translate_manga_azure.py \
  --input src/chapter.md \
  --output src_en/chapter.md \
  --lang en
```

**验证翻译同步**：
```bash
make check-translation
# 或者
./check_translation_sync.sh
```

**注意**：需要配置 Azure API 密钥（见 `.env` 或环境变量）。

---

## 🐛 问题排查

### Q: 构建失败，提示 "mdbook: command not found"

**A**: 需要安装 mdBook：

```bash
# 使用 Cargo（Rust 包管理器）
cargo install mdbook

# 或者使用 Homebrew (macOS)
brew install mdbook
```

### Q: 图片无法显示/路径错误

**A**: 常见原因和解决方法：

1. **路径大小写** - Linux/macOS 区分大小写，Windows 不区分
   - 检查文件名大小写是否匹配
   
2. **相对路径错误** - manga-book 和 text-book 路径不同
   - manga-book: `../images/章节/图片.png`
   - text-book: `images/图片.png`

3. **图片缺失** - 运行检查脚本：
   ```bash
   make check-manga
   # 或者
   ./check_manga_images.sh
   ```

### Q: CI/CD 构建失败，但本地正常

**A**: 可能的原因：

1. **环境差异**
   - 本地有未提交的文件
   - GitHub Actions 使用 Ubuntu 环境

2. **依赖缺失**
   - 检查 `.github/workflows/` 配置
   - 确保所有依赖都在 `requirements.txt` 或工作流中

3. **权限问题**
   - 脚本没有执行权限
   - 运行：`chmod +x *.sh`

**调试方法**：
- 查看 GitHub Actions 日志
- 在干净环境（Docker）中测试
- 运行 `make check-all` 确保本地也能通过

### Q: Markdown 格式检查报错

**A**: 运行 Markdown lint 查看详情：

```bash
make lint
# 或者
./check_markdown_lint.sh
```

常见问题：
- **未闭合的 HTML 标签** - 使用反引号包裹：`` `<tag>` ``
- **尾随空格** - 编辑器配置自动删除
- **过度空行** - 保持最多 1 个空行
- **图片缺少 alt text** - 添加描述：`![描述](path.png)`

---

## 📖 内容相关

### Q: text-book 和 manga-book 的内容是同步的吗？

**A**: 

- **核心概念相同**：三大技术债务、实验为单元、默认行为等
- **表现形式不同**：
  - text-book：技术深度更高，适合系统学习
  - manga-book：故事化叙述，小研的成长经历

**不需要强制同步**，两者独立维护，互为补充。

### Q: 我发现了内容错误/改进建议，应该如何反馈？

**A**: 三种方式：

1. **GitHub Issue**（推荐）
   - 使用模板：Bug Report / Content Improvement
   - 详细描述问题和建议

2. **Pull Request**（直接修复）
   - Fork 仓库 → 修改 → 提交 PR
   - 遵循 [CONTRIBUTING.md](CONTRIBUTING.md) 指南

3. **记录到 IMPROVEMENTS.md**
   - 非紧急改进建议
   - 优先级排序后处理

### Q: 为什么选择 mdBook 而不是其他工具？

**A**: 

**优点**：
- ✅ 专为技术文档设计
- ✅ 支持 Markdown（易于编辑和版本控制）
- ✅ 搜索功能强大
- ✅ 多语言支持良好
- ✅ 快速构建
- ✅ 可定制主题

**缺点**：
- ❌ 需要 Rust 环境（安装略复杂）
- ❌ 不如 GitBook 商业化工具功能丰富

权衡后，mdBook 的简洁性和性能更适合 REOS 的需求。

---

## 🏢 项目管理

### Q: 项目的许可证是什么？

**A**: 

目前许可证 **待定**，正在评估中。

**推荐选项**：
- **CC-BY-4.0** - 允许商用，要求署名（教育友好）
- **CC-BY-SA-4.0** - 要求衍生品也开源
- **双许可证** - MIT（代码） + CC-BY-4.0（内容）

详见：[LICENSE_GUIDE.md](LICENSE_GUIDE.md)

### Q: 项目的长期规划是什么？

**A**: 查看 [TODO.md](TODO.md)：

- **短期**（1-2 天）：质量改进、翻译完善
- **中期**（1-2 周）：manga-book 故事增强、用户体验优化
- **长期**（1 个月+）：社区建设、插件开发、内容扩展

项目处于稳定维护期，重点是内容质量和社区建设。

### Q: 如何成为项目维护者？

**A**: 

目前项目由 **Li Hongmin（李鸿敏）** 维护。

成为维护者的路径：
1. 持续贡献（3+ 次有价值的 PR）
2. 展示责任感（代码审查、问题解答）
3. 熟悉项目架构和工具链
4. 与现有维护者沟通意愿

欢迎通过 Issues/Discussions 参与社区建设！

---

## 🔗 资源链接

### 项目链接
- **GitHub 仓库**：https://github.com/li-hongmin/Research-Engineering-OS
- **在线阅读（主站）**：https://li-hongmin.github.io/Research-Engineering-OS/
- **在线阅读（英文）**：https://li-hongmin.github.io/Research-Engineering-OS/en/
- **在线阅读（日文）**：https://li-hongmin.github.io/Research-Engineering-OS/ja/
- **在线阅读（漫画版）**：https://li-hongmin.github.io/Research-Engineering-OS/manga/

### 文档导航
- 📋 [DOCS_INDEX.md](DOCS_INDEX.md) - 完整文档索引
- ⚡ [QUICKSTART.md](QUICKSTART.md) - 快速上手
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - 项目架构
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- 📜 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - 行为准则

### 外部资源
- **mdBook 文档**：https://rust-lang.github.io/mdBook/
- **Markdown 指南**：https://www.markdownguide.org/
- **Git 入门**：https://git-scm.com/book/zh/v2

---

## 💡 还有问题？

- **搜索现有 Issues**：https://github.com/li-hongmin/Research-Engineering-OS/issues
- **提交新 Issue**：使用模板提问（Bug Report / Question）
- **GitHub Discussions**：一般性讨论和交流
- **Email**：lihongmin@edu.k.u-tokyo.ac.jp（复杂问题）

---

**维护说明**：
- 收集实际用户问题后持续更新
- 高频问题优先添加
- 保持答案简洁实用
- 定期审查过时内容

**Last Updated**: 2026-02-09 12:06 JST  
**Version**: 1.0 - 初始版本
