#!/bin/bash

# check_content_consistency.sh
# Purpose: 检查 text-book 和 manga-book 三语言版本的内容一致性
# Created: 2026-02-07 04:05 JST (REOS hourly push)

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}REOS Content Consistency Check${NC}"
echo -e "${BLUE}========================================${NC}"
echo

ERRORS=0
WARNINGS=0

# Function: check directory structure consistency
check_structure() {
    local book_type=$1
    local book_dir=$2
    
    echo -e "${BLUE}[CHECK] ${book_type} 目录结构一致性${NC}"
    
    if [[ ! -d "$book_dir" ]]; then
        echo -e "${RED}  ✗ 目录不存在: $book_dir${NC}"
        ((ERRORS++))
        return
    fi
    
    pushd "$book_dir" > /dev/null
    
    # Get file lists (excluding SUMMARY.md, README.md)
    local zh_files=$(find src -name "*.md" ! -name "SUMMARY.md" ! -name "README.md" | sort)
    local en_files=$(find src_en -name "*.md" ! -name "SUMMARY.md" ! -name "README.md" 2>/dev/null | sort || echo "")
    local ja_files=$(find src_ja -name "*.md" ! -name "SUMMARY.md" ! -name "README.md" 2>/dev/null | sort || echo "")
    
    # Count files
    local zh_count=$(echo "$zh_files" | wc -l | xargs)
    local en_count=$(echo "$en_files" | wc -l | xargs)
    local ja_count=$(echo "$ja_files" | wc -l | xargs)
    
    echo -e "  ${YELLOW}文件数量: 中文=$zh_count | 英文=$en_count | 日文=$ja_count${NC}"
    
    # Check if counts match
    if [[ "$zh_count" == "$en_count" && "$en_count" == "$ja_count" ]]; then
        echo -e "  ${GREEN}✓ 文件数量一致${NC}"
    else
        echo -e "  ${YELLOW}⚠ 文件数量不一致${NC}"
        ((WARNINGS++))
    fi
    
    # Check for missing translations
    local zh_basenames=$(echo "$zh_files" | sed 's|^src/||')
    local en_basenames=$(echo "$en_files" | sed 's|^src_en/||')
    local ja_basenames=$(echo "$ja_files" | sed 's|^src_ja/||')
    
    # Files in zh but not in en
    local missing_en=$(comm -23 <(echo "$zh_basenames") <(echo "$en_basenames"))
    if [[ -n "$missing_en" ]]; then
        echo -e "  ${YELLOW}⚠ 英文版缺失文件:${NC}"
        echo "$missing_en" | sed 's/^/    - /'
        ((WARNINGS++))
    fi
    
    # Files in zh but not in ja
    local missing_ja=$(comm -23 <(echo "$zh_basenames") <(echo "$ja_basenames"))
    if [[ -n "$missing_ja" ]]; then
        echo -e "  ${YELLOW}⚠ 日文版缺失文件:${NC}"
        echo "$missing_ja" | sed 's/^/    - /'
        ((WARNINGS++))
    fi
    
    popd > /dev/null
    echo
}

# Function: check SUMMARY.md consistency
check_summary() {
    local book_type=$1
    local book_dir=$2
    
    echo -e "${BLUE}[CHECK] ${book_type} SUMMARY.md 一致性${NC}"
    
    pushd "$book_dir" > /dev/null
    
    local zh_summary="src/SUMMARY.md"
    local en_summary="src_en/SUMMARY.md"
    local ja_summary="src_ja/SUMMARY.md"
    
    # Count chapter entries (lines with .md links)
    local zh_chapters=$(grep -c "\.md)" "$zh_summary" 2>/dev/null || echo 0)
    local en_chapters=$(grep -c "\.md)" "$en_summary" 2>/dev/null || echo 0)
    local ja_chapters=$(grep -c "\.md)" "$ja_summary" 2>/dev/null || echo 0)
    
    echo -e "  ${YELLOW}章节数量: 中文=$zh_chapters | 英文=$en_chapters | 日文=$ja_chapters${NC}"
    
    if [[ "$zh_chapters" == "$en_chapters" && "$en_chapters" == "$ja_chapters" ]]; then
        echo -e "  ${GREEN}✓ SUMMARY.md 章节数量一致${NC}"
    else
        echo -e "  ${YELLOW}⚠ SUMMARY.md 章节数量不一致${NC}"
        ((WARNINGS++))
    fi
    
    popd > /dev/null
    echo
}

