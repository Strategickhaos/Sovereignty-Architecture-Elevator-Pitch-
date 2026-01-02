# Athena Network Recovery Automation Script
# Purpose: Diagnose and fix network connectivity issues on Athena node
# Operator: strategickhaos / Domenic Garza
# Version: 1.0

#Requires -RunAsAdministrator

$ErrorActionPreference = "SilentlyContinue"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔥 ATHENA NETWORK RECOVERY AUTOMATION" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Function to test connectivity
function Test-NetworkConnectivity {
    param(
        [string]$TestName,
        [string]$Target = "8.8.8.8"
    )
    
    Write-Host "Testing: $TestName" -NoNewline
    $result = Test-Connection -ComputerName $Target -Count 2 -Quiet
    
    if ($result) {
        Write-Host " ✅ SUCCESS" -ForegroundColor Green
        return $true
    } else {
        Write-Host " ❌ FAILED" -ForegroundColor Red
        return $false
    }
}

# Function to display network adapter status
function Show-NetworkStatus {
    Write-Host "`n📊 CURRENT NETWORK STATUS" -ForegroundColor Cyan
    Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray
    
    $adapters = Get-NetAdapter | Where-Object {$_.Status -eq "Up"}
    foreach ($adapter in $adapters) {
        $ip = (Get-NetIPAddress -InterfaceAlias $adapter.Name -AddressFamily IPv4 -ErrorAction SilentlyContinue).IPAddress
        $metric = (Get-NetIPInterface -InterfaceAlias $adapter.Name -AddressFamily IPv4 -ErrorAction SilentlyContinue).InterfaceMetric
        
        Write-Host "  Interface: $($adapter.Name)" -ForegroundColor White
        Write-Host "    Status: $($adapter.Status)" -ForegroundColor Green
        Write-Host "    IP: $ip" -ForegroundColor Gray
        Write-Host "    Metric: $metric" -ForegroundColor Gray
        Write-Host "    Bytes Received: $($adapter.ReceivedBytes / 1MB) MB" -ForegroundColor Gray
        Write-Host ""
    }
}

