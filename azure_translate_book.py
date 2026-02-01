#!/usr/bin/env python3
"""
书籍多语言翻译器
使用Azure OpenAI GPT-5.2批量翻译整本书
"""

import os
from pathlib import Path
from openai import AzureOpenAI
import time

# Azure配置
client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
)

GPT_DEPLOYMENT = "gpt-5.2"

CHAPTERS = [
    "00-preface.md",
    "01-why-flip.md",
    "02-experiment-unit.md",
    "03-repo-layout.md",
    "04-git-proof.md",
    "05-dod.md",
    "06-logging.md",
    "07-ai-workflow.md",
    "08-multi-path.md",
    "no-boom.md",
    "team.md",
    "appendix-templates.md",
    "appendix-ai-disasters.md",
]


class BookTranslator:
    """书籍翻译器"""

    def __init__(self, source_lang="Chinese", target_lang="English"):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.src_dir = Path("mdbook/src")
        self.target_dir = Path(f"mdbook_{target_lang.lower()}/src")
        self.target_dir.mkdir(parents=True, exist_ok=True)

    def translate_chapter(self, chapter_file):
        """翻译单个章节"""
        src_path = self.src_dir / chapter_file
        target_path = self.target_dir / chapter_file

        if not src_path.exists():
            print(f"  ⚠️  源文件不存在: {chapter_file}")
            return False

        print(f"\n📖 读取章节: {chapter_file}")

        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分段翻译（避免超长文本）
        chunks = self.split_content(content, max_length=3000)
        translated_chunks = []

        for i, chunk in enumerate(chunks, 1):
            print(f"  🌐 翻译段落 {i}/{len(chunks)}...", end=" ")

            system_prompt = f"""You are a professional translator specializing in technical and academic content.

Task: Translate from {self.source_lang} to {self.target_lang}.

Requirements:
1. Maintain technical accuracy
2. Preserve markdown formatting (headers, lists, code blocks, links)
3. Keep code blocks unchanged (only translate comments)
4. Preserve technical terms when appropriate
5. Natural, fluent {self.target_lang}
6. Academic writing style suitable for technical books

Special notes:
- Keep run_id, git, JSON, YAML terms untranslated
- Translate code comments in code blocks
- Preserve file paths and commands exactly"""

            user_prompt = f"""Translate the following markdown content to {self.target_lang}:

{chunk}

Output only the translated content, no explanations."""

            try:
                response = client.chat.completions.create(
                    model=GPT_DEPLOYMENT,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_completion_tokens=4000,  # GPT-5.2 uses max_completion_tokens
                    temperature=0.3  # Lower temperature for more consistent translation
                )

                translated = response.choices[0].message.content
                translated_chunks.append(translated)
                print("✓")

                # 避免API限流
                time.sleep(1)

            except Exception as e:
                print(f"❌ 错误: {e}")
                translated_chunks.append(chunk)  # 失败时保留原文

        # 合并翻译结果
        final_translation = "\n\n".join(translated_chunks)

        # 保存翻译
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(final_translation)

        print(f"  ✓ 保存到: {target_path}")
        return True

    def split_content(self, content, max_length=3000):
        """智能分段内容（按段落边界）"""
        if len(content) <= max_length:
            return [content]

        chunks = []
        current_chunk = ""
        paragraphs = content.split('\n\n')

        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 <= max_length:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def translate_book(self):
        """翻译整本书"""
        print("=" * 60)
        print(f"  书籍翻译：{self.source_lang} → {self.target_lang}")
        print("=" * 60)
        print(f"源目录: {self.src_dir}")
        print(f"目标目录: {self.target_dir}")
        print(f"章节数: {len(CHAPTERS)}")
        print("=" * 60)

        success_count = 0

        for i, chapter in enumerate(CHAPTERS, 1):
            print(f"\n[{i}/{len(CHAPTERS)}] {chapter}")
            if self.translate_chapter(chapter):
                success_count += 1

        # 同步其他文件
        self.sync_non_content_files()

        print("\n" + "=" * 60)
        print(f"✅ 翻译完成！")
        print(f"成功: {success_count}/{len(CHAPTERS)} 章")
        print(f"输出目录: {self.target_dir.parent}")
        print("=" * 60)

    def sync_non_content_files(self):
        """同步非内容文件（README, SUMMARY等）"""
        print("\n📋 同步配置文件...")

        # 复制SUMMARY.md并翻译
        summary_src = self.src_dir / "SUMMARY.md"
        summary_target = self.target_dir / "SUMMARY.md"

        if summary_src.exists():
            with open(summary_src, 'r', encoding='utf-8') as f:
                summary_content = f.read()

            # 翻译SUMMARY
            print("  🌐 翻译目录...")
            system_prompt = f"Translate this book table of contents to {self.target_lang}. Keep markdown structure and file paths unchanged."

            try:
                response = client.chat.completions.create(
                    model=GPT_DEPLOYMENT,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": summary_content}
                    ],
                    max_completion_tokens=1000,
                    temperature=0.3
                )

                translated_summary = response.choices[0].message.content

                with open(summary_target, 'w', encoding='utf-8') as f:
                    f.write(translated_summary)

                print("  ✓ SUMMARY.md 已翻译")

            except Exception as e:
                print(f"  ⚠️  SUMMARY翻译失败: {e}")
                # 复制原文
                with open(summary_target, 'w', encoding='utf-8') as f:
                    f.write(summary_content)

        # 翻译README
        readme_src = self.src_dir / "README.md"
        readme_target = self.target_dir / "README.md"

        if readme_src.exists():
            print("  🌐 翻译README...")
            with open(readme_src, 'r', encoding='utf-8') as f:
                readme_content = f.read()

            try:
                system_prompt = f"Translate this book introduction to {self.target_lang}. Keep markdown formatting."
                response = client.chat.completions.create(
                    model=GPT_DEPLOYMENT,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": readme_content}
                    ],
                    max_completion_tokens=2000,
                    temperature=0.3
                )

                translated_readme = response.choices[0].message.content

                with open(readme_target, 'w', encoding='utf-8') as f:
                    f.write(translated_readme)

                print("  ✓ README.md 已翻译")

            except Exception as e:
                print(f"  ⚠️  README翻译失败: {e}")

        # 复制images目录
        images_src = self.src_dir / "images"
        images_target = self.target_dir / "images"

        if images_src.exists():
            import shutil
            shutil.copytree(images_src, images_target, dirs_exist_ok=True)
            print("  ✓ 图片目录已复制")

    def create_book_toml(self):
        """为翻译版创建book.toml"""
        book_toml_content = f"""[book]
title = "Research Engineering OS"
description = "Compressing Rework into Standards + Templates + Checklists"
authors = ["Li Hongmin (李鸿敏)"]
language = "{self.target_lang.lower()[:2]}"
src = "src"

[build]
build-dir = "book"

[output.html]
default-theme = "light"
preferred-dark-theme = "navy"
additional-css = ["theme/custom.css"]

[output.html.search]
enable = true

[output.pdf]
optional = true
"""

        toml_path = self.target_dir.parent / "book.toml"
        with open(toml_path, 'w', encoding='utf-8') as f:
            f.write(book_toml_content)

        print(f"  ✓ book.toml 已创建: {toml_path}")


def main():
    """主函数"""
    print("🌍 Research Engineering OS - 多语言翻译器")
    print("\n可用语言:")
    print("  1. English (英语)")
    print("  2. Japanese (日语)")
    print("  3. Spanish (西班牙语)")
    print("  4. French (法语)")
    print("  5. German (德语)")

    choice = input("\n选择目标语言 (1-5，默认1): ").strip() or "1"

    lang_map = {
        "1": "English",
        "2": "Japanese",
        "3": "Spanish",
        "4": "French",
        "5": "German"
    }

    target_lang = lang_map.get(choice, "English")

    print(f"\n目标语言: {target_lang}")
    confirm = input("确认开始翻译？(y/N): ").strip().lower()

    if confirm == 'y':
        translator = BookTranslator(target_lang=target_lang)
        translator.translate_book()
        translator.create_book_toml()

        print("\n下一步:")
        print(f"  cd mdbook_{target_lang.lower()}")
        print("  mdbook build")
        print("  mdbook serve")
    else:
        print("已取消")


if __name__ == "__main__":
    main()
