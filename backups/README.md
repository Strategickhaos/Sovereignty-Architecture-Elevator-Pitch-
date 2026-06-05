# Backups

This directory contains scripts and configurations for automated backup to Proton Drive and other secure storage locations.

## Quick Start

```bash
./scripts/backup-to-proton.sh
```

## Backup Strategy

The backup system implements the **Sister Protocol** principle: Never rely on a single point of failure.

### Backup Locations

1. **Proton Drive** (Primary)
   - End-to-end encrypted
   - Swiss privacy laws
   - Redundant data centers

2. **Local Storage** (Secondary)
   - External drives
   - NAS systems
   - Local archives

3. **GitHub** (Code)
   - Version controlled
   - Public/private repos
   - Distributed worldwide

4. **USB/VM** (Portable)
   - Bootable USB images
   - VirtualBox VMs
   - Self-contained environments

## Backup Structure

```
Proton-Drive/
├── RELEASES/              # Official releases
│   ├── v1.0.0/
│   └── latest/
├── SNAPSHOTS/             # Daily snapshots
│   ├── 2025-01-25/
│   └── 2025-01-26/
├── PROJECTS/              # Individual projects
│   ├── sagco-os/
│   ├── flamelang/
│   └── trig6/
├── LEGAL/                 # Legal documents
├── BOOKS/                 # Documentation
└── METADATA/              # Backup logs
```

## Scripts

### backup-to-proton.sh

Main backup script that:
1. Creates compressed archives
2. Encrypts with GPG
3. Uploads to Proton Drive
4. Verifies upload integrity
5. Logs backup history

Usage:
```bash
# Basic backup
./scripts/backup-to-proton.sh

# With custom GPG recipient
GPG_RECIPIENT=custom@email.com ./scripts/backup-to-proton.sh

# With custom Proton Drive mount
PROTON_MOUNT=/custom/path ./scripts/backup-to-proton.sh
```

## Configuration

### Proton Drive Setup

#### Option 1: Using rclone

```bash
# Install rclone
sudo apt-get install rclone

# Configure Proton Drive
rclone config
# Follow prompts to add Proton Drive

# Mount Proton Drive
rclone mount proton: /mnt/proton-drive --daemon
```

#### Option 2: Native Client

```bash
# Download Proton Drive client
# https://proton.me/drive/download

# Mount drive
# Follow client instructions
```

### GPG Setup

```bash
# Generate GPG key (if not exists)
gpg --full-generate-key
# Follow prompts

# List keys
gpg --list-keys

# Set default key
export GPG_RECIPIENT=sovereignty@strategickhaos.com
```

## Backup Schedule

### Automated Backups

Add to crontab:

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/backups/scripts/backup-to-proton.sh >> /var/log/sovereignty-backup.log 2>&1

# Add weekly full backup on Sunday at 3 AM
0 3 * * 0 /path/to/backups/scripts/backup-to-proton.sh >> /var/log/sovereignty-backup.log 2>&1
```

### Systemd Timer

Create `/etc/systemd/system/sovereignty-backup.service`:

```ini
[Unit]
Description=Sovereignty Architecture Backup
After=network.target

[Service]
Type=oneshot
ExecStart=/path/to/backups/scripts/backup-to-proton.sh
User=sovereign

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/sovereignty-backup.timer`:

```ini
[Unit]
Description=Daily Sovereignty Backup
Requires=sovereignty-backup.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:
```bash
sudo systemctl enable sovereignty-backup.timer
sudo systemctl start sovereignty-backup.timer
```

## Recovery Procedures

### Full System Recovery

1. **Download Backups**
   ```bash
   # Mount Proton Drive
   rclone mount proton: /mnt/proton-drive
   
   # Find latest snapshot
   ls -la /mnt/proton-drive/SNAPSHOTS/
   ```

2. **Decrypt Backups**
   ```bash
   gpg --decrypt code-snapshot.tar.gz.gpg > code-snapshot.tar.gz
   gpg --decrypt config-snapshot.tar.gz.gpg > config-snapshot.tar.gz
   ```

3. **Extract Files**
   ```bash
   tar xzf code-snapshot.tar.gz
   tar xzf config-snapshot.tar.gz
   ```

4. **Verify Integrity**
   ```bash
   # Check manifest
   cat manifest.json
   
   # Verify checksums
   sha256sum -c checksums.txt
   ```

### Partial Recovery

Restore specific project:
```bash
# Download project backup
rclone copy proton:/PROJECTS/flamelang/ ./flamelang-recovery/

# Decrypt if encrypted
for file in *.gpg; do
    gpg --decrypt "$file" > "${file%.gpg}"
done

# Extract
tar xzf flamelang-latest.tar.gz
```

## Verification

### Test Backup Integrity

```bash
# Download backup
rclone copy proton:/SNAPSHOTS/2025-01-25/ /tmp/test-restore/

# Decrypt
gpg --decrypt /tmp/test-restore/code-snapshot.tar.gz.gpg > /tmp/test-restore/code-snapshot.tar.gz

# Test extraction
tar tzf /tmp/test-restore/code-snapshot.tar.gz | head -20

# Cleanup
rm -rf /tmp/test-restore/
```

### Verify Encryption

```bash
# Ensure files are encrypted
file code-snapshot.tar.gz.gpg
# Should output: GPG encrypted data

# Verify can decrypt
gpg --list-packets code-snapshot.tar.gz.gpg
```

## Best Practices

1. **3-2-1 Rule**
   - 3 copies of data
   - 2 different storage media
   - 1 off-site backup

2. **Encryption**
   - Always encrypt sensitive data
   - Use strong GPG keys
   - Rotate keys periodically

3. **Testing**
   - Test restore monthly
   - Verify integrity weekly
   - Document recovery procedures

4. **Monitoring**
   - Check backup logs
   - Monitor disk space
   - Alert on failures

## Troubleshooting

**Backup fails:**
```bash
# Check Proton Drive mount
ls -la /mnt/proton-drive

# Check GPG key
gpg --list-keys sovereignty@strategickhaos.com

# Check disk space
df -h
```

**Upload slow:**
```bash
# Use compression
tar czf - files/ | gpg -e | rclone rcat proton:/path/file.tar.gz.gpg

# Limit bandwidth if needed
rclone --bwlimit 10M copy ...
```

**Decrypt fails:**
```bash
# Check GPG key availability
gpg --list-secret-keys

# Import key if needed
gpg --import private-key.asc
```

## Files

- `scripts/backup-to-proton.sh` - Main backup script
- `backup-log.txt` - Backup history log
- `README.md` - This file

## Support

For backup issues:
- Check logs: `tail -f backup-log.txt`
- Verify Proton Drive connection
- Test GPG encryption/decryption
- Open issue on GitHub

---

**Built with 🔥 by the Sovereignty Architecture collective**

*"Never rely on a single point of failure."*
