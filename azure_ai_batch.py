#!/usr/bin/env python3
"""
Azure AI 批量任务处理器
为《Research Engineering OS》书籍生成AI增强内容
"""

import os
import json
import time
from pathlib import Path
from openai import AzureOpenAI
import requests

# Azure OpenAI配置
AZURE_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")
GPT_DEPLOYMENT = "gpt-5.2"
IMAGE_DEPLOYMENT = "gpt-image-1.5"
FLUX_DEPLOYMENT = "FLUX.2-pro"

# 初始化客户端
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT
)

# 章节信息
CHAPTERS = [
    {
        "id": "00",
        "title": "前言",
        "file": "00-preface.md",
        "keywords": "research engineering, reproducibility, AI era",
        "color_theme": "warm, welcoming"
    },
    {
        "id": "01",
        "title": "为什么总是最后翻车",
        "file": "01-why-flip.md",
        "keywords": "technical debt, deadline, crisis, explosion",
        "color_theme": "red, warning"
    },
    {
        "id": "02",
        "title": "实验才是单元",
        "file": "02-experiment-unit.md",
        "keywords": "experiment, reproducibility, scientific method",
        "color_theme": "blue, systematic"
    },
    {
        "id": "03",
        "title": "仓库结构",
        "file": "03-repo-layout.md",
        "keywords": "directory structure, organization, file layout",
        "color_theme": "green, organized"
    },
    {
        "id": "04",
        "title": "Git作为证据链",
        "file": "04-git-proof.md",
        "keywords": "git, version control, provenance, audit trail",
        "color_theme": "purple, trustworthy"
    },
    {
        "id": "05",
        "title": "Definition of Done",
        "file": "05-dod.md",
        "keywords": "checklist, quality gates, completion criteria",
        "color_theme": "teal, professional"
    },
    {
        "id": "06",
        "title": "日志",
        "file": "06-logging.md",
        "keywords": "logging, debugging, observability, monitoring",
        "color_theme": "orange, informative"
    },
    {
        "id": "07",
        "title": "AI时代的工作流",
        "file": "07-ai-workflow.md",
        "keywords": "AI assistant, copilot, verification, validation",
        "color_theme": "cyan, futuristic"
    },
    {
        "id": "08",
        "title": "多路探索",
        "file": "08-multi-path.md",
        "keywords": "experimentation, branching, parallel paths",
        "color_theme": "magenta, creative"
    },
    {
        "id": "09",
        "title": "避免临deadline炸雷",
        "file": "no-boom.md",
        "keywords": "risk management, prevention, early detection",
        "color_theme": "yellow, cautionary"
    },
    {
        "id": "10",
        "title": "团队协作",
        "file": "team.md",
        "keywords": "collaboration, communication, teamwork",
        "color_theme": "indigo, harmonious"
    },
]


