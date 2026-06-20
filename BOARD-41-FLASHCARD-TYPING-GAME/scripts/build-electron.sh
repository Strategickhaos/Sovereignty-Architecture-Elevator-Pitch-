#!/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "Installing dependencies..."
npm install
echo "Building Electron packages..."
npm run build-win
npm run build-mac
npm run build-linux
echo "Build complete. Packages are in the dist/ directory."
