#!/bin/bash
# REOS Markdown Lint Check Script
# Purpose: Detect common Markdown formatting issues in text-book and manga-book
# Usage: ./check_markdown_lint.sh [--verbose]

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

VERBOSE=false
if [[ "${1:-}" == "--verbose" ]]; then
    VERBOSE=true
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    if $VERBOSE; then
        echo -e "${GREEN}✓${NC} $1"
    fi
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# ============================================
# Check for unclosed HTML tags in Markdown
# ============================================
echo "🔍 Checking for unclosed HTML tags..."

UNCLOSED_TAGS=0
CHECKED_FILES=0

# Common HTML tags that should be avoided or properly closed in Markdown
DANGEROUS_TAGS=("file" "hash" "id" "path" "name" "type" "value" "key" "data" "input" "output")

# Find all Markdown files in text-book and manga-book
while IFS= read -r file; do
    CHECKED_FILES=$((CHECKED_FILES + 1))
    
    for tag in "${DANGEROUS_TAGS[@]}"; do
        # Look for unescaped <tag> patterns (not in code blocks)
        # This is a simplified check - could be enhanced with more sophisticated parsing
        if grep -n "<${tag}>" "$file" 2>/dev/null | grep -v '```' | grep -v '`<' > /dev/null; then
            MATCHES=$(grep -n "<${tag}>" "$file" | grep -v '```' | grep -v '`<')
            while IFS= read -r match; do
                log_error "Unclosed/unescaped <${tag}> in: $file:${match%%:*}"
                if $VERBOSE; then
                    echo "    ${match#*:}"
                fi
                UNCLOSED_TAGS=$((UNCLOSED_TAGS + 1))
            done <<< "$MATCHES"
        fi
    done
done < <(find text-book manga-book -type f -name "*.md" 2>/dev/null)

if [ $UNCLOSED_TAGS -eq 0 ]; then
    log_info "No unclosed HTML tags found (checked $CHECKED_FILES files)"
else
    log_error "Found $UNCLOSED_TAGS unclosed/unescaped HTML tags in $CHECKED_FILES files"
fi

# ============================================
# Check for trailing whitespace
# ============================================
echo ""
echo "🔍 Checking for trailing whitespace..."

TRAILING_WS=0

while IFS= read -r file; do
    if grep -n '[[:space:]]$' "$file" > /dev/null 2>&1; then
        LINE_COUNT=$(grep -n '[[:space:]]$' "$file" | wc -l | tr -d ' ')
        log_warn "Trailing whitespace in: $file ($LINE_COUNT lines)"
        if $VERBOSE; then
            grep -n '[[:space:]]$' "$file" | head -5 | while IFS=: read -r line rest; do
                echo "    Line $line: ${rest:0:60}..."
            done
            if [ "$LINE_COUNT" -gt 5 ]; then
                echo "    ... and $((LINE_COUNT - 5)) more lines"
            fi
        fi
        TRAILING_WS=$((TRAILING_WS + 1))
    fi
done < <(find text-book manga-book -type f -name "*.md" 2>/dev/null)

if [ $TRAILING_WS -eq 0 ]; then
    log_info "No trailing whitespace found"
else
    log_warn "Found trailing whitespace in $TRAILING_WS files"
fi

# ============================================
# Check for multiple consecutive blank lines
# ============================================
echo ""
echo "🔍 Checking for excessive blank lines..."

EXCESSIVE_BLANKS=0

while IFS= read -r file; do
    # Check for 3+ consecutive blank lines
    if grep -Pzo '(\n\s*){3,}' "$file" > /dev/null 2>&1; then
        log_warn "Excessive blank lines in: $file"
        EXCESSIVE_BLANKS=$((EXCESSIVE_BLANKS + 1))
    fi
done < <(find text-book manga-book -type f -name "*.md" 2>/dev/null)

if [ $EXCESSIVE_BLANKS -eq 0 ]; then
    log_info "No excessive blank lines found"
else
    log_warn "Found excessive blank lines in $EXCESSIVE_BLANKS files"
fi

# ============================================
# Check for missing alt text in images
# ============================================
echo ""
echo "🔍 Checking for images without alt text..."

MISSING_ALT=0

while IFS= read -r file; do
    # Match ![](path) pattern (empty alt text)
    if grep -n '!\[\](' "$file" > /dev/null 2>&1; then
        MATCHES=$(grep -n '!\[\](' "$file")
        while IFS= read -r match; do
            log_warn "Image without alt text in: $file:${match%%:*}"
            if $VERBOSE; then
                echo "    ${match#*:}"
            fi
            MISSING_ALT=$((MISSING_ALT + 1))
        done <<< "$MATCHES"
    fi
done < <(find text-book manga-book -type f -name "*.md" 2>/dev/null)

if [ $MISSING_ALT -eq 0 ]; then
    log_info "All images have alt text"
else
    log_warn "Found $MISSING_ALT images without alt text"
fi

# ============================================
# Summary
# ============================================
echo ""
echo "════════════════════════════════════════"
echo "📊 Markdown Lint Summary"
echo "════════════════════════════════════════"
echo "Files checked: $CHECKED_FILES"
echo "Unclosed HTML tags: $UNCLOSED_TAGS"
echo "Files with trailing whitespace: $TRAILING_WS"
echo "Files with excessive blanks: $EXCESSIVE_BLANKS"
echo "Images without alt text: $MISSING_ALT"
echo ""

# Exit with error if critical issues found
if [ $UNCLOSED_TAGS -gt 0 ]; then
    echo -e "${RED}✗ FAILED${NC} - Found critical Markdown issues"
    exit 1
else
    echo -e "${GREEN}✓ SUCCESS${NC} - No critical issues found"
    if [ $TRAILING_WS -gt 0 ] || [ $EXCESSIVE_BLANKS -gt 0 ] || [ $MISSING_ALT -gt 0 ]; then
        echo -e "${YELLOW}⚠${NC} Warning: Found minor style issues (non-blocking)"
    fi
    exit 0
fi
