#!/bin/bash
# Build script for SAGCO Hypervisor Core

set -e

echo "🔥 Building SAGCO Hypervisor Core..."

# Check if we're in the hypervisor directory
if [ ! -f "Cargo.toml" ]; then
    echo "Error: Must be run from hypervisor directory"
    exit 1
fi

# Build the Rust library
echo "📦 Building Rust library..."
cargo build --release

echo ""
echo "✅ Build complete!"
echo ""
echo "Library location:"
if [ -f "target/release/libsagco_hv_core.so" ]; then
    echo "  target/release/libsagco_hv_core.so"
elif [ -f "target/release/libsagco_hv_core.dylib" ]; then
    echo "  target/release/libsagco_hv_core.dylib"
elif [ -f "target/release/sagco_hv_core.dll" ]; then
    echo "  target/release/sagco_hv_core.dll"
fi
echo ""
echo "To test with example C code:"
echo "  gcc -o hv_test examples/generated_hv_main.c -L target/release -l sagco_hv_core -I include"
echo "  LD_LIBRARY_PATH=target/release ./hv_test"
