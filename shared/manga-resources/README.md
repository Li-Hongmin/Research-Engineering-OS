# Research Engineering OS 漫画书

将《Research Engineering OS》转化为一本完整的漫画书，以故事驱动的方式呈现研究工程实践。

## 项目概述

- **主角**: 年轻研究员「小研」(Xiao Yan)，从菜鸟到高手的成长故事
- **叙事线**: 论文截止日前的危机 → 逐步学习研究工程实践 → 成功发表
- **风格**: 日式漫画，轻松幽默但内容硬核
- **总计**: 12章，264格漫画

## 目录结构

```
manga/
├── README.md              # 本文件
├── generate_manga.py      # 主生成脚本
├── storyboards/           # 分镜脚本 (YAML)
│   ├── 00-prologue.yaml
│   ├── 01-why-flip.yaml
│   └── ...
└── panels/                # 生成的漫画格子
    ├── 00-prologue/
    ├── 01-why-flip/
    └── ...
```

## 使用方法

### 1. 列出所有分镜脚本

```bash
python3 generate_manga.py --list
```

### 2. 生成特定章节

```bash
# 设置环境变量
source ~/.azure_openai_config

# 生成序章
python3 generate_manga.py --chapter 00-prologue

# 生成多个章节
python3 generate_manga.py --chapter 00-prologue 01-why-flip

# 使用更多并行线程
python3 generate_manga.py --chapter 00-prologue --workers 10
```

### 3. 生成全部章节

```bash
python3 generate_manga.py --all --workers 8
```

### 4. 强制重新生成

```bash
python3 generate_manga.py --chapter 00-prologue --force
```

### 5. 试运行（不实际生成）

```bash
python3 generate_manga.py --chapter 00-prologue --dry-run
```

## 分镜脚本格式

每个章节的分镜脚本使用YAML格式：

```yaml
chapter: "00-prologue"
title_zh: "截止日前3天"
title_en: "3 Days Before Deadline"

style_base: |
  Japanese manga illustration, clean anime art style...

panels:
  - id: "00_001"
    type: "establishing"
    description_zh: "深夜实验室，小研对着电脑"
    description_en: "Late night lab, Xiao Yan at computer"
    prompt: |
      Late night university research lab, young researcher...
```

## 章节目录

| 章节 | 漫画标题 | 格数 | 内容概要 |
|------|---------|------|---------|
| 00 | 截止日前3天 | 15 | 小研发现实验结果无法复现，三种债务怪兽出现 |
| 01 | 三种债务怪兽 | 25 | 深入了解探索债/验证债/复现债 |
| 02 | 实验才是单元 | 20 | 学会实验六要素 |
| 03 | 仓库大改造 | 25 | 整理混乱的代码结构 |
| 04 | Git侦探 | 25 | 用Git追溯问题根源 |
| 05 | 完成的定义 | 22 | 建立质量门 |
| 06 | 日志考古学 | 20 | 学会结构化记录 |
| 07 | AI助手的陷阱 | 25 | 与AI协作的正确姿势 |
| 08 | 多路探索 | 22 | 管理多条研究路径 |
| 09 | 炸弹拆除 | 25 | 提前预防截止日危机 |
| 10 | 团队协作 | 25 | 与团队成员配合 |
| 11 | 论文提交成功 | 15 | 小研的成长与收获 |
| **总计** | | **264** | |

## 环境要求

- Python 3.8+
- 依赖包：`pip install openai pyyaml requests`
- Azure OpenAI API 凭证（设置环境变量）

### 环境变量

```bash
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com"
export AZURE_OPENAI_API_VERSION="2024-08-01-preview"
```

## 生成时间估算

- 每张图片约10-15秒
- 使用8个并行线程
- 264张图片总计约 45-60 分钟

## 后续步骤

1. **审核**: 检查生成的图片风格一致性
2. **重生成**: 对不满意的图片使用 `--force` 重新生成
3. **排版**: 使用 `layout_manga.py` 生成漫画页面布局
4. **集成**: 将漫画集成到 mdBook 或独立发布
