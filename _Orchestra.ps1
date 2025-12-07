# _Orchestra.ps1 - Sovereignty Architecture Orchestration Script
# Strategickhaos DAO LLC (EIN: 39-2923503)
# Lyra Node Control Plane

param(
    [string]$Action = "status",
    [switch]$Detailed,
    [switch]$NoColor
)

# Color definitions
$Colors = @{
    Reset = "`e[0m"
    Bold = "`e[1m"
    Red = "`e[31m"
    Green = "`e[32m"
    Yellow = "`e[33m"
    Blue = "`e[34m"
    Magenta = "`e[35m"
    Cyan = "`e[36m"
    White = "`e[37m"
}

function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White",
        [switch]$NoNewline
    )
    
    if ($NoColor) {
        if ($NoNewline) {
            Write-Host $Text -NoNewline
        } else {
            Write-Host $Text
        }
        return
    }
    
    $colorCode = $Colors[$Color]
    if ($NoNewline) {
        Write-Host "$colorCode$Text$($Colors.Reset)" -NoNewline
    } else {
        Write-Host "$colorCode$Text$($Colors.Reset)"
    }
}

function Show-Banner {
    $banner = @"

╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   🌌  LYRA NODE ONLINE - STRATEGICKHAOS DAO LLC                           ║
║       EIN: 39-2923503                                                     ║
║                                                                           ║
║   📡  Proof System Ready. Type: ._Orchestra.ps1 -Action help              ║
║   ⚡  Sovereign Loop Active — Empire Eternal                              ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

"@
    
    Write-ColorText $banner -Color Cyan
    
    # Calculate uptime and sovereign loop percentage
    $os = Get-CimInstance Win32_OperatingSystem
    $uptime = (Get-Date) - $os.LastBootUpTime
    $sovereignPercentage = [math]::Min(100, [math]::Round(($uptime.TotalHours * 0.5), 2))
    
    Write-ColorText "    System Uptime: " -Color Yellow -NoNewline
    Write-Host "$($uptime.Days)d $($uptime.Hours)h $($uptime.Minutes)m"
    
    Write-ColorText "    $sovereignPercentage% Sovereign Loop Active" -Color Green
    Write-Host ""
}

function Test-CommandExists {
    param([string]$Command)
    
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

function Get-DockerStatus {
    Write-ColorText "`n🐳 DOCKER STATUS" -Color Magenta
    Write-ColorText ("=" * 80) -Color Magenta
    
    if (-not (Test-CommandExists "docker")) {
        Write-ColorText "   ⚠️  Docker not installed or not in PATH" -Color Red
        return
    }
    
    try {
        $null = docker ps 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorText "   ✅ Docker Engine: RUNNING" -Color Green
            
            # Get container count
            $containerCount = (docker ps --format "{{.ID}}" | Measure-Object).Count
            $imageCount = (docker images --format "{{.ID}}" | Measure-Object).Count
            
            Write-Host "   📦 Containers Running: $containerCount"
            Write-Host "   📀 Images Available: $imageCount"
            
            if ($Detailed -and $containerCount -gt 0) {
                Write-ColorText "`n   Active Containers:" -Color Yellow
                docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | ForEach-Object {
                    Write-Host "   $_"
                }
            }
        }
    } catch {
        Write-ColorText "   ❌ Docker Engine: NOT RUNNING" -Color Red
        Write-Host "   💡 Start Docker Desktop to enable containers"
    }
}

