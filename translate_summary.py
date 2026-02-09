#!/usr/bin/env python3
import requests

def translate_summary(source_file, target_file, target_lang):
    """翻译 SUMMARY.md 文件"""
    
    endpoint = "https://eastus2.api.cognitive.microsoft.com/"
    api_key = "3e3a7c53784247a6ad61d3f1bed81752"
    deployment = "gpt-5.2"
    api_version = "2024-08-01-preview"
    
    # 读取源文件
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 准备翻译提示
    if target_lang == 'en':
        system_prompt = "You are a professional translator. Translate the following Chinese text to English. Preserve markdown formatting and links (keep file paths unchanged). Only translate the text content, not the markdown syntax or file paths."
    elif target_lang == 'ja':
        system_prompt = "You are a professional translator. Translate the following Chinese text to Japanese. Preserve markdown formatting and links (keep file paths unchanged). Only translate the text content, not the markdown syntax or file paths."
    
    url = f"{endpoint}openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': content}
        ],
        'temperature': 0.3,
        'max_completion_tokens': 8000
    }
    
    print(f"正在翻译 SUMMARY.md 到 {target_lang}...")
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        result = response.json()
        translated_content = result['choices'][0]['message']['content']
        
        # 保存译文
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"✅ 完成: {target_file}")
        return True
    else:
        print(f"❌ 错误: {response.text}")
        return False

# 翻译到英文
translate_summary(
    '/Users/lihongmin/ideas/Research-Engineering-OS-/manga-book/src/SUMMARY.md',
    '/Users/lihongmin/ideas/Research-Engineering-OS-/manga-book/src_en/SUMMARY.md',
    'en'
)

# 翻译到日文
translate_summary(
    '/Users/lihongmin/ideas/Research-Engineering-OS-/manga-book/src/SUMMARY.md',
    '/Users/lihongmin/ideas/Research-Engineering-OS-/manga-book/src_ja/SUMMARY.md',
    'ja'
)

print("\n✨ SUMMARY.md 翻译完成！")
