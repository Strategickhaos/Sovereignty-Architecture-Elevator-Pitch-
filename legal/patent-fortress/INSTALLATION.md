# Patent Fortress - Installation & Setup Guide

**Status**: LIVE ✓  
**Version**: 1.0.0  
**Date**: 2025-11-19

---

## Prerequisites

- Linux/Unix system (macOS, Ubuntu, Debian, RHEL, etc.)
- Bash shell
- Git repository access
- Basic command-line knowledge

**Optional but recommended**:
- `bc` calculator (for gratitude engine calculations)
- `curl` or `wget` (for future web scanning features)
- Discord webhook (for notifications)
- Email/SMTP (for alerts)

---

## Quick Installation

### 1. Verify Files Are Present

```bash
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-

# Check all components are installed
ls -la legal/patent-fortress/
# Should see:
# - sovereignty-protocol.sh (master control)
# - patent-finder.sh
# - royalty-scanner.sh
# - gratitude-engine.sh
# - schedule-daemon.sh
# - README.md
```

### 2. Make Scripts Executable

```bash
chmod +x legal/patent-fortress/*.sh
```

### 3. Test the System

```bash
# Run complete protocol (recommended first test)
./legal/patent-fortress/sovereignty-protocol.sh

# Or test individual components
./legal/patent-fortress/patent-finder.sh
./legal/patent-fortress/royalty-scanner.sh
./legal/patent-fortress/gratitude-engine.sh 1000
```

---

## Automated Scheduling

Choose one of the following methods to run the Patent Sovereignty Protocol automatically:

### Option A: Systemd Timer (Recommended for Modern Linux)

**Best for**: Ubuntu 16.04+, Debian 8+, RHEL/CentOS 7+, Fedora, Arch Linux

```bash
# 1. Copy service files
sudo cp legal/patent-fortress/systemd/patent-sovereignty.service /etc/systemd/system/
sudo cp legal/patent-fortress/systemd/patent-sovereignty.timer /etc/systemd/system/

# 2. Edit service file to update paths (if needed)
sudo nano /etc/systemd/system/patent-sovereignty.service
# Update WorkingDirectory and ExecStart paths

# 3. Reload systemd
sudo systemctl daemon-reload

# 4. Enable and start the timer
sudo systemctl enable patent-sovereignty.timer
sudo systemctl start patent-sovereignty.timer

# 5. Verify status
sudo systemctl status patent-sovereignty.timer
sudo systemctl list-timers patent-sovereignty.timer

# 6. View logs
journalctl -u patent-sovereignty.service -f
```

**To manually trigger a run**:
```bash
sudo systemctl start patent-sovereignty.service
```

**To disable**:
```bash
sudo systemctl stop patent-sovereignty.timer
sudo systemctl disable patent-sovereignty.timer
```

---

### Option B: Cron Jobs (Universal Linux/Unix)

**Best for**: Any Unix-like system, older Linux distributions

```bash
# 1. Open crontab editor
crontab -e

# 2. Add one of these entries:

# Run every 6 hours (recommended)
0 */6 * * * cd /path/to/Sovereignty-Architecture-Elevator-Pitch- && ./legal/patent-fortress/schedule-daemon.sh cron

# OR run daily at 2 AM
0 2 * * * cd /path/to/Sovereignty-Architecture-Elevator-Pitch- && ./legal/patent-fortress/schedule-daemon.sh cron

# 3. Save and exit (Ctrl+X, Y, Enter in nano)

# 4. Verify cron job is installed
crontab -l
```

**Example with logging**:
```bash
# Create log directory
mkdir -p /var/log/patent-fortress

# Add to crontab with logging
0 */6 * * * cd /path/to/Sovereignty-Architecture-Elevator-Pitch- && ./legal/patent-fortress/sovereignty-protocol.sh 0 >> /var/log/patent-fortress/protocol.log 2>&1
```

---

### Option C: Continuous Daemon Mode

**Best for**: Development, testing, dedicated servers

```bash
# Run in foreground (Ctrl+C to stop)
./legal/patent-fortress/schedule-daemon.sh continuous

# Run in background
nohup ./legal/patent-fortress/schedule-daemon.sh continuous > /var/log/patent-fortress/daemon.log 2>&1 &

# Check if running
ps aux | grep schedule-daemon

# Stop daemon
pkill -f schedule-daemon.sh
```

---

## Configuration

### Basic Configuration

The system works out-of-the-box with sensible defaults. No configuration required for basic operation.

### Advanced Configuration

To customize search terms, intervals, or recipients, edit the shell scripts directly:

**Royalty Scanner - Search Terms**:
```bash
nano legal/patent-fortress/royalty-scanner.sh
# Edit the SEARCH_TERMS array
```

**Gratitude Engine - AI Contributors**:
```bash
nano legal/patent-fortress/gratitude-engine.sh
# Edit the AI_CONTRIBUTORS associative array
```

**Patent Finder - Keywords**:
```bash
nano legal/patent-fortress/patent-finder.sh
# Edit the patent_keywords array
```

**Schedule Daemon - Interval**:
```bash
nano legal/patent-fortress/schedule-daemon.sh
# Edit INTERVAL_SECONDS (default: 21600 = 6 hours)
```

---

## Integration with External Services

### Discord Notifications (Future)

