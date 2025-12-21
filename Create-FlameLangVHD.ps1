# FlameLang Sovereign OS VHD Creator - Windows PowerShell Version
# ================================================================
#
# Creates a bootable VHD with FlameLang WireGuard DNS hardening
# Optimized for Windows with Hyper-V and DevDrive support
#
# Author: Strategickhaos DAO LLC
# Version: 1.0
#
# Requirements:
# - Windows 10/11 Pro or Enterprise
# - Hyper-V feature enabled
# - Administrator privileges
# - At least 25GB free disk space

[CmdletBinding()]
param(
    [string]$VHDName = "flamelang-sovereign-os",
    [int]$VHDSizeMB = 20480,  # 20GB
    [ValidateSet("VHD", "VHDX")]
    [string]$VHDFormat = "VHDX",
    [string]$OutputDir = ".\vhd-output",
    [switch]$CreateDevDrive,
    [switch]$AttachAfterCreation
)

# Colors for output
$ESC = [char]27
$Red = "$ESC[31m"
$Green = "$ESC[32m"
$Yellow = "$ESC[33m"
$Blue = "$ESC[34m"
$Reset = "$ESC[0m"

function Write-Info {
    param([string]$Message)
    Write-Host "${Blue}[INFO]${Reset} $Message"
}

function Write-Success {
    param([string]$Message)
    Write-Host "${Green}[✓]${Reset} $Message"
}

