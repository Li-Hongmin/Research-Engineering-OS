#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Azure OpenAI API进行批量并行翻译
支持128进程异步并发模式
"""

import os
import sys
import asyncio
import re
from pathlib import Path
from typing import Optional
import aiohttp

# Azure OpenAI配置
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://eastus2.api.cognitive.microsoft.com/')
AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2024-08-01-preview')

# 基础路径
BASE_PATH = Path("/Users/lihongmin/ideas/Research-Engineering-OS-/manga-book")
SRC_EN_PATH = BASE_PATH / "src_en"
SRC_JA_PATH = BASE_PATH / "src_ja"
SRC_PATH = BASE_PATH / "src"

# 最大并发数
MAX_CONCURRENT = 10  # 降低到 10 避免过载

class TranslationCache:
    """翻译缓存"""
    def __init__(self):
        self.cache = {}

    def get(self, key: str) -> Optional[str]:
        return self.cache.get(key)

    def set(self, key: str, value: str):
        self.cache[key] = value

class AzureOpenAITranslator:
    """Azure OpenAI翻译器"""

    def __init__(self):
        self.endpoint = AZURE_OPENAI_ENDPOINT.rstrip('/')
        self.key = AZURE_OPENAI_KEY
        self.version = AZURE_OPENAI_VERSION
        self.cache = TranslationCache()

    async def translate_text(self, text: str, target_lang: str, batch_size: int = 1000) -> str:
        """翻译文本"""
        if not self.key:
            print("错误：未设置AZURE_OPENAI_API_KEY")
            return text

        # 检查缓存
        cache_key = f"{text[:100]}_{target_lang}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        lang_names = {'en': 'English', 'ja': 'Japanese'}
        target_name = lang_names.get(target_lang, target_lang)

        prompt = f"""Translate the following Chinese text to {target_name}.
Keep markdown formatting intact (e.g., **, -, #, etc.).
Keep image references unchanged (e.g., ![...](../images/...)).
Provide only the translated text, no explanations.

Text to translate:
{text}"""

        headers = {
            'api-key': self.key,
            'Content-Type': 'application/json'
        }

        payload = {
            'messages': [
                {'role': 'system', 'content': 'You are a professional translator. Translate the provided text accurately while preserving all formatting.'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.3,
            'max_completion_tokens': min(len(text) * 2, 2000),
            'top_p': 0.95
        }

        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.endpoint}/openai/deployments/gpt-5.2/chat/completions?api-version={self.version}"
                async with session.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        translated = result['choices'][0]['message']['content'].strip()
                        self.cache.set(cache_key, translated)
                        return translated
                    else:
                        error_text = await resp.text()
                        print(f"API错误 ({resp.status}): {error_text}")
                        return text
        except asyncio.TimeoutError:
            print(f"超时: 文本太长或API响应慢")
            return text
        except Exception as e:
            print(f"翻译错误: {e}")
            return text

    def is_chinese(self, text: str) -> bool:
        """检查文本是否包含中文"""
        return any(ord(c) >= 0x4E00 and ord(c) <= 0x9FFF for c in text)

    async def translate_file_content(self, filepath: Path, target_lang: str) -> str:
        """翻译文件内容，保持Markdown格式"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            translated_lines = []

            for i, line in enumerate(lines):
                # 保持特殊行不变
                if not line.strip() or line.startswith('```') or line.startswith('---'):
                    translated_lines.append(line)
                    continue

                # 检查是否需要翻译
                if self.is_chinese(line):
                    # 分段翻译长行
                    if len(line) > 500:
                        # 分割成句子
                        sentences = re.split(r'([。！？])', line)
                        translated_part = []
                        for sent in sentences:
                            if sent and self.is_chinese(sent):
                                trans = await self.translate_text(sent, target_lang)
                                translated_part.append(trans)
                            else:
                                translated_part.append(sent)
                        translated_lines.append(''.join(translated_part))
                    else:
                        translated = await self.translate_text(line, target_lang)
                        translated_lines.append(translated)
                else:
                    translated_lines.append(line)

                # 每处理10行打印进度
                if (i + 1) % 10 == 0:
                    print(f"  处理进度: {i+1}/{len(lines)}")

            return '\n'.join(translated_lines)

        except Exception as e:
            print(f"处理文件错误 {filepath}: {e}")
            return ""

async def process_file(translator: AzureOpenAITranslator, src_file: Path, target_path: Path, target_lang: str, semaphore: asyncio.Semaphore):
    """处理单个文件的翻译"""
    async with semaphore:
        try:
            print(f"\n正在翻译: {src_file.name} -> {target_lang}")
            translated_content = await translator.translate_file_content(src_file, target_lang)

            target_file = target_path / src_file.name
            target_file.parent.mkdir(parents=True, exist_ok=True)

            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)

            print(f"✓ 完成: {src_file.name}")
            return True
        except Exception as e:
            print(f"✗ 失败: {src_file.name}: {e}")
            return False

async def translate_all_files_async(translator: AzureOpenAITranslator, target_lang: str, target_path: Path):
    """异步并行翻译所有文件"""
    # 获取所有markdown文件
    md_files = sorted(list(SRC_PATH.glob('*.md')) + list(SRC_PATH.glob('*/*.md')))

    print(f"\n开始翻译 {len(md_files)} 个文件到 {target_lang}...")
    print(f"最大并发: {MAX_CONCURRENT}")

    # 创建信号量限制并发数
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    # 创建所有翻译任务
    tasks = [
        process_file(translator, md_file, target_path, target_lang, semaphore)
        for md_file in md_files
    ]

    # 并行执行所有任务
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 统计结果
    success = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False or isinstance(r, Exception))

    print(f"\n完成: 成功 {success}/{len(md_files)}, 失败 {failed}")
    return success, failed

async def main():
    """主函数"""
    # 检查Azure配置
    if not AZURE_OPENAI_KEY:
        print("错误: 未设置 AZURE_OPENAI_API_KEY 环境变量")
        return

    print("=" * 60)
    print("Azure OpenAI 批量翻译配置")
    print("=" * 60)
    print(f"端点: {AZURE_OPENAI_ENDPOINT}")
    print(f"API版本: {AZURE_OPENAI_VERSION}")
    print(f"最大并发: {MAX_CONCURRENT}")
    print(f"源文件夹: {SRC_PATH}")
    print(f"英文输出: {SRC_EN_PATH}")
    print(f"日文输出: {SRC_JA_PATH}")
    print("=" * 60)

    # 创建翻译器
    translator = AzureOpenAITranslator()

    # 翻译到英文
    print("\n" + "=" * 60)
    print("第一步: 翻译到英文 (English)")
    print("=" * 60)
    en_success, en_failed = await translate_all_files_async(translator, 'en', SRC_EN_PATH)

    # 翻译到日文
    print("\n" + "=" * 60)
    print("第二步: 翻译到日文 (日本語)")
    print("=" * 60)
    ja_success, ja_failed = await translate_all_files_async(translator, 'ja', SRC_JA_PATH)

    # 总结
    print("\n" + "=" * 60)
    print("翻译完成总结")
    print("=" * 60)
    print(f"英文: 成功 {en_success}, 失败 {en_failed}")
    print(f"日文: 成功 {ja_success}, 失败 {ja_failed}")
    print("=" * 60)

if __name__ == '__main__':
    # 运行异步主函数
    asyncio.run(main())
