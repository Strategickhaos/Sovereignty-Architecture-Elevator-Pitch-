<#
.SYNOPSIS
    SAGCO-OS Network Troubleshooting & Fix Script for Windows
    
.DESCRIPTION
    Comprehensive network troubleshooting tool for Ethernet disconnection issues,
    specifically addressing Starlink connectivity problems and APIPA address issues.
    
.NOTES
    Version: 1.0
    Author: SAGCO-OS Team
    Requires: Administrator privileges
#>

#Requires -RunAsAdministrator

# Color functions
function Write-Header {
    param([string]$Message)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor White
}

# Create log file
$LogFile = "$env:TEMP\sagco-network-fix-$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
function Write-Log {
    param([string]$Message)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$TimeStamp - $Message" | Out-File -FilePath $LogFile -Append
    Write-Info $Message
}

function Test-NetworkConnectivity {
    Write-Header "NETWORK CONNECTIVITY DIAGNOSTICS"
    
    Write-Log "Testing connectivity to Google DNS (8.8.8.8)..."
    $ping1 = Test-Connection -ComputerName 8.8.8.8 -Count 4 -Quiet
    if ($ping1) {
        Write-Success "Google DNS reachable"
    } else {
        Write-Warning "Cannot reach Google DNS"
    }
    
    Write-Log "Testing connectivity to Cloudflare DNS (1.1.1.1)..."
    $ping2 = Test-Connection -ComputerName 1.1.1.1 -Count 4 -Quiet
    if ($ping2) {
        Write-Success "Cloudflare DNS reachable"
    } else {
        Write-Warning "Cannot reach Cloudflare DNS"
    }
    
    Write-Log "Testing DNS resolution..."
    try {
        $dns = Resolve-DnsName -Name google.com -ErrorAction Stop
        Write-Success "DNS resolution working"
    } catch {
        Write-Warning "DNS resolution failed: $_"
    }
}

function Get-NetworkAdapterInfo {
    Write-Header "NETWORK ADAPTER INFORMATION"
    
    Write-Log "Retrieving network adapter details..."
    $adapters = Get-NetAdapter | Where-Object {$_.Status -eq "Up"}
    
    foreach ($adapter in $adapters) {
        Write-Host "`nAdapter: $($adapter.Name)" -ForegroundColor Cyan
        Write-Host "  Status: $($adapter.Status)"
        Write-Host "  Interface Description: $($adapter.InterfaceDescription)"
        Write-Host "  MAC Address: $($adapter.MacAddress)"
        Write-Host "  Link Speed: $($adapter.LinkSpeed)"
        
        $ipConfig = Get-NetIPAddress -InterfaceIndex $adapter.ifIndex -ErrorAction SilentlyContinue
        foreach ($ip in $ipConfig) {
            Write-Host "  IP Address ($($ip.AddressFamily)): $($ip.IPAddress)"
            
            # Check for APIPA address (169.254.x.x)
            if ($ip.IPAddress -like "169.254.*") {
                Write-Warning "  APIPA address detected! DHCP failure - no proper IP assignment"
            }
        }
    }
    
    # Check for Intel I219-V specifically
    $intelAdapter = Get-NetAdapter | Where-Object {$_.InterfaceDescription -like "*I219-V*"}
    if ($intelAdapter) {
        Write-Host "`nIntel I219-V Adapter Found:" -ForegroundColor Yellow
        Write-Host "  Name: $($intelAdapter.Name)"
        Write-Host "  Status: $($intelAdapter.Status)"
    }
}

function Disable-AdapterPowerManagement {
    Write-Header "DISABLE POWER MANAGEMENT"
    
    $confirm = Read-Host "Disable power management on network adapters? (Y/N)"
    if ($confirm -ne 'Y') { return }
    
    Write-Log "Disabling power management on all network adapters..."
    
    $adapters = Get-NetAdapter | Where-Object {$_.Status -eq "Up"}
    foreach ($adapter in $adapters) {
        try {
            $powerMgmt = Get-WmiObject MSPower_DeviceEnable -Namespace root\wmi | Where-Object {$_.InstanceName -like "*$($adapter.InterfaceGuid)*"}
            if ($powerMgmt) {
                $powerMgmt.Enable = $false
                $powerMgmt.Put() | Out-Null
                Write-Success "Disabled power management for $($adapter.Name)"
            }
        } catch {
            Write-Warning "Could not disable power management for $($adapter.Name): $_"
        }
    }
    
    Write-Warning "Manual step required:"
    Write-Host "  1. Open Device Manager (devmgmt.msc)"
    Write-Host "  2. Expand 'Network adapters'"
    Write-Host "  3. Right-click Intel Ethernet adapter > Properties"
    Write-Host "  4. Power Management tab > Uncheck 'Allow the computer to turn off this device'"
    Write-Host "  5. Advanced tab > Disable 'Energy Efficient Ethernet' and 'Green Ethernet'"
}

