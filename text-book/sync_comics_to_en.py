#!/usr/bin/env python3
"""Sync comic images from Chinese markdown to English markdown."""

import re
from pathlib import Path

def extract_comics_with_context(content: str) -> list:
    """Extract comic images with their preceding heading context."""
    lines = content.split('\n')
    comics = []
    current_heading = ""

    for i, line in enumerate(lines):
        # Track current heading
        if line.startswith('#'):
            current_heading = line.strip()
        # Find comic image
        match = re.match(r'!\[([^\]]*)\]\((images/comics/[^)]+)\)', line)
        if match:
            alt_text = match.group(1)
            img_path = match.group(2)
            comics.append({
                'line_num': i,
                'heading': current_heading,
                'alt_text': alt_text,
                'img_path': img_path,
                'full_line': line
            })
    return comics

def remove_existing_comics(content: str) -> str:
    """Remove all existing comic images from content."""
    # Remove comic image lines
    content = re.sub(r'\n*!\[[^\]]*\]\(images/comics/[^)]+\)\n*', '\n', content)
    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content

def find_heading_line(lines: list, zh_heading: str) -> int:
    """Find the corresponding English heading line number."""
    # Extract heading level and approximate content
    zh_level = len(re.match(r'^(#+)', zh_heading).group(1))

    for i, line in enumerate(lines):
        if line.startswith('#' * zh_level) and not line.startswith('#' * (zh_level + 1)):
            return i
    return -1

def sync_comics(zh_file: Path, en_file: Path):
    """Sync comics from Chinese file to English file."""
    zh_content = zh_file.read_text(encoding='utf-8')
    en_content = en_file.read_text(encoding='utf-8')

    # Extract comics from Chinese version
    zh_comics = extract_comics_with_context(zh_content)

    if not zh_comics:
        print(f"  跳过 {zh_file.name}: 无配图")
        return 0

    # Remove existing comics from English version
    en_content = remove_existing_comics(en_content)
    en_lines = en_content.split('\n')

    # Build a map of heading positions in English
    en_headings = []
    for i, line in enumerate(en_lines):
        if line.startswith('#'):
            en_headings.append((i, line))

    # Insert comics at similar positions
    insertions = []  # (line_num, image_line)

    for comic in zh_comics:
        zh_heading = comic['heading']
        zh_line = comic['line_num']

        # Find the heading index in Chinese
        zh_lines = zh_content.split('\n')
        zh_heading_indices = [(i, l) for i, l in enumerate(zh_lines) if l.startswith('#')]

        # Find which heading this comic follows
        comic_heading_idx = -1
        for idx, (line_num, heading) in enumerate(zh_heading_indices):
            if line_num <= zh_line:
                comic_heading_idx = idx
            else:
                break

        # Map to English heading at same index
        if comic_heading_idx >= 0 and comic_heading_idx < len(en_headings):
            en_line_num = en_headings[comic_heading_idx][0]
            img_line = f"\n![{comic['alt_text']}]({comic['img_path']})"
            insertions.append((en_line_num + 1, img_line))

    # Sort insertions by line number (descending to avoid offset issues)
    insertions.sort(key=lambda x: x[0], reverse=True)

    # Apply insertions
    for line_num, img_line in insertions:
        # Check if image already exists nearby
        nearby = '\n'.join(en_lines[max(0, line_num-2):min(len(en_lines), line_num+3)])
        img_file = re.search(r'images/comics/([^)]+)', img_line)
        if img_file and img_file.group(1) not in nearby:
            en_lines.insert(line_num, img_line)

    # Write back
    result = '\n'.join(en_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    en_file.write_text(result, encoding='utf-8')

    return len(insertions)

def main():
    src_zh = Path(__file__).parent / 'src'
    src_en = Path(__file__).parent / 'src_en'

    print("🔄 同步中文配图到英文版...")
    print("=" * 50)

    total = 0

    # Get matching files
    for zh_file in sorted(src_zh.glob('*.md')):
        en_file = src_en / zh_file.name
        if en_file.exists():
            count = sync_comics(zh_file, en_file)
            if count > 0:
                print(f"  ✅ {zh_file.name}: {count} 张配图")
                total += count

    print("=" * 50)
    print(f"✅ 完成: 同步 {total} 张配图")

if __name__ == '__main__':
    main()
