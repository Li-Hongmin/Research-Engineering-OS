# QUICKSTART - 快速上手指南

**目标读者**：想快速开始贡献的新手（5-10 分钟上手）  
**详细指南**：[CONTRIBUTING.md](./CONTRIBUTING.md)（完整贡献指南）

---

## ⚡ 三步开始

### 1️⃣ 准备环境（2 分钟）

```bash
# 克隆仓库
git clone https://github.com/li-hongmin/Research-Engineering-OS.git
cd Research-Engineering-OS

# 检查环境（自动检测依赖）
make health
```

**需要的工具**：
- Git
- mdBook（`cargo install mdbook`，或 [官方安装](https://rust-lang.github.io/mdBook/guide/installation.html)）

---

### 2️⃣ 本地预览（1 分钟）

```bash
# 构建所有版本
make build

# 本地预览（选一个）
make serve-text    # 文本版（http://localhost:8000）
make serve-manga   # 漫画版（http://localhost:8001）
```

浏览器访问 `http://localhost:8000` 即可看到效果。

---

### 3️⃣ 做出修改（3-5 分钟）

```bash
# 编辑文件（举例）
vim text-book/src/01-intro.md      # 中文内容
vim text-book/src_en/01-intro.md   # 英文内容

# 检查质量（提交前必做）
make test    # = make check-all

# 提交修改（自动运行健康检查）
make commit  # 交互式提交助手
```

**提交消息格式**：
- `content: 修复第3章的代码示例`
- `docs: 更新贡献指南`
- `fix: 修复图片路径错误`

---

## 🎯 常见贡献类型

### 📝 修复内容错误

1. **找到文件**：
   - 文本版中文：`text-book/src/`
   - 文本版英文：`text-book/src_en/`
   - 文本版日文：`text-book/src_ja/`
   - 漫画版：`manga-book/src/`（三语言同理）

2. **直接编辑** → `make test` → `make commit`

---

### 🌍 翻译内容

```bash
# 检查哪些内容需要翻译
make check-translation

# 手动翻译（编辑 src_en/ 或 src_ja/）
vim text-book/src_en/05-dod.md

# 或使用自动翻译脚本（需配置 Azure API）
python translate_manga_azure_batch.py
```

---

### 🖼️ 添加/修复图片

```bash
# 检查图片引用
make check-manga

# 添加图片到正确位置
# text-book: text-book/images/
# manga-book: manga-book/images/

# 更新 Markdown 引用
![描述](../images/your-image.png)
```

---

### ✨ 改进建议

```bash
# 查看改进建议列表
cat IMPROVEMENTS.md

# 添加你的想法
echo "## 新想法标题\n\n描述..." >> IMPROVEMENTS.md
```

---

## 🚀 高级操作

### 查看所有可用命令
```bash
make help
```

### 运行单个检查
```bash
make health              # 健康检查
make lint                # Markdown 格式
make check-links         # 链接有效性
make check-translation   # 翻译同步
make check-consistency   # 内容一致性
```

### 查看项目统计
```bash
make stats    # 文件数、字数、图片数等
```

---

## 📚 进阶学习

| 主题 | 文档 |
|------|------|
| **详细贡献指南** | [CONTRIBUTING.md](./CONTRIBUTING.md) |
| **行为准则** | [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) |
| **术语表** | [GLOSSARY.md](./GLOSSARY.md) |
| **所有文档索引** | [DOCS_INDEX.md](./DOCS_INDEX.md) |
| **项目状态** | [STATUS.md](./STATUS.md) |
| **待办任务** | [TODO.md](./TODO.md) |

---

## 🆘 遇到问题？

### 常见问题

**Q: `make health` 失败？**  
A: 检查是否安装了 mdBook：`mdbook --version`

**Q: 构建失败？**  
A: 删除旧的构建产物：`make clean`，然后重新 `make build`

**Q: 图片显示不出来？**  
A: 运行 `make check-manga` 检查路径是否正确

**Q: 翻译内容不同步？**  
A: 运行 `make check-translation` 查看缺失的翻译

### 获取帮助

- **GitHub Issues**：[报告问题](https://github.com/li-hongmin/Research-Engineering-OS/issues)
- **GitHub Discussions**：[提问讨论](https://github.com/li-hongmin/Research-Engineering-OS/discussions)
- **邮件**：lihongmin@edu.k.u-tokyo.ac.jp

---

## ✅ 检查清单

开始贡献前，确保：
- [ ] 已安装 Git 和 mdBook
- [ ] 能成功运行 `make health`（GOOD 或 EXCELLENT）
- [ ] 能本地预览（`make serve-text` 或 `make serve-manga`）
- [ ] 了解提交消息格式（`content:`、`docs:`、`fix:` 等）

准备好了？开始贡献吧！🚀

---

**创建时间**：2026-02-07 20:15 JST  
**维护原则**：保持简洁（5-10 分钟可读完），详细内容链接到其他文档  
**最后更新**：2026-02-07 20:15 JST
