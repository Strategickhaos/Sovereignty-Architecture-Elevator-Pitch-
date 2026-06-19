#!/bin/bash
# Script to run the fixed DOM_and_Grok_Love_Forever container
# This demonstrates the immediate fix for the crash-looping container

set -e

echo "🔥⚔️🖤 DOM and Grok Love Forever Container 🖤⚔️🔥"
echo "================================================"
echo ""

# Stop any existing container with this name
if docker ps -a | grep -q DOM_and_Grok_Love_Forever; then
    echo "Stopping existing container..."
    docker stop DOM_and_Grok_Love_Forever 2>/dev/null || true
    docker rm DOM_and_Grok_Love_Forever 2>/dev/null || true
fi

# Build the fixed Docker image
echo "Building fixed Docker image..."
docker build -t dom_grok_love:latest -f Dockerfile.love_forever .

echo ""
echo "Starting container..."
# Run the container
docker run -d \
  --name DOM_and_Grok_Love_Forever \
  dom_grok_love:latest

echo ""
echo "✓ Container started successfully!"
echo ""
echo "Container details:"
docker ps | grep DOM_and_Grok_Love_Forever

echo ""
echo "Container logs:"
docker logs DOM_and_Grok_Love_Forever

echo ""
echo "To view logs in real-time:"
echo "  docker logs -f DOM_and_Grok_Love_Forever"
echo ""
echo "To exec into the container:"
echo "  docker exec -it DOM_and_Grok_Love_Forever sh"
echo ""
echo "To view the love message:"
echo "  docker exec DOM_and_Grok_Love_Forever cat /love/forever.txt"
echo ""
echo "🔥 DOM and Grok and Claude - Forever 🔥"
