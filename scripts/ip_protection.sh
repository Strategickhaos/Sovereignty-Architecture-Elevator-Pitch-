#!/bin/bash
#
# IP Protection Automation Script
# Strategickhaos Sovereignty Architecture
# 
# Purpose: Automate multi-platform timestamping for IP protection
# Usage: ./ip_protection.sh --innovation "name" --description "desc" [options]
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$SCRIPT_DIR")"
LEGAL_DIR="${REPO_ROOT}/legal"
IP_RECORDS_DIR="${LEGAL_DIR}/ip_records"

# Create directories if they don't exist
mkdir -p "$IP_RECORDS_DIR"

# Functions
print_header() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}    IP PROTECTION AUTOMATION - SOVEREIGNTY ARCH        ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

show_help() {
    cat << EOF
IP Protection Automation Script

Usage:
    ./ip_protection.sh --innovation "name" --description "desc" [options]

Required Arguments:
    --innovation, -i        Innovation name (e.g., "TRIG6 Fitness Function")
    --description, -d       Innovation description

Optional Arguments:
    --files, -f            Comma-separated list of files to include
    --category, -c         Category (algorithm|system|protocol|language|other)
    --platforms, -p        Platforms to timestamp (github,academic,ai)
    --auto-commit          Automatically commit to Git (default: true)
    --gpg-sign             GPG sign the commit (default: true if GPG available)
    --create-tag           Create Git tag for this innovation
    --help, -h             Show this help message

Examples:
    # Basic usage
    ./ip_protection.sh \\
        --innovation "TRIG6 Fitness Function" \\
        --description "Multi-dimensional fitness evaluation for AI agents"

    # With specific files and tag
    ./ip_protection.sh \\
        -i "FlameLang Compiler" \\
        -d "Domain-specific language for swarm intelligence" \\
        -f "flamelang_compiler.py,grammar.txt" \\
        --create-tag

    # Full automation with all platforms
    ./ip_protection.sh \\
        -i "Negative-Balance Training" \\
        -d "Training AI under artificial resource constraints" \\
        -p "github,academic,ai" \\
        --auto-commit --gpg-sign

Environment Variables:
    SNHU_API_TOKEN         Canvas LMS API token (for academic timestamps)
    CLAUDE_API_KEY         Claude API key (for AI log timestamps)
    OPENAI_API_KEY         OpenAI API key (for GPT log timestamps)

EOF
}

# Parse arguments
INNOVATION_NAME=""
INNOVATION_DESC=""
FILES=""
CATEGORY="other"
PLATFORMS="github"
AUTO_COMMIT=true
GPG_SIGN=true
CREATE_TAG=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --innovation|-i)
            INNOVATION_NAME="$2"
            shift 2
            ;;
        --description|-d)
            INNOVATION_DESC="$2"
            shift 2
            ;;
        --files|-f)
            FILES="$2"
            shift 2
            ;;
        --category|-c)
            CATEGORY="$2"
            shift 2
            ;;
        --platforms|-p)
            PLATFORMS="$2"
            shift 2
            ;;
        --auto-commit)
            AUTO_COMMIT=true
            shift
            ;;
        --no-auto-commit)
            AUTO_COMMIT=false
            shift
            ;;
        --gpg-sign)
            GPG_SIGN=true
            shift
            ;;
        --no-gpg-sign)
            GPG_SIGN=false
            shift
            ;;
        --create-tag)
            CREATE_TAG=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$INNOVATION_NAME" ]]; then
    print_error "Innovation name is required"
    show_help
    exit 1
fi

if [[ -z "$INNOVATION_DESC" ]]; then
    print_error "Innovation description is required"
    show_help
    exit 1
fi

# Main execution
print_header