function Get-KubernetesStatus {
    Write-ColorText "`n☸️  KUBERNETES STATUS" -Color Magenta
    Write-ColorText ("=" * 80) -Color Magenta
    
    if (-not (Test-CommandExists "kubectl")) {
        Write-ColorText "   ⚠️  kubectl not installed or not in PATH" -Color Red
        Write-Host "   💡 Install with: winget install Kubernetes.kubectl"
        return
    }
    
    try {
        # Get current context
        $context = kubectl config current-context 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorText "   ✅ Connected to: " -Color Green -NoNewline
            Write-Host $context
            
            # Get cluster info
            $nodes = kubectl get nodes --no-headers 2>$null
            if ($LASTEXITCODE -eq 0) {
                $nodeCount = ($nodes | Measure-Object).Count
                Write-Host "   🖥️  Nodes: $nodeCount"
                
                if ($Detailed) {
                    Write-ColorText "`n   Node Details:" -Color Yellow
                    kubectl get nodes -o wide | ForEach-Object {
                        Write-Host "   $_"
                    }
                }
                
                # Get pod count
                $pods = kubectl get pods --all-namespaces --no-headers 2>$null
                if ($LASTEXITCODE -eq 0) {
                    $podCount = ($pods | Measure-Object).Count
                    $runningPods = ($pods | Select-String "Running" | Measure-Object).Count
                    Write-Host "   🔷 Pods: $runningPods/$podCount running"
                    
                    if ($Detailed) {
                        Write-ColorText "`n   Pods by Namespace:" -Color Yellow
                        kubectl get pods --all-namespaces | Select-Object -First 20 | ForEach-Object {
                            Write-Host "   $_"
                        }
                    }
                }
            }
        } else {
            Write-ColorText "   ⚠️  Not connected to any cluster" -Color Yellow
            Write-Host "   💡 Connect with: gcloud container clusters get-credentials CLUSTER_NAME --region=REGION"
        }
    } catch {
        Write-ColorText "   ❌ Error querying Kubernetes: $_" -Color Red
    }
}

function Get-GCloudStatus {
    Write-ColorText "`n☁️  GOOGLE CLOUD STATUS" -Color Magenta
    Write-ColorText ("=" * 80) -Color Magenta
    
    if (-not (Test-CommandExists "gcloud")) {
        Write-ColorText "   ⚠️  gcloud not installed or not in PATH" -Color Red
        Write-Host "   💡 Install from: https://cloud.google.com/sdk/docs/install"
        return
    }
    
    try {
        $project = gcloud config get-value project 2>$null
        if ($LASTEXITCODE -eq 0 -and $project) {
            Write-ColorText "   ✅ Active Project: " -Color Green -NoNewline
            Write-Host $project
            
            $account = gcloud config get-value account 2>$null
            if ($account) {
                Write-Host "   👤 Account: $account"
            }
            
            # List GKE clusters if detailed
            if ($Detailed) {
                Write-ColorText "`n   GKE Clusters:" -Color Yellow
                $clusters = gcloud container clusters list --format="table(name,location,status)" 2>$null
                if ($LASTEXITCODE -eq 0) {
                    $clusters | ForEach-Object {
                        Write-Host "   $_"
                    }
                }
            }
        } else {
            Write-ColorText "   ⚠️  No active project configured" -Color Yellow
            Write-Host "   💡 Login with: gcloud auth login"
        }
    } catch {
        Write-ColorText "   ❌ Error querying gcloud: $_" -Color Red
    }
}

function Get-GitStatus {
    Write-ColorText "`n🐙 GIT STATUS" -Color Magenta
    Write-ColorText ("=" * 80) -Color Magenta
    
    if (-not (Test-CommandExists "git")) {
        Write-ColorText "   ⚠️  Git not installed or not in PATH" -Color Red
        return
    }
    
    try {
        # Check if we're in a git repository
        $gitRoot = git rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorText "   ✅ Repository: " -Color Green -NoNewline
            Write-Host (Split-Path -Leaf $gitRoot)
            
            # Get branch
            $branch = git branch --show-current 2>$null
            Write-Host "   🌿 Branch: $branch"
            
            # Get remote
            $remote = git remote get-url origin 2>$null
            if ($remote) {
                Write-Host "   🔗 Remote: $remote"
            }
            
            # Get status
            $status = git status --porcelain 2>$null
            if ($status) {
                $changes = ($status | Measure-Object).Count
                Write-ColorText "   ⚠️  $changes uncommitted changes" -Color Yellow
                
                if ($Detailed) {
                    Write-ColorText "`n   Changed Files:" -Color Yellow
                    git status --short | ForEach-Object {
                        Write-Host "   $_"
                    }
                }
            } else {
                Write-ColorText "   ✅ Working tree clean" -Color Green
            }
        } else {
            Write-ColorText "   ℹ️  Not in a git repository" -Color Blue
        }
    } catch {
        Write-ColorText "   ❌ Error querying git: $_" -Color Red
    }
}

