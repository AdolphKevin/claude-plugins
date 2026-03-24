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

**Required before running**: Stage your code files with `git add <files>`

## Step 1: Analyze Staged Changes
Run `git diff --cached --stat` to see what files are staged.

### Step 2: Infer Commit Details
**Automatically determine from the diff:**

- **Change type**: Infer from file paths and diff content:
  - `docs/*.md`, `*.md` changes → `Docs`
  - `cmd/`, `internal/`, `pkg/` with new functionality → `Feature`
  - `fix`, `bug`, `hotfix` in messages → `Bugfix` or `Critical-Fix`
  - `refactor`, `rename`, `extract` → `Refactor`
  - `perf`, `optimize`, `faster` → `Perf`
  - Default to `Feature` if ambiguous

- **Summary**: Generate from the most meaningful changed files/functions. Focus on *what changed* not *how*.

- **Risk Analysis**: Evaluate:
  - Scope of changes (small = low risk, wide = higher risk)
  - Whether critical paths are affected (auth, payment, data)
  - If tests are included
  - Breaking API changes

### Step 3: Run log_change.py
The script auto-detects the project root via git. Run from any subdirectory.

```bash
python <skill_dir>/scripts/log_change.py <type> <summary> <risk_analysis>
```

**Example:**
```bash
python ~/.claude/skills/git-commit/scripts/log_change.py Feature "Add cursor-based pagination" "Uses efficient composite index, no breaking changes"
```

### Step 4: Stage AI_CHANGELOG.md
```bash
git add docs/AI_CHANGELOG.md
```

### Step 5: Create Commit WITHOUT Co-Authored-By or Signed-off-by
Use plain `git commit` (without `-s` or `-a` flags):

```bash
git commit -m "[Type](scope): Subject

Body explaining the changes in detail.

- Specific key point derived from actual diff
- Another specific key point from the changes
- Technical implementation detail from the code

Risk: <risk_analysis from Step 2>"
```

**⚠️ CRITICAL: Replace placeholder bullets with actual content from the diff. Never use literal placeholders like "Key point 1" - extract specific details from what actually changed.**

**Important**: Do NOT use the Co-Authored-By line or Signed-off-by line. The commit should only contain the message body above.

## log_change.py Script

The script auto-detects project root and finds `docs/AI_CHANGELOG.md`. Supports TWO formats:

### Format 1: Positional arguments (recommended)
```bash
python ~/.claude/skills/git-commit/scripts/log_change.py <type> <summary> <risk_analysis>
```

### Format 2: Flag arguments
```bash
python ~/.claude/skills/git-commit/scripts/log_change.py --type <type> --change <summary> --risk <risk_analysis>
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

- Specific key point from the diff
- Another specific key point from changes
- Concrete technical detail from code

Risk: <risk_analysis from Step 2>
```

**⚠️ Never use literal placeholders. Always extract real content from the diff.**
