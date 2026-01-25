# SAGCO-OS Network Troubleshooting Scripts

This directory contains network troubleshooting and diagnostic tools for resolving Ethernet connectivity issues.

## Scripts Overview

### 1. SAGCO-Network-Fix.ps1
**Platform:** Windows (PowerShell)  
**Requires:** Administrator privileges  
**Purpose:** Comprehensive network troubleshooting for Windows systems

#### Features
- Network connectivity testing
- Network adapter information display
- Network stack reset (fix-all)
- Power management configuration
- IPv6 disable utility
- Conflicting adapter management
- Driver update guidance
- Starlink-specific troubleshooting
- Diagnostic report generation
- Interactive menu system (11 options)

#### Usage
```powershell
# Open PowerShell as Administrator
cd scripts
.\SAGCO-Network-Fix.ps1

# Or run directly from anywhere
& "C:\path\to\scripts\SAGCO-Network-Fix.ps1"
```

#### Quick Fix (Option 3)
```powershell
.\SAGCO-Network-Fix.ps1
# Select option 3: Reset network stack (FIX-ALL)
# Select Y to confirm
# Restart computer when prompted
```

---

### 2. sagco-network-fix.sh
**Platform:** Linux, macOS, Windows (Git Bash/WSL)  
**Requires:** Root/Administrator privileges  
**Purpose:** Cross-platform network troubleshooting

#### Features
- Network diagnostics and connectivity testing
- Starlink Ethernet troubleshooting
- Network stack reset
- IPv6 configuration
- Hardware recommendations
- Diagnostic report generation
- Interactive menu system (9 options)
- Platform detection (Windows/Linux/macOS)

#### Usage
```bash
# Linux/macOS
sudo ./sagco-network-fix.sh

# Windows Git Bash (run as Administrator)
./sagco-network-fix.sh

# Skip admin check (testing only)
SKIP_ADMIN_CHECK=true ./sagco-network-fix.sh
```

#### Quick Fix (Option 2)
```bash
sudo ./sagco-network-fix.sh
# Select option 2: Reset network stack (fix-all)
# Confirm when prompted
# Restart system when complete
```

---

## Common Use Cases

### Issue: APIPA Address (169.254.x.x)
**Symptom:** Network adapter shows 169.254.x.x instead of proper IP

**Solution:**
```powershell
# PowerShell
.\SAGCO-Network-Fix.ps1
# Select option 3: Reset network stack
```

```bash
# Bash
sudo ./sagco-network-fix.sh
# Select option 2: Reset network stack
```

### Issue: Intermittent Ethernet Disconnections
**Symptom:** Connection randomly drops, then reconnects

**Solution:**
```powershell
# PowerShell
.\SAGCO-Network-Fix.ps1
# Select option 4: Disable power management
# Then option 5: Disable IPv6
```

### Issue: Starlink Ethernet Not Working
**Symptom:** Ethernet adapter shows as connected but no internet

**Solution:**
1. Check Starlink app for obstructions
2. Add an unmanaged switch between router and PC
3. Run script:
```powershell
.\SAGCO-Network-Fix.ps1
# Select option 8: Starlink troubleshooting guide
# Follow recommendations
# Select option 3: Reset network stack
```

---

## Script Features Comparison

| Feature | PowerShell | Bash |
|---------|-----------|------|
| Network connectivity test | ✅ | ✅ |
| Adapter information | ✅ | ✅ |
| Network stack reset | ✅ | ✅ |
| Power management config | ✅ | Manual |
| IPv6 disable | ✅ | ✅ |
| Conflicting adapter detection | ✅ | ❌ |
| Driver update guidance | ✅ | ✅ |
| Starlink troubleshooting | ✅ | ✅ |
| Diagnostic report | ✅ | ✅ |
| Platform detection | Windows only | Multi-platform |

---

## Environment Variables

### SKIP_ADMIN_CHECK (bash only)
Skip administrator privilege check (for testing)
```bash
SKIP_ADMIN_CHECK=true ./sagco-network-fix.sh
```

---

## Logging

Both scripts generate log files in the temp directory:

**Windows:**
```
%TEMP%\sagco-network-fix-YYYYMMDD_HHMMSS.log
```

**Linux/macOS:**
```
/tmp/sagco-network-fix-YYYYMMDD_HHMMSS.log
```

---

## Diagnostic Reports

Generated reports include:
- System information
- Network adapter details
- IP configuration
- Active connections
- Routing table
- DNS configuration
- Firewall status (Windows)

**Report location:**
- Windows: `%TEMP%\sagco-network-report-YYYYMMDD_HHMMSS.txt`
- Linux/macOS: `/tmp/sagco-network-report-YYYYMMDD_HHMMSS.txt`

---

## Safety Notes

⚠️ **Before running scripts:**
1. Backup any custom network configurations
2. Document your current settings
3. Close all network-dependent applications
4. Be prepared to restart your computer

⚠️ **Admin privileges required:**
- Both scripts require administrator/root privileges
- Network stack reset affects all network adapters
- Changes may require system restart

⚠️ **Testing in production:**
- Test in a safe environment first
- Document changes made
- Have a rollback plan ready

---

## Troubleshooting the Scripts

### PowerShell Execution Policy
If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Bash Permission Denied
If you get permission denied:
```bash
chmod +x sagco-network-fix.sh
sudo ./sagco-network-fix.sh
```

### Script Not Found
Ensure you're in the correct directory:
```bash
cd /path/to/SAGCO-OS/scripts
ls -la *.sh *.ps1
```

---

## Related Documentation

- **[Complete Troubleshooting Guide](../docs/NETWORK_TROUBLESHOOTING.md)**
- **[Quick Reference Card](../docs/NETWORK_QUICK_REFERENCE.md)**
- **[Main README](../README.md)**
- **[CHANGELOG](../CHANGELOG.md)**

---

## Support

For issues or questions:
1. Check the [troubleshooting documentation](../docs/NETWORK_TROUBLESHOOTING.md)
2. Generate a diagnostic report using the scripts
3. Open an issue on GitHub with the report attached
4. Join the Discord community for real-time help

---

## Version History

- **v1.0** (2025-01-25)
  - Initial release
  - PowerShell and Bash versions
  - Full network troubleshooting suite
  - Starlink-specific fixes
  - Platform detection
  - Improved error handling

---

**Built with 🔥 by the SAGCO-OS Team**
