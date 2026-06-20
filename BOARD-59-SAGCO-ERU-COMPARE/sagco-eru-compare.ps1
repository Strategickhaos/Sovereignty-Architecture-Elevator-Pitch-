# BOARD-59 — SAGCO ERU Burnrate Comparator (PowerShell launcher)
# Usage:
#   .\sagco-eru-compare.ps1             # full report
#   .\sagco-eru-compare.ps1 --live      # auto-refresh every 60s
#   .\sagco-eru-compare.ps1 --json      # JSON output

param(
    [switch]$Live,
    [switch]$Json,
    [string]$Board = ""
)

$RepoRoot  = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Script    = Join-Path $PSScriptRoot "eru_compare.py"

# Fallback: find repo relative to user profile
if (-not (Test-Path $Script)) {
    $RepoRoot = Join-Path $env:USERPROFILE "Sovereignty-Architecture-Elevator-Pitch-"
    $Script   = Join-Path $RepoRoot "BOARD-59-SAGCO-ERU-COMPARE\eru_compare.py"
}

if (-not (Test-Path $Script)) {
    Write-Host "[ERU] Cannot find eru_compare.py — clone the repo first:" -ForegroundColor Red
    Write-Host "  git clone https://github.com/strategickhaos/Sovereignty-Architecture-Elevator-Pitch-" -ForegroundColor Yellow
    exit 1
}

$args_list = @()
if ($Live)  { $args_list += "--live" }
if ($Json)  { $args_list += "--json" }
if ($Board) { $args_list += "--board"; $args_list += $Board }

Write-Host ""
Write-Host "  SAGCO ERU BURNRATE COMPARATOR" -ForegroundColor Cyan
Write-Host "  SAGCO vs Industry Baseline (DORA / GitHub Octoverse)" -ForegroundColor DarkGray
Write-Host ""

python3 $Script @args_list
