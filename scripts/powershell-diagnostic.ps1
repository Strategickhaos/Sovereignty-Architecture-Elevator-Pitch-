# powershell-diagnostic.ps1
# Windows PowerShell Diagnostic Tool for Strategic Khaos
# Collects system information and identifies configuration issues

<#
.SYNOPSIS
    Comprehensive diagnostic tool for Windows PowerShell environments

.DESCRIPTION
    Collects information about:
    - PowerShell profile status and syntax
    - Network configuration
    - Docker and development tools
    - Active connections
    - System resources
    - Git configuration
    - Environment variables

.PARAMETER SendToDiscord
    Send diagnostic results to Discord webhook

.PARAMETER Detailed
    Include detailed network and process information

.EXAMPLE
    .\powershell-diagnostic.ps1
    
.EXAMPLE
    .\powershell-diagnostic.ps1 -SendToDiscord -Detailed
#>

param(
    [switch]$SendToDiscord,
    [switch]$Detailed
)

# Color output
function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-ColorText "═══════════════════════════════════════════════════════" -Color Cyan
    Write-ColorText " $Title" -Color Cyan
    Write-ColorText "═══════════════════════════════════════════════════════" -Color Cyan
    Write-Host ""
}

# Banner
Write-Host ""
Write-ColorText "╔════════════════════════════════════════════════════════╗" -Color Magenta
Write-ColorText "║   Strategic Khaos Windows Diagnostic Tool             ║" -Color Magenta
Write-ColorText "║   Nitro V15 Lyra Node Health Check                    ║" -Color Magenta
Write-ColorText "╚════════════════════════════════════════════════════════╝" -Color Magenta
Write-Host ""

$diagnosticResults = @{
    timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    hostname = $env:COMPUTERNAME
    username = "$env:USERDOMAIN\$env:USERNAME"
    checks = @{}
    issues = @()
    recommendations = @()
}

# 1. System Information
Write-Section "System Information"

$osInfo = Get-CimInstance Win32_OperatingSystem
$computerInfo = Get-CimInstance Win32_ComputerSystem

Write-ColorText "OS: " -Color Gray
Write-Host "  $($osInfo.Caption) ($($osInfo.Version))"
Write-ColorText "Hostname: " -Color Gray
Write-Host "  $($computerInfo.Name)"
Write-ColorText "Username: " -Color Gray
Write-Host "  $env:USERDOMAIN\$env:USERNAME"
Write-ColorText "RAM: " -Color Gray
Write-Host "  $([math]::Round($computerInfo.TotalPhysicalMemory / 1GB, 2)) GB"
Write-ColorText "PowerShell Version: " -Color Gray
Write-Host "  $($PSVersionTable.PSVersion.ToString())"

$diagnosticResults.checks.system = @{
    os = $osInfo.Caption
    hostname = $computerInfo.Name
    ram_gb = [math]::Round($computerInfo.TotalPhysicalMemory / 1GB, 2)
    powershell_version = $PSVersionTable.PSVersion.ToString()
    status = "ok"
}

# 2. PowerShell Profile Check
Write-Section "PowerShell Profile Status"

$profileCheck = @{
    exists = Test-Path $PROFILE
    path = $PROFILE
    size = 0
    syntax_valid = $false
    functions_count = 0
}

if (Test-Path $PROFILE) {
    Write-ColorText "✅ Profile exists: " -Color Green
    Write-Host "  $PROFILE"
    
    $profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
    $profileCheck.size = $profileContent.Length
    
    Write-ColorText "Size: " -Color Gray
    Write-Host "  $($profileContent.Length) characters"
    
    # Check syntax
    try {
        $null = [scriptblock]::Create($profileContent)
        Write-ColorText "✅ Syntax: " -Color Green
        Write-Host "  Valid"
        $profileCheck.syntax_valid = $true
    } catch {
        Write-ColorText "❌ Syntax: " -Color Red
        Write-Host "  Invalid - $($_.Exception.Message)"
        $profileCheck.syntax_valid = $false
        $diagnosticResults.issues += "PowerShell profile has syntax errors: $($_.Exception.Message)"
        $diagnosticResults.recommendations += "Run: .\scripts\fix-powershell-profile.ps1"
    }
    
    # Count functions
    $functionMatches = [regex]::Matches($profileContent, 'function\s+(\w+)')
    $profileCheck.functions_count = $functionMatches.Count
    
    if ($functionMatches.Count -gt 0) {
        Write-ColorText "Functions defined: " -Color Gray
        Write-Host "  $($functionMatches.Count)"
        foreach ($match in $functionMatches) {
            Write-Host "    - $($match.Groups[1].Value)"
        }
    }
} else {
    Write-ColorText "⚠️  Profile does not exist: " -Color Yellow
    Write-Host "  $PROFILE"
    $diagnosticResults.recommendations += "Create PowerShell profile with custom functions"
}

$diagnosticResults.checks.profile = $profileCheck

