# FlameLang WireGuard DNS - Quick Reference Guide

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
cd Sovereignty-Architecture-Elevator-Pitch-

# Test FlameLang components
python3 flamelang_wireguard_dns.py
python3 flamelang_36_tools_integration.py
```

### Create VHD (Linux/macOS)
```bash
chmod +x create_flamelang_vhd.sh
sudo ./create_flamelang_vhd.sh
```

### Create VHD (Windows)
```powershell
# Run as Administrator
.\Create-FlameLangVHD.ps1

# With custom settings
.\Create-FlameLangVHD.ps1 -VHDSizeMB 40960 -VHDFormat VHDX -AttachAfterCreation
```

---

## 📖 Core Concepts

### FlameLang 5-Layer Pipeline

1. **Linguistic** → Meroitic glyphs (23 symbols)
2. **Numeric** → Hex encoding + SHA-256 entropy
3. **Wave** → Physics parameters (frequency, amplitude, phase)
4. **Biological** → DNA codons (ACGT sequences)
5. **Machine** → LLVM IR generation

### Meroitic Glyphs Quick Reference

| Glyph | Operation | Usage |
|-------|-----------|-------|
| 𐦴 | sovereign | All operations start with this |
| 𐦠 | tunnel | WireGuard tunnel operations |
| 𐦡 | query | DNS queries |
| 𐦢 | resolve | DNS resolution |
| 𐦣 | leak | Leak detection |
| 𐦤 | poison | Poisoning detection |
| 𐦥 | encrypt | Encryption |
| 𐦦 | verify | Verification |

**Full list:** See `FLAMELANG_WIREGUARD_DNS_COMPLETE.md` Appendix

---

## 🔒 DNS Security Operations

### Detect DNS Leak
```python
from flamelang_wireguard_dns import WireGuardDNSHardener

hardener = WireGuardDNSHardener()

# Check if query will leak outside tunnel
leak = hardener.detect_dns_leak("example.com", "eth0")
print(f"Leak detected: {leak}")

# Trusted WireGuard interface
leak = hardener.detect_dns_leak("example.com", "wg0")
print(f"Leak detected: {leak}")  # Should be False
```

### Verify DNS Response
```python
response = {
    "domain": "secure.example.com",
    "ip": "203.0.113.50",
    "ttl": 3600
}

verified = hardener.mitigate_dns_poisoning(response)
print(f"Verified: {verified['verified']}")
print(f"DNA Signature: {verified['flamelang_signature'][:16]}...")
```

### Generate Sovereign WireGuard Config
```python
config = {
    "private_key": "YOUR_PRIVATE_KEY_HERE",
    "address": "10.99.0.2/24",
    "dns": "10.99.0.1",
    "peer_key": "PEER_PUBLIC_KEY_HERE",
    "endpoint": "vpn.example.com:51820",
    "allowed_ips": "0.0.0.0/0, ::/0"
}

wg_config = hardener.configure_sovereign_dns(config)

# Save to WireGuard config
with open("/etc/wireguard/wg0.conf", "w") as f:
    f.write(wg_config)
```

---

## 🛠️ Tool Integration

### List Available Tools
```python
from flamelang_36_tools_integration import FlameLangToolConverter, ADVANCED_TOOLS

converter = FlameLangToolConverter()

# Show all 36 tools
for tool in ADVANCED_TOOLS:
    print(f"{tool.id:2d}. {tool.name:20s} [{tool.category.value}]")
```

### Convert Specific Tool
```python
# Convert Sliver C2
sliver = converter.convert_tool(1)
print(f"Tool: {sliver['tool_name']}")
print(f"Layer: {sliver['flamelang_layer']}")
print(f"Functions: {sliver['extracted_functions']}")

# Convert WireGuard-tools
wg = converter.convert_tool(8)
print(f"Deployment: {wg['deployment']}")
```

### Get Tools by Category
```python
from flamelang_36_tools_integration import ToolCategory

# Get all WireGuard tools
wg_tools = converter.get_tools_by_category(ToolCategory.VPN_WIREGUARD)
for tool in wg_tools:
    print(f"- {tool.name}: {tool.description}")

# Get DNS security tools
dns_tools = converter.get_tools_by_category(ToolCategory.DNS_SECURITY)
for tool in dns_tools:
    print(f"- {tool.name}: {tool.description}")
```

### Generate Integration Manifest
```python
# Create JSON manifest of all tools
manifest = converter.generate_integration_manifest()

# Save to file
import json
with open("flamelang_tools_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Manifest created with {manifest['total_tools']} tools")
```

---

## 🔬 Advanced Usage

### Custom DNS Operation
```python
from flamelang_wireguard_dns import DNSOperation, FlameLangCompiler

compiler = FlameLangCompiler()

# Define custom operation
operation = DNSOperation(
    operation="custom_dns_filter",
    params={
        "domains": ["blocked.example.com"],
        "action": "quarantine"
    },
    entropy_level=0.75,
    trust_score=0.85
)

# Compile through all layers
compiled = compiler.compile(operation)

print(f"Linguistic: {compiled['layers']['linguistic']}")
print(f"Wave Freq: {compiled['layers']['wave']['frequency']} Hz")
print(f"DNA: {compiled['layers']['biological'][:32]}...")
print(f"Compression: {compiled['compression_ratio']:.2f}x")
```

### Entropy Calculation
```python
hardener = WireGuardDNSHardener()

