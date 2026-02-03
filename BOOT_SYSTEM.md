# CPU Boot System - Recovery Protocol

**Mount persistent artifacts before letting volatile interpretation run.**

## Overview

The CPU Boot System is a deterministic state restoration tool that helps you recover context and confidence when returning to a project. It's your brain's "GitHub screenshot recovery" but automated.

## The Problem It Solves

When you return to a project after a break, you often experience:
- Uncertainty about what you were working on
- Lost context about project state
- Need to manually scan through commits and files
- "Impostor syndrome" or confidence loss

The Boot System solves this by automatically:
1. Loading "truth artifacts" (git stats, recent changes, key docs)
2. Generating a one-page digest
3. Writing BOOT_REPORT.md
4. Setting CONFIDENCE_OK flag based on repo state

## Quick Start

### Installation

The boot system is already installed. It's in the `cpu/` directory and uses only Python standard library (zero external dependencies).

### Basic Usage

**Full boot digest** (loads anchor docs, analyzes repo):
```bash
python -m cpu doctor
```

**Fast mode** (git stats only, <1 second):
```bash
python -m cpu panic
# or
python -m cpu doctor --fast
```

**Console only** (don't write BOOT_REPORT.md):
```bash
python -m cpu doctor --no-report
```

## Output Example

```
======================================================================
SAGCO BOOT DIGEST
======================================================================
Timestamp: 2026-02-03 18:03:29
Repo: Sovereignty-Architecture-Elevator-Pitch-
Branch: copilot/implement-boot-time-self-linking
Commits: 2
Last commit: 2026-02-03
  └─ Initial plan
Local branches: 1
Files changed (7 days): 0
Recent modules: promptsvc.py, worker.py, antibody_system.py
Anchors loaded: README.md, BOOT_RECON.md, DEPLOYMENT.md
STATUS: CONFIDENCE_OK
======================================================================

Next action: Review recent changes and continue development
```

## Configuration

Edit `boot_manifest.json` to customize what the boot system loads:

```json
{
  "version": "BOOT-MANIFEST-1.0",
  "anchors": [
    "README.md",
    "BOOT_RECON.md",
    "DEPLOYMENT.md"
  ],
  "globs": [
    "docs/**/*.md"
  ],
  "max_files": 25,
  "max_chars_per_file": 12000
}
```

### Configuration Options

- **anchors**: List of specific files to always load (high-signal docs)
- **globs**: Pattern-based file loading (currently not fully implemented)
- **max_files**: Maximum number of files to load
- **max_chars_per_file**: Character limit per file to avoid overload

## Recovery Protocol

When you feel that wobble of uncertainty:

1. **Run panic mode first**: `python -m cpu panic`
   - Ultra-fast (<1 second)
   - Shows basic git stats
   - Restores baseline confidence

2. **If you need more context**: `python -m cpu doctor`
   - Loads anchor documents
   - Shows recent modules
   - Generates full BOOT_REPORT.md
   - Takes 2-5 seconds

3. **Read BOOT_REPORT.md**
   - Persistent snapshot of repo state
   - Includes recovery checklist
   - Can be committed or ignored

## How It Works

### Boot Pipeline

```
BOOT
 ├─ Locate repo root (walks up for .git)
 ├─ Read boot_manifest.json
 ├─ Compute git metrics
 │   ├─ Commit count
 │   ├─ Last commit time & message
 │   ├─ Current branch
 │   ├─ Local branch count
 │   ├─ Files changed last 7 days
 │   └─ Recent Python modules
 ├─ Load anchor docs (if not fast mode)
 ├─ Render boot digest
 └─ Write BOOT_REPORT.md (if not disabled)
```

### Key Design Principles

1. **Zero dependencies**: Uses only Python stdlib + git
2. **Fast by default**: Panic mode runs in <1 second
3. **Deterministic**: Same repo state = same output
4. **Non-invasive**: Doesn't modify your code or git history
5. **Git-native**: Works entirely through git commands

## Commands

### `doctor` - Full Boot Digest

Comprehensive system check with document loading.

```bash
python -m cpu doctor              # Full analysis + BOOT_REPORT.md
python -m cpu doctor --fast       # Skip docs, faster
python -m cpu doctor --no-report  # Console only
```

**When to use:**
- Returning to project after days/weeks
- Need to understand current phase
- Want persistent snapshot (BOOT_REPORT.md)

### `panic` - Emergency Recovery

Ultra-fast confidence restoration (<1 second).

```bash
python -m cpu panic
```

**When to use:**
- Feeling lost or uncertain
- Need immediate context
- Don't want to wait for doc loading

## Integration Ideas

### Add to Git Hooks

Run boot digest after checkout:

```bash
# .git/hooks/post-checkout
#!/bin/bash
python -m cpu panic
```

### Add to Shell Prompt

Show confidence status in your prompt:

```bash
# .bashrc or .zshrc
function sagco_status() {
    python -m cpu panic --no-report 2>/dev/null | grep STATUS | cut -d: -f2
}
```

### VS Code Task

Add to `.vscode/tasks.json`:

```json
{
  "label": "SAGCO Boot Check",
  "type": "shell",
  "command": "python -m cpu doctor",
  "presentation": {
    "echo": true,
    "reveal": "always",
    "panel": "new"
  }
}
```

## Files

- **cpu/boot_digest.py**: Main boot system implementation
- **cpu/__init__.py**: Package initialization
- **cpu/__main__.py**: CLI entry point
- **cpu/test_boot_digest.py**: Test suite
- **boot_manifest.json**: Configuration file
- **BOOT_REPORT.md**: Generated report (gitignored by default)

## Testing

Run the test suite:

```bash
python cpu/test_boot_digest.py
```

All tests should pass. The test suite validates:
- Module initialization
- Digest generation
- Fast mode vs full mode
- CLI commands (doctor, panic)
- BOOT_REPORT.md creation

## Philosophy

> **Mount persistent artifacts before you let volatile interpretation run.**

This is how operating systems stay sane. The boot system applies the same principle to your development workflow:

1. **Truth from storage**: Git is persistent, your memory isn't
2. **State restoration**: Deterministic rebuild of context
3. **Confidence flag**: Clear signal of system health

Not ego. Not vibes. A deterministic state restoration step.

## Exit Codes

- **0**: CONFIDENCE_OK (repo has commits and is healthy)
- **1**: CONFIDENCE_LOW or error occurred

## Future Enhancements

Potential improvements (not yet implemented):

- PR count from GitHub API
- More detailed git log analysis
- Integration with issue trackers
- Smart "next action" suggestions based on branch name
- Glob pattern support for anchor loading
- Caching for faster repeated boots

## Support

For issues or questions, refer to the main project README or documentation.

---

*Generated by CPU Boot Digest - Deterministic state restoration*
