#!/usr/bin/env python3
"""
LaTeX to mdBook Conversion Script
将Research Engineering OS的LaTeX源文件转换为mdBook格式
"""

import os
import subprocess
import re
import shutil
from pathlib import Path

# 配置
LATEX_CHAPTERS_DIR = "chapters"
MDBOOK_SRC_DIR = "mdbook/src"
CHAPTER_FILES = [
    ("00_preface.tex", "00-preface.md", "前言"),
    ("01_why_flip.tex", "01-why-flip.md", "为什么总是最后翻车"),
    ("02_experiment_unit.tex", "02-experiment-unit.md", "实验才是单元"),
    ("03_repo_layout.tex", "03-repo-layout.md", "仓库结构"),
    ("04_git_proof.tex", "04-git-proof.md", "Git作为证据链"),
    ("05_dod.tex", "05-dod.md", "Definition of Done"),
    ("06_logging.tex", "06-logging.md", "日志"),
    ("07_ai_workflow.tex", "07-ai-workflow.md", "AI时代的工作流"),
    ("08_multi_path.tex", "08-multi-path.md", "多路探索"),
    ("no_boom.tex", "no-boom.md", "避免临deadline炸雷"),
    ("team.tex", "team.md", "团队协作"),
    ("templates.tex", "appendix-templates.md", "附录：模板"),
    ("ai_disasters.tex", "appendix-ai-disasters.md", "附录：AI灾难案例"),
]


def create_mdbook_structure():
    """创建mdBook项目结构"""
    print("📁 创建mdBook目录结构...")
    os.makedirs(MDBOOK_SRC_DIR, exist_ok=True)
    os.makedirs("mdbook/src/images", exist_ok=True)

    # 复制图片
    if os.path.exists("diagram.jpg"):
        shutil.copy("diagram.jpg", "mdbook/src/images/")
        print("  ✓ 复制图片: diagram.jpg")


