# SAGCO Phone Link — Desktop Client (PowerShell)
# BOARD-58: Headless replacement for Microsoft Phone Link
#
# Usage:
#   .\sagco-phonelink.ps1                        # auto-detect phone on LAN
#   .\sagco-phonelink.ps1 -Host 192.168.1.89     # direct connect
#   .\sagco-phonelink.ps1 -Host 192.168.1.89 -Port 9944

param(
    [string]$PhoneHost = "",
    [int]$Port = 9944,
    [string]$Secret = ""
)

$BANNER = @"
  ╔══════════════════════════════════════════╗
  ║   SAGCO PHONE LINK — Headless Terminal   ║
  ║   Strategickhaos DAO LLC                 ║
  ╚══════════════════════════════════════════╝
"@

function Find-SagcoPhone {
    Write-Host "[link] scanning LAN for SAGCO Z Fold node..." -ForegroundColor Cyan
    $subnet = "192.168.1"
    # Check known phone IP first
    foreach ($candidate in @("192.168.1.89", "192.168.1.86", "192.168.1.88")) {
        try {
            $tcp = New-Object System.Net.Sockets.TcpClient
            $conn = $tcp.BeginConnect($candidate, $Port, $null, $null)
            $wait = $conn.AsyncWaitHandle.WaitOne(500, $false)
            if ($wait -and $tcp.Connected) {
                $tcp.Close()
                Write-Host "[link] found SAGCO node at $candidate" -ForegroundColor Green
                return $candidate
            }
            $tcp.Close()
        } catch {}
    }
    Write-Host "[link] auto-detect failed — specify -PhoneHost <ip>" -ForegroundColor Yellow
    return $null
}

function Start-SagcoLink {
    param([string]$Host_, [int]$Port_)

    Write-Host $BANNER -ForegroundColor Green
    Write-Host "[link] connecting to $Host_`:$Port_..." -ForegroundColor Cyan

    try {
        $tcp    = New-Object System.Net.Sockets.TcpClient($Host_, $Port_)
        $stream = $tcp.GetStream()
        $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
        $writer = New-Object System.IO.StreamWriter($stream, [System.Text.Encoding]::UTF8)
        $writer.AutoFlush = $true
    } catch {
        Write-Host "[link] connection failed: $_" -ForegroundColor Red
        return
    }

    Write-Host "[link] connected to SAGCO Z Fold" -ForegroundColor Green
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor DarkGray
    Write-Host "  !shell <cmd>   run shell command on phone" -ForegroundColor DarkGray
    Write-Host "  !sagco <cmd>   run sagco organism command" -ForegroundColor DarkGray
    Write-Host "  !disk          phone storage status" -ForegroundColor DarkGray
    Write-Host "  !ls            list phone home dir" -ForegroundColor DarkGray
    Write-Host "  !recon         nmap LAN scan from phone" -ForegroundColor DarkGray
    Write-Host "  !nmap <ip>     port scan target from phone" -ForegroundColor DarkGray
    Write-Host "  quit           disconnect" -ForegroundColor DarkGray
    Write-Host ""

    # Background receiver thread
    $recvJob = [System.Threading.Thread]::new({
        param($rdr)
        $buf = ""
        try {
            while ($true) {
                $b = $rdr.BaseStream.ReadByte()
                if ($b -lt 0) { break }
                if ($b -eq 0) {
                    # null terminator — flush buffer
                    if ($buf.Trim()) {
                        Write-Host ""
                        Write-Host $buf.Trim() -ForegroundColor White
                        Write-Host ""
                    }
                    $buf = ""
                } else {
                    $buf += [char]$b
                }
            }
        } catch {}
    })
    $recvJob.IsBackground = $true

    # Simpler synchronous approach (works better in PS)
    $TERM = [byte[]](0, 10)  # \x00\n

    function Read-Response {
        $buf = New-Object System.Collections.Generic.List[byte]
        try {
            while ($true) {
                $b = $stream.ReadByte()
                if ($b -lt 0) { return $null }
                $buf.Add($b)
                # Check for \x00\n terminator
                $n = $buf.Count
                if ($n -ge 2 -and $buf[$n-2] -eq 0 -and $buf[$n-1] -eq 10) {
                    # Remove terminator
                    $buf.RemoveRange($n-2, 2)
                    return [System.Text.Encoding]::UTF8.GetString($buf.ToArray()).Trim()
                }
            }
        } catch { return $null }
    }

    # Read banner
    $banner_resp = Read-Response
    if ($banner_resp) {
        Write-Host $banner_resp -ForegroundColor Cyan
    }

    # Main REPL
    while ($true) {
        Write-Host -NoNewline "sagco-link › " -ForegroundColor Green
        $cmd = Read-Host

        if (-not $cmd.Trim()) { continue }
        if ($cmd.ToLower() -in @("quit","exit","q")) {
            $writer.WriteLine("quit")
            break
        }

        $writer.WriteLine($cmd)

        # Read response with timeout
        $stream.ReadTimeout = 35000
        $resp = Read-Response
        if ($null -eq $resp) {
            Write-Host "[link] connection lost" -ForegroundColor Red
            break
        }
        if ($resp) {
            Write-Host $resp -ForegroundColor White
        }
    }

    $stream.Close()
    $tcp.Close()
    Write-Host "[link] disconnected from Z Fold" -ForegroundColor Yellow
}

# ── MAIN ──────────────────────────────────────────────────────────────────────

if (-not $PhoneHost) {
    $PhoneHost = Find-SagcoPhone
}

if ($PhoneHost) {
    Start-SagcoLink -Host_ $PhoneHost -Port_ $Port
} else {
    Write-Host "Usage: .\sagco-phonelink.ps1 -PhoneHost 192.168.1.89" -ForegroundColor Yellow
}
