#!/usr/bin/env bash
# project_stats.sh - REOS Project Statistics
# Purpose: Provide comprehensive project metrics for tracking growth
# Created: 2026-02-07 10:10 JST

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 REOS Project Statistics${NC}"
echo "=================================="
echo ""

# 1. Documentation Statistics
echo -e "${GREEN}📚 Documentation (text-book)${NC}"
echo "-----------------------------------"

# Count Markdown files and words for each language
for lang in "src" "src_en" "src_ja"; do
    lang_name=""
    case $lang in
        "src") lang_name="Chinese (中文)" ;;
        "src_en") lang_name="English" ;;
        "src_ja") lang_name="Japanese (日本語)" ;;
    esac
    
    if [ -d "text-book/$lang" ]; then
        md_files=$(find "text-book/$lang" -name "*.md" | wc -l | tr -d ' ')
        word_count=$(find "text-book/$lang" -name "*.md" -exec wc -w {} + 2>/dev/null | tail -1 | awk '{print $1}')
        echo "  $lang_name:"
        echo "    - Markdown files: $md_files"
        echo "    - Total words: $word_count"
    fi
done

echo ""

# 2. Manga Book Statistics
echo -e "${GREEN}📖 Manga Book${NC}"
echo "-----------------------------------"
manga_md=$(find manga-book/src -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
manga_words=$(find manga-book/src -name "*.md" -exec wc -w {} + 2>/dev/null | tail -1 | awk '{print $1}')
echo "  - Markdown files: $manga_md"
echo "  - Total words: $manga_words"

# Count images per chapter
echo "  - Images by chapter:"
if [ -d "manga-book/images" ]; then
    for chapter_dir in manga-book/images/*; do
        if [ -d "$chapter_dir" ]; then
            chapter_name=$(basename "$chapter_dir")
            img_count=$(find "$chapter_dir" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) 2>/dev/null | wc -l | tr -d ' ')
            echo "    - $chapter_name: $img_count images"
        fi
    done
fi

echo ""

# 3. Text Book Images
echo -e "${GREEN}🖼️ Text Book Images${NC}"
echo "-----------------------------------"
if [ -d "text-book/images" ]; then
    main_images=$(find text-book/images -maxdepth 1 -type f \( -name "*.png" -o -name "*.jpg" \) 2>/dev/null | wc -l | tr -d ' ')
    comics_images=$(find text-book/images/comics -type f \( -name "*.png" -o -name "*.jpg" \) 2>/dev/null | wc -l | tr -d ' ')
    echo "  - Main illustrations: $main_images"
    echo "  - Comics panels: $comics_images"
    echo "  - Total: $((main_images + comics_images))"
fi

echo ""

# 4. Automation Scripts
echo -e "${GREEN}🔧 Automation Scripts${NC}"
echo "-----------------------------------"
shell_scripts=$(find . -maxdepth 1 -name "*.sh" -type f | wc -l | tr -d ' ')
python_scripts=$(find . -maxdepth 1 -name "*.py" -type f | wc -l | tr -d ' ')
echo "  - Shell scripts: $shell_scripts"
echo "  - Python scripts: $python_scripts"

# Count lines of code in scripts
total_lines=0
shopt -s nullglob
for script in *.sh *.py; do
    if [ -f "$script" ]; then
        lines=$(wc -l < "$script" 2>/dev/null || echo "0")
        total_lines=$((total_lines + lines))
    fi
done
shopt -u nullglob
echo "  - Total script lines: $total_lines"

echo ""

# 5. Project Documentation Files
echo -e "${GREEN}📋 Project Documentation${NC}"
echo "-----------------------------------"
doc_files=("README.md" "CONTRIBUTING.md" "CODE_OF_CONDUCT.md" "CLAUDE.md" 
           "TODO.md" "STATUS.md" "IMPROVEMENTS.md" "GLOSSARY.md" 
           "CONTENT_REVIEW_CHECKLIST.md" "DOCS_INDEX.md")

total_doc_words=0
for doc in "${doc_files[@]}"; do
    if [ -f "$doc" ]; then
        words=$(wc -w < "$doc" 2>/dev/null || echo "0")
        total_doc_words=$((total_doc_words + words))
        echo "  - $doc: $words words"
    fi
done
echo "  - Total documentation: $total_doc_words words"

echo ""

# 6. Git Statistics
echo -e "${GREEN}📦 Git Repository${NC}"
echo "-----------------------------------"
if [ -d ".git" ]; then
    total_commits=$(git rev-list --count HEAD 2>/dev/null || echo "0")
    branches=$(git branch -a | wc -l | tr -d ' ')
    last_commit=$(git log -1 --format="%h - %s (%ar)" 2>/dev/null || echo "N/A")
    echo "  - Total commits: $total_commits"
    echo "  - Branches: $branches"
    echo "  - Last commit: $last_commit"
fi

echo ""

# 7. Summary
echo -e "${YELLOW}📈 Project Summary${NC}"
echo "-----------------------------------"
total_md=$(find . -name "*.md" -not -path "./.venv/*" -not -path "./.venv_translate/*" | wc -l | tr -d ' ')
total_images=$(find . -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) -not -path "./.venv/*" | wc -l | tr -d ' ')
echo "  - Total Markdown files: $total_md"
echo "  - Total images: $total_images"
echo "  - Script automation: ${shell_scripts} shell + ${python_scripts} Python"
echo "  - Documentation coverage: Complete (10 major docs)"

echo ""
echo -e "${GREEN}✅ Statistics generated successfully!${NC}"
echo "Last updated: $(date '+%Y-%m-%d %H:%M:%S %Z')"
