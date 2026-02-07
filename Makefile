# REOS Project Makefile
# Purpose: Unified entry point for common development tasks
# Created: 2026-02-07 07:05 JST

.PHONY: help health lint check-links check-translation check-manga check-consistency check-all test build clean commit

# Default target
help:
	@echo "REOS Project - Available Commands"
	@echo "=================================="
	@echo ""
	@echo "Quality Checks:"
	@echo "  make health              - Run comprehensive project health check"
	@echo "  make lint                - Run Markdown lint check"
	@echo "  make check-links         - Check link validity (fast mode)"
	@echo "  make check-links-full    - Check link validity (full mode)"
	@echo "  make check-translation   - Check translation synchronization"
	@echo "  make check-manga         - Check manga image assets"
	@echo "  make check-consistency   - Check three-language content consistency"
	@echo "  make check-all           - Run all quality checks"
	@echo "  make test                - Alias for check-all (quick shorthand)"
	@echo ""
	@echo "Building:"
	@echo "  make build               - Build all versions (text-book + manga-book)"
	@echo "  make build-text          - Build text-book (all languages)"
	@echo "  make build-manga         - Build manga-book"
	@echo ""
	@echo "Cleaning:"
	@echo "  make clean               - Clean build artifacts"
	@echo ""
	@echo "Development:"
	@echo "  make serve-text          - Serve text-book locally (port 8000)"
	@echo "  make serve-manga         - Serve manga-book locally (port 8001)"
	@echo ""
	@echo "Statistics:"
	@echo "  make stats               - Show comprehensive project statistics"
	@echo ""
	@echo "Git:"
	@echo "  make status              - Show git status"
	@echo "  make sync                - Pull latest changes from remote"
	@echo "  make commit              - Interactive commit helper (checks + status + commit)"
	@echo ""

# Quality Checks
health:
	@echo "🏥 Running comprehensive health check..."
	@./check_health.sh

lint:
	@echo "📝 Running Markdown lint check..."
	@./check_markdown_lint.sh

check-links:
	@echo "🔗 Checking link validity (fast mode)..."
	@./check_links.sh --fast

check-links-full:
	@echo "🔗 Checking link validity (full mode)..."
	@./check_links.sh

check-translation:
	@echo "🌍 Checking translation synchronization..."
	@./check_translation_sync.sh

check-manga:
	@echo "🖼️ Checking manga image assets..."
	@./check_manga_images.sh

check-consistency:
	@echo "📊 Checking three-language content consistency..."
	@./check_content_consistency.sh

check-all: health lint check-links check-translation check-manga check-consistency
	@echo ""
	@echo "✅ All quality checks completed!"

# Building
build: build-text build-manga
	@echo ""
	@echo "✅ All builds completed!"

build-text:
	@echo "📚 Building text-book (all languages)..."
	@cd text-book && ./build_all.sh

build-manga:
	@echo "📖 Building manga-book..."
	@cd manga-book && mdbook build

# Cleaning
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf text-book/book
	@rm -rf manga-book/book
	@echo "✅ Clean completed!"

# Development
serve-text:
	@echo "🌐 Serving text-book at http://localhost:8000"
	@cd text-book/book && python3 -m http.server 8000

serve-manga:
	@echo "🌐 Serving manga-book at http://localhost:8001"
	@cd manga-book/book && python3 -m http.server 8001

# Statistics
stats:
	@./project_stats.sh

# Git
status:
	@git status

sync:
	@echo "🔄 Pulling latest changes from remote..."
	@git pull
	@echo "✅ Sync completed!"

commit:
	@echo "🚀 REOS Interactive Commit Helper"
	@echo "=================================="
	@echo ""
	@echo "Step 1: Running quality checks..."
	@./check_health.sh || { echo "❌ Health check failed! Fix issues before committing."; exit 1; }
	@echo ""
	@echo "Step 2: Git status"
	@git status
	@echo ""
	@echo "Step 3: Ready to commit!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Review changes above"
	@echo "  2. Stage files: git add <files>"
	@echo "  3. Commit: git commit -m \"your message\""
	@echo "  4. Push: git push"
	@echo ""
	@echo "💡 Tip: Pre-commit hook will run health check automatically"

# Testing (alias for check-all)
test: check-all
	@echo ""
	@echo "✅ All tests passed!"
