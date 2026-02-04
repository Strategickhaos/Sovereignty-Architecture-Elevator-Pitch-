# SAGCO Menu - Tool Discovery & Navigation System

**Version:** 1.3 (TRIG6-verified)  
**Status:** ✅ Production Ready

## Overview

SAGCO Menu is a YAML-driven tool discovery and navigation system for the Sovereignty Architecture ecosystem. It provides an intuitive interface to browse, search, and manage access to the tool suite.

## Features

### Core Functionality
- 📋 **List Mode** - Browse all tools organized by category
- 🔍 **Fuzzy Search** - Find tools with typo-tolerant matching
- ⏱️ **Recent Items** - Quick access to recently used tools
- 💾 **Per-User State** - Personal preferences persisted across sessions
- 🛡️ **Safe Parsing** - Comprehensive error handling for malformed configs

### Technical Highlights
- **Zero External Dependencies** (except PyYAML)
- **O(n) Performance** - Linear operations, fast even with 100+ tools
- **Modular Architecture** - Clean separation of loaders, extractors, handlers
- **Portable** - Works on Linux, macOS, Windows
- **Pedagogical** - Clear code patterns for learning

## Installation

### Prerequisites
- Python 3.7 or higher
- PyYAML library

```bash
# Install PyYAML
pip install pyyaml

# Make script executable
chmod +x sagco-menu.py
```

### Quick Start

```bash
# List all available tools
./sagco-menu.py --list

# Search for deployment tools
./sagco-menu.py --search deploy

# Show recently used tools
./sagco-menu.py --recent

# Get help
./sagco-menu.py --help
```

## Usage

### Command-Line Interface

```
Usage: sagco-menu.py [OPTIONS] [CONFIG_PATH]

Options:
  --list, -l              List all categories and items
  --search QUERY, -s      Search for tools matching QUERY
  --recent, -r            Show recent selections
  --help, -h              Show this help message

Config Path:
  Path to SPM configuration file (YAML/JSON)
  Default: ./spm_tools.yaml
```

### Examples

**Browse Tool Catalog:**
```bash
./sagco-menu.py --list
```
Output:
```
======================================================================
SAGCO Tools & Systems (v1.2)
Sovereignty Architecture Tool Ecosystem
======================================================================

🔍  1. Recon & Intelligence
----------------------------------------------------------------------
  1.1 jetbrains_deep_recon
      → Deep reconnaissance of JetBrains ecosystem
  1.2 launch_recon
      → Launch comprehensive recon suite
  ...
```

**Search for Tools:**
```bash
# Find deployment tools
./sagco-menu.py --search deploy

# Find monitoring tools
./sagco-menu.py --search monitor

# Fuzzy search handles typos
./sagco-menu.py --search deploi  # Still finds "deploy_*"
```

**Access Recent Tools:**
```bash
./sagco-menu.py --recent
```
Output:
```
⏱️  Recent Selections
----------------------------------------------------------------------
  R1. network_monitor (Security & Defense)
      → Monitor network sovereignty
  R2. deploy_empire (Deployment & Orchestration)
      → Deploy full empire infrastructure
  ...
```

**Use Custom Config:**
```bash
./sagco-menu.py custom_tools.yaml --list
```

## Configuration

### SPM Configuration Format

The tool uses SPM (System/Tools Package Manager) YAML format:

```yaml
version: "1.2"
name: "SAGCO Tools & Systems"
description: "Sovereignty Architecture Tool Ecosystem"

categories:
  - name: "Deployment & Orchestration"
    icon: "🚀"
    items:
      - name: "deploy_empire"
        command: "./deploy-empire.sh"
        description: "Deploy full empire infrastructure"
      
      - name: "quick_deploy"
        command: "./quick-deploy.sh"
        description: "Quick deployment for testing"
```

### Configuration Schema

- `version` (string) - Config format version
- `name` (string) - System/tool suite name
- `description` (string, optional) - Brief description
- `categories` (array) - List of tool categories
  - `name` (string) - Category name
  - `icon` (string, optional) - Emoji icon for display
  - `items` (array) - Tools in this category
    - `name` (string) - Unique tool identifier
    - `command` (string) - Shell command to run
    - `description` (string, optional) - Tool description

### State Management

Recent selections are stored in `~/.sagco_recent.json`:

```json
{
  "recent": [
    "network_monitor",
    "deploy_empire",
    "status_check"
  ]
}
```

- Automatically managed by the tool
- Capped at 5 most recent items
- Deduplicated on each addition
- Per-user (stored in home directory)

## Integration

### Shell Alias

```bash
# Add to ~/.bashrc or ~/.zshrc
alias sm='./sagco-menu.py'
alias sml='./sagco-menu.py --list'
alias sms='./sagco-menu.py --search'
alias smr='./sagco-menu.py --recent'

# Usage
sm --search deploy
sml
```