# Function: check code block consistency
check_code_blocks() {
    local book_type=$1
    local book_dir=$2
    
    echo -e "${BLUE}[CHECK] ${book_type} 代码块一致性${NC}"
    
    pushd "$book_dir" > /dev/null
    
    # Count code blocks in all files
    local zh_code_blocks=$(find src -name "*.md" -exec grep -c '^```' {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
    local en_code_blocks=$(find src_en -name "*.md" -exec grep -c '^```' {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
    local ja_code_blocks=$(find src_ja -name "*.md" -exec grep -c '^```' {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
    
    echo -e "  ${YELLOW}代码块数量: 中文=$zh_code_blocks | 英文=$en_code_blocks | 日文=$ja_code_blocks${NC}"
    
    # Calculate difference percentage
    local max_blocks=$zh_code_blocks
    [[ $en_code_blocks -gt $max_blocks ]] && max_blocks=$en_code_blocks
    [[ $ja_code_blocks -gt $max_blocks ]] && max_blocks=$ja_code_blocks
    
    if [[ $max_blocks -eq 0 ]]; then
        echo -e "  ${GREEN}✓ 无代码块（正常）${NC}"
    else
        local diff_en=$(( (max_blocks - en_code_blocks) * 100 / max_blocks ))
        local diff_ja=$(( (max_blocks - ja_code_blocks) * 100 / max_blocks ))
        
        if [[ $diff_en -le 10 && $diff_ja -le 10 ]]; then
            echo -e "  ${GREEN}✓ 代码块数量基本一致（差异 ≤10%）${NC}"
        else
            echo -e "  ${YELLOW}⚠ 代码块数量差异较大（>10%）${NC}"
            ((WARNINGS++))
        fi
    fi
    
    popd > /dev/null
    echo
}

# Function: check image references consistency
check_images() {
    local book_type=$1
    local book_dir=$2
    
    echo -e "${BLUE}[CHECK] ${book_type} 图片引用一致性${NC}"
    
    pushd "$book_dir" > /dev/null
    
    # Count image references
    local zh_images=$(find src -name "*.md" -exec grep -c '!\[' {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
    local en_images=$(find src_en -name "*.md" -exec grep -c '!\[' {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
    local ja_images=$(find src_ja -name "*.md" -exec grep -c '!\[' {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
    
    echo -e "  ${YELLOW}图片引用数量: 中文=$zh_images | 英文=$en_images | 日文=$ja_images${NC}"
    
    # Calculate difference percentage
    local max_images=$zh_images
    [[ $en_images -gt $max_images ]] && max_images=$en_images
    [[ $ja_images -gt $max_images ]] && max_images=$ja_images
    
    if [[ $max_images -eq 0 ]]; then
        echo -e "  ${GREEN}✓ 无图片引用（正常）${NC}"
    else
        local diff_en=$(( (max_images - en_images) * 100 / max_images ))
        local diff_ja=$(( (max_images - ja_images) * 100 / max_images ))
        
        if [[ $diff_en -le 5 && $diff_ja -le 5 ]]; then
            echo -e "  ${GREEN}✓ 图片引用数量基本一致（差异 ≤5%）${NC}"
        else
            echo -e "  ${YELLOW}⚠ 图片引用数量差异较大（>5%）${NC}"
            ((WARNINGS++))
        fi
    fi
    
    popd > /dev/null
    echo
}

# Main execution
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}1. text-book 检查${NC}"
echo -e "${BLUE}========================================${NC}"
echo

check_structure "text-book" "text-book"
check_summary "text-book" "text-book"
check_code_blocks "text-book" "text-book"
check_images "text-book" "text-book"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}2. manga-book 检查${NC}"
echo -e "${BLUE}========================================${NC}"
echo

check_structure "manga-book" "manga-book"
check_summary "manga-book" "manga-book"
check_code_blocks "manga-book" "manga-book"
check_images "manga-book" "manga-book"

# Final summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}检查总结${NC}"
echo -e "${BLUE}========================================${NC}"
echo

if [[ $ERRORS -eq 0 && $WARNINGS -eq 0 ]]; then
    echo -e "${GREEN}✓ EXCELLENT - 所有检查通过${NC}"
    echo -e "${GREEN}  三语言版本内容高度一致${NC}"
    exit 0
elif [[ $ERRORS -eq 0 && $WARNINGS -gt 0 ]]; then
    echo -e "${YELLOW}⚠ GOOD - $WARNINGS 个警告${NC}"
    echo -e "${YELLOW}  建议检查不一致的内容${NC}"
    exit 0
else
    echo -e "${RED}✗ FAILED - $ERRORS 个错误, $WARNINGS 个警告${NC}"
    echo -e "${RED}  请修复错误后重新运行${NC}"
    exit 1
fi