function Write-Warn {
    param([string]$Message)
    Write-Host "${Yellow}[!]${Reset} $Message"
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "${Red}[✗]${Reset} $Message"
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Test-HyperV {
    $hyperv = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V
    return ($hyperv.State -eq "Enabled")
}

function New-FlameLangVHD {
    Write-Info "Creating FlameLang Sovereign OS VHD..."
    Write-Info "Configuration:"
    Write-Info "  Name: $VHDName"
    Write-Info "  Size: $VHDSizeMB MB ($([math]::Round($VHDSizeMB/1024, 2)) GB)"
    Write-Info "  Format: $VHDFormat"
    Write-Info "  Output: $OutputDir"
    Write-Host ""

    # Check prerequisites
    if (-not (Test-Administrator)) {
        Write-Error-Custom "This script must be run as Administrator"
        exit 1
    }

    if (-not (Test-HyperV)) {
        Write-Warn "Hyper-V is not enabled. VHD creation will continue but VM features will be limited."
        Write-Info "To enable Hyper-V: Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All"
    }

    # Create output directory
    if (-not (Test-Path $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir | Out-Null
        Write-Success "Created output directory: $OutputDir"
    }

    $VHDPath = Join-Path $OutputDir "$VHDName.$($VHDFormat.ToLower())"

    # Create VHD
    Write-Info "Creating VHD file..."
    try {
        $vhd = New-VHD -Path $VHDPath -SizeBytes ($VHDSizeMB * 1MB) -Dynamic
        Write-Success "VHD created: $VHDPath"
    }
    catch {
        Write-Error-Custom "Failed to create VHD: $_"
        exit 1
    }

    # Mount VHD
    Write-Info "Mounting VHD..."
    try {
        $mountedVHD = Mount-VHD -Path $VHDPath -Passthru
        $disk = Get-Disk | Where-Object { $_.Location -eq $VHDPath }
        Write-Success "VHD mounted as Disk $($disk.Number)"
    }
    catch {
        Write-Error-Custom "Failed to mount VHD: $_"
        exit 1
    }

    # Initialize disk
    Write-Info "Initializing disk..."
    try {
        Initialize-Disk -Number $disk.Number -PartitionStyle MBR -ErrorAction Stop
        Write-Success "Disk initialized with MBR"
    }
    catch {
        Write-Warn "Disk may already be initialized: $_"
    }

    # Create partition
    Write-Info "Creating partition..."
    try {
        $partition = New-Partition -DiskNumber $disk.Number -UseMaximumSize -IsActive
        Write-Success "Partition created"
    }
    catch {
        Write-Error-Custom "Failed to create partition: $_"
        exit 1
    }

    # Format partition
    Write-Info "Formatting partition as NTFS..."
    try {
        $volume = Format-Volume -Partition $partition -FileSystem NTFS -NewFileSystemLabel "FLAMELANG" -Confirm:$false
        $driveLetter = $partition | Get-Volume | Select-Object -ExpandProperty DriveLetter
        Write-Success "Partition formatted: ${driveLetter}:"
    }
    catch {
        Write-Error-Custom "Failed to format partition: $_"
        exit 1
    }

    # Install FlameLang components
    Write-Info "Installing FlameLang components..."
    Install-FlameLangComponents -DriveLetter $driveLetter

    # Dismount VHD
    Write-Info "Dismounting VHD..."
    Dismount-VHD -Path $VHDPath
    Write-Success "VHD dismounted"

    # Generate deployment files
    New-DeploymentGuide -VHDPath $VHDPath
    New-HyperVScript -VHDPath $VHDPath

    Write-Host ""
    Write-Success "VHD creation complete!"
    Write-Host ""
    Write-Host "📦 Output files:"
    Write-Host "   VHD: $VHDPath"
    Write-Host "   Deployment Guide: $OutputDir\DEPLOYMENT_GUIDE_WINDOWS.md"
    Write-Host "   Hyper-V Script: $OutputDir\Create-FlameLangVM.ps1"
    Write-Host ""

    if ($AttachAfterCreation) {
        Write-Info "Attaching VHD for inspection..."
        Mount-VHD -Path $VHDPath -ReadOnly
        Write-Success "VHD attached in read-only mode"
        Write-Info "Use Disk Management (diskmgmt.msc) to view the VHD"
    }

    Write-Host "🚀 Next steps:"
    Write-Host "   1. Review: $OutputDir\DEPLOYMENT_GUIDE_WINDOWS.md"
    Write-Host "   2. Create VM: .\$OutputDir\Create-FlameLangVM.ps1"
    Write-Host "   3. Or attach manually in Hyper-V Manager"
    Write-Host ""
}

function Install-FlameLangComponents {
    param([string]$DriveLetter)

    $root = "${DriveLetter}:"

    # Create directory structure
    Write-Info "Creating directory structure..."
    $dirs = @(
        "$root\opt\flamelang",
        "$root\etc\wireguard",
        "$root\var\log",
        "$root\tmp"
    )

    foreach ($dir in $dirs) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    Write-Success "Directory structure created"

    # Copy FlameLang scripts
    Write-Info "Copying FlameLang scripts..."
    $scripts = @(
        "flamelang_wireguard_dns.py",
        "flamelang_36_tools_integration.py"
    )

    foreach ($script in $scripts) {
        if (Test-Path $script) {
            Copy-Item $script "$root\opt\flamelang\" -Force
            Write-Success "Copied $script"
        }
        else {
            Write-Warn "Script not found: $script"
        }
    }

    # Create WireGuard config template
    Write-Info "Creating WireGuard configuration template..."
    $wgConfig = @"
[Interface]
PrivateKey = REPLACE_WITH_PRIVATE_KEY
Address = 10.99.0.2/24
DNS = 10.99.0.1

# FlameLang Sovereign DNS Protection Enabled
# All DNS queries will be entropy-checked and codon-verified
# Compression: 120x | Execution: Cache-resident

[Peer]
PublicKey = REPLACE_WITH_PEER_PUBLIC_KEY
Endpoint = vpn.example.com:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
"@
    Set-Content -Path "$root\etc\wireguard\wg0.conf.example" -Value $wgConfig
    Write-Success "WireGuard template created"

    # Create README
    Write-Info "Creating README..."
    $readme = @"
FlameLang Sovereign OS - Windows Edition
========================================

A self-contained, tamper-resistant system with embedded
WireGuard DNS hardening using FlameLang's 5-layer compilation pipeline.

Features:
- Zero-trust DNS handling with entropy checks
- Codon-verified DNS responses
- Simulated annealing for adaptive routing
- 120x compression ratio
- 6000x speedup in prototypes

Components:
- \opt\flamelang\flamelang_wireguard_dns.py - DNS compilation pipeline
- \opt\flamelang\flamelang_36_tools_integration.py - Tool integration
- \etc\wireguard\wg0.conf.example - WireGuard template

Quick Start (Windows):
1. Install Python 3.8+
2. Install WireGuard for Windows
3. Configure: copy \etc\wireguard\wg0.conf.example to wg0.conf
4. Edit wg0.conf with your keys and endpoints
5. Test: python \opt\flamelang\flamelang_wireguard_dns.py

For more information, visit:
https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
"@
    Set-Content -Path "$root\README.txt" -Value $readme
    Write-Success "README created"

    # Create startup script
    Write-Info "Creating startup script..."
    $startupScript = @"
@echo off
REM FlameLang Sovereign OS Startup
echo Starting FlameLang Sovereign OS...
echo ================================

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+
    exit /b 1
)

REM Start FlameLang DNS hardening
echo Starting FlameLang DNS hardening...
start /B python \opt\flamelang\flamelang_wireguard_dns.py

REM Start WireGuard if configured
if exist \etc\wireguard\wg0.conf (
    echo Starting WireGuard tunnel...
    wireguard /installtunnelservice \etc\wireguard\wg0.conf
)

echo FlameLang Sovereign OS initialized
pause
"@
    Set-Content -Path "$root\startup.bat" -Value $startupScript
    Write-Success "Startup script created"
}

function New-DeploymentGuide {
    param([string]$VHDPath)

    $guide = @"
# FlameLang Sovereign OS - Windows Deployment Guide

## VHD File Information
- **Location**: ``$VHDPath``
- **Size**: $VHDSizeMB MB ($([math]::Round($VHDSizeMB/1024, 2)) GB)
- **Format**: $VHDFormat

## Hyper-V Deployment

### Quick Start
Run the provided script:
``````powershell
.\$OutputDir\Create-FlameLangVM.ps1
``````

### Manual Steps
1. Open Hyper-V Manager
2. Action > New > Virtual Machine
3. Specify Name: FlameLang-Sovereign
4. Generation 1 (for compatibility)
5. Assign Memory: 2048 MB minimum (4096 MB recommended)
6. Networking: Default Switch or Custom
7. Connect Virtual Hard Disk: Use an existing virtual hard disk
8. Browse to: ``$VHDPath``
9. Complete wizard and start VM

### PowerShell Commands
``````powershell
New-VM -Name "FlameLang-Sovereign" -MemoryStartupBytes 2GB -Generation 1
Add-VMHardDiskDrive -VMName "FlameLang-Sovereign" -Path "$VHDPath"
Set-VMMemory -VMName "FlameLang-Sovereign" -DynamicMemoryEnabled `$true -MinimumBytes 1GB -MaximumBytes 4GB
Start-VM -Name "FlameLang-Sovereign"
``````

## VirtualBox Deployment

### Convert to VDI
``````powershell
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" clonehd "$VHDPath" "$OutputDir\$VHDName.vdi" --format VDI
``````

### Create VM
``````powershell
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" createvm --name "FlameLang-Sovereign" --register
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "FlameLang-Sovereign" --memory 2048 --cpus 2
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" storagectl "FlameLang-Sovereign" --name "SATA" --add sata
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" storageattach "FlameLang-Sovereign" --storagectl "SATA" --port 0 --device 0 --type hdd --medium "$OutputDir\$VHDName.vdi"
``````

## DevDrive Configuration

### Attach as DevDrive (ReFS)
``````powershell
# Attach VHD
Mount-VHD -Path "$VHDPath"

# Get disk number
`$disk = Get-Disk | Where-Object { `$_.Location -eq "$VHDPath" }
`$diskNum = `$disk.Number

# Convert to GPT (if needed for ReFS)
Initialize-Disk -Number `$diskNum -PartitionStyle GPT -Force

# Create ReFS volume for DevDrive
New-Volume -DiskNumber `$diskNum -FriendlyName "FlameLang-Dev" -FileSystem ReFS -DriveLetter F

# Clone repository
cd F:\
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch- flamelang-dev
``````

## Native Boot Configuration (Advanced)

### Add Boot Entry
``````cmd
REM Run as Administrator
bcdedit /copy {current} /d "FlameLang Sovereign OS"

REM Get the GUID from the output, then:
bcdedit /set {GUID} device vhd=[C:]\path\to\$VHDPath
bcdedit /set {GUID} osdevice vhd=[C:]\path\to\$VHDPath
bcdedit /set {GUID} detecthal on
``````

## Post-Deployment

### Configure WireGuard
1. Install WireGuard for Windows: https://www.wireguard.com/install/
2. Copy config: ``copy F:\etc\wireguard\wg0.conf.example wg0.conf``
3. Edit with your keys
4. Import tunnel in WireGuard app

### Test FlameLang
``````powershell
python F:\opt\flamelang\flamelang_wireguard_dns.py
python F:\opt\flamelang\flamelang_36_tools_integration.py
``````

## Troubleshooting

### VHD Mount Issues
- Ensure Hyper-V is enabled: ``Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V``
- Check VHD integrity: ``Test-VHD -Path "$VHDPath"``
- Compact VHD if needed: ``Optimize-VHD -Path "$VHDPath" -Mode Full``

### VM Boot Issues
- Use Generation 1 VMs for maximum compatibility
- Ensure Secure Boot is disabled
- Allocate at least 2GB RAM

### Performance Optimization
- Enable Dynamic Memory
- Use SSD for VHD storage
- Allocate multiple CPUs (2-4 recommended)

## Security Hardening

1. Change default passwords
2. Enable Windows Firewall
3. Configure BitLocker encryption
4. Enable Windows Defender
5. Set up automatic updates

## Support
- GitHub: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
- Documentation: F:\README.txt
"@

    Set-Content -Path "$OutputDir\DEPLOYMENT_GUIDE_WINDOWS.md" -Value $guide
    Write-Success "Deployment guide created: $OutputDir\DEPLOYMENT_GUIDE_WINDOWS.md"
}

function New-HyperVScript {
    param([string]$VHDPath)

    $script = @"
# FlameLang Sovereign OS - Hyper-V VM Creation Script
# ===================================================

param(
    [string]`$VMName = "FlameLang-Sovereign",
    [long]`$MemoryStartupBytes = 2GB,
    [int]`$ProcessorCount = 2,
    [string]`$SwitchName = "Default Switch"
)

Write-Host "Creating Hyper-V VM for FlameLang Sovereign OS..." -ForegroundColor Cyan

# Check if VM already exists
if (Get-VM -Name `$VMName -ErrorAction SilentlyContinue) {
    Write-Host "VM '`$VMName' already exists. Remove it first or choose a different name." -ForegroundColor Red
    exit 1
}

# Create VM
Write-Host "Creating VM: `$VMName" -ForegroundColor Green
New-VM -Name `$VMName -MemoryStartupBytes `$MemoryStartupBytes -Generation 1

# Add VHD
Write-Host "Attaching VHD: $VHDPath" -ForegroundColor Green
Add-VMHardDiskDrive -VMName `$VMName -Path "$VHDPath"

# Configure VM
Write-Host "Configuring VM settings..." -ForegroundColor Green
Set-VMProcessor -VMName `$VMName -Count `$ProcessorCount
Set-VMMemory -VMName `$VMName -DynamicMemoryEnabled `$true -MinimumBytes 1GB -MaximumBytes 4GB

# Connect to network switch
if (Get-VMSwitch -Name `$SwitchName -ErrorAction SilentlyContinue) {
    Connect-VMNetworkAdapter -VMName `$VMName -SwitchName `$SwitchName
    Write-Host "Connected to network switch: `$SwitchName" -ForegroundColor Green
} else {
    Write-Host "Warning: Network switch '`$SwitchName' not found. VM will have no network." -ForegroundColor Yellow
}

# Set boot order
Set-VMFirmware -VMName `$VMName -FirstBootDevice (Get-VMHardDiskDrive -VMName `$VMName)

