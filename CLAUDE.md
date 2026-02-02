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
Research-Engineering-OS-/
├── text-book/                       # Multilingual research engineering book
│   ├── src/                         # Chinese source (primary)
│   ├── src_en/                      # English source
│   ├── src_ja/                      # Japanese source
│   ├── theme/                       # mdBook theme
│   │   ├── custom.css               # Custom styles
│   │   └── language-picker.js       # Language switcher
│   ├── book.toml                    # mdBook configuration
│   ├── build_all.sh                 # Multilingual build script
│   └── book/                        # Build output (generated)
│
├── manga-book/                      # Independent manga/comic edition
│   ├── src/                         # Manga markdown source (Chinese)
│   ├── images/                      # Manga panel images
│   ├── theme/                       # Custom mdBook theme
│   ├── book.toml                    # mdBook configuration
│   ├── CLAUDE.md                    # Manga-specific guidance
│   ├── .gitignore                   # Git ignore rules
│   └── book/                        # Build output (generated)
│
├── shared/                          # Shared resources & tools
│   ├── scripts/                     # Illustration generation tools
│   │   ├── generate_comics.py       # Original comic generator
│   │   ├── generate_comics_v2.py    # Improved version
│   │   ├── generate_comics_parallel.py  # Parallel generator (Azure OpenAI)
│   │   ├── generate_illustrations.py    # Illustration processor
│   │   ├── sync_comics_to_en.py    # Sync to other languages
│   │   └── insert_comics_en.py     # Insert into markdown
│   │
│   ├── manga-resources/             # Illustration assets
│   │   ├── panels/                  # 180+ manga panel images (PNG)
│   │   │   ├── 00-preface/
│   │   │   ├── 01-why-flip/
│   │   │   ├── 02-experiment-unit/
│   │   │   ├── ... (chapters 3-11)
│   │   │   └── 11-epilogue/
│   │   │
│   │   ├── storyboards/             # Chapter specifications (YAML)
│   │   │   ├── 00-preface.yaml
│   │   │   ├── 01-why-flip.yaml
│   │   │   └── ... (all 12 chapters)
│   │   │
│   │   ├── prompts/                 # AI generation prompts
│   │   ├── generate_manga.py        # Manga generation tool
│   │   └── README.md                # Asset documentation
│   │
│   └── README.md                    # Shared resources guide
│
└── .github/
    └── workflows/
        └── deploy.yml               # CI/CD pipeline (deploys text-book)
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
4. See `manga-book/CLAUDE.md` for detailed guidance

### Generating New Illustrations

**Illustration assets are stored in `shared/manga-resources/`**

#### 1. Syncing Illustrations (across languages for text-book/)
```bash
cd shared/scripts
# After adding comics to Chinese, sync to English
python3 sync_comics_to_en.py
```

#### 2. Generating Comics (new panels via Azure OpenAI)
```bash
cd shared/scripts

# Setup Azure OpenAI credentials
source ~/.azure_openai_config

# Generate comics for specific chapter or all
python3 generate_comics_parallel.py --chapter 04-git-proof --workers 4
python3 generate_comics_parallel.py --all --workers 8

# Outputs to: ../manga-resources/panels/
```

#### 3. Inserting Comics into Markdown
```bash
cd shared/scripts
# Insert generated comics into English markdown
python3 insert_comics_en.py
```

### Working with Shared Resources

**Scripts location**: `shared/scripts/`
```bash
cd shared/scripts
python3 generate_comics_parallel.py --help   # View all options
```

**Assets location**: `shared/manga-resources/`
```
panels/           # 180+ generated manga-style illustrations
storyboards/      # 12 YAML chapter specifications
prompts/          # AI generation prompts
```

**For both text-book and manga-book**:
- Reference panels from `../../shared/manga-resources/panels/`
- Use storyboards as narrative templates
- Run generation scripts as needed

### Heading Hierarchy Rules
- `#` - Chapter title (one per file)
- `##` - Major sections
- `###` - Subsections
- `####` - Sub-subsections
- **No level jumps** (e.g., `##` directly to `####`)

## Shared Resources Guide

The `shared/` directory contains reusable tools and assets used by both `text-book/` and `manga-book/`:

