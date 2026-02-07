# Changelog

All notable changes to the Research Engineering OS (REOS) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses date-based versioning (YYYY-MM-DD).

## [Unreleased]

## [2026-02-07] - Latest

### Added
- **Project Statistics Tool** (`project_stats.sh`)
  - 7 major statistics categories: documentation, manga, images, scripts, git repo
  - Colorful output for better readability
  - Integrated into Makefile as `make stats`
  - Reveals project scale: 65k+ words, 671 images, 921 files
- **Makefile** - Unified command entry point
  - 20+ commands organized into Quality Checks, Building, Cleaning, Development, Git
  - `make help` - Self-documenting command list
  - `make check-all` - Run all quality checks at once
  - `make build` - Build all versions (text-book + manga-book)
- **Content Consistency Checker** (`check_content_consistency.sh`)
  - Validates tri-lingual consistency (中/英/日)
  - Checks directory structure, chapter count, code blocks, image references
  - Percentage-based diff reporting
- **GitHub Issue Templates** (6 templates)
  - Bug Report, Content Improvement, Translation, Feature Request, Question
  - Bilingual support (Chinese/English)
  - Structured forms with dropdowns and validation
- **Code of Conduct** (`CODE_OF_CONDUCT.md`)
  - Based on Contributor Covenant 2.1
  - Adapted for REOS: multi-lingual, academic-industry fusion, education-friendly
  - Complete reporting process and enforcement guidelines
  - Bilingual summary (English full + Chinese summary)
- **Contributing Guide** (`CONTRIBUTING.md`)
  - 5 contribution pathways: content, translation, design, QA, community
  - Complete workflow: fork → build → test → PR
  - Style guide & conventions: Markdown, code, terminology, commit
  - Translation workflow with Azure batch translation
  - Quality assurance system (6 scripts + CI/CD)
- **Content Review Checklist** (`CONTENT_REVIEW_CHECKLIST.md`)
  - 8 major review areas: terminology, code quality, references, images, i18n, narrative, markdown, CI/CD
  - Integration with automation scripts
  - Issue/PR review templates
- **Documentation Index** (`DOCS_INDEX.md`)
  - Centralized navigation for all project documentation
  - Quick reference guide for common tasks
  - Organized by category: Learning, Development, Quality, Translation

### Changed
- **CONTRIBUTING.md** - Promoted Makefile usage
  - Added "Quick Start with Makefile" section
  - Recommended `make` commands as primary method
  - Kept direct script execution as fallback option
- **README.md** → v2.2
  - Added content consistency checker to automation tools list
  - Enhanced "Documentation & Guidelines" section
  - Added quick links to 4 core docs
- **Pre-commit Hook** - Now runs health check automatically
  - Prevents commits when critical issues detected
  - Ensures continuous quality assurance

### Fixed
- **Broken Links**
  - CODE_OF_CONDUCT.md: Fixed GitHub Discussions URL
  - manga-book/src_ja/: Fixed 265 image path references (../../images/ → ../images/)
  - Unified image paths across tri-lingual versions
- **Unclosed HTML Tags** (3 files)
  - src_en/07-ai-workflow.md: Fixed `<file>`, `<hash>` tags
  - src_ja/05-dod.md: Fixed `<id>` tag
  - Wrapped tags with backticks to escape rendering

### Maintenance
- **STATUS.md** - Archived 2026-02-06 records
  - Created `archive/STATUS-2026-02-06.md` (689 lines)
  - Reduced main file by 60% (1094 → 431 lines)
  - Established sustainable archival mechanism

---

## [2026-02-06]

### Added
- **Health Check Script** (`check_health.sh`)
  - Comprehensive project health validation
  - Git status, build verification, documentation completeness
  - Color-coded output (EXCELLENT/GOOD/NEEDS ATTENTION)
- **Markdown Lint Tool** (`check_markdown_lint.sh`)
  - Detects unclosed HTML tags (critical)
  - Checks trailing spaces, excessive blank lines, missing alt text (warnings)
  - Integrated into CI/CD workflow
- **Link Checker** (`check_links.sh`)
  - Fast mode (--fast) for quick checks
  - Full mode for comprehensive validation
  - Supports internal and external links
- **Manga Image Checker** (`check_manga_images.sh` + `.py`)
  - Validates image references in manga chapters
  - Detects missing images and broken paths
  - Python + shell dual implementation
- **Translation Sync Checker** (`check_translation_sync.sh`)
  - Compares chapter completeness across src/, src_en/, src_ja/
  - Validates SUMMARY.md consistency
  - Identifies missing translations
- **Pre-commit Hook** (`.git/hooks/pre-commit`)
  - Automatically runs health check before commit
  - Prevents commits with critical issues
  - 5-second timeout for fast commits

### Changed
- **CI/CD Workflow** - Enhanced with multiple quality checks
  - Health check, markdown lint, link validation
  - Runs on push to main and pull requests
  - Automated deployment to GitHub Pages
- **README.md** → v2.1
  - Added automation tools section (6 scripts)
  - Enhanced project description
  - Updated status and deployment info

### Fixed
- **manga-book Image Paths**
  - Fixed 45+ image references across chapters
  - Renamed `00-prologue` → `00-preface` (tri-lingual)
  - Verified with mdbook build

### Documentation
- **STATUS.md** - Hourly work tracking system
  - Record: task → execution → output → traceability
  - Small steps, quick wins (5-45 min cycles)
  - Full commit SHA and file path tracking
- **TODO.md** - Structured task tracking
  - Short-term (next session), Mid-term (1-2 days), Long-term (1 week)
  - Idea pool for unscheduled improvements
  - REOS principles checklist per task
- **GLOSSARY.md** - Terminology consistency
  - 14 core terms with Chinese/English/Japanese
  - Unified terminology across tri-lingual versions

---

## [2026-02-02 and Earlier]

### Initial Release
- **text-book** - Main documentation
  - Complete tri-lingual support (中文/English/日本語)
  - 13 chapters covering research engineering methodology
  - Built with mdBook, deployed to GitHub Pages
- **manga-book** - Visual storytelling version
  - 12 chapters following Xiao Yan's journey
  - 284 manga panels + illustrations
  - Character-driven narrative approach
- **Tri-lingual Infrastructure**
  - Separate source directories: src/, src_en/, src_ja/
  - Unified build system for all languages
  - Language switcher in UI
- **Azure Translation Pipeline**
  - Batch translation with Azure Cognitive Services
  - Safe translation wrapper with API key management
  - Fallback to manual translation when needed

---

## Project Statistics (as of 2026-02-07)

- **Documentation**: 65,817 words
  - text-book: 43,916 words (中 10,103 + 英 27,072 + 日 6,741)
  - manga-book: 11,006 words
  - Project docs: 10,895 words
- **Images**: 671 total (284 manga + 139 text-book + others)
- **Scripts**: 15 automation tools (7 shell + 8 Python)
- **Git**: 127 commits, 4 branches
- **Markdown**: 921 files

---

## Links

- **Repository**: [GitHub](https://github.com/li-hongmin/Research-Engineering-OS-)
- **Documentation**: [GitHub Pages](https://li-hongmin.github.io/Research-Engineering-OS-/)
- **Issue Tracker**: [GitHub Issues](https://github.com/li-hongmin/Research-Engineering-OS-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/li-hongmin/Research-Engineering-OS-/discussions)

---

*This changelog is maintained as part of the REOS "记录优先" (Record First) principle.*
