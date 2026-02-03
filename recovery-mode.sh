#!/bin/bash
# Operational Hygiene - Recovery Mode Script
# Run this when you're questioning yourself

echo "🔍 DOM.SYSTEM Recovery Mode"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check commit count
COMMIT_COUNT=$(git log --oneline 2>/dev/null | wc -l)
echo "📊 Total Commits: $COMMIT_COUNT"
echo ""

# Show recent work
echo "📁 Recent Work (last 10 commits):"
git log --oneline -10 2>/dev/null || echo "Not in a git repository"
echo ""

# The reminder
echo "🔥 Reminder:"
echo "  ✓ Check the commit history"
echo "  ✓ Check the specs"
echo "  ✓ Check the validators"
echo "  ✓ Then laugh and keep building"
echo ""
echo "Your system never lost integrity."
echo "It just rebooted without auto-mounting /confidence."
echo ""
echo "Remember: 🍔 Eat  💧 Drink  😴 Sleep"
echo "GitHub will still be there in the morning."