### System-Wide Installation

```bash
# Link to system bin
sudo ln -s $(pwd)/sagco-menu.py /usr/local/bin/sagco

# Use anywhere
sagco --search monitor
```

### Script Integration

```bash
# Extract command from search result
COMMAND=$(./sagco-menu.py --search "deploy_empire" | \
          grep '^\s*\$' | \
          sed 's/^\s*\$\s*//')

# Execute the command
if [ -n "$COMMAND" ]; then
  echo "Executing: $COMMAND"
  eval "$COMMAND"
fi
```

## Error Handling

The tool provides clear error messages for common issues:

### File Not Found
```bash
$ ./sagco-menu.py /nonexistent/file.yaml --list
Error: Configuration file not found: /nonexistent/file.yaml
```

### Malformed YAML
```bash
$ ./sagco-menu.py bad_config.yaml --list
Error: Malformed YAML in bad_config.yaml:
  while scanning a quoted scalar
  in "bad_config.yaml", line 10, column 22
found unexpected end of stream
  in "bad_config.yaml", line 11, column 1
```

### Missing Search Query
```bash
$ ./sagco-menu.py --search
Error: --search requires a query argument
```

## Performance

Benchmarked with 32 items across 8 categories:

- **List mode:** ~150ms
- **Search mode:** ~150ms
- **Recent mode:** ~150ms

Performance is O(n) where n is the number of tools. Efficient even with 100+ tools.

## TRIG6 Verification

This tool has been formally verified against the TRIG6 framework:

- ✅ **ANGLE 1** - Structural Architecture: Modular design
- ✅ **ANGLE 2** - Narrative Physics: O(n) performance
- ✅ **ANGLE 3** - Emotional Resonance: User-friendly UX
- ✅ **ANGLE 4** - Technical Accuracy: Safe implementation
- ✅ **ANGLE 5** - Pedagogical Effectiveness: Clear code
- ✅ **ANGLE 6** - Meta-Narrative Function: YAML-to-UI bridge

See [TRIG6_VERIFICATION_sagco-menu.md](TRIG6_VERIFICATION_sagco-menu.md) for detailed analysis.

## Architecture

### Module Structure

```
sagco-menu.py
├── LOADERS: SPM + State (YAML/JSON)
│   ├── load_spm_config()    - Safe YAML/JSON loading
│   ├── load_recent_state()  - Load recent items
│   └── save_recent_state()  - Persist recent items
├── EXTRACTORS: Categories + Items
│   ├── extract_categories() - Parse category structure
│   └── extract_all_items()  - Flatten for search
├── HANDLERS: Recent Management
│   └── add_recent()         - Capped, deduped updates
├── SEARCH: Fuzzy Matching
│   └── fuzzy_search()       - difflib-based search
└── OUTPUT: Display Functions
    ├── print_header()
    ├── print_categories()
    ├── print_recent()
    └── print_search_results()
```

### Design Principles

1. **Modularity** - Each function has a single responsibility
2. **Safety** - Comprehensive error handling, no crashes
3. **Simplicity** - Clear code patterns, minimal complexity
4. **Performance** - O(n) operations, no recursion
5. **Portability** - Cross-platform, minimal dependencies

## Extending

### Adding New Modes

```python
# Add new mode in main()
elif mode == 'favorite':
    print_favorites(favorites, all_items)
```

### Adding New Features

Common extensions:
- **Tags** - Add tag-based filtering
- **Colors** - Use colorama for colored output
- **Interactive** - Add curses-based TUI
- **Execution** - Add mode to run commands directly
- **Favorites** - Separate from recent items
- **History** - Full usage history with timestamps

### Custom Output Formats

```python
# Add JSON output
def print_json(data):
    print(json.dumps(data, indent=2))
```

## Troubleshooting

### Import Error: No module named 'yaml'
```bash
pip install pyyaml
```

### Permission Denied
```bash
chmod +x sagco-menu.py
```

### Config Not Found
```bash
# Specify full path
./sagco-menu.py /full/path/to/spm_tools.yaml --list
```

### Recent State Not Saving
Check write permissions:
```bash
ls -la ~/.sagco_recent.json
```

## Contributing

Contributions welcome! Key areas:
- Additional output formats (JSON, CSV)
- Interactive mode (curses/prompt_toolkit)
- Command execution integration
- Tag-based filtering
- Color themes

## License

See repository [LICENSE](LICENSE) file.

## Support

- **Documentation:** This README + [TRIG6_VERIFICATION_sagco-menu.md](TRIG6_VERIFICATION_sagco-menu.md)
- **Configuration:** [spm_tools.yaml](spm_tools.yaml) example
- **Issues:** GitHub Issues

---

**Built with 🔥 for the Strategickhaos Sovereignty Architecture**

*"Search turns config into conversation."*
