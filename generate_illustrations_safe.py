#!/usr/bin/env python3
"""
温暖彩色插图生成器（避免版权触发）
风格：手绘动画风格、温暖水彩感
"""

import os, base64, time
from pathlib import Path
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="3e3a7c53784247a6ad61d3f1bed81752",
    api_version="2024-08-01-preview",
    azure_endpoint="https://eastus2.api.cognitive.microsoft.com"
)

# 安全的风格描述
STYLE = "Warm hand-drawn animation style, soft watercolor feel, gentle pastel colors, whimsical illustration, peaceful atmosphere, detailed but friendly, children's book aesthetic"

ILLUSTRATIONS = [
    ("01_messy_desk.png", "研究环境",
     f"{STYLE}, researcher at desk with scattered papers, multiple laptops, tangled cables, warm afternoon light, gentle chaos, sympathetic mood"),

    ("02_garden.png", "实验花园",
     f"{STYLE}, beautiful garden with different plants, gardener tending plants, some blooming some not, watering can, notebook, peaceful"),

    ("03_library.png", "整理书架",
     f"{STYLE}, cozy library with organized shelves, person arranging books, warm natural light, calm orderly atmosphere"),

    ("04_timeline.png", "时间线",
     f"{STYLE}, person on magical glowing ribbon timeline, floating nodes, gentle sky background, adventurous feeling"),

    ("05_wings.png", "检查清单",
     f"{STYLE}, person with checklist transforming into wings, lifting upward, glowing checkboxes, hopeful mood, clear sky"),

    ("06_trail.png", "面包屑路径",
     f"{STYLE}, person following glowing trail through gentle forest, breadcrumbs showing path, dappled sunlight, guidance"),

    ("07_companion.png", "助手伙伴",
     f"{STYLE}, person working with friendly glowing spirit helper, floating light orbs, warm collaborative atmosphere"),

    ("08_crossroads.png", "多条路径",
     f"{STYLE}, person at crossroads, multiple gentle paths through landscape, some with treasure chests, peaceful exploration"),

    ("09_shield.png", "保护盾",
     f"{STYLE}, person with protective light shield, deflecting small clouds, calm confident, reassuring warm colors"),

    ("10_teamwork.png", "团队花园",
     f"{STYLE}, small team working together in shared garden, diverse people, harmonious collaboration, warm peaceful"),
]

output_dir = Path("illustrations")
output_dir.mkdir(exist_ok=True)

print(f"🎨 生成 {len(ILLUSTRATIONS)} 张温暖彩色插图\n")

success = 0
for i, (filename, title, prompt) in enumerate(ILLUSTRATIONS, 1):
    print(f"[{i}/{len(ILLUSTRATIONS)}] {title}...", end=" ")

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
        success += 1
        time.sleep(2)

    except Exception as e:
        error_msg = str(e)
        if 'moderation_blocked' in error_msg:
            print(f"⚠️ 被拦截，跳过")
        else:
            print(f"❌ {error_msg[:50]}")

print(f"\n✅ 成功生成 {success}/{len(ILLUSTRATIONS)} 张")
print(f"输出: {output_dir}/")
