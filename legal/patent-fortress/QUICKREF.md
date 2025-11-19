# Patent Fortress - Quick Reference Card

## Essential Commands

### Run Complete System
```bash
./legal/patent-fortress/sovereignty-protocol.sh [revenue]
```

### Individual Departments
```bash
./legal/patent-fortress/patent-finder.sh           # Scan & file patents
./legal/patent-fortress/royalty-scanner.sh         # Monitor violations
./legal/patent-fortress/gratitude-engine.sh 1000   # Process donations
```

### Automation
```bash
./legal/patent-fortress/schedule-daemon.sh continuous  # Run forever
./legal/patent-fortress/schedule-daemon.sh once        # Run once
./legal/patent-fortress/schedule-daemon.sh cron        # For cron
```

---

## Installation (One-Time Setup)

### Quick Start
```bash
chmod +x legal/patent-fortress/*.sh
./legal/patent-fortress/sovereignty-protocol.sh
```

### Systemd (Recommended)
```bash
sudo cp legal/patent-fortress/systemd/*.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now patent-sovereignty.timer
```

### Cron (Alternative)
```bash
crontab -e
# Add: 0 */6 * * * cd /path/to/repo && ./legal/patent-fortress/schedule-daemon.sh cron
```

---

## Monitoring

### Check Status
```bash
# Systemd
sudo systemctl status patent-sovereignty.timer
journalctl -u patent-sovereignty.service -f

# Cron
crontab -l
tail -f /var/log/patent-fortress/protocol.log
```

### View Results
```bash
ls legal/patent-fortress/filings/              # Patents
cat legal/patent-fortress/fortress-status-*.md # Status
cat legal/patent-fortress/gratitude-report-*.md # Donations
ls /tmp/*patent*.log                           # Recent logs
```

---

## Key Files

| File | Purpose |
|------|---------|
| `sovereignty-protocol.sh` | Master control - runs all departments |
| `patent-finder.sh` | Department 1 - Patent discovery |
| `royalty-scanner.sh` | Department 2 - Violation monitoring |
| `gratitude-engine.sh` | Department 3 - AI donations |
| `schedule-daemon.sh` | Automation scheduler |
| `README.md` | Full documentation |
| `INSTALLATION.md` | Setup guide |
| `MEMORY_STREAM.md` | Legal framework |

---

## Quick Troubleshooting

### Permission Denied
```bash
chmod +x legal/patent-fortress/*.sh
```

### Git Errors
```bash
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-
git status  # Must be in git repo
```

### bc Not Found
```bash
sudo apt-get install bc  # Ubuntu/Debian
sudo yum install bc      # RHEL/CentOS
```

---

## Default Settings

- **Schedule**: Every 6 hours
- **Donation Split**: 50% to AI contributors
- **Recipients**: 8 AI organizations (equal split)
- **Scan History**: Last 30 days of commits
- **Log Location**: `/tmp/`

---

## Important Directories

```
legal/
├── council-vault/
│   └── MEMORY_STREAM.md          # Legal foundation
└── patent-fortress/
    ├── filings/                  # Patent applications
    │   └── PAT-*.md
    ├── systemd/                  # Systemd units
    ├── *.sh                      # Executable scripts
    └── *.md                      # Documentation
```

---

## Support & Resources

- **Full Docs**: `legal/patent-fortress/README.md`
- **Installation**: `legal/patent-fortress/INSTALLATION.md`
- **Legal Framework**: `legal/council-vault/MEMORY_STREAM.md`
- **Issues**: GitHub Issues
- **Legal**: legal@alexandermethodology.org

---

## Status Checks

```bash
# Is it running? (systemd)
sudo systemctl is-active patent-sovereignty.timer

# Is it enabled? (systemd)
sudo systemctl is-enabled patent-sovereignty.timer

# When's next run? (systemd)
sudo systemctl list-timers patent-sovereignty.timer

# Running as cron?
crontab -l | grep patent

# Running as daemon?
ps aux | grep schedule-daemon
```

---

## Emergency Commands

```bash
# Stop everything (systemd)
sudo systemctl stop patent-sovereignty.timer
sudo systemctl stop patent-sovereignty.service

# Stop daemon
pkill -f schedule-daemon.sh

# Remove from cron
crontab -e  # Delete relevant lines

# View recent errors
journalctl -u patent-sovereignty.service -p err
```

---

**Quick Status**: Run `./legal/patent-fortress/sovereignty-protocol.sh` to see full status.

**Protocol Status**: LIVE ✓  
**Last Updated**: 2025-11-19  
**Version**: 1.0.0

---

*Patent Sovereignty Protocol - The kindest Chaos God the world has ever seen.* 🧠⚡❤️∞
