# BOOT_RECON.md – "Recon on boot" for Strategickhaos

Run **any** of the numbered commands below in a fresh terminal (or paste the whole file into an LLM).  
All commands assume the repo is cloned, `.env` is sourced, and Docker Compose is installed.

```bash
# Load env once
set -a; source .env; set +a
```

## Environment Overview
- **Entry points**:
  - Discord bot: slash commands (/status, /logs, /deploy, /scale, /recon)
  - Event gateway: POST /webhooks/github (HMAC), metrics at :8080/metrics
  - Refinory AI: FastAPI at :8000/docs with AI agent orchestration
- **Observability** (optional overlay):
  - Prometheus :9090, Grafana :3000, Loki :3100, Vault :8200
  - Qdrant :6333, Redis :6379, PostgreSQL :5432

## 🚀 First 10 Minutes Checklist

### 1. Config / Secret Inventory
```bash
grep -RIl "\.env\|\.yml\|\.yaml\|\.json\|Dockerfile\|docker-compose" . | head -10 | xargs -I{} sh -c "echo '=== {} ==='; head -n5 {}"
```

### 2. Discovery.yml Map (Table)
```bash
yq e '. | to_entries | map("|\(.key)|\(.value|type)|") | .[]' discovery.yml 2>/dev/null || echo "Install yq for YAML parsing"
```

### 3. All Entry Points
```bash
find . -type f \( -perm /111 -o -name "*.sh" -o -name "*.js" -o -name "Dockerfile" \) \
  -exec grep -lE "^#!|node |python|bash" {} \; | head -10
```

### 4. Discord References
```bash
grep -RIn "DISCORD_.*\|webhook" . | cut -d: -f1,2 | sort -u | head -10
```

### 5. GitHub References
```bash
grep -RIn "GITHUB_.*\|github\.com" . | cut -d: -f1,2 | sort -u | head -10
```

### 6. Secret Usage
```bash
grep -RIn "HMAC_SECRET\|JWT_SECRET\|VAULT_TOKEN\|API_KEY" . | cut -d: -f1 | sort -u
```

## 🔧 Core Stack Bring-Up

### 7. Runtime Environment Per Service
```bash
docker compose config --services 2>/dev/null | head -5 | xargs -I{} sh -c "echo '--- {} ---'; docker compose ps {} --format 'table {{.Name}}\t{{.Ports}}\t{{.State}}' 2>/dev/null || echo 'Not running'"
```

### 8. Observability Endpoints  
```bash
docker compose -f docker-compose.obs.yml config 2>/dev/null | yq e '.services.*.ports[]?.target' - | sort -u | head -10
```

### 9. Package.json Critical Deps
```bash
jq '.dependencies + .devDependencies | to_entries[] | "\(.key)@\(.value)"' package.json 2>/dev/null | head -10
```

### 10. Slash-Command / Webhook Handlers
```bash
grep -RIn "interactionCreate\|webhook" src/ refinory/ | cut -d: -f1 | sort -u
```

## 🤖 AI/LLM Integration Points

### 11. LLM Key Usage
```bash
grep -RIn "OPENAI\|XAI\|ANTHROPIC" src/ refinory/ | cut -d: -f1 | sort -u
```

### 12. Hard-Coded Secrets (Security Check)
```bash
grep -RInE "([a-zA-Z0-9+/]{20,}=)" . | grep -v -E "\.env|node_modules|\.git" | head -5
```

### 13. GitHub → Gateway → Discord Diagram (ASCII)
```bash
echo '
GitHub Webhooks ──HMAC──> Event Gateway (:8080)
     │                         │
     │                         ▼
     └────────────────> Discord Bot (:3000)
                              │
                              ▼
                       #pr-channel / #dev-feed
                              │
                              ▼
                      Refinory AI Agents (:8000)
                              │
                              ▼
                    Architecture Generation & PRs
'
```

## 🩺 Smoke Tests

### 14. Basic Service Health
```bash
# Bot online check
./gl2discord.sh "${DISCORD_PR_CHANNEL_ID:-}" "🔥 Recon Smoke Test" "Bot alive at $(date)" "0x00ff00" 2>/dev/null || echo "gl2discord.sh not configured"

# Gateway reachable  
curl -s http://localhost:8080/health 2>/dev/null || echo "Gateway not responding"

# Refinory API
curl -s http://localhost:8000/health 2>/dev/null | jq .status || echo "Refinory API not responding"
```

### 15. TODO/FIXME Inventory
```bash
grep -RIn "TODO\|FIXME\|HACK\|XXX" . | grep -v node_modules | head -10
```

### 16. CI Inputs & Requirements  
```bash
find .github/workflows -name "*.yml" -exec yq e '.jobs.*.steps[].uses // .jobs.*.env // empty' {} \; 2>/dev/null | sort -u | head -10
```

## 🚀 Bootstrap Commands

### 17. One-Shot Fresh Host Bootstrap
```bash
# Copy and customize this for new environments:
cat > bootstrap-fresh.sh << 'EOF'
#!/bin/bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
cp .env.example .env  # Edit tokens!
npm ci
docker compose up --build -d
EOF
chmod +x bootstrap-fresh.sh
```

