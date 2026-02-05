#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Azure Translator API进行批量并行翻译
支持128进程异步并发模式
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import List, Tuple
import aiohttp
import requests

# Azure Translator配置
AZURE_TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY')
AZURE_TRANSLATOR_ENDPOINT = os.getenv('AZURE_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com')
AZURE_TRANSLATOR_REGION = os.getenv('AZURE_TRANSLATOR_REGION', 'eastasia')

# 基础路径
BASE_PATH = Path("/Users/lihongmin/ideas/Research-Engineering-OS-/manga-book")
SRC_EN_PATH = BASE_PATH / "src_en"
SRC_JA_PATH = BASE_PATH / "src_ja"
SRC_PATH = BASE_PATH / "src"

# 最大并发数
MAX_CONCURRENT = 128

class AzureTranslator:
    """Azure翻译器"""

    def __init__(self):
        self.key = AZURE_TRANSLATOR_KEY
        self.endpoint = AZURE_TRANSLATOR_ENDPOINT
        self.region = AZURE_TRANSLATOR_REGION

    async def translate_text(self, text: str, target_lang: str) -> str:
        """翻译文本"""
        if not self.key:
            print("错误：未设置AZURE_TRANSLATOR_KEY环境变量")
            return text

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-Type': 'application/xml'
        }

        params = {
            'api-version': '3.0',
            'from': 'zh-Hans',
            'to': target_lang
        }

        body = f'<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">{text}</string>'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.endpoint}/translate',
                    headers=headers,
                    params=params,
                    data=body,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 200:
                        result = await resp.text()
                        # 提取翻译结果
                        import xml.etree.ElementTree as ET
                        root = ET.fromstring(result)
                        translated = root.find('.//{http://schemas.microsoft.com/2003/10/Serialization/}string')
                        if translated is not None:
                            return translated.text
                    return text
        except Exception as e:
            print(f"翻译错误: {e}")
            return text

    async def translate_file_content(self, filepath: Path, target_lang: str) -> str:
        """翻译文件内容"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 分离Markdown标记，只翻译文本内容
            import re

            # 提取需要翻译的文本块
            lines = content.split('\n')
            translated_lines = []

            for line in lines:
                # 跳过Markdown标记和已经是英文的内容
                if line.startswith('#') or line.startswith('![') or line.startswith('*') or \
                   line.startswith('---') or line.startswith('```') or not line.strip():
                    translated_lines.append(line)
                else:
                    # 尝试翻译
                    if any(ord(c) >= 0x4E00 for c in line):  # 包含中文
                        translated = await self.translate_text(line, target_lang)
                        translated_lines.append(translated)
                    else:
                        translated_lines.append(line)

            return '\n'.join(translated_lines)

        except Exception as e:
            print(f"处理文件错误 {filepath}: {e}")
            return ""

async def process_file(translator: AzureTranslator, src_file: Path, target_path: Path, target_lang: str, semaphore: asyncio.Semaphore):
    """处理单个文件的翻译"""
    async with semaphore:
        try:
            translated_content = await translator.translate_file_content(src_file, target_lang)
            target_file = target_path / src_file.name

            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)

            print(f"✓ {src_file.name} -> {target_lang}")
            return True
        except Exception as e:
            print(f"✗ {src_file.name}: {e}")
            return False

async def translate_all_files_async(translator: AzureTranslator, target_lang: str, target_path: Path):
    """异步并行翻译所有文件"""
    # 获取所有markdown文件
    md_files = list(SRC_PATH.glob('*.md')) + list(SRC_PATH.glob('*/*.md'))

    print(f"\n开始翻译 {len(md_files)} 个文件到 {target_lang}...")

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
    if not AZURE_TRANSLATOR_KEY:
        print("错误: 未设置 AZURE_TRANSLATOR_KEY 环境变量")
        print("请设置: export AZURE_TRANSLATOR_KEY='your-key'")
        return

    print(f"Azure Translator 配置:")
    print(f"  端点: {AZURE_TRANSLATOR_ENDPOINT}")
    print(f"  区域: {AZURE_TRANSLATOR_REGION}")
    print(f"  最大并发: {MAX_CONCURRENT}")

    translator = AzureTranslator()

    # 翻译到英文
    print("\n" + "="*50)
    print("翻译到英文 (English)")
    print("="*50)
    en_success, en_failed = await translate_all_files_async(translator, 'en', SRC_EN_PATH)

    # 翻译到日文
    print("\n" + "="*50)
    print("翻译到日文 (日本語)")
    print("="*50)
    ja_success, ja_failed = await translate_all_files_async(translator, 'ja', SRC_JA_PATH)

    # 总结
    print("\n" + "="*50)
    print("翻译完成总结")
    print("="*50)
    print(f"英文: 成功 {en_success}, 失败 {en_failed}")
    print(f"日文: 成功 {ja_success}, 失败 {ja_failed}")

if __name__ == '__main__':
    # 运行异步主函数
    asyncio.run(main())
