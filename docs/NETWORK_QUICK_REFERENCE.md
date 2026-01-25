# 🚨 SAGCO-OS Network Emergency Quick Reference

## 🔥 IMMEDIATE FIXES (No Scripts Needed)

### Option 1: Quick Network Reset (Windows - Run as Admin)
```cmd
netsh int ip reset && netsh winsock reset && ipconfig /release && ipconfig /renew && ipconfig /flushdns
```
**Then restart your computer.**

### Option 2: SAGCO Fix-All Command
```powershell
# PowerShell as Administrator
cd C:\path\to\SAGCO-OS\scripts
.\SAGCO-Network-Fix.ps1
# Select option 10
```

```bash
# Git Bash/WSL as Administrator
cd /path/to/SAGCO-OS/scripts
./sagco-network-fix.sh
# Select option 8
```

---

## 📋 5-Minute Starlink Ethernet Fix

1. **Add a cheap switch** ($15 unmanaged 5-port Gigabit)
   - Between Starlink router and your PC
   - Fixes 90% of Starlink Ethernet issues

2. **Disable power management**
   - Device Manager > Network adapters > Intel Ethernet
   - Properties > Power Management
   - Uncheck "Allow computer to turn off this device"

3. **Swap the cable**
   - Use Cat6 or higher
   - Try a different cable to rule out physical damage

4. **Reboot Starlink**
   - Unplug router for 30 seconds
   - Check Starlink app for obstructions

5. **Update Intel driver**
   - Download from: https://www.intel.com/content/www/us/en/download/15084/

---

## 🎯 Check for APIPA Address (169.254.x.x)

### Windows
```powershell
Get-NetIPAddress | Where-Object {$_.IPAddress -like "169.254.*"}
```

### Command Prompt
```cmd
ipconfig | findstr "169.254"
```

**If you see 169.254.x.x → DHCP failure! Run network reset above.**

---

## 🔍 Quick Diagnostics

### Test Connectivity
```cmd
ping 8.8.8.8
ping 1.1.1.1
ping google.com
```

### Check Adapters
```powershell
Get-NetAdapter | Format-Table Name, Status, LinkSpeed
```

### Release & Renew IP
```cmd
ipconfig /release
ipconfig /renew
```

---

## ⚡ PowerShell One-Liners

### Disable IPv6 on all adapters
```powershell
Get-NetAdapter | Disable-NetAdapterBinding -ComponentID ms_tcpip6
```

### Disable unused adapters (Tailscale, VirtualBox, Wi-Fi)
```powershell
Get-NetAdapter | Where-Object {$_.InterfaceDescription -like "*Tailscale*" -or $_.InterfaceDescription -like "*VirtualBox*"} | Disable-NetAdapter -Confirm:$false
```

### Re-enable Ethernet adapter
```powershell
Enable-NetAdapter -Name "Ethernet"
```

---

## 🛠️ Windows Network Reset (Settings)

```
Settings > Network & Internet > Advanced network settings > Network reset > Reset now
```
**Requires restart. This will reinstall all network adapters.**

---

## 📞 When All Else Fails

1. **Clean boot** to isolate software conflicts
   - `msconfig` > Services > Hide Microsoft > Disable all

2. **USB Ethernet adapter** as workaround
   - Bypasses problematic onboard NIC

3. **Check Windows Event Log**
   ```powershell
   Get-EventLog -LogName System -Source "e1dexpress" -Newest 20
   ```

4. **Generate diagnostic report**
   ```powershell
   .\SAGCO-Network-Fix.ps1  # Option 9
   ```

---

## 📝 Checklist Before Calling Support

- [ ] Tried different Ethernet cable
- [ ] Rebooted Starlink router
- [ ] Disabled power management on adapter
- [ ] Updated Intel network driver
- [ ] Ran network reset commands
- [ ] Checked Starlink app for obstructions
- [ ] Disabled conflicting adapters
- [ ] Generated diagnostic report

---

**Save this file! Print it! Pin it to your wall!**

**For full guide, see:** `docs/NETWORK_TROUBLESHOOTING.md`
