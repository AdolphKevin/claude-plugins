---
name: git-commit
description: Use when committing staged code changes and need auto-generated commit messages with AI_CHANGELOG updates
---

# Git Commit

Generates a clean commit with properly formatted message and automatically updates AI_CHANGELOG.md.

## Usage

```bash
/git-commit
```

**No manual parameters needed** - the skill automatically analyzes staged changes to determine:
- **Type**: Feature, Bugfix, Refactor, Critical-Fix, Docs, Perf
- **Summary**: Brief description of the change
- **Risk**: Why this change is safe or what to watch out for

## Workflow

1. **Stage your code files first**: `git add <files>` (do this BEFORE running the skill)
2. **Run `/git-commit`** - the skill automatically:
   - Analyzes staged changes
   - Determines appropriate type, summary, and risk level
   - Runs `log_change.py` to write entry to `docs/AI_CHANGELOG.md`:
     - If `docs/AI_CHANGELOG.md` doesn't exist: create it then append entry
     - If `docs/AI_CHANGELOG.md` exists: **prepend** entry to the **top** of the file
   - **Only if** log_change.py succeeds:
     - `git add docs/AI_CHANGELOG.md` (only this file, not other staged files)
   - Generate commit message from **staged changes** (which is now just AI_CHANGELOG.md)
   - Create the commit

## log_change.py Script Usage

The script supports TWO formats - use whichever is clearer:

### Format 1: Positional arguments (recommended)
```bash
python skills/git-commit/scripts/log_change.py <type> <summary> <risk_analysis>
```

### Format 2: Flag arguments
```bash
python skills/git-commit/scripts/log_change.py --type <type> --change <summary> --risk <risk_analysis>
```

**Example (positional):**
```bash
python skills/git-commit/scripts/log_change.py Feature "Add cursor-based pagination" "Uses efficient composite index"
```

**Example (flags):**
```bash
python skills/git-commit/scripts/log_change.py --type Feature --change "Add cursor-based pagination" --risk "Uses efficient composite index"
```

**⚠️ VALID types (must match exactly):**
- `Feature` - New feature
- `Bugfix` - Bug fix
- `Refactor` - Code refactoring
- `Critical-Fix` - Critical bug fix
- `Docs` - Documentation changes
- `Perf` - Performance improvements

**❌ WRONG types (will cause error):**
- `Fix`, `fix` - Must use `Bugfix`

## Key Behavior

**Important:**
- AI_CHANGELOG.md is **ONLY staged** if log_change.py successfully writes content to it
- After staging AI_CHANGELOG.md, **only that file is staged** (original staged files are not included in the commit)
- Commit message is generated from the staged changes (AI_CHANGELOG.md diff)

## Available Types

**⚠️ Use EXACTLY these types (case-sensitive):**

| Type | Description |
|------|-------------|
| `Feature` | New feature or functionality |
| `Bugfix` | Bug fix |
| `Refactor` | Code refactoring without changing behavior |
| `Critical-Fix` | Critical/security bug fix |
| `Docs` | Documentation changes |
| `Perf` | Performance improvements |

## Commit Message Format

The generated commit follows this format:
```
[Type](scope): Subject

Body explaining the changes in detail.

- Key point 1
- Key point 2
- Technical details
```

## Documentation Consistency Check

**Trigger**: Runs on every commit that modifies code files (`.go`, `.ts`, `.tsx`, `.js`, `.py`, etc.)

**Check Rules**:
| Code Changed | Documentation Status     | Action                                                 |
| ------------ | ------------------------ | ------------------------------------------------------ |
| `.go` files  | No corresponding docs    | WARN: Consider adding code comments or updating README |
| API changes  | No proto docs updated    | WARN: API changed but documentation not updated        |
| New feature  | No feature docs          | WARN: New feature without documentation                |
| Bug fix      | Related docs not updated | WARN: Bug fixed but docs reflect old behavior          |

**Warning Levels**:
- **ERROR**: Breaking API changes without documentation
- **WARN**: New features without documentation updates
- **INFO**: Code refactoring - documentation still accurate

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
