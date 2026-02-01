#!/usr/bin/env python3
"""
书籍插图和漫画批量生成器
使用Azure AI为《Research Engineering OS》生成丰富的视觉内容
"""

import os
import time
from pathlib import Path
from openai import AzureOpenAI
import requests

# Azure配置
client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
)

GPT_DEPLOYMENT = "gpt-5.2"
IMAGE_DEPLOYMENT = "gpt-image-1.5"
FLUX_DEPLOYMENT = "FLUX.2-pro"


class IllustrationGenerator:
    """插图生成器"""

    def __init__(self, output_dir="illustrations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # 创建分类目录
        self.comics_dir = self.output_dir / "comics"
        self.diagrams_dir = self.output_dir / "diagrams"
        self.concepts_dir = self.output_dir / "concepts"
        self.scenarios_dir = self.output_dir / "scenarios"

        for d in [self.comics_dir, self.diagrams_dir,
                  self.concepts_dir, self.scenarios_dir]:
            d.mkdir(exist_ok=True)

    def generate_image(self, prompt, filepath, deployment=IMAGE_DEPLOYMENT,
                      size="1024x1024", quality="standard"):
        """生成并保存图像"""
        try:
            print(f"  🎨 生成中...", end=" ")
            response = client.images.generate(
                model=deployment,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1
            )

            image_url = response.data[0].url
            print(f"下载中...", end=" ")

            # 下载图像
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()

            with open(filepath, 'wb') as f:
                f.write(img_response.content)

            print(f"✓ {filepath.name}")
            return True

        except Exception as e:
            print(f"❌ {e}")
            return False

    # ========== 类型1：漫画式场景 ==========
    def generate_comics(self):
        """生成漫画风格的故事场景"""
        print("\n📚 生成漫画式场景")
        print("风格：简洁、幽默、技术主题")
        print("=" * 60)

        comic_scenarios = [
            {
                "name": "01_deadline_panic",
                "title": "临deadline前的混乱",
                "prompt": """Comic-style illustration: A researcher panicking at their desk,
                surrounded by floating error messages and broken git branches,
                clock showing midnight, coffee cups everywhere,
                laptop screen showing 'merge conflict', papers flying,
                style: clean line art, simple colors, humorous tone,
                technical accuracy maintained"""
            },
            {
                "name": "02_clean_workflow",
                "title": "井然有序的工作流",
                "prompt": """Comic-style illustration: Same researcher now calm and organized,
                clean desk with organized git workflow visualization,
                checklist with checkmarks, automated testing passing,
                green CI/CD pipeline, peaceful expression,
                style: clean line art, simple colors, inspirational tone"""
            },
            {
                "name": "03_ai_assistant_helper",
                "title": "AI助手的正确使用",
                "prompt": """Comic panel illustration: Researcher using AI coding assistant,
                one panel shows blindly accepting suggestions (X mark),
                another panel shows carefully reviewing and testing (checkmark),
                split screen showing good vs bad practices,
                style: educational comic, clear visual metaphors"""
            },
            {
                "name": "04_experiment_explosion",
                "title": "实验结果难复现",
                "prompt": """Comic illustration: Researcher confused looking at two laptops,
                same code giving different results, question marks floating,
                missing config files, unclear environment,
                style: relatable tech humor, simple line art"""
            },
            {
                "name": "05_git_time_machine",
                "title": "Git作为时光机",
                "prompt": """Comic-style illustration: Researcher traveling through git history,
                viewing past commits like a timeline, finding the exact moment bug was introduced,
                'git bisect' shown as a detective tool,
                style: creative visualization, tech metaphor"""
            },
        ]

        for i, scenario in enumerate(comic_scenarios, 1):
            print(f"\n[{i}/{len(comic_scenarios)}] {scenario['title']}")
            filepath = self.comics_dir / f"{scenario['name']}.png"

            self.generate_image(
                prompt=scenario['prompt'],
                filepath=filepath,
                deployment=FLUX_DEPLOYMENT,
                size="1024x1024",
                quality="hd"
            )

            time.sleep(3)

        print(f"\n✅ 漫画生成完成: {self.comics_dir}")

    # ========== 类型2：流程图和架构图 ==========
    def generate_diagrams(self):
        """生成技术流程图"""
        print("\n📊 生成流程图和架构图")
        print("=" * 60)

        diagrams = [
            {
                "name": "01_experiment_workflow",
                "title": "实验工作流程",
                "prompt": """Clean technical diagram showing research experiment workflow:
                Start → Configure → Execute → Log → Validate → Archive
                Each step with icons, arrows showing flow,
                side notes showing key files (run.json, run.md),
                style: minimalist, professional, flat design,
                color scheme: blue and white"""
            },
            {
                "name": "02_repo_structure",
                "title": "仓库结构可视化",
                "prompt": """Technical diagram of research code repository structure:
                Root directory branching to: src/ (slow), experiments/ (fast),
                configs/, outputs/, tests/,
                visual hierarchy showing which parts change frequently,
                style: isometric view, clean icons, organized layout"""
            },
            {
                "name": "03_git_provenance",
                "title": "Git证据链",
                "prompt": """Visualization of git provenance chain:
                Commit history → Code changes → Config → Results → Publication,
                arrows showing traceable lineage,
                timestamp and hash labels,
                style: flowchart, professional, academic"""
            },
            {
                "name": "04_three_debts",
                "title": "三种技术债",
                "prompt": """Concept diagram showing three types of research debt:
                1. Exploration debt (rapid prototyping shortcuts)
                2. Validation debt (missing control experiments)
                3. Reproducibility debt (undocumented environment)
                Each with icon and brief description,
                interconnected arrows showing relationships,
                style: infographic, clean, educational"""
            },
            {
                "name": "05_dod_checklist",
                "title": "完成定义检查清单",
                "prompt": """Visual checklist diagram for 'Definition of Done':
                Checkbox items for: Code tested, Documented, Committed,
                Reproducible, Reviewed, Archived,
                progress bar visualization,
                style: modern UI design, clean icons"""
            },
        ]

        for i, diagram in enumerate(diagrams, 1):
            print(f"\n[{i}/{len(diagrams)}] {diagram['title']}")
            filepath = self.diagrams_dir / f"{diagram['name']}.png"

            self.generate_image(
                prompt=diagram['prompt'],
                filepath=filepath,
                deployment=IMAGE_DEPLOYMENT,
                size="1024x1024"
            )

            time.sleep(3)

        print(f"\n✅ 流程图生成完成: {self.diagrams_dir}")

    # ========== 类型3：概念可视化 ==========
    def generate_concept_visualizations(self):
        """生成抽象概念的视觉表达"""
        print("\n💡 生成概念可视化")
        print("=" * 60)

        concepts = [
            {
                "name": "01_fast_slow_variables",
                "title": "快变量vs慢变量",
                "prompt": """Abstract visualization of fast vs slow variables:
                Left side: rapidly changing experiment scripts (motion blur effect),
                Right side: stable core library (solid, structured),
                clear visual separation,
                style: minimalist, conceptual, split-screen design"""
            },
            {
                "name": "02_exploration_path",
                "title": "探索路径分支",
                "prompt": """Visualization of experimental exploration paths:
                Tree structure with main trunk (validated approach)
                and multiple branches (explorations),
                some branches marked with X (failed),
                some with checkmarks (promising),
                style: organic tree metaphor, technical accuracy"""
            },
            {
                "name": "03_reproducibility_spectrum",
                "title": "可复现性光谱",
                "prompt": """Spectrum visualization from 'not reproducible' to 'fully reproducible':
                Left (red): messy, no docs, broken,
                Right (green): automated, documented, containerized,
                gradient showing stages in between,
                icons representing each level"""
            },
            {
                "name": "04_ai_verification_loop",
                "title": "AI代码验证循环",
                "prompt": """Circular flow diagram showing AI-assisted development:
                AI suggests code → Human reviews → Tests run →
                Validation → Accept or reject → Learn,
                emphasis on human-in-the-loop,
                style: modern tech illustration"""
            },
            {
                "name": "05_technical_debt_accumulation",
                "title": "技术债累积曲线",
                "prompt": """Graph visualization showing technical debt accumulation:
                X-axis: project timeline,
                Y-axis: debt amount,
                curve showing slow accumulation then sudden spike near deadline,
                danger zone marked in red,
                style: clean chart, professional"""
            },
        ]

        for i, concept in enumerate(concepts, 1):
            print(f"\n[{i}/{len(concepts)}] {concept['title']}")
            filepath = self.concepts_dir / f"{concept['name']}.png"

            self.generate_image(
                prompt=concept['prompt'],
                filepath=filepath,
                deployment=IMAGE_DEPLOYMENT,
                size="1024x1024"
            )

            time.sleep(3)

        print(f"\n✅ 概念图生成完成: {self.concepts_dir}")

    # ========== 类型4：真实场景案例 ==========
    def generate_scenario_illustrations(self):
        """生成真实研究场景的示意图"""
        print("\n🔬 生成场景案例图")
        print("=" * 60)

        scenarios = [
            {
                "name": "01_notebook_vs_script",
                "title": "Notebook vs Script对比",
                "prompt": """Side-by-side comparison illustration:
                Left: Jupyter notebook (exploratory, cells, outputs visible),
                Right: Python script (production, clean, modular),
                annotations showing use cases for each,
                style: educational comparison, clear labels"""
            },
            {
                "name": "02_broken_environment",
                "title": "环境不一致的困境",
                "prompt": """Illustration showing environment inconsistency problem:
                Same code running on three computers,
                different results on each screen,
                missing dependencies, version conflicts,
                frustrated researchers,
                style: problem illustration, relatable"""
            },
            {
                "name": "03_successful_handoff",
                "title": "成功的项目交接",
                "prompt": """Illustration of successful project handoff:
                Two researchers, one explaining, one understanding,
                laptop showing clear documentation,
                README, setup script, test passing,
                smooth knowledge transfer,
                style: positive, collaborative, professional"""
            },
            {
                "name": "04_automated_testing",
                "title": "自动化测试保护网",
                "prompt": """Visualization of automated testing as safety net:
                Code changes at top, falling through layers of tests
                (unit → integration → E2E),
                bugs caught at each level,
                style: protective layers metaphor"""
            },
            {
                "name": "05_config_management",
                "title": "配置管理最佳实践",
                "prompt": """Illustration showing proper config management:
                Centralized config files, version controlled,
                environment-specific configs separated,
                secrets properly handled,
                clear visual organization,
                style: organizational diagram, clean"""
            },
        ]

        for i, scenario in enumerate(scenarios, 1):
            print(f"\n[{i}/{len(scenarios)}] {scenario['title']}")
            filepath = self.scenarios_dir / f"{scenario['name']}.png"

            self.generate_image(
                prompt=scenario['prompt'],
                filepath=filepath,
                deployment=IMAGE_DEPLOYMENT,
                size="1024x1024"
            )

            time.sleep(3)

        print(f"\n✅ 场景图生成完成: {self.scenarios_dir}")

    def run_all(self):
        """生成所有插图"""
        print("\n" + "=" * 60)
        print("  插图批量生成器")
        print("  Research Engineering OS")
        print("=" * 60)
        print(f"输出目录: {self.output_dir}")
        print("=" * 60)

        self.generate_comics()
        time.sleep(5)

        self.generate_diagrams()
        time.sleep(5)

        self.generate_concept_visualizations()
        time.sleep(5)

        self.generate_scenario_illustrations()

        print("\n" + "=" * 60)
        print("🎉 所有插图生成完成！")
        print(f"\n生成的插图:")
        print(f"  - 漫画: {len(list(self.comics_dir.glob('*.png')))} 张")
        print(f"  - 流程图: {len(list(self.diagrams_dir.glob('*.png')))} 张")
        print(f"  - 概念图: {len(list(self.concepts_dir.glob('*.png')))} 张")
        print(f"  - 场景图: {len(list(self.scenarios_dir.glob('*.png')))} 张")
        print(f"\n总计: {len(list(self.output_dir.rglob('*.png')))} 张")
        print("=" * 60)

        self.generate_markdown_gallery()

    def generate_markdown_gallery(self):
        """生成图片画廊Markdown"""
        gallery_md = "# 插图画廊\n\n"

        categories = [
            ("comics", "漫画式场景"),
            ("diagrams", "流程图和架构图"),
            ("concepts", "概念可视化"),
            ("scenarios", "真实场景案例")
        ]

        for dirname, title in categories:
            category_dir = self.output_dir / dirname
            images = sorted(category_dir.glob("*.png"))

            if images:
                gallery_md += f"## {title}\n\n"
                for img in images:
                    name = img.stem.replace("_", " ").title()
                    gallery_md += f"### {name}\n"
                    gallery_md += f"![{name}]({dirname}/{img.name})\n\n"

        gallery_path = self.output_dir / "GALLERY.md"
        with open(gallery_path, 'w', encoding='utf-8') as f:
            f.write(gallery_md)

        print(f"\n📖 图片画廊已生成: {gallery_path}")


def main():
    """主函数"""
    generator = IllustrationGenerator()

    print("\n可用任务:")
    print("  1. 生成漫画式场景 (5张)")
    print("  2. 生成流程图和架构图 (5张)")
    print("  3. 生成概念可视化 (5张)")
    print("  4. 生成真实场景案例 (5张)")
    print("  5. 生成所有插图 (20张)")

    choice = input("\n选择任务 (1-5): ").strip()

    if choice == "1":
        generator.generate_comics()
    elif choice == "2":
        generator.generate_diagrams()
    elif choice == "3":
        generator.generate_concept_visualizations()
    elif choice == "4":
        generator.generate_scenario_illustrations()
    elif choice == "5":
        generator.run_all()
    else:
        print("无效选择")


if __name__ == "__main__":
    main()
