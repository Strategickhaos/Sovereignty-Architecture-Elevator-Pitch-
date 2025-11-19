# 🛠️ Local Development Setup Guide

## Overview

This guide walks you through setting up a complete local development environment for the Strategickhaos Sovereignty Architecture, including webhook testing with ngrok.

## Prerequisites

- **Docker** and **Docker Compose** installed
- **Node.js** v18+ and **npm** installed
- **Git** for version control
- **ngrok** account (free tier works) for webhook testing

## Quick Start

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
npm install
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Required environment variables:
- `DISCORD_TOKEN` - Your Discord bot token
- `GITHUB_WEBHOOK_SECRET` - Secret for GitHub webhook verification
- `PRS_CHANNEL_ID` - Discord channel ID for pull requests
- `DEPLOYMENTS_CHANNEL_ID` - Discord channel ID for deployments
- `ALERTS_CHANNEL_ID` - Discord channel ID for alerts

### 3. Start Local Services

```bash
# Start all services with Docker Compose
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f event-gateway
```

The following services will be available:
- **Event Gateway**: http://localhost:8080
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Qdrant**: http://localhost:6333

## 🌐 Setting Up ngrok for Webhook Testing

### Why ngrok?

During local development, GitHub webhooks need a publicly accessible URL to send events to your local event gateway. ngrok creates a secure tunnel from the internet to your localhost, making webhook testing possible without deploying to a remote server.

### Installing ngrok

#### Windows

**Option 1: Download Installer (Recommended)**

