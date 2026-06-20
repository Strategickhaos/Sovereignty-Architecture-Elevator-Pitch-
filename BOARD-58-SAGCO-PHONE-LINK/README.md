# BOARD-58 — SAGCO Phone Link Headless
## Sovereign replacement for Microsoft Phone Link

**Two nodes. One organism. Zero Microsoft.**

---

## Start server on Z Fold (Termux)
```bash
python3 BOARD-58-SAGCO-PHONE-LINK/server.py
```

## Connect from SAGCO-OS Desktop (PowerShell)
```powershell
# Auto-detect phone on LAN:
.\BOARD-58-SAGCO-PHONE-LINK\sagco-phonelink.ps1

# Direct connect:
.\BOARD-58-SAGCO-PHONE-LINK\sagco-phonelink.ps1 -PhoneHost 192.168.1.89
```

---

## Commands (from desktop)

| Command | What it does |
|---------|-------------|
| `!shell <cmd>` | Run any shell command on phone |
| `!sagco <cmd>` | Run sagco organism command on phone |
| `!disk` | Phone storage status |
| `!ls` | Phone home directory |
| `!recon` | nmap LAN scan FROM the phone |
| `!nmap <ip>` | Port scan target from phone |
| `quit` | Disconnect |

---

## Examples
```
sagco-link › !disk
sagco-link › !sagco status
sagco-link › !shell cat ~/sagco_master_command.yaml
sagco-link › !shell nmap -p 22,80,443 192.168.1.71
sagco-link › !recon
```

---

## Security
Set `SAGCO_LINK_SECRET` env var on both sides for HMAC auth:
```bash
# Phone:
export SAGCO_LINK_SECRET=your_secret
python3 server.py

# Desktop:
.\sagco-phonelink.ps1 -PhoneHost 192.168.1.89 -Secret your_secret
```

---

## Phase 2 — Auto-start on boot (Termux)
```bash
# Add to ~/.bashrc or Termux:Boot
python3 ~/BOARD-58-SAGCO-PHONE-LINK/server.py &
```
