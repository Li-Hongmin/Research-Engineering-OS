#!/usr/bin/env python3
"""
生成漫画书 Markdown 文件
从 YAML 分镜脚本生成 mdBook 章节
"""

import os
import yaml
import shutil
from pathlib import Path

# 目录配置
SCRIPT_DIR = Path(__file__).parent
STORYBOARD_DIR = SCRIPT_DIR.parent / "manga" / "storyboards"
PANELS_DIR = SCRIPT_DIR.parent / "manga" / "panels"
OUTPUT_DIR = SCRIPT_DIR / "src"
IMAGES_DIR = OUTPUT_DIR / "images"

# 章节顺序和中文标题映射
CHAPTER_ORDER = [
    ("00-prologue", "序章：截止日前3天"),
    ("01-why-flip", "第一章：为什么翻车"),
    ("02-experiment-unit", "第二章：实验作为基本单元"),
    ("03-repo-layout", "第三章：仓库结构"),
    ("04-git-proof", "第四章：Git 作为证明"),
    ("05-dod", "第五章：完成的定义"),
    ("06-logging", "第六章：记录的艺术"),
    ("07-ai-workflow", "第七章：AI 协作工作流"),
    ("08-multi-path", "第八章：多路径探索"),
    ("09-no-boom", "第九章：不爆炸的科学"),
    ("10-team", "第十章：团队协作"),
    ("11-epilogue", "终章：新的开始"),
]


def load_storyboard(chapter_id: str) -> dict:
    """加载章节分镜脚本"""
    yaml_path = STORYBOARD_DIR / f"{chapter_id}.yaml"
    if not yaml_path.exists():
        print(f"警告：找不到 {yaml_path}")
        return None

    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def copy_chapter_images(chapter_id: str) -> int:
    """复制章节图片到输出目录"""
    src_dir = PANELS_DIR / chapter_id
    dst_dir = IMAGES_DIR / chapter_id

    if not src_dir.exists():
        print(f"警告：找不到图片目录 {src_dir}")
        return 0

    # 创建目标目录
    dst_dir.mkdir(parents=True, exist_ok=True)

    # 复制所有 PNG 文件
    count = 0
    for png in sorted(src_dir.glob("*.png")):
        shutil.copy2(png, dst_dir / png.name)
        count += 1

    return count


def generate_chapter_markdown(chapter_id: str, chapter_title: str, storyboard: dict) -> str:
    """生成章节 Markdown 内容"""
    lines = [f"# {chapter_title}\n"]

    if storyboard is None:
        lines.append("\n*（本章漫画制作中...）*\n")
        return "\n".join(lines)

    # 添加章节信息
    if 'title_zh' in storyboard:
        lines.append(f"\n**{storyboard['title_zh']}**\n")

    # 处理每个格子
    panels = storyboard.get('panels', [])
    for i, panel in enumerate(panels, 1):
        panel_id = panel.get('id', f'{chapter_id[:2]}_{i:03d}')
        description = panel.get('description_zh', '（无描述）')

        # 图片路径
        img_path = f"images/{chapter_id}/{panel_id}.png"

        lines.append(f"\n### 第{i}格\n")
        lines.append(f"![{description}]({img_path})\n")
        lines.append(f"*{description}*\n")
        lines.append("\n---\n")

    return "\n".join(lines)


def generate_summary() -> str:
    """生成 SUMMARY.md 目录"""
    lines = ["# 目录\n\n"]
    lines.append("[封面](README.md)\n\n")
    lines.append("---\n\n")

    for chapter_id, chapter_title in CHAPTER_ORDER:
        lines.append(f"- [{chapter_title}]({chapter_id}.md)\n")

    return "".join(lines)


def generate_readme() -> str:
    """生成封面 README.md"""
    return """# 研究工程 OS - 漫画版

<div class="intro-section">

## 用漫画讲述研究工程实践的故事

</div>

---

## 关于本书

这是《研究工程 OS》的漫画版，通过生动的漫画故事，讲述科研中的工程实践挑战与解决方案。

跟随主人公**小研**的旅程，一起了解：

- **三种技术债务**：探索债、验证债、复现债
- **实验作为基本单元**：把实验而非代码作为思考的基本单位
- **Git 作为证明**：用版本控制建立可追溯的证据链
- **AI 协作工作流**：在 AI 时代如何保持研究的可靠性

---

## 人物介绍

### 小研（Xiao Yan）
- 计算生物学博士生
- 热情但经验不足
- 正在经历研究中的各种挑战

### 导师
- 资深研究员
- 将传授研究工程的智慧

---

## 阅读提示

每一章包含 15-25 格漫画，建议按顺序阅读。

**开始阅读 →** [序章：截止日前3天](00-prologue.md)

---

<div style="text-align: center; color: #666; font-size: 0.9em;">

作者：李鸿敏 | 东京大学计算生物学研究科

[完整版阅读](https://li-hongmin.github.io/Research-Engineering-OS/)

</div>
"""


def main():
    """主函数"""
    print("=" * 60)
    print("研究工程 OS 漫画书生成器")
    print("=" * 60)

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # 生成 SUMMARY.md
    summary_content = generate_summary()
    summary_path = OUTPUT_DIR / "SUMMARY.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    print(f"✅ 生成目录: {summary_path}")

    # 生成 README.md
    readme_content = generate_readme()
    readme_path = OUTPUT_DIR / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✅ 生成封面: {readme_path}")

    # 处理每个章节
    total_panels = 0
    for chapter_id, chapter_title in CHAPTER_ORDER:
        print(f"\n处理章节: {chapter_id}")

        # 加载分镜脚本
        storyboard = load_storyboard(chapter_id)

        # 复制图片
        panel_count = copy_chapter_images(chapter_id)
        total_panels += panel_count
        print(f"  📷 复制 {panel_count} 张图片")

        # 生成 Markdown
        md_content = generate_chapter_markdown(chapter_id, chapter_title, storyboard)
        md_path = OUTPUT_DIR / f"{chapter_id}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  📝 生成 {md_path.name}")

    print("\n" + "=" * 60)
    print(f"🎉 完成！共处理 {len(CHAPTER_ORDER)} 章，{total_panels} 张漫画")
    print("=" * 60)
    print("\n下一步：")
    print("  cd manga_book && mdbook build")
    print("  cd book && python -m http.server 8001")


if __name__ == "__main__":
    main()
