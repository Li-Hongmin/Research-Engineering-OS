#!/bin/bash
# REOS Project Health Check Script
# Purpose: Automated health monitoring for Research-Engineering-OS project
# Usage: ./check_health.sh [--verbose]

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
# 1. Git Status Check
# ============================================
echo "🔍 Checking Git Status..."
if git diff-index --quiet HEAD --; then
    log_info "Working tree is clean"
    GIT_CLEAN=true
else
    log_warn "Working tree has uncommitted changes"
    GIT_CLEAN=false
fi

# Check if local is behind remote
git fetch origin main &>/dev/null
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" = "$REMOTE" ]; then
    log_info "Local branch is up to date with origin/main"
    GIT_SYNCED=true
elif [ "$LOCAL" = "$(git merge-base @ @{u})" ]; then
    log_warn "Local branch is behind origin/main"
    GIT_SYNCED=false
else
    log_warn "Local and remote have diverged"
    GIT_SYNCED=false
fi

# ============================================
# 2. Build Check (text-book)
# ============================================
echo "📚 Checking text-book builds..."
BUILD_STATUS=true

for lang in zh en ja; do
    BUILD_DIR="text-book/book/$lang"
    if [ -d "$BUILD_DIR" ] && [ -f "$BUILD_DIR/index.html" ]; then
        log_info "text-book/$lang: Build exists"
    else
        log_warn "text-book/$lang: Build missing or incomplete"
        BUILD_STATUS=false
    fi
done

# ============================================
# 3. Manga Book Check
# ============================================
echo "📖 Checking manga-book build..."
MANGA_BUILD_DIR="manga-book/book"
if [ -d "$MANGA_BUILD_DIR" ] && [ -f "$MANGA_BUILD_DIR/index.html" ]; then
    log_info "manga-book: Build exists"
    MANGA_BUILD=true
else
    log_warn "manga-book: Build missing"
    MANGA_BUILD=false
fi

# ============================================
# 4. Image Asset Check
# ============================================
echo "🖼️ Checking manga image assets..."
MANGA_IMAGES="manga-book/images"
if [ -d "$MANGA_IMAGES" ]; then
    IMAGE_COUNT=$(find "$MANGA_IMAGES" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.webp" \) | wc -l)
    log_info "Found $IMAGE_COUNT manga images"
    IMAGES_OK=true
else
    log_warn "Manga images directory not found"
    IMAGES_OK=false
fi

# ============================================
# 5. Documentation Check
# ============================================
echo "📝 Checking core documentation..."
REQUIRED_DOCS=("README.md" "STATUS.md" "CLAUDE.md" "text-book/book.toml" "manga-book/book.toml")
DOCS_OK=true

for doc in "${REQUIRED_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        log_info "$doc exists"
    else
        log_error "$doc is missing"
        DOCS_OK=false
    fi
done

# ============================================
# 6. Dependency Check
# ============================================
echo "🔧 Checking dependencies..."
DEPS_OK=true

if command -v mdbook &> /dev/null; then
    MDBOOK_VERSION=$(mdbook --version | head -n1)
    log_info "mdbook installed: $MDBOOK_VERSION"
else
    log_error "mdbook is not installed"
    DEPS_OK=false
fi

# ============================================
# Summary Report
# ============================================
echo ""
echo "========================================="
echo "📊 REOS Project Health Report"
echo "========================================="
echo "🕐 Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

print_status() {
    if $1; then
        echo -e "  ${GREEN}✓${NC} $2"
    else
        echo -e "  ${RED}✗${NC} $2"
    fi
}

print_status $GIT_CLEAN "Git working tree clean"
print_status $GIT_SYNCED "Git synchronized with remote"
print_status $BUILD_STATUS "text-book builds complete"
print_status $MANGA_BUILD "manga-book build exists"
print_status $IMAGES_OK "Manga image assets present"
print_status $DOCS_OK "Core documentation complete"
print_status $DEPS_OK "Dependencies installed"

echo ""

# Overall status
if $GIT_CLEAN && $GIT_SYNCED && $BUILD_STATUS && $MANGA_BUILD && $IMAGES_OK && $DOCS_OK && $DEPS_OK; then
    echo -e "${GREEN}✅ Project health: EXCELLENT${NC}"
    exit 0
elif $DOCS_OK && $DEPS_OK; then
    echo -e "${YELLOW}⚠️ Project health: GOOD (minor issues)${NC}"
    exit 0
else
    echo -e "${RED}❌ Project health: NEEDS ATTENTION${NC}"
    exit 1
fi
