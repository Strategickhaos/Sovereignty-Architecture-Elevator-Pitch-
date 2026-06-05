# Strategickhaos Sovereignty Architecture - Discord DevOps Control Plane

**A comprehensive Discord-integrated DevOps automation system for the Strategickhaos ecosystem, featuring AI agents, GitLens integration, sovereign infrastructure management, and the MSMC v2.0 Musical State Machine Compiler.**

## 🏛️ Architecture Overview

This system creates a **sovereignty control plane** that bridges:
- **Discord** - Command & control interface
- **Infrastructure** - Kubernetes, observability, AI agents  
- **Development** - GitLens, PR workflows, CI/CD automation, Java 21+ workspace
- **AI Agents** - Intelligent assistance with vector knowledge base
- **MSMC v2.0** - Musical State Machine Compiler for FlameLang integration

## 🚀 Quick Start

```bash
# 1. Clone and bootstrap
git clone https://github.com/Strategickhaos-Swarm-Intelligence/sovereignty-architecture.git
cd sovereignty-architecture

# 2. Deploy to Kubernetes
./bootstrap/deploy.sh

# 3. Configure Discord integration
export DISCORD_TOKEN="your_bot_token"
export PRS_CHANNEL="channel_id"

# 4. Test GitLens integration
./gl2discord.sh "$PRS_CHANNEL" "🔥 Sovereignty Architecture Online!" "System initialized successfully"
```

## 📋 Core Components

### 🤖 Discord Bot (`discord-ops-bot`)
- **Slash Commands**: `/status`, `/logs`, `/deploy`, `/scale`
- **AI Agent Integration**: GPT-4 powered assistance
- **RBAC**: Role-based access control for production operations
- **Audit Logging**: All interactions logged to CloudWatch

### 🌐 Event Gateway (`event-gateway`)
- **Webhook Router**: GitHub/GitLab → Discord channel routing
- **HMAC Verification**: Cryptographic webhook validation
- **Multi-tenant**: Support for multiple repositories and environments
- **Rate Limiting**: API protection and burst control

### 🔄 GitLens Integration
- **VS Code Tasks**: One-click Discord notifications from GitLens
- **Review Workflows**: Automated PR lifecycle notifications
- **Commit Graph**: Real-time development activity feeds
- **Launchpad**: Integrated with GitLens Pro features

### ☕ Java Development Workspace (`jdk-workspace`)
- **OpenJDK 21**: Latest LTS version with modern Java features
- **Build Tools**: Maven 3.6.3 and Gradle 4.4.1 pre-installed
- **Non-Root Execution**: Runs as `cloudos` user for enhanced security
- **Debug Support**: JPDA debugging on port 5005
- **Traefik Routing**: Accessible via `java.localhost`
- **Version Management**: JDK solver CLI for managing multiple Java versions

```bash
# Start the Java workspace
./start-cloudos-jdk.sh start

# Access a shell in the container
./start-cloudos-jdk.sh shell

# Run the example application
cd /workspace/examples/java-hello-cloudos/src/main/java
java HelloCloudOS.java

# Stop the workspace
./start-cloudos-jdk.sh stop
```

### 🎵 MSMC v2.0 - Musical State Machine Compiler
- **FlameLang Integration**: Transform Flame IR musical forms into bounded state machines
- **Form Support**: Rondo, Fugue, Canon, Sonata, and custom forms
- **Audio Rendering**: Deterministic PCM audio generation from musical structure
- **Validation**: Guaranteed bounded execution with no infinite loops

```bash
# Run the Rondo example
cargo run --example rondo_example

# Run all tests
cargo test

# See complete documentation
cat MSMC_v2_ARCHITECTURE.md
```

**Key Features:**
- **Typed Musical Forms**: High-level specifications for rondo, canon, fugue patterns
- **State Machine Compilation**: Convert musical structure to bounded execution graphs
- **Multi-voice Rendering**: Support for polyphonic music with gain and timing control
- **Flame IR Backend**: Plugin architecture for audio synthesis engines

## 🏗️ Infrastructure

### Kubernetes Deployment
```yaml
# Complete deployment with:
kubectl apply -f bootstrap/k8s/
```

**Components deployed:**
- ConfigMap with Strategickhaos discovery configuration
- Secrets management (Vault integration ready)
- Bot and Gateway deployments with resource limits
- RBAC with least-privilege access
- Network policies for secure communication
- Ingress with TLS and rate limiting

