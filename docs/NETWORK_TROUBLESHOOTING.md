# 🌐 SAGCO-OS Network Troubleshooting Guide

## Overview

This guide addresses Ethernet disconnection issues, particularly with Starlink setups, including APIPA address problems (169.254.x.x) and intermittent connectivity drops.

## Quick Reference

### Problem Symptoms
- ✅ Sometimes shows valid IP (e.g., 192.168.1.28)
- ❌ Other times falls back to APIPA address (169.254.x.x)
- ⚠️ Intermittent connection drops
- ⚠️ DHCP lease failures

### Common Causes
1. **Hardware/Cable Issues**: Faulty cable, loose connections, Starlink adapter problems
2. **Power Management**: Windows turning off adapter to save power
3. **Driver Conflicts**: Outdated Intel I219-V driver, Tailscale/VirtualBox interference
4. **Starlink-Specific**: Signal obstructions, firmware bugs, router overload
5. **Other**: Router issues, IPv6 conflicts, Energy Efficient Ethernet settings

---

## 🚀 Quick Fixes (Try First)

### 1. Basic Hardware Checks

```bash
# Physical checks (no commands needed):
- Swap Ethernet cable with known good Cat6 or higher
- Insert cheap unmanaged switch between PC and Starlink router
- Reboot Starlink router (via app or unplug 30 seconds)
- Check Starlink app for obstructions
```

### 2. Disable Power Saving (Windows)

**GUI Method:**
1. Open Device Manager (`devmgmt.msc`)
2. Expand "Network adapters"
3. Right-click "Intel(R) Ethernet Connection (2) I219-V"
4. Properties > Power Management tab
5. **Uncheck** "Allow the computer to turn off this device to save power"
6. Advanced tab > **Disable** "Energy Efficient Ethernet" and "Green Ethernet"

**PowerShell Method:**
```powershell
# Run as Administrator
Get-NetAdapter | ForEach-Object {
    $adapter = $_
    $powerMgmt = Get-WmiObject MSPower_DeviceEnable -Namespace root\wmi | 
        Where-Object {$_.InstanceName -like "*$($adapter.InterfaceGuid)*"}
    if ($powerMgmt) {
        $powerMgmt.Enable = $false
        $powerMgmt.Put()
    }
}
```

### 3. Update Network Drivers

**Windows Update:**
```
Settings > Update & Security > Windows Update > Check for updates
```

**Manual Download:**
- Intel I219-V Driver: https://www.intel.com/content/www/us/en/download/15084/
- Download latest version for Windows 11

**Uninstall/Reinstall Method:**
1. Device Manager > Network adapters
2. Right-click Intel Ethernet > Uninstall device
3. Check "Delete the driver software"
4. Restart computer (Windows will reinstall driver)

### 4. Disable Conflicting Adapters

**PowerShell:**
```powershell
# Disable Tailscale
Disable-NetAdapter -Name "Tailscale" -Confirm:$false

# Disable VirtualBox Host-Only
Get-NetAdapter | Where-Object {$_.InterfaceDescription -like "*VirtualBox*"} | 
    Disable-NetAdapter -Confirm:$false

# Disable Wi-Fi (if using Ethernet)
Disable-NetAdapter -Name "Wi-Fi*" -Confirm:$false
```

**IPv6 Disable:**
```powershell
# Disable IPv6 on all adapters
Get-NetAdapter | ForEach-Object {
    Disable-NetAdapterBinding -Name $_.Name -ComponentID ms_tcpip6
}
```

---

## 🔧 Command-Based Reset (FIX-ALL)

### Using SAGCO-OS Scripts

**PowerShell (Recommended for Windows):**
```powershell
# Run as Administrator
cd scripts
.\SAGCO-Network-Fix.ps1
# Select option 10 for "Run all fixes"
```

**Bash (Git Bash/WSL):**
```bash
# Run as Administrator
cd scripts
chmod +x sagco-network-fix.sh
./sagco-network-fix.sh
# Select option 8 for "Run all fixes"
```

### Manual Network Reset Commands

**Windows (Command Prompt as Admin):**
```cmd
netsh int ip reset
netsh winsock reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns
netsh advfirewall reset
```

