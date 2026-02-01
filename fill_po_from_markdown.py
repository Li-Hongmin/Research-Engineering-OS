#!/usr/bin/env python3
"""
将现有英文Markdown翻译填充到PO文件
"""

import polib
from pathlib import Path
import re

# 核心翻译映射
TRANSLATIONS = {
    # 导航和目录
    "Summary": "Summary",
    "介绍": "Introduction",
    "前言": "Preface",
    "为什么总是最后翻车": "Why Projects Fail at the Last Minute",
    "实验才是单元": "Experiments as the Unit",
    "仓库结构": "Repository Structure",
    "Git作为证据链": "Git as Evidence Chain",
    "Definition of Done": "Definition of Done",
    "日志": "Logging",
    "AI时代的工作流": "AI-Era Workflow",
    "多路探索": "Multi-Path Exploration",
    "避免临deadline炸雷": "Avoiding Deadline Explosions",
    "团队协作": "Team Collaboration",
    "附录": "Appendices",
    "附录：模板": "Appendix: Templates",
    "附录：AI灾难案例": "Appendix: AI Disaster Cases",

    # 首页
    "Research Engineering OS": "Research Engineering OS",
    "**把返工压缩成规范 + 模板 + 检查清单**": "**Compressing Rework into Standards + Templates + Checklists**",
    "作者：Li Hongmin (李鸿敏) 东京大学 计算生物与医科学专业": "Author: Li Hongmin, Dept. of Computational Biology, University of Tokyo",
    "关于本书": "About This Book",

    # 章节标题
    "# 前言": "# Preface",
    "# 为什么总是最后翻车": "# Why Projects Fail at the Last Minute",
    "# 实验才是单元": "# Experiments as the Unit",
    "# 仓库结构": "# Repository Structure",
    "# Git作为证据链": "# Git as Evidence Chain",
    "# Definition of Done": "# Definition of Done",
    "# 日志": "# Logging",
    "# AI时代的工作流": "# AI-Era Workflow",
    "# 多路探索": "# Multi-Path Exploration",
    "# 避免临deadline炸雷": "# Avoiding Deadline Explosions",
    "# 团队协作": "# Team Collaboration",
    "# 附录：模板": "# Appendix: Templates",
    "# 附录：AI灾难案例": "# Appendix: AI Disaster Cases",

    # 常见二级标题
    "## 核心观点": "## Core Ideas",
    "## 三种债务": "## Three Types of Debt",
    "## 实验对象模型": "## Experiment Object Model",
    "## 快变量 vs 慢变量": "## Fast Variables vs Slow Variables",
    "## 推荐结构": "## Recommended Structure",
    "## Git 最佳实践": "## Git Best Practices",
    "## 日志的价值": "## The Value of Logging",
    "## AI 辅助开发": "## AI-Assisted Development",
    "## 并行探索策略": "## Parallel Exploration Strategies",
    "## 风险管理": "## Risk Management",
    "## 代码审查": "## Code Review",
    "## 10分钟行动": "## 10-Minute Actions",
    "## 小结": "## Summary",
    "## 检查清单": "## Checklist",

    # 常见术语
    "探索债": "Exploration Debt",
    "验证债": "Validation Debt",
    "复现债": "Reproducibility Debt",
    "run_id": "run_id",
    "快变量": "Fast Variables",
    "慢变量": "Slow Variables",
}

def fill_po_translations():
    """填充PO文件翻译"""
    po_file = polib.pofile('book_i18n/po/en.po')

    print(f"📖 加载PO文件: {len(po_file)} 条目\n")

    matched = 0
    for entry in po_file:
        # 直接匹配
        if entry.msgid in TRANSLATIONS:
            entry.msgstr = TRANSLATIONS[entry.msgid]
            matched += 1
        # 如果msgid是英文，保持不变
        elif entry.msgid.isascii() and entry.msgid.strip():
            entry.msgstr = entry.msgid
            matched += 1
        # 对于代码块和特殊格式，保持原样
        elif entry.msgid.startswith('```') or entry.msgid.startswith('!['):
            entry.msgstr = entry.msgid
            matched += 1

    print(f"✅ 匹配: {matched}/{len(po_file)} 条目")
    print(f"📝 保存PO文件...")

    po_file.save('book_i18n/po/en.po')
    print("✅ 完成！")

if __name__ == "__main__":
    try:
        import polib
    except ImportError:
        print("❌ 需要安装polib: pip install polib")
        exit(1)

    fill_po_translations()