# Function to check routing table
function Show-RouteInfo {
    Write-Host "📍 DEFAULT GATEWAY ROUTE" -ForegroundColor Cyan
    Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray
    
    $defaultRoute = Get-NetRoute -DestinationPrefix "0.0.0.0/0" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($defaultRoute) {
        Write-Host "  Gateway: $($defaultRoute.NextHop)" -ForegroundColor White
        Write-Host "  Interface: $($defaultRoute.InterfaceAlias)" -ForegroundColor Gray
        Write-Host "  Metric: $($defaultRoute.RouteMetric)" -ForegroundColor Gray
    } else {
        Write-Host "  ⚠️  No default gateway found!" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Initial diagnostics
Write-Host "🔍 PHASE 0: INITIAL DIAGNOSTICS" -ForegroundColor Magenta
Write-Host ""
Show-NetworkStatus
Show-RouteInfo

$initialTest = Test-NetworkConnectivity -TestName "Baseline connectivity"
Write-Host ""

if ($initialTest) {
    Write-Host "🎉 NETWORK IS ALREADY WORKING!" -ForegroundColor Green
    Write-Host "No fixes needed. Exiting." -ForegroundColor Green
    exit 0
}

# FIX ATTEMPT 1: Interface Metric Optimization
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔧 FIX ATTEMPT 1: INTERFACE METRIC OPTIMIZATION" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

try {
    Write-Host "Setting Ethernet interface metric to 1..." -ForegroundColor White
    Set-NetIPInterface -InterfaceAlias "Ethernet" -InterfaceMetric 1 -ErrorAction Stop
    Start-Sleep -Seconds 2
    
    $fix1Result = Test-NetworkConnectivity -TestName "After metric optimization"
    
    if ($fix1Result) {
        Write-Host "`n✅ FIX SUCCESSFUL: Interface metric optimization worked!" -ForegroundColor Green
        Write-Host "Internet connectivity restored." -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "  1. cd C:\Users\Me10101\sovereign-cloud" -ForegroundColor White
        Write-Host "  2. git push -u origin main" -ForegroundColor White
        exit 0
    }
} catch {
    Write-Host "⚠️  Could not modify Ethernet interface: $_" -ForegroundColor Yellow
}

Write-Host ""

# FIX ATTEMPT 2: VPN Service Termination
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔧 FIX ATTEMPT 2: VPN SERVICE TERMINATION" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Stop Tailscale
Write-Host "Stopping Tailscale service..." -ForegroundColor White
Stop-Service -Name "Tailscale" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Kill ProtonVPN processes
Write-Host "Terminating ProtonVPN processes..." -ForegroundColor White
$protonProcesses = Get-Process | Where-Object {$_.Name -like "*ProtonVPN*"}
foreach ($proc in $protonProcesses) {
    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
    Write-Host "  Killed: $($proc.Name) (PID: $($proc.Id))" -ForegroundColor Gray
}

# Kill DuckDuckGo VPN processes
Write-Host "Terminating DuckDuckGo VPN processes..." -ForegroundColor White
$ddgProcesses = Get-Process | Where-Object {$_.Name -like "*DuckDuckGo*"}
foreach ($proc in $ddgProcesses) {
    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
    Write-Host "  Killed: $($proc.Name) (PID: $($proc.Id))" -ForegroundColor Gray
}

Start-Sleep -Seconds 3

$fix2Result = Test-NetworkConnectivity -TestName "After VPN termination"

if ($fix2Result) {
    Write-Host "`n✅ FIX SUCCESSFUL: VPN conflicts resolved!" -ForegroundColor Green
    Write-Host "Internet connectivity restored." -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  WARNING: Tailscale is stopped. Restart after git push:" -ForegroundColor Yellow
    Write-Host "  Start-Service Tailscale" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. cd C:\Users\Me10101\sovereign-cloud" -ForegroundColor White
    Write-Host "  2. git push -u origin main" -ForegroundColor White
    Write-Host "  3. Start-Service Tailscale" -ForegroundColor White
    exit 0
}

Write-Host ""

# FIX ATTEMPT 3: Flush DNS and Reset Network Stack
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔧 FIX ATTEMPT 3: DNS FLUSH & NETWORK STACK RESET" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "Flushing DNS cache..." -ForegroundColor White
ipconfig /flushdns | Out-Null

Write-Host "Resetting Winsock catalog..." -ForegroundColor White
netsh winsock reset | Out-Null

Write-Host "Resetting IP stack..." -ForegroundColor White
netsh int ip reset | Out-Null

Start-Sleep -Seconds 2

$fix3Result = Test-NetworkConnectivity -TestName "After network stack reset"

if ($fix3Result) {
    Write-Host "`n✅ FIX SUCCESSFUL: Network stack reset worked!" -ForegroundColor Green
    Write-Host "Internet connectivity restored." -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  SYSTEM RESTART RECOMMENDED to complete network stack reset." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. cd C:\Users\Me10101\sovereign-cloud" -ForegroundColor White
    Write-Host "  2. git push -u origin main" -ForegroundColor White
    exit 0
}

Write-Host ""

# FINAL STATUS
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "❌ AUTOMATED FIXES UNSUCCESSFUL" -ForegroundColor Red
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔧 MANUAL INTERVENTION REQUIRED" -ForegroundColor Yellow
Write-Host ""
Write-Host "Remaining Options:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Option 3: Direct Router Connection" -ForegroundColor White
Write-Host "  1. Unplug Athena from current switch" -ForegroundColor Gray
Write-Host "  2. Connect directly to ASUS ROG router" -ForegroundColor Gray
Write-Host "  3. Wait 30 seconds" -ForegroundColor Gray
Write-Host "  4. Re-run this script" -ForegroundColor Gray
Write-Host ""
Write-Host "Option 4: USB Tether Bypass" -ForegroundColor White
Write-Host "  1. Connect phone to Athena via USB" -ForegroundColor Gray
Write-Host "  2. Enable USB Tethering on phone" -ForegroundColor Gray
Write-Host "  3. Wait 30 seconds" -ForegroundColor Gray
Write-Host "  4. Re-run this script" -ForegroundColor Gray
Write-Host ""

Write-Host "🔍 DIAGNOSTIC INFORMATION" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray

# Show Windows Filtering Platform status
Write-Host "`nWindows Filtering Platform Status:" -ForegroundColor White
$wfpService = Get-Service -Name "BFE" -ErrorAction SilentlyContinue
if ($wfpService) {
    Write-Host "  Status: $($wfpService.Status)" -ForegroundColor Gray
}

# Show firewall profiles
Write-Host "`nFirewall Profiles:" -ForegroundColor White
$fwProfiles = Get-NetFirewallProfile
foreach ($profile in $fwProfiles) {
    Write-Host "  $($profile.Name): $($profile.Enabled)" -ForegroundColor Gray
}

# Show route table
Write-Host "`nRoute Table:" -ForegroundColor White
route print 0.0.0.0 | Select-String "0.0.0.0"

Write-Host ""
Write-Host "For detailed diagnostics, review:" -ForegroundColor Cyan
Write-Host "  SOVEREIGN_CLOUD_INFRASTRUCTURE_STATUS.md" -ForegroundColor White
Write-Host "  ATHENA_NETWORK_QUICKFIX.md" -ForegroundColor White
Write-Host ""

exit 1