def convert_chapter(latex_file, md_file, title):
    """使用Pandoc转换单个章节"""
    latex_path = os.path.join(LATEX_CHAPTERS_DIR, latex_file)
    md_path = os.path.join(MDBOOK_SRC_DIR, md_file)

    if not os.path.exists(latex_path):
        print(f"  ⚠️  跳过不存在的文件: {latex_file}")
        return False

    print(f"  🔄 转换: {latex_file} → {md_file}")

    try:
        # 使用Pandoc转换
        cmd = [
            "pandoc",
            latex_path,
            "-f", "latex",
            "-t", "markdown",
            "--wrap=none",
            "--extract-media=mdbook/src/images",
            "-o", md_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        # 后处理Markdown
        post_process_markdown(md_path, title)

        print(f"  ✓ 完成: {md_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"  ❌ 转换失败: {latex_file}")
        print(f"     错误: {e.stderr.decode('utf-8')}")
        return False


def post_process_markdown(md_path, title):
    """后处理Markdown文件"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 添加标题（如果不存在）
    if not content.startswith('#'):
        content = f"# {title}\n\n{content}"

    # 修复代码块语言标注
    # verbatim环境通常转换为无语言标注的代码块
    content = re.sub(r'```\s*\n([\s\S]*?)```', lambda m: detect_code_language(m.group(1)), content)

    # 修复图片路径
    content = re.sub(r'!\[(.*?)\]\((.*?)\)', r'![\1](images/\2)', content)

    # 修复交叉引用（LaTeX \ref{} → mdBook链接）
    content = re.sub(r'\\ref\{(.*?)\}', r'[参见相关章节](#)', content)

    # 清理LaTeX残留
    content = content.replace('\\textbf{', '**').replace('}', '**')
    content = content.replace('\\emph{', '*').replace('}', '*')

    # 修复列表缩进（Pandoc有时会过度缩进）
    content = re.sub(r'^    -', '-', content, flags=re.MULTILINE)
    content = re.sub(r'^    \d+\.', lambda m: m.group(0).strip(), content, flags=re.MULTILINE)

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)


def detect_code_language(code_block):
    """智能检测代码块语言"""
    code = code_block.strip()

    # Python
    if any(keyword in code for keyword in ['def ', 'import ', 'class ', 'self.', 'print(']):
        return f"```python\n{code}\n```"

    # Bash/Shell
    if any(keyword in code for keyword in ['#!/bin/bash', 'git ', 'mkdir ', 'cd ', 'echo ', 'export ']):
        return f"```bash\n{code}\n```"

    # JSON
    if code.startswith('{') and code.endswith('}') and '"' in code:
        return f"```json\n{code}\n```"

    # YAML
    if ':' in code and not code.startswith('http'):
        if any(keyword in code for keyword in ['name:', 'version:', 'config:']):
            return f"```yaml\n{code}\n```"

    # 目录结构
    if any(char in code for char in ['├', '└', '│']) or code.count('/') > 2:
        return f"```text\n{code}\n```"

    # 默认无语言标注
    return f"```\n{code}\n```"


def generate_summary():
    """生成SUMMARY.md目录文件"""
    summary_path = os.path.join(MDBOOK_SRC_DIR, "SUMMARY.md")

    print("📝 生成SUMMARY.md...")

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# Summary\n\n")
        f.write("[介绍](./README.md)\n\n")

        # 前言
        f.write("---\n\n")

        # 主要章节
        for i, (_, md_file, title) in enumerate(CHAPTER_FILES):
            if md_file.startswith("appendix"):
                continue  # 跳过附录，后面单独处理

            # 根据文件名判断层级
            if md_file.startswith("00"):
                f.write(f"- [{title}](./{md_file})\n")
            else:
                f.write(f"- [{title}](./{md_file})\n")

        # 附录
        f.write("\n---\n\n")
        f.write("# 附录\n\n")
        for _, md_file, title in CHAPTER_FILES:
            if md_file.startswith("appendix"):
                f.write(f"- [{title}](./{md_file})\n")

    print("  ✓ SUMMARY.md 已生成")


def create_readme():
    """创建README.md（书籍首页）"""
    readme_path = os.path.join(MDBOOK_SRC_DIR, "README.md")

    print("📝 创建README.md...")

    content = """# Research Engineering OS

**把返工压缩成规范 + 模板 + 检查清单**

作者：Li Hongmin (李鸿敏)
东京大学 计算生物与医科学专业

---

## 关于本书

这不是一本教你"如何写代码"的书，而是一本教你**如何管理研究代码**的书。

目标读者：
- AI/ML研究人员
- 计算生物学研究者
- 需要维护实验代码的科研工作者

核心理念：
- **实验才是单元**（不是代码文件）
- **探索可以野，但输出必须可清理**
- **结论可以暂时脆弱，但证据链必须扎实**

---

## 在线阅读

本书完全开源，可以在线免费阅读。如果觉得有帮助，欢迎：
- ⭐ 在 [GitHub](https://github.com/your-username/research-engineering-os) 上点星
- 📖 购买 [纸质版/Kindle版](https://kdp.amazon.com) 收藏
- 💬 提供反馈和建议

---

## 版本信息

- **在线版本**：持续更新，包含最新内容
- **纸质版**：v1.0，2026年2月首次发布

---

## 开始阅读

从 [前言](./00-preface.md) 开始，或直接跳转到：
- [为什么总是最后翻车](./01-why-flip.md) - 理解问题的根源
- [实验才是单元](./02-experiment-unit.md) - 核心理念
- [仓库结构](./03-repo-layout.md) - 实践指南

---

## 联系方式

- **邮箱**: lihongmin@edu.k.u-tokyo.ac.jp
- **网站**: [li-hongmin.github.io](https://li-hongmin.github.io)

---

© 2026 Li Hongmin. All rights reserved.
"""

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("  ✓ README.md 已创建")


def main():
    """主函数"""
    print("=" * 60)
    print("  LaTeX to mdBook 转换脚本")
    print("  Research Engineering OS")
    print("=" * 60)
    print()

    # 检查Pandoc
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 错误：未安装Pandoc")
        print("   请运行: brew install pandoc")
        return

    # 创建目录结构
    create_mdbook_structure()
    print()

    # 转换所有章节
    print("📚 开始转换章节...")
    success_count = 0
    for latex_file, md_file, title in CHAPTER_FILES:
        if convert_chapter(latex_file, md_file, title):
            success_count += 1

    print()
    print(f"✓ 成功转换 {success_count}/{len(CHAPTER_FILES)} 个章节")
    print()

    # 生成SUMMARY.md
    generate_summary()
    print()

    # 创建README.md
    create_readme()
    print()

    print("=" * 60)
    print("✅ 转换完成！")
    print()
    print("下一步：")
    print("  1. cd mdbook")
    print("  2. mdbook build")
    print("  3. mdbook serve  # 本地预览")
    print("=" * 60)


if __name__ == "__main__":
    main()
