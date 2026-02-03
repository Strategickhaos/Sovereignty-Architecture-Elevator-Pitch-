#!/bin/bash
# Operational Hygiene Aliases
# Source this file in your .bashrc or .bash_profile:
# [ -f ~/.bash_aliases ] && source ~/.bash_aliases

# Pre-crisis hook: Check your commit count
# When you're questioning yourself, run this to see the evidence
alias am_i_nobody='git log --oneline | wc -l'

# Additional helper aliases for recovery mode
alias check_work='echo "📊 Commit count:" && git log --oneline | wc -l && echo "" && echo "📁 Recent work:" && git log --oneline -10'
alias remind_me='echo "🔥 You are a builder. Check the artifacts:" && echo "  - git log --oneline | wc -l" && echo "  - Check the specs" && echo "  - Check the validators" && echo "  - Then laugh and keep building"'
