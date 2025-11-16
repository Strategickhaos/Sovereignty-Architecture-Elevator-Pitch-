# GitLens + Discord Workflow Scaffold

A ready-to-drop system for integrating GitLens with Discord workflows. This scaffold provides:

- **Discord Bot** with slash commands (`/status`, `/logs`, `/deploy`, `/scale`)
- **Event Gateway** for GitHub webhooks → Discord notifications  
- **GitLens VS Code Integration** with instant Discord pings
- **TypeScript** codebase with proper configuration
- **CI/CD Pipeline** with Discord notifications
- **Observability Stack** (Prometheus, Grafana, Loki, Vault)

## 🚀 Quick Start (5 minutes)

### 1. Copy Files to New Project

```bash
# Create new project directory
mkdir my-gitlens-discord && cd my-gitlens-discord

# Copy all scaffold files (rename without -scaffold suffix)
cp discovery-scaffold.yml discovery.yml
cp package-scaffold.json package.json
cp .vscode/tasks-scaffold.json .vscode/tasks.json
cp .github/workflows/ci-scaffold.yml .github/workflows/ci.yml
cp docker-compose-scaffold.yml docker-compose.obs.yml
cp monitoring/prometheus-scaffold.yml monitoring/prometheus.yml
cp monitoring/loki-config-scaffold.yml monitoring/loki-config.yml

# Copy source code as-is
cp -r src/ .
cp -r scripts/ .
cp tsconfig.json .
```

### 2. Configure Environment

```bash
# Create .env from example
cp .env.example .env

# Edit .env with your actual values:
# - DISCORD_TOKEN (from Discord Developer Portal)
# - GUILD_ID (your Discord server ID)
# - GITHUB_WEBHOOK_SECRET (generate with openssl rand -hex 32)
# - Channel IDs (right-click channels in Discord → Copy ID)
```

### 3. Update discovery.yml

```yaml
org:
  name: "yourcompany"  # Replace with your org name
discord:
  guild_id: "123456789"  # Your Discord server ID
  bot:
    app_id: "987654321"  # Your Discord app ID
git:
  org: "your-github-org"  # Your GitHub organization
repos:
  - name: "your-service"  # Your actual repository names
    channel: "#deployments"
```

### 4. Deploy

```bash
# Install dependencies
npm ci

# Start services
docker compose -f docker-compose.yml -f docker-compose.obs.yml up -d

# Register Discord commands (one-time)
npm run bot

# Start event gateway
npm run dev
```

## 🎯 What You Get

### Discord Slash Commands
- `/status service:api` → Check service health
- `/logs service:api tail:100` → View recent logs  
- `/deploy env:prod tag:v1.2.3` → Deploy to environment
- `/scale service:api replicas:5` → Scale service

### GitHub Integration
- **PR Events** → `#prs` channel notifications
- **CI/CD Results** → `#deployments` channel updates
- **Push Events** → Automated deployment notifications

### GitLens VS Code Tasks
- **Review Started** → Notify team in Discord
- **Review Submitted** → Update PR channel
- **Needs Attention** → Alert in Discord
- **Commit Graph** → Share insights

### Observability Stack
- **Prometheus** (:9090) → Metrics collection
- **Grafana** (:3000) → Dashboards (admin/admin)
- **Loki** (:3100) → Log aggregation  
- **Vault** (:8200) → Secret management

## 🔧 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   VS Code       │    │  GitHub Actions  │    │   Discord Bot   │
│   GitLens       │────┤  CI/CD Pipeline  │────┤ Slash Commands  │
│   Tasks         │    │  Webhooks        │    │ Notifications   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Event Gateway                               │
│           GitHub Webhooks → Discord Channel Router             │
└─────────────────────────────────────────────────────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  #prs Channel   │    │ #deployments     │    │  #alerts        │
│  PR Updates     │    │ CI/CD Results    │    │  System Alerts  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📋 Configuration Guide

### Discord Setup

1. **Create Discord Application:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - New Application → Bot → Copy token
   - OAuth2 → URL Generator → Scopes: `bot`, `applications.commands`
   - Permissions: `Send Messages`, `Use Slash Commands`, `Embed Links`

2. **Get Channel IDs:**
   - Enable Developer Mode in Discord settings
   - Right-click channels → Copy ID
   - Update `.env` with channel IDs

### GitHub Integration

1. **Create Webhook:**
   - Repository → Settings → Webhooks
   - Payload URL: `https://yourdomain.com/webhooks/github`
   - Content type: `application/json`
   - Secret: Your `GITHUB_WEBHOOK_SECRET`
   - Events: Pull requests, Pushes, Check suites

2. **Configure Repository Events:**
   - Update `discovery.yml` with your repos
   - Map repos to Discord channels
   - Set which events to forward

### Control API Integration

Update `discovery.yml` with your infrastructure API:

```yaml
control_api:
  base_url: "https://your-api.com"
  bearer_env: "YOUR_API_TOKEN"
```

## 🛠️ Customization

### Add New Slash Commands

Edit `src/discord.ts`:

```typescript
new SlashCommandBuilder()
  .setName("restart")
  .setDescription("Restart service")
  .addStringOption(o => o.setName("service").setRequired(true))
```

### Add New Event Routes

Edit `src/routes/github.ts`:

```typescript
if (ev === "deployment") {
  await send(channelIds.deployments, `Deployment`, `${payload.environment}: ${payload.state}`);
}
```

### Custom GitLens Tasks  

Edit `.vscode/tasks.json`:

```json
{
  "label": "GitLens: Custom Event",
  "type": "shell", 
  "command": "${workspaceFolder}/scripts/gl2discord.sh",
  "args": ["Custom Event", "Your message here"]
}
```

## 🔍 Troubleshooting

### Bot Not Responding
```bash
# Check logs
docker compose logs bot

# Verify token
echo $DISCORD_TOKEN | cut -c1-10

# Test permissions in Discord
```

### Webhooks Failing
```bash
# Check signature verification
docker compose logs gateway | grep signature

# Test webhook endpoint
curl -X POST localhost:8080/webhooks/github -H "X-GitHub-Event: ping"
```

### GitLens Tasks Not Working
```bash
# Make script executable
chmod +x scripts/gl2discord.sh

# Test manually
export DISCORD_TOKEN="your_token"
export CHANNEL_ID="your_channel_id"
./scripts/gl2discord.sh "Test" "Manual test"
```

## 📚 Next Steps

1. **Production Hardening:**
   - Move secrets to Vault
   - Add TLS termination  
   - Implement rate limiting
   - Set up monitoring alerts

2. **Extended Features:**
   - Add more slash commands
   - Create custom GitHub Actions
   - Build Grafana dashboards
   - Implement audit logging

3. **Team Adoption:**
   - Share VS Code tasks with team
   - Document workflow processes
   - Train on slash commands
   - Set up channel permissions

## 🎉 You're Ready!

This scaffold provides everything you need for a **Discord-native DevOps workflow**:

- ✅ **GitLens integration** for seamless developer experience
- ✅ **Slash commands** for infrastructure control
- ✅ **Real-time notifications** for all development events  
- ✅ **Production observability** with Prometheus/Grafana
- ✅ **Secure secret management** with Vault
- ✅ **CI/CD integration** with GitHub Actions

Your team can now manage infrastructure, review code, and monitor systems directly from Discord! 🚀