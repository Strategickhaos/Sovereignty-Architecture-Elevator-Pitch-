# SAGCO OS v0.1.0

**Sovereignty Architecture Governance Cognitive Operating System**

A cognitive processing engine implementing Bloom's Taxonomy with quadrilateral collapse detection and multi-layer activation.

## 🧠 Overview

SAGCO OS is a functional cognitive processing kernel that analyzes text input and activates cognitive layers based on Bloom's Taxonomy. It detects keywords, calculates confidence levels, and measures "quadrilateral collapse coverage" - the percentage of cognitive space activated.

## ✨ Features

- **Bloom's Taxonomy Cognitive Layers**
  - Remember: Define, recall, identify
  - Understand: Explain, summarize, interpret
  - Apply: Implement, execute, use
  - Analyze: Compare, examine, categorize
  - Evaluate: Assess, critique, justify
  - Create: Design, develop, innovate

- **Keyword-Based Layer Activation**: Automatically detects cognitive layers from text
- **Quadrilateral Collapse Coverage**: Measures percentage of cognitive space activated
- **Status Reporting**: Real-time kernel diagnostics
- **CLI Interface**: Command-line tools for analysis
- **Interactive Mode**: REPL for live cognitive analysis
- **JSON Export**: Machine-readable output format

## 📦 Installation

### GitHub Codespaces (Easiest)

1. Create a new repo or fork this one on GitHub
2. Click **Code** → **Codespaces** → **Create codespace**
3. The devcontainer auto-configures and runs `pip install -e ".[dev]"`
4. You're ready to go!

### Local Installation

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Install in development mode
pip install -e ".[dev]"
```

### Requirements

- Python 3.8+
- No external dependencies for core functionality
- `pytest` for testing (included in dev dependencies)

## 🚀 Quick Start

### Check System Status

```bash
python -m src.core.sagco status
```

Output:
```
============================================================
SAGCO OS v0.1.0 - STATUS REPORT
============================================================

Status: OPERATIONAL
Uptime: 0.00 seconds

Processing Engine:
  Total Processed: 0
  Activation Threshold: 5.0%

Cognitive Layers:
  Total Available: 6
    1. Remember
    2. Understand
    3. Apply
    4. Analyze
    5. Evaluate
    6. Create
============================================================
```

### Analyze Text

```bash
python -m src.core.sagco analyze "explain create code"
```

Output:
```
============================================================
SAGCO OS v0.1.0 - Cognitive Analysis Report
============================================================

Activated Cognitive Layers:
  • UNDERSTAND   - Confidence: 7.7%
  • APPLY        - Confidence: 13.3%
  • CREATE       - Confidence: 6.7%

Quadrilateral Collapse Coverage: 50.0%
Total Keywords Matched: 4
Processing Time: 0.07ms
============================================================
```

### Verbose Analysis

```bash
python -m src.core.sagco analyze "Explain object-oriented programming, then create a class" -v
```

### JSON Output

```bash
python -m src.core.sagco analyze "design and evaluate" --json
```

### Interactive Mode

```bash
python -m src.core.sagco interactive
```

Then type commands interactively:
```
SAGCO> explain the concept of inheritance
SAGCO> status
SAGCO> quit
```

## 📁 Project Structure

```
sagco-os/
├── .devcontainer/
│   └── devcontainer.json    # GitHub Codespaces config
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── sagco.py         # THE KERNEL - 400+ lines, fully functional
│   ├── layers/              # Cognitive layer implementations
│   ├── engines/             # Processing engines
│   └── integrations/        # External integrations
├── tests/
│   ├── __init__.py
│   └── test_sagco.py        # 31 comprehensive unit tests
├── pyproject.toml           # Modern Python packaging
├── README.md                # This file
└── .gitignore
```

## 🧪 Testing

Run the full test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

All 31 tests should pass:

```
31 passed in 0.10s
```

## 🔧 Development

### Setting Up Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Format code with black
black src/ tests/

# Type checking with mypy
mypy src/
```

