#!/usr/bin/env bash
# REOS Translation Sync Checker
# Purpose: Check chapter completeness across text-book three language versions
# Created: 2026-02-06 08:23 JST

set -euo pipefail

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Working directories
TEXT_BOOK_DIR="text-book"
SRC_ZH="${TEXT_BOOK_DIR}/src"
SRC_EN="${TEXT_BOOK_DIR}/src_en"
SRC_JA="${TEXT_BOOK_DIR}/src_ja"

echo "=========================================="
echo "REOS Translation Sync Check"
echo "=========================================="
echo "Time: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

# Check if directory exists
if [ ! -d "$TEXT_BOOK_DIR" ]; then
    echo -e "${RED}ERROR: text-book directory not found${NC}"
    exit 1
fi

# Function: Get markdown file list (exclude SUMMARY.md)
get_md_files() {
    local dir=$1
    find "$dir" -name "*.md" -not -name "SUMMARY.md" 2>/dev/null | sed "s|$dir/||" | sort || echo ""
}

# Function: Get chapters from SUMMARY.md
get_summary_chapters() {
    local summary_file=$1
    if [ -f "$summary_file" ]; then
        grep -oE '\[.*\]\(.*\.md\)' "$summary_file" 2>/dev/null | sed 's/.*(\(.*\))/\1/' | sort || echo ""
    else
        echo ""
    fi
}

echo "Scanning files..."
echo ""

# Get file lists for each language
ZH_FILES=$(get_md_files "$SRC_ZH")
EN_FILES=$(get_md_files "$SRC_EN")
JA_FILES=$(get_md_files "$SRC_JA")

# Get chapters from SUMMARY.md
ZH_SUMMARY=$(get_summary_chapters "$SRC_ZH/SUMMARY.md")
EN_SUMMARY=$(get_summary_chapters "$SRC_EN/SUMMARY.md")
JA_SUMMARY=$(get_summary_chapters "$SRC_JA/SUMMARY.md")

# Count files
ZH_COUNT=$(echo "$ZH_FILES" | grep -c "^" || echo 0)
EN_COUNT=$(echo "$EN_FILES" | grep -c "^" || echo 0)
JA_COUNT=$(echo "$JA_FILES" | grep -c "^" || echo 0)

echo "File Statistics:"
echo -e "  Chinese: ${GREEN}${ZH_COUNT}${NC} files"
echo -e "  English: ${GREEN}${EN_COUNT}${NC} files"
echo -e "  Japanese: ${GREEN}${JA_COUNT}${NC} files"
echo ""

# Compare translations function
compare_translations() {
    local base_lang_name="$1"
    local base_list="$2"
    local target_lang_name="$3"
    local target_list="$4"
    
    local missing_count=0
    local missing_items=""
    
    if [ -z "$base_list" ]; then
        echo -e "${GREEN}OK ${target_lang_name} is complete (base is empty)${NC}"
        return 0
    fi
    
    while IFS= read -r item; do
        if [ -n "$item" ]; then
            if ! echo "$target_list" | grep -qF "$item"; then
                missing_count=$((missing_count + 1))
                missing_items="${missing_items}  - ${item}\n"
            fi
        fi
    done <<< "$base_list"
    
    if [ $missing_count -gt 0 ]; then
        echo -e "${YELLOW}WARNING: ${target_lang_name} missing ${missing_count} files (vs ${base_lang_name})${NC}"
        echo -e "${missing_items}"
        return 1
    else
        echo -e "${GREEN}OK ${target_lang_name} is complete (vs ${base_lang_name})${NC}"
        return 0
    fi
}

echo "Translation Comparison:"
echo ""

# Use Chinese as baseline
echo "[Chinese -> English]"
compare_translations "Chinese" "$ZH_FILES" "English" "$EN_FILES"
EN_STATUS=$?
echo ""

echo "[Chinese -> Japanese]"
compare_translations "Chinese" "$ZH_FILES" "Japanese" "$JA_FILES"
JA_STATUS=$?
echo ""

# Check SUMMARY.md consistency
echo "SUMMARY.md Check:"
echo ""

check_summary_consistency() {
    local lang_name="$1"
    local summary_list="$2"
    local file_list="$3"
    
    local orphaned_count=0
    local orphaned_items=""
    
    if [ -z "$file_list" ]; then
        echo -e "${GREEN}OK ${lang_name} SUMMARY.md is complete (no files)${NC}"
        return 0
    fi
    
    while IFS= read -r item; do
        if [ -n "$item" ]; then
            if ! echo "$summary_list" | grep -qF "$item"; then
                orphaned_count=$((orphaned_count + 1))
                orphaned_items="${orphaned_items}  - ${item}\n"
            fi
        fi
    done <<< "$file_list"
    
    if [ $orphaned_count -gt 0 ]; then
        echo -e "${YELLOW}WARNING: ${lang_name} SUMMARY.md missing ${orphaned_count} file references${NC}"
        echo -e "${orphaned_items}"
        return 1
    else
        echo -e "${GREEN}OK ${lang_name} SUMMARY.md is complete${NC}"
        return 0
    fi
}

check_summary_consistency "Chinese" "$ZH_SUMMARY" "$ZH_FILES"
ZH_SUMMARY_STATUS=$?
echo ""

check_summary_consistency "English" "$EN_SUMMARY" "$EN_FILES"
EN_SUMMARY_STATUS=$?
echo ""

check_summary_consistency "Japanese" "$JA_SUMMARY" "$JA_FILES"
JA_SUMMARY_STATUS=$?
echo ""

# Summary
echo "=========================================="
echo "Summary"
echo "=========================================="

TOTAL_ISSUES=$((EN_STATUS + JA_STATUS + ZH_SUMMARY_STATUS + EN_SUMMARY_STATUS + JA_SUMMARY_STATUS))

if [ $TOTAL_ISSUES -eq 0 ]; then
    echo -e "${GREEN}SUCCESS: All translation versions are synced!${NC}"
    exit 0
else
    echo -e "${YELLOW}WARNING: Found ${TOTAL_ISSUES} sync issues${NC}"
    echo ""
    echo "Suggested Actions:"
    if [ $EN_STATUS -ne 0 ]; then
        echo "  1. Translate missing English chapters"
    fi
    if [ $JA_STATUS -ne 0 ]; then
        echo "  2. Translate missing Japanese chapters"
    fi
    if [ $ZH_SUMMARY_STATUS -ne 0 ] || [ $EN_SUMMARY_STATUS -ne 0 ] || [ $JA_SUMMARY_STATUS -ne 0 ]; then
        echo "  3. Update SUMMARY.md to include all files"
    fi
    exit 1
fi
