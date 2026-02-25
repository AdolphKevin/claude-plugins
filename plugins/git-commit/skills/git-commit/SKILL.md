---
name: git-commit
description: Generate a clean commit with a well-formatted message, auto-update CHANGELOG, and track documentation consistency
---

# Commit Current Changes

Generates a clean commit with a properly formatted message, optionally auto-updates CHANGELOG, and validates documentation consistency.

## Usage

```bash
/git-commit                           # Auto-generate commit message
/git-commit --changelog               # Auto-generate + update CHANGELOG.md
/git-commit --check-docs              # Check docs consistency without committing
```

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

## ChangeLog Auto-Maintenance

**Trigger**: Use `--changelog` flag or commit message contains `feat`, `fix`, `perf`, `docs`

**Process**:
1. Detect if CHANGELOG.md exists in repository root
2. If exists, append entry in Unreleased section
3. If not exists, create new CHANGELOG.md with initial entry

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

**Trigger**: Any commit that modifies code files (`.go`, `.ts`, `.tsx`, `.js`, `.py`, etc.)

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

## Examples

```bash
# Auto-generate commit message
/git-commit

# Auto-generate commit message + update CHANGELOG
/git-commit --changelog

# Check docs consistency before committing
/git-commit --check-docs

# Commit with specific type
/git-commit feature

# Commit with custom message
/git-commit fix "Resolve memory leak in message handler"

# Commit with scope
/git-commit refactor conversation "Optimize message retrieval logic"

# Preview before committing
/git-commit --dry-run

# Full: dry-run + changelog + docs check
/git-commit --dry-run --changelog --check-docs
```

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
3. **Check documentation consistency** (if --check-docs or by default for code changes)
4. **Update CHANGELOG.md** (if --changelog flag present or type is feat/fix/docs/perf)
5. **IMPORTANT**: If using Flight Recorder, stage AI_CHANGELOG.md together with code BEFORE commit
6. Show the commit message for confirmation (unless --dry-run)
7. Create the commit with clean formatting (including AI_CHANGELOG.md if used)
8. Show a summary of what was committed
9. **NEVER add any Co-Authored-By or AI signatures**. The commit message should only contain the change description, nothing else.

## Red Flags - STOP and Reconsider

- Skipping --changelog for feature/fix/perf commits "because it's just a small change"
- Ignoring --check-docs warnings "I'll update docs later"
- Committing breaking API changes without documentation
- Adding new features without considering if docs need updates

**All of these mean: Use --changelog and --check-docs flags**

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
- CHANGELOG.md entries can auto-generate GitHub Releases
- Documentation consistency affects PR review quality
- Breaking changes should be marked in both CHANGELOG and docs

---

# Automatic Flight Recording (自动飞行记录仪)

## Rule: Record BEFORE Commit (not after!)

**CORRECT ORDER**:
1. Write your code changes
2. **Run log_change.py** to record the change in AI_CHANGELOG.md
3. **Stage AI_CHANGELOG.md** together with your code files: `git add docs/AI_CHANGELOG.md`
4. **Commit together**: `git commit -m "..."`

**WRONG ORDER (❌)**: Commit first, then record - this creates separate commits!

**WHEN** you have successfully modified any code logic (Feature, Bugfix, or Refactor):

1. **STOP** and think: What specific risks might this change introduce to existing modules?
2. **EXECUTE** the `~/.claude/skills/git-commit/scripts/log_change.py` script FIRST.
3. **Stage AI_CHANGELOG.md** with your code: `git add docs/AI_CHANGELOG.md`
4. **Commit together**: One commit contains both code and change log.

**GOAL**: Ensure `docs/AI_CHANGELOG.md` is always committed WITH your code changes.

## Flight Recorder Command

**Script Location**: `~/.claude/skills/git-commit/scripts/log_change.py` (shared across all projects)

```bash
# Step 1: Record the change FIRST
python ~/.claude/skills/git-commit/scripts/log_change.py <type> <summary> <risk_analysis>

# Step 2: Stage AI_CHANGELOG.md together with your code
git add docs/AI_CHANGELOG.md
git add <your-code-files>

# Step 3: Commit together
git commit -m "Your commit message"

# Example:
python ~/.claude/skills/git-commit/scripts/log_change.py Feature "Add timeline index optimization" "May affect existing queries performance"
git add docs/AI_CHANGELOG.md protos/conversation/conversation.proto
git commit -m "feat(conversation): Add timeline message jump support"
```

## Correct Commit Flow

```
1. Modify code files
2. Run: python ~/.claude/skills/git-commit/scripts/log_change.py Feature "Add feature" "Risk..."
3. Run: git add docs/AI_CHANGELOG.md <your-files>
4. Run: git commit -m "feat: Add feature"
   ↓
Single commit contains:
  - Your code changes
  - AI_CHANGELOG.md entry
```

## ChangeLog Format

The script generates entries in this format:
```markdown
## [2026-02-25 14:31] [Feature] ✨

- **Change**: Add timeline index optimization
- **Risk Analysis**: May affect existing queries performance

---
```

## AI_CHANGELOG.md Location

- **Path**: `docs/AI_CHANGELOG.md` (in each project directory where you run the script)
- **Generated by**: `~/.claude/skills/git-commit/scripts/log_change.py`
- **Commit with**: Always commit this file along with your code changes

## Why Risk Analysis Matters

The risk analysis field is the most important because it:
- Forces you to think about side effects before committing
- Creates a historical record for debugging future issues
- Helps team members understand potential problems
- Enables better code review discussions

**If you can't write a risk analysis, you don't understand the change well enough to commit it.**