### 18. Exposed Network Endpoints
```bash
docker compose config 2>/dev/null | yq e '.services.*.ports[] | "\(.published // "none"):\(.target) (\(.service // "unknown"))"' - | sort -u
```

## 🚨 Incident Response Playbooks

### 19. Incident: Bot Offline, Gateway Up
```bash
echo "=== Bot Diagnostic ==="
docker logs bot-container 2>/dev/null | tail -20 || echo "No bot container found"
docker exec bot-container node -e "console.log('Token prefix:', process.env.DISCORD_TOKEN?.slice(0,8))" 2>/dev/null || echo "Cannot exec into bot"
```

### 20. Incident: Webhooks Not Reaching Discord
```bash
echo "=== Webhook Diagnostic ==="
docker logs gateway-container 2>/dev/null | grep -i "signature\|error" | tail -10 || echo "No gateway logs"
echo "Test webhook:"
echo 'curl -v -X POST http://localhost:8080/webhook -H "X-Hub-Signature-256: sha256=test" -d "{}"'
```

### 21. Standard JSON Log Format (Template)
```json
{
  "timestamp": "2025-11-16T12:00:00Z",
  "level": "info", 
  "service": "gateway",
  "component": "webhook_handler",
  "message": "GitHub webhook received",
  "metadata": {
    "event_type": "pull_request",
    "repo": "Strategickhaos/repo-name",
    "pr_number": 123,
    "action": "opened"
  },
  "trace_id": "abc-123-def"
}
```

### 22. ENV=Development → Production Diff
```bash
grep -R "development\|dev\|debug" . | grep -v node_modules | cut -d: -f1 | sort -u | head -10
```

## 🛠️ Scripts Inventory

### 23. Scripts/ Directory Map
```bash
ls -la scripts/*.sh 2>/dev/null | awk '{print $9 " → " $1 " " $5 "bytes"}' || echo "No scripts/ directory"
ls -la *.sh | awk '{print $9 " → " $1 " " $5 "bytes"}'
```

### 24. Vault Health Check
```bash
docker exec vault-container vault status 2>/dev/null | grep "Sealed\|Initialized" || echo "Vault container not found"
```

### 25. Boot Scripts (Cold/Warm/Disaster)
```bash
echo "=== Cold Boot ==="
echo "docker compose down -v && docker compose up --build -d"
echo ""
echo "=== Warm Restart ==="  
echo "docker compose restart bot gateway refinory-api"
echo ""
echo "=== Disaster Restore ==="
echo "docker compose down && docker system prune -f && docker compose up -d"
```

## 📊 Full Recon Summary

### 26. Complete Environment Status
```bash
echo "## 🏗️ Architecture Stack Status"
echo "Date: $(date)"
echo ""
echo "### Services"
docker compose ps --format "table {{.Name}}\t{{.State}}\t{{.Ports}}" 2>/dev/null || echo "Docker Compose not running"
echo ""
echo "### Secrets Loaded" 
env | grep -E "DISCORD|GITHUB|VAULT|JWT|HMAC|OPENAI|XAI|ANTHROPIC" | wc -l | xargs echo "Secret count:"
echo ""
echo "### Key Endpoints"
echo "- Discord Bot: Check guild for slash commands"
echo "- Event Gateway: http://localhost:8080/health"
echo "- Refinory API: http://localhost:8000/docs" 
echo "- Prometheus: http://localhost:9090"
echo "- Grafana: http://localhost:3000 (admin/admin)"
echo "- Vault: http://localhost:8200"
echo ""
echo "### Next Actions"
echo "1. Run smoke tests (commands 14-16)"
echo "2. Check Discord bot permissions"
echo "3. Test webhook signature validation"
echo "4. Verify Refinory AI expert responses"
```

---

## 🎯 Elite Recon Prompts (Copy-Paste to any LLM)

**Systems Architecture:**
1. "Given this repo and its current state, design a high-level *Sovereignty Architecture* diagram that shows all services, bots, gateways, and AI agents, and describe how data, logs, and secrets flow between them."

**Configuration Analysis:**  
2. "Read `discovery.yml` and generate a human-readable spec: explain org, Discord, infra, AI agents, Git, and event_gateway sections as if you're onboarding a new senior engineer on Strategickhaos."

**Security Audit:**
3. "Audit the current `.env`, `Dockerfile`, and `docker-compose.yml`. Identify security risks, environment leaks, and any missing secrets management, and propose a hardened version with Vault integration."

**Dependency Mapping:**
4. "From this workspace, infer all external dependencies (Docker images, Node modules, Vault, GitHub Apps, Discord bot perms) and produce a dependency manifest: what needs to exist *outside* the repo for the system to work."

**Incident Response:**
5. "Generate an **Ops FAQ**: list the top 15 likely 'WTF is happening?' questions an on-call engineer will ask when the bot, gateway, or webhooks misbehave, and answer them based on this codebase."

---

Run `VERIFIED` after you commit this file and test the observability stack! 🚀