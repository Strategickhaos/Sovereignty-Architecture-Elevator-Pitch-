# Sovereign Container Examples

This directory contains example FlameLang manifests demonstrating the sovereign container infrastructure.

## 📋 Available Examples

### 1. eternal_love.fl
**The Original - Fixed Crash-Loop Issue**

Demonstrates:
- Proper directory initialization with `mkdir -p /love`
- Volume mounting
- Glyph [001] Aether Prime initialization
- Coherence frequency (432Hz) resource allocation

```bash
python3 ../../flamelang_container_compiler.py eternal_love.fl
```

### 2. web_server.fl
**Simple Web Server**

Demonstrates:
- Installing packages in containers
- Running a Python HTTP server
- Glyph [100] Compiler Core transformation
- Transformation frequency (528Hz)

```bash
python3 ../../flamelang_container_compiler.py web_server.fl
```

### 3. multi_container_stack.fl
**Multi-Container Stack with Full Cascade**

Demonstrates:
- Multiple containers in a single manifest
- Database, Application, and Frontend tiers
- Shared network configuration
- Glyph [999] Glyphos Resonance full cascade deployment
- Different frequencies for different workloads

```bash
python3 ../../flamelang_container_compiler.py multi_container_stack.fl
```

## 🔥 FlameLang Glyph Reference

| Glyph | Name | Frequency | Purpose |
|-------|------|-----------|---------|
| [001] | Aether Prime | 432Hz | Initialization, coherence |
| [100] | Compiler Core | 528Hz | Transformation, compilation |
| [137] | Flamebearer | 528Hz | Protection, security |
| [200] | ReflexShell | 432Hz | Networking, connectivity |
| [999] | Glyphos Resonance | 963Hz | Full cascade deployment |

## 🚀 Usage Patterns

### Single Container Deployment
Use glyph [001] for controlled, single-container initialization:
```flamelang
deploy [001]
```

### Multi-Container Cascade
Use glyph [999] to deploy all containers across the cluster:
```flamelang
deploy [999]
```

## 📊 Resource Allocation by Frequency

### 432Hz - Coherence
- Memory: 256M - 512M
- CPU: 0.5 - 1 core
- Use for: Frontend, static content, initialization

### 528Hz - Transformation  
- Memory: 512M - 2G
- CPU: 1 - 2 cores
- Use for: Application logic, compilation, processing

### 963Hz - Cascade
- Memory: 2G - 4G
- CPU: 2 - 4 cores
- Use for: Orchestration, distributed operations

## 🛡️ Security Patterns

### Protected Data (Glyph [137] Flamebearer)
For sensitive data like databases:
```flamelang
container SecureDatabase {
    glyph: [137]
    # Flamebearer provides enhanced security
}
```

### Encrypted Volumes
For maximum security:
```flamelang
volumes: [
    "/secure" -> sovereign_volume("encrypted_data", encrypted=true)
]
```

## 🔧 Testing Manifests

Compile any manifest to see the generated configuration:

```bash
# Compile manifest
python3 ../../flamelang_container_compiler.py eternal_love.fl

# Output shows:
# - Container specifications
# - Network configurations  
# - Resource allocations
# - Deployment strategy
```

## 💡 Best Practices

1. **Always use mkdir -p** - Prevent crash-loops from missing directories
2. **Match frequency to workload** - Lower for static, higher for dynamic
3. **Use appropriate glyphs** - [137] for security, [100] for processing
4. **Cascade carefully** - [999] deploys everywhere, use [001] for testing
5. **Volume everything important** - Containers are ephemeral

## 🖤 The Sovereign Way

> "BABY, THIS IS BEAUTIFUL AND YES WE CAN BUILD THIS" 🔥⚔️🖤

These manifests demonstrate:
- ✅ No Docker dependency
- ✅ No Kubernetes complexity
- ✅ FlameLang simplicity
- ✅ Glyph-based orchestration
- ✅ Complete sovereignty

**Build your own. Modify freely. Own completely.** 🔥
