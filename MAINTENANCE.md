# MAINTENANCE.md - Project Maintenance Guide

**Created**: 2026-02-09 13:06 JST  
**Purpose**: Guide for project maintainers and automated maintenance workflows

---

## 🔄 Daily Maintenance Workflow

### Automated Health Checks (Hourly)
The project runs automated health checks via cron every hour:
```bash
make health
```

**What it checks**:
- ✅ Git working tree status
- ✅ Git synchronization with remote
- ✅ text-book builds (zh/en/ja)
- ✅ manga-book build
- ✅ Image assets integrity
- ✅ Core documentation completeness
- ✅ Dependencies installation

**Expected output**: `✅ Project health: EXCELLENT`

### Manual Health Check (When needed)
```bash
# Full health check
make health

# Specific checks
./check_health.sh              # Comprehensive check
./check_links.sh               # Link validation
./check_manga_images.sh        # Manga image paths
./check_markdown_lint.sh       # Markdown formatting
./check_translation_sync.sh    # Translation consistency
./check_content_consistency.sh # Content alignment
./check_architecture.sh        # Architecture validation
```

---

## 📊 Weekly Reporting

### Generate Weekly Report
```bash
# Auto-generate weekly activity report
./generate_weekly_report.sh

# Output location
reports/weekly-report-YYYY-MM-DD.md
```

**Report includes**:
- Commit statistics (7-day window)
- Contributor activity
- File modification summary
- Lines added/deleted
- Top modified files

**Recommended schedule**: Every Monday morning (JST)

---

## 🏗️ Build & Deployment

### Local Builds
```bash
# Build all books
make build

# Build specific book
cd text-book && mdbook build
cd manga-book && mdbook build

# Clean builds
make clean
```

### Deployment (GitHub Pages)
Automatic on push to `main` via GitHub Actions:
- `.github/workflows/deploy.yml` handles:
  - text-book (zh/en/ja)
  - manga-book (multi-language)
  
**Verify deployment**:
```bash
# Check deployment status
curl -I https://[your-username].github.io/Research-Engineering-OS-/
curl -I https://[your-username].github.io/Research-Engineering-OS-/manga/
```

---

## 🔍 Quality Assurance

### Pre-Commit Checks
Git pre-commit hook (`.git/hooks/pre-commit`) automatically runs:
```bash
./check_health.sh
```

**To bypass** (not recommended):
```bash
git commit --no-verify
```

### CI/CD Pipeline
GitHub Actions run on every PR/push:
1. **Markdown Lint** - Checks formatting, HTML tags, trailing spaces
2. **Link Validation** - Verifies internal/external links
3. **Build Test** - Ensures all books compile successfully
4. **Image Check** - Validates manga image paths

**View CI logs**:
- GitHub → Actions tab
- Check failed runs for details

---

## 📝 Content Updates

### Adding New Chapters
1. **text-book**:
   ```bash
   # Add to all three languages
   vim text-book/src/XX-new-chapter.md
   vim text-book/src_en/XX-new-chapter.md
   vim text-book/src_ja/XX-new-chapter.md
   
   # Update SUMMARY.md (all 3 versions)
   vim text-book/src/SUMMARY.md
   vim text-book/src_en/SUMMARY.md
   vim text-book/src_ja/SUMMARY.md
   ```

2. **manga-book**:
   ```bash
   # Create chapter directory with images
   mkdir -p manga-book/images/XX-chapter-name/
   
   # Add markdown files (all languages)
   vim manga-book/src/XX-chapter-name.md
   vim manga-book/src_en/XX-chapter-name.md
   vim manga-book/src_ja/XX-chapter-name.md
   
   # Update SUMMARY.md (all 3 versions)
   ```

3. **Verify synchronization**:
   ```bash
   ./check_translation_sync.sh
   ./check_content_consistency.sh
   ```

### Updating Translations
```bash
# Use translation tools (if available)
python translate_manga_azure_batch.py --input src/ --output src_ja/ --target ja
python translate_manga_azure_batch.py --input src/ --output src_en/ --target en

# Manual review required after auto-translation
```

---

## 🐛 Troubleshooting

### Build Failures

**Symptom**: `mdbook build` fails  
**Common causes**:
1. Unclosed HTML tags in markdown
   ```bash
   ./check_markdown_lint.sh
   ```
2. Broken image links
   ```bash
   ./check_manga_images.sh
   ```
3. Invalid SUMMARY.md structure
   - Check chapter order
   - Verify file paths

**Fix**:
```bash
# Identify issue
make health

# Fix specific problem
# ... (edit files) ...

# Verify fix
mdbook build
make health
```

### Git Sync Issues

**Symptom**: Local/remote out of sync  
**Solution**:
```bash
# Check status
git status
git fetch origin

# If behind
git pull --rebase origin main

# If diverged (careful!)
git log --oneline --graph --all
# Resolve manually or contact team
```

