# SAGCO RECON ALL-IN-ONE  —  BOARD-13-RECON
# Run in Admin PowerShell ISE
# Discovers: processes, services, docker, wsl, network, gcloud (if available)
# Emits:     YAML nodes, CSV reports, JSON artifacts
# Loop:      reality -> recon -> node -> yaml -> citizen -> antibody -> deployment

param(
    [string]$World      = "E:\SAGCO-WORLD",
    [string]$GcpProject = ""           # optional: override auto-detect
)

$RECON    = "$World\BOARD-13-RECON"
$ANTIBODY = "$World\BOARD-11-ANTIBODIES\antibodies"
$REPORTS  = "$RECON\reports"
$MANIFESTS= "$RECON\manifests"
$SCANS    = "$RECON\scans"

Write-Host "`nSAGCO RECON — BOARD-13" -ForegroundColor Cyan
Write-Host "loop: reality -> recon -> node -> yaml -> citizen -> antibody -> deployment`n" -ForegroundColor DarkCyan

# ── 1. Create directory tree ─────────────────────────────────────────────────
foreach ($dir in @($RECON,$REPORTS,$SCANS,$MANIFESTS,"$RECON\antibodies","$RECON\daemon",$ANTIBODY)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

# ── 2. Write antibody ────────────────────────────────────────────────────────
@"
name: RECON_REPORT_PATH_MISSING
trigger: DirectoryNotFoundException
cause: Export target folder was not created before recon export
expected: reports directory exists
actual: reports directory missing
remedy:
  - Create BOARD-13-RECON/reports before Export-Csv
severity: LOW
department: RECON
status: LEARNED
"@ | Set-Content "$ANTIBODY\RECON_REPORT_PATH_MISSING.yaml"

# ── 3. Processes ─────────────────────────────────────────────────────────────
Write-Host "  scanning processes..." -NoNewline
Get-Process | Select-Object ProcessName,Id,CPU,StartTime -ErrorAction SilentlyContinue |
    Export-Csv "$REPORTS\processes.csv" -NoTypeInformation
$count = (Import-Csv "$REPORTS\processes.csv").Count
Write-Host " $count found" -ForegroundColor Green

# ── 4. Services ──────────────────────────────────────────────────────────────
Write-Host "  scanning services..." -NoNewline
Get-Service | Select-Object Name,Status,StartType |
    Export-Csv "$REPORTS\services.csv" -NoTypeInformation
$count = (Import-Csv "$REPORTS\services.csv").Count
Write-Host " $count found" -ForegroundColor Green

# ── 5. Docker ────────────────────────────────────────────────────────────────
Write-Host "  scanning docker..." -NoNewline
try {
    docker ps --format "table {{.Names}}`t{{.Image}}`t{{.Status}}`t{{.Ports}}" |
        Out-File "$REPORTS\docker-containers.txt"
    Write-Host " done" -ForegroundColor Green
} catch {
    "docker not available: $_" | Out-File "$REPORTS\docker-containers.txt"
    Write-Host " not available" -ForegroundColor Yellow
}

# ── 6. WSL ───────────────────────────────────────────────────────────────────
Write-Host "  scanning WSL distros..." -NoNewline
try {
    wsl -l -v | Out-File "$REPORTS\wsl-distros.txt"
    Write-Host " done" -ForegroundColor Green
} catch {
    "WSL not available" | Out-File "$REPORTS\wsl-distros.txt"
    Write-Host " not available" -ForegroundColor Yellow
}

# ── 7. Network + ARP (Pi detection) ─────────────────────────────────────────
Write-Host "  scanning network..." -NoNewline
ipconfig /all | Out-File "$REPORTS\network-ipconfig.txt"
$arpTable = arp -a
$arpTable | Out-File "$REPORTS\arp-table.txt"
$piPrefixes = @("b8-27-eb","dc-a6-32","e4-5f-01","d8-3a-dd","28-cd-c1")
$piCandidates = $arpTable | Where-Object {
    $line = $_.ToLower()
    $piPrefixes | ForEach-Object { if ($line -match $_) { return $true } }
}
Write-Host " done" -ForegroundColor Green
if ($piCandidates) {
    Write-Host "  ⚡ Raspberry Pi candidate(s) found:" -ForegroundColor Magenta
    $piCandidates | ForEach-Object { Write-Host "    $_" -ForegroundColor Magenta }
    $piCandidates | Out-File "$REPORTS\pi-candidates.txt"
}

# ── 8. GCloud (optional) ─────────────────────────────────────────────────────
$gcloudAvailable = $null -ne (Get-Command gcloud -ErrorAction SilentlyContinue)
if ($gcloudAvailable) {
    Write-Host "  scanning GCP..." -NoNewline
    $project = $GcpProject
    if (-not $project) {
        $project = (gcloud config get-value project 2>$null).Trim()
    }
    if ($project) {
        gcloud run services list --format=json --project=$project 2>$null |
            Out-File "$REPORTS\gcp-cloud-run.json"
        gcloud container clusters list --format=json --project=$project 2>$null |
            Out-File "$REPORTS\gcp-gke-clusters.json"
        gcloud pubsub topics list --format=json --project=$project 2>$null |
            Out-File "$REPORTS\gcp-pubsub.json"
        Write-Host " done (project=$project)" -ForegroundColor Green
    } else {
        Write-Host " no project configured" -ForegroundColor Yellow
    }
} else {
    Write-Host "  gcloud not found — skipping cloud recon" -ForegroundColor DarkGray
}

# ── 9. Write board manifest ──────────────────────────────────────────────────
@"
board: BOARD-13-RECON
purpose: Discover, classify, and register local machine reality before deployment.
outputs:
  - reports/processes.csv
  - reports/services.csv
  - reports/docker-containers.txt
  - reports/wsl-distros.txt
  - reports/network-ipconfig.txt
  - reports/arp-table.txt
  - reports/pi-candidates.txt
  - reports/gcp-cloud-run.json
  - reports/gcp-gke-clusters.json
  - reports/gcp-pubsub.json
loop: reality -> recon -> node -> yaml -> citizen -> antibody -> deployment
status: ACTIVE
ran_at: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')
"@ | Set-Content "$RECON\recon.yaml"

# ── 10. Summary ──────────────────────────────────────────────────────────────
Write-Host "`nSAGCO RECON COMPLETE" -ForegroundColor Green
Get-ChildItem $REPORTS | Format-Table Name,Length,LastWriteTime -AutoSize
Write-Host "`nNext: python sagco_recon.py pi --auto   (register Pi as SAGCO node)" -ForegroundColor Cyan
