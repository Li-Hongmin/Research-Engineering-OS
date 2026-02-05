#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量翻译漫画书内容
"""

import os
import re

# 翻译字典
TRANSLATIONS = {
    # 第一章
    "### 第1格": "### Panel 1",
    "### 第2格": "### Panel 2",
    "### 第3格": "### Panel 3",
    "### 第4格": "### Panel 4",
    "### 第5格": "### Panel 5",
    "### 第6格": "### Panel 6",
    "### 第7格": "### Panel 7",
    "### 第8格": "### Panel 8",
    "### 第9格": "### Panel 9",
    "### 第10格": "### Panel 10",
    "### 第11格": "### Panel 11",
    "### 第12格": "### Panel 12",
    "### 第13格": "### Panel 13",
    "### 第14格": "### Panel 14",
    "### 第15格": "### Panel 15",
    "### 第16格": "### Panel 16",
    "### 第17格": "### Panel 17",
    "### 第18格": "### Panel 18",
    "### 第19格": "### Panel 19",
    "### 第20格": "### Panel 20",
    "### 第21格": "### Panel 21",
    "### 第22格": "### Panel 22",
    "### 第23格": "### Panel 23",
    "### 第24格": "### Panel 24",
    "### 第25格": "### Panel 25",
}

# 第一章的描述翻译
CHAPTER_1_TRANSLATIONS = {
    "小研在图书馆深夜阅读Research Engineering OS": "Xiao Yan deep in the library at night, reading Research Engineering OS",
    "书中浮现三种债务的图解": "The three types of debt visualized in the book",
    "回忆：项目开始时的兴奋": "Flashback: The excitement at the project's start",
    "快速推进：日子飞逝的蒙太奇": "Fast forward: Days flying by in a montage",
    "现实：截止日前发现问题": "Reality: Problems discovered before the deadline",
    "探索债怪兽详解：由快速原型构成": "Understanding the Exploration Debt Monster: Built from rapid prototypes",
    "探索债的诞生：快速验证想法": "How Exploration Debt is born: Rapid idea validation",
    "探索债的积累：原型变成依赖": "How Exploration Debt accumulates: Prototypes become dependencies",
    "探索债爆发：需要改动时崩溃": "Exploration Debt explodes: System crashes when changes are needed",
    "探索债的解决：定期清理和重构": "Resolving Exploration Debt: Regular cleanup and refactoring",
    "验证债怪兽详解：由跳过的测试构成": "Understanding the Verification Debt Monster: Built from skipped tests",
    "验证债的诞生：没时间写测试": "How Verification Debt is born: No time to write tests",
    "验证债积累：结果看起来对但是...": "Verification Debt accumulates: Results look correct... but are they?",
    "验证债爆发：审稿人质疑统计显著性": "Verification Debt explodes: Reviewers question statistical significance",
    "验证债解决：测试驱动的研究": "Resolving Verification Debt: Test-driven research",
    "复现债怪兽详解：由丢失的环境构成": "Understanding the Reproducibility Debt Monster: Built from lost environments",
    "复现债诞生：它在我的电脑上能跑": "How Reproducibility Debt is born: It works on my machine",
    "复现债积累：依赖变化但没记录": "Reproducibility Debt accumulates: Dependencies change without records",
    "复现债爆发：三个月后无法复现": "Reproducibility Debt explodes: Cannot reproduce three months later",
    "复现债解决：环境即代码": "Resolving Reproducibility Debt: Environment as code",
    "三种债务的关系：相互放大": "The relationship between the three debts: Amplifying each other",
    "小研明白：问题不是最后一刻产生的": "Xiao Yan understands: Problems don't appear at the last moment",
    "决心改变：每日小习惯": "Commitment to change: Daily small habits",
    "10分钟行动：检查你的债务": "10-minute action: Examine your technical debt",
    "下一章预告：实验才是单元": "Next chapter teaser: The experiment is the unit",
}

def translate_file_en(filepath):
    """翻译一个文件到英文"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 先翻译标题和副标题
    for zh, en in TRANSLATIONS.items():
        content = content.replace(zh, en)

    # 翻译第一章具体内容
    if '01-why-flip' in filepath:
        for zh, en in CHAPTER_1_TRANSLATIONS.items():
            content = content.replace(f"![{zh}]", f"![{en}]")
            content = content.replace(f"*{zh}*", f"*{en}*")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ 已翻译英文版本: {filepath}")

def translate_panel_headings_ja(filepath):
    """将Panel标题翻译为日文"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 将Panel标题转换为日文格式
    panel_map = {
        "### Panel 1": "### パネル1",
        "### Panel 2": "### パネル2",
        "### Panel 3": "### パネル3",
        "### Panel 4": "### パネル4",
        "### Panel 5": "### パネル5",
        "### Panel 6": "### パネル6",
        "### Panel 7": "### パネル7",
        "### Panel 8": "### パネル8",
        "### Panel 9": "### パネル9",
        "### Panel 10": "### パネル10",
        "### Panel 11": "### パネル11",
        "### Panel 12": "### パネル12",
        "### Panel 13": "### パネル13",
        "### Panel 14": "### パネル14",
        "### Panel 15": "### パネル15",
        "### Panel 16": "### パネル16",
        "### Panel 17": "### パネル17",
        "### Panel 18": "### パネル18",
        "### Panel 19": "### パネル19",
        "### Panel 20": "### パネル20",
        "### Panel 21": "### パネル21",
        "### Panel 22": "### パネル22",
        "### Panel 23": "### パネル23",
        "### Panel 24": "### パネル24",
        "### Panel 25": "### パネル25",
    }

    for en, ja in panel_map.items():
        content = content.replace(en, ja)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ 已转换日文Panel标题: {filepath}")

# 处理所有章节文件
base_path = "/Users/lihongmin/ideas/Research-Engineering-OS-/manga-book"
src_en_path = os.path.join(base_path, "src_en")

# 先处理01-why-flip.md
filepath_01_en = os.path.join(src_en_path, "01-why-flip.md")
if os.path.exists(filepath_01_en):
    translate_file_en(filepath_01_en)

# 处理日文版本的Panel标题
src_ja_path = os.path.join(base_path, "src_ja")
for i in range(1, 12):
    filename = f"{i:02d}-*.md" if i < 10 else f"{i}-*.md"
    # 需要找到确切的文件名

print("翻译完成!")
