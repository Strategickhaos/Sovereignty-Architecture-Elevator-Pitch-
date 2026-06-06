##############################################################################
#  SAGCO Firefox Dev Plugin Wing — BOARD-28
#  Paste in Admin PowerShell ISE
##############################################################################

$WORLD   = "E:\SAGCO-WORLD"
$REPO    = "$WORLD\Sovereignty-Architecture-Elevator-Pitch-"
$BOARD   = "$REPO\BOARD-28-FIREFOX-DEV-PLUGIN"
$EXT     = "$BOARD\extension"
$AGENTS  = "$REPO\sagco-agents"
$PY      = "python"

Write-Host @"
╔════════════════════════════════════════════════════════════╗
║  SAGCO Firefox Dev Plugin — BOARD-28                      ║
║  Console events → JSON export → SAGCO cases + citizens    ║
╚════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host "`n  [1] Open Firefox extension loader (about:debugging)"
Write-Host "  [2] Ingest exported events JSON → SAGCO cases + citizens"
Write-Host "  [3] List open BOARD-26 Firefox cases"
Write-Host "  [4] Show BOARD-28 antibodies"
Write-Host "  [5] Classify a single browser event"
Write-Host ""

$choice = Read-Host "  Select"

switch ($choice) {
    "1" {
        Write-Host "`n  Opening Firefox extension loader..." -ForegroundColor Yellow
        Write-Host "  1. In Firefox: navigate to about:debugging#/runtime/this-firefox"
        Write-Host "  2. Click: Load Temporary Add-on"
        Write-Host "  3. Select: $EXT\manifest.json"
        Write-Host "`n  Extension files:" -ForegroundColor Cyan
        Get-ChildItem $EXT | Format-Table Name, Length, LastWriteTime
        Start-Process "firefox" "about:debugging#/runtime/this-firefox" -ErrorAction SilentlyContinue
    }
    "2" {
        $eventsFile = Read-Host "  Path to exported firefox-events JSON (drag file here)"
        if (-not $eventsFile) {
            $eventsFile = "$env:USERPROFILE\Downloads\sagco-firefox-events.json"
        }
        $eventsFile = $eventsFile.Trim('"')
        Write-Host "`n  Ingesting: $eventsFile" -ForegroundColor Yellow
        & $PY "$BOARD\src\firefox_event_ingester.py" --file $eventsFile --emit-cases --emit-citizens --summary
    }
    "3" {
        Write-Host "`n  Open Firefox cases (BOARD-26):" -ForegroundColor Yellow
        & $PY "$AGENTS\sagco.py" open-case --list --status open 2>$null
        Get-ChildItem "$REPO\BOARD-26-REMEDIATION-ENGINE\cases\open\FF-*.yaml" -ErrorAction SilentlyContinue |
            ForEach-Object { Write-Host "  · $($_.Name)" }
    }
    "4" {
        Write-Host "`n  BOARD-28 Antibodies:" -ForegroundColor Yellow
        $abs = @(
            "BROWSER_TOKEN_IN_REFERRER",
            "BROWSER_THIRD_PARTY_WIDGET_EVENT",
            "BROWSER_ANALYTICS_SAMPLING",
            "BROWSER_PII_IN_TRACKING_PIXEL",
            "BROWSER_TRACKING_PIXEL_FAILURE",
            "BROWSER_DOWNLOAD_IN_FLIGHT",
            "BROWSER_OAUTH_DRIFT"
        )
        foreach ($ab in $abs) {
            $path = "$REPO\BOARD-11-ANTIBODIES\antibodies\$ab.yaml"
            $exists = if (Test-Path $path) { "✓" } else { "✗" }
            Write-Host "  $exists  $ab"
        }
    }
    "5" {
        $url = Read-Host "  URL or event text to classify"
        & $PY "$AGENTS\sagco.py" comms --classify "browser" $url
    }
}

Write-Host "`n  Quick commands:" -ForegroundColor Magenta
Write-Host "    python $AGENTS\sagco.py firefox --file events.json --emit-cases --emit-citizens" -ForegroundColor White
Write-Host "    python $AGENTS\sagco.py antibody --list" -ForegroundColor White
Write-Host "    Extension path: $EXT\manifest.json" -ForegroundColor White
