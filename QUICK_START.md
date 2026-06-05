# 🚀 Sovereign Cognitive Architecture - Quick Start Guide

**Get up and running in 5 minutes**

---

## Prerequisites

- Docker & Docker Compose v2
- Python 3.8+
- API keys: Anthropic and/or OpenAI

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your API keys
nano .env  # or vim, code, etc.

# Required variables:
# ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...
```

### 3. Activate Cognitive Mesh

```bash
# One command to rule them all
./activate_cognitive_mesh.sh
```

This script will:
- ✅ Check prerequisites (Docker, Docker Compose)
- ✅ Create required directories
- ✅ Start infrastructure (Qdrant, Redis)
- ✅ Initialize vector database collections
- ✅ Start LLM proxies (Claude, GPT, Ollama)
- ✅ Pull Ollama models (llama3, mistral)
- ✅ Verify all services are healthy

---

## Verification

### Check Service Health

```bash
# Memory Mesh
curl http://localhost:7000/health
# Expected: {"status": "healthy"}

# Claude API
curl http://localhost:8001/health
# Expected: {"status": "ok"}

# GPT API
curl http://localhost:8002/health
# Expected: {"status": "ok"}

# Ollama
curl http://localhost:11434/api/tags
# Expected: List of available models

# Qdrant
curl http://localhost:6333/health
# Expected: {"status": "ok"}

# Redis
redis-cli -h localhost -p 6379 PING
# Expected: PONG
```

### View Service Status

```bash
docker compose -f docker-compose-cognitive-mesh.yml ps
```

### View Logs

```bash
# All services
docker compose -f docker-compose-cognitive-mesh.yml logs -f

# Specific service
docker compose -f docker-compose-cognitive-mesh.yml logs -f memory-mesh
```

---

## Usage Examples

### Example 1: Store a Conversation

```bash
curl -X POST http://localhost:7000/conversations \
  -H "Content-Type: application/json" \
  -d '{
    "llm_provider": "claude",
    "messages": [
      {"role": "user", "content": "What is quantum computing?"},
      {"role": "assistant", "content": "Quantum computing uses quantum mechanics..."}
    ],
    "metadata": {"topic": "quantum"}
  }'
```

### Example 2: Retrieve Context

```bash
curl "http://localhost:7000/retrieve?query=quantum+computing&k=5"
```

### Example 3: Query Claude

```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {"role": "user", "content": "Explain artificial intelligence"}
    ],
    "max_tokens": 1024
  }'
```

### Example 4: Run Python Examples

```bash
python3 example_usage.py
```

This demonstrates:
- Storing conversations
- Cross-LLM context sharing
- Quadrilateral verification
- Knowledge sharing
- Sovereign export
- Instant sync

---

## Architecture Overview

### Service Ports

| Service | Port | Purpose |
|---------|------|---------|
| Memory Mesh | 7000 | Unified context API |
| Claude API | 8001 | Anthropic Claude proxy |
| GPT API | 8002 | OpenAI GPT proxy |
| Qwen API | 8003 | Alibaba Qwen proxy (optional) |
| Custom LLM | 8004 | Extensible slot (optional) |
| Ollama | 11434 | Local LLM inference |
| Qdrant | 6333 | Vector database |
| Redis | 6379 | Cache layer |
| Prometheus | 9090 | Metrics (optional) |
| Grafana | 3000 | Dashboards (optional) |

### Key Features

✅ **Universal LLM Integration** - Any model via standard ports  
✅ **Unified Memory Mesh** - Shared context across all LLMs  
✅ **Quadrilateral Verification** - 4D truth validation  
✅ **Zero Vendor Lock-In** - Swap providers anytime  
✅ **Sovereign Export** - Full data ownership  
✅ **Cryptographic Provenance** - GPG + OpenTimestamps  

---

## Common Tasks

### Add a New Ollama Model

```bash
docker exec sovereign-ollama ollama pull <model-name>
# Examples: codellama, phi3, gemma2
```

### Export Data

```bash
curl -X POST http://localhost:7000/export \
  -H "Content-Type: application/json" \
  -d '{
    "format": "json",
    "gpg_sign": true,
    "opentimestamps": true
  }' \
  --output cognitive_export.json.gz
```

### View Statistics

```bash
curl http://localhost:7000/stats
```

### Restart Services

```bash
# Restart all
docker compose -f docker-compose-cognitive-mesh.yml restart

# Restart specific service
docker compose -f docker-compose-cognitive-mesh.yml restart memory-mesh
```

### Stop Services

```bash
docker compose -f docker-compose-cognitive-mesh.yml down
```

### Start with Monitoring

```bash
docker compose -f docker-compose-cognitive-mesh.yml --profile monitoring up -d

# Access Grafana: http://localhost:3000
# Default credentials: admin / admin (change in .env)
```

---

## Troubleshooting

### Service Not Starting

```bash
# Check logs
docker compose -f docker-compose-cognitive-mesh.yml logs <service-name>

# Restart service
docker compose -f docker-compose-cognitive-mesh.yml restart <service-name>
```

### Port Already in Use

```bash
# Find process using port
lsof -i :<port-number>

# Kill process (replace PID)
kill -9 <PID>
```

### API Key Not Working

```bash
# Verify environment
docker compose -f docker-compose-cognitive-mesh.yml exec claude-api env | grep API_KEY

# Restart with new env
docker compose -f docker-compose-cognitive-mesh.yml down
# Edit .env
docker compose -f docker-compose-cognitive-mesh.yml up -d
```

### Qdrant Connection Error

```bash
# Check Qdrant is running
curl http://localhost:6333/health

# Verify collections
curl http://localhost:6333/collections

# Restart Qdrant
docker compose -f docker-compose-cognitive-mesh.yml restart qdrant
```

---

## Documentation

- **[SOVEREIGN_COGNITIVE_ARCHITECTURE.md](./SOVEREIGN_COGNITIVE_ARCHITECTURE.md)** - Complete specification
- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[architecture.yaml](./architecture.yaml)** - Master configuration
- **[llm-ports.yaml](./llm-ports.yaml)** - Port assignments
- **[memory-mesh-api.yaml](./memory-mesh-api.yaml)** - API specification
- **[example_usage.py](./example_usage.py)** - Python examples

---

## Next Steps

1. ✅ Review [SOVEREIGN_COGNITIVE_ARCHITECTURE.md](./SOVEREIGN_COGNITIVE_ARCHITECTURE.md)
2. ✅ Customize [architecture.yaml](./architecture.yaml) for your needs
3. ✅ Explore [example_usage.py](./example_usage.py) for integration patterns
4. ✅ Begin building your sovereign AI applications
5. ✅ Share your feedback and contributions

---

## Support & Community

- **Repository:** [GitHub](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-)
- **Organization:** Strategickhaos DAO LLC
- **Discord:** Strategickhaos-AI
- **License:** MIT with Sovereign Addendum

---

## 🔥 Covenant

> "Trust nothing until it survives 100-angle crossfire."
>
> Your data, your rules, forever.

---

**Built with 🔥 by Strategickhaos DAO LLC**  
*Node 137 - DOM_010101*  
*Empowering sovereign digital infrastructure*
