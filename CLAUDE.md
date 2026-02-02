# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Research Engineering OS** (把返工压缩成规范 + 模板 + 检查清单) - A multilingual mdBook targeting researchers in AI/ML/computational biology who need reproducible, traceable research practices.

**Languages**: Chinese (primary), English, Japanese
**Author**: Li Hongmin (李鸿敏), Dept of Computational Biology, University of Tokyo
**Live Site**: https://li-hongmin.github.io/Research-Engineering-OS/

### Core Themes
- **Experiment as Unit**: Treating experiments (not code) as the fundamental unit
- **Three Types of Debt**: Exploration debt, validation debt, reproducibility debt
- **Default Behaviors**: Lightweight habits over complex tools
- **AI-Era Challenges**: AI makes code generation easy but verification harder

## Build Commands

```bash
# Build multilingual book (Chinese + English + Japanese)
cd text-book
./build_all.sh

# Local preview
cd text-book/book && python -m http.server 8000
# Visit http://localhost:8000
```

**Output Structure**:
```
book/
├── index.html  # Redirects to /zh/
├── zh/         # Chinese version
├── en/         # English version
└── ja/         # Japanese version
```

## Project Structure

```
text-book/                 # Multilingual research engineering book
├── src/                    # Chinese source (primary)
├── src_en/                 # English source
├── src_ja/                 # Japanese source
├── manga/                  # Manga/comics resources for illustrations
├── theme/
│   ├── custom.css          # Custom styles
│   └── language-picker.js  # Language switcher dropdown
├── book.toml               # mdBook configuration
├── build_all.sh            # Multilingual build script
├── generate_comics_parallel.py  # Manga illustration generator (Azure OpenAI)
├── sync_comics_to_en.py    # Sync illustrations across languages
└── insert_comics_en.py     # Insert comics into English markdown

manga-book/                # Independent manga/comic edition
├── src/                    # Manga markdown source
├── images/                 # Manga panel images
├── theme/
├── book.toml               # mdBook configuration
└── CLAUDE.md              # Manga-specific guidance
```

### Source Files (in each src/ directory)
- `README.md` - Book introduction
- `SUMMARY.md` - Table of contents (defines chapter order)
- `00-preface.md` through `08-multi-path.md` - Main chapters
- `no-boom.md`, `team.md` - Additional chapters
- `appendix-templates.md` - Templates appendix
- `images/` - Chapter header images
- `images/comics/` - Manga-style illustrations (124 per language)

## Key Workflows

### Adding/Editing Content (text-book/)
1. Edit markdown in `text-book/src/` (Chinese primary)
2. Update corresponding file in `text-book/src_en/` and `text-book/src_ja/`
3. Run `text-book/build_all.sh` to verify
4. Commit and push (GitHub Actions auto-deploys)

### Working on Manga Edition (manga-book/)
1. Edit markdown in `manga-book/src/`
2. Add/update images in `manga-book/images/`
3. Run `mdbook build` in `manga-book/` directory
4. See manga-book/CLAUDE.md for detailed guidance

### Syncing Illustrations (for text-book/)
```bash
cd text-book
# After adding comics to Chinese, sync to English
python3 sync_comics_to_en.py
```

### Generating New Illustrations (for text-book/)
```bash
cd text-book
# Requires Azure OpenAI credentials in ~/.azure_openai_config
source ~/.azure_openai_config
python3 generate_comics_parallel.py --all --workers 8
```

### Heading Hierarchy Rules
- `#` - Chapter title (one per file)
- `##` - Major sections
- `###` - Subsections
- `####` - Sub-subsections
- **No level jumps** (e.g., `##` directly to `####`)

## GitHub Actions Deployment

Configured in `.github/workflows/deploy.yml`:
- Triggers on push to `main`
- Runs `text-book/build_all.sh` for multilingual book
- Deploys `text-book/book/` (Chinese + English + Japanese) to GitHub Pages
- Note: Manga edition (manga-book/) currently requires manual deployment

**GitHub Pages Setup**: Settings → Pages → Source: "GitHub Actions"

## Content Conventions

- **Language**: Chinese primary with English technical terms
- **Structure**: "Problem → Symptoms → Cost → Solution" pattern
- **10-Minute Actions**: Practical steps at chapter ends
- **Bold formatting**: `**text**：` (colon outside), not `**text：**`