1. Visit [ngrok.com/download](https://ngrok.com/download)
2. Download the Windows installer (ngrok installer.zip)
3. Extract the zip file to a folder (e.g., `C:\Program Files\ngrok`)
4. Add the ngrok folder to your system PATH:
   - Right-click "This PC" → Properties → Advanced System Settings
   - Click "Environment Variables"
   - Under "System Variables", find and edit "Path"
   - Add the path to your ngrok folder
   - Click OK to save

**Option 2: Using Chocolatey**

```powershell
choco install ngrok
```

**Option 3: Using Scoop**

```powershell
scoop install ngrok
```

#### macOS

**Option 1: Using Homebrew (Recommended)**

```bash
brew install ngrok/ngrok/ngrok
```

**Option 2: Manual Installation**

```bash
# Download and install
curl -O https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip
unzip ngrok-v3-stable-darwin-amd64.zip
sudo mv ngrok /usr/local/bin/
```

#### Linux

**Option 1: Using Package Manager**

```bash
# Ubuntu/Debian
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# Fedora/RHEL
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/yum.repos.d/ngrok.asc
sudo yum install ngrok
```

**Option 2: Manual Installation**

```bash
# Download and install
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
sudo tar xvzf ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin
```

### Configuring ngrok

1. **Sign up for ngrok** (if you haven't already):
   - Visit [ngrok.com](https://ngrok.com) and create a free account

2. **Get your authentication token**:
   - Go to [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
   - Copy your authtoken

3. **Add your authtoken to ngrok**:
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

### Starting ngrok Tunnel

#### For Event Gateway (port 8080)

```bash
# Start ngrok tunnel to your local event gateway
ngrok http 8080

# Or with a custom subdomain (requires paid plan)
ngrok http 8080 --subdomain=strategickhaos-dev
```

You should see output like:
```
ngrok                                                                                               
                                                                                                    
Session Status                online                                                               
Account                       your-email@example.com (Plan: Free)                                
Version                       3.x.x                                                                
Region                        United States (us)                                                   
Latency                       45ms                                                                 
Web Interface                 http://127.0.0.1:4040                                               
Forwarding                    https://abc123xyz.ngrok-free.app -> http://localhost:8080           
                                                                                                    
Connections                   ttl     opn     rt1     rt5     p50     p90                         
                              0       0       0.00    0.00    0.00    0.00
```

**Important**: Copy the `https://` URL (e.g., `https://abc123xyz.ngrok-free.app`) - you'll use this as your webhook URL.

#### Using ngrok Web Interface

ngrok provides a web interface at http://127.0.0.1:4040 where you can:
- Inspect all HTTP requests and responses
- Replay requests for testing
- View request/response details
- Debug webhook issues

## 🔗 Configuring GitHub Webhooks with ngrok

### Method 1: Repository-level Webhook

1. Go to your GitHub repository
2. Navigate to **Settings** → **Webhooks** → **Add webhook**
3. Configure the webhook:
   - **Payload URL**: `https://YOUR_NGROK_URL.ngrok-free.app/webhooks/github`
   - **Content type**: `application/json`
   - **Secret**: Your `GITHUB_WEBHOOK_SECRET` from `.env`
   - **Events**: Select individual events:
     - Pull requests
     - Pushes
     - Check suites
     - Or select "Send me everything"
   - **Active**: ✓ (checked)
4. Click **Add webhook**

### Method 2: GitHub App Webhook

If you're using a GitHub App:

1. Go to **GitHub** → **Settings** → **Developer settings** → **GitHub Apps**
2. Select your app or create a new one
3. Set **Webhook URL**: `https://YOUR_NGROK_URL.ngrok-free.app/webhooks/github`
4. Set **Webhook secret**: Your `GITHUB_WEBHOOK_SECRET`
5. Subscribe to events:
   - Pull requests
   - Pushes
   - Check runs
   - Check suites
6. Save changes

## 🧪 Testing Webhooks

### Test 1: Health Check

```bash
# Test the event gateway is running
curl http://localhost:8080/health

# Test through ngrok
curl https://YOUR_NGROK_URL.ngrok-free.app/health
```

### Test 2: Manual Webhook Trigger

```bash
# Create a test payload
cat > test-webhook.json << 'EOF'
{
  "action": "opened",
  "pull_request": {
    "number": 123,
    "title": "Test PR",
    "user": {
      "login": "testuser"
    },
    "html_url": "https://github.com/test/repo/pull/123",
    "base": {
      "repo": {
        "full_name": "test/repo"
      }
    }
  }
}
EOF

# Calculate HMAC signature
SECRET="your_github_webhook_secret"
PAYLOAD=$(cat test-webhook.json)
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | sed 's/^.* //')

# Send test webhook
curl -X POST http://localhost:8080/webhooks/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: pull_request" \
  -H "X-Hub-Signature-256: sha256=$SIGNATURE" \
  -d @test-webhook.json
```

### Test 3: Trigger from GitHub

1. Create a new branch in your repository
2. Open a pull request
3. Check the ngrok web interface (http://127.0.0.1:4040) to see the webhook request
4. Check your Discord channel for the notification
5. Check Docker logs:
   ```bash
   docker-compose logs -f event-gateway
   ```

## 📊 Monitoring and Debugging

### View Event Gateway Logs

```bash
# Real-time logs
docker-compose logs -f event-gateway

# Last 100 lines
docker-compose logs --tail=100 event-gateway

# Filter for errors
docker-compose logs event-gateway | grep -i error
```

### ngrok Request Inspector

Visit http://127.0.0.1:4040 to see:
- All incoming requests
- Request headers and body
- Response status and body
- Request timing
- Ability to replay requests

### Common Issues

**Problem: Webhook signature validation fails**
```
Solution: Ensure your GITHUB_WEBHOOK_SECRET matches in:
- Your .env file
- GitHub webhook settings
- Test scripts
```

**Problem: ngrok tunnel keeps disconnecting**
```
Solution: 
- Free tier tunnels expire after 2 hours
- Restart ngrok and update the webhook URL
- Consider upgrading to a paid plan for persistent URLs
```

**Problem: Discord notifications not appearing**
```
Solution:
- Verify DISCORD_TOKEN is correct
- Check channel IDs in .env match your Discord server
- Ensure bot has permissions to send messages
- Check bot is online: docker-compose logs discord-bot
```

**Problem: Port 8080 already in use**
```
Solution:
# Stop conflicting services
sudo lsof -i :8080
# Or change the port in docker-compose.yml
```

## 🔄 Development Workflow

### Typical Development Cycle

1. **Start services**:
   ```bash
   docker-compose up -d
   ```

2. **Start ngrok tunnel**:
   ```bash
   ngrok http 8080
   ```

3. **Update GitHub webhook URL** with the new ngrok URL (if changed)

4. **Make code changes** in `src/`

5. **Restart affected service**:
   ```bash
   docker-compose restart event-gateway
   ```

6. **Test changes** by triggering GitHub events or using the ngrok inspector to replay requests

7. **View logs** to debug:
   ```bash
   docker-compose logs -f event-gateway
   ```

### Hot Reload Development

For faster iteration without Docker:

```bash
# Terminal 1: Start ngrok
ngrok http 3001

# Terminal 2: Start services (except event-gateway)
docker-compose up -d postgres redis qdrant prometheus grafana

# Terminal 3: Run event-gateway in dev mode with hot reload
npm run dev
```

This starts the event gateway on port 3001 with automatic reload on file changes.

## 🔐 Security Best Practices

1. **Never commit secrets**: Keep `.env` in `.gitignore`
2. **Use strong webhook secrets**: Generate with `openssl rand -hex 32`
3. **Verify signatures**: Always validate GitHub webhook signatures
4. **Rotate tokens regularly**: Especially if exposed or for production
5. **Use different tokens**: Separate tokens for dev/staging/prod
6. **Limit bot permissions**: Only grant necessary Discord permissions
7. **Monitor ngrok traffic**: Review requests in the web interface

## 🚀 Next Steps

Once you have webhooks working locally:

1. **Test all webhook events**: PRs, pushes, check runs
2. **Test Discord bot commands**: `/status`, `/deploy`, etc.
3. **Set up GitLens integration**: Configure VS Code tasks
4. **Add custom webhook handlers**: Extend `src/routes/github.ts`
5. **Deploy to production**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)

## 📚 Additional Resources

- [ngrok Documentation](https://ngrok.com/docs)
- [GitHub Webhooks Guide](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
- [Discord.js Documentation](https://discord.js.org/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 💡 Tips & Tricks

### Using ngrok Configuration File

Create `~/.ngrok2/ngrok.yml` for persistent configuration:

```yaml
version: "2"
authtoken: YOUR_AUTH_TOKEN
tunnels:
  event-gateway:
    proto: http
    addr: 8080
    subdomain: strategickhaos-dev  # requires paid plan
  refinory:
    proto: http
    addr: 8085
```

Start multiple tunnels:
```bash
ngrok start event-gateway refinory
```

### Using ngrok with Docker Compose

Add ngrok as a service:

```yaml
services:
  ngrok:
    image: ngrok/ngrok:latest
    environment:
      NGROK_AUTHTOKEN: ${NGROK_AUTHTOKEN}
    command: http event-gateway:8080
    ports:
      - "4040:4040"
    networks:
      - strategickhaos_network
```

### Persistent ngrok URLs (Paid Feature)

If you have a paid ngrok plan:

```bash
# Reserve a domain in the ngrok dashboard
# Then use it consistently
ngrok http 8080 --domain=your-reserved-domain.ngrok-free.app
```

## 🆘 Getting Help

- **Discord Server**: [Join Strategickhaos](https://discord.gg/strategickhaos)
- **GitHub Issues**: [Report bugs or request features](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- **Community**: Read [COMMUNITY.md](COMMUNITY.md) to learn about contributing

---

**Happy coding! 🔥**

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*
