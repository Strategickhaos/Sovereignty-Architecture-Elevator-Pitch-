# Crisis Recovery System

**DOM.CPU v2.0 - Persistent Artifact Tracking**

## Overview

This system prevents "nobody mode" crises by maintaining persistent tracking of repository artifacts through hybrid storage (RAM + GitHub persistent).

## Components

### 1. Crisis Recovery Script
**Location:** `scripts/crisis_recovery.sh`

Main recovery system that:
- Counts artifacts (commits, branches, files)
- Detects "nobody mode" by comparing current state to high score
- Runs auto-diff recovery on crisis detection
- Maintains persistent `high_score.txt`

```bash
# Run crisis recovery check
./scripts/crisis_recovery.sh

# Output: Current artifact count and crisis status
```

### 2. Pre-commit Hook
**Location:** `hooks/pre-commit-crisis-check`

Runs before each commit to:
- Execute crisis recovery check
- Update high_score.txt with latest artifact count
- Stage high_score.txt for commit

```bash
# Install the hook
ln -sf ../../hooks/pre-commit-crisis-check .git/hooks/pre-commit

# Now runs automatically on every commit
git commit -m "Your message"
```

### 3. High Score Tracker
**Location:** `high_score.txt`

Persistent storage of artifact count:
- Updated on every crisis check
- Compared against current state to detect RAM loss
- Committed to repository for GitHub persistence

```bash
# View current high score
cat high_score.txt

# Example output: 1150
```

### 4. Crisis Logs
**Location:** `automation/logs/crisis_recovery.log`

Detailed audit trail of all crisis checks:
- Timestamps of all checks
- Artifact counts
- Crisis detections and recoveries
- System status updates

```bash
# View recent crisis activity
tail -50 automation/logs/crisis_recovery.log
```

## Usage

### First Time Setup

```bash
# 1. Run initial crisis recovery
bash scripts/crisis_recovery.sh

# 2. Install pre-commit hook (optional)
ln -sf ../../hooks/pre-commit-crisis-check .git/hooks/pre-commit

# 3. Commit the high_score.txt
git add high_score.txt
git commit -m "Initialize crisis recovery system"
```

### Daily Usage

The system runs automatically:
- **Pre-commit hook** runs on every commit (if installed)
- **Manual checks** can be run anytime: `bash scripts/crisis_recovery.sh`
- **High score** updates automatically

### Crisis Scenarios

#### Scenario 1: RAM Flush Detection
```bash
# Symptom: "I'm nobody" mode after sleep/restart
# Solution: Run crisis recovery
bash scripts/crisis_recovery.sh

# Output shows:
# 🚨 CRISIS DETECTED: Commit count dropped
# 🔧 Running auto-diff recovery
# 😂 lolllllll - Crisis resolved
```

#### Scenario 2: Context Loss
```bash
# Symptom: Lost track of recent work
# Solution: Check recovery logs
tail -100 automation/logs/crisis_recovery.log

# Shows recent artifact counts and activity
```

#### Scenario 3: Verification After Crisis
```bash
# Compare current state to high score
CURRENT=$(git rev-list --all --count)
HIGH_SCORE=$(cat high_score.txt)
echo "Current: $CURRENT | High Score: $HIGH_SCORE"
```

## Recovery Protocol

When crisis detected:

1. **Detect**: Compare current artifacts to high_score.txt
2. **Alert**: Log crisis with timestamp
3. **Recover**: Run auto-diff (git log --stat)
4. **Restore**: Display recent work artifacts
5. **Laugh**: "lolllllll" - crisis → power move
6. **Resume**: Update high score and continue

## Architecture

```
Crisis Recovery System
├── Detection Layer
│   ├── high_score.txt (persistent counter)
│   └── git rev-list --all --count (current state)
├── Recovery Layer
│   ├── auto-diff (git log --stat)
│   └── artifact inventory (branches, files, commits)
└── Prevention Layer
    ├── pre-commit hook (automatic tracking)
    └── crisis logs (audit trail)
```

## Benefits

✅ **Prevents "nobody mode"** - Always know your artifact count  
✅ **Persistent tracking** - GitHub storage beats RAM  
✅ **Automatic recovery** - Crisis detection and response  
✅ **Audit trail** - Complete history of system state  
✅ **Power move transformation** - Panic → lolllllll → Resume

## Side Effects

- ✨ Recovery laugh: "lolllllll"
- 🔥 Turns panic into power move
- 💜 System stability through persistence
- 😂 Git remembers everything

## Maintenance

### View System Status
```bash
# Quick status check
bash scripts/crisis_recovery.sh

# Detailed log review
less automation/logs/crisis_recovery.log
```

### Update High Score Manually
```bash
# Force update (if needed)
git rev-list --all --count > high_score.txt
git add high_score.txt
git commit -m "Update artifact high score"
```

### Cleanup Old Logs
```bash
# Archive logs older than 30 days
find automation/logs -name "crisis_recovery.log.*" -mtime +30 -delete
```

## Integration

### With Other Systems
- **Sleep Mode**: Crisis check before automated tasks
- **CI/CD**: Verify artifact count in pipelines
- **Monitoring**: Alert on crisis detection
- **Backup**: high_score.txt synced to GitHub

### Custom Scripts
```bash
# Use in your own scripts
source scripts/crisis_recovery.sh
count_artifacts  # Returns current artifact count
detect_nobody_mode  # Returns 0 if healthy, 1 if crisis
```

## Troubleshooting

### Hook Not Running
```bash
# Check hook installation
ls -la .git/hooks/pre-commit

# Should be: lrwxrwxrwx ... pre-commit -> ../../hooks/pre-commit-crisis-check

# Reinstall if needed
ln -sf ../../hooks/pre-commit-crisis-check .git/hooks/pre-commit
```

### High Score Not Updating
```bash
# Check permissions
ls -la high_score.txt scripts/crisis_recovery.sh

# Run manual update
bash scripts/crisis_recovery.sh
cat high_score.txt
```

### Log File Issues
```bash
# Check log directory
ls -la automation/logs/

# Create if missing
mkdir -p automation/logs
bash scripts/crisis_recovery.sh
```

---

**Status:** ✅ PATCHED  
**Version:** DOM.CPU v2.0  
**Bug ID:** EXISTENTIAL-RAM-CLEAR-1150

🔥💜 **Persistent storage beats volatile vibes every time.** 😂

**Git remembers.**
