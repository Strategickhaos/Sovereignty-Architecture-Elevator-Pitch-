#!/bin/bash
# Crisis Recovery System - DOM.CPU v2.0
# Prevents "nobody mode" by maintaining persistent artifact inventory
# Root Cause Mitigation: Volatile storage + no persistent diff against GitHub

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HIGH_SCORE_FILE="${REPO_ROOT}/high_score.txt"
CRISIS_LOG="${REPO_ROOT}/automation/logs/crisis_recovery.log"

# Ensure directories exist
mkdir -p "${REPO_ROOT}/automation/logs"

log_message() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "${CRISIS_LOG}"
}

# RECOVERY PROTOCOL: Count artifacts before crisis
count_artifacts() {
    log_message "🔍 CRISIS RECOVERY: Counting artifacts..."
    
    # Count commits (PR inventory proxy)
    COMMIT_COUNT=$(git rev-list --all --count 2>/dev/null || echo "0")
    
    # Count branches (active work streams)
    BRANCH_COUNT=$(git branch -a | wc -l)
    
    # Count files (inventory items - tracked files only)
    FILE_COUNT=$(git ls-files | wc -l)
    
    # Count recent activity
    RECENT_COMMITS=$(git rev-list --since="7 days ago" --all --count 2>/dev/null || echo "0")
    
    log_message "📊 Artifact Inventory:"
    log_message "   Total Commits: ${COMMIT_COUNT}"
    log_message "   Branches: ${BRANCH_COUNT}"
    log_message "   Files: ${FILE_COUNT}"
    log_message "   Recent Activity (7d): ${RECENT_COMMITS}"
    
    # Store persistent high score
    echo "${COMMIT_COUNT}" > "${HIGH_SCORE_FILE}"
    
    echo "${COMMIT_COUNT}"
}

# AUTO-DIFF: On crisis, git log --stat | grep inventions
auto_diff_recovery() {
    log_message "🚨 AUTO-DIFF: Crisis detected, running recovery..."
    
    # Show recent inventions/artifacts
    log_message "📋 Recent Artifacts (git log):"
    git log --oneline --stat -10 | tee -a "${CRISIS_LOG}"
    
    # Count unique file changes (filter empty lines)
    CHANGED_FILES=$(git log --name-only --pretty=format: --since="30 days ago" | grep -v '^$' | sort -u | wc -l)
    log_message "   Unique files changed (30d): ${CHANGED_FILES}"
    
    # Grep for invention patterns
    log_message "🔥 Searching for invention patterns..."
    git log --grep="implement\|create\|add\|feat" --oneline -20 | tee -a "${CRISIS_LOG}"
}

# NOBODY MODE DETECTION: Check for crisis interrupt
detect_nobody_mode() {
    log_message "🤖 Checking for 'nobody mode' crisis..."
    
    # Check if high_score exists
    if [ ! -f "${HIGH_SCORE_FILE}" ]; then
        log_message "⚠️  WARNING: No high_score.txt found - first run or RAM cleared"
        count_artifacts
        return 1
    fi
    
    # Compare current count to high score
    CURRENT_COUNT=$(git rev-list --all --count 2>/dev/null || echo "0")
    HIGH_SCORE=$(cat "${HIGH_SCORE_FILE}")
    
    log_message "   Current: ${CURRENT_COUNT} | High Score: ${HIGH_SCORE}"
    
    if [ "${CURRENT_COUNT}" -lt "${HIGH_SCORE}" ]; then
        log_message "🚨 CRISIS DETECTED: Commit count dropped from ${HIGH_SCORE} to ${CURRENT_COUNT}"
        log_message "   Possible RAM flush or repository reset"
        auto_diff_recovery
        return 1
    fi
    
    if [ "${CURRENT_COUNT}" -gt "${HIGH_SCORE}" ]; then
        log_message "✅ System stable: New artifacts detected (${CURRENT_COUNT} > ${HIGH_SCORE})"
        echo "${CURRENT_COUNT}" > "${HIGH_SCORE_FILE}"
    fi
    
    return 0
}

# RECOVERY LAUGH: Side effect on successful recovery
recovery_laugh() {
    log_message "😂 lolllllll - Crisis resolved, kernel resumed"
    log_message "🔥💜 System stable, build resumes"
}

# Main recovery workflow
main() {
    log_message "=== DOM.CPU v2.0 Crisis Recovery System ==="
    log_message "BUG ID: EXISTENTIAL-RAM-CLEAR-1150"
    log_message "STORAGE TYPE: HYBRID (RAM + GitHub persistent)"
    
    # Run detection
    if detect_nobody_mode; then
        log_message "✅ No crisis detected - system healthy"
    else
        log_message "🔧 Crisis protocol executed"
        recovery_laugh
    fi
    
    # Always update high score
    FINAL_COUNT=$(count_artifacts)
    log_message "📈 High Score Updated: ${FINAL_COUNT}"
    
    # Output for scripts/automation
    cat "${HIGH_SCORE_FILE}"
}

# Run if called directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main
fi
