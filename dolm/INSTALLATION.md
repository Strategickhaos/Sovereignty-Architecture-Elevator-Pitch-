# DoLM Installation Guide

## Quick Start

### Option 1: Automatic Installation (Recommended)

#### Linux/macOS
```bash
cd dolm
chmod +x activate-dolm.sh
./activate-dolm.sh
```

#### Windows (PowerShell as Administrator)
```powershell
cd dolm
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\activate-dolm.ps1
```

### Option 2: Docker Compose

```bash
cd dolm
docker-compose -f docker-compose.dolm.yml up -d
```

### Option 3: Manual Docker

```bash
cd dolm

# Build the image
docker build -t dolm-daemon:local .

# Run the daemon
docker run -d \
  --name dolm-daemon \
  --restart unless-stopped \
  -v $(pwd)/..:/swarm:ro \
  -v ~/strategic-khaos-private/dolm-vault:/vault \
  -e DOLM_WATCH_PATH=/swarm \
  -e DOLM_VAULT_PATH=/vault \
  dolm-daemon:local
```

### Option 4: Local Python (Development)

```bash
cd dolm

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DOLM_VAULT_PATH="$HOME/strategic-khaos-private/dolm-vault"
export DOLM_WATCH_PATH="$(pwd)/.."

# Run daemon
python dolm_daemon.py
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DOLM_VAULT_PATH` | `~/strategic-khaos-private/dolm-vault` | Location of Obsidian vault |
| `DOLM_WATCH_PATH` | `/swarm` (Docker) or `$(pwd)` (local) | Directory to watch for code files |

### Custom Configuration

Create a custom configuration by setting environment variables before running:

```bash
# Watch a specific project
export DOLM_WATCH_PATH="/path/to/my/project"

# Use a different vault location
export DOLM_VAULT_PATH="/path/to/my/vault"

# Run DoLM
./activate-dolm.sh
```

## Post-Installation

### 1. Install Obsidian

Download from: https://obsidian.md/download

### 2. Open the Vault

1. Launch Obsidian
2. Click "Open folder as vault"
3. Navigate to: `~/strategic-khaos-private/dolm-vault`
4. Click "Open"

### 3. Explore Your Notes

- Browse `todos/` folder for all TODO items
- Browse `errors/` folder for error patterns
- Check `daily/` for daily summaries
- Use Graph View to see connections

### 4. Verify DoLM is Running

```bash
# Check Docker container
docker ps | grep dolm-daemon

# View logs
docker logs -f dolm-daemon

# Check vault is being updated
ls -la ~/strategic-khaos-private/dolm-vault/todos/
```

## Monitoring

### View Logs

```bash
# Docker
docker logs -f dolm-daemon

# Docker Compose
docker-compose -f docker-compose.dolm.yml logs -f

# Check container status
docker ps -a | grep dolm
```

### Check Vault Statistics

```bash
# Count TODO notes
ls ~/strategic-khaos-private/dolm-vault/todos/ | wc -l

# Count error notes
ls ~/strategic-khaos-private/dolm-vault/errors/ | wc -l

# View latest daily summary
cat ~/strategic-khaos-private/dolm-vault/daily/$(date +%Y-%m-%d).md
```

## Updating

### Update Docker Image

```bash
cd dolm

# Rebuild image
docker build -t dolm-daemon:local .

# Restart container
docker stop dolm-daemon
docker rm dolm-daemon
./activate-dolm.sh
```

### Update Local Installation

```bash
cd dolm

# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart daemon (Ctrl+C and run again)
python dolm_daemon.py
```

## Troubleshooting

### Container Won't Start

```bash
# Check Docker is running
docker info

# Check logs for errors
docker logs dolm-daemon

# Verify paths exist
ls -la ~/strategic-khaos-private/dolm-vault
```

### No Notes Appearing

1. **Verify container is running:**
   ```bash
   docker ps | grep dolm-daemon
   ```

2. **Check watched directory has code files:**
   ```bash
   find /path/to/code -name "*.py" -o -name "*.js" | head
   ```

3. **Verify files contain TODOs:**
   ```bash
   grep -r "TODO\|FIXME\|HACK" /path/to/code
   ```

4. **Check container logs:**
   ```bash
   docker logs -f dolm-daemon
   ```

### Permission Issues

```bash
# Linux/macOS: Ensure vault directory is writable
chmod -R u+w ~/strategic-khaos-private/dolm-vault

# Docker: Run with user ID
docker run -d --user $(id -u):$(id -g) ...
```

### High CPU Usage

DoLM uses file watching which is efficient, but for very large codebases:

1. **Exclude directories:**
   ```bash
   # Add to .gitignore or modify watch paths
   # DoLM automatically skips: node_modules, __pycache__, venv, .git
   ```

2. **Increase processing delay:**
   Modify `dolm_daemon.py` line ~303:
   ```python
   time.sleep(0.5)  # Increase to 1.0 or 2.0
   ```

### Obsidian Can't Open Vault

1. **Check vault has .obsidian directory:**
   ```bash
   ls -la ~/strategic-khaos-private/dolm-vault/.obsidian
   ```

2. **Reinitialize vault:**
   ```bash
   rm -rf ~/strategic-khaos-private/dolm-vault/.obsidian
   # Restart DoLM to recreate
   ```

3. **Try creating vault in Obsidian first:**
   - File → Create new vault
   - Choose the dolm-vault directory

## Uninstallation

### Remove Docker Container

```bash
docker stop dolm-daemon
docker rm dolm-daemon
docker rmi dolm-daemon:local
```

### Remove Vault (Optional)

```bash
# CAUTION: This deletes all tracked TODOs and errors
rm -rf ~/strategic-khaos-private/dolm-vault
```

### Clean Up

```bash
# Remove only Docker artifacts
docker system prune -a

# Keep the vault but remove the daemon
docker stop dolm-daemon && docker rm dolm-daemon
```

## Security Considerations

1. **Read-Only Code Mount:** Code directory is mounted read-only (`:ro`)
2. **No Network Access:** Container runs without network access
3. **Local Only:** Vault stays on your machine
4. **No External Calls:** DoLM doesn't connect to external services
5. **Safe File Operations:** All file operations use context managers

## Performance

- **Memory:** ~50-100MB typical usage
- **CPU:** <5% during active scanning, <1% idle
- **Disk I/O:** Minimal, only writes when changes detected
- **Scaling:** Tested with codebases up to 10,000+ files

## Support

- **Documentation:** [README.md](README.md)
- **Issues:** Open an issue in the main repository
- **Examples:** See [example_usage.py](example_usage.py)
- **Main Docs:** [DOLM.md](../DOLM.md)

---

**Department of Living Memory**  
*"Nothing is ever lost. Every error is a lesson. Every TODO is a prophecy."*
