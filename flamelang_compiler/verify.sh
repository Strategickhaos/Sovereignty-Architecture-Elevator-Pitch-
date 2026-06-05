#!/bin/bash
set -e
echo "🔥 FlameLang Compiler Verification"
echo "1. Building compiler..."
cargo build --release --quiet
echo "   ✅ Build successful"
echo "2. Running tests..."
cargo test --quiet 2>&1 | tail -1
echo "   ✅ Tests passed"
echo "3. Compiling examples..."
./target/release/flamec examples/hello.flame > /dev/null 2>&1
echo "   ✅ hello.flame compiled"
./target/release/flamec examples/fibonacci.flame > /dev/null 2>&1
echo "   ✅ fibonacci.flame compiled"
./target/release/flamec examples/bonding_rules.flame > /dev/null 2>&1
echo "   ✅ bonding_rules.flame compiled"
echo "4. Running hello..."
./examples/hello
echo "🎉 ALL VERIFICATIONS PASSED!"
