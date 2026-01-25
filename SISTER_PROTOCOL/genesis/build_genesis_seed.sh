#!/bin/bash
# build_genesis_seed.sh
# Builds a bootable genesis seed from the Sister Protocol repository

set -e

echo "🌱 Building Genesis Seed for Sister Protocol v1.0.0"
echo "=================================================="

# Configuration
GENESIS_DIR="$(dirname "$0")"
ROOT_DIR="$(dirname "$GENESIS_DIR")"
OUTPUT_DIR="$ROOT_DIR/genesis/output"
SEED_NAME="sister-protocol-genesis-v1.0.0"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo ""
echo "📦 Step 1: Collecting core files..."
# Copy VERSION and DNA_STRAND
cp "$ROOT_DIR/VERSION" "$OUTPUT_DIR/"
cp "$ROOT_DIR/DNA_STRAND.txt" "$OUTPUT_DIR/"

echo "✅ Core files collected"

echo ""
echo "🧬 Step 2: Packaging TRIG6 kernel..."
# Package the TRIG6 kernel
mkdir -p "$OUTPUT_DIR/trig6"
cp "$ROOT_DIR/trig6/trig6_kernel.py" "$OUTPUT_DIR/trig6/"
echo "✅ TRIG6 kernel packaged"

echo ""
echo "🧪 Step 3: Including sample genes..."
# Include representative genes
mkdir -p "$OUTPUT_DIR/trig6/failures"
mkdir -p "$OUTPUT_DIR/trig6/recipes"
mkdir -p "$OUTPUT_DIR/craft_genes"

cp "$ROOT_DIR/trig6/failures/SP_01_7pct_bypass.t6.yaml" "$OUTPUT_DIR/trig6/failures/" || true
cp "$ROOT_DIR/trig6/recipes/RECIPE_NEURO_001.t6.yaml" "$OUTPUT_DIR/trig6/recipes/" || true
cp "$ROOT_DIR/craft_genes/PAPYRUS_001.t6.yaml" "$OUTPUT_DIR/craft_genes/" || true

echo "✅ Sample genes included"

echo ""
echo "📚 Step 4: Including documentation..."
# Include README and key docs
cp "$ROOT_DIR/README.md" "$OUTPUT_DIR/"
cp "$ROOT_DIR/book/THE_SISTER_PROTOCOL_FAILURES_AS_FUEL.md" "$OUTPUT_DIR/" || true

echo "✅ Documentation included"

echo ""
echo "🔐 Step 5: Generating checksums..."
# Generate SHA256 checksums
cd "$OUTPUT_DIR"
find . -type f -exec sha256sum {} \; > SHA256SUMS.txt
echo "✅ Checksums generated"

echo ""
echo "📦 Step 6: Creating archive..."
# Create tarball
cd "$(dirname "$OUTPUT_DIR")"
tar -czf "$SEED_NAME.tar.gz" "$(basename "$OUTPUT_DIR")"

echo "✅ Archive created: $SEED_NAME.tar.gz"

echo ""
echo "=================================================="
echo "🎉 Genesis Seed Build Complete!"
echo ""
echo "Output: genesis/$SEED_NAME.tar.gz"
echo "Size: $(du -h "$SEED_NAME.tar.gz" | cut -f1)"
echo ""
echo "To extract and run:"
echo "  tar -xzf $SEED_NAME.tar.gz"
echo "  cd output"
echo "  python3 trig6/trig6_kernel.py trig6/failures/SP_01_7pct_bypass.t6.yaml"
echo ""