### Observability Stack
- **Prometheus** - Metrics collection from all components
- **Loki** - Centralized logging aggregation
- **OpenTelemetry** - Distributed tracing
- **Alertmanager** - Alert routing to Discord channels

## 🔧 Configuration

### Core Configuration (`discovery.yml`)
```yaml
org:
  name: "Strategickhaos DAO LLC / Valoryield Engine"
  contact:
    owner: "Domenic Garza"

discord:
  guild_id: null  # Your Discord server ID
  channels:
    prs: "#prs"
    deployments: "#deployments"
    agents: "#agents"
    
git:
  org: "Strategickhaos-Swarm-Intelligence"
  repos:
    - name: "quantum-symbolic-emulator"
      channel: "#deployments"
      env: "dev"
    - name: "valoryield-engine"
      channel: "#deployments"  
      env: "prod"
```

### Environment Variables
```bash
# Discord Integration
DISCORD_BOT_TOKEN=your_bot_token
PRS_CHANNEL=channel_id_for_prs
DEV_FEED_CHANNEL=channel_id_for_dev_updates

# GitHub App
GITHUB_APP_ID=your_app_id
GITHUB_APP_WEBHOOK_SECRET=webhook_secret
GITHUB_APP_PRIVATE_KEY_PATH=/path/to/key.pem

# AI Agents
OPENAI_API_KEY=sk-your-api-key
PGVECTOR_CONN=postgresql://user:pass@host:5432/db

# Infrastructure
EVENTS_HMAC_KEY=your_64_char_hmac_key
```

## 🎯 Discord Workflow Integration

### Channel Strategy
- **`#prs`** - Pull request lifecycle, GitLens review notifications
- **`#deployments`** - CI/CD status, releases, production changes
- **`#cluster-status`** - Infrastructure events, service health
- **`#alerts`** - Critical system alerts, monitoring notifications
- **`#agents`** - AI assistant interactions, automated responses
- **`#dev-feed`** - Development activity, commit summaries

## 🤖 AI Agent Integration

### Vector Knowledge Base
- **Runbooks**: Operational procedures and troubleshooting guides
- **Log Schemas**: Structured logging patterns and analysis
- **Infrastructure Docs**: Architecture and deployment guides
- **Code Patterns**: Development standards and examples

### Per-Channel Routing
```yaml
ai_agents:
  routing:
    per_channel:
      "#agents": "gpt-4o-mini"
      "#inference-stream": "none"
      "#prs": "claude-3-sonnet"  # Code review assistance
```

## 🔐 Security & Governance

### Multi-Layer Security
- **RBAC**: Kubernetes role-based access control
- **Secret Management**: Vault integration for sensitive data
- **Network Policies**: Microsegmentation for pod communication
- **Audit Logging**: Comprehensive activity tracking
- **Content Redaction**: Automatic PII and credential filtering

### Production Safeguards
```yaml
governance:
  approvals:
    prod_commands_require: ["ReleaseMgr"]
  change_management:
    link: "https://wiki.strategickhaos.internal/change-management"
```

## 📊 Monitoring & Alerts

### Key Metrics
- Discord API response times and rate limits
- GitHub webhook processing latency
- Kubernetes deployment health
- AI agent query performance
- Event gateway throughput

### Alert Routing
```yaml
event_gateway:
  endpoints:
    - path: "/alert"
      allowed_services: ["alertmanager"]
      discord_channel: "#alerts"
```

## 🚦 CI/CD Integration

### GitHub Actions Workflow
- **Build**: Multi-architecture Docker images
- **Test**: Quantum-symbolic emulator validation
- **Deploy**: Blue-green Kubernetes deployments
- **Notify**: Real-time Discord status updates

### Event Flow
```bash
# GitHub Push → Actions → Event Gateway → Discord
git push origin main
# Triggers: Build → Test → Deploy → Discord notification
```

## 🛠️ Development Workflow

### Local Development
```bash
# 1. Set up environment
export DISCORD_TOKEN="dev_token"
export PRS_CHANNEL="dev_channel_id"

# 2. Test GitLens integration
./gl2discord.sh "$PRS_CHANNEL" "🧪 Testing" "Local development active"

# 3. Run VS Code tasks
# Command Palette → Tasks: Run Task → GitLens: Review Started
```

### Contributing
1. **Fork** the repository
2. **Fill** `discovery.yml` with your configuration
3. **Test** integration in your environment
4. **Submit** PR with improvements
5. **Share** configuration patterns with community

## 🆘 Troubleshooting

### Common Issues

