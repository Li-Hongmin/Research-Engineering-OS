# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LaTeX book project titled **"Research Engineering OS: 把返工压缩成规范 + 模板 + 检查清单"** (Research Engineering OS: Compressing Rework into Standards + Templates + Checklists). The book is written in Chinese with mixed English technical terms and targets researchers in AI/ML/computational biology who need to maintain reproducible, traceable research code.

### Core Themes
- **Experiment as Unit**: Treating experiments (not code) as the fundamental unit of research
- **Debt Management**: Managing exploration debt, validation debt, and reproducibility debt
- **Default Behaviors**: Establishing lightweight, sustainable research practices over complex tools
- **AI-Era Challenges**: Addressing how AI coding assistants make code generation easy but verification/reproduction harder

## Build Commands

### Compilation
```bash
# Compile the book (requires XeLaTeX for Unicode/CJK support)
xelatex main.tex

# Full build (compile twice for TOC and cross-references)
xelatex main.tex && xelatex main.tex
```

**IMPORTANT**: This project MUST be compiled with XeLaTeX (or LuaLaTeX), NOT pdflatex, due to:
- Chinese (CJK) text throughout the document
- Unicode font requirements
- `fontspec` and `xeCJK` package dependencies

### Font Configuration
The project uses macOS system fonts for reliability:
- **Latin**: Times New Roman (with full italic/bold variants)
- **CJK Serif**: Songti SC (with AutoFakeSlant for italic effect)
- **CJK Mono**: Heiti SC

If compilation fails with font errors on other systems, you may need to adjust the font settings in main.tex lines 8-20 to use available fonts.

### VS Code LaTeX Workshop
The repository includes `.vscode/settings.json` configured for:
- Automatic XeLaTeX compilation (twice for TOC)
- Save-on-build enabled
- PDF viewer in tab
- Automatic cleanup of auxiliary files

To use in VS Code:
1. Install the "LaTeX Workshop" extension
2. Open the project folder
3. Open main.tex and save (Cmd+S / Ctrl+S) to trigger compilation
4. View PDF in the side panel

## File Structure

```
.
├── main.tex              # Main document (book class, XeLaTeX compilation)
├── chapters/             # Chapter files
│   ├── 00_preface.tex   # 前言 (Preface)
│   ├── 01_why_flip.tex  # Why last-minute overhauls happen
│   ├── 02_experiment_unit.tex  # Experiment as the fundamental unit
│   ├── 03_repo_layout.tex      # Repository structure
│   ├── 04_git_proof.tex        # Git-based provenance
│   ├── 05_dod.tex              # Definition of Done
│   ├── 06_logging.tex          # Logging practices
│   ├── 07_ai_workflow.tex      # AI-assisted workflows
│   ├── 08_multi_path.tex       # Multi-path exploration
│   ├── no_boom.tex             # Avoiding late-stage explosions
│   ├── team.tex                # Team collaboration
│   ├── templates.tex           # Appendix: Templates
│   └── ai_disasters.tex        # Appendix: AI failure cases
└── diagram.jpg           # Diagram asset (1024x1024 JPEG)
```

### Chapter Organization
- **Frontmatter**: Preface (00)
- **Mainmatter**: Chapters 01-08 + no_boom + team
- **Appendix**: templates + ai_disasters

### Chapter Files
All chapters now use consistent **numbered naming** (`01_why_flip.tex`, `02_experiment_unit.tex`, etc.). The unnumbered duplicate files have been removed for clarity.

## Architecture & Content Structure

### Key Concepts (explained in the book)

1. **Three Types of Debt** (Chapter 01: why_flip.tex)
   - **Exploration Debt**: Technical shortcuts taken for rapid prototyping that must be cleanable
   - **Validation Debt**: Skipped control experiments and rigorous testing
   - **Reproducibility Debt**: Missing environment/config/version tracking preventing result replication