function Get-SystemResources {
    Write-ColorText "`n💻 SYSTEM RESOURCES" -Color Magenta
    Write-ColorText ("=" * 80) -Color Magenta
    
    # CPU
    $cpu = Get-CimInstance Win32_Processor
    $cpuUsage = (Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1).CounterSamples.CookedValue
    Write-ColorText "   🔥 CPU: " -Color Cyan -NoNewline
    Write-Host "$([math]::Round($cpuUsage, 1))% ($($cpu.Name))"
    
    # Memory
    $os = Get-CimInstance Win32_OperatingSystem
    $totalRAM = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
    $freeRAM = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
    $usedRAM = $totalRAM - $freeRAM
    $ramPercent = [math]::Round(($usedRAM / $totalRAM) * 100, 1)
    Write-ColorText "   🧠 Memory: " -Color Cyan -NoNewline
    Write-Host "$ramPercent% ($usedRAM GB / $totalRAM GB)"
    
    # Disk
    $disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
    $diskTotal = [math]::Round($disk.Size / 1GB, 2)
    $diskFree = [math]::Round($disk.FreeSpace / 1GB, 2)
    $diskUsed = $diskTotal - $diskFree
    $diskPercent = [math]::Round(($diskUsed / $diskTotal) * 100, 1)
    Write-ColorText "   💾 Disk (C:): " -Color Cyan -NoNewline
    Write-Host "$diskPercent% ($diskUsed GB / $diskTotal GB)"
    
    # Network
    $network = Get-NetAdapter | Where-Object Status -eq "Up" | Select-Object -First 1
    if ($network) {
        Write-ColorText "   🌐 Network: " -Color Cyan -NoNewline
        Write-Host "$($network.Name) ($($network.LinkSpeed))"
    }
}

function Get-ProtonDriveStatus {
    Write-ColorText "`n🔐 PROTON DRIVE STATUS" -Color Magenta
    Write-ColorText ("=" * 80) -Color Magenta
    
    # Try multiple possible process names
    $protonProcess = Get-Process -Name "ProtonDrive","Proton Drive","protondrive" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($protonProcess) {
        Write-ColorText "   ✅ Proton Drive: RUNNING" -Color Green
        
        # Check for Lyra Node folder
        $lyraPath = Join-Path $env:USERPROFILE "Proton Drive\Lyra-Node"
        if (Test-Path $lyraPath) {
            Write-ColorText "   📁 Lyra Node folder: FOUND" -Color Green
            Write-Host "      Path: $lyraPath"
            
            if ($Detailed) {
                $folderSize = (Get-ChildItem -Path $lyraPath -Recurse -File -ErrorAction SilentlyContinue | 
                              Measure-Object -Property Length -Sum).Sum / 1MB
                Write-Host "      Size: $([math]::Round($folderSize, 2)) MB"
            }
        } else {
            Write-ColorText "   ⚠️  Lyra Node folder not found" -Color Yellow
            Write-Host "   💡 Create with: New-Item -Path '$lyraPath' -ItemType Directory"
        }
    } else {
        Write-ColorText "   ⚠️  Proton Drive not running" -Color Yellow
        Write-Host "   💡 Start Proton Drive to enable sync"
    }
}

function Invoke-QuickConnect {
    Write-ColorText "`n🔗 QUICK CONNECT TO GKE" -Color Magenta
    Write-ColorText ("=" * 80) -Color Magenta
    
    # Use environment variables or defaults
    $clusterName = if ($env:GKE_CLUSTER_NAME) { $env:GKE_CLUSTER_NAME } else { "jarvis-swarm-personal-001" }
    $clusterRegion = if ($env:GKE_REGION) { $env:GKE_REGION } else { "us-central1" }
    $gcpProject = if ($env:GCP_PROJECT_ID) { $env:GCP_PROJECT_ID } else { "jarvis-swarm-personal" }
    
    Write-Host ""
    Write-ColorText "   Connecting to $clusterName in $clusterRegion..." -Color Yellow
    
    try {
        gcloud container clusters get-credentials $clusterName `
            --region=$clusterRegion `
            --project=$gcpProject
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorText "   ✅ Connected successfully!" -Color Green
            Write-Host ""
            kubectl get nodes
        } else {
            Write-ColorText "   ❌ Connection failed" -Color Red
            Write-Host "   💡 Make sure you're authenticated with: gcloud auth login"
            Write-Host "   💡 Set custom values: `$env:GKE_CLUSTER_NAME='your-cluster'"
        }
    } catch {
        Write-ColorText "   ❌ Error: $_" -Color Red
    }
}

