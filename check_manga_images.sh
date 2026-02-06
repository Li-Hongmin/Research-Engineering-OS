#!/bin/bash
# REOS Manga Image Link Checker - 快速检查 manga-book 图片链接
# Created: 2026-02-06 13:10 JST
# Purpose: 专门检查漫画图片引用的有效性

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== REOS Manga Image Link Checker ===${NC}"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

cd manga-book

total_files=0
total_image_links=0
broken_image_links=0
broken_files=()

echo -e "${YELLOW}Scanning manga markdown files...${NC}"

for lang_dir in src src_en src_ja; do
    if [[ ! -d "$lang_dir" ]]; then
        continue
    fi
    
    echo -e "${BLUE}Checking $lang_dir...${NC}"
    
    for file in $(find "$lang_dir" -name "*.md" -type f); do
        ((total_files++))
        
        # Extract image links (../images/...)
        image_links=$(grep -oE '!\[.*\]\([^)]+\)' "$file" | sed -E 's/!\[.*\]\(([^)]+)\)/\1/' || true)
        
        for link in $image_links; do
            [[ -z "$link" ]] && continue
            ((total_image_links++))
            
            # Check if image file exists
            dir=$(dirname "$file")
            full_path="$dir/$link"
            
            if [[ ! -f "$full_path" ]]; then
                echo -e "${RED}✗ Missing image:${NC}"
                echo -e "  File: $file"
                echo -e "  Link: $link"
                echo -e "  Expected: $full_path"
                echo ""
                ((broken_image_links++))
                broken_files+=("$file")
            fi
        done
    done
done

# Get unique broken files
unique_broken=$(printf '%s\n' "${broken_files[@]}" | sort -u | wc -l | tr -d ' ')

echo -e "${BLUE}=== Summary ===${NC}"
echo -e "Files scanned:       ${total_files}"
echo -e "Image links found:   ${total_image_links}"
echo -e "Broken image links:  ${broken_image_links}"
echo -e "Files with issues:   ${unique_broken}"
echo ""

if [[ $broken_image_links -eq 0 ]]; then
    echo -e "${GREEN}✓ All manga image links are valid!${NC}"
    exit 0
else
    echo -e "${RED}✗ Found ${broken_image_links} broken image link(s) in ${unique_broken} file(s)${NC}"
    echo -e "${YELLOW}Tip: Check if image paths match the actual directory structure${NC}"
    echo -e "${YELLOW}     Image directories: $(ls images/ | tr '\n' ' ')${NC}"
    exit 1
fi