### Scripts (`shared/scripts/`)
- **generate_comics.py** - Original comic generation
- **generate_comics_v2.py** - Improved version with better quality
- **generate_comics_parallel.py** - Parallel generation via Azure OpenAI (recommended)
- **generate_illustrations.py** - Illustration post-processing
- **sync_comics_to_en.py** - Synchronize comics across languages
- **insert_comics_en.py** - Insert comics into English markdown files

### Manga Resources (`shared/manga-resources/`)
- **panels/** - 180+ generated manga panel images organized by chapter
  - Format: `{chapter_id}_{page_number:03d}.png`
  - Example: `04_001.png`, `04_002.png`, ..., `04_025.png`
  - Location pattern: `panels/{chapter-name}/`

- **storyboards/** - YAML specifications for each chapter
  - Used by generation scripts to define narrative flow
  - One file per chapter (e.g., `04-git-proof.yaml`)
  - Enables reproducible illustration generation

- **prompts/** - AI generation prompts and templates

- **generate_manga.py** - Manga-specific generation tool

- **README.md** - Detailed asset documentation

### Using Shared Resources

**From text-book:**
```bash
# Run generation tools
cd shared/scripts
python3 generate_comics_parallel.py --all --workers 8

# Outputs placed in: shared/manga-resources/panels/
# Reference in markdown: ../../../shared/manga-resources/panels/04_001.png
```

**From manga-book:**
```bash
# Reference panels from shared
cd manga-book/images
# Create symlink or copy: ln -s ../../shared/manga-resources/panels/* .

# Or reference in markdown:
# ![](../../shared/manga-resources/panels/04_001.png)
```

**For detailed workflow**, see `shared/README.md`.

---

## GitHub Actions Deployment

Configured in `.github/workflows/deploy.yml`:
- Triggers on push to `main`
- **Builds both editions:**
  - Runs `text-book/build_all.sh` → generates Chinese + English + Japanese
  - Runs `mdbook build` in `manga-book/` → generates manga edition
  - Combines outputs: manga-book deployed to `/manga/` subdirectory
- Deploys unified output to GitHub Pages

**Final structure at GitHub Pages:**
```
https://li-hongmin.github.io/Research-Engineering-OS/
├── index.html         ← Navigation page (文本版 / 漫画版)
├── zh/                ← Text book Chinese
├── en/                ← Text book English
├── ja/                ← Text book Japanese
└── manga/             ← Manga edition
    └── (all manga chapters)
```

**GitHub Pages Setup**: Settings → Pages → Source: "GitHub Actions"

## Directory-Specific Guidance

### text-book/ Focus

- Edit multilingual content (src/, src_en/, src_ja/)
- Reference: `text-book/CLAUDE.md` (if exists) or ask for help
- Build: `./build_all.sh` generates Chinese + English + Japanese
- Content: Comprehensive chapters with technical depth
- Deployment: ✅ Automatic via GitHub Actions

### manga-book/ Focus

- Edit manga narrative and story (src/*.md)
- Manage manga-specific illustrations (images/)
- Build: `mdbook build` for Chinese version only
- Content: Visual storytelling with character development
- Reference: `manga-book/CLAUDE.md` for detailed patterns
- Deployment: 📝 Manual (can be set up via new workflow)

### shared/ Focus

- Maintain illustration generation tools (scripts/)
- Manage illustration assets (manga-resources/)
- **Do not edit files here lightly** - affects both projects
- Update documentation in `shared/README.md`
- Version control all assets (git tracks PNG files)

---

## Content Conventions

### Markdown Standards

- **Language**: Chinese primary with English technical terms
- **Structure**: "Problem → Symptoms → Cost → Solution" pattern
- **10-Minute Actions**: Practical steps at chapter ends
- **Bold formatting**: `**text**：` (colon outside), not `**text：**`

### Heading Hierarchy

- `#` - Chapter title (one per file)
- `##` - Major sections
- `###` - Subsections
- `####` - Sub-subsections
- **No level jumps** (e.g., `##` directly to `####`)

### Image References

**text-book:**

```markdown
![Description](../images/chapter-id/image-name.png)
```

**manga-book:**

```markdown
![Description](../images/chapter-id/panel-name.png)
# Or reference from shared:
# ![](../../shared/manga-resources/panels/04_001.png)
```
