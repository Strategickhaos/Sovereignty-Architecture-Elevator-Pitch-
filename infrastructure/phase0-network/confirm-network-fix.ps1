# Phase 0: Network Fix Confirmation - DOM Evolution
# Confirms Ethernet interface metric fix and network connectivity

$ErrorActionPreference = "Stop"

Write-Host "🔥 DOM Evolution - Phase 0: Neural Pulse Confirmation 🔥" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Function to test network connectivity
function Test-NetworkPulse {
    Write-Host "Testing network connectivity to 8.8.8.8..." -ForegroundColor Yellow
    $pingResult = Test-Connection -ComputerName 8.8.8.8 -Count 4 -ErrorAction SilentlyContinue
    
    if ($pingResult) {
        Write-Host "✓ Network pulse detected! Average latency: $([math]::Round(($pingResult | Measure-Object -Property ResponseTime -Average).Average, 2))ms" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ Network pulse failed - no connectivity" -ForegroundColor Red
        return $false
    }
}

# Function to apply Ethernet metric fix
function Set-EthernetMetric {
    Write-Host ""
    Write-Host "Applying Ethernet interface metric fix..." -ForegroundColor Yellow
    
    try {
        # Get Ethernet interface
        $ethernetInterface = Get-NetAdapter | Where-Object { $_.Name -like "*Ethernet*" -and $_.Status -eq "Up" } | Select-Object -First 1
        
        if (-not $ethernetInterface) {
            Write-Host "✗ No active Ethernet interface found" -ForegroundColor Red
            return $false
        }
        
        Write-Host "Found interface: $($ethernetInterface.Name)" -ForegroundColor White
        
        # Set metric to 1 (highest priority)
        Set-NetIPInterface -InterfaceAlias $ethernetInterface.Name -InterfaceMetric 1
        
        Write-Host "✓ Ethernet metric set to 1 (highest priority)" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "✗ Failed to set metric: $_" -ForegroundColor Red
        return $false
    }
}

# Function to export routing table
function Export-RoutingTable {
    param([string]$outputFile = "routes.txt")
    
    Write-Host ""
    Write-Host "Exporting routing table to $outputFile..." -ForegroundColor Yellow
    
    try {
        route print | Out-File -FilePath $outputFile -Encoding UTF8
        Write-Host "✓ Routing table exported to $outputFile" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "✗ Failed to export routing table: $_" -ForegroundColor Red
        return $false
    }
}

# Function to check VPN interference
function Test-VPNInterference {
    Write-Host ""
    Write-Host "Checking for VPN interference..." -ForegroundColor Yellow
    
    $vpnInterfaces = Get-NetAdapter | Where-Object { 
        $_.InterfaceDescription -like "*VPN*" -or 
        $_.InterfaceDescription -like "*TAP*" -or
        $_.InterfaceDescription -like "*Proton*"
    }
    
    if ($vpnInterfaces) {
        Write-Host "⚠ VPN interfaces detected:" -ForegroundColor Yellow
        $vpnInterfaces | ForEach-Object {
            Write-Host "  - $($_.Name) ($($_.Status))" -ForegroundColor White
        }
        return $true
    } else {
        Write-Host "✓ No VPN interference detected" -ForegroundColor Green
        return $false
    }
}

# Main execution flow
Write-Host "Step 1: Initial network test..." -ForegroundColor Cyan
$initialTest = Test-NetworkPulse

if (-not $initialTest) {
    Write-Host ""
    Write-Host "Network connectivity failed. Applying fix..." -ForegroundColor Yellow
    
    # Apply the fix
    $fixApplied = Set-EthernetMetric
    
    if ($fixApplied) {
        Start-Sleep -Seconds 2
        Write-Host ""
        Write-Host "Step 2: Testing network after fix..." -ForegroundColor Cyan
        $postFixTest = Test-NetworkPulse
        
        if ($postFixTest) {
            Write-Host ""
            Write-Host "✓✓✓ SUCCESS! Network pulse confirmed - Ethernet reigns! ✓✓✓" -ForegroundColor Green
            Write-Host "Proceed to push/deploy phase." -ForegroundColor Green
            exit 0
        } else {
            Write-Host ""
            Write-Host "⚠ Network still failing after metric fix. Deeper investigation needed." -ForegroundColor Yellow
            Export-RoutingTable
            Test-VPNInterference
            
            Write-Host ""
            Write-Host "NEXT STEPS:" -ForegroundColor Yellow
            Write-Host "1. Review routes.txt for routing conflicts" -ForegroundColor White
            Write-Host "2. Try Option 3: Direct Ethernet plug" -ForegroundColor White
            Write-Host "3. If VPN detected, consider temporary disable: netsh advfirewall set allprofiles state off" -ForegroundColor White
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "✗ Failed to apply fix. Manual intervention required." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "✓✓✓ Network already operational! Neural pulse confirmed! ✓✓✓" -ForegroundColor Green
    Write-Host "Ethernet reigns - proceed to Git push and empire evolution." -ForegroundColor Green
    exit 0
}