# 3. Development Tools
Write-Section "Development Tools"

$tools = @(
    @{ Name = "Git"; Command = "git"; VersionArg = "--version" },
    @{ Name = "Docker"; Command = "docker"; VersionArg = "--version" },
    @{ Name = "Node.js"; Command = "node"; VersionArg = "--version" },
    @{ Name = "npm"; Command = "npm"; VersionArg = "--version" },
    @{ Name = "Python"; Command = "python"; VersionArg = "--version" },
    @{ Name = "WSL"; Command = "wsl"; VersionArg = "--version" }
)

$toolsStatus = @{}

foreach ($tool in $tools) {
    $installed = Get-Command $tool.Command -ErrorAction SilentlyContinue
    
    if ($installed) {
        try {
            $version = & $tool.Command $tool.VersionArg 2>&1 | Select-Object -First 1
            Write-ColorText "✅ $($tool.Name): " -Color Green
            Write-Host "  $version"
            $toolsStatus[$tool.Name] = @{ installed = $true; version = $version }
        } catch {
            Write-ColorText "✅ $($tool.Name): " -Color Green
            Write-Host "  Installed (version check failed)"
            $toolsStatus[$tool.Name] = @{ installed = $true; version = "unknown" }
        }
    } else {
        Write-ColorText "❌ $($tool.Name): " -Color Red
        Write-Host "  Not found"
        $toolsStatus[$tool.Name] = @{ installed = $false }
        $diagnosticResults.recommendations += "Install $($tool.Name)"
    }
}

$diagnosticResults.checks.tools = $toolsStatus

# 4. Docker Status
Write-Section "Docker Status"

if (Get-Command docker -ErrorAction SilentlyContinue) {
    try {
        $dockerInfo = docker info 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorText "✅ Docker: " -Color Green
            Write-Host "  Running"
            
            # Count running containers
            $containers = docker ps --format "{{.Names}}" 2>&1
            if ($LASTEXITCODE -eq 0) {
                $containerCount = ($containers | Measure-Object).Count
                Write-ColorText "Containers: " -Color Gray
                Write-Host "  $containerCount running"
                
                if ($Detailed -and $containerCount -gt 0) {
                    foreach ($container in $containers) {
                        Write-Host "    - $container"
                    }
                }
            }
            
            $diagnosticResults.checks.docker = @{ running = $true; containers = $containerCount }
        } else {
            Write-ColorText "⚠️  Docker: " -Color Yellow
            Write-Host "  Not running"
            $diagnosticResults.issues += "Docker is installed but not running"
            $diagnosticResults.recommendations += "Start Docker Desktop"
            $diagnosticResults.checks.docker = @{ running = $false }
        }
    } catch {
        Write-ColorText "❌ Docker: " -Color Red
        Write-Host "  Error checking status"
        $diagnosticResults.checks.docker = @{ running = $false; error = $_.Exception.Message }
    }
}

# 5. Network Configuration
Write-Section "Network Configuration"

$netAdapter = Get-NetAdapter | Where-Object { $_.Status -eq "Up" } | Select-Object -First 1
if ($netAdapter) {
    $ipConfig = Get-NetIPAddress -InterfaceIndex $netAdapter.ifIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue
    
    Write-ColorText "Primary Interface: " -Color Gray
    Write-Host "  $($netAdapter.Name) ($($netAdapter.InterfaceDescription))"
    
    if ($ipConfig) {
        Write-ColorText "IP Address: " -Color Gray
        Write-Host "  $($ipConfig.IPAddress)"
        
        $diagnosticResults.checks.network = @{
            interface = $netAdapter.Name
            ip_address = $ipConfig.IPAddress
            status = "connected"
        }
    }
}

# Check connectivity to key services
$connectivityTests = @(
    @{ Name = "GitHub"; Host = "github.com"; Port = 443 },
    @{ Name = "Docker Hub"; Host = "hub.docker.com"; Port = 443 },
    @{ Name = "npm Registry"; Host = "registry.npmjs.org"; Port = 443 }
)

Write-Host ""
Write-ColorText "Connectivity Tests:" -Color Gray

foreach ($test in $connectivityTests) {
    try {
        $result = Test-NetConnection -ComputerName $test.Host -Port $test.Port -InformationLevel Quiet -WarningAction SilentlyContinue
        if ($result) {
            Write-ColorText "  ✅ $($test.Name): " -Color Green
            Write-Host "Reachable"
        } else {
            Write-ColorText "  ❌ $($test.Name): " -Color Red
            Write-Host "Unreachable"
            $diagnosticResults.issues += "$($test.Name) is unreachable"
        }
    } catch {
        Write-ColorText "  ⚠️  $($test.Name): " -Color Yellow
        Write-Host "Test failed"
    }
}

# 6. Git Configuration
Write-Section "Git Configuration"

