#!/bin/bash
# backup-to-proton.sh - Automated Proton Drive backup script
#
# This script creates encrypted backups and uploads them to Proton Drive

set -euo pipefail

# Configuration
BACKUP_DATE=$(date +%Y-%m-%d)
BACKUP_TIME=$(date +%H%M%S)
BACKUP_DIR="/tmp/sovereignty-backup-${BACKUP_DATE}-${BACKUP_TIME}"
PROTON_MOUNT="${PROTON_MOUNT:-/mnt/proton-drive}"
GPG_RECIPIENT="${GPG_RECIPIENT:-sovereignty@strategickhaos.com}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

cleanup() {
    if [ -d "${BACKUP_DIR}" ]; then
        log_info "Cleaning up temporary backup directory..."
        rm -rf "${BACKUP_DIR}"
    fi
}

trap cleanup EXIT

main() {
    log_info "📦 Sovereignty Architecture - Proton Drive Backup"
    log_info "Date: ${BACKUP_DATE}"
    log_info "Time: ${BACKUP_TIME}"
    
    # Create backup directory
    log_info "Creating backup directory..."
    mkdir -p "${BACKUP_DIR}"
    
    # Backup code repositories
    log_info "Backing up code repositories..."
    tar czf "${BACKUP_DIR}/code-snapshot.tar.gz" \
        --exclude=node_modules \
        --exclude=.git \
        --exclude=__pycache__ \
        --exclude=*.pyc \
        --exclude=.venv \
        --exclude=venv \
        --exclude=dist \
        --exclude=build \
        --exclude=target \
        . 2>/dev/null || log_warn "Some files could not be backed up"
    
    log_info "Code backup size: $(du -h "${BACKUP_DIR}/code-snapshot.tar.gz" | cut -f1)"
    
    # Backup configuration files
    log_info "Backing up configuration files..."
    tar czf "${BACKUP_DIR}/config-snapshot.tar.gz" \
        --exclude=.git \
        .env* \
        *.yaml \
        *.yml \
        *.json \
        *.toml \
        docker-compose*.yml \
        Dockerfile* \
        2>/dev/null || log_warn "Some config files could not be backed up"
    
    # Backup documentation
    log_info "Backing up documentation..."
    tar czf "${BACKUP_DIR}/docs-snapshot.tar.gz" \
        --exclude=.git \
        *.md \
        docs/ \
        books/ \
        legal/ \
        2>/dev/null || log_warn "Some docs could not be backed up"
    
    # Encrypt backups
    log_info "🔐 Encrypting backups..."
    for file in "${BACKUP_DIR}"/*.tar.gz; do
        if [ -f "$file" ]; then
            log_info "Encrypting $(basename "$file")..."
            gpg --encrypt --recipient "${GPG_RECIPIENT}" \
                --trust-model always \
                --output "${file}.gpg" \
                "${file}"
            
            # Remove unencrypted version
            rm "${file}"
        fi
    done
    
    # Generate manifest
    log_info "Generating backup manifest..."
    cat > "${BACKUP_DIR}/manifest.json" << EOF
{
  "backup_date": "${BACKUP_DATE}",
  "backup_time": "${BACKUP_TIME}",
  "files": [
$(ls -1 "${BACKUP_DIR}"/*.gpg | while read file; do
    size=$(du -h "$file" | cut -f1)
    sha256=$(sha256sum "$file" | cut -d' ' -f1)
    echo "    {"
    echo "      \"name\": \"$(basename "$file")\","
    echo "      \"size\": \"$size\","
    echo "      \"sha256\": \"$sha256\""
    echo "    },"
done | sed '$ s/,$//')
  ],
  "encryption": "GPG",
  "recipient": "${GPG_RECIPIENT}"
}
EOF
    
    # Upload to Proton Drive (if configured)
    if [ -d "${PROTON_MOUNT}" ] && command -v rclone &> /dev/null; then
        log_info "☁️  Uploading to Proton Drive..."
        
        # Create snapshot directory on Proton Drive
        SNAPSHOT_DIR="${PROTON_MOUNT}/SNAPSHOTS/${BACKUP_DATE}"
        mkdir -p "${SNAPSHOT_DIR}"
        
        # Upload files
        rclone copy "${BACKUP_DIR}/" "${SNAPSHOT_DIR}/" \
            --progress \
            --checksum
        
        # Verify upload
        log_info "✅ Verifying upload..."
        rclone check "${BACKUP_DIR}/" "${SNAPSHOT_DIR}/" \
            --checksum
        
        if [ $? -eq 0 ]; then
            log_info "✅ Upload verified successfully"
        else
            log_error "Upload verification failed!"
            exit 1
        fi
        
    elif [ -d "${PROTON_MOUNT}" ]; then
        log_info "☁️  Copying to Proton Drive mount..."
        
        SNAPSHOT_DIR="${PROTON_MOUNT}/SNAPSHOTS/${BACKUP_DATE}"
        mkdir -p "${SNAPSHOT_DIR}"
        cp -v "${BACKUP_DIR}"/* "${SNAPSHOT_DIR}/"
        
        log_info "✅ Files copied to Proton Drive"
        
    else
        log_warn "Proton Drive not mounted at ${PROTON_MOUNT}"
        log_warn "Backup files saved locally in ${BACKUP_DIR}"
        log_warn "Manual upload required"
        
        # Don't cleanup if manual upload is needed
        trap - EXIT
        
        log_info "To upload manually:"
        log_info "  1. Mount Proton Drive"
        log_info "  2. Copy ${BACKUP_DIR}/* to Proton Drive/SNAPSHOTS/${BACKUP_DATE}/"
        log_info "  3. Verify upload"
        log_info "  4. Delete ${BACKUP_DIR}"
        
        exit 0
    fi
    
    # Log to backup history
    log_info "Logging backup to history..."
    echo "${BACKUP_DATE} ${BACKUP_TIME}: Backup completed successfully" >> backup-log.txt
    
    # Success
    log_info "✅ Backup complete!"
    log_info ""
    log_info "Backup location: ${PROTON_MOUNT}/SNAPSHOTS/${BACKUP_DATE}/"
    log_info "Encrypted files:"
    ls -lh "${BACKUP_DIR}"/*.gpg 2>/dev/null | awk '{print "  - "$9" ("$5")"}'
    log_info ""
    log_info "To restore:"
    log_info "  1. Download files from Proton Drive"
    log_info "  2. Decrypt: gpg --decrypt file.tar.gz.gpg > file.tar.gz"
    log_info "  3. Extract: tar xzf file.tar.gz"
}

# Check for required tools
if ! command -v gpg &> /dev/null; then
    log_error "GPG is not installed. Please install it first."
    exit 1
fi

main "$@"
