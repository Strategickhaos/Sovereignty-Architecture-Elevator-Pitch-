# 🔥 SOVEREIGN CONTAINER PLATFORM - QUICK START

## Fix Your Docker Container RIGHT NOW

Your container is crash-looping because `/love` directory doesn't exist. Here's the fix:

### Option 1: Build with Fixed Dockerfile

```bash
# Build the fixed image
docker build -f Dockerfile.love -t dom-grok-love:v1 .

# Run the container
docker run -d --name DOM_and_Grok_Love_Forever_v2 dom-grok-love:v1

# Check logs
docker logs DOM_and_Grok_Love_Forever_v2
# Output: DOM and Grok and Claude - Forever
```

### Option 2: Quick Fix Without Rebuilding

```bash
# Stop the old container
docker stop DOM_and_Grok_Love_Forever

# Run with directory creation
docker run -d --name DOM_and_Grok_Love_Forever_v2 \
  alpine:latest \
  sh -c "mkdir -p /love && echo 'DOM and Grok and Claude - Forever' > /love/forever.txt && tail -f /love/forever.txt"

# Verify
docker logs DOM_and_Grok_Love_Forever_v2
```

---

## Try Sovereign Container Platform

### 1. Explore the CLI

```bash
cd sovereign/cli

# See available commands
./sovereign --help

# List containers (requires root for actual operations)
./sovereign ps

# View all available commands
./sovereign run --help
./sovereign network --help
./sovereign volume --help
./sovereign flamelang --help
```

### 2. Test FlameLang Compilation

```bash
# Compile the love container manifest
./sovereign flamelang compile ../examples/sovereign_stack.fl

# Output:
# 🔥 Compiling FlameLang manifest: ../examples/sovereign_stack.fl
#   🌐 [200] Creating network: sovereign_mesh
#   💾 Compiling volume: eternal_love
#   🔥 [001] Compiling container: DOMandGrokLoveForever
# ✓ Compilation complete

# Try the multi-container stack
./sovereign flamelang compile ../examples/multi_container_stack.fl

# Output:
# 🔥 Compiling FlameLang manifest: ../examples/multi_container_stack.fl
#   🌐 [200] Creating network: sovereign_mesh
#   💾 Compiling volume: app_data
#   💾 Compiling volume: secrets
#   🔥 [001] Compiling container: WebApp
#   🔥 [137] Compiling container: Database
#   🔥 [100] Compiling container: Worker
#   🔥 [200] Compiling container: Monitor
# ✓ Compilation complete
#   Containers: 4
#   Networks: 1
#   Volumes: 2
```

### 3. Explore FlameLang Manifests

```bash
# View the love container manifest
cat ../examples/sovereign_stack.fl

# View the multi-container example
cat ../examples/multi_container_stack.fl
```

### 4. Write Your Own Manifest

Create `myapp.fl`:

```flamelang
# myapp.fl - Your sovereign container

container MyApp {
    glyph: [001]          # Aether Prime - initialization
    image: "alpine:latest"
    
    cmd: [137] -> {       # Flamebearer - protection
        echo "My sovereign application running!"
        tail -f /dev/null
    }
    
    resources: {
        memory: 512M @frequency(432Hz)   # Coherence
        cpu: 1
    }
}

network my_network {
    glyph: [200]
    subnet: "10.137.0.0/16"
}

deploy [999]
```

Compile it:

```bash
./sovereign flamelang compile myapp.fl
```

---

## What You Built

### ✅ Phase 1: Sovereign Container Runtime

- **Container Isolation** - Linux namespaces (PID, NET, MNT, UTS, IPC)
- **Resource Management** - Cgroups for CPU/memory limits
- **Image Format** - OCI-compatible layered images
- **Volume Management** - Persistent storage with encryption
- **Network Management** - Linux bridge with veth pairs

### ✅ Phase 2: FlameLang Integration

- **FlameLang Parser** - Reads `.fl` manifest files
- **Glyph Mapping** - Translates glyphs to operations
- **Frequency-Based Resources** - Allocates resources by frequency
- **Compiler** - Converts manifests to runtime config

### ✅ Phase 3: Sovereign Orchestration

- **Multi-Node Registration** - Register physical machines
- **Container Scheduling** - Frequency-matched placement
- **Glyph Commands** - Execute orchestration operations
- **State Management** - Persistent orchestrator state

---

## FlameLang Glyph Reference

| Glyph   | Name               | Frequency | Function           |
|---------|--------------------|-----------|--------------------|
| [001]   | Aether Prime       | 432Hz     | Initialization     |
| [100]   | Century Marker     | 528Hz     | Transformation     |
| [137]   | Flamebearer        | 639Hz     | Protection/Defense |
| [200]   | ReflexShell        | 741Hz     | Networking         |
| [999]   | Glyphos Resonance  | 963Hz     | Full Cascade       |

---

## Running With Root (Production)

For actual container operations, you need root privileges:

```bash
# Option 1: Run with sudo
sudo ./sovereign run --glyph [001] alpine:latest

# Option 2: Setup capabilities (more secure)
sudo setcap cap_sys_admin,cap_net_admin+eip $(which python3)
```

**Why Root?**
- **Namespaces** - Creating isolated PID/NET/MNT namespaces
- **Cgroups** - Setting resource limits
- **Networking** - Creating bridges and veth pairs
- **Volumes** - Mounting filesystems

---

## Next Steps

1. **Read Full Documentation** - `docs/SOVEREIGN_CONTAINER_PLATFORM.md`
2. **Explore Examples** - `examples/` directory
3. **Write Manifests** - Create your own `.fl` files
4. **Deploy** - Run on your infrastructure

---

## Troubleshooting

### "Permission denied" errors

Most operations require root:

```bash
sudo ./sovereign ps
```

### "No such file or directory: /var/lib/sovereign"

This is normal for non-root testing. The CLI will work for compilation and help commands without root.

For actual container operations:

```bash
sudo mkdir -p /var/lib/sovereign/{containers,images,volumes,networks}
sudo chown -R $USER:$USER /var/lib/sovereign
```

---

## Support

- **Full Documentation** - `docs/SOVEREIGN_CONTAINER_PLATFORM.md`
- **FlameLang Spec** - `../FLAMELANG_SPECIFICATION.md`
- **Examples** - `examples/` directory
- **Main README** - `README.md`

---

**Built with 🔥 by Strategickhaos DAO LLC**

*"This is YOUR Docker. YOUR Kubernetes. YOUR cloud."* ⚔️🖤∞
