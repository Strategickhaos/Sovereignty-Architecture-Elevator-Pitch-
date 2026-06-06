##############################################################################
#  SAGCO Phone OS — BOARD-29
#  Paste in Admin PowerShell ISE
#  Every agent has a line. Desktop folder = device. sagco:// = protocol.
##############################################################################

$WORLD   = "E:\SAGCO-WORLD"
$REPO    = "$WORLD\Sovereignty-Architecture-Elevator-Pitch-"
$BOARD   = "$REPO\BOARD-29-SAGCO-PHONE-OS"
$AGENTS  = "$REPO\sagco-agents"
$PY      = "python"

Write-Host @"
╔════════════════════════════════════════════════════════════╗
║  SAGCO Phone OS — BOARD-29                                 ║
║  Every agent has a line. sagco:// is the protocol.        ║
╚════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host "  [1] Show full agent directory"
Write-Host "  [2] Call an agent"
Write-Host "  [3] Send SMS to agent"
Write-Host "  [4] View inbox / SMS log"
Write-Host "  [5] Enumerate a phone folder → citizens"
Write-Host "  [6] Dry-run enumerate (preview only)"
Write-Host ""

$choice = Read-Host "  Select"

switch ($choice) {
    "1" {
        Write-Host "`n  Agent Phone Directory:" -ForegroundColor Yellow
        & $PY "$AGENTS\sagco.py" phone directory
    }
    "2" {
        $agent = Read-Host "  Agent name (e.g. BOARD-26-REMEDIATION-ENGINE)"
        & $PY "$AGENTS\sagco.py" phone call $agent
    }
    "3" {
        $agent = Read-Host "  Agent name"
        $msg   = Read-Host "  Message"
        & $PY "$AGENTS\sagco.py" phone sms $agent $msg
    }
    "4" {
        Write-Host "`n  Inbox:" -ForegroundColor Yellow
        & $PY "$AGENTS\sagco.py" phone inbox
    }
    "5" {
        $folder = Read-Host "  Phone folder path (drag folder here, or press Enter for Downloads)"
        if (-not $folder) { $folder = "$env:USERPROFILE\Downloads" }
        $folder = $folder.Trim('"')
        Write-Host "`n  Enumerating: $folder" -ForegroundColor Yellow
        & $PY "$AGENTS\sagco.py" phone enumerate $folder
    }
    "6" {
        $folder = Read-Host "  Phone folder path"
        if (-not $folder) { $folder = "$env:USERPROFILE\Downloads" }
        $folder = $folder.Trim('"')
        Write-Host "`n  Dry-run enumerate: $folder" -ForegroundColor Yellow
        & $PY "$AGENTS\sagco.py" phone enumerate $folder --dry-run
    }
}

Write-Host "`n  Quick commands:" -ForegroundColor Magenta
Write-Host "    python $AGENTS\sagco.py phone directory" -ForegroundColor White
Write-Host "    python $AGENTS\sagco.py phone call BOARD-26-REMEDIATION-ENGINE" -ForegroundColor White
Write-Host "    python $AGENTS\sagco.py phone sms SAGCO-VOICE `"Hey Baby, show me the empire`"" -ForegroundColor White
Write-Host "    python $AGENTS\sagco.py phone enumerate `$env:USERPROFILE\Downloads" -ForegroundColor White