2. **Experiment Object Model** (Chapter 02: experiment_unit.tex)
   ```
   experiment = code_version + config + data_version + environment + output + metrics
   ```
   Every experiment must answer 6 questions:
   - What code? (commit hash, dirty status)
   - What config? (file path + expanded params)
   - What data? (version/hash/split)
   - What environment? (Python/deps/drivers/hardware)
   - Where are artifacts? (models, logs, predictions)
   - What metrics? (evaluation script + post-processing)

3. **Repository Structure** (Chapter 03: repo_layout.tex)
   Fast vs. Slow variables separation:
   - **Slow (stable)**: `src/` - reusable, tested, maintainable core library
   - **Fast (explore)**: `experiments/` - disposable entry points and glue code
   ```
   src/          # Core library (slow variable)
   experiments/  # Entry points (fast variable, disposable)
   configs/      # Unified config (diffable, traceable)
   outputs/      # Organized by run_id (cleanable/archivable)
   reports/      # Generated from outputs (reproducible)
   tests/        # Smoke tests + unit tests
   ```

4. **run_id Convention**
   Every run should have a unique, sortable identifier:
   ```
   2026-02-01_0930_baseline
   2026-02-01_1130_ablation_noaug
   ```
   Outputs organized as:
   ```
   outputs/<run_id>/
     run.json
     run.md
     metrics.json
     artifacts/
   ```

### Templates (Appendix: templates.tex)

The book provides minimal templates for:
- **PR/Commit description** (even for solo work): purpose, changes, result impact, validation command, expected output, rollback
- **Experiment log** (run.md): Hypothesis, Change, Result, Compare-to, Next
- **Makefile targets**: test, train, eval, reproduce

## Writing Guidelines

### When Writing New Content

1. **Language**: Primary language is Chinese; technical terms often in English
2. **Tone**: Practical, experience-driven; author explicitly states this is NOT abstract methodology but "executable defaults" from real research experience
3. **Structure**: Heavy use of:
   - `\textbf{}` for emphasis
   - `\begin{itemize}` / `\begin{enumerate}` for structured lists
   - `\begin{verbatim}` for code/file structure examples
   - `\section{}` / `\subsection{}` / `\paragraph{}` hierarchy

4. **Recurring Patterns**:
   - "Definition → Symptoms → Cost → Solution" structure
   - "10-minute action" sections at chapter ends (immediate actionable steps)
   - Case references like `见案例~\ref{case:...}` linking to appendix

5. **Cross-references**: Use `\label{}` and `\ref{}` for chapters and cases

### LaTeX-Specific Notes

- **No italic for CJK**: The template uses `AutoFakeSlant=0.2` to simulate italic for Chinese fonts
- **Paragraph spacing**: `\parindent=0pt`, `\parskip=0.6\baselineskip` for readability
- **Book class**: Uses `\frontmatter`, `\mainmatter`, `\appendix` divisions
- **Include pattern**: `\include{chapters/XX}` (no .tex extension)

## Common Tasks

### Adding a New Chapter

1. Create `chapters/NN_title.tex` (numbered format)
2. Add `\include{chapters/NN_title}` in main.tex at appropriate location
3. Start with `\chapter{章节标题}` and `\label{ch:short_name}`
4. Compile twice to update TOC

### Checking Compilation

```bash
# Quick check for syntax errors
xelatex main.tex | grep -i error

# Check for font warnings
xelatex main.tex | grep -i "font"
```

### Viewing Output

The compilation produces `main.pdf` in the root directory.

## AI Workflow Context

This book specifically addresses working with AI coding assistants (mentioned in preface and Chapter 07). Key principles when suggesting AI-related content:

- **AI makes "working code" easier**: But not necessarily "trustworthy, traceable, reproducible research code"
- **AI failure modes**: Referenced in ai_disasters.tex appendix (e.g., code translation hallucinations, over-delegation)
- **Validation over generation**: The book emphasizes that the bottleneck is validation, not code generation

## References & Context

- **Author**: Li Hongmin (李鸿敏), Dept of Computational Biology, University of Tokyo
- **Target Audience**: ML/computational biology researchers in the AI era
- **Philosophy**: "Exploration can be wild, but outputs must be cleanable; conclusions can be tentatively fragile, but evidence chains must be solid."