# Calculate entropy of DNS query
entropy = hardener._calculate_entropy("suspicious.long.domain.example.com")
print(f"Entropy: {entropy:.3f}")

# Higher entropy = more random/suspicious
if entropy > 0.8:
    print("⚠️  High entropy detected - possible DNS tunneling")
```

### Trust Scoring
```python
# Score different network interfaces
interfaces = ["wg0", "tun0", "eth0", "wlan0"]

for iface in interfaces:
    trust = hardener._calculate_trust(iface)
    print(f"{iface:6s}: Trust = {trust:.2f}")
```

---

## 📦 VHD Deployment

### Linux/macOS VHD Creation
```bash
# Default 20GB VHD
sudo ./create_flamelang_vhd.sh

# Custom size (40GB)
VHD_SIZE=40960 sudo ./create_flamelang_vhd.sh

# VHDX format
VHD_FORMAT=vhdx sudo ./create_flamelang_vhd.sh

# Custom output directory
OUTPUT_DIR=/mnt/storage/vhds sudo ./create_flamelang_vhd.sh
```

### Windows VHD Creation
```powershell
# Default settings
.\Create-FlameLangVHD.ps1

# 40GB VHDX with DevDrive
.\Create-FlameLangVHD.ps1 -VHDSizeMB 40960 -VHDFormat VHDX -CreateDevDrive

# Attach after creation
.\Create-FlameLangVHD.ps1 -AttachAfterCreation
```

### Deploy to VirtualBox
```bash
# Convert to VDI
VBoxManage clonehd flamelang-sovereign-os.vhd flamelang.vdi --format VDI

# Create and configure VM
VBoxManage createvm --name "FlameLang" --register
VBoxManage modifyvm "FlameLang" --memory 2048 --cpus 2
VBoxManage storagectl "FlameLang" --name "SATA" --add sata
VBoxManage storageattach "FlameLang" --storagectl "SATA" \
    --port 0 --device 0 --type hdd --medium flamelang.vdi

# Start VM
VBoxManage startvm "FlameLang"
```

### Deploy to Hyper-V
```powershell
# Use generated script
.\vhd-output\Create-FlameLangVM.ps1

# Or manual creation
New-VM -Name "FlameLang" -MemoryStartupBytes 2GB -Generation 1
Add-VMHardDiskDrive -VMName "FlameLang" -Path ".\flamelang-sovereign-os.vhdx"
Start-VM -Name "FlameLang"
```

---

## 🧪 Testing & Validation

### Run All Tests
```bash
# Test compilation pipeline
python3 flamelang_wireguard_dns.py

# Test tool integration
python3 flamelang_36_tools_integration.py

# Both should end with ✅ success messages
```

### Verify VHD
```bash
# Linux
qemu-img info vhd-output/flamelang-sovereign-os.vhd

# Windows
Test-VHD -Path .\vhd-output\flamelang-sovereign-os.vhdx
```

### Performance Benchmark
```python
import time
from flamelang_wireguard_dns import FlameLangCompiler, DNSOperation

compiler = FlameLangCompiler()
iterations = 1000

start = time.time()
for i in range(iterations):
    op = DNSOperation(
        operation=f"test_{i}",
        params={"index": i},
        entropy_level=0.5,
        trust_score=1.0
    )
    compiler.compile(op)
end = time.time()

print(f"Compiled {iterations} operations in {end-start:.2f}s")
print(f"Average: {(end-start)/iterations*1000:.2f}ms per operation")
```

---

## 🔍 Troubleshooting

### Import Errors
```bash
# Ensure Python 3.7+
python3 --version

# Check if scripts are in current directory
ls -l flamelang_*.py
```

### VHD Creation Fails (Linux)
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install qemu-utils parted e2fsprogs grub2-common

# Check available space
df -h .

# Run with verbose logging
bash -x ./create_flamelang_vhd.sh
```

### VHD Creation Fails (Windows)
```powershell
# Ensure running as Administrator
[Security.Principal.WindowsIdentity]::GetCurrent().Groups -contains 'S-1-5-32-544'

# Check Hyper-V
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V

# Enable Hyper-V if needed
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

### VM Won't Boot
- Use Generation 1 VMs for compatibility
- Disable Secure Boot
- Allocate at least 2GB RAM
- Check VHD integrity with Test-VHD (Windows) or qemu-img check (Linux)

---

## 📚 Additional Resources

- **Full Documentation:** `FLAMELANG_WIREGUARD_DNS_COMPLETE.md`
- **FlameLang Spec:** `FLAMELANG_SPECIFICATION.md`
- **DNS Configuration:** `TLS_DNS_CONFIG.md`
- **Repository:** https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-

---

## 🔑 Key Takeaways

1. **120x Compression:** Dense Meroitic encoding achieves massive compression
2. **5 Layers:** Each layer adds security and optimization
3. **36 Tools:** All major security tools integrated
4. **Zero-Trust DNS:** All queries verified before tunnel routing
5. **Codon Verification:** DNA-based immutable execution
6. **Entropy Detection:** Automatic anomaly detection
7. **Pure Sovereign:** No external dependencies
8. **Bootable VHD:** Complete OS in a virtual disk

---

**🔥 Reignite. Trust nothing until it survives 100-angle crossfire.**
