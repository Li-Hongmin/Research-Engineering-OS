# Research Engineering OS - mdBook版本

这是《Research Engineering OS: 把返工压缩成规范 + 模板 + 检查清单》的mdBook在线版本。

## 本地开发

### 安装依赖

```bash
# 安装mdBook
brew install mdbook

# 安装mdbook-pdf（用于生成PDF）
cargo install mdbook-pdf
```

### 构建和预览

```bash
# 构建HTML和PDF
mdbook build

# 本地预览（自动刷新）
mdbook serve

# 在浏览器中打开
open http://localhost:3000
```

### 文件结构

```
mdbook/
├── book.toml          # mdBook配置文件
├── src/               # Markdown源文件
│   ├── SUMMARY.md     # 目录结构
│   ├── README.md      # 首页
│   ├── 00-preface.md  # 前言
│   ├── 01-why-flip.md # 第1章
│   └── ...
├── theme/             # 自定义主题
│   └── custom.css     # 自定义CSS样式
└── book/              # 构建输出（git忽略）
    ├── html/          # HTML版本
    └── pdf/           # PDF版本
```

## 从LaTeX转换

如果需要重新从LaTeX源文件转换：

```bash
# 回到项目根目录
cd ..

# 运行转换脚本
python3 latex_to_mdbook.py

# 返回mdbook目录构建
cd mdbook
mdbook build
```

## 在线部署

### GitHub Pages

1. 在GitHub仓库设置中启用Pages
2. 选择 "GitHub Actions" 作为部署源
3. 推送到main分支即可自动部署

访问URL：`https://your-username.github.io/research-engineering-os/`

### 自定义域名

1. 在 `book.toml` 中设置 `cname = "yourdomain.com"`
2. 在DNS提供商添加CNAME记录指向 `your-username.github.io`
3. 在GitHub仓库设置中添加自定义域名

## KDP出版

生成的PDF文件位于 `book/pdf/output.pdf`，可以直接用于：
- Kindle Direct Publishing (KDP) 电子书
- KDP Print-on-Demand (POD) 纸质书

### PDF质量说明

mdbook-pdf使用Chrome headless渲染，质量适合电子阅读和POD印刷。如果需要更高质量的PDF（如专业印刷），可以继续使用LaTeX源文件生成。

## 双版本策略

- **在线版（mdBook）**：免费阅读，快速迭代，搜索功能
- **PDF版（LaTeX）**：高质量排版，KDP销售，收藏价值

## 贡献

欢迎提交Issue或Pull Request改进内容！

## 许可

© 2026 Li Hongmin (李鸿敏). All rights reserved.
