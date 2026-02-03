#!/bin/bash
# Manual Crisis Test - DOM.CPU v2.0
# Simulates "nobody mode" for testing recovery protocol

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HIGH_SCORE_FILE="${REPO_ROOT}/high_score.txt"
BACKUP_FILE="${REPO_ROOT}/high_score.backup"

echo "🧪 CRISIS SIMULATION TEST"
echo "========================="
echo ""

# Backup current high score
if [ -f "${HIGH_SCORE_FILE}" ]; then
    cp "${HIGH_SCORE_FILE}" "${BACKUP_FILE}"
    ORIGINAL_SCORE=$(cat "${HIGH_SCORE_FILE}")
    echo "✅ Backed up current high score: ${ORIGINAL_SCORE}"
else
    echo "⚠️  No existing high score found"
    ORIGINAL_SCORE="0"
fi

echo ""
echo "SIMULATION OPTIONS:"
echo "1. Simulate RAM flush (set high score to 0)"
echo "2. Simulate partial loss (reduce high score by 50%)"
echo "3. Restore from backup"
echo "4. Cancel"
echo ""
read -p "Select option (1-4): " option

case $option in
    1)
        echo "💥 Simulating RAM flush..."
        echo "0" > "${HIGH_SCORE_FILE}"
        echo "⚠️  High score set to 0 (nobody mode)"
        echo ""
        echo "Run crisis recovery to test:"
        echo "  bash scripts/crisis_recovery.sh"
        ;;
    2)
        if [ "${ORIGINAL_SCORE}" -gt "0" ]; then
            NEW_SCORE=$((ORIGINAL_SCORE / 2))
            echo "⚠️  Simulating partial loss..."
            echo "${NEW_SCORE}" > "${HIGH_SCORE_FILE}"
            echo "High score reduced: ${ORIGINAL_SCORE} → ${NEW_SCORE}"
            echo ""
            echo "Run crisis recovery to test:"
            echo "  bash scripts/crisis_recovery.sh"
        else
            echo "❌ Cannot simulate partial loss with score of 0"
        fi
        ;;
    3)
        if [ -f "${BACKUP_FILE}" ]; then
            cp "${BACKUP_FILE}" "${HIGH_SCORE_FILE}"
            RESTORED_SCORE=$(cat "${HIGH_SCORE_FILE}")
            echo "✅ Restored from backup: ${RESTORED_SCORE}"
        else
            echo "❌ No backup file found"
        fi
        ;;
    4)
        echo "❌ Cancelled"
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "Current high score: $(cat ${HIGH_SCORE_FILE})"
echo "Current commits:    $(git rev-list --all --count)"
echo ""
echo "Backup saved to: ${BACKUP_FILE}"
