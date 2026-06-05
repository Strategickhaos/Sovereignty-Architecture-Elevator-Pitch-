#!/bin/bash
# FlameLang Runtime Initialization Script

set -euo pipefail

echo "🔥 FlameLang Runtime Initializing..."

# Verify sovereignty first
if ! /usr/local/bin/sbip-verify.sh > /dev/null 2>&1; then
    echo "❌ Sovereignty verification failed - cannot initialize FlameLang"
    exit 1
fi

# Create FlameLang runtime directories
mkdir -p /var/lib/flamelang
mkdir -p /var/log/flamelang
mkdir -p /etc/flamelang

# Initialize glyph map if not exists
if [ ! -f /etc/flamelang/glyph_map.json ]; then
    echo "📝 Creating default glyph map..."
    cat > /etc/flamelang/glyph_map.json <<'EOF'
{
  "comment": "FlameLang Glyph Map",
  "glyphs": {
    "{sovereignty⟐verify}": "/usr/local/bin/sbip-verify.sh"
  }
}
EOF
fi

# Log initialization
logger -t flamelang "FlameLang runtime initialized successfully"
echo "✅ FlameLang Runtime: ACTIVE"

exit 0