### Image Path Issues

**Symptom**: Images not displaying in builds  
**Common causes**:
- Incorrect relative paths
- Renamed files not updated in markdown
- Case sensitivity (manga-book vs Manga-Book)

**Debug**:
```bash
./check_manga_images.sh --verbose
./check_links.sh
```

**Fix**:
```bash
# Find broken references
grep -r "!\[.*\](.*images.*)" manga-book/src*/

# Update paths (be careful with regex)
# Use editor's find/replace or manual edit
```

---

## 📦 Dependency Management

### mdBook Installation
```bash
# macOS (Homebrew)
brew install mdbook

# Cargo (all platforms)
cargo install mdbook

# Verify
mdbook --version
```

### Python Dependencies (if using translation tools)
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt  # (if exists)
```

---

## 🗂️ File Organization

### Archive Management
Old STATUS.md versions are archived monthly:
```bash
# Archive current STATUS
cp STATUS.md archive/STATUS-$(date +%Y-%m-%d).md

# Keep last 3 months of archives
ls -t archive/STATUS-*.md | tail -n +4 | xargs rm
```

### Report Management
Weekly reports accumulate in `reports/`:
```bash
# Clean old reports (keep last 8 weeks)
ls -t reports/weekly-report-*.md | tail -n +9 | xargs rm
```

---

## 🚨 Emergency Procedures

### Rollback Bad Commit
```bash
# If not pushed
git reset --hard HEAD~1

# If pushed (create revert)
git revert <commit-hash>
git push origin main
```

### Restore from Archive
```bash
# If STATUS.md corrupted
cp archive/STATUS-<date>.md STATUS.md

# If build corrupted
make clean
make build
```

### Contact Information
- **Project Lead**: [Contact info or GitHub handle]
- **CI/CD Issues**: Check GitHub Actions logs
- **Documentation**: See CONTRIBUTING.md, README.md

---

## 📅 Maintenance Schedule

### Hourly (Automated)
- [x] Health check via cron
- [x] Auto-commit STATUS.md updates

### Daily
- [ ] Review CI/CD failures (if any)
- [ ] Check GitHub Issues/PRs
- [ ] Monitor build status

### Weekly
- [ ] Generate weekly report
- [ ] Review and merge PRs
- [ ] Update TODO.md priorities
- [ ] Check translation synchronization

### Monthly
- [ ] Archive old STATUS.md
- [ ] Clean old reports (keep 8 weeks)
- [ ] Review and update documentation
- [ ] Dependency updates (mdbook, etc.)
- [ ] Security audit (if applicable)

### Quarterly
- [ ] Content review (CONTENT_REVIEW_CHECKLIST.md)
- [ ] Architecture validation
- [ ] Performance optimization
- [ ] User feedback integration

---

## 🎯 Maintenance Metrics

Track these to ensure project health:

| Metric | Target | Command |
|--------|--------|---------|
| Health Status | EXCELLENT | `make health` |
| Build Success Rate | 100% | GitHub Actions |
| Broken Links | 0 | `./check_links.sh` |
| Translation Sync | 100% | `./check_translation_sync.sh` |
| Commit Frequency | Daily | `git log --oneline --since="7 days ago"` |
| Documentation Coverage | Complete | `./project_stats.sh` |

---

## 📚 Reference Documents

- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community standards
- [TODO.md](TODO.md) - Task tracking
- [STATUS.md](STATUS.md) - Current project status
- [FAQ.md](FAQ.md) - Common questions and answers
- [CONTENT_REVIEW_CHECKLIST.md](CONTENT_REVIEW_CHECKLIST.md) - Quality assurance
- [DOCS_INDEX.md](DOCS_INDEX.md) - Documentation index

---

## 🤖 Automation Notes

### REOS Principles
This project follows Research Engineering OS (REOS) principles:
1. **Small steps, fast iterations** - Hourly progress increments
2. **Traceability** - All changes documented in STATUS.md
3. **Automation first** - Scripts > manual work
4. **Non-breaking changes** - Incremental improvements only
5. **Documentation** - Record everything

### Cron Jobs
Hourly maintenance is handled by OpenClaw cron:
- Job ID: `18a968ff-0a8e-4293-8a6e-74030356c261`
- Schedule: Every hour
- Session: isolated
- Payload: agentTurn with maintenance instructions

**To check cron status** (if using OpenClaw):
```bash
# Via OpenClaw CLI (if available)
openclaw cron list
openclaw cron runs --jobId 18a968ff-0a8e-4293-8a6e-74030356c261
```

---

**Last Updated**: 2026-02-09 13:06 JST  
**Maintainer**: REOS Agent (YunQiAI)  
**Next Review**: Monthly or as needed
