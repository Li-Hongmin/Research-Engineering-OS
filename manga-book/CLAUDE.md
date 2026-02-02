# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Research Engineering OS - Manga Edition** is a story-driven educational book using manga panels to teach research engineering practices to AI/ML/computational biology researchers.

**Key Details**:
- **Format**: mdBook with manga panel illustrations (翻页模式 - page-turning mode)
- **Author**: Li Hongmin, Dept of Computational Biology, University of Tokyo
- **Content Structure**: 12 chapters + prologue/epilogue, 11-25 pages per chapter
- **Language**: Chinese (primary language)
- **Main Character**: 小研 (Xiao Yan) - a computational biology PhD student learning research engineering
- **Themes**: Three types of technical debt, experiments as unit of analysis, Git as evidence, AI-era workflows

## Project Architecture

### Directory Structure

```
manga_book/
├── src/                     # Markdown source files (generated/edited here)
│   ├── 00-preface/         # Prologue (15 pages)
│   ├── 01-why-flip/        # Chapter 1 (25 pages)
│   ├── 02-experiment-unit/ # Chapter 2 (20 pages)
│   ├── 03-repo-layout/     # Chapter 3 (25 pages)
│   ├── 04-git-proof/       # Chapter 4 (25 pages)
│   ├── 05-dod/             # Chapter 5 (22 pages) ← Recently enhanced
│   ├── 06-logging/         # Chapter 6 (20 pages)
│   ├── 07-ai-workflow/     # Chapter 7 (25 pages)
│   ├── 08-multi-path/      # Chapter 8 (22 pages)
│   ├── 09-no-boom/         # Chapter 9 (25 pages)
│   ├── 10-team/            # Chapter 10 (25 pages)
│   ├── 11-epilogue/        # Epilogue (15 pages)
│   ├── images/             # Manga panel images organized by chapter
│   ├── README.md           # Cover/intro page
│   └── SUMMARY.md          # Table of contents (auto-generated)
├── book/                    # Build output (mdBook HTML)
├── theme/                   # Custom CSS styling
├── generate_manga_book.py   # Python generator (legacy, for reference)
├── book.toml               # mdBook configuration
└── CLAUDE.md              # This file
```

### Content Format: Page-Turning Mode

Each chapter is split into individual Markdown files (01.md, 02.md, ... 25.md), with consistent HTML structure:

```html
<div class="manga-layout">

<div class="manga-story">
<div class="manga-story-label">📖 第X页</div>
<p class="manga-story-content">
  Story narration, dialogue, or character internal monologue.
  Use <em>💭 inner-thought</em> for character thoughts.
  Use <strong>context headers</strong> for scene transitions.
</p>
</div>

<div class="manga-image-container">
![Description](../images/CHAPTER-ID/PANEL-ID.png)
</div>

</div>

---

<div class="manga-footer">
[← Previous/Return] &nbsp;&nbsp;&nbsp; [Next →]
</div>
```

**Key conventions**:
- `📖 第X页` label for each page number
- Story text is always in `<p class="manga-story-content">`
- Character internal thoughts marked with 💭 emoji wrapped in `<em>` tags
- Scene descriptions in `<strong>` tags
- Bottom navigation using relative Markdown links
- One story block per page (do not split narrative across multiple `<div class="manga-story">` unless necessary)

## Build Commands

### Build the book
```bash
cd /Users/lihongmin/ideas/Research-Engineering-OS-/book_i18n/manga_book
mdbook build
```

### Preview locally
```bash
cd book && python -m http.server 8001
# Open http://localhost:8001
```

### Complete workflow (from project root)
```bash
cd /Users/lihongmin/ideas/Research-Engineering-OS-/book_i18n/manga_book
mdbook build && cd book && python -m http.server 8001
```

## Editing Workflow

### Story Enhancement Guidelines

When enhancing chapter narratives (e.g., 05-dod for stronger storytelling):

1. **Read source files** in `src/XX-chapter/` to understand current narrative
2. **Enhance story quality** while preserving chapter structure
3. **Maintain character consistency**: 小研 is inexperienced but driven; 导师 is wise and Socratic
4. **Use narrative techniques**:
   - Internal monologue (💭) for character perspective
   - Scene transitions (`<strong>Bold descriptions</strong>`) for pacing
   - Multiple `<p>` tags within single `<div class="manga-story">` for paragraph breaks
   - Natural dialogue flow between characters
5. **Link knowledge to story**: Make technical concepts emerge naturally from character experiences
6. **Test after editing**: Run `mdbook build` and preview in browser

### File Naming & Organization

- Chapter directories: `XX-chapter-name` (e.g., `05-dod`)
- Page files: Sequential numbers `01.md`, `02.md`, ... `NN.md`
- Images: Organized in `images/XX-chapter-name/` with panel IDs (e.g., `05_001.png`, `05_002.png`)
- Never edit `SUMMARY.md` manually - it reflects actual chapter/page count

## Story Structure & Themes

### Chapter 5: Definition of Done (05-dod) - Enhanced Example

This chapter demonstrates the narrative structure:

