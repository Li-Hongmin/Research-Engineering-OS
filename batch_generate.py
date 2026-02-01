#!/usr/bin/env python3
"""批量生成书籍插图 - 使用gpt-image-1.5"""

import os, base64, time, json
from pathlib import Path
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="3e3a7c53784247a6ad61d3f1bed81752",
    api_version="2024-08-01-preview",
    azure_endpoint="https://eastus2.api.cognitive.microsoft.com"
)

TASKS = [
    ("cover_1.png", "封面-极简", "Professional book cover 'Research Engineering OS', minimalist, soft pastel colors, light beige cream background, subtle geometric shapes, clean modern typography, gentle academic aesthetic"),
    ("cover_2.png", "封面-插画", "Technical book cover 'Research Engineering OS', soft illustration style, light colors pastel palette, gentle gradients, clean typography, approachable friendly design"),
    ("cover_3.png", "封面-抽象", "Abstract book cover 'Research Engineering OS', light background, subtle flowing lines, soft pastel gradients cream to light cyan, minimal elegant typography, calm professional"),
    ("comic_deadline.png", "漫画-deadline", "Comic: researcher at desk, light colors, soft pastel palette, simple line art, friendly humorous style, light background"),
    ("diagram_workflow.png", "流程-实验", "Diagram: experiment workflow, light background, pastel colors, soft lines, minimal clean design, gentle professional"),
    ("diagram_repo.png", "架构-仓库", "Diagram: code repository structure, light colors, pastel palette, clean soft icons, organized friendly layout"),
    ("concept_debts.png", "概念-债务", "Infographic: three debts, light background, soft pastel colors, gentle icons, clean educational style"),
    ("diagram_git.png", "流程-Git", "Flowchart: git provenance, light colors, soft arrows, pastel palette, clean professional academic"),
    ("concept_vars.png", "概念-变量", "Abstract: fast slow variables, light background, soft colors, gentle contrast, minimal clean design"),
    ("diagram_ai.png", "流程-AI", "Cycle diagram: AI workflow, light colors, pastel palette, soft arrows, modern friendly aesthetic"),
]

output_dir = Path("generated_images")
output_dir.mkdir(exist_ok=True)

print(f"🎨 批量生成 {len(TASKS)} 张插图\n")

for i, (filename, desc, prompt) in enumerate(TASKS, 1):
    print(f"[{i}/{len(TASKS)}] {desc}...", end=" ")

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
        print(f"❌ {str(e)[:50]}")

print(f"\n✅ 完成！查看: {output_dir}/")