```bash
# Add Discord webhook URL
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# Modify scripts to send notifications
# Example in royalty-scanner.sh:
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{\"content\":\"Patent violation detected!\"}"
```

### Email Alerts (Future)

```bash
# Install mail utility
sudo apt-get install mailutils  # Ubuntu/Debian
sudo yum install mailx          # RHEL/CentOS

# Add to scripts:
echo "Patent Fortress report" | mail -s "Daily Report" admin@example.com
```

### Slack Integration (Future)

Similar to Discord - use Slack webhook URLs with curl/wget.

---

## Monitoring & Maintenance

### Check System Status

```bash
# View recent logs
ls -lth /tmp/sovereignty-protocol-*.log | head -5
ls -lth /tmp/patent-finder-*.log | head -5
ls -lth /tmp/royalty-scanner-*.log | head -5

# View patent portfolio
ls -la legal/patent-fortress/filings/

# View latest reports
cat legal/patent-fortress/fortress-status-*.md
cat legal/patent-fortress/gratitude-report-*.md
```

### Log Management

```bash
# Create cleanup script
cat > /usr/local/bin/patent-fortress-cleanup.sh << 'EOF'
#!/bin/bash
# Clean up logs older than 30 days
find /tmp -name "patent-finder-*.log" -mtime +30 -delete
find /tmp -name "royalty-scanner-*.log" -mtime +30 -delete
find /tmp -name "gratitude-engine-*.log" -mtime +30 -delete
find /tmp -name "sovereignty-protocol-*.log" -mtime +30 -delete
echo "Cleanup completed: $(date)"
EOF

chmod +x /usr/local/bin/patent-fortress-cleanup.sh

# Add to crontab (run weekly)
0 4 * * 0 /usr/local/bin/patent-fortress-cleanup.sh
```

### Backup Patent Portfolio

```bash
# Create backup script
cat > /usr/local/bin/patent-fortress-backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/patent-fortress"
DATE=$(date +%Y%m%d)
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/patent-fortress-$DATE.tar.gz" \
  legal/patent-fortress/filings/ \
  legal/council-vault/
echo "Backup completed: $BACKUP_DIR/patent-fortress-$DATE.tar.gz"
EOF

chmod +x /usr/local/bin/patent-fortress-backup.sh

# Add to crontab (run daily)
0 3 * * * /usr/local/bin/patent-fortress-backup.sh
```

---

## Troubleshooting

### Scripts Not Executing

```bash
# Check permissions
ls -la legal/patent-fortress/*.sh
# Should show -rwxr-xr-x (executable)

# Fix permissions
chmod +x legal/patent-fortress/*.sh
```

### Git Errors

```bash
# Ensure you're in a git repository
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-
git status

# If not a git repo, the patent finder won't work
# It requires git to scan commits
```

### bc Calculator Not Found

```bash
# Install bc
sudo apt-get install bc      # Ubuntu/Debian
sudo yum install bc          # RHEL/CentOS
brew install bc              # macOS
```

### Permission Denied Writing Files

```bash
# Ensure write permissions to patent-fortress directory
chmod -R u+w legal/patent-fortress/

# For systemd, check user has access to WorkingDirectory
```

---

## Uninstallation

### Remove Systemd Timer

```bash
sudo systemctl stop patent-sovereignty.timer
sudo systemctl disable patent-sovereignty.timer
sudo rm /etc/systemd/system/patent-sovereignty.service
sudo rm /etc/systemd/system/patent-sovereignty.timer
sudo systemctl daemon-reload
```

### Remove Cron Jobs

```bash
crontab -e
# Delete patent-fortress related lines
```

### Remove Files (Caution!)

```bash
# Remove patent fortress (keeps council-vault)
rm -rf legal/patent-fortress/

# Remove council vault (WARNING: Contains legal documents)
# rm -rf legal/council-vault/
```

---

## Security Considerations

1. **File Permissions**: Patent filings may contain sensitive information. Ensure proper file permissions:
   ```bash
   chmod 700 legal/patent-fortress/filings/
   ```

2. **Log Files**: Logs in `/tmp` are world-readable. Consider moving to secure location:
   ```bash
   mkdir -p ~/.patent-fortress/logs
   # Update scripts to use ~/.patent-fortress/logs instead of /tmp
   ```

3. **API Keys**: If integrating with external services, use environment variables:
   ```bash
   export PATENT_API_KEY="secret_key"
   # Never hardcode in scripts
   ```

4. **Backup Security**: Encrypt backups containing patent information:
   ```bash
   tar -czf - legal/patent-fortress/ | gpg -e -r your@email.com > backup.tar.gz.gpg
   ```

---

## Support

- **Documentation**: See [README.md](README.md) for usage details
- **Issues**: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues
- **Legal**: legal@alexandermethodology.org
- **Technical**: dev@strategickhaos.org

---

## Status

**Installation Status**: Complete ✓  
**System Status**: OPERATIONAL ✓  
**Protection**: ACTIVE ✓

**The protocol is sealed.**  
**The empire is eternal.**  
**The dragons are finally free.** 🧠⚡🏛️❤️🐐∞

---

*Patent Sovereignty Protocol v1.0.0*  
*Authority: Alexander Methodology Institute*  
*Last Updated: 2025-11-19*