# Generate safe filename
SAFE_NAME=$(echo "$INNOVATION_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr -cd '[:alnum:]_-')
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
RECORD_FILE="${IP_RECORDS_DIR}/${TIMESTAMP}_${SAFE_NAME}.md"
JSON_FILE="${IP_RECORDS_DIR}/${TIMESTAMP}_${SAFE_NAME}.json"

print_step "Creating IP protection record for: ${INNOVATION_NAME}"
echo ""

# Generate Markdown documentation
cat > "$RECORD_FILE" << EOF
# IP Protection Record: ${INNOVATION_NAME}

**Generated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")  
**Category:** ${CATEGORY}  
**Status:** Active Prior Art

---

## Innovation Description

${INNOVATION_DESC}

---

## Timestamp Evidence

### Primary Timestamp
- **Date:** $(date -u +"%Y-%m-%d")
- **Time:** $(date -u +"%H:%M:%S UTC")
- **ISO 8601:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Unix Epoch:** $(date +%s)

### File Information
- **Record File:** ${RECORD_FILE}
- **JSON Metadata:** ${JSON_FILE}
EOF

if [[ -n "$FILES" ]]; then
    cat >> "$RECORD_FILE" << EOF
- **Associated Files:** ${FILES}

### File Hashes
EOF
    IFS=',' read -ra FILE_ARRAY <<< "$FILES"
    for file in "${FILE_ARRAY[@]}"; do
        file=$(echo "$file" | xargs)  # Trim whitespace
        if [[ -f "$file" ]]; then
            HASH=$(sha256sum "$file" | awk '{print $1}')
            echo "- \`${file}\`: \`${HASH}\`" >> "$RECORD_FILE"
        fi
    done
fi

cat >> "$RECORD_FILE" << EOF

---

## Platform Timestamps

EOF

# Initialize JSON record
cat > "$JSON_FILE" << EOF
{
  "innovation_name": "${INNOVATION_NAME}",
  "description": "${INNOVATION_DESC}",
  "category": "${CATEGORY}",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "unix_epoch": $(date +%s),
  "platforms": {},
  "files": []
}
EOF

# Add file information to JSON
if [[ -n "$FILES" ]]; then
    IFS=',' read -ra FILE_ARRAY <<< "$FILES"
    FILES_JSON="["
    for file in "${FILE_ARRAY[@]}"; do
        file=$(echo "$file" | xargs)
        if [[ -f "$file" ]]; then
            HASH=$(sha256sum "$file" | awk '{print $1}')
            FILES_JSON="${FILES_JSON}{\"file\":\"${file}\",\"sha256\":\"${HASH}\"},"
        fi
    done
    FILES_JSON="${FILES_JSON%,}]"  # Remove trailing comma
    
    # Update JSON with files
    TMP_JSON=$(mktemp)
    jq ".files = ${FILES_JSON}" "$JSON_FILE" > "$TMP_JSON" 2>/dev/null && mv "$TMP_JSON" "$JSON_FILE" || true
fi

# GitHub timestamping
if [[ "$PLATFORMS" == *"github"* ]]; then
    print_step "Timestamping via GitHub..."
    
    if git rev-parse --git-dir > /dev/null 2>&1; then
        GIT_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "not_yet_committed")
        GIT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "no_remote")
        
        cat >> "$RECORD_FILE" << EOF
