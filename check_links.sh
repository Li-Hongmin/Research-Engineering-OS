#!/bin/bash
# REOS Link Checker - 检查项目中所有 Markdown 文件的链接有效性
# Created: 2026-02-06 13:05 JST
# Purpose: 自动化优先 + 追溯闭环
# Usage: ./check_links.sh [--fast]  (--fast: skip external URL checks)

set -e

# Parse arguments
FAST_MODE=false
if [[ "$1" == "--fast" ]]; then
    FAST_MODE=true
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== REOS Link Checker ===${NC}"
if [[ "$FAST_MODE" == true ]]; then
    echo -e "${YELLOW}Mode: FAST (internal links only)${NC}"
fi
echo "Started: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

# Counters
total_files=0
total_links=0
broken_links=0
checked_urls=()

# Function to check if URL was already checked
is_url_checked() {
    local url="$1"
    for checked in "${checked_urls[@]}"; do
        if [[ "$checked" == "$url" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to check external URL
check_external_url() {
    local url="$1"
    local file="$2"
    
    # Skip in fast mode
    if [[ "$FAST_MODE" == true ]]; then
        return 0
    fi
    
    # Skip already checked URLs
    if is_url_checked "$url"; then
        return 0
    fi
    
    # Check URL with timeout (reduced to 5s for faster checks)
    if curl -sL --head --fail --max-time 5 "$url" > /dev/null 2>&1; then
        checked_urls+=("$url")
        return 0
    else
        echo -e "${RED}✗ Broken external link in $file:${NC}"
        echo -e "  URL: $url"
        checked_urls+=("$url")
        return 1
    fi
}

# Function to check internal link
check_internal_link() {
    local link="$1"
    local file="$2"
    local dir=$(dirname "$file")
    
    # Remove anchor if present
    local target="${link%%#*}"
    
    # Resolve relative path using cd (handles .. correctly)
    local full_path
    if full_path=$(cd "$dir" 2>/dev/null && cd "$(dirname "$target")" 2>/dev/null && pwd)/$(basename "$target"); then
        if [[ -f "$full_path" ]]; then
            return 0
        fi
    fi
    
    echo -e "${RED}✗ Broken internal link in $file:${NC}"
    echo -e "  Link: $link"
    echo -e "  Resolved path: $full_path"
    return 1
}

echo -e "${YELLOW}📚 Scanning for Markdown files...${NC}"

# Find all markdown files
md_files=$(find . -name "*.md" -not -path "*/\.*" -not -path "*/target/*" -not -path "*/node_modules/*")

for file in $md_files; do
    ((total_files++))
    
    # Extract all links from the file using grep + sed
    # Matches [text](url) format
    while IFS= read -r line; do
        # Extract URLs from markdown links
        extracted_links=$(echo "$line" | grep -oE '\]\([^)]+\)' | sed 's/][(]//' | sed 's/)//' || true)
        
        for link in $extracted_links; do
            [[ -z "$link" ]] && continue
            ((total_links++))
            
            # Check if it's an external URL
            if [[ "$link" =~ ^https?:// ]]; then
                if ! check_external_url "$link" "$file"; then
                    ((broken_links++))
                fi
            # Check if it's an internal link (relative path)
            elif [[ "$link" =~ ^[./] ]] || [[ ! "$link" =~ ^[a-zA-Z]+: ]]; then
                # Skip anchors-only links
                if [[ "$link" =~ ^# ]]; then
                    continue
                fi
                if ! check_internal_link "$link" "$file"; then
                    ((broken_links++))
                fi
            fi
        done
    done < <(grep -E '\[.*\]\(.*\)' "$file" || true)
done

echo ""
echo -e "${BLUE}=== Summary ===${NC}"
echo -e "Files scanned:     ${total_files}"
echo -e "Links found:       ${total_links}"
echo -e "Unique URLs checked: ${#checked_urls[@]}"
echo -e "Broken links:      ${broken_links}"
echo ""

if [[ $broken_links -eq 0 ]]; then
    echo -e "${GREEN}✓ All links are valid!${NC}"
    exit 0
else
    echo -e "${RED}✗ Found ${broken_links} broken link(s)${NC}"
    echo -e "${YELLOW}Tip: Review and fix broken links before deployment${NC}"
    exit 1
fi
