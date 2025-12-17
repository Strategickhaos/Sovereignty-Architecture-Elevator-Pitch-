# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 5.1.x   | :white_check_mark: |
| 5.0.x   | :x:                |
| 4.0.x   | :white_check_mark: |
| < 4.0   | :x:                |

## Reporting a Vulnerability

Use this section to tell people how to report a vulnerability.

Tell them where to go, how often they can expect to get an update on a
reported vulnerability, what to expect if the vulnerability is accepted or
declined, etc.

## GitHub Personal Access Token (PAT) Management

### Token Regeneration Process

If a GitHub Personal Access Token has been exposed, compromised, or needs rotation, follow these steps immediately:

#### 1. Regenerate the Token on GitHub

1. Navigate to your GitHub token settings: https://github.com/settings/tokens
2. Locate the specific token that needs regeneration (e.g., token ID: 2896174608)
3. Click on the token name or the "Regenerate" button
4. Confirm the regeneration - this will invalidate the old token immediately
5. **Important**: Copy the new token value immediately - it will only be shown once

#### 2. Update Token in GitHub Repository Secrets

After regenerating the token, update it in all locations where it's used:

1. Go to repository Settings → Secrets and variables → Actions
2. Update the following secrets with the new token value:
   - `GITHUB_TOKEN` (if using a custom PAT instead of the default)
   - Any other secrets that reference this token

#### 3. Update Token in External Systems

Update the token in all external systems that use it:

- **Vault**: Update the secret at `vault://kv/github/pat`
- **Docker Compose**: Update environment variables that reference `GITHUB_TOKEN`
- **Local Development**: Update `.env` files or environment configurations
- **CI/CD Pipelines**: Verify all workflows are using the updated secret

#### 4. Verify Token Functionality

After updating, verify that the new token works correctly:

```bash
# Test GitHub API access
curl -H "Authorization: token YOUR_NEW_TOKEN" https://api.github.com/user

# Verify repository access
git clone https://YOUR_NEW_TOKEN@github.com/your-org/your-repo.git
```

#### 5. Audit and Monitor

- Review GitHub audit logs for any suspicious activity with the old token
- Monitor API usage to ensure the new token is functioning properly
- Document the incident and rotation in your security logs

### Token Security Best Practices

1. **Never commit tokens to source code** - Use environment variables or secret management systems
2. **Use fine-grained permissions** - Create tokens with minimal necessary scopes
3. **Rotate regularly** - Set up a regular token rotation schedule (e.g., every 90 days)
4. **Monitor usage** - Track token usage through GitHub audit logs
5. **Use GitHub Secrets** - Store tokens in GitHub Actions secrets, not in code or config files
6. **Enable 2FA** - Always enable two-factor authentication on GitHub accounts
7. **Limit token lifetime** - Use token expiration settings when available
8. **Use Vault** - Store tokens in HashiCorp Vault or similar secret management systems

### Emergency Response Checklist

If a token is suspected to be compromised:

- [ ] Immediately regenerate the token on GitHub
- [ ] Review GitHub audit logs for unauthorized access
- [ ] Update all systems that use the token
- [ ] Verify no malicious changes were made to repositories
- [ ] Document the incident
- [ ] Review access controls and permissions
- [ ] Consider rotating related credentials
- [ ] Notify team members if necessary
- [ ] Update security procedures to prevent recurrence

### Token Inventory

Maintain an inventory of all tokens used in the project:

| Token Purpose | Storage Location | Rotation Schedule | Last Rotated |
|--------------|------------------|-------------------|--------------|
| GitHub PAT (CI/CD) | GitHub Secrets | Every 90 days | [Date] |
| Discord Bot Token | Vault: `discord/*` | Every 180 days | [Date] |
| HMAC Signing Key | Vault: `shared/hmac` | Every 365 days | [Date] |

For detailed secret rotation procedures, see [VAULT_SECURITY_PLAYBOOK.md](VAULT_SECURITY_PLAYBOOK.md).
