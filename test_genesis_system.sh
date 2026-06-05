#!/bin/bash
# End-to-end test of the Genesis System

set -e

echo "═══════════════════════════════════════════════════════"
echo "   GENESIS SYSTEM END-TO-END TEST"
echo "═══════════════════════════════════════════════════════"
echo ""

# Clean up any previous test
echo "🧹 Cleaning up previous test..."
rm -rf /tmp/test-synapse-bus-core
rm -f /tmp/test-blueprint.yaml

# Step 1: Generate repository structure
echo ""
echo "Step 1: Running genesis.py..."
cd /home/runner/work/Sovereignty-Architecture-Elevator-Pitch-/Sovereignty-Architecture-Elevator-Pitch-
python3 genesis.py

# Verify structure created
if [ -d "synapse-bus-core" ]; then
    echo "✅ Repository structure created"
else
    echo "❌ Failed to create repository structure"
    exit 1
fi

# Step 2: Test ingestion valve
echo ""
echo "Step 2: Testing ingestion valve..."
cat > /tmp/test_chat_dump.txt << 'EOF'
This is the Genesis Architecture for the SynapseBus-Core.

References:
- INV-076: GSCH Framework
- Board Meeting 003
- Ripley Gate 2 (Solution)

Directory structure:
- src/claims/gsch_claim8.rs: "ref: INV-076, Patent Claim 8"

TASK: Implement GSCH primitives
EOF

python3 scripts/ingest_chat.py /tmp/test_chat_dump.txt
if [ -f "blueprint.yaml" ]; then
    echo "✅ Blueprint generated"
else
    echo "❌ Failed to generate blueprint"
    exit 1
fi

# Step 3: Test hydration
echo ""
echo "Step 3: Testing mason agent..."
cd synapse-bus-core
TARGET_DIR=. python3 ../scripts/hydrate_file.py

# Verify hydrated files exist
if [ -f "src/claims/gsch_claim8.rs" ]; then
    echo "✅ Files hydrated"
    echo ""
    echo "Sample hydrated file:"
    head -20 src/claims/gsch_claim8.rs
else
    echo "❌ Failed to hydrate files"
    exit 1
fi

# Step 4: Verify workflows
echo ""
echo "Step 4: Verifying workflows..."
cd ..
if [ -f ".github/workflows/thermodynamics.yaml" ] && [ -f ".github/workflows/ripley-gates.yaml" ]; then
    echo "✅ Workflows present"
else
    echo "❌ Workflows missing"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "   ✅ ALL TESTS PASSED"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Genesis System is fully operational!"
echo ""
echo "Next steps:"
echo "1. cd synapse-bus-core"
echo "2. docker-compose up mason  # Hydrate more files"
echo "3. docker-compose up builder # Build containers"
