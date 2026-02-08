#!/usr/bin/env bash
# check_architecture.sh - 验证实际目录结构与 ARCHITECTURE.md 的一致性
# Created: 2026-02-08 22:05 JST
# Purpose: 确保架构文档准确反映项目实际结构

set -euo pipefail

echo "🏗️ Checking project structure against ARCHITECTURE.md..."
echo ""

# 定义预期的关键目录和文件
declare -a EXPECTED_DIRS=(
    "text-book/src"
    "text-book/src_en"
    "text-book/src_ja"
    "manga-book/src"
    "manga-book/src_en"
    "manga-book/src_ja"
    "manga-book/images"
    "shared"
    "archive"
    ".github/workflows"
)

declare -a EXPECTED_FILES=(
    "text-book/book.toml"
    "text-book/build_all.sh"
    "manga-book/book.toml"
    "check_health.sh"
    "check_links.sh"
    "check_translation_sync.sh"
    "check_manga_images.sh"
    "check_content_consistency.sh"
    "check_markdown_lint.sh"
    "project_stats.sh"
    "README.md"
    "QUICKSTART.md"
    "CONTRIBUTING.md"
    "CODE_OF_CONDUCT.md"
    "TODO.md"
    "STATUS.md"
    "CHANGELOG.md"
    "IMPROVEMENTS.md"
    "GLOSSARY.md"
    "DOCS_INDEX.md"
    "LICENSE_GUIDE.md"
    "CONTENT_REVIEW_CHECKLIST.md"
    "CLAUDE.md"
    "ARCHITECTURE.md"
    ".editorconfig"
    ".gitattributes"
    ".gitignore"
    "Makefile"
)

MISSING_DIRS=()
MISSING_FILES=()

# 检查目录
echo "📂 Checking directories..."
for dir in "${EXPECTED_DIRS[@]}"; do
    if [[ -d "$dir" ]]; then
        echo "  ✓ $dir"
    else
        echo "  ✗ $dir (MISSING)"
        MISSING_DIRS+=("$dir")
    fi
done
echo ""

# 检查文件
echo "📄 Checking files..."
for file in "${EXPECTED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MISSING)"
        MISSING_FILES+=("$file")
    fi
done
echo ""

# 总结
echo "========================================="
if [[ ${#MISSING_DIRS[@]} -eq 0 && ${#MISSING_FILES[@]} -eq 0 ]]; then
    echo "✅ Project structure matches ARCHITECTURE.md"
    echo "   All expected directories and files are present."
    exit 0
else
    echo "⚠️ Structure validation warnings:"
    if [[ ${#MISSING_DIRS[@]} -gt 0 ]]; then
        echo "   Missing directories: ${#MISSING_DIRS[@]}"
        for dir in "${MISSING_DIRS[@]}"; do
            echo "     - $dir"
        done
    fi
    if [[ ${#MISSING_FILES[@]} -gt 0 ]]; then
        echo "   Missing files: ${#MISSING_FILES[@]}"
        for file in "${MISSING_FILES[@]}"; do
            echo "     - $file"
        done
    fi
    echo ""
    echo "Consider updating ARCHITECTURE.md if these changes are intentional."
    exit 1
fi