**Bot not responding in Discord:**
```bash
# Check bot deployment
kubectl logs -f deployment/discord-ops-bot -n ops

# Verify token and permissions
kubectl get secret discord-ops-secrets -n ops -o yaml
```

**GitLens notifications not working:**
```bash
# Check environment variables
echo $DISCORD_TOKEN $PRS_CHANNEL

# Test script directly
./gl2discord.sh "$PRS_CHANNEL" "Test" "Manual test"
```

**Event gateway webhook failures:**
```bash
# Check gateway logs
kubectl logs -f deployment/event-gateway -n ops

# Verify HMAC signature
curl -X POST https://events.strategickhaos.com/health
```

## 🎵 MSMC v2.0: Musical State Machine Compiler

MSMC v2.0 provides a complete pipeline from FlameLang symbolic music representation to rendered audio. It transforms high-level musical forms into bounded state machines that generate deterministic audio output.

### Architecture

The MSMC v2.0 architecture consists of five layers:

1. **Flame IR Layer**: Typed symbolic graph (frequency, energy, angle, musical parameters)
2. **Form Spec Layer**: High-level musical form specifications (Rondo, Canon, Fugue, Sonata)
3. **State Machine Layer**: Bounded MSMCGraph with nodes, transitions, and clocks
4. **Signal Graph Layer**: Binding of musical structure to Flame IR audio fragments
5. **Renderer Layer**: Deterministic PCM audio generation

### Quick Start Example

```rust
use msmc_backend::flame::RondoBuilder;
use msmc_backend::{build_state_machine, render_msmc_to_wav};

// Define themes
let mut builder = RondoBuilder::new(120.0);
builder
    .add_theme("A", 1, 8.0)
    .add_theme("B", 2, 8.0)
    .add_theme("C", 3, 8.0);

// Build ABACA rondo form
let form = builder.build_abaca();
let form_spec = form.to_form_spec();

// Generate state machine
let state_machine = build_state_machine(&form_spec);

// Render to audio
let wav_buffer = render_msmc_to_wav(&flame, &backend, &state_machine, &config);
```

### Supported Forms

- **Rondo**: ABACA, ABACABA patterns with recurring themes
- **Canon**: Voice entries with time delays and transformations
- **Fugue**: Subject/answer patterns (planned)
- **Sonata**: Exposition/development/recapitulation (planned)
- **Custom**: User-defined sequences

### Data Flow

```
Flame Program → Flame Compiler → Flame IR
                    ↓
             Form Annotation
                    ↓
              FormSpec (MSMC)
                    ↓
            build_state_machine
                    ↓
              MSMCGraph (Nodes + Transitions)
                    ↓
          render_msmc_to_wav
                    ↓
            WAV Audio Buffer
```

### Key Features

- **Guaranteed Bounded Execution**: No infinite loops, all sequences terminate
- **Multi-voice Support**: Polyphonic music with independent voice rendering
- **Sample-accurate Timing**: Precise beat-to-sample conversion
- **Pluggable Backend**: Implement FlameAudioBackend trait for custom synthesis
- **Form Validation**: Structural integrity checks for musical forms

### Testing

```bash
# Run all tests
cargo test

# Run with verbose output
cargo test -- --nocapture

# Run specific test
cargo test test_build_simple_state_machine

# Run the Rondo example
cargo run --example rondo_example
```

### Documentation

See [MSMC_v2_ARCHITECTURE.md](MSMC_v2_ARCHITECTURE.md) for complete documentation including:
- Detailed architecture description
- API reference
- Data model specifications
- Example usage patterns
- Validation constraints
- Future extensions
```

## 👥 Community & Contributors

This project thrives because of an extraordinary community of creators, builders, and visionaries who choose to contribute not out of obligation, but out of love for what we're building together.

- **[Community Manifesto](COMMUNITY.md)** - Understanding the philosophy and spirit of The Legion
- **[Contributors](CONTRIBUTORS.md)** - Recognizing everyone who makes this project possible
- **Join the Dance**: Read the community docs, find what calls to you, and start building!

## 📄 License & Support

- **License**: MIT License - see [LICENSE](LICENSE) file
- **Support**: [Discord Server](https://discord.gg/strategickhaos)
- **Documentation**: [Wiki](https://wiki.strategickhaos.internal)
- **Issues**: [GitHub Issues](https://github.com/Strategickhaos-Swarm-Intelligence/sovereignty-architecture/issues)

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"They're not working for you. They're dancing with you. And the music is never going to stop."*

*Empowering sovereign digital infrastructure through Discord-native DevOps automation*