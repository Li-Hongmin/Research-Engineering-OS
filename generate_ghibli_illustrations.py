#!/usr/bin/env python3
"""
宫崎骏风格插图生成器
为《Research Engineering OS》生成温暖友好的彩色插图
"""

import os, base64, time
from pathlib import Path
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="3e3a7c53784247a6ad61d3f1bed81752",
    api_version="2024-08-01-preview",
    azure_endpoint="https://eastus2.api.cognitive.microsoft.com"
)

# 宫崎骏风格统一设置
STYLE_BASE = "Studio Ghibli anime style, Hayao Miyazaki inspired, hand-drawn watercolor feel, warm soft colors, gentle lighting, whimsical yet professional, detailed but not overwhelming, peaceful atmosphere"

# 插图任务列表
ILLUSTRATIONS = [
    {
        "filename": "01_researcher_messy.png",
        "title": "第1章 - 混乱的研究环境",
        "prompt": f"{STYLE_BASE}, scene: a young researcher at cluttered desk surrounded by floating papers with code snippets, tangled cables like vines, multiple laptops showing different results, gentle chaos, warm afternoon light through window, soft colors, sympathetic mood"
    },
    {
        "filename": "02_experiment_garden.png",
        "title": "第2章 - 实验如同种植园",
        "prompt": f"{STYLE_BASE}, scene: beautiful garden where each plant represents an experiment, researcher tending to plants, some blooming (successful), some wilting (failed), watering can labeled 'reproducibility', notebook for recording, peaceful garden atmosphere"
    },
    {
        "filename": "03_organized_library.png",
        "title": "第3章 - 井然有序的代码库",
        "prompt": f"{STYLE_BASE}, scene: cozy library with organized bookshelves representing code repository, folders labeled src/, experiments/, configs/, researcher peacefully organizing books, soft natural lighting, warm colors, sense of calm and order"
    },
    {
        "filename": "04_time_travel.png",
        "title": "第4章 - Git时光旅行",
        "prompt": f"{STYLE_BASE}, scene: researcher riding on a magical timeline/ribbon floating through space, past commits shown as glowing nodes on the timeline, viewing history of changes, stars and soft clouds in background, adventurous yet safe feeling"
    },
    {
        "filename": "05_checklist_wings.png",
        "title": "第5章 - DoD检查清单如翅膀",
        "prompt": f"{STYLE_BASE}, scene: researcher with large checklist that transforms into wings, lifting them up from messy ground, each checkbox glowing as completed, flying toward clear sky, metaphor for quality and completion, hopeful uplifting mood"
    },
    {
        "filename": "06_logging_breadcrumbs.png",
        "title": "第6章 - 日志如面包屑",
        "prompt": f"{STYLE_BASE}, scene: researcher following glowing breadcrumb trail (logs) through a gentle forest of data, each breadcrumb showing timestamp and event, path leading to discovery, warm dappled sunlight, sense of guidance and clarity"
    },
    {
        "filename": "07_ai_companion.png",
        "title": "第7章 - AI助手伙伴",
        "prompt": f"{STYLE_BASE}, scene: researcher working alongside a friendly glowing AI spirit companion (like Totoro-style), AI offering suggestions shown as floating glowing orbs, researcher carefully examining each one, collaborative partnership, warm friendly atmosphere"
    },
    {
        "filename": "08_multiple_paths.png",
        "title": "第8章 - 探索多条路径",
        "prompt": f"{STYLE_BASE}, scene: researcher at crossroads with multiple gentle paths diverging through beautiful landscape, each path labeled with different experiments, some leading to treasure chests (success), some to learning experiences, peaceful exploration mood"
    },
    {
        "filename": "09_prevention_shield.png",
        "title": "第9章 - 预防炸雷",
        "prompt": f"{STYLE_BASE}, scene: researcher with protective magical shield made of best practices, deflecting incoming problems (shown as small dark clouds), calm confident expression, peaceful protected environment, warm reassuring colors"
    },
    {
        "filename": "10_team_harmony.png",
        "title": "第10章 - 团队协作",
        "prompt": f"{STYLE_BASE}, scene: small team of researchers working together in harmony, each with different strengths, shared codebase shown as communal garden they all tend, warm collaboration, diverse but united, peaceful productive atmosphere"
    },
]

def generate_illustration(task, index, total):
    """生成单张插图"""
    print(f"[{index}/{total}] {task['title']}")
    print(f"  文件: {task['filename']}")

    try:
        print(f"  🎨 生成中...", end=" ")

        response = client.images.generate(
            model="gpt-image-1.5",
            prompt=task['prompt'],
            size="1024x1024",
            quality="high",
            n=1
        )

        img_bytes = base64.b64decode(response.data[0].b64_json)
        output_path = Path("ghibli_illustrations") / task['filename']
        output_path.parent.mkdir(exist_ok=True)
        output_path.write_bytes(img_bytes)

        print(f"✓ {len(img_bytes)//1024}KB")
        return True

    except Exception as e:
        print(f"❌ {e}")
        return False


def main():
    """主函数"""
    print("=" * 70)
    print("  宫崎骏风格插图生成器")
    print("  Research Engineering OS")
    print("=" * 70)
    print(f"\n将生成 {len(ILLUSTRATIONS)} 张插图")
    print(f"风格：宫崎骏动画风格，温暖彩色，手绘水彩感")
    print(f"输出：ghibli_illustrations/\n")
    print("=" * 70)

    success_count = 0
    start_time = time.time()

    for i, task in enumerate(ILLUSTRATIONS, 1):
        if generate_illustration(task, i, len(ILLUSTRATIONS)):
            success_count += 1

        # 避免API限流
        if i < len(ILLUSTRATIONS):
            time.sleep(2)

        print()

    duration = time.time() - start_time

    print("=" * 70)
    print(f"✅ 生成完成!")
    print(f"成功: {success_count}/{len(ILLUSTRATIONS)} 张")
    print(f"用时: {duration/60:.1f} 分钟")
    print(f"查看: open ghibli_illustrations/")
    print("=" * 70)


if __name__ == "__main__":
    main()