class AzureAIBatchProcessor:
    """批量处理Azure AI任务"""

    def __init__(self, output_dir="ai_generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # 创建子目录
        self.covers_dir = self.output_dir / "covers"
        self.chapter_images_dir = self.output_dir / "chapter_images"
        self.social_cards_dir = self.output_dir / "social_cards"
        self.code_examples_dir = self.output_dir / "code_examples"

        for d in [self.covers_dir, self.chapter_images_dir,
                  self.social_cards_dir, self.code_examples_dir]:
            d.mkdir(exist_ok=True)

    def generate_text(self, prompt, system_prompt="You are a helpful assistant.",
                     max_tokens=2000):
        """使用GPT-5.2生成文本"""
        try:
            response = client.chat.completions.create(
                model=GPT_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"  ❌ 文本生成失败: {e}")
            return None

    def generate_image(self, prompt, size="1024x1024", quality="standard",
                      deployment=IMAGE_DEPLOYMENT):
        """使用Azure DALL-E生成图像"""
        try:
            # 注意：这里使用的是Azure OpenAI的图像生成API
            # 根据你的部署可能需要调整
            response = client.images.generate(
                model=deployment,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1
            )
            return response.data[0].url
        except Exception as e:
            print(f"  ❌ 图像生成失败: {e}")
            return None

    def download_image(self, url, filepath):
        """下载图像到本地"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            print(f"  ❌ 图像下载失败: {e}")
            return False

    # ========== 任务1：生成书籍封面 ==========
    def task_generate_covers(self, num_variants=3):
        """批量生成书籍封面（多个变体）"""
        print("\n📚 任务1：生成书籍封面")
        print(f"目标：生成 {num_variants} 个封面变体")
        print("=" * 60)

        # 首先用GPT-5.2生成封面设计提示词
        design_prompt = """
        为技术书籍《Research Engineering OS: 把返工压缩成规范 + 模板 + 检查清单》设计封面。

        书籍信息：
        - 目标读者：AI/ML/计算生物学研究人员
        - 核心主题：研究代码管理、实验可复现性、AI时代工作流
        - 风格：专业、学术、现代、简洁

        请生成3个不同风格的封面设计提示词（英文），每个包括：
        1. 视觉风格
        2. 配色方案
        3. 主要元素
        4. 排版布局

        格式：JSON数组
        """

        print("\n🎨 Step 1: 生成封面设计方案...")
        design_concepts = self.generate_text(
            design_prompt,
            system_prompt="You are a professional book cover designer.",
            max_tokens=1500
        )

        if not design_concepts:
            print("  ❌ 设计方案生成失败")
            return

        print(f"  ✓ 设计方案已生成")

        # 保存设计方案
        with open(self.covers_dir / "design_concepts.txt", 'w', encoding='utf-8') as f:
            f.write(design_concepts)

        # 解析或直接使用设计概念生成图像
        cover_prompts = [
            # 方案1：极简主义
            """Professional book cover design for 'Research Engineering OS',
            minimalist style, clean typography, geometric shapes,
            color scheme: deep blue (#003366) and white,
            subtle git branch visualization in background,
            modern sans-serif fonts, academic yet approachable,
            dimensions: portrait 1600x2560px for Kindle""",

            # 方案2：技术插画
            """Technical book cover for 'Research Engineering OS',
            isometric illustration style, showing code repository structure,
            experiment workflow diagram, git branches,
            color palette: teal, orange, purple gradients,
            clean modern design, flat illustration,
            typography: bold title, clean subtitle,
            professional tech book aesthetic""",

            # 方案3：抽象概念
            """Abstract book cover for 'Research Engineering OS',
            flowing network of interconnected nodes representing experiments,
            gradient background: dark blue to light cyan,
            glowing connection lines, data visualization aesthetic,
            futuristic yet trustworthy feel,
            elegant typography overlay,
            suitable for academic and tech audience"""
        ]

        print(f"\n🖼️  Step 2: 生成 {len(cover_prompts)} 个封面图像...")

        for i, prompt in enumerate(cover_prompts, 1):
            print(f"\n  [{i}/{len(cover_prompts)}] 生成封面变体 {i}...")

            # 使用FLUX.2-pro生成高质量封面
            image_url = self.generate_image(
                prompt=prompt,
                size="1024x1792",  # 接近书籍比例
                quality="hd",
                deployment=FLUX_DEPLOYMENT
            )

            if image_url:
                filepath = self.covers_dir / f"cover_variant_{i}.png"
                if self.download_image(image_url, filepath):
                    print(f"    ✓ 保存到: {filepath}")
                else:
                    print(f"    ⚠️  下载失败")
            else:
                print(f"    ⚠️  生成失败")

            # 避免API限流
            time.sleep(2)

        print(f"\n✅ 封面生成完成！查看目录: {self.covers_dir}")

    # ========== 任务2：生成章节配图 ==========
    def task_generate_chapter_images(self):
        """为每个章节生成配图"""
        print("\n🎨 任务2：生成章节配图")
        print(f"目标：为 {len(CHAPTERS)} 个章节各生成1张配图")
        print("=" * 60)

        for i, chapter in enumerate(CHAPTERS, 1):
            print(f"\n[{i}/{len(CHAPTERS)}] 章节 {chapter['id']}: {chapter['title']}")

            # 构建图像生成提示词
            prompt = f"""
            Create a conceptual illustration for a book chapter titled '{chapter['title']}'.

            Context: Technical book about research engineering and reproducible science.
            Keywords: {chapter['keywords']}
            Style: Clean, modern, minimalist, technical illustration
            Color theme: {chapter['color_theme']}, professional

            Requirements:
            - Abstract or symbolic representation
            - Suitable for technical documentation
            - Clear visual metaphor
            - Not too complex, easy to understand at small size
            """

            print(f"  🖼️  生成图像...")
            image_url = self.generate_image(
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                deployment=IMAGE_DEPLOYMENT
            )

            if image_url:
                filename = f"chapter_{chapter['id']}_{chapter['file'].replace('.md', '')}.png"
                filepath = self.chapter_images_dir / filename

                if self.download_image(image_url, filepath):
                    print(f"    ✓ 保存到: {filepath}")
                else:
                    print(f"    ⚠️  下载失败")
            else:
                print(f"    ⚠️  生成失败")

            # 避免API限流
            time.sleep(3)

        print(f"\n✅ 章节配图生成完成！查看目录: {self.chapter_images_dir}")

    # ========== 任务3：生成社交媒体卡片 ==========
    def task_generate_social_cards(self):
        """为每个章节生成社交媒体分享卡片"""
        print("\n📱 任务3：生成社交媒体分享卡片")
        print(f"目标：为 {len(CHAPTERS)} 个章节各生成1张卡片")
        print("=" * 60)

        for i, chapter in enumerate(CHAPTERS, 1):
            print(f"\n[{i}/{len(CHAPTERS)}] 章节 {chapter['id']}: {chapter['title']}")

            # 先用GPT-5.2提取章节金句
            print(f"  💬 提取金句...")

            # 读取章节内容
            chapter_path = Path(f"mdbook/src/{chapter['file']}")
            if chapter_path.exists():
                with open(chapter_path, 'r', encoding='utf-8') as f:
                    content = f.read()[:2000]  # 只读前2000字符

                quote_prompt = f"""
                从以下章节内容中提取1句最有影响力的金句（20-40字）：

                {content}

                要求：
                - 简短有力
                - 适合社交媒体分享
                - 体现核心观点

                只输出金句本身，不要其他内容。
                """

                quote = self.generate_text(
                    quote_prompt,
                    max_tokens=100
                )

                if quote:
                    quote = quote.strip().strip('"\'')
                    print(f"    金句: {quote}")
                else:
                    quote = chapter['title']
            else:
                quote = chapter['title']

            # 生成社交媒体卡片
            card_prompt = f"""
            Create a social media share card (1200x630px) for a book chapter.

            Text to include: "{quote}"
            Chapter title: {chapter['title']}

            Design requirements:
            - Clean, modern design
            - Readable text overlay
            - {chapter['color_theme']} color scheme
            - Book branding: "Research Engineering OS"
            - Professional tech aesthetic
            - Optimized for Twitter/LinkedIn sharing
            """

            print(f"  🎴 生成分享卡片...")
            # 注意：大部分图像生成API不直接支持文本叠加
            # 这里生成背景图，之后需要用PIL添加文字

            image_url = self.generate_image(
                prompt=card_prompt,
                size="1024x1024",  # 会后期裁剪为1200x630
                quality="standard",
                deployment=IMAGE_DEPLOYMENT
            )

            if image_url:
                filename = f"social_card_{chapter['id']}.png"
                filepath = self.social_cards_dir / filename

                if self.download_image(image_url, filepath):
                    print(f"    ✓ 保存到: {filepath}")

                    # 保存金句到文本文件
                    quote_file = self.social_cards_dir / f"quote_{chapter['id']}.txt"
                    with open(quote_file, 'w', encoding='utf-8') as f:
                        f.write(quote)
                else:
                    print(f"    ⚠️  下载失败")
            else:
                print(f"    ⚠️  生成失败")

            time.sleep(3)

        print(f"\n✅ 社交卡片生成完成！查看目录: {self.social_cards_dir}")

    # ========== 任务4：生成补充代码示例 ==========
    def task_generate_code_examples(self):
        """为关键章节生成补充代码示例"""
        print("\n💻 任务4：生成补充代码示例")
        print("=" * 60)

        # 选择需要代码示例的章节
        code_chapters = [
            {"id": "02", "title": "实验单元", "topic": "实验对象封装"},
            {"id": "03", "title": "仓库结构", "topic": "项目模板生成器"},
            {"id": "04", "title": "Git证明", "topic": "Git hooks实现"},
            {"id": "05", "title": "DoD", "topic": "自动化检查脚本"},
            {"id": "06", "title": "日志", "topic": "结构化日志库"},
        ]

        for i, chapter in enumerate(code_chapters, 1):
            print(f"\n[{i}/{len(code_chapters)}] {chapter['title']} - {chapter['topic']}")

            code_prompt = f"""
            为《Research Engineering OS》书籍的"{chapter['title']}"章节编写一个实用的Python代码示例。

            主题: {chapter['topic']}

            要求:
            1. 完整可运行的代码（100-200行）
            2. 包含docstring和注释
            3. 遵循PEP 8规范
            4. 包含使用示例
            5. 适合研究工程场景

            输出格式：纯Python代码，开头用三引号注释说明用途。
            """

            print(f"  ⌨️  生成代码...")
            code = self.generate_text(
                code_prompt,
                system_prompt="You are an expert Python developer specializing in research engineering.",
                max_tokens=2000
            )

            if code:
                filename = f"{chapter['id']}_{chapter['topic'].replace(' ', '_')}.py"
                filepath = self.code_examples_dir / filename

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code)

                print(f"    ✓ 保存到: {filepath}")
            else:
                print(f"    ⚠️  生成失败")

            time.sleep(2)

        print(f"\n✅ 代码示例生成完成！查看目录: {self.code_examples_dir}")

    # ========== 主菜单 ==========
    def run_interactive(self):
        """交互式任务选择"""
        print("\n" + "=" * 60)
        print("  Azure AI 批量任务处理器")
        print("  Research Engineering OS 书籍增强")
        print("=" * 60)

        tasks = [
            ("生成书籍封面（3个变体）", self.task_generate_covers),
            ("生成章节配图（11张）", self.task_generate_chapter_images),
            ("生成社交媒体卡片（11张）", self.task_generate_social_cards),
            ("生成补充代码示例（5个）", self.task_generate_code_examples),
            ("运行所有任务", lambda: self.run_all_tasks())
        ]

        print("\n可用任务:")
        for i, (name, _) in enumerate(tasks, 1):
            print(f"  {i}. {name}")

        print("\n输入任务编号（逗号分隔多个，如 1,2）或 'all' 运行全部:")
        choice = input("> ").strip()

        if choice.lower() == 'all':
            self.run_all_tasks()
        else:
            try:
                selected = [int(x.strip()) for x in choice.split(',')]
                for num in selected:
                    if 1 <= num <= len(tasks):
                        print(f"\n{'='*60}")
                        print(f"执行任务 {num}")
                        print('='*60)
                        tasks[num-1][1]()
            except ValueError:
                print("❌ 输入格式错误")

    def run_all_tasks(self):
        """运行所有任务"""
        print("\n🚀 运行所有任务")

        self.task_generate_covers()
        time.sleep(5)

        self.task_generate_chapter_images()
        time.sleep(5)

        self.task_generate_social_cards()
        time.sleep(5)

        self.task_generate_code_examples()

        print("\n" + "=" * 60)
        print("🎉 所有任务完成！")
        print(f"输出目录: {self.output_dir}")
        print("=" * 60)


def main():
    """主函数"""
    processor = AzureAIBatchProcessor()
    processor.run_interactive()


if __name__ == "__main__":
    main()