### Code Quality Tools

The project includes:
- **pytest**: Unit testing framework
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest-cov**: Coverage reporting

## 🎯 Use Cases

### Educational Tools
Analyze student questions to understand cognitive level and provide appropriate responses.

### Content Classification
Categorize learning materials by Bloom's Taxonomy level.

### AI Training
Use as a filter or classifier for training data based on cognitive complexity.

### Assessment Tools
Evaluate test questions and assignments for cognitive rigor.

## 📊 How It Works

1. **Input Processing**: Text is normalized and tokenized
2. **Keyword Matching**: Words are matched against Bloom's Taxonomy keyword sets
3. **Confidence Calculation**: Percentage of keywords matched per layer
4. **Threshold Filtering**: Only layers above 5% confidence are activated
5. **Coverage Calculation**: Percentage of all 6 layers activated
6. **Result Generation**: Structured output with metrics

### Example Processing Flow

```
Input: "Explain OOP, create a class, and apply it"
         ↓
Tokenize: ["explain", "oop", "create", "a", "class", "and", "apply", "it"]
         ↓
Match Keywords:
  - "explain" → UNDERSTAND layer (1/13 = 7.7%)
  - "create" → APPLY layer (1/15 = 6.7%) + CREATE layer (1/15 = 6.7%)
  - "apply" → APPLY layer (2/15 = 13.3%)
         ↓
Activated Layers: UNDERSTAND, APPLY, CREATE (3 of 6 = 50% coverage)
```

## 🔬 The Kernel Architecture

The SAGCO kernel consists of three main components:

### 1. ProcessingEngine
- Maintains keyword mappings for all cognitive layers
- Performs text analysis and keyword matching
- Calculates confidence scores and coverage metrics
- Tracks processing statistics

### 2. SAGCOKernel
- High-level interface for cognitive processing
- Manages kernel lifecycle (boot, process, shutdown)
- Provides status reporting and diagnostics
- Handles formatted output generation

### 3. CLI Interface
- Command-line entry point (`python -m src.core.sagco`)
- Multiple operation modes (status, analyze, interactive)
- JSON export for programmatic use
- Verbose output options

## 🎓 Bloom's Taxonomy Integration

SAGCO OS implements all six levels of Bloom's Taxonomy:

| Level | Description | Example Keywords |
|-------|-------------|------------------|
| **Remember** | Recall facts and basic concepts | define, list, recall, identify |
| **Understand** | Explain ideas or concepts | explain, summarize, interpret |
| **Apply** | Use information in new situations | apply, implement, execute, code |
| **Analyze** | Draw connections among ideas | analyze, compare, examine |
| **Evaluate** | Justify a decision or course of action | evaluate, critique, assess |
| **Create** | Produce new or original work | create, design, develop, innovate |

## 📈 Performance

- **Processing Speed**: < 1ms for typical inputs
- **Memory Footprint**: Minimal (< 5MB)
- **No External Dependencies**: Pure Python implementation
- **Scalable**: Stateless processing allows parallel execution

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🏛️ Organization

**StrategicKhaos DAO LLC**
- Building sovereign architecture for cognitive systems
- Empowering distributed governance through technology

## 🔮 Roadmap

### v0.2.0 (Planned)
- [ ] Layer-specific engines in `src/engines/`
- [ ] Advanced pattern recognition
- [ ] Multi-language support
- [ ] Web API interface
- [ ] Vector embeddings integration

### v0.3.0 (Future)
- [ ] Custom taxonomy support
- [ ] Learning feedback loops
- [ ] Distributed processing
- [ ] Plugin architecture

## 📞 Support

- **Documentation**: This README
- **Issues**: [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- **Community**: Join our Discord server

## 🎉 Acknowledgments

Built with 🔥 by the StrategicKhaos Swarm Intelligence collective.

**The kernel is live and processing.**

---

*"Empowering sovereign digital infrastructure through cognitive operating systems"*