**After running commands:**
```
Restart computer for changes to take effect
```

**Linux/WSL:**
```bash
sudo systemctl restart NetworkManager
sudo dhclient -r && sudo dhclient
sudo systemd-resolve --flush-caches
```

---

## 🛠️ Starlink-Specific Troubleshooting

### Common Starlink Issues

1. **Ethernet Adapter Compatibility**
   - Starlink adapters known for intermittent drops with certain routers/NICs
   - **Solution**: Add unmanaged Gigabit switch (5-port from Amazon ~$15)
   - Place switch between Starlink router and PC

2. **Cable Quality**
   - Use Cat6 or higher Ethernet cable
   - Maximum recommended length: 100 meters
   - Test with different cable to rule out physical damage

3. **Router Management**
   - Reboot router via Starlink app
   - Or unplug power for 30 seconds, then plug back in
   - Check for firmware updates in app
   - Ensure router has proper ventilation (can overheat)

4. **Dish Alignment & Obstructions**
   - Open Starlink app
   - Navigate to Visibility/Obstructions section
   - Ensure dish has clear sky view
   - Move dish if trees/buildings obstruct view
   - Check for physical damage or snow/ice buildup

5. **Signal Quality Monitoring**
   - Use Starlink app to monitor signal quality
   - Check for pattern: Does connection drop during specific times?
   - Note if drops correlate with weather conditions

6. **High Load Scenarios**
   - Monitor GPU usage during disconnections
   - High GPU load (76%+) may correlate with network drops
   - Consider power circuit capacity for all equipment

---

## 🔍 Diagnostic Tools

### Check Current Network Status

**PowerShell:**
```powershell
# View all network adapters
Get-NetAdapter | Format-Table Name, Status, LinkSpeed, InterfaceDescription

# Check IP configuration
Get-NetIPAddress | Where-Object {$_.AddressFamily -eq "IPv4"} | 
    Format-Table InterfaceAlias, IPAddress, PrefixLength

# Identify APIPA addresses (169.254.x.x)
Get-NetIPAddress | Where-Object {$_.IPAddress -like "169.254.*"}

# Test connectivity
Test-Connection -ComputerName 8.8.8.8 -Count 4
Test-Connection -ComputerName 1.1.1.1 -Count 4

# Check DNS
Resolve-DnsName google.com
```

**Command Prompt:**
```cmd
ipconfig /all
netstat -an
route print
arp -a
```

### Generate Diagnostic Report

**Using SAGCO Script:**
```powershell
.\SAGCO-Network-Fix.ps1
# Select option 9: "Generate diagnostic report"
```

**Manual Report:**
```cmd
systeminfo > %TEMP%\network-report.txt
ipconfig /all >> %TEMP%\network-report.txt
route print >> %TEMP%\network-report.txt
netstat -an >> %TEMP%\network-report.txt
notepad %TEMP%\network-report.txt
```

---

## 🏥 Advanced Troubleshooting

### Clean Boot to Isolate Software Conflicts

1. Press `Win + R`, type `msconfig`, press Enter
2. Services tab > Check "Hide all Microsoft services"
3. Click "Disable all"
4. Startup tab > Open Task Manager
5. Disable all startup items
6. Restart computer
7. Test network connectivity
8. If working, re-enable services one-by-one to identify culprit

### Windows Network Reset

**Settings Method:**
```
Settings > Network & Internet > Advanced network settings > 
Network reset > Reset now
```

This will:
- Remove and reinstall all network adapters
- Reset networking components to defaults
- Requires restart

### Registry Tweaks (Advanced Users Only)

**Disable Large Send Offload (LSO):**
```powershell
Set-NetAdapterLso -Name "Ethernet" -IPv4Enabled $false -IPv6Enabled $false
```

**Disable TCP Chimney Offload:**
```cmd
netsh int tcp set global chimney=disabled
```

**Disable Receive Side Scaling (RSS):**
```powershell
Set-NetAdapterRss -Name "Ethernet" -Enabled $false
```

### Hardware Workarounds

1. **USB Ethernet Adapter**
   - Use as temporary workaround
   - Often bypasses driver/NIC compatibility issues
   - Recommended: USB 3.0 Gigabit adapters

