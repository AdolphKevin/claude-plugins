---
name: git-commit
description: Generate clean commits with well-formatted messages, auto-update AI_CHANGELOG, and validate documentation consistency. Use this skill whenever committing code changes.
---

# Commit Current Changes

Generates a clean commit with a properly formatted message, automatically updates AI_CHANGELOG, and validates documentation consistency on every run.

## Usage

```bash
/git-commit                           # Auto-generate commit message, update AI_CHANGELOG, check docs
```

**Note**: Simply run `/git-commit` with no arguments. The command automatically:

1. Checks staged changes
2. Analyzes the changes
3. **Automatically runs log_change.py to record in AI_CHANGELOG**
4. **Checks documentation consistency**
5. Generates commit message and creates the commit

## Available Types

- **Feature**: New feature or functionality
- **Fix**: Bug fix
- **Refactor**: Code refactoring without changing behavior
- **Docs**: Documentation changes
- **Test**: Adding or updating tests
- **Chore**: Maintenance tasks, dependency updates
- **Perf**: Performance improvements
- **Style**: Code style changes (formatting, etc.)
- **CI**: CI/CD related changes
- **Build**: Build system or dependency changes

**ChangeLog Format**:
```markdown
## [Unreleased]

### Added
- feature: Add new message handler (2026-02-25)

### Fixed
- fix: Resolve memory leak in connection pool (2026-02-25)
```

**Entry Format**: `{type}: {subject} ({date})`

## Documentation Consistency Check

**Trigger**: Always runs on every commit that modifies code files (`.go`, `.ts`, `.tsx`, `.js`, `.py`, etc.)

**Check Rules**:
| Code Changed | Documentation Status     | Action                                                 |
| ------------ | ------------------------ | ------------------------------------------------------ |
| `.go` files  | No corresponding docs    | WARN: Consider adding code comments or updating README |
| API changes  | No proto docs updated    | WARN: API changed but documentation not updated        |
| New feature  | No feature docs          | WARN: New feature without documentation                |
| Bug fix      | Related docs not updated | WARN: Bug fixed but docs reflect old behavior          |

**Documentation Types to Check**:
- README.md
- CLAUDE.md
- docs/*.md
- API documentation (proto comments)
- Inline code comments for public APIs

**Warning Levels**:
- **ERROR**: Breaking API changes without documentation
- **WARN**: New features without documentation updates
- **INFO**: Code refactoring - documentation still accurate

## Commit Message Format

The generated commit follows this format:
```
[Type](scope): Subject

Body explaining the changes in detail.

- Key point 1
- Key point 2
- Technical details
```

The command will:
1. Check if there are staged changes
2. Analyze the changes and generate a meaningful commit message
3. **Automatically run log_change.py to update AI_CHANGELOG.md**
4. **Check documentation consistency** (always enabled for code changes)
5. Stage AI_CHANGELOG.md together with your code files
6. Show the commit message for confirmation (unless --dry-run)
7. Create the commit with clean formatting (including AI_CHANGELOG.md)
8. Show a summary of what was committed
9. **NEVER add any Co-Authored-By or AI signatures**. The commit message should only contain the change description, nothing else.

## Red Flags - STOP and Reconsider

- Ignoring documentation warnings with "I'll update docs later"
- Committing breaking API changes without documentation
- Adding new features without considering if docs need updates

## Common Rationalizations

| Excuse                                      | Reality                                    |
| ------------------------------------------- | ------------------------------------------ |
| "Small change, no need for changelog"       | Every change should be traceable           |
| "I'll update docs later"                    | Later = never                              |
| "This is just a refactor, docs don't apply" | Internal APIs may have public contracts    |
| "Tests don't need documentation"            | Test structure documents expected behavior |
| "The code is self-explanatory"              | Future you won't remember                  |

## Integration with GitHub

When repository has GitHub integration:
- AI_CHANGELOG.md entries can auto-generate GitHub Releases
- Documentation consistency affects PR review quality
- Breaking changes should be marked in both AI_CHANGELOG and docs

---

# Automatic Flight Recording

## Rule: Automatic Recording

**Everything happens automatically when you run `/git-commit`**:
1. Analyzes staged changes
2. Automatically determines change type and summary
3. Automatically runs log_change.py to record in AI_CHANGELOG.md
4. Automatically stages AI_CHANGELOG.md
5. Creates a single commit containing both code and changelog

**Just run `/git-commit` - everything else is automatic!**

## Flight Recorder Command

**Script Location**: `{SKILL_DIR}/scripts/log_change.py` (shared across all projects)

```bash
# Just run this one command!
/git-commit

# Internally executes:
# 1. Analyzes staged changes
# 2. Generates change type and summary
# 3. Runs log_change.py to record change
# 4. Stages AI_CHANGELOG.md
# 5. Creates commit
```

## Correct Commit Flow

```
1. Modify code files
2. Run: /git-commit
   ↓
Single commit contains:
  - Your code changes
  - AI_CHANGELOG.md entry
  - Documentation consistency check
```

## ChangeLog Format

Auto-generated entry format:
```markdown
## [2026-02-25 14:31] [Feature] ✨

- **Change**: Add timeline index optimization
- **Risk Analysis**: May affect existing queries performance

---
```

## AI_CHANGELOG.md Location

- **Path**: `docs/AI_CHANGELOG.md` (in each project directory)
- **Generated by**: `{SKILL_DIR}/scripts/log_change.py` (runs automatically)
- **Commit with**: Automatically committed with your code

## Why Risk Analysis Matters

The risk analysis field is the most important because it:
- Forces you to think about side effects before committing
- Creates a historical record for debugging future issues
- Helps team members understand potential problems
- Enables better code review discussions

**If you can't write a risk analysis, you don't understand the change well enough to commit it.**
