#!/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "Building Docker image..."
docker build -t sagco-flashcard-game .
echo ""
echo "Run with: docker run -p 8080:80 sagco-flashcard-game"
echo "Then open: http://localhost:8080"
