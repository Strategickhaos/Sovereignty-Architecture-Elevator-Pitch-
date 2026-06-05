# Scripts Directory

This directory contains utility scripts for the Sovereignty Architecture project.

## Security Scripts

### regenerate_github_token.sh

**Purpose**: Automated GitHub Personal Access Token (PAT) regeneration and update workflow.

**Usage**:
```bash
./scripts/regenerate_github_token.sh [TOKEN_ID]
```

**Example**:
```bash
# Regenerate token with ID 2896174608
./scripts/regenerate_github_token.sh 2896174608

# Use default token ID
./scripts/regenerate_github_token.sh
```

**Features**:
- Interactive guided token regeneration process
- Token validation and format checking
- Automatic Vault integration (if available)
- GitHub Actions secrets update via GitHub CLI
- Token functionality verification
- Incident documentation and reporting
- Color-coded output for easy reading

**Prerequisites**:
- `curl` - API requests
- `jq` - JSON parsing
- `vault` - HashiCorp Vault CLI (optional)
- `gh` - GitHub CLI (optional but recommended)
- `git` - Repository detection

**What it does**:
1. Guides you through regenerating the token on GitHub
2. Validates the new token format
3. Updates the token in Vault (if configured)
4. Updates GitHub Actions secrets
5. Verifies token functionality via GitHub API
6. Creates an incident report for documentation

**When to use**:
- Token compromise detected
- Routine token rotation (every 90 days)
- Security audit recommendations
- Token exposure in logs/code
- Pre-production deployment preparation

**Related Documentation**:
- [SECURITY.md](../SECURITY.md) - Token management policies
- [VAULT_SECURITY_PLAYBOOK.md](../VAULT_SECURITY_PLAYBOOK.md) - Comprehensive rotation procedures

## Integration Scripts

### gl2discord.sh

**Purpose**: Send notifications from GitLens/Git events to Discord channels.

**Usage**:
```bash
./scripts/gl2discord.sh CHANNEL_ID "Title" "Message"
```

**Features**:
- Discord webhook integration
- Rich embed formatting
- GitLens event notifications

## Utility Scripts

### configure_sleep_mode.py

**Purpose**: Configure system sleep and power management settings.

### run_benchmarks.py

**Purpose**: Execute performance benchmarks for the system.

## Contributing

When adding new scripts:
1. Make scripts executable: `chmod +x scripts/your_script.sh`
2. Add proper shebang line: `#!/bin/bash` or `#!/usr/bin/env python3`
3. Include help/usage information in the script
4. Document in this README
5. Add error handling and validation
6. Use color-coded output for user feedback
7. Follow security best practices (no hardcoded secrets)

## Script Guidelines

### Security
- Never hardcode credentials or tokens
- Use environment variables or Vault for secrets
- Validate all user inputs
- Log security-relevant actions
- Include audit trails

### Usability
- Provide clear usage instructions
- Use color-coded output (errors in red, success in green)
- Include progress indicators
- Handle errors gracefully
- Create documentation/reports

### Reliability
- Check prerequisites before execution
- Validate all dependencies
- Use `set -e` in bash scripts for fail-fast
- Include rollback procedures where applicable
- Test in non-production first