1. **Problem Setup (Pages 1-4)**: 小研 confidently submits her experiment, then 导师 asks three probing questions
   - Page 1: Excitement + doubt
   - Pages 2-4: Three incremental questions (Can replicate? Why work? Fair baseline?)
2. **Problem Deepening (Pages 5-10)**: Hidden "landmines" (bugs) explode
   - Pages 7-9: Each landmine manifested in 小研's actual experience
   - Page 10: Critical moment of crisis (before solution)
3. **Solution & Learning (Pages 11-17)**: 导师 guides DoD (Definition of Done)
   - Page 11: Principle - "detect landmines early"
   - Pages 12-17: Each DoD criterion tied to previous landmine
4. **Application (Pages 18-22)**: 小研 applies lessons

**Narrative Techniques Used**:
- **Emotional arc**: Confidence → Doubt → Despair → Insight → Action
- **Internal monologue**: 💭 Marks show 小研's changing perspective
- **Story-knowledge fusion**: Each DoD item directly relates to a problem 小研 just experienced
- **Pacing**: Mix of dialogue, action, reflection, and teaching moments

### Core Themes Across All Chapters

1. **Three Types of Technical Debt**: Exploration, validation, reproducibility
2. **Experiments as Units**: Think in terms of complete reproducible experiments, not isolated code
3. **Git as Evidence**: Version history proves causality and intent
4. **AI-Era Challenges**: Easy to generate code, hard to verify correctness
5. **Team & Communication**: How research engineering scales across groups

## Styling & CSS

Custom CSS in `theme/custom.css` provides:

- `.manga-layout`: Flex container for story + image
- `.manga-story`: Yellow background with left border (story text area)
- `.manga-story-label`: Small orange label "📖 第X页"
- `.manga-story-content`: Main narrative text (font: PingFang SC, size 1.15em)
- `.manga-image-container`: Image display area
- `.manga-footer`: Navigation links at bottom

**Do not modify CSS lightly** - ensure any changes preserve readability and manga aesthetic.

## Common Development Tasks

### Add a new page to a chapter
1. Create new file `src/XX-chapter/NN.md` with standard HTML structure
2. Update navigation links in adjacent pages (previous/next)
3. Add corresponding image to `images/XX-chapter/` (or use placeholder)
4. Rebuild with `mdbook build`

### Enhance an existing chapter
1. Read all pages in that chapter to understand narrative arc
2. Identify weak points (wooden dialogue, disconnected story-knowledge, flat emotions)
3. Enhance using internal monologue, scene descriptions, and concrete examples
4. Maintain page count (or update navigation if adding pages)
5. Test rebuild

### Review story quality
Focus on:
- **Emotional engagement**: Does the reader care about 小研's journey?
- **Knowledge integration**: Do technical concepts emerge naturally from story?
- **Character consistency**: Do dialogue and internal thoughts match personality?
- **Pacing**: Is there good balance between narrative and teaching?
- **Clarity**: Is the connection between problem-solution clear?

## Character Voice Guide

### 小研 (Xiao Yan)
- **Personality**: Smart, hardworking, but inexperienced and self-doubting
- **Speech**: Direct questions, self-criticism, moment of insight ("Oh, I see now!")
- **Internal thoughts**: Worry about mistakes, pride in accomplishments, gradual self-awareness
- **Arc**: Grows from "I finished, so I'm done" to "What does 'done' really mean?"

### 导师 (Mentor/Professor)
- **Personality**: Patient, wise, Socratic questioning style
- **Speech**: Asks clarifying questions rather than giving answers
- **Teaching method**: "Let me point out three problems... see why each matters?"
- **Role**: Guide 小研 to self-discovery, not blame

### 其他角色 (Other Characters)
- Keep distinct voices - avoid all characters sounding alike
- Use names consistently
- Dialogue should reveal character personality, not just information

## mdBook Configuration

See `book.toml`:
- Title: "研究工程 OS - 漫画版"
- Language: zh (Chinese)
- Theme: Custom CSS in `theme/custom.css`
- Git repository URL for source link

Minor updates to `book.toml` are safe; major changes (output format, chapter structure) require testing.

## Technical Notes

- **No multilingual build here**: This is Chinese-only (unlike parent `/book_i18n/` which has zh/en/ja versions)
- **Image paths**: Relative to each markdown file, pointing to `../images/CHAPTER-ID/`
- **SUMMARY.md**: Auto-generated from directory structure - do not edit manually
- **No code compilation**: Pure markdown + HTML, no programming language dependencies
- **Browser compatibility**: Standard mdBook output, works in all modern browsers

## Future Enhancement Patterns

The 05-dod chapter improvements (strong emotional arc + internal monologue + story-knowledge fusion) can be applied to other chapters:

1. **Phase 1 - Core narrative (pages 1-4, 7-10, 12-15)**: Enhance conflict, add 💭 thoughts, connect to learnings
2. **Phase 2 - Deepening (pages 5-6, 16-17, 18-21)**: Add transitions, reinforce character growth
3. **Phase 3 - Polish**: Dialogue refinement, pacing adjustments, final testing

Priority chapters for similar treatment: 01-why-flip, 06-logging, 07-ai-workflow (higher impact on reader engagement).
