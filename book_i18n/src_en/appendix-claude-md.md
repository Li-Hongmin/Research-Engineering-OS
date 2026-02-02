# Appendix B: CLAUDE.md Template

Save the following content as `CLAUDE.md` in your project root. AI assistants will automatically follow these rules.

---

```markdown
# CLAUDE.md - Research Engineering Rules

## Project Info
- Project: [name]
- Language: Python
- Framework: PyTorch

## Core Principles

1. **Three Types of Debt**: Exploration debt (clean up prototypes), Validation debt (must test), Reproducibility debt (record environment)
2. **Six Experiment Elements**: Code version, Data version, Config, Environment, Results, Logs
3. **AI is an Assistant**: Generation can be fast, deployment must be slow; don't accept code you don't understand

## Directory Structure

```
src/           # Stable code (tested)
experiments/   # Experiment code (can be rough)
configs/       # Configuration files
tests/         # Tests
outputs/       # Output (don't commit)
data/          # Data (don't commit)
```

## Git Conventions

**Commit format**: `<type>: <description>`
- `feat:` New feature | `fix:` Bug fix | `exp:` Experiment | `refactor:` Refactoring

**Rules**:
- Each change ≤200 lines
- Separate feature and refactoring commits
- Don't modify main branch directly

## AI-Generated Code Rules

**Required**:
- [ ] Include verification method
- [ ] Human review of core logic (data processing, model, evaluation)
- [ ] Verify in experiment branch first

**Forbidden**:
- Mix feature + refactoring together
- Skip tests and merge directly

## Definition of Done (DoD)

- [ ] Results are reproducible
- [ ] Can explain why it works
- [ ] Fair comparison with baseline
- [ ] Has test coverage
- [ ] Config is recorded

## Weekly Check

- [ ] Key experiments can run
- [ ] Code is pushed
- [ ] Data is backed up
```

---

**Full version**: See Chapter 7 "AI-Era Workflow"