2. **PCIe Network Card**
   - Install dedicated network card
   - Bypass onboard Intel I219-V completely
   - Recommended brands: Intel, Broadcom, Realtek

---

## 📊 Monitoring & Prevention

### Continuous Monitoring

**PowerShell Monitoring Script:**
```powershell
while ($true) {
    $adapters = Get-NetAdapter | Where-Object {$_.Status -eq "Up"}
    foreach ($adapter in $adapters) {
        $ip = (Get-NetIPAddress -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4).IPAddress
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        
        if ($ip -like "169.254.*") {
            Write-Host "$timestamp - WARNING: APIPA address on $($adapter.Name): $ip" -ForegroundColor Red
        } else {
            Write-Host "$timestamp - OK: $($adapter.Name) has valid IP: $ip" -ForegroundColor Green
        }
    }
    Start-Sleep -Seconds 60
}
```

### Event Log Monitoring

**Check Network Events:**
```powershell
Get-EventLog -LogName System -Source "e1dexpress" -Newest 50 |
    Format-Table TimeGenerated, EntryType, Message -AutoSize
```

### Automated Reconnection Script

**PowerShell Auto-Reconnect:**
```powershell
# Save as auto-reconnect.ps1, run as Administrator
$adapterName = "Ethernet"

while ($true) {
    $ip = (Get-NetIPAddress -InterfaceAlias $adapterName -AddressFamily IPv4 -ErrorAction SilentlyContinue).IPAddress
    
    if ($ip -like "169.254.*" -or $null -eq $ip) {
        Write-Host "APIPA detected or no IP. Attempting reconnect..." -ForegroundColor Yellow
        
        # Disable and re-enable adapter
        Disable-NetAdapter -Name $adapterName -Confirm:$false
        Start-Sleep -Seconds 5
        Enable-NetAdapter -Name $adapterName -Confirm:$false
        Start-Sleep -Seconds 10
        
        # Renew DHCP
        ipconfig /release
        ipconfig /renew
    }
    
    Start-Sleep -Seconds 30
}
```

---

## 🎯 Troubleshooting Decision Tree

```
Network Issue?
│
├─ APIPA Address (169.254.x.x)?
│  ├─ Yes → Run Network Reset Commands
│  │       → Check DHCP Server (Router)
│  │       → Disable/Re-enable Adapter
│  └─ No → Continue to next check
│
├─ Intermittent Drops?
│  ├─ Yes → Disable Power Management
│  │       → Check Cable/Hardware
│  │       → Update Drivers
│  └─ No → Continue to next check
│
├─ Starlink Setup?
│  ├─ Yes → Add Unmanaged Switch
│  │       → Check Dish Obstructions
│  │       → Reboot Router
│  └─ No → Continue to next check
│
├─ Multiple Adapters Active?
│  ├─ Yes → Disable Unused Adapters
│  │       → Disable IPv6
│  │       → Check for Conflicts
│  └─ No → Continue to next check
│
└─ Still Having Issues?
   → Generate Diagnostic Report
   → Contact Support with Report
   → Consider Hardware Replacement
```

---

## 📞 Support & Resources

### Official Resources
- **Intel Driver Support**: https://www.intel.com/content/www/us/en/support.html
- **Starlink Support**: https://support.starlink.com/
- **Microsoft Network Troubleshooter**: `ms-settings:network-troubleshooter`

### Community Resources
- SAGCO-OS GitHub Issues: [Report network issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- Discord Community: Join for real-time support

### Script Locations
- **PowerShell**: `/scripts/SAGCO-Network-Fix.ps1`
- **Bash**: `/scripts/sagco-network-fix.sh`

---

## ⚠️ Important Notes

1. **Always backup important data** before running network reset commands
2. **Administrator privileges required** for most fixes
3. **Restart required** after most changes
4. **Document your configuration** before making changes
5. **One change at a time** - easier to identify what fixed the issue

---

## 🔄 Version History

- **v1.0** (2025-01-25): Initial release
  - Network reset commands
  - Starlink troubleshooting
  - Power management fixes
  - Driver update guidance

---

**Built with 🔥 by the SAGCO-OS Team**

*Sovereign Network Infrastructure for Everyone*
