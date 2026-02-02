# Archive (归档)

This directory contains one-time generation and migration scripts that were used to create the initial illustrations and content structure.

## 📦 Archived Scripts (`scripts/`)

### One-Time Tools (Keep for reference)

| Script | Purpose | Status | Notes |
|--------|---------|--------|-------|
| `generate_comics.py` | Original comic generation | ✓ Archived | First implementation, superseded by v2/parallel |
| `generate_comics_v2.py` | Improved comic generation | ✓ Archived | Better quality, but parallel version is preferred |
| `generate_illustrations.py` | Illustration post-processing | ✓ Archived | Used for refining generated images |
| `generate_manga.py` | Manga panel generation | ✓ Archived | Reference for panel creation workflow |
| `generate_manga_book.py` | Generate manga Markdown from YAML | ✓ Archived | Used to create initial 12 chapters from storyboards |
| `insert_comics_en.py` | Insert comics into English markdown | ✓ Archived | One-time migration tool for content insertion |
| `sync_comics_to_en.py` | Sync comics across languages | ✓ Archived | Used for initial language synchronization |

## 🎯 When to Use Archived Scripts

### Reference Implementation
```bash
# If you need to understand the original approach
cat scripts/generate_comics.py          # Original version
cat scripts/generate_comics_v2.py       # Improved version
```

### Emergency Fallback
If `generate_comics_parallel.py` fails or needs alternative approaches:
```bash
# Try the original implementation
cd shared/archive/scripts
python3 generate_comics.py --help
```

### Historical Context
These scripts represent the iterative development of the comic generation system:
1. `generate_comics.py` - Initial working version
2. `generate_comics_v2.py` - Quality improvements
3. `generate_comics_parallel.py` (active) - Parallel Azure OpenAI implementation

## 📝 Why Archived?

**One-time Usage**
- Initial content generation complete
- Manga panel assets created and stored
- Language synchronization completed

**Maintenance Burden**
- Multiple versions create maintenance complexity
- Parallel version is faster and more reliable
- Original versions have Azure OpenAI credential issues

**Active Alternative**
- `shared/scripts/generate_comics_parallel.py` is the recommended tool
- More recent, more efficient, better documented

## 🔄 Restoring from Archive

If you need to restore an archived script:

```bash
# Move back to active scripts
git mv shared/archive/scripts/generate_comics_v2.py shared/scripts/

# Update documentation
# Update CLAUDE.md to reference the restored script

# Commit
git add .
git commit -m "restore: bring back generate_comics_v2.py for X reason"
```

## 📚 Related Documentation

- **Active scripts**: See `../scripts/` directory
- **Overall workflow**: See `../README.md`
- **Project guide**: See `../../CLAUDE.md`

## 🗂️ Archive Organization

```
archive/
├── scripts/                 # One-time generation tools
├── README.md               # This file
└── [future]                # Space for other archived items
```

---

**Last Updated**: 2026-02-02
**Status**: All required content has been generated; archive scripts are for reference only
