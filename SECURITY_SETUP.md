# SAGCO OS v0.1.0 - Security Setup Guide

## 🔒 Production Deployment Security

### CRITICAL: Secret Management

Before deploying to production, you MUST configure proper secrets:

#### 1. Kubernetes Secrets

The default `k8s/sagco-deployment.yaml` has empty secrets. Generate and set them:

```bash
# Generate strong passwords
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
export REDIS_PASSWORD=$(openssl rand -base64 32)
export JWT_SECRET=$(openssl rand -base64 64)

# Create secrets in Kubernetes
kubectl create secret generic sagco-secrets \
  --from-literal=postgres-password="$POSTGRES_PASSWORD" \
  --from-literal=redis-password="$REDIS_PASSWORD" \
  --from-literal=jwt-secret="$JWT_SECRET" \
  --namespace=sagco

# For GitHub integration (optional)
kubectl create secret generic sagco-secrets \
  --from-literal=github-token="your_github_token" \
  --namespace=sagco --dry-run=client -o yaml | kubectl apply -f -
```

#### 2. Environment Variables

For local development, create a `.env.production` file:

```bash
# DO NOT commit this file!
POSTGRES_PASSWORD=your_secure_password_here
REDIS_PASSWORD=your_secure_password_here
JWT_SECRET=your_jwt_secret_here
GITHUB_TOKEN=your_github_token_optional
DISCORD_BOT_TOKEN=your_discord_token_optional
```

Add to `.gitignore`:
```
.env.production
.env.local
*.secret
```

#### 3. CI/CD Secrets

For GitHub Actions, add these secrets in repository settings:

- `POSTGRES_PASSWORD`
- `JWT_SECRET`
- `KUBECONFIG` (for Kubernetes deployment)
- `DISCORD_WEBHOOK_URL` (optional, for notifications)

### Security Best Practices

#### Container Security
✅ Non-root user (UID 1000)  
✅ Read-only root filesystem (where possible)  
✅ Minimal base image  
✅ No privileged containers  

#### Kubernetes Security
✅ NetworkPolicies for microsegmentation  
✅ RBAC with least-privilege access  
✅ PodSecurityPolicy enforcement  
✅ Resource limits and quotas  

#### Application Security
✅ JWT-based authentication  
✅ Password hashing with bcrypt  
✅ SQL injection prevention (SQLAlchemy ORM)  
✅ Input validation with Pydantic  

### Configuration

The kernel supports configurable paths via environment variables:

```bash
# State directory (default: /tmp)
export SAGCO_STATE_DIR=/var/lib/sagco

# Log directory
export SAGCO_LOG_DIR=/var/log/sagco
```

### Security Scanning

The CI/CD pipeline includes Trivy security scanning:

```bash
# Manual scan
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image sagco:latest
```

### Network Security

#### Ingress Configuration
- TLS 1.2+ only
- Rate limiting enabled
- CORS properly configured
- Security headers enabled

#### Database Access
- Internal cluster network only
- No external exposure
- TLS connections enforced

### Monitoring & Alerts

Configure alerts for:
- Failed authentication attempts
- Unusual API usage patterns
- Container vulnerabilities
- Secret access attempts

### Compliance

✅ OWASP Top 10 considerations  
✅ CIS Kubernetes Benchmark  
✅ Container Image Security Best Practices  
✅ Secret Management Best Practices  

## Quick Security Checklist

Before production deployment:

- [ ] Generate strong, unique passwords for all services
- [ ] Store secrets in Kubernetes Secrets or vault
- [ ] Enable TLS for all external endpoints
- [ ] Configure network policies
- [ ] Set up monitoring and alerting
- [ ] Enable audit logging
- [ ] Review and minimize RBAC permissions
- [ ] Scan container images for vulnerabilities
- [ ] Configure backup and disaster recovery
- [ ] Document security incident response plan

## Need Help?

- Security issues: Report via GitHub Security tab
- Questions: See SECURITY.md
- Updates: Watch for security advisories

---

**Remember: Security is a continuous process, not a one-time setup!**

SAGCO OS v0.1.0 - Built with security in mind 🔒