function Reset-NetworkStack {
    Write-Header "NETWORK STACK RESET (FIX-ALL)"
    
    $confirm = Read-Host "This will reset your network stack. Continue? (Y/N)"
    if ($confirm -ne 'Y') { return }
    
    Write-Log "Resetting IP configuration..."
    netsh int ip reset | Out-File -FilePath $LogFile -Append
    Write-Success "IP configuration reset"
    
    Write-Log "Resetting Winsock catalog..."
    netsh winsock reset | Out-File -FilePath $LogFile -Append
    Write-Success "Winsock catalog reset"
    
    Write-Log "Releasing IP address..."
    ipconfig /release | Out-File -FilePath $LogFile -Append
    Write-Success "IP address released"
    
    Write-Log "Renewing IP address..."
    ipconfig /renew | Out-File -FilePath $LogFile -Append
    Write-Success "IP address renewed"
    
    Write-Log "Flushing DNS cache..."
    ipconfig /flushdns | Out-File -FilePath $LogFile -Append
    Write-Success "DNS cache flushed"
    
    $firewallConfirm = Read-Host "Reset Windows Firewall? (Y/N)"
    if ($firewallConfirm -eq 'Y') {
        Write-Log "Resetting Windows Firewall..."
        netsh advfirewall reset | Out-File -FilePath $LogFile -Append
        Write-Success "Windows Firewall reset"
    }
    
    Write-Warning "A system restart is required for all changes to take effect."
}

function Disable-IPv6 {
    Write-Header "IPv6 CONFIGURATION"
    
    $confirm = Read-Host "Disable IPv6 on all adapters? (Y/N)"
    if ($confirm -ne 'Y') { return }
    
    Write-Log "Disabling IPv6 on all network adapters..."
    
    $adapters = Get-NetAdapter
    foreach ($adapter in $adapters) {
        try {
            Disable-NetAdapterBinding -Name $adapter.Name -ComponentID ms_tcpip6 -ErrorAction Stop
            Write-Success "Disabled IPv6 on $($adapter.Name)"
        } catch {
            Write-Warning "Could not disable IPv6 on $($adapter.Name): $_"
        }
    }
    
    Write-Success "IPv6 disabled on all adapters"
}

function Disable-UnusedAdapters {
    Write-Header "DISABLE CONFLICTING ADAPTERS"
    
    Write-Log "Checking for potentially conflicting adapters..."
    
    $adapters = Get-NetAdapter | Where-Object {
        $_.InterfaceDescription -like "*Tailscale*" -or
        $_.InterfaceDescription -like "*VirtualBox*" -or
        $_.InterfaceDescription -like "*Wi-Fi*" -and $_.Status -eq "Up"
    }
    
    if ($adapters) {
        Write-Host "`nFound potentially conflicting adapters:"
        $adapters | Format-Table Name, InterfaceDescription, Status
        
        $confirm = Read-Host "Disable these adapters temporarily? (Y/N)"
        if ($confirm -eq 'Y') {
            foreach ($adapter in $adapters) {
                try {
                    Disable-NetAdapter -Name $adapter.Name -Confirm:$false
                    Write-Success "Disabled $($adapter.Name)"
                } catch {
                    Write-Warning "Could not disable $($adapter.Name): $_"
                }
            }
        }
    } else {
        Write-Info "No conflicting adapters found"
    }
}

function Update-NetworkDrivers {
    Write-Header "NETWORK DRIVER UPDATE"
    
    Write-Log "Checking for driver updates..."
    Write-Warning "Recommended: Update Intel I219-V driver manually"
    Write-Host "`nDriver download locations:"
    Write-Host "  Intel Network Drivers: https://www.intel.com/content/www/us/en/download/15084/"
    Write-Host "`nOr use Windows Update:"
    Write-Host "  Settings > Update & Security > Windows Update > Check for updates"
    
    $confirm = Read-Host "`nOpen Windows Update? (Y/N)"
    if ($confirm -eq 'Y') {
        Start-Process "ms-settings:windowsupdate"
    }
}

