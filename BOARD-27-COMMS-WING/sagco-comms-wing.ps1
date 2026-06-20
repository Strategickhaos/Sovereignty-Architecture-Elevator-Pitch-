##############################################################################
#  SAGCO Comms Wing — Email + Cell + Sequence
#  Paste in Admin PowerShell
#  District: frequency_coast
##############################################################################

$WORLD  = "E:\SAGCO-WORLD"
$REPO   = "$WORLD\Sovereignty-Architecture-Elevator-Pitch-"
$AGENTS = "$REPO\sagco-agents"
$PY     = "python"

Write-Host @"
╔════════════════════════════════════════════════════════════╗
║  SAGCO Comms Wing — Frequency Coast                       ║
║  Email · SMS · Sequence · Contacts                        ║
╚════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host "`n  [1] Scan SMS (Phone Link demo — Z Fold 7)"
Write-Host "  [2] Show known contacts"
Write-Host "  [3] Classify a message"
Write-Host "  [4] Comms district stats"
Write-Host "  [5] Analyze heap snapshot"
Write-Host "  [6] Register Sequence as citizen"
Write-Host "  [7] Full comms inbox scan"
Write-Host ""

$choice = Read-Host "  Select"

switch ($choice) {
    "1" {
        Write-Host "`n  SMS scan..." -ForegroundColor Yellow
        & $PY "$AGENTS\sagco.py" comms --sms
    }
    "2" {
        Write-Host "`n  Known contacts:" -ForegroundColor Yellow
        & $PY "$AGENTS\sagco.py" comms --contacts
    }
    "3" {
        $sender = Read-Host "  Sender (number or email)"
        $body   = Read-Host "  Message body"
        & $PY "$AGENTS\sagco.py" comms --classify $sender $body --emit-citizens
    }
    "4" {
        & $PY "$AGENTS\sagco.py" comms --stats
    }
    "5" {
        $heap = Read-Host "  Heap snapshot path (default: Downloads\Heap-20260606T164726.heapsnapshot)"
        if (-not $heap) { $heap = "$env:USERPROFILE\Downloads\Heap-20260606T164726.heapsnapshot" }
        Write-Host "`n  Analyzing heap snapshot..." -ForegroundColor Magenta
        & $PY "$REPO\BOARD-13-RECON\heap_analyzer.py" --file $heap --eru --emit-citizens
    }
    "6" {
        Write-Host "`n  Registering Sequence as frequency_coast citizen..." -ForegroundColor Yellow
        & $PY "$AGENTS\sagco.py" catpush --name "sequence-workflow-tool" --kind artifact --district frequency_coast
    }
    "7" {
        Write-Host "`n  Full inbox scan (Gmail MCP required)..." -ForegroundColor Yellow
        & $PY "$AGENTS\sagco.py" comms --inbox
    }
}

Write-Host "`n  Quick commands:" -ForegroundColor Magenta
Write-Host "    python $AGENTS\sagco.py comms --sms"              -ForegroundColor White
Write-Host "    python $AGENTS\sagco.py comms --contacts"         -ForegroundColor White
Write-Host "    python $AGENTS\sagco.py comms --stats"            -ForegroundColor White
Write-Host "    python $REPO\BOARD-13-RECON\heap_analyzer.py --file HEAP.heapsnapshot --eru" -ForegroundColor White
