# Shared Resources (共享资源)

This directory contains resources shared between the text-book and manga-book projects.

## 📁 Directory Structure

### `scripts/` - Active Utility Scripts
```
scripts/
├── generate_comics_parallel.py     # Parallel generation (Azure OpenAI) ⭐ ACTIVE
└── README.md                       # Script documentation
```

### `archive/scripts/` - One-Time Generation Tools
```
archive/scripts/
├── generate_comics.py              # Original comic generation (v1)
├── generate_comics_v2.py           # Version 2 with improvements
├── generate_illustrations.py       # Illustration post-processor
├── generate_manga.py              # Manga-specific generator
├── sync_comics_to_en.py           # Language synchronization tool
└── insert_comics_en.py            # Markdown insertion tool
```

**Note:** Archived scripts were used for initial content generation and are kept for reference only. See `archive/README.md` for details.

**Usage:**
```bash
cd shared/scripts
python3 generate_comics_parallel.py --all --workers 8
```

### `manga-resources/` - Illustration and Storyboard Assets
```
manga-resources/
├── panels/                         # Generated manga panel images
│   ├── 00-preface/                # Panels for preface
│   ├── 01-why-flip/               # Panels for chapter 1
│   └── ...                        # Panels for other chapters (11-epilogue)
├── storyboards/                    # YAML storyboard definitions
│   ├── 00-preface.yaml
│   ├── 01-why-flip.yaml
│   └── ...                        # Storyboards for all chapters
├── prompts/                        # AI generation prompts (if any)
├── generate_manga.py              # Manga-specific generation script
└── README.md                      # Manga resources documentation
```

**Contents:**
- **panels/**: 180+ generated manga-style illustrations organized by chapter
- **storyboards/**: YAML specifications for each chapter's visual narrative
- **generate_manga.py**: Scripts for manga generation and illustration processing

## 🔗 Usage from Projects

### From text-book/
These scripts are used to generate comic illustrations for the multilingual book:

```bash
cd shared/scripts
source ~/.azure_openai_config
python3 generate_comics_parallel.py --all --workers 8
# Output: images placed in text-book/src/images/comics/
```

### From manga-book/
The manga-resources can serve as reference or be symlinked:

```bash
# Option 1: Reference from shared
cd manga-book/images
# Create symlink or copy panels from ../../shared/manga-resources/panels/

# Option 2: Use storyboards as reference
ls ../../shared/manga-resources/storyboards/
```

## 📝 Key Scripts

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `generate_comics_parallel.py` | Bulk comic generation via Azure OpenAI | Storyboards | PNG panel images |
| `generate_comics.py` | Original comic generation | Prompts | Comic images |
| `generate_comics_v2.py` | Improved generation logic | Storyboards | Refined images |
| `sync_comics_to_en.py` | Synchronize comics across languages | Chinese panels | English-ready structure |
| `insert_comics_en.py` | Insert comics into English markdown | Comic paths, markdown | Updated markdown with images |
| `generate_manga.py` | Manga-specific generation pipeline | Specifications | Manga panels |

## 🎨 Illustration Generation Workflow

### Prerequisites
```bash
# Azure OpenAI API credentials
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="your-endpoint"
export AZURE_OPENAI_API_VERSION="your-version"
```

### Basic Workflow
```bash
cd shared/scripts

# 1. Generate new comics
python3 generate_comics_parallel.py --chapter 04-git-proof --workers 4

# 2. Sync to other languages
python3 sync_comics_to_en.py

# 3. Insert into English markdown
python3 insert_comics_en.py
```

## 📊 Asset Organization

### Panel Image Naming Convention
- Format: `{chapter_id}_{page_number:03d}.png`
- Example: `04_001.png`, `04_002.png`, ..., `04_025.png`
- Location: `manga-resources/panels/{chapter-name}/`

### Storyboard Format
- YAML specification files
- Defines narrative flow and illustration requirements
- Location: `manga-resources/storyboards/{chapter-name}.yaml`

## 🔄 Workflow Integration

### For text-book (Multilingual)
1. Edit storyboards in `manga-resources/storyboards/`
2. Run generation scripts in `scripts/`
3. Output automatically placed in `text-book/src/images/comics/`
4. Run `text-book/build_all.sh` to build multilingual version

### For manga-book (Manga Edition)
1. Reference or copy panels from `manga-resources/panels/`
2. Use storyboards as narrative template from `manga-resources/storyboards/`
3. Create markdown in `manga-book/src/`
4. Run `mdbook build` in `manga-book/`

## 🛠️ Maintenance

### Adding New Illustrations (If Needed)
1. Create/update storyboard YAML in `manga-resources/storyboards/`
2. Run generation script:
   ```bash
   cd scripts
   python3 generate_comics_parallel.py --chapter {chapter-name} --workers 4
   ```
3. Generated panels stored in `manga-resources/panels/`
4. Update references in both `text-book/` and `manga-book/`

### Working with Archived Scripts
- For reference: See `archive/scripts/` and `archive/README.md`
- To restore: Use `git mv` to bring back from archive
- To understand alternatives: Check different versions in archive

### Critical Assets (Do Not Delete)
- ✅ `manga-resources/panels/` - 180+ finished panel images
- ✅ `manga-resources/storyboards/` - 12 YAML specifications
- ✅ `scripts/generate_comics_parallel.py` - Active generation tool

## 📦 Versioning

All shared resources are version-controlled via Git:
- Script changes are tracked in commits
- Panel images (PNG) are stored as binary artifacts
- YAML storyboards enable reproducible generation

## 💡 Future Enhancements

- Automated image optimization pipeline
- Script version management and compatibility tracking
- Storyboard validation and consistency checking
- Multi-language generation coordination

---

**Last Updated**: 2026-02-02
**Related Projects**: text-book, manga-book
**Maintenance**: Li Hongmin (李鸿敏)
