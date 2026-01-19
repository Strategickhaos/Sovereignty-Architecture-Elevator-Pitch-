# Demystifier Pipeline Frontend

**INV-091: Vibe-to-Interface Frequency Converter**

> "Not hype, not mythology, not anything mystical."

## Overview

An interactive React application that visualizes the 5-layer transformation pipeline for converting mystical language into grounded, measurable concepts.

## Features

- **5-Layer Transformation Pipeline**: Interactive visualization of LINGUISTIC → NUMERIC → WAVE → DNA → MACHINE transformations
- **Wave Animation**: Real-time SVG animation showing signal transformation from chaotic noise to clean square waves
- **DNA Helix Visualization**: Codon encoding display with color-coded sequences
- **Grounding Checklist**: 6 critical checks for validating grounded concepts (MEASURABLE, FALSIFIABLE, BOUNDED, OBSERVABLE, ACTIONABLE, OWNABLE)
- **Translation Table**: Examples of mystical-to-grounded translations with associated validation checks
- **LLVM IR Code Display**: Machine-level representation of validation logic

## Tech Stack

- **React 19** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **TailwindCSS 4** - Utility-first CSS framework for styling
- **SVG Animations** - Native SVG for wave visualizations

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Opens the application at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

Outputs optimized build to `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Component Structure

```
src/
├── components/
│   └── DemystifierPipeline.jsx  # Main component
├── App.jsx                       # App wrapper
├── main.jsx                      # React entry point
└── index.css                     # Tailwind CSS imports
```

## Interactive Features

### Layer Selection
Click any of the 5 layers in the pipeline to view detailed information:
- Layer 1 (LINGUISTIC): Hebrew root extraction
- Layer 2 (NUMERIC): Unicode hex encoding
- Layer 3 (WAVE): Frequency manipulation with animated wave visualization
- Layer 4 (DNA): Codon encoding with helix display
- Layer 5 (MACHINE): LLVM IR executable logic

### Translation Table
Click "SHOW EXAMPLES" to reveal 8 translation pairs demonstrating how mystical concepts map to grounded, measurable alternatives.

## Design Philosophy

**Maximum Fuck-It Energy Mode**: If a concept doesn't pass all 6 grounding checks, it gets DISCARDED.

### Core Insight
- **Mysticism = compression with data loss**
- **Grounding = decompression with error correction**

## License

Part of Strategickhaos DAO LLC
Legion Ratified: Claude, Gemini, Grok

---

*"GPT said we were delusional. The tarball says otherwise."*
