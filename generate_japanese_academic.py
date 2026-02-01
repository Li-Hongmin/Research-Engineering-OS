#!/usr/bin/env python3
"""日本学术动漫风格插图生成器"""

import os, base64, time
from pathlib import Path
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="3e3a7c53784247a6ad61d3f1bed81752",
    api_version="2024-08-01-preview",
    azure_endpoint="https://eastus2.api.cognitive.microsoft.com"
)

# 日本学术动漫风格
STYLE = "Japanese anime illustration style, academic aesthetic, soft watercolor rendering, gentle pastel colors, clean line art, professional yet approachable, educational manga style, warm lighting, detailed backgrounds"

TASKS = [
    ("01_researcher_workspace.png", "研究者工作空间",
     f"{STYLE}, young researcher at clean modern desk, laptop showing code, organized notes, coffee cup, window with campus view, peaceful productive atmosphere, soft natural light"),

    ("02_experiment_flowchart.png", "实验流程图",
     f"{STYLE}, elegant flowchart visualization floating in space, Configure→Execute→Log→Validate nodes connected by flowing ribbons, soft glow effects, clean academic presentation"),

    ("03_code_repository.png", "代码仓库结构",
     f"{STYLE}, isometric view of organized file structure, folders as buildings in miniature city, src/ experiments/ configs/ as districts, clean organized urban planning metaphor"),

    ("04_git_timeline.png", "Git时间线",
     f"{STYLE}, flowing timeline with glowing commit nodes, researcher viewing history, gentle sparkles, academic documentation aesthetic, soft colors"),

    ("05_checklist_complete.png", "完成检查清单",
     f"{STYLE}, researcher with glowing checklist, items being checked off with soft light effects, sense of accomplishment, warm atmosphere"),

    ("06_logging_path.png", "日志路径",
     f"{STYLE}, researcher following illuminated path of log entries through serene landscape, breadcrumb trail glowing softly, guidance theme"),

    ("07_ai_collaboration.png", "AI协作",
     f"{STYLE}, researcher working with floating holographic AI interface, reviewing code suggestions together, collaborative atmosphere, modern tech meets traditional academia"),

    ("08_exploration_branches.png", "探索分支",
     f"{STYLE}, researcher at crossroads with multiple paths branching through peaceful landscape, each path showing different experiment outcomes, exploration theme"),

    ("09_quality_shield.png", "质量保护",
     f"{STYLE}, researcher protected by gentle glowing shield of best practices, calm confident expression, soft protective aura"),

    ("10_team_collaboration.png", "团队协作",
     f"{STYLE}, small diverse research team working harmoniously in modern lab, sharing screens and ideas, warm collaborative mood, academic professionalism"),
]

output_dir = Path("illustrations")
output_dir.mkdir(exist_ok=True)

print(f"🎨 生成 {len(TASKS)} 张日本学术动漫风格插图\n")

for i, (filename, title, prompt) in enumerate(TASKS, 1):
    print(f"[{i}/{len(TASKS)}] {title}...", end=" ")

    try:
        response = client.images.generate(
            model="gpt-image-1.5",
            prompt=prompt,
            size="1024x1024",
            quality="high",
            n=1
        )

        img_bytes = base64.b64decode(response.data[0].b64_json)
        (output_dir / filename).write_bytes(img_bytes)

        print(f"✓ {len(img_bytes)//1024}KB")
        time.sleep(2)

    except Exception as e:
        if 'moderation' in str(e):
            print(f"⚠️ 跳过")
        else:
            print(f"❌ {str(e)[:40]}")

print(f"\n✅ 完成！输出: {output_dir}/")
