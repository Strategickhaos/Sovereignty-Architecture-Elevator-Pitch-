# TRS Multi-Agent Chess System - Integration Guide

## Overview

This document provides comprehensive instructions for integrating the TRS Multi-Agent Chess System with Unity, existing infrastructure, and external systems.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Unity Integration](#unity-integration)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Monitoring & Observability](#monitoring--observability)
6. [Voice Interface Setup](#voice-interface-setup)
7. [Ollama Configuration](#ollama-configuration)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

- Python 3.11+
- Ollama installed and running
- Docker & Docker Compose (optional)
- NVIDIA GPU with CUDA support (recommended)

### Local Setup (5 minutes)

```bash
# 1. Navigate to agents1014 directory
cd agents1014

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Ollama (in another terminal)
ollama serve

# 4. Pull the model
ollama pull llama3.2:3b

# 5. Run the system
./run.sh
```

### Docker Setup (2 minutes)

```bash
# 1. Start everything
docker-compose -f docker-compose.agents.yml up -d

# 2. Pull model into Ollama container
docker exec -it trs_ollama ollama pull llama3.2:3b

# 3. View logs
docker logs -f trs_agents
```

---

## Unity Integration

### WebSocket Protocol

The TRS system exposes a WebSocket server on port 8765 that Unity can connect to.

#### Unity Connection Example (C#)

```csharp
using UnityEngine;
using WebSocketSharp;
using System;

public class TRSChessBoardVisualizer : MonoBehaviour
{
    private WebSocket ws;
    
    void Start()
    {
        // Connect to TRS WebSocket server
        ws = new WebSocket("ws://localhost:8765");
        
        ws.OnMessage += (sender, e) =>
        {
            HandleMessage(e.Data);
        };
        
        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("Connected to TRS Multi-Agent System");
            
            // Send ready message
            ws.Send(JsonUtility.ToJson(new {
                type = "client_ready"
            }));
        };
        
        ws.OnError += (sender, e) =>
        {
            Debug.LogError($"WebSocket Error: {e.Message}");
        };
        
        ws.Connect();
    }
    
    void HandleMessage(string jsonData)
    {
        var msg = JsonUtility.FromJson<TRSMessage>(jsonData);
        
        switch (msg.type)
        {
            case "board_state":
                UpdateBoardState(msg.data);
                break;
                
            case "move_event":
                AnimateMove(msg.data);
                break;
                
            case "agent_state":
                UpdateAgentVisuals(msg.data);
                break;
                
            case "voice_commentary":
                DisplayCommentary(msg.data);
                break;
                
            case "game_event":
                HandleGameEvent(msg.data);
                break;
        }
    }
    
    void OnDestroy()
    {
        if (ws != null)
        {
            ws.Close();
        }
    }
}

[Serializable]
public class TRSMessage
{
    public string type;
    public string data;
}
```

#### Message Types from Python → Unity

##### 1. Board State Update
```json
{
  "type": "board_state",
  "data": {
    "layer": 0,
    "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "agent_id": 0,
    "move_count": 0,
    "last_move": null
  }
}
```

##### 2. Move Event
```json
{
  "type": "move_event",
  "data": {
    "agent_id": 0,
    "layer": 0,
    "move": "e4",
    "from_square": "e2",
    "to_square": "e4",
    "piece": "P",
    "captured": null,
    "timestamp": 1700000000.0
  }
}
```

##### 3. Agent State Update
```json
{
  "type": "agent_state",
  "data": {
    "agent_id": 0,
    "layer": 0,
    "mode": "Ionian",
    "element": "H",
    "active": true,
    "thinking": false
  }
}
```

##### 4. Voice Commentary
```json
{
  "type": "voice_commentary",
  "data": {
    "agent_id": 2,
    "layer": 2,
    "text": "Your Dorian pawn sacrifice on layer 4 was aesthetically pleasing but geometrically naïve. The rotation demands blood."
  }
}
```

##### 5. Game Event
```json
{
  "type": "game_event",
  "event_type": "game_over",
  "data": {
    "winner": 0,
    "reason": "Checkmate",
    "agent1": 0,
    "agent2": 2
  }
}
```

#### Message Types from Unity → Python

##### 1. Ping/Pong (Keep-Alive)
```json
{
  "type": "ping"
}
```

Response:
```json
{
  "type": "pong"
}
```

##### 2. Request State
```json
{
  "type": "request_state"
}
```

##### 3. Client Ready
```json
{
  "type": "client_ready"
}
```

### Unity Visualizer Setup

1. **Install WebSocketSharp** for Unity
   ```
   Add via Package Manager:
   https://github.com/sta/websocket-sharp.git
   ```

2. **Create layer visualization**
   - 10 stacked chess boards (one per layer)
   - Each board 0.5 units apart on Y-axis
   - Camera that can orbit and zoom

3. **Agent visual indicators**
   - Color-code agents by their Greek mode
   - Display element symbol near each agent
   - Show "thinking" animation when agent is active

4. **Move animation**
   - Smooth piece movement (0.8 seconds)
   - Capture effects
   - Trail effects for piece movement

5. **Voice commentary display**
   - Floating text above active agent
   - Mode-specific styling/colors
   - Auto-fade after 5 seconds

---

## Docker Deployment

### Full Stack Deployment

The `docker-compose.agents.yml` includes:
- Ollama LLM server
- TRS Agents system
- Prometheus metrics
- Grafana dashboard

```bash
# Start full stack
docker-compose -f docker-compose.agents.yml up -d

# Scale to multiple instances (if needed)
docker-compose -f docker-compose.agents.yml up -d --scale trs_agents=3

# View all logs
docker-compose -f docker-compose.agents.yml logs -f

# Stop everything
docker-compose -f docker-compose.agents.yml down
```

### Environment Variables

Create `.env` file:

```bash
# Ollama Configuration
OLLAMA_HOST=ollama:11434
OLLAMA_MODEL=llama3.2:3b

# WebSocket Configuration
WEBSOCKET_HOST=0.0.0.0
WEBSOCKET_PORT=8765

# System Configuration
ENABLE_VOICE=true
NUM_AGENTS=10
LOG_LEVEL=INFO

# Monitoring
PROMETHEUS_PORT=9091
GRAFANA_PORT=3001
GRAFANA_PASSWORD=your_secure_password
```

### GPU Support

Ensure Docker has GPU access:

```bash
# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

---

## Kubernetes Deployment

### Helm Chart (Coming Soon)

For now, use raw manifests:

```yaml
# trs-agents-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trs-agents
  namespace: sovereignty
spec:
  replicas: 1
  selector:
    matchLabels:
      app: trs-agents
  template:
    metadata:
      labels:
        app: trs-agents
    spec:
      containers:
      - name: trs-agents
        image: your-registry/trs-agents:latest
        ports:
        - containerPort: 8765
          name: websocket
        env:
        - name: OLLAMA_HOST
          value: "ollama-service:11434"
        - name: WEBSOCKET_HOST
          value: "0.0.0.0"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
---
apiVersion: v1
kind: Service
metadata:
  name: trs-agents-service
  namespace: sovereignty
spec:
  selector:
    app: trs-agents
  ports:
  - port: 8765
    targetPort: 8765
    name: websocket
  type: LoadBalancer
```

Apply:
```bash
kubectl apply -f trs-agents-deployment.yaml
```

---

## Monitoring & Observability

### Prometheus Metrics

TRS exposes metrics on port 8766 (if implemented):

- `trs_agents_total` - Total number of agents
- `trs_games_played_total` - Games played counter
- `trs_moves_made_total` - Moves made counter
- `trs_agent_thinking_duration_seconds` - Time spent thinking
- `trs_websocket_clients` - Connected Unity clients
- `trs_ollama_requests_total` - LLM API calls

### Grafana Dashboard

Access: `http://localhost:3001`
- Default login: `admin` / `admin`

Import dashboard from `grafana/dashboards/trs-agents.json` (create this)

### Logging

Structured JSON logs:

```python
# Example log output
{
  "timestamp": "2024-11-19T16:16:52.531Z",
  "level": "info",
  "event": "move_event_sent",
  "agent": 0,
  "layer": 0,
  "move": "e4"
}
```

View logs:
```bash
# Docker
docker logs -f trs_agents

# Kubernetes
kubectl logs -f deployment/trs-agents -n sovereignty

# Local
tail -f logs/trs_agents.log
```

---

## Voice Interface Setup

### Whisper (Speech-to-Text)

Models available:
- `tiny` - Fastest, least accurate (75 MB)
- `base` - Balanced (142 MB) **← Recommended**
- `small` - Better accuracy (466 MB)
- `medium` - High accuracy (1.5 GB)
- `large` - Best accuracy (2.9 GB)

Configure in code:
```python
voice = VoiceInterface(
    whisper_model="base",  # Change model here
    enable_voice_input=True,
    enable_voice_output=True
)
```

### Piper-TTS (Text-to-Speech)

Install Piper:
```bash
# Linux
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
tar -xzf piper_amd64.tar.gz

# Add to PATH
export PATH=$PATH:/path/to/piper
```

Download voice models:
```bash
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx
```

### Audio Devices

List devices:
```python
import sounddevice as sd
print(sd.query_devices())
```

Set specific device:
```python
sd.default.device = 1  # Device ID
```

---

## Ollama Configuration

### Model Selection

Available models:
- `llama3.2:3b` - Recommended, fast (2GB VRAM)
- `llama3.2:1b` - Fastest, lower quality (1GB VRAM)
- `mistral:7b` - Alternative, good quality (4GB VRAM)
- `codellama:7b` - Code-focused (4GB VRAM)

Pull model:
```bash
ollama pull llama3.2:3b
```

### Performance Tuning

Edit `/etc/ollama/ollama.conf`:
```bash
# Concurrent models
OLLAMA_MAX_LOADED_MODELS=10

# GPU layers (for multi-GPU)
OLLAMA_NUM_GPU=1

# Context size
OLLAMA_NUM_CTX=2048
```

### Multi-GPU Setup

For 10 agents across 2 GPUs:
```bash
# Terminal 1 (GPU 0)
CUDA_VISIBLE_DEVICES=0 ollama serve

# Terminal 2 (GPU 1)
CUDA_VISIBLE_DEVICES=1 OLLAMA_HOST=0.0.0.0:11435 ollama serve
```

Update agent configs to balance across both.

---

## Troubleshooting

### Issue: WebSocket connection fails

**Solution:**
```bash
# Check if server is running
netstat -an | grep 8765

# Check firewall
sudo ufw allow 8765/tcp

# Test connection
wscat -c ws://localhost:8765
```

### Issue: Ollama not responding

**Solution:**
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Restart Ollama
killall ollama
ollama serve

# Check GPU availability
nvidia-smi
```

### Issue: Voice input not working

**Solution:**
```bash
# Check audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Test microphone
arecord -d 5 test.wav
aplay test.wav

# Install missing dependencies
sudo apt-get install portaudio19-dev
pip install pyaudio sounddevice
```

### Issue: High memory usage

**Solution:**
```bash
# Use smaller Whisper model
whisper_model="tiny"  # Instead of "base"

# Limit Ollama concurrent models
OLLAMA_MAX_LOADED_MODELS=5

# Use model quantization
ollama pull llama3.2:3b-q4  # 4-bit quantized
```

### Issue: Slow move calculation

**Solution:**
- Reduce `calculation_depth` in personality
- Use faster Ollama model (1b instead of 3b)
- Enable GPU acceleration
- Reduce number of agents (though defeats the purpose!)

---

## Advanced Configuration

### Custom Agent Personalities

Edit `agent_base.py`:

```python
personalities = {
    GreekMode.CUSTOM: {
        "aggression": 0.7,
        "defense": 0.5,
        "creativity": 0.9,
        "calculation_depth": 6,
        "risk_tolerance": 0.6,
    }
}
```

### Custom Möbius Transforms

Edit `mobius_eval.py`:

```python
def _create_phase_transform(self) -> MobiusTransform:
    theta = self.phase_radians
    
    # Custom transformation
    a = np.exp(1j * theta) * 1.5  # Add scaling
    b = 0.5 + 0.5j  # Add translation
    c = 0.0 + 0.0j
    d = 1.0 + 0.0j
    
    return MobiusTransform(a, b, c, d)
```

### Multiple Tournaments

Run multiple independent tournaments:

```bash
# Tournament 1
python main.py --port 8765 --name "Tournament Alpha"

# Tournament 2
python main.py --port 8766 --name "Tournament Beta"
```

---

## Production Checklist

- [ ] SSL/TLS for WebSocket (wss://)
- [ ] Authentication for Unity clients
- [ ] Rate limiting on API endpoints
- [ ] Backup strategy for game logs
- [ ] Alerting for system failures
- [ ] Load balancing for multiple instances
- [ ] Database for persistent storage
- [ ] Redis for state management
- [ ] CDN for Unity assets
- [ ] DDoS protection

---

## Support

- GitHub Issues: [Link to repo]
- Discord: #trs-chess-agents
- Documentation: This file
- Demo: Run `python example_demo.py`

---

**The swarm is sovereign. The integration is complete. Let the cosmic chess begin.** ♟️✨