if (Get-Command git -ErrorAction SilentlyContinue) {
    $gitUser = git config --global user.name 2>&1
    $gitEmail = git config --global user.email 2>&1
    
    if ($gitUser -and $LASTEXITCODE -eq 0) {
        Write-ColorText "User: " -Color Gray
        Write-Host "  $gitUser"
    } else {
        Write-ColorText "⚠️  Git user.name not configured" -Color Yellow
        $diagnosticResults.recommendations += "Set Git user: git config --global user.name 'Your Name'"
    }
    
    if ($gitEmail -and $LASTEXITCODE -eq 0) {
        Write-ColorText "Email: " -Color Gray
        Write-Host "  $gitEmail"
    } else {
        Write-ColorText "⚠️  Git user.email not configured" -Color Yellow
        $diagnosticResults.recommendations += "Set Git email: git config --global user.email 'your@email.com'"
    }
    
    $diagnosticResults.checks.git = @{
        user = $gitUser
        email = $gitEmail
    }
}

# 7. Environment Variables
Write-Section "Strategic Khaos Environment Variables"

$strategicKhaosVars = @(
    "DISCORD_TOKEN",
    "DISCORD_WEBHOOK_URL",
    "GITHUB_TOKEN",
    "OPENAI_API_KEY",
    "XAI_API_KEY"
)

$envVarsStatus = @{}
$missingVars = @()

foreach ($varName in $strategicKhaosVars) {
    $value = [Environment]::GetEnvironmentVariable($varName)
    if ($value) {
        Write-ColorText "✅ $varName: " -Color Green
        Write-Host "  Set (${value.Substring(0, [Math]::Min(8, $value.Length))}...)"
        $envVarsStatus[$varName] = $true
    } else {
        Write-ColorText "❌ $varName: " -Color Red
        Write-Host "  Not set"
        $envVarsStatus[$varName] = $false
        $missingVars += $varName
    }
}

if ($missingVars.Count -gt 0) {
    $diagnosticResults.recommendations += "Set missing environment variables: $($missingVars -join ', ')"
}

$diagnosticResults.checks.environment = $envVarsStatus

# 8. Summary
Write-Section "Diagnostic Summary"

$issueCount = $diagnosticResults.issues.Count
$recommendationCount = $diagnosticResults.recommendations.Count

if ($issueCount -eq 0) {
    Write-ColorText "✅ System Status: " -Color Green
    Write-Host "  All checks passed"
} else {
    Write-ColorText "⚠️  Issues Found: " -Color Yellow
    Write-Host "  $issueCount"
    Write-Host ""
    foreach ($issue in $diagnosticResults.issues) {
        Write-ColorText "  • " -Color Red
        Write-Host $issue
    }
}

if ($recommendationCount -gt 0) {
    Write-Host ""
    Write-ColorText "💡 Recommendations:" -Color Cyan
    Write-Host ""
    foreach ($recommendation in $diagnosticResults.recommendations) {
        Write-ColorText "  • " -Color Yellow
        Write-Host $recommendation
    }
}

# Save report
$reportPath = "diagnostic-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
$diagnosticResults | ConvertTo-Json -Depth 10 | Set-Content $reportPath -Encoding UTF8

Write-Host ""
Write-ColorText "📊 Report saved: " -Color Gray
Write-Host "  $reportPath"

# Send to Discord
if ($SendToDiscord -and $env:DISCORD_WEBHOOK_URL) {
    Write-Host ""
    Write-ColorText "📤 Sending to Discord..." -Color Cyan
    
    $embedColor = if ($issueCount -eq 0) { 0x00ff00 } else { 0xff6b00 }
    
    $discordBody = @{
        embeds = @(
            @{
                title = "🔍 PowerShell Diagnostic Report"
                description = "**Node:** $($diagnosticResults.hostname)`n**User:** $($diagnosticResults.username)"
                color = $embedColor
                fields = @(
                    @{
                        name = "Profile Status"
                        value = if ($profileCheck.syntax_valid) { "✅ Valid" } else { "❌ Syntax errors" }
                        inline = $true
                    },
                    @{
                        name = "Docker"
                        value = if ($diagnosticResults.checks.docker.running) { "✅ Running" } else { "❌ Not running" }
                        inline = $true
                    },
                    @{
                        name = "Issues"
                        value = "$issueCount found"
                        inline = $true
                    }
                )
                timestamp = $diagnosticResults.timestamp
                footer = @{
                    text = "Strategic Khaos Diagnostics"
                }
            }
        )
    } | ConvertTo-Json -Depth 10
    
    try {
        Invoke-RestMethod -Uri $env:DISCORD_WEBHOOK_URL -Method Post -Body $discordBody -ContentType "application/json"
        Write-ColorText "✅ Sent to Discord successfully" -Color Green
    } catch {
        Write-ColorText "⚠️  Failed to send to Discord: $($_.Exception.Message)" -Color Yellow
    }
}

Write-Host ""
Write-ColorText "🎯 Diagnostic complete!" -Color Magenta
Write-Host ""
