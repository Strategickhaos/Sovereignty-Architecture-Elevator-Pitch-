# SAGCO OS — Sovereignty Architecture General Compiler OS

Pure Python stdlib. Zero external dependencies. No pip installs.

## What It Is

SAGCO OS is a complete Python package built around the Water Street Oyster Bar memory engine. It includes:

- **SAGCO Language** — a small but complete programming language with lexer, parser, evaluator, and fuzz tester
- **ERU Engine** — Expected/Actual/Variance analysis (PASS/PARTIAL/FAIL)
- **Solver Pipeline** — extract → classify → normalize → ERU → flashcards → quiz → summary
- **154 Flashcards** — extracted from the Oyster Drop Memory Engine XLSX
- **Physarum Simulation** — slime mold network flow simulation
- **Citizen Registry** — JSON-backed registry with ERU status tracking

## Quick Start

```bash
# Run the solver on Water Street menu
python3 sagco_cli.py solve --demo

# Execute a SAGCO program
python3 sagco_cli.py run examples/hello.sagco

# Run the fuzz tester
python3 sagco_cli.py fuzz --n 200

# ERU analysis
python3 sagco_cli.py eru data/oyster_flashcards.csv

# Interactive flashcard game
python3 sagco_cli.py flashgame
```

## The SAGCO Language

```sagco
# hello.sagco
CELL A1 = "Eggs Orleans"
CELL A2 = "$20"
CELL B1 = ERU("brunch item", A1)
CELL C1 = GUARD(A2)
CELL D1 = MORSE(A1)
ASSERT C1 == "OPEN_VARIANCE"
ASSERT D1 == "MOBIUS_READY"
PRINT D1
```

### Built-in Functions

| Function | Returns |
|---|---|
| `ERU(expected, actual)` | `VARIANCE_0` or `OPEN_VARIANCE` |
| `GUARD(text)` | `MOBIUS_READY` or `NOT_READY` |
| `MORSE(text)` | Morse code string |
| `SANITY(text)` | `SOVEREIGN` or `HALLUCINATION_RISK` |
| `SOLVE(expr)` | Algebraic solution or `UNSOLVABLE` |
| `LEN(s)`, `UPPER(s)`, `LOWER(s)` | String utilities |

## XLSX Data Source

The canonical data is the Oyster Drop Memory Engine XLSX (154 rows):

| Column | Description |
|---|---|
| ID | Unique item ID (1-154) |
| Category | Menu category (21 categories) |
| Item | Item name |
| Price | Price in dollars |
| Details | Full description |
| Question | Flashcard question |
| Answer | Flashcard answer |
| Mnemonic / Lyric Cue | Memory aid |
| Expected Price / Actual Price / Variance | ERU data |
| ERU | PASS/PARTIAL/FAIL |
| Rust Token | snake_case identifier |
| Compression Ratio | Compression metric |

## Running Tests

```bash
python3 -m pytest tests/ -v
```

42 tests, all passing. Zero external dependencies.

## Directory Structure

```
sagco-os/
├── sagco_cli.py          # main CLI
├── sagco/
│   ├── lang/             # SAGCO language: lexer, parser, evaluator, fuzz
│   ├── core/             # ERU engine, extractor, classifier, tokenizer
│   ├── solver/           # pipeline, flashcards, quiz, summary
│   ├── physarum/         # network simulation
│   ├── university/       # atoms, bonds, molecules
│   ├── citizens/         # citizen registry
│   └── io/               # XLSX/YAML/CSV/PDF readers (pure stdlib)
├── data/
│   ├── oyster_flashcards.csv
│   └── water_street_menu.yaml
└── tests/                # 42 unit tests
```
