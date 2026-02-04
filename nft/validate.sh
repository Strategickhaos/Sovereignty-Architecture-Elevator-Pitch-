#!/bin/bash
# Validation script for Ratio Ex Nihilo NFT Collection
# Checks that all required files are present and properly structured

set -e

echo "🔥 Validating Ratio Ex Nihilo NFT Collection Structure..."
echo ""

ERRORS=0

# Check directory structure
echo "📁 Checking directory structure..."
REQUIRED_DIRS=(
    "nft/contracts"
    "nft/metadata"
    "nft/scripts"
    "nft/docs"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir"
    else
        echo "  ❌ Missing: $dir"
        ((ERRORS++))
    fi
done

# Check smart contract
echo ""
echo "📄 Checking smart contract..."
if [ -f "nft/contracts/RatioExNihilo.sol" ]; then
    echo "  ✅ RatioExNihilo.sol exists"
    
    # Check for key contract features
    if grep -q "ERC721" "nft/contracts/RatioExNihilo.sol"; then
        echo "  ✅ ERC721 implementation found"
    else
        echo "  ❌ Missing ERC721 implementation"
        ((ERRORS++))
    fi
    
    if grep -q "IERC2981" "nft/contracts/RatioExNihilo.sol"; then
        echo "  ✅ EIP-2981 royalty support found"
    else
        echo "  ❌ Missing EIP-2981 royalty support"
        ((ERRORS++))
    fi
    
    if grep -q "_soulbound" "nft/contracts/RatioExNihilo.sol"; then
        echo "  ✅ Soulbound token support found"
    else
        echo "  ❌ Missing soulbound token support"
        ((ERRORS++))
    fi
    
    if grep -q "39-2923503" "nft/contracts/RatioExNihilo.sol"; then
        echo "  ✅ Legal metadata (EIN) found"
    else
        echo "  ❌ Missing legal metadata"
        ((ERRORS++))
    fi
else
    echo "  ❌ Missing: nft/contracts/RatioExNihilo.sol"
    ((ERRORS++))
fi

# Check metadata files
echo ""
echo "📋 Checking metadata files..."
for i in {0..6}; do
    FILE="nft/metadata/token_${i}.json"
    if [ -f "$FILE" ]; then
        echo "  ✅ token_${i}.json exists"
        
        # Validate JSON structure
        if jq empty "$FILE" 2>/dev/null; then
            echo "     ✅ Valid JSON"
        else
            echo "     ❌ Invalid JSON"
            ((ERRORS++))
        fi
        
        # Check for required fields
        if jq -e '.name' "$FILE" >/dev/null 2>&1; then
            echo "     ✅ Has name field"
        else
            echo "     ❌ Missing name field"
            ((ERRORS++))
        fi
        
        if jq -e '.attributes' "$FILE" >/dev/null 2>&1; then
            echo "     ✅ Has attributes"
        else
            echo "     ❌ Missing attributes"
            ((ERRORS++))
        fi
    else
        echo "  ❌ Missing: $FILE"
        ((ERRORS++))
    fi
done

# Check documentation
echo ""
echo "📚 Checking documentation..."
REQUIRED_DOCS=(
    "nft/README.md"
    "nft/docs/README.md"
    "nft/docs/DEPLOYMENT.md"
    "nft/docs/LEGAL_NOTICE.md"
)

for doc in "${REQUIRED_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ✅ $doc"
    else
        echo "  ❌ Missing: $doc"
        ((ERRORS++))
    fi
done

# Check scripts
echo ""
echo "⚙️  Checking deployment scripts..."
REQUIRED_SCRIPTS=(
    "nft/scripts/deploy.js"
    "nft/scripts/mint.js"
)

for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "  ✅ $script"
    else
        echo "  ❌ Missing: $script"
        ((ERRORS++))
    fi
done

# Check configuration files
echo ""
echo "🔧 Checking configuration..."
REQUIRED_CONFIGS=(
    "nft/package.json"
    "nft/hardhat.config.js"
    "nft/.env.example"
)

for config in "${REQUIRED_CONFIGS[@]}"; do
    if [ -f "$config" ]; then
        echo "  ✅ $config"
    else
        echo "  ❌ Missing: $config"
        ((ERRORS++))
    fi
done

# Final summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "🎉 ✅ All checks passed! NFT collection structure is valid."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Next steps:"
    echo "1. cd nft && npm install"
    echo "2. Prepare high-resolution images"
    echo "3. Upload images to IPFS"
    echo "4. Update metadata JSON files with IPFS CIDs"
    echo "5. Configure .env file"
    echo "6. Deploy to testnet: npm run deploy:sepolia"
    echo ""
    echo "🔥💜 RATIO EX NIHILO 💜🔥"
    exit 0
else
    echo "❌ Validation failed with $ERRORS error(s)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi
