# Contributing to Research Engineering OS

Thank you for your interest in contributing to **Research Engineering OS**! 🎉

This project aims to teach practical research engineering practices through two complementary formats:
- **text-book**: Multilingual technical guide (Chinese/English/Japanese)
- **manga-book**: Visual story-driven manga edition (Chinese)

We welcome contributions from researchers, engineers, educators, translators, and illustrators.

---

## 🌟 Ways to Contribute

### 1. Content Improvements
- **Fix typos, grammar, or unclear explanations**
- **Add practical examples** from your research experience
- **Suggest missing topics** in research engineering
- **Improve code examples** for better clarity or correctness

### 2. Translation
- **Maintain consistency** across Chinese/English/Japanese versions
- **Improve existing translations** for accuracy or natural phrasing
- **Add translations** for newly added content
- See [Translation Guide](#translation-workflow) below

### 3. Illustrations & Visual Design
- **Manga panels** for manga-book (Chinese visual edition)
- **Diagrams and figures** for technical concepts
- **UI/UX improvements** for web interface

### 4. Quality Assurance
- **Report broken links** or missing images
- **Test build processes** on different platforms
- **Run automated checks** and fix issues
- See [Quality Checks](#quality-checks) below

### 5. Community & Discussion
- **Share your experience** using REOS principles in real research
- **Answer questions** in GitHub Discussions or Issues
- **Spread the word** on social media or conferences

---

## 🚀 Getting Started

### Prerequisites
- **Git** for version control
- **mdBook** for building documentation
  ```bash
  cargo install mdbook
  # or via package manager (Homebrew, apt, etc.)
  ```
- **Python 3.x** (optional, for translation scripts)
- **Rust toolchain** (optional, for mdBook plugins)

### Fork & Clone
```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/Research-Engineering-OS-.git
cd Research-Engineering-OS-

# 3. Add upstream remote
git remote add upstream https://github.com/li-hongmin/Research-Engineering-OS-.git

# 4. Create a feature branch
git checkout -b feature/your-feature-name
```

### Build Locally

#### Text Book (All Languages)
```bash
cd text-book
./build_all.sh          # Build Chinese + English + Japanese
cd book && python -m http.server 8000
# Open http://localhost:8000
```

#### Manga Book
```bash
cd manga-book
mdbook build
cd book && python -m http.server 8000
# Open http://localhost:8000
```

---

## 📝 Contribution Workflow

### 1. Create an Issue (Optional but Recommended)
Before making significant changes, create an issue to discuss:
- What you want to add or fix
- Why it's needed
- How you plan to implement it

This helps avoid duplicate work and ensures alignment with project goals.

### 2. Make Your Changes
- **Follow existing style** (see [Style Guide](#style-guide) below)
- **Keep commits small and focused** (one logical change per commit)
- **Write clear commit messages** (see [Commit Guidelines](#commit-guidelines))

### 3. Run Quality Checks
Before committing, run automated checks:
```bash
# Health check (structure, paths, consistency)
./check_health.sh

# Markdown lint (HTML tags, formatting)
./check_markdown_lint.sh

# Link validation
./check_links.sh --fast  # Quick check for text-book + manga-book

# Manga image paths (manga-book only)
./check_manga_images.sh

# Translation sync (text-book only)
./check_translation_sync.sh
```

**Pre-commit Hook**: `check_health.sh` runs automatically before each commit.

### 4. Test Your Changes
- **Build the book** locally and verify changes render correctly
- **Check for broken links** or missing images
- **Test on multiple browsers** if you changed UI/CSS

### 5. Submit a Pull Request
```bash
# Commit your changes
git add .
git commit -m "docs: improve DoD chapter with real-world example"

# Push to your fork
git push origin feature/your-feature-name

# Open a Pull Request on GitHub
```

#### Pull Request Checklist
- [ ] PR title follows [Conventional Commits](#commit-guidelines)
- [ ] Description explains **what** and **why** (not just how)
- [ ] All automated checks pass (GitHub Actions CI)
- [ ] Changes tested locally (build + preview)
- [ ] Related issues linked (e.g., "Fixes #123")
- [ ] Screenshots/GIFs included for UI changes

---

## 📐 Style Guide

### Markdown
- **Headings**: Use ATX-style (`#`, `##`, etc.)
- **Lists**: Consistent indentation (2 spaces)
- **Code blocks**: Always specify language (````bash`, ```python`, etc.)
- **Links**: Use reference-style for repeated URLs
- **Images**: Include descriptive `alt` text

### Code Examples
- **Runnable**: Code should work copy-paste (or explain if conceptual)
- **Commented**: Add brief comments for non-obvious parts
- **Realistic**: Use realistic file names, paths, and data
- **Self-contained**: Avoid dependencies on unlisted files

### Terminology
Use consistent terms across languages. See `GLOSSARY.md` for key terms:
- **Definition of Done (DoD)** → 完成的定义 → 完了の定義
- **Technical Debt** → 技术债务 → 技術的負債
- **Reproducibility** → 可重现性 → 再現性

---

## 🌍 Translation Workflow

### Adding Translations
1. **Check existing translations** in `GLOSSARY.md` for consistency
2. **Translate content** in the appropriate directory:
   - English: `text-book/src_en/`
   - Japanese: `text-book/src_ja/`
3. **Update SUMMARY.md** in the language directory
4. **Run sync check**:
   ```bash
   ./check_translation_sync.sh
   ```

### Translation Principles
- **Accuracy over literalness**: Convey meaning, not word-by-word translation
- **Natural phrasing**: Use idiomatic expressions in target language
- **Technical terms**: Follow `GLOSSARY.md` or academic conventions
- **Code comments**: Translate comments; keep code syntax unchanged

### Batch Translation (Azure AI)
For large updates, use the batch translation script:
```bash
cd text-book
python translate_manga_azure_batch.py --source src/ --target src_en/ --lang en
```
**Note**: Always review and refine AI-generated translations.

---

## 🧪 Quality Checks

### Automated Checks (Must Pass)
- **Health Check**: Structure, paths, file consistency
- **Markdown Lint**: Unclosed HTML tags, formatting issues
- **Link Validation**: Broken internal/external links
- **Translation Sync**: Chapter structure across languages

### Manual Review (Recommended)
See `CONTENT_REVIEW_CHECKLIST.md` for comprehensive review areas:
- Terminology consistency
- Code example quality
- Citation completeness
- Image quality and alt text
- Narrative coherence (manga-book)

---

## 📋 Commit Guidelines

Use **[Conventional Commits](https://www.conventionalcommits.org/)** format:
```
<type>(<scope>): <subject>

<body> (optional)
<footer> (optional)
```

### Types
- `feat`: New content, chapter, or feature
- `fix`: Fix typos, errors, or broken links
- `docs`: Documentation improvements (README, CONTRIBUTING, etc.)
- `style`: Formatting, whitespace (no content change)
- `refactor`: Restructure without changing content
- `test`: Add or update tests/checks
- `chore`: Maintenance, build scripts, dependencies

### Examples
```bash
git commit -m "feat(text-book): add section on experiment traceability"
git commit -m "fix(manga-book): correct image path in chapter 05"
git commit -m "docs: update translation workflow in CONTRIBUTING.md"
git commit -m "chore: add pre-commit hook for health checks"
```

---

## 🛠️ Development Tools

### Useful Scripts
| Script | Purpose |
|--------|---------|
| `check_health.sh` | Validate project structure |
| `check_markdown_lint.sh` | Detect Markdown issues |
| `check_links.sh` | Verify link validity |
| `check_manga_images.sh` | Check manga image references |
| `check_translation_sync.sh` | Ensure translation consistency |
| `translate_manga_azure_batch.py` | Batch translation (Azure AI) |

### GitHub Actions CI/CD
Automated checks run on every push/PR:
1. **Health Check**: `check_health.sh`
2. **Markdown Lint**: `check_markdown_lint.sh`
3. **Build Test**: All mdBook builds succeed
4. **Deployment**: Publish to GitHub Pages (on `main` branch)

See `.github/workflows/` for details.

---

## 🤝 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level (student, researcher, engineer)
- Background (academia, industry, self-taught)
- Identity (age, gender, ethnicity, etc.)

### Expected Behavior
- **Be respectful** in discussions and code reviews
- **Assume good intent** when interpreting feedback
- **Give constructive feedback** (focus on content, not person)
- **Welcome newcomers** and help them get started

### Unacceptable Behavior
- Harassment, discrimination, or personal attacks
- Trolling, insulting, or derogatory comments
- Publishing others' private information without permission
- Other conduct inappropriate in a professional/educational setting

**Enforcement**: Violations can be reported to the maintainers. We reserve the right to remove, edit, or reject contributions that violate this Code of Conduct.

---

## 💬 Communication Channels

### GitHub Issues
- **Bug reports**: Use the issue template
- **Feature requests**: Describe use case and benefits
- **Questions**: Ask in Discussions (preferred) or Issues

### GitHub Discussions
- **General questions**: About using REOS principles
- **Show & Tell**: Share your research engineering stories
- **Ideas**: Propose new topics or features

### Pull Requests
- **For code/content changes**: Always preferred over Issues for concrete changes
- **Reference related Issues**: Use "Fixes #123" or "Closes #456"

---

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the **MIT License** (see `LICENSE` file).

- **You retain copyright** of your contributions
- **You grant permission** for the project to use/modify your contributions
- **Attribution**: Contributors are listed in git history and may be acknowledged in releases

---

## 🙏 Acknowledgments

Thank you to all contributors who help make research engineering practices more accessible!

- **Content contributors**: Adding chapters, examples, and translations
- **Quality reviewers**: Finding bugs, broken links, and inconsistencies
- **Community members**: Sharing stories, asking questions, and spreading the word

Your contributions, big or small, make a difference. 🌟

---

**Questions?** Open an issue or start a discussion on GitHub. We're here to help!

**Ready to contribute?** Fork the repo and start building! 🚀
