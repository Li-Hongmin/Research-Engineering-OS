# Research Engineering OS (研究工程 OS)

A story-driven educational resource series for researchers in AI/ML/computational biology who need reproducible, traceable research practices.

[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md) [![Contributing](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md) ![Last Commit](https://img.shields.io/github/last-commit/Li-Hongmin/Research-Engineering-OS) ![Languages](https://img.shields.io/github/languages/count/Li-Hongmin/Research-Engineering-OS) ![Top Language](https://img.shields.io/github/languages/top/Li-Hongmin/Research-Engineering-OS) ![Repo Size](https://img.shields.io/github/repo-size/Li-Hongmin/Research-Engineering-OS) ![GitHub Pages](https://img.shields.io/badge/docs-live-success?logo=github)

## 📚 Project Overview

**Research Engineering OS** teaches practical research engineering practices through two complementary formats:

### 🌐 **text-book/** - Multilingual Text Edition
The comprehensive multilingual version with technical depth.
- **Languages**: Chinese 🇨🇳 (primary), English 🇺🇸, Japanese 🇯🇵
- **Format**: Traditional mdBook with text + illustrations
- **Scope**: 8+ chapters covering research engineering fundamentals
- **Audience**: Researchers wanting structured guidance
- **Live**: https://li-hongmin.github.io/Research-Engineering-OS/

### 📖 **manga-book/** - Manga Edition
A visual, story-driven version using manga-style illustrations.
- **Language**: Chinese 🇨🇳 (primary language, independent project)
- **Format**: Page-turning mdBook with manga panels
- **Scope**: 12 chapters + prologue/epilogue, 11-25 pages each
- **Main Character**: 小研 (Xiao Yan) - a computational biology PhD student
- **Audience**: Visual learners and anyone wanting narrative context

## 🚀 Quick Start

### For Text Book (Multilingual)
```bash
cd text-book
./build_all.sh          # Build all 3 language versions
cd book && python -m http.server 8000   # Preview locally
```

### For Manga Book
```bash
cd manga-book
mdbook build            # Build Chinese version
cd book && python -m http.server 8000   # Preview locally
```

## 📖 Core Content Structure

### text-book/
```
src/              → Chinese content (primary)
src_en/           → English translated content
src_ja/           → Japanese translated content
manga/            → Illustration generation resources
build_all.sh      → Multilingual build orchestration
```

### manga-book/
```
src/              → Manga markdown source (Chinese)
images/           → Manga panel images (organized by chapter)
theme/            → Custom mdBook theme
book.toml         → mdBook configuration
```

## 📝 Key Concepts

### Three Types of Technical Debt
1. **Exploration Debt** - Incomplete investigation of feasibility
2. **Validation Debt** - Skipped or incomplete verification
3. **Reproducibility Debt** - Missing documentation/traceability

### Experiment as Unit
- Treat complete reproducible experiments (not isolated code) as the fundamental unit
- Record experiment context: why, what, results
- Use Git to maintain execution history and proof

### Default Behaviors
- Lightweight practices over complex tools
- Incremental verification over big-bang testing
- Story-based learning over abstract principles

## 🌍 Supported Languages

| Edition | Language | Status | Location |
|---------|----------|--------|----------|
| Text Book | 中文 (Chinese) | Active | `text-book/src/` |
| Text Book | English | Active | `text-book/src_en/` |
| Text Book | 日本語 (Japanese) | Active | `text-book/src_ja/` |
| Manga Book | 中文 (Chinese) | Active | `manga-book/src/` |

## 👤 Author

**Li Hongmin (李鸿敏)**
- Department of Computational Biology, University of Tokyo
- Focus: Research engineering practices for AI/ML researchers

## 🔗 Links

- **Published Site**: https://li-hongmin.github.io/Research-Engineering-OS/
- **GitHub**: https://github.com/li-hongmin/Research-Engineering-OS-
- **Author Profile**: [University of Tokyo](https://www.u-tokyo.ac.jp/)

## 📦 Project Structure

```
Research-Engineering-OS-/
├── text-book/              # Multilingual text edition
│   ├── src/               # Chinese source files
│   ├── src_en/            # English source files
│   ├── src_ja/            # Japanese source files
│   ├── manga/             # Illustration resources
│   ├── theme/             # mdBook theme
│   ├── book.toml          # Configuration
│   └── build_all.sh       # Build script
│
├── manga-book/            # Manga edition (independent)
│   ├── src/               # Manga source files
│   ├── images/            # Manga panel images
│   ├── theme/             # Custom theme
│   ├── book.toml          # Configuration
│   └── CLAUDE.md          # Development guide
│
├── .github/workflows/     # CI/CD pipeline
└── CLAUDE.md             # Root-level development guide
```

## 🔧 Development Workflow

### Contributing to Text Book
See `CLAUDE.md` in project root for:
- Content editing guidelines
- Language sync workflow
- Illustration generation
- Build and deployment

### Contributing to Manga Book
See `manga-book/CLAUDE.md` for:
- Story enhancement patterns
- Page structure conventions
- Character voice guide
- Manga-specific styling

## 📚 Building the Book

### Multilingual Build (All 3 Languages)
```bash
cd text-book
chmod +x build_all.sh
./build_all.sh
# Outputs to: text-book/book/{zh,en,ja}/
```

### Single Language Build
```bash
cd text-book
mdbook build              # Builds Chinese version
```

### Manga Build
```bash
cd manga-book
mdbook build
# Outputs to: manga-book/book/
```

## 🚀 Deployment

### GitHub Pages (Automatic)
The multilingual text book is automatically deployed to GitHub Pages on every push to `main` branch via GitHub Actions.

- Workflow: `.github/workflows/deploy.yml`
- Deployment: `text-book/book/` → GitHub Pages
- URL: https://li-hongmin.github.io/Research-Engineering-OS/

### Manga Book (Manual)
Currently, the manga edition requires manual deployment setup.

## 📋 Documentation & Guidelines

### Quick Links
- ⚡ **[Quick Start](QUICKSTART.md)** - 5-10 minute guide for new contributors
- 📚 **[Documentation Index](DOCS_INDEX.md)** - Complete navigation to all project docs
- ✅ **[Content Review Checklist](CONTENT_REVIEW_CHECKLIST.md)** - Systematic quality review guide
- 🤝 **[Contributing Guide](CONTRIBUTING.md)** - How to contribute (5 ways + workflows)
- 📜 **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines
- 📋 **[Changelog](CHANGELOG.md)** - Project history and release notes
- ⚖️ **[License Selection Guide](LICENSE_GUIDE.md)** - Guide for choosing the right license

### Content Guidelines
- **Language**: Chinese primary with English technical terms
- **Structure**: Problem → Symptoms → Cost → Solution
- **Heading Levels**: No jumps (# → ## → ### → ####)
- **Bold Formatting**: `**text**：` (colon outside) not `**text：**`
- **10-Minute Actions**: Practical steps at chapter ends

## 🛠️ Quality Assurance & Automation

### Quick Commands (Makefile)
The project includes a Makefile for unified command entry:

```bash
make help                # Show all available commands
make health              # Run comprehensive project health check
make lint                # Run Markdown lint check
make check-all           # Run all quality checks
make build               # Build all versions (text-book + manga-book)
make clean               # Clean build artifacts
```

See `make help` for the complete list of 20+ available commands.

### Automated Health Checks
The project includes comprehensive health check tools (also available via Makefile):

```bash
./check_health.sh                 # Comprehensive project health check
./check_markdown_lint.sh          # Markdown quality verification
./check_links.sh --fast           # Link validity check
./check_translation_sync.sh       # Translation completeness check
./check_manga_images.sh           # Manga image asset verification
./check_content_consistency.sh    # Three-language content consistency check
```

### Continuous Integration
- **GitHub Actions**: Automatic health check + deployment on every push
- **Pre-commit Hook**: Local validation before commits
- **Daily Health Reports**: Automatic daily project status check (09:00 JST)
- **PR Comments**: Automated health status feedback on pull requests

### Project Health Status
Current status: ✅ **EXCELLENT** (as of 2026-02-07 18:05 JST)
- 923 Markdown files validated
- 671 images (139 text-book + 264 manga + 268 other assets)
- 3 language versions synchronized
- 65k+ words across all editions
- All builds passing

## ⚖️ License

[Specify license information here]

## 📧 Contact

For questions or contributions, please reach out through:
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community discussions
- **Email**: lihongmin@edu.k.u-tokyo.ac.jp (Li Hongmin)

---

**Last Updated**: 2026-02-07 18:05 JST
**Version**: 2.3 (Updated project statistics, contact info, and health status)
