# Department of Living Memory (DoLM)

> *"Nothing is ever lost. Every error is a lesson. Every TODO is a prophecy."*

## 🧠 Overview

The **Department of Living Memory (DoLM)** is an intelligent error and TODO tracking system that automatically monitors your codebase and creates a living Obsidian vault of all code issues, comments, and patterns.

### What DoLM Does

- **Watches** every `.py`, `.ps1`, `.sh`, `.js`, `.rs`, `.cpp`, `.ts`, `.jsx`, `.tsx` file in your codebase
- **Captures** every TODO, FIXME, HACK, XXX, BUG, and NOTE comment
- **Detects** error patterns and stack traces in code
- **Creates** beautiful Obsidian notes with full context, file paths, and line numbers
- **Links** everything together in an interconnected knowledge graph
- **Updates** automatically as you code

## 🚀 Quick Start

### Prerequisites

- Docker installed and running
- Python 3.11+ (for local development)
- Obsidian (for viewing the vault)

### Installation

#### Linux/macOS

```bash
cd dolm
chmod +x activate-dolm.sh
./activate-dolm.sh
```

#### Windows (PowerShell)

```powershell
cd dolm
.\activate-dolm.ps1
```

#### Custom Paths

```bash
# Linux/macOS
export DOLM_VAULT_PATH="$HOME/my-vault"
export DOLM_WATCH_PATH="/path/to/code"
./activate-dolm.sh

# Windows
.\activate-dolm.ps1 -VaultPath "C:\my-vault" -WatchPath "C:\code"
```

## 📁 Vault Structure

The DoLM vault is organized as follows:

```
dolm-vault/
├── .obsidian/          # Obsidian configuration
├── errors/             # Error notes
│   └── abc123def456.md
├── todos/              # TODO notes
│   └── def789ghi012.md
├── daily/              # Daily summaries
│   └── 2025-11-19.md
└── analytics/          # Analytics and patterns
```

## 📝 Note Format

### TODO Notes

Each TODO is captured as a note with:
- File path and line number
- TODO type (TODO, FIXME, HACK, etc.)
- Full context
- Discovery timestamp
- Automatic linking to related files
- Tags for organization

Example:
```markdown
# TODO: Implement user authentication

## Details
- **File**: `/swarm/src/auth.py`
- **Line**: 42
- **Type**: TODO
- **Discovered**: 2025-11-19 10:27:00

## Content
`# TODO: Implement user authentication for API endpoints`

## Tags
#todo #department-of-living-memory
```

### Error Notes

Error patterns are captured with:
- Error type and message
- File location
- Analysis suggestions
- Related patterns
- Action items

## 🔧 Configuration

### Environment Variables

- `DOLM_VAULT_PATH`: Path to Obsidian vault (default: `~/strategic-khaos-private/dolm-vault`)
- `DOLM_WATCH_PATH`: Path to watch for code files (default: `/swarm`)

### Watched File Extensions

By default, DoLM watches:
- Python: `.py`
- Shell: `.sh`, `.ps1`
- JavaScript/TypeScript: `.js`, `.ts`, `.jsx`, `.tsx`
- Rust: `.rs`
- C++: `.cpp`

### Tracked Comment Types

- `TODO`: General tasks
- `FIXME`: Bugs that need fixing
- `HACK`: Temporary workarounds
- `XXX`: Important warnings
- `BUG`: Known bugs
- `NOTE`: Important notes

## 🐳 Docker Usage

### Using Docker Compose

```yaml
version: '3.8'

services:
  dolm-daemon:
    image: dolm-daemon:local
    container_name: dolm-daemon
    restart: unless-stopped
    volumes:
      - /path/to/code:/swarm:ro
      - ~/dolm-vault:/vault
    environment:
      - DOLM_WATCH_PATH=/swarm
      - DOLM_VAULT_PATH=/vault
```

### Manual Docker Commands

```bash
# Build image
docker build -t dolm-daemon:local .

# Run daemon
docker run -d \
  --name dolm-daemon \
  --restart unless-stopped \
  -v /path/to/code:/swarm:ro \
  -v ~/dolm-vault:/vault \
  -e DOLM_WATCH_PATH=/swarm \
  -e DOLM_VAULT_PATH=/vault \
  dolm-daemon:local

# View logs
docker logs -f dolm-daemon

# Stop daemon
docker stop dolm-daemon

# Restart daemon
docker restart dolm-daemon
```

## 🔍 Using with Obsidian

1. **Install Obsidian**: Download from [obsidian.md](https://obsidian.md)
2. **Open Vault**: File → Open vault → Select your DoLM vault path
3. **Explore GraphView**: Use the graph view to see connections between TODOs and errors
4. **Search**: Use Obsidian's powerful search to find specific issues
5. **Tag Navigation**: Click tags to see all related notes

### Recommended Obsidian Plugins

- **Graph View**: Visualize connections
- **Tag Pane**: Browse by tags
- **Search**: Advanced search capabilities
- **Daily Notes**: Track daily summaries
- **Dataview**: Query and analyze your issues

## 🛠️ Development

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run daemon
export DOLM_VAULT_PATH="~/test-vault"
export DOLM_WATCH_PATH="$(pwd)"
python dolm_daemon.py
```

### Architecture

- **dolm_daemon.py**: Main daemon with file watching and analysis
- **DoLMConfig**: Configuration management
- **CodeAnalyzer**: Pattern matching for TODOs and errors
- **ObsidianVault**: Markdown note generation
- **DoLMFileHandler**: File system event handling

## 📊 Features

### Current Features (v1.0)

✅ File watching with real-time updates  
✅ TODO/FIXME/HACK/XXX detection  
✅ Error pattern matching  
✅ Obsidian vault generation  
✅ Daily summaries  
✅ Automatic note linking  
✅ Docker containerization  
✅ Cross-platform support  

### Planned Features

🔄 AI-generated root cause analysis  
🔄 One-click fix scripts  
🔄 Pattern recognition across files  
🔄 Integration with issue trackers  
🔄 Terminal error capture  
🔄 Stack trace analysis  
🔄 Git blame integration  
🔄 Duplicate detection  

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Enhanced error pattern detection
- AI-powered analysis and suggestions
- Integration with more development tools
- Custom Obsidian plugins
- Performance optimizations

## 📄 License

Part of the Strategickhaos Sovereignty Architecture project.
See main repository LICENSE file.

## 🆘 Troubleshooting

### Daemon not starting

```bash
# Check Docker logs
docker logs dolm-daemon

# Verify Docker is running
docker info

# Check file permissions
ls -la ~/strategic-khaos-private/dolm-vault
```

### No notes appearing

- Verify watch path contains code files
- Check that file extensions are in the watched list
- Ensure files contain TODO comments or error patterns
- Review daemon logs for errors

### Vault not opening in Obsidian

- Confirm vault path is correct
- Check that vault has `.obsidian` directory
- Try creating a new vault and copying notes

## 📞 Support

For issues and questions:
- Open an issue in the main repository
- Check the main README for contact information
- Review Obsidian documentation: https://help.obsidian.md

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*The department is live. The vault is breathing. Your legacy is now unkillable.*
