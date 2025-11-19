###############################################################################
# Department of Living Memory (DoLM) - Activation Script (PowerShell)
# "Nothing is ever lost. Every error is a lesson. Every TODO is a prophecy."
###############################################################################

param(
    [string]$VaultPath = "$HOME\strategic-khaos-private\dolm-vault",
    [string]$WatchPath = "C:\Users\garza\Chaos God DOM_010101",
    [string]$ContainerName = "dolm-daemon",
    [string]$ImageName = "ghcr.io/strategickhaos/dolm-daemon:latest",
    [string]$LocalImageName = "dolm-daemon:local"
)

$ErrorActionPreference = "Stop"

# ASCII Art Banner
Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   DEPARTMENT OF LIVING MEMORY (DoLM)                          ║
║                                                               ║
║   "Nothing is ever lost. Every error is a lesson.             ║
║    Every TODO is a prophecy."                                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Magenta

# Check Docker availability
Write-Host "[1/5] Checking Docker installation..." -ForegroundColor Cyan
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
    exit 1
}

# Check if Docker daemon is running
try {
    docker info | Out-Null
    Write-Host "✓ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker daemon is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again" -ForegroundColor Yellow
    exit 1
}

# Initialize vault
Write-Host "[2/5] Initializing DoLM vault..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $VaultPath | Out-Null
Write-Host "✓ Vault directory created: $VaultPath" -ForegroundColor Green

# Build or pull image
Write-Host "[3/5] Preparing DoLM daemon container..." -ForegroundColor Cyan
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$dockerfilePath = Join-Path $scriptDir "Dockerfile"

if (Test-Path $dockerfilePath) {
    Write-Host "Building local DoLM image..." -ForegroundColor Yellow
    docker build -t $LocalImageName $scriptDir
    $imageToUse = $LocalImageName
    Write-Host "✓ Built local DoLM image" -ForegroundColor Green
} else {
    Write-Host "! Dockerfile not found, will try to pull from registry" -ForegroundColor Yellow
    $imageToUse = $ImageName
}

# Stop existing container
Write-Host "[4/5] Stopping existing DoLM daemon (if any)..." -ForegroundColor Cyan
try {
    $existingContainer = docker ps -a --format "{{.Names}}" | Where-Object { $_ -eq $ContainerName }
    if ($existingContainer) {
        docker stop $ContainerName 2>$null | Out-Null
        docker rm $ContainerName 2>$null | Out-Null
        Write-Host "✓ Cleaned up existing container" -ForegroundColor Green
    } else {
        Write-Host "! No existing container found" -ForegroundColor Yellow
    }
} catch {
    Write-Host "! Could not clean up existing container" -ForegroundColor Yellow
}

# Start new container
Write-Host "[5/5] Starting DoLM daemon..." -ForegroundColor Cyan

# Convert Windows paths for Docker
$dockerWatchPath = $WatchPath -replace '\\', '/' -replace '^([A-Za-z]):', '//$1'
$dockerVaultPath = $VaultPath -replace '\\', '/' -replace '^([A-Za-z]):', '//$1'

docker run -d `
    --name $ContainerName `
    --restart unless-stopped `
    -v "${WatchPath}:/swarm:ro" `
    -v "${VaultPath}:/vault" `
    -e DOLM_WATCH_PATH=/swarm `
    -e DOLM_VAULT_PATH=/vault `
    $imageToUse

Write-Host "✓ DoLM daemon started" -ForegroundColor Green

# Verify installation
Start-Sleep -Seconds 2
$runningContainer = docker ps --format "{{.Names}}" | Where-Object { $_ -eq $ContainerName }

if ($runningContainer) {
    Write-Host @"

════════════════════════════════════════════════════════════
Department of Living Memory is now ONLINE
════════════════════════════════════════════════════════════

"@ -ForegroundColor Blue

    Write-Host "Vault location: " -NoNewline -ForegroundColor Cyan
    Write-Host $VaultPath
    Write-Host "Watching: " -NoNewline -ForegroundColor Cyan
    Write-Host $WatchPath
    
    Write-Host @"

Next steps:
  1. Download Obsidian: https://obsidian.md/download
  2. Open the vault in Obsidian: File → Open vault → $VaultPath
  3. Watch as DoLM discovers TODOs and errors in your code
  4. Explore the GraphView to see connections

Useful commands:
  • View logs:    docker logs -f $ContainerName
  • Stop daemon:  docker stop $ContainerName
  • Restart:      docker restart $ContainerName

"@ -ForegroundColor Yellow

    Write-Host "Every error, every TODO, every breath you take in the terminal" -ForegroundColor Magenta
    Write-Host "is now eternal, beautiful, and linked in Obsidian GraphView." -ForegroundColor Magenta
    Write-Host ""
    Write-Host "The department is live. The vault is breathing." -ForegroundColor Green
    Write-Host "Your legacy is now unkillable." -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "✗ DoLM daemon failed to start" -ForegroundColor Red
    Write-Host "Check logs with: docker logs $ContainerName" -ForegroundColor Yellow
    exit 1
}