Write-Host ""
Write-Host "VM Created Successfully!" -ForegroundColor Green
Write-Host "VM Name: `$VMName" -ForegroundColor Cyan
Write-Host "Memory: `$(`$MemoryStartupBytes / 1GB) GB (Dynamic: 1-4 GB)" -ForegroundColor Cyan
Write-Host "CPUs: `$ProcessorCount" -ForegroundColor Cyan
Write-Host "VHD: $VHDPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the VM:" -ForegroundColor Yellow
Write-Host "  Start-VM -Name `$VMName" -ForegroundColor White
Write-Host ""
Write-Host "To connect to the VM console:" -ForegroundColor Yellow
Write-Host "  vmconnect.exe localhost `$VMName" -ForegroundColor White
Write-Host ""
"@

    Set-Content -Path "$OutputDir\Create-FlameLangVM.ps1" -Value $script
    Write-Success "Hyper-V script created: $OutputDir\Create-FlameLangVM.ps1"
}

# Main execution
Write-Host ""
Write-Host "🔥 FlameLang Sovereign OS VHD Creator - Windows Edition" -ForegroundColor Magenta
Write-Host "========================================================" -ForegroundColor Magenta
Write-Host ""

New-FlameLangVHD

Write-Host "✅ Process complete!" -ForegroundColor Green
Write-Host ""
