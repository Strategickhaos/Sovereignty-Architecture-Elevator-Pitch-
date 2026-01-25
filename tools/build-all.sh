#!/bin/bash
# build-all.sh - Build all Sovereignty Architecture distribution artifacts
#
# This is the master build script that creates:
# 1. Bootable USB image
# 2. VirtualBox VM
# 3. PDF documentation
# 4. AI-generated movie
# 5. Release package
# 6. Proton Drive backup

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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

log_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} $1"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
}

# Configuration
BUILD_DIR="./build-output"
RELEASE_VERSION="${RELEASE_VERSION:-1.0.0}"
RELEASE_DATE=$(date +%Y%m%d)

main() {
    log_header "🔥 Sovereignty Architecture - Build All Artifacts"
    
    log_info "Release Version: ${RELEASE_VERSION}"
    log_info "Build Date: ${RELEASE_DATE}"
    log_info "Build Directory: ${BUILD_DIR}"
    echo ""
    
    # Create build directory
    log_info "Creating build directory..."
    mkdir -p "${BUILD_DIR}"
    
    # 1. Build Bootable USB Image
    log_header "📦 Step 1: Building Bootable USB Image"
    if [ -f "./usb/build-scripts/build-sovereignty-usb.sh" ]; then
        cd usb/build-scripts
        ./build-sovereignty-usb.sh || log_warn "USB build failed or requires sudo"
        cd ../..
        
        # Move outputs to build directory
        mv usb/build-scripts/sovereignty-os-*.img* "${BUILD_DIR}/" 2>/dev/null || log_warn "No USB image found"
    else
        log_warn "USB build script not found, skipping"
    fi
    echo ""
    
    # 2. Build VirtualBox VM
    log_header "🖥️  Step 2: Building VirtualBox VM"
    if [ -f "./vm/virtualbox/build-vm.sh" ]; then
        if command -v VBoxManage &> /dev/null; then
            cd vm/virtualbox
            ./build-vm.sh || log_warn "VM build failed"
            cd ../..
            
            # Move outputs to build directory
            mv vm/virtualbox/sovereignty-vm-*.ova* "${BUILD_DIR}/" 2>/dev/null || log_warn "No VM OVA found"
            mv vm/virtualbox/VM_INFO.txt "${BUILD_DIR}/" 2>/dev/null || true
        else
            log_warn "VirtualBox not installed, skipping VM build"
        fi
    else
        log_warn "VM build script not found, skipping"
    fi
    echo ""
    
    # 3. Build PDF Documentation
    log_header "📚 Step 3: Building PDF Documentation"
    if [ -f "DISTRIBUTION_ARTIFACTS.md" ]; then
        log_info "Converting DISTRIBUTION_ARTIFACTS.md to PDF..."
        
        if command -v pandoc &> /dev/null; then
            if command -v xelatex &> /dev/null; then
                pandoc DISTRIBUTION_ARTIFACTS.md \
                    -o "${BUILD_DIR}/sovereignty-distribution-guide-v${RELEASE_VERSION}.pdf" \
                    --pdf-engine=xelatex \
                    --toc \
                    --number-sections \
                    -V geometry:margin=1in \
                    -V fontsize=11pt || log_warn "PDF generation failed"
            else
                log_warn "xelatex not found. Install with: sudo apt-get install texlive-xelatex"
                log_info "Skipping PDF generation"
            fi
        else
            log_warn "Pandoc not installed. Install with: sudo apt-get install pandoc texlive-xelatex"
            log_info "Skipping PDF generation"
        fi
    fi
    
    if [ -f "README.md" ]; then
        log_info "Converting README.md to PDF..."
        
        if command -v pandoc &> /dev/null && command -v xelatex &> /dev/null; then
            pandoc README.md \
                -o "${BUILD_DIR}/sovereignty-readme-v${RELEASE_VERSION}.pdf" \
                --pdf-engine=xelatex \
                --toc \
                -V geometry:margin=1in \
                -V fontsize=11pt || log_warn "README PDF generation failed"
        fi
    fi
    echo ""
    
    # 4. Generate Movie Storyboard (placeholder - actual generation would be complex)
    log_header "🎬 Step 4: Movie Generation"
    log_info "Movie storyboard available in: media/movie/storyboard/STORYBOARD.md"
    log_warn "Full movie generation requires additional tools (ElevenLabs, Stable Diffusion, etc.)"
    log_info "See STORYBOARD.md for production instructions"
    
    # Copy storyboard to build directory
    cp media/movie/storyboard/STORYBOARD.md "${BUILD_DIR}/movie-storyboard.md" 2>/dev/null || true
    echo ""
    
    # 5. Create Release Package
    log_header "📦 Step 5: Creating Release Package"
    RELEASE_NAME="sovereignty-architecture-v${RELEASE_VERSION}-${RELEASE_DATE}"
    RELEASE_DIR="${BUILD_DIR}/${RELEASE_NAME}"
    
    log_info "Creating release directory: ${RELEASE_NAME}"
    mkdir -p "${RELEASE_DIR}"
    
    # Copy all artifacts
    log_info "Copying artifacts to release directory..."
    cp "${BUILD_DIR}"/sovereignty-*.img* "${RELEASE_DIR}/" 2>/dev/null || true
    cp "${BUILD_DIR}"/sovereignty-*.ova* "${RELEASE_DIR}/" 2>/dev/null || true
    cp "${BUILD_DIR}"/sovereignty-*.pdf "${RELEASE_DIR}/" 2>/dev/null || true
    cp "${BUILD_DIR}"/VM_INFO.txt "${RELEASE_DIR}/" 2>/dev/null || true
    cp "${BUILD_DIR}"/movie-storyboard.md "${RELEASE_DIR}/" 2>/dev/null || true
    
    # Create README for release
    cat > "${RELEASE_DIR}/README.txt" << EOF
Sovereignty Architecture - Release ${RELEASE_VERSION}
Built: ${RELEASE_DATE}

This release contains the following artifacts:

📦 Bootable USB Image
   - sovereignty-os-*.img - Write to USB with dd command
   - sovereignty-os-*.img.sha256 - Checksum for verification

🖥️  VirtualBox VM
   - sovereignty-vm-*.ova - Import into VirtualBox
   - sovereignty-vm-*.ova.sha256 - Checksum for verification
   - VM_INFO.txt - VM specifications and usage

📚 Documentation
   - sovereignty-distribution-guide-*.pdf - Complete distribution guide
   - sovereignty-readme-*.pdf - Quick start guide
   - movie-storyboard.md - AI movie production plan

QUICK START:

Option 1: Bootable USB
  sudo dd if=sovereignty-os-*.img of=/dev/sdX bs=4M status=progress
  (Replace /dev/sdX with your USB device)

Option 2: VirtualBox VM
  VBoxManage import sovereignty-vm-*.ova
  VBoxManage startvm "Sovereignty-Architecture" --type gui

Option 3: GitHub Repository
  git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-

VERIFICATION:

Verify checksums:
  sha256sum -c *.sha256

SUPPORT:

- Documentation: README.pdf and DISTRIBUTION_GUIDE.pdf
- Issues: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues
- Community: See COMMUNITY.md in repository

Built with 🔥 by the Sovereignty Architecture collective
"This is not randomness. This is cognitive sovereignty."
EOF
    
    # Generate checksums
    log_info "Generating checksums..."
    cd "${RELEASE_DIR}"
    sha256sum sovereignty-* > checksums.txt 2>/dev/null || true
    cd - > /dev/null
    
    # Sign checksums (if GPG key available)
    if command -v gpg &> /dev/null && gpg --list-keys sovereignty@strategickhaos.com &> /dev/null; then
        log_info "Signing checksums with GPG..."
        cd "${RELEASE_DIR}"
        gpg --clearsign --local-user sovereignty@strategickhaos.com checksums.txt || log_warn "GPG signing failed"
        cd - > /dev/null
    else
        log_warn "GPG key not available, skipping signature"
    fi
    
    # Create tarball
    log_info "Creating release tarball..."
    cd "${BUILD_DIR}"
    tar czf "${RELEASE_NAME}.tar.gz" "${RELEASE_NAME}/"
    sha256sum "${RELEASE_NAME}.tar.gz" > "${RELEASE_NAME}.tar.gz.sha256"
    cd - > /dev/null
    
    log_info "✅ Release package created: ${BUILD_DIR}/${RELEASE_NAME}.tar.gz"
    echo ""
    
    # 6. Upload to Proton Drive
    log_header "☁️  Step 6: Backup to Proton Drive"
    if [ -f "./backups/scripts/backup-to-proton.sh" ]; then
        ./backups/scripts/backup-to-proton.sh || log_warn "Proton Drive backup failed or not configured"
    else
        log_warn "Backup script not found, skipping"
    fi
    echo ""
    
    # Summary
    log_header "✅ Build Complete - Summary"
    
    log_info "Build artifacts location: ${BUILD_DIR}/"
    log_info "Release package: ${BUILD_DIR}/${RELEASE_NAME}.tar.gz"
    echo ""
    
    log_info "Contents:"
    du -sh "${RELEASE_DIR}"/* 2>/dev/null | while read size file; do
        echo "  - $(basename "$file"): $size"
    done
    echo ""
    
    log_info "Total release size: $(du -sh "${BUILD_DIR}/${RELEASE_NAME}.tar.gz" | cut -f1)"
    echo ""
    
    log_info "Next steps:"
    log_info "  1. Test each artifact"
    log_info "  2. Upload to GitHub releases"
    log_info "  3. Share with community"
    log_info "  4. Document deployment"
    echo ""
    
    log_info "🔥 Sovereignty Architecture - Build Complete!"
}

main "$@"
