#!/usr/bin/env python3
"""
REOS Manga Image Link Checker - Python版
Created: 2026-02-06 15:06 JST
Purpose: 快速准确地检查 manga-book 图片链接有效性
"""

import re
from pathlib import Path
from collections import defaultdict

def check_image_links():
    manga_dir = Path("manga-book")
    if not manga_dir.exists():
        print("❌ manga-book directory not found")
        return 1
    
    print("🔍 REOS Manga Image Link Checker")
    print(f"Started at: {Path.cwd()}")
    print()
    
    total_files = 0
    total_image_links = 0
    broken_image_links = 0
    broken_by_file = defaultdict(list)
    
    # Pattern to match markdown image links
    image_pattern = re.compile(r'!\[.*?\]\(([^)]+)\)')
    
    for lang_dir in ["src", "src_en", "src_ja"]:
        lang_path = manga_dir / lang_dir
        if not lang_path.exists():
            continue
        
        print(f"📁 Checking {lang_dir}...")
        
        for md_file in lang_path.rglob("*.md"):
            total_files += 1
            
            content = md_file.read_text(encoding='utf-8')
            image_links = image_pattern.findall(content)
            
            for link in image_links:
                # Skip external URLs
                if link.startswith('http'):
                    continue
                
                total_image_links += 1
                
                # Resolve relative path from markdown file location
                image_path = (md_file.parent / link).resolve()
                
                if not image_path.exists():
                    broken_image_links += 1
                    rel_md = md_file.relative_to(manga_dir)
                    broken_by_file[str(rel_md)].append((link, str(image_path)))
    
    print()
    print("📊 Summary")
    print(f"  Files scanned:       {total_files}")
    print(f"  Image links found:   {total_image_links}")
    print(f"  Broken links:        {broken_image_links}")
    print(f"  Files with issues:   {len(broken_by_file)}")
    print()
    
    if broken_image_links > 0:
        print("❌ Broken image links:")
        for file, links in sorted(broken_by_file.items()):
            print(f"\n  📄 {file}")
            for link, resolved in links[:3]:  # Show first 3 per file
                print(f"     ✗ {link}")
                print(f"       → {resolved}")
            if len(links) > 3:
                print(f"     ... and {len(links) - 3} more")
        return 1
    else:
        print("✅ All manga image links are valid!")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(check_image_links())
