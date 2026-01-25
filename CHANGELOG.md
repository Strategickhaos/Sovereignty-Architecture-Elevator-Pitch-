# Changelog

All notable changes to the SAGCO-OS / Sovereignty Architecture project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added - 2025-01-25

#### Network Troubleshooting Tools
- **SAGCO-Network-Fix.ps1**: Comprehensive PowerShell script for Windows network troubleshooting
  - Network stack reset functionality
  - Power management configuration for network adapters
  - IPv6 disable utility
  - Conflicting adapter detection and management
  - Driver update guidance
  - Diagnostic report generation
  - Interactive menu system with 11 options
  
- **sagco-network-fix.sh**: Bash script for Linux/WSL/Git Bash network troubleshooting
  - Network diagnostics and connectivity testing
  - Starlink-specific Ethernet fixes
  - Network stack reset commands
  - IPv6 configuration management
  - Hardware recommendations
  - Interactive menu system with 9 options

#### Documentation
- **docs/NETWORK_TROUBLESHOOTING.md**: Complete network troubleshooting guide (432 lines)
  - Quick fixes for common issues
  - Starlink-specific troubleshooting section
  - Command-based reset procedures
  - Diagnostic tools and commands
  - Advanced troubleshooting techniques
  - Monitoring and prevention strategies
  - Decision tree for systematic troubleshooting
  
- **docs/NETWORK_QUICK_REFERENCE.md**: Emergency quick reference card (153 lines)
  - Immediate fix commands
  - 5-minute Starlink Ethernet fix procedure
  - APIPA address detection
  - Quick diagnostics commands
  - PowerShell one-liners
  - Support checklist

#### Features Addressed
- APIPA address problems (169.254.x.x)
- Intermittent Ethernet disconnections
- Starlink adapter compatibility issues
- DHCP lease failures
- Power management causing network drops
- Driver conflicts (Intel I219-V)
- IPv6 conflicts
- VirtualBox/Tailscale adapter interference

#### README Updates
- Added Network Troubleshooting section
- Quick fix commands for immediate use
- Links to comprehensive documentation
- Script usage instructions

### Fixed
- Ethernet disconnection issues with Starlink setups
- APIPA address fallback problems
- Network adapter power management issues
- IPv6 interference with connectivity

### Changed
- Enhanced README with network troubleshooting information
- Improved documentation structure with dedicated network docs

## [1.7.0] - Previous Release

See git history for previous changes.

---

**Note**: This CHANGELOG was created to track the network troubleshooting feature additions. Historical changes may be added in future updates.
