#!/usr/bin/env python3
"""
生成漫画书 Markdown 文件
从 YAML 分镜脚本生成 mdBook 章节（页码翻页模式）
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

# 章节顺序和中文标题映射（注意：panel目录是00-preface不是00-prologue）
CHAPTER_ORDER = [
    ("00-preface", "序章：截止日前3天"),
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
        print(f"  ⚠️  找不到 {yaml_path}")
        return None

    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def copy_chapter_images(chapter_id: str) -> int:
    """复制章节图片到输出目录"""
    src_dir = PANELS_DIR / chapter_id
    dst_dir = IMAGES_DIR / chapter_id

    if not src_dir.exists():
        print(f"  ⚠️  找不到图片目录 {src_dir}")
        return 0

    # 创建目标目录
    dst_dir.mkdir(parents=True, exist_ok=True)

    # 复制所有 PNG 文件
    count = 0
    for png in sorted(src_dir.glob("*.png")):
        shutil.copy2(png, dst_dir / png.name)
        count += 1

    return count


def generate_chapter_pages(chapter_id: str, chapter_title: str, storyboard: dict) -> int:
    """生成章节的多个独立 Markdown 页面"""
    chapter_dir = OUTPUT_DIR / chapter_id
    chapter_dir.mkdir(parents=True, exist_ok=True)

    if storyboard is None:
        # 如果没有YAML，创建一个简单的占位页面
        with open(chapter_dir / "01.md", 'w', encoding='utf-8') as f:
            f.write(f"# {chapter_title}\n\n*本章内容制作中...*\n")
        return 1

    panels = storyboard.get('panels', [])
    num_panels = len(panels)

    for i, panel in enumerate(panels, 1):
        panel_id = panel.get('id', f'{chapter_id[:2]}_{i:03d}')
        # 使用YAML中的详细description_zh
        description = panel.get('description_zh', '（继续探索故事...）')

        # 图片路径（相对于md文件）
        img_path = f"../images/{chapter_id}/{panel_id}.png"

        # 生成翻页导航
        nav_parts = []
        if i > 1:
            nav_parts.append(f"[← 上一页]({i-1:02d}.md)")
        else:
            nav_parts.append("[← 返回目录](../README.md)")

        if i < num_panels:
            nav_parts.append(f"[下一页 →]({i+1:02d}.md)")
        else:
            # 查找下一章
            next_chapter = None
            current_found = False
            for c_id, c_title in CHAPTER_ORDER:
                if current_found:
                    next_chapter = (c_id, c_title)
                    break
                if c_id == chapter_id:
                    current_found = True

            if next_chapter:
                nav_parts.append(f"[下一章：{next_chapter[1]} →](../{next_chapter[0]}/01.md)")
            else:
                nav_parts.append("[返回目录](../README.md)")

        # 生成页面内容
        content = f"""<div class="manga-layout">

<div class="manga-story">
<div class="manga-story-label">📖 第{i}页</div>
<p class="manga-story-content">{description}</p>
</div>

<div class="manga-image-container">

![{description}]({img_path})

</div>

</div>

---

<div class="manga-footer">
{" &nbsp;&nbsp;&nbsp; ".join(nav_parts)}
</div>
"""

        with open(chapter_dir / f"{i:02d}.md", 'w', encoding='utf-8') as f:
            f.write(content)

    return num_panels


def generate_summary(chapters_info: list) -> str:
    """生成 SUMMARY.md 目录"""
    lines = ["# 目录\n\n"]
    lines.append("[📖 封面](README.md)\n\n")
    lines.append("---\n\n")

    for chapter_id, chapter_title, panel_count in chapters_info:
        # 章节标题链接到第一页
        lines.append(f"- [{chapter_title}]({chapter_id}/01.md)\n")
        # 嵌套子页面（从第2页开始）
        if panel_count > 1:
            for i in range(2, panel_count + 1):
                lines.append(f"  - [第 {i} 页]({chapter_id}/{i:02d}.md)\n")

    return "".join(lines)


def generate_readme() -> str:
    """生成封面 README.md"""
    return """# 研究工程 OS - 漫画版

<div class="intro-section">

## 📚 用漫画讲述研究工程实践的故事

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

## 👤 人物介绍

### 小研（Xiao Yan）
- 计算生物学博士生
- 热情但经验不足
- 正在经历研究中的各种挑战

### 导师
- 资深研究员
- 将传授研究工程的智慧

---

## 📖 阅读提示

本书采用**翻页模式**，每一页包含一幅漫画和故事描述。

点击底部的"下一页"按钮翻页，或使用键盘左右箭头键。

**开始阅读 →** [序章：截止日前3天](00-preface/01.md)

---

<div style="text-align: center; color: #666; font-size: 0.9em; margin-top: 3em;">

作者：李鸿敏 | 东京大学计算生物学研究科

[完整文字版阅读](https://li-hongmin.github.io/Research-Engineering-OS/)

</div>
"""


def main():
    """主函数"""
    print("=" * 70)
    print("📚 研究工程 OS 漫画书生成器")
    print("=" * 70)

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # 处理每个章节
    total_panels = 0
    chapters_info = []

    for chapter_id, chapter_title in CHAPTER_ORDER:
        print(f"\n📖 处理章节: {chapter_id} - {chapter_title}")

        # 加载分镜脚本
        storyboard = load_storyboard(chapter_id)

        # 复制图片
        panel_count = copy_chapter_images(chapter_id)
        total_panels += panel_count
        if panel_count > 0:
            print(f"   📷 复制 {panel_count} 张图片")

        # 生成页面
        actual_panels = generate_chapter_pages(chapter_id, chapter_title, storyboard)
        chapters_info.append((chapter_id, chapter_title, actual_panels))
        print(f"   ✅ 生成 {actual_panels} 个页面")

    # 生成 SUMMARY.md
    summary_content = generate_summary(chapters_info)
    summary_path = OUTPUT_DIR / "SUMMARY.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    print(f"\n✅ 生成目录: {summary_path}")

    # 生成 README.md
    readme_content = generate_readme()
    readme_path = OUTPUT_DIR / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✅ 生成封面: {readme_path}")

    print("\n" + "=" * 70)
    print(f"🎉 完成！共处理 {len(CHAPTER_ORDER)} 章，{total_panels} 张漫画")
    print("=" * 70)
    print("\n📝 下一步：")
    print("  cd manga_book")
    print("  mdbook build")
    print("  cd book && python -m http.server 8001")
    print()


if __name__ == "__main__":
    main()
