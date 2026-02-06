#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全版翻译脚本 - 低并发 + 断点续传
"""

import os
import sys
import asyncio
import re
import json
from pathlib import Path
from typing import Optional
import aiohttp

# Azure OpenAI配置
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://eastus2.api.cognitive.microsoft.com/')
AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2024-08-01-preview')
DEPLOYMENT_NAME = 'gpt-5.2'

# 基础路径
BASE_PATH = Path("/Users/lihongmin/ideas/Research-Engineering-OS-/manga-book")
SRC_EN_PATH = BASE_PATH / "src_en"
SRC_JA_PATH = BASE_PATH / "src_ja"
SRC_PATH = BASE_PATH / "src"

# 降低并发数
MAX_CONCURRENT = 5  # 从 128 降到 5

# 进度文件
PROGRESS_FILE = BASE_PATH / ".translation_progress.json"

def load_progress():
    """加载翻译进度"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"en": [], "ja": []}

def save_progress(progress):
    """保存翻译进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

class AzureOpenAITranslator:
    """Azure OpenAI翻译器"""

    def __init__(self):
        self.endpoint = AZURE_OPENAI_ENDPOINT.rstrip('/')
        self.key = AZURE_OPENAI_KEY
        self.version = AZURE_OPENAI_VERSION
        self.deployment = DEPLOYMENT_NAME

    async def translate_text(self, text: str, target_lang: str, session: aiohttp.ClientSession) -> str:
        """翻译文本"""
        
        # 跳过图片路径和某些特殊内容
        if not text.strip() or text.startswith('![') or text.startswith('../images/'):
            return text
            
        # 构建提示词
        if target_lang == 'en':
            system_prompt = "You are a professional translator. Translate the following Chinese text to English. Preserve markdown formatting and image paths (keep them unchanged). Only translate the text content."
        elif target_lang == 'ja':
            system_prompt = "You are a professional translator. Translate the following Chinese text to Japanese. Preserve markdown formatting and image paths (keep them unchanged). Only translate the text content."
        else:
            raise ValueError(f"Unsupported language: {target_lang}")

        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.version}"
        
        headers = {
            'api-key': self.key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': text}
            ],
            'temperature': 0.3,
            'max_completion_tokens': 4000
        }

        try:
            async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
                else:
                    error_text = await response.text()
                    print(f"API Error {response.status}: {error_text}")
                    return text  # 失败时返回原文
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # 失败时返回原文

async def translate_file(translator: AzureOpenAITranslator, src_file: Path, target_file: Path, 
                        target_lang: str, session: aiohttp.ClientSession, progress: dict) -> bool:
    """翻译单个文件"""
    
    # 检查是否已完成
    relative_path = str(src_file.relative_to(SRC_PATH))
    if relative_path in progress[target_lang]:
        print(f"⏭️  跳过已完成: {relative_path}")
        return True
    
    try:
        # 读取源文件
        with open(src_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📝 翻译中: {relative_path} -> {target_lang}")
        
        # 按段落翻译
        paragraphs = content.split('\n\n')
        translated_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                translated = await translator.translate_text(para, target_lang, session)
                translated_paragraphs.append(translated)
            else:
                translated_paragraphs.append(para)
        
        translated_content = '\n\n'.join(translated_paragraphs)
        
        # 保存译文
        target_file.parent.mkdir(parents=True, exist_ok=True)
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        # 更新进度
        progress[target_lang].append(relative_path)
        save_progress(progress)
        
        print(f"✅ 完成: {relative_path}")
        return True
        
    except Exception as e:
        print(f"❌ 错误: {relative_path} - {e}")
        return False

async def translate_all_files(translator: AzureOpenAITranslator, target_lang: str, target_dir: Path):
    """翻译所有文件"""
    
    # 获取所有 .md 文件
    md_files = sorted(SRC_PATH.rglob("*.md"))
    progress = load_progress()
    
    print(f"\n找到 {len(md_files)} 个文件")
    print(f"已完成 {len(progress[target_lang])} 个文件")
    print(f"剩余 {len(md_files) - len(progress[target_lang])} 个文件")
    
    # 创建 aiohttp session
    async with aiohttp.ClientSession() as session:
        # 使用 semaphore 控制并发
        semaphore = asyncio.Semaphore(MAX_CONCURRENT)
        
        async def translate_with_semaphore(src_file):
            async with semaphore:
                relative_path = src_file.relative_to(SRC_PATH)
                target_file = target_dir / relative_path
                return await translate_file(translator, src_file, target_file, target_lang, session, progress)
        
        # 并发翻译
        tasks = [translate_with_semaphore(f) for f in md_files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 统计结果
    success = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False or isinstance(r, Exception))
    
    print(f"\n完成: 成功 {success}/{len(md_files)}, 失败 {failed}")
    return success, failed

async def main():
    """主函数"""
    
    if not AZURE_OPENAI_KEY:
        print("❌ 错误: 未设置 AZURE_OPENAI_API_KEY 环境变量")
        return

    print("=" * 60)
    print("🌐 Azure OpenAI 翻译配置")
    print("=" * 60)
    print(f"端点: {AZURE_OPENAI_ENDPOINT}")
    print(f"部署: {DEPLOYMENT_NAME}")
    print(f"并发数: {MAX_CONCURRENT}")
    print(f"源目录: {SRC_PATH}")
    print(f"英文输出: {SRC_EN_PATH}")
    print(f"日文输出: {SRC_JA_PATH}")
    print("=" * 60)

    translator = AzureOpenAITranslator()

    # 翻译到英文
    print("\n" + "=" * 60)
    print("📖 第一步: 翻译到英文 (English)")
    print("=" * 60)
    en_success, en_failed = await translate_all_files(translator, 'en', SRC_EN_PATH)

    # 翻译到日文
    print("\n" + "=" * 60)
    print("📖 第二步: 翻译到日文 (日本語)")
    print("=" * 60)
    ja_success, ja_failed = await translate_all_files(translator, 'ja', SRC_JA_PATH)

    # 总结
    print("\n" + "=" * 60)
    print("✨ 翻译完成总结")
    print("=" * 60)
    print(f"英文: 成功 {en_success}, 失败 {en_failed}")
    print(f"日文: 成功 {ja_success}, 失败 {ja_failed}")
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())
