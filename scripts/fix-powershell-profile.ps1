# fix-powershell-profile.ps1
# Strategic Khaos PowerShell Profile Repair Script
# Automatically fixes common syntax errors in Windows PowerShell profiles

<#
.SYNOPSIS
    Repairs PowerShell profile syntax errors identified in Nitro V15 Lyra node diagnostics

.DESCRIPTION
    This script:
    - Backs up the current PowerShell profile
    - Fixes common syntax errors (backslash escapes, missing parameters)
    - Adds proper error handling
    - Validates the corrected profile
    - Creates a report of changes made

.PARAMETER ProfilePath
    Path to the PowerShell profile to fix. Defaults to current user's profile.

.PARAMETER DryRun
    Show what would be changed without making actual modifications

.PARAMETER Force
    Skip confirmation prompts

.EXAMPLE
    .\fix-powershell-profile.ps1
    
.EXAMPLE
    .\fix-powershell-profile.ps1 -DryRun
    
.EXAMPLE
    .\fix-powershell-profile.ps1 -ProfilePath "C:\Users\garza\Documents\WindowsPowerShell\profile.ps1" -Force
#>

param(
    [string]$ProfilePath = $PROFILE,
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

# Color output functions
function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

function Write-Success { param([string]$Msg) Write-ColorText "✅ $Msg" -Color Green }
function Write-Info { param([string]$Msg) Write-ColorText "ℹ️  $Msg" -Color Cyan }
function Write-Warning2 { param([string]$Msg) Write-ColorText "⚠️  $Msg" -Color Yellow }
function Write-ErrorMsg { param([string]$Msg) Write-ColorText "❌ $Msg" -Color Red }

# Banner
Write-Host ""
Write-ColorText "╔════════════════════════════════════════════════════════╗" -Color Magenta
Write-ColorText "║   Strategic Khaos PowerShell Profile Repair Tool      ║" -Color Magenta
Write-ColorText "║   Nitro V15 Lyra Node - Diagnostic Resolution         ║" -Color Magenta
Write-ColorText "╚════════════════════════════════════════════════════════╝" -Color Magenta
Write-Host ""

# Check if profile exists
if (-not (Test-Path $ProfilePath)) {
    Write-ErrorMsg "Profile not found: $ProfilePath"
    Write-Info "Creating new profile..."
    
    $profileDir = Split-Path $ProfilePath -Parent
    if (-not (Test-Path $profileDir)) {
        New-Item -Path $profileDir -ItemType Directory -Force | Out-Null
    }
    
    New-Item -Path $ProfilePath -ItemType File -Force | Out-Null
    Write-Success "Created new profile at: $ProfilePath"
}

Write-Info "Profile path: $ProfilePath"
Write-Host ""

# Read current profile content
$originalContent = Get-Content -Path $ProfilePath -Raw -ErrorAction SilentlyContinue

if ([string]::IsNullOrWhiteSpace($originalContent)) {
    Write-Warning2 "Profile is empty. Creating basic profile template..."
    $originalContent = @"
# PowerShell Profile for Strategic Khaos
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

# Custom functions will be added below
"@
}

# Backup current profile
$backupPath = "$ProfilePath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Write-Info "Creating backup: $backupPath"

if (-not $DryRun) {
    Copy-Item -Path $ProfilePath -Destination $backupPath -Force
    Write-Success "Backup created"
}

# Define fixes to apply
$fixes = @(
    @{
        Name = "Fix backslash escape in Mandatory parameter"
        Pattern = 'Mandatory\s*=\s*\\True'
        Replacement = 'Mandatory=$True'
        Description = "Replace \True with `$True (PowerShell boolean)"
    },
    @{
        Name = "Fix backslash escape in parameter type"
        Pattern = '\[string\]\\'
        Replacement = '[string]$Target'
        Description = "Replace [string]\ with [string]`$Target"
    },
    @{
        Name = "Fix incomplete param declaration"
        Pattern = 'param\(\[Parameter\(Mandatory=\$True\)\]\[string\]\$Target\)'
        Replacement = 'param([Parameter(Mandatory=$True)][string]$Target)'
        Description = "Ensure proper param block formatting"
    },
    @{
        Name = "Fix Bash-style OR operator"
        Pattern = '\s+\|\|\s+'
        Replacement = '; if (-not $?) { '
        Description = "Replace || with PowerShell error handling"
    },
    @{
        Name = "Fix Bash-style AND operator"
        Pattern = '\s+&&\s+'
        Replacement = '; '
        Description = "Replace && with semicolon"
    },
    @{
        Name = "Fix 2>/dev/null (stderr redirect)"
        Pattern = '2>/dev/null'
        Replacement = '2>$null'
        Description = "Replace Unix stderr redirect with PowerShell equivalent"
    }
)

# Apply fixes
$modifiedContent = $originalContent
$changesApplied = @()

Write-Info "Analyzing profile for issues..."
Write-Host ""

foreach ($fix in $fixes) {
    if ($modifiedContent -match $fix.Pattern) {
        Write-ColorText "🔧 $($fix.Name)" -Color Yellow
        Write-ColorText "   Pattern: $($fix.Pattern)" -Color Gray
        Write-ColorText "   Fix: $($fix.Description)" -Color Gray
        
        $modifiedContent = $modifiedContent -replace $fix.Pattern, $fix.Replacement
        $changesApplied += $fix.Name
        Write-Host ""
    }
}

if ($changesApplied.Count -eq 0) {
    Write-Success "No issues found! Profile is already correct."
    exit 0
}

# Display changes
Write-ColorText "═══════════════════════════════════════════════════════" -Color Cyan
Write-ColorText "CHANGES TO BE APPLIED ($($changesApplied.Count) fixes)" -Color Cyan
Write-ColorText "═══════════════════════════════════════════════════════" -Color Cyan
Write-Host ""

foreach ($change in $changesApplied) {
    Write-ColorText "  ✓ $change" -Color Green
}

Write-Host ""

# Show diff (simplified)
Write-ColorText "═══════════════════════════════════════════════════════" -Color Cyan
Write-ColorText "PREVIEW OF CHANGES" -Color Cyan
Write-ColorText "═══════════════════════════════════════════════════════" -Color Cyan
Write-Host ""

# Find changed lines
$originalLines = $originalContent -split "`n"
$modifiedLines = $modifiedContent -split "`n"

for ($i = 0; $i -lt [Math]::Max($originalLines.Count, $modifiedLines.Count); $i++) {
    $origLine = if ($i -lt $originalLines.Count) { $originalLines[$i] } else { "" }
    $modLine = if ($i -lt $modifiedLines.Count) { $modifiedLines[$i] } else { "" }
    
    if ($origLine -ne $modLine) {
        Write-ColorText "  Line $($i + 1):" -Color Yellow
        if ($origLine) {
            Write-ColorText "  - $origLine" -Color Red
        }
        if ($modLine) {
            Write-ColorText "  + $modLine" -Color Green
        }
        Write-Host ""
    }
}

# Validate syntax
Write-Info "Validating PowerShell syntax..."
try {
    $null = [scriptblock]::Create($modifiedContent)
    Write-Success "Syntax validation passed"
} catch {
    Write-ErrorMsg "Syntax validation failed: $($_.Exception.Message)"
    Write-Warning2 "The automated fix may not resolve all issues. Manual review recommended."
    
    if (-not $Force) {
        $continue = Read-Host "Continue anyway? (y/N)"
        if ($continue -ne 'y' -and $continue -ne 'Y') {
            Write-Info "Aborted. No changes made."
            exit 1
        }
    }
}

Write-Host ""

# Confirm changes
if ($DryRun) {
    Write-ColorText "═══════════════════════════════════════════════════════" -Color Magenta
    Write-ColorText "DRY RUN MODE - No changes applied" -Color Magenta
    Write-ColorText "═══════════════════════════════════════════════════════" -Color Magenta
    Write-Host ""
    Write-Info "Remove -DryRun flag to apply these changes"
    exit 0
}

if (-not $Force) {
    Write-Host ""
    $confirm = Read-Host "Apply these changes? (Y/n)"
    if ($confirm -eq 'n' -or $confirm -eq 'N') {
        Write-Info "Aborted. No changes made."
        exit 0
    }
}

# Apply changes
Write-Info "Applying fixes to profile..."
Set-Content -Path $ProfilePath -Value $modifiedContent -Encoding UTF8
Write-Success "Profile updated successfully"

# Create repair report
$reportPath = "$ProfilePath.repair-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"
$report = @"
PowerShell Profile Repair Report
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Profile: $ProfilePath
Backup: $backupPath

Changes Applied ($($changesApplied.Count)):
$($changesApplied | ForEach-Object { "  - $_" } | Out-String)

Original Profile Size: $($originalContent.Length) characters
Modified Profile Size: $($modifiedContent.Length) characters

Status: ✅ Repair completed successfully

To revert changes, restore from backup:
  Copy-Item "$backupPath" "$ProfilePath" -Force

To test the profile:
  . $ProfilePath
"@

Set-Content -Path $reportPath -Value $report -Encoding UTF8

# Summary
Write-Host ""
Write-ColorText "═══════════════════════════════════════════════════════" -Color Green
Write-ColorText "REPAIR COMPLETE" -Color Green
Write-ColorText "═══════════════════════════════════════════════════════" -Color Green
Write-Host ""
Write-Success "Profile repaired: $ProfilePath"
Write-Success "Backup created: $backupPath"
Write-Success "Report saved: $reportPath"
Write-Host ""
Write-Info "Next steps:"
Write-Host "  1. Close and reopen PowerShell to load the fixed profile"
Write-Host "  2. Test your custom functions"
Write-Host "  3. Review the report for details: $reportPath"
Write-Host ""
Write-ColorText "🚀 Strategic Khaos operations restored!" -Color Magenta
Write-Host ""