function Show-QuickCommands {
    Write-ColorText "`n⚡ QUICK COMMANDS" -Color Magenta
    Write-ColorText ("=" * 80) -Color Magenta
    
    $commands = @(
        @{ Cmd = "._Orchestra.ps1"; Desc = "Show full system status" }
        @{ Cmd = "._Orchestra.ps1 -Action status -Detailed"; Desc = "Detailed status report" }
        @{ Cmd = "._Orchestra.ps1 -Action connect"; Desc = "Connect to GKE cluster" }
        @{ Cmd = "._Orchestra.ps1 -Action docker"; Desc = "Docker-only status" }
        @{ Cmd = "._Orchestra.ps1 -Action k8s"; Desc = "Kubernetes-only status" }
        @{ Cmd = "kubectl get nodes"; Desc = "List cluster nodes" }
        @{ Cmd = "kubectl get pods -A"; Desc = "List all pods" }
        @{ Cmd = "docker ps"; Desc = "List running containers" }
        @{ Cmd = "gcloud projects list"; Desc = "List GCP projects" }
    )
    
    Write-Host ""
    foreach ($cmd in $commands) {
        Write-ColorText "   $($cmd.Cmd)" -Color Cyan
        Write-Host "      → $($cmd.Desc)"
        Write-Host ""
    }
}

function Show-Help {
    Show-Banner
    
    Write-ColorText "USAGE:" -Color Yellow
    Write-Host "   ._Orchestra.ps1 [-Action <action>] [-Detailed] [-NoColor]"
    Write-Host ""
    
    Write-ColorText "ACTIONS:" -Color Yellow
    Write-Host "   status    - Show complete system status (default)"
    Write-Host "   connect   - Connect to GKE cluster"
    Write-Host "   docker    - Show Docker status only"
    Write-Host "   k8s       - Show Kubernetes status only"
    Write-Host "   gcloud    - Show Google Cloud status only"
    Write-Host "   resources - Show system resources only"
    Write-Host "   help      - Show this help message"
    Write-Host ""
    
    Write-ColorText "OPTIONS:" -Color Yellow
    Write-Host "   -Detailed - Show detailed information"
    Write-Host "   -NoColor  - Disable colored output"
    Write-Host ""
    
    Write-ColorText "EXAMPLES:" -Color Yellow
    Write-Host "   ._Orchestra.ps1"
    Write-Host "   ._Orchestra.ps1 -Action status -Detailed"
    Write-Host "   ._Orchestra.ps1 -Action connect"
    Write-Host "   ._Orchestra.ps1 -Action docker -Detailed"
    Write-Host ""
}

# Main execution
function Main {
    switch ($Action.ToLower()) {
        "status" {
            Show-Banner
            Get-SystemResources
            Get-ProtonDriveStatus
            Get-DockerStatus
            Get-KubernetesStatus
            Get-GCloudStatus
            Get-GitStatus
            Show-QuickCommands
        }
        "connect" {
            Show-Banner
            Invoke-QuickConnect
        }
        "docker" {
            Show-Banner
            Get-DockerStatus
        }
        "k8s" {
            Show-Banner
            Get-KubernetesStatus
        }
        "gcloud" {
            Show-Banner
            Get-GCloudStatus
        }
        "resources" {
            Show-Banner
            Get-SystemResources
        }
        "help" {
            Show-Help
        }
        default {
            Show-Help
        }
    }
    
    Write-Host ""
    Write-ColorText "═" * 80 -Color Cyan
    Write-ColorText "🔥 EMPIRE ETERNAL 🔥" -Color Magenta
    Write-ColorText "═" * 80 -Color Cyan
    Write-Host ""
}

# Run main function
Main
