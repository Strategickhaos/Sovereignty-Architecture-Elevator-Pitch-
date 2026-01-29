# TRIG6/KHAOS Quick Start Guide

## What is TRIG6?

TRIG6 (Trigonometric Reasoning and Inference Geometric Engine) is a sovereign computational mathematics engine with **zero vendor lock-in** and **no external dependencies**. It provides:

- ✅ Offline trigonometric calculations (bridle operations)
- ✅ Health monitoring and metrics for observability
- ✅ Logical fallacy detection for debate validation
- ✅ Citation system for governance and audit

## Quick Test

```bash
# Test version
python3 trig6/trig6.py version

# Calculate sin/cos/tan for 45 degrees
python3 trig6/trig6.py bridle --angle 45 --json

# Run health check
python3 trig6/doctor.py

# Check for logical fallacies
python3 trig6/fallacy.py "Everyone knows this is true"
```

## Docker Usage

```bash
# Build image
docker build -f Dockerfile.trig6 -t strategickhaos/trig6:latest .

# Run health check
docker run --rm strategickhaos/trig6:latest python3 /app/trig6/doctor.py

# Calculate angles
docker run --rm strategickhaos/trig6:latest \
  python3 /app/trig6/trig6.py bridle --angle 90 --json
```

## Docker Compose

```bash
# Start all services including TRIG6
docker-compose up -d

# Check TRIG6 health
docker exec trig6-engine python3 /app/trig6/doctor.py

# Run calculations
docker exec trig6-engine python3 /app/trig6/trig6.py bridle --angle 30 --json
```

## SAGCO Bootloader

The SAGCO (Sovereign Architecture Governance & Configuration Orchestrator) bootloader validates your runtime environment:

```bash
# Run bootloader
bash bootstrap/sagco/bootloader.sh

# View boot manifest
cat bootstrap/sagco/boot_manifest.json
```

## Proof Generation

Generate irrefutable proof of integration:

```bash
# Run proof protocol
bash generate-proof.sh

# View proof summary
cat proof_artifacts/proof_summary.txt

# Check hash
sha256sum proof.tar.gz
```

## KHAOS Glyphs

Access symbolic glyphs for AI operations:

```bash
# View all glyphs
python3 -c "import json; data = json.load(open('data/khaos/glyphs.json')); print(json.dumps(data['glyphs'], indent=2))"

# Read the KHAOS hymn
cat data/khaos/hymn.md
```

## Integration Points

### With Discord Bot
```python
# Example slash command integration
@bot.command()
async def trig6(ctx, angle: float):
    result = subprocess.run(
        ["python3", "trig6/trig6.py", "bridle", "--angle", str(angle), "--json"],
        capture_output=True, text=True
    )
    await ctx.send(f"```json\n{result.stdout}\n```")
```

### With Monitoring
```python
# Prometheus metrics integration
from trig6.doctor import Doctor

doctor = Doctor()
metrics = doctor.run()["metrics"]
# metrics["trig6_health_status"] -> 1 (healthy) or 0 (unhealthy)
```

### With AI Agents
```python
# Fallacy detection in arguments
from trig6.fallacy import FallacyDetector

detector = FallacyDetector()
result = detector.check("Your argument text here")
print(result["recommendation"])
```

## Architecture

```
trig6/
├── trig6.py           # Main CLI
├── doctor.py          # Health checks
├── fallacy.py         # Debate engine
├── constants/         # Mathematical constants
│   └── mathematical_constants.json
└── __init__.py

data/khaos/
├── glyphs.json        # Symbolic glyphs
└── hymn.md           # KHAOS anthem

bootstrap/sagco/
├── bootloader.sh      # Runtime validator
└── boot_manifest.json # Boot state
```

## Sovereignty Guarantees

- **Zero Dependencies**: Uses only Python stdlib
- **No Network Calls**: Fully offline operation
- **No Vendor Lock-in**: Standard formats (JSON, Python)
- **Audit Ready**: Citation system for compliance
- **Self-Validating**: Health checks and doctor module

## Support

For full documentation, see [TRIG6_INTEGRATION.md](TRIG6_INTEGRATION.md)

---

**Status**: ✅ OPERATIONAL  
**Sovereignty Level**: SOVEREIGN  
**Vendor Lock-in**: ZERO
