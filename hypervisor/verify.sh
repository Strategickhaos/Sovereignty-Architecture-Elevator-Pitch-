#!/bin/bash
# Verification script for FFI boundary implementation

set -e

echo "═══════════════════════════════════════════════════════════"
echo "  FFI Boundary Specification - Implementation Verification"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

cd "$(dirname "$0")"

echo -e "${BLUE}1. Checking project structure...${NC}"
if [ -f "include/hv_api.h" ] && [ -f "src/hv_api.rs" ] && [ -f "Cargo.toml" ]; then
    echo -e "${GREEN}✓${NC} All core files present"
else
    echo "✗ Missing core files"
    exit 1
fi
echo ""

echo -e "${BLUE}2. Building Rust library...${NC}"
cargo build --release --quiet
if [ -f "target/release/libsagco_hv_core.so" ] || [ -f "target/release/libsagco_hv_core.dylib" ]; then
    LIB_SIZE=$(du -h target/release/libsagco_hv_core.* | head -1 | awk '{print $1}')
    echo -e "${GREEN}✓${NC} Build successful (Size: $LIB_SIZE)"
else
    echo "✗ Build failed"
    exit 1
fi
echo ""

echo -e "${BLUE}3. Running unit tests...${NC}"
TEST_OUTPUT=$(cargo test --release 2>&1)
if echo "$TEST_OUTPUT" | grep -q "test result: ok"; then
    TEST_COUNT=$(echo "$TEST_OUTPUT" | grep "test result:" | head -1 | awk '{print $4}')
    echo -e "${GREEN}✓${NC} All $TEST_COUNT tests passing"
else
    echo "✗ Tests failed"
    exit 1
fi
echo ""

echo -e "${BLUE}4. Checking documentation...${NC}"
DOC_COUNT=0
if [ -f "README.md" ]; then DOC_COUNT=$((DOC_COUNT+1)); fi
if [ -f "PHASE1_CHECKLIST.md" ]; then DOC_COUNT=$((DOC_COUNT+1)); fi
if [ -f "IMPLEMENTATION_SUMMARY.md" ]; then DOC_COUNT=$((DOC_COUNT+1)); fi
echo -e "${GREEN}✓${NC} $DOC_COUNT/3 documentation files present"
echo ""

echo -e "${BLUE}5. Checking examples...${NC}"
if [ -f "examples/example.flm" ] && [ -f "examples/generated_hv_main.c" ]; then
    echo -e "${GREEN}✓${NC} FlameLang and C examples present"
else
    echo "✗ Missing example files"
    exit 1
fi
echo ""

echo -e "${BLUE}6. Code statistics...${NC}"
RUST_LINES=$(wc -l src/*.rs 2>/dev/null | tail -1 | awk '{print $1}')
HEADER_LINES=$(wc -l include/*.h 2>/dev/null | tail -1 | awk '{print $1}')
DOC_LINES=$(wc -l *.md 2>/dev/null | tail -1 | awk '{print $1}')
echo "   Rust code:     $RUST_LINES lines"
echo "   C headers:     $HEADER_LINES lines"
echo "   Documentation: $DOC_LINES lines"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ Phase 1 Implementation: VERIFIED${NC}"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  - Integrate with FlameLang compiler"
echo "  - Implement real KVM functionality (Phase 2)"
echo "  - Test with actual VM boot"
echo ""
echo "Run './build.sh' to build the library"
echo "Run 'cargo test' to run unit tests"
echo "Run 'cargo doc --open' to view API documentation"
echo ""