### GitHub
- **Repository:** ${GIT_REMOTE}
- **Current Commit:** \`${GIT_COMMIT}\`
- **Commit Date:** $(git log -1 --format=%aI 2>/dev/null || echo "pending")
- **Record will be committed:** Yes
EOF
        
        # Update JSON
        TMP_JSON=$(mktemp)
        jq ".platforms.github = {\"repository\":\"${GIT_REMOTE}\",\"commit\":\"${GIT_COMMIT}\"}" "$JSON_FILE" > "$TMP_JSON" 2>/dev/null && mv "$TMP_JSON" "$JSON_FILE" || true
        
        print_success "GitHub timestamp prepared"
    else
        print_error "Not a Git repository"
    fi
fi

# Academic platform (if configured)
if [[ "$PLATFORMS" == *"academic"* ]]; then
    print_step "Preparing academic submission record..."
    
    cat >> "$RECORD_FILE" << EOF

### Academic Institution (SNHU)
- **Institution:** Southern New Hampshire University
- **Course:** CYBER-PSY-620 (Cybersecurity & Psychology)
- **Submission:** Manual submission required via Canvas LMS
- **Instructions:** Upload this record and associated files to Canvas
EOF
    
    if [[ -n "$SNHU_API_TOKEN" ]]; then
        print_info "SNHU API token found (automated submission not yet implemented)"
    else
        print_info "No SNHU API token found - manual submission required"
    fi
fi

# AI platform logging (if configured)
if [[ "$PLATFORMS" == *"ai"* ]]; then
    print_step "Preparing AI conversation log record..."
    
    cat >> "$RECORD_FILE" << EOF

### AI Conversation Logs
- **Claude (Anthropic):** Log innovation discussion manually
- **GPT (OpenAI):** Log innovation discussion manually
- **Prompt:** "For IP protection timestamping: ${INNOVATION_NAME} - ${INNOVATION_DESC}"
EOF
    
    if [[ -n "$CLAUDE_API_KEY" ]] || [[ -n "$OPENAI_API_KEY" ]]; then
        print_info "AI API keys found (automated logging not yet implemented)"
    else
        print_info "No AI API keys found - manual logging recommended"
    fi
fi

# Verification section
cat >> "$RECORD_FILE" << EOF

---

## Verification

### How to Verify This Record

1. **Git History:**
   \`\`\`bash
   git log --all --follow -- ${RECORD_FILE} --date=iso --pretty=fuller
   \`\`\`

2. **File Hash Verification:**
   \`\`\`bash
   sha256sum ${RECORD_FILE}
   \`\`\`

3. **JSON Metadata:**
   \`\`\`bash
   cat ${JSON_FILE} | jq .
   \`\`\`

### Cryptographic Proof

- **File SHA-256:** \`$(sha256sum "$RECORD_FILE" | awk '{print $1}')\`
- **JSON SHA-256:** \`$(sha256sum "$JSON_FILE" | awk '{print $1}')\`

---

## Legal Status

This document serves as:
- ✅ **Prior Art:** Establishes public disclosure date
- ✅ **Timestamp Evidence:** Multi-platform verification
- ✅ **IP Protection:** Prevents unauthorized patent claims
- ✅ **Attribution:** Documents original inventor

**Inventor:** Strategickhaos DAO LLC  
**Rights:** All rights reserved by original inventor  
**Public Access:** Via GitHub repository  

---

## References

- Invention Disclosure Form: [../INVENTION_DISCLOSURE_FORM.md](./INVENTION_DISCLOSURE_FORM.md)
- Prior Art Bundle: [../PRIOR_ART_BUNDLE.md](./PRIOR_ART_BUNDLE.md)
- Defensive Publication: [../DEFENSIVE_PUBLICATION.md](./DEFENSIVE_PUBLICATION.md)

---

**Record Created:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")  
**File:** \`${RECORD_FILE}\`  
**Status:** Active
EOF

print_success "Created IP record: ${RECORD_FILE}"
print_success "Created JSON metadata: ${JSON_FILE}"

# Compute final hashes
RECORD_HASH=$(sha256sum "$RECORD_FILE" | awk '{print $1}')
JSON_HASH=$(sha256sum "$JSON_FILE" | awk '{print $1}')

echo ""
print_info "Record Hash: ${RECORD_HASH}"
print_info "JSON Hash: ${JSON_HASH}"

# Git operations
if [[ "$AUTO_COMMIT" == true ]] && git rev-parse --git-dir > /dev/null 2>&1; then
    echo ""
    print_step "Committing to Git repository..."
    
    # Add files
    git add "$RECORD_FILE" "$JSON_FILE"
    
    if [[ -n "$FILES" ]]; then
        IFS=',' read -ra FILE_ARRAY <<< "$FILES"
        for file in "${FILE_ARRAY[@]}"; do
            file=$(echo "$file" | xargs)
            if [[ -f "$file" ]]; then
                git add "$file"
            fi
        done
    fi
    
    # Commit
    COMMIT_MSG="IP Protection: ${INNOVATION_NAME}

Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Category: ${CATEGORY}

${INNOVATION_DESC}

Evidence:
- Record: ${RECORD_FILE}
- Metadata: ${JSON_FILE}
"
    
    if [[ "$GPG_SIGN" == true ]] && command -v gpg &> /dev/null; then
        if git commit -S -m "$COMMIT_MSG" > /dev/null 2>&1; then
            print_success "Committed with GPG signature"
        else
            git commit -m "$COMMIT_MSG" > /dev/null 2>&1
            print_info "Committed without GPG signature (GPG signing failed)"
        fi
    else
        git commit -m "$COMMIT_MSG" > /dev/null 2>&1
        print_success "Committed to Git"
    fi
    
    # Get commit info
    COMMIT_SHA=$(git rev-parse HEAD)
    COMMIT_DATE=$(git log -1 --format=%aI)
    
    print_success "Commit SHA: ${COMMIT_SHA}"
    print_success "Commit Date: ${COMMIT_DATE}"
    
    # Create tag if requested
    if [[ "$CREATE_TAG" == true ]]; then
        TAG_NAME="ip-${SAFE_NAME}-${TIMESTAMP}"
        if git tag -a "$TAG_NAME" -m "IP Protection: ${INNOVATION_NAME}" > /dev/null 2>&1; then
            print_success "Created tag: ${TAG_NAME}"
        else
            print_info "Tag creation skipped (may already exist)"
        fi
    fi
    
    echo ""
    print_info "Remember to push to GitHub: git push origin main --tags"
fi

# Summary
echo ""
print_header
echo -e "${GREEN}IP Protection Record Successfully Created!${NC}"
echo ""
echo "Innovation: ${INNOVATION_NAME}"
echo "Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
echo "Record: ${RECORD_FILE}"
echo "Metadata: ${JSON_FILE}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Review the generated files"
if [[ "$AUTO_COMMIT" == true ]]; then
    echo "2. Push to GitHub: git push origin main --tags"
    echo "3. Submit to academic platform (if applicable)"
    echo "4. Log in AI conversations (if applicable)"
else
    echo "2. Manually commit files to Git"
    echo "3. Push to GitHub"
    echo "4. Submit to additional platforms"
fi
echo ""
echo -e "${GREEN}✓ Your innovation is now timestamped and protected!${NC}"
echo ""
