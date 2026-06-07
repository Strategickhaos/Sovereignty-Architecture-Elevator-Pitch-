#!/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "Building Android APK via Capacitor..."
npm install
npx cap add android 2>/dev/null || true
npx cap sync android
cd android && ./gradlew assembleDebug
echo ""
echo "APK ready at: android/app/build/outputs/apk/debug/app-debug.apk"