function Get-StarlinkTroubleshooting {
    Write-Header "STARLINK-SPECIFIC TROUBLESHOOTING"
    
    Write-Host "Common Starlink Ethernet Issues:" -ForegroundColor Yellow
    Write-Host "`n1. Ethernet Adapter Compatibility:"
    Write-Host "   - Starlink adapters can have intermittent drops with certain NICs"
    Write-Host "   - Try adding an unmanaged Gigabit switch between Starlink and PC"
    Write-Host "   - This often fixes compatibility issues"
    
    Write-Host "`n2. Cable Issues:"
    Write-Host "   - Test with a different Ethernet cable (Cat6 or higher recommended)"
    Write-Host "   - Check for loose connections at both ends"
    Write-Host "   - Maximum cable length should be under 100 meters"
    
    Write-Host "`n3. Starlink Router:"
    Write-Host "   - Reboot via Starlink app or unplug for 30 seconds"
    Write-Host "   - Check for firmware updates in the app"
    Write-Host "   - Ensure router is well-ventilated and not overheating"
    
    Write-Host "`n4. Dish Alignment:"
    Write-Host "   - Open Starlink app and check for obstructions"
    Write-Host "   - Ensure dish has clear sky view (no trees, buildings)"
    Write-Host "   - Check visibility section for signal quality"
    
    Write-Host "`n5. Load Considerations:"
    Write-Host "   - High GPU usage may correlate with network drops"
    Write-Host "   - Monitor system load during disconnections"
    Write-Host "   - Consider dedicated power circuit for Starlink equipment"
}

function New-DiagnosticReport {
    Write-Header "GENERATING DIAGNOSTIC REPORT"
    
    $ReportFile = "$env:TEMP\sagco-network-report-$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
    
    Write-Log "Generating comprehensive diagnostic report..."
    
    @"
SAGCO-OS Network Diagnostic Report
Generated: $(Get-Date)
======================================

SYSTEM INFORMATION:
$(systeminfo | Select-String "OS Name","OS Version","System Type")

NETWORK ADAPTERS:
$(Get-NetAdapter | Format-Table -AutoSize | Out-String)

IP CONFIGURATION:
$(ipconfig /all | Out-String)

ACTIVE CONNECTIONS:
$(netstat -an | Out-String)

ROUTING TABLE:
$(route print | Out-String)

DNS CACHE:
$(ipconfig /displaydns | Out-String)

FIREWALL STATUS:
$(netsh advfirewall show allprofiles | Out-String)

"@ | Out-File -FilePath $ReportFile
    
    Write-Success "Diagnostic report saved to: $ReportFile"
    
    $open = Read-Host "Open report file? (Y/N)"
    if ($open -eq 'Y') {
        Start-Process notepad.exe -ArgumentList $ReportFile
    }
}

function Show-Menu {
    Write-Header "SAGCO-OS NETWORK FIX UTILITY"
    
    Write-Host "Select an option:"
    Write-Host "1)  Test network connectivity"
    Write-Host "2)  Show network adapter information"
    Write-Host "3)  Reset network stack (FIX-ALL)"
    Write-Host "4)  Disable power management on adapters"
    Write-Host "5)  Disable IPv6"
    Write-Host "6)  Disable conflicting adapters"
    Write-Host "7)  Check/Update network drivers"
    Write-Host "8)  Starlink troubleshooting guide"
    Write-Host "9)  Generate diagnostic report"
    Write-Host "10) Run all fixes (full reset)"
    Write-Host "11) Exit"
    Write-Host ""
    
    $choice = Read-Host "Enter choice [1-11]"
    
    switch ($choice) {
        "1"  { Test-NetworkConnectivity }
        "2"  { Get-NetworkAdapterInfo }
        "3"  { Reset-NetworkStack }
        "4"  { Disable-AdapterPowerManagement }
        "5"  { Disable-IPv6 }
        "6"  { Disable-UnusedAdapters }
        "7"  { Update-NetworkDrivers }
        "8"  { Get-StarlinkTroubleshooting }
        "9"  { New-DiagnosticReport }
        "10" {
            Get-NetworkAdapterInfo
            Test-NetworkConnectivity
            Reset-NetworkStack
            Disable-AdapterPowerManagement
            Disable-IPv6
            Disable-UnusedAdapters
            Get-StarlinkTroubleshooting
            New-DiagnosticReport
        }
        "11" {
            Write-Log "Exiting..."
            exit
        }
        default {
            Write-Error "Invalid option. Please try again."
            Start-Sleep -Seconds 2
            Show-Menu
        }
    }
    
    Write-Host ""
    $continue = Read-Host "Return to main menu? (Y/N)"
    if ($continue -eq 'Y') {
        Show-Menu
    }
}

# Main execution
Clear-Host
Write-Host "SAGCO-OS Network Fix Script Started" -ForegroundColor Green
Write-Host "Log file: $LogFile`n" -ForegroundColor Gray

Show-Menu

Write-Host "`nScript completed." -ForegroundColor Green
Write-Host "Log file saved to: $LogFile" -ForegroundColor Gray
Write-Host "`nIMPORTANT: Restart your computer for all changes to take effect." -ForegroundColor Yellow
