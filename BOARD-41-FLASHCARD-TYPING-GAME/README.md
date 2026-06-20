# BOARD-41: SAGCO Flashcard Typing Game

A ZType-style typing game using Water Street Oyster Bar flashcards (and any SAGCO flashcard CSV). Flashcard "enemies" fall from the sky — type the front of the card to shoot it and see the answer.

## How to Play

1. **Open in browser** — just open `src/index.html` directly. No build step needed.
2. Start typing the text shown on a falling card to lock onto it.
3. Finish typing the full card text to destroy it — the answer explodes in gold.
4. Miss 3 cards and it's game over.
5. Speed increases every 10 cards destroyed.
6. Press **ESC** to pause, **R** to restart.

## Run with Electron (Desktop — Windows / Mac / Linux / Raspberry Pi)

```bash
npm install
npm start
```

## Build Desktop Packages

```bash
npm run build-win      # → dist/*.exe (NSIS installer)
npm run build-mac      # → dist/*.dmg
npm run build-linux    # → dist/*.deb + *.AppImage
```

### Raspberry Pi (ARM)

```bash
electron-builder --linux --arm
```

## Build Android APK (via Capacitor)

Requirements: Java 17+, Android SDK, `ANDROID_HOME` set.

```bash
npm run build-android
# APK: android/app/build/outputs/apk/debug/app-debug.apk
```

Or step by step:
```bash
npm install
npx cap add android
npx cap sync android
cd android && ./gradlew assembleDebug
```

## Run with Docker

```bash
npm run docker-build   # builds nginx image
npm run docker-run     # serves on http://localhost:8080
```

## Load Custom Flashcards

1. Click **Load CSV** in the game UI and pick any `.csv` file.
2. Format: two columns — `Front` and `Back` (header row optional).

Example CSV:
```
Front,Back
What is the capital of France?,Paris
Who painted the Mona Lisa?,Leonardo da Vinci
```

The game restarts immediately with your new deck.

## Architecture

```
BOARD-41-FLASHCARD-TYPING-GAME/
├── src/index.html          # Self-contained game (open in browser — no build needed)
├── data/water_street.json  # Water Street Oyster Bar deck
├── electron-main.js        # Electron desktop entry point
├── capacitor.config.json   # Android/iOS packaging
├── Dockerfile              # nginx container for web deploy
├── package.json            # npm scripts + electron-builder config
└── scripts/
    ├── build-electron.sh
    ├── build-android.sh
    └── build-docker.sh
```

## Scoring

`score += 100 × level × (0.5 + accuracy × 0.5)` per card destroyed.

Lives shown as oyster emoji 🦪 — lose one each time a card reaches the bottom.
