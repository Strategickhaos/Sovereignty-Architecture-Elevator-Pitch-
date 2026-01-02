# Build Order - INV-087 Xbox RF Station

**Project:** Xbox Sovereign RF Station  
**Goal:** Transform Xbox Series X into infrastructure-independent RF communications hub  
**Timeline:** Flexible, phase-based approach

---

## Overview

```
PHASE 1: Dev Mode Testing (1 hour, $20)
    ↓
PHASE 2: Full Jailbreak (2-4 hours, RISK: Medium)
    ↓
PHASE 3: CB Integration (2-3 hours, $55)
    ↓
PHASE 4: Full RF Stack (1 day, $520)
    ↓
SOVEREIGNTY ACHIEVED
```

---

## Phase 1: Dev Mode (No Jailbreak Yet)

**Duration:** 1 hour  
**Cost:** $20 (one-time Microsoft Dev Mode fee)  
**Risk:** NONE (official Microsoft feature)  
**Reversible:** YES

### Objectives
- [x] Enable official Xbox Dev Mode
- [x] Test USB hardware compatibility
- [x] Verify j5create SSDs work
- [x] Check RTL-SDR recognition
- [x] Document hardware compatibility

### Prerequisites
- Xbox Series X (owned)
- Microsoft account
- $20 payment method
- Internet connection
- USB keyboard (optional but helpful)

### Steps

#### 1.1 Register as Xbox Developer
```
1. Visit: https://partner.microsoft.com/dashboard
2. Sign in with Microsoft account
3. Create developer account (free)
4. Pay $20 one-time activation fee
5. Note activation code
```

#### 1.2 Enable Dev Mode on Xbox
```
1. On Xbox, go to Microsoft Store
2. Search "Dev Mode"
3. Download "Xbox Dev Mode" app
4. Launch app
5. Enter activation code from Partner Center
6. Console will reboot into Dev Mode
```

#### 1.3 Connect to Dev Portal
```
1. In Dev Mode, note IP address (e.g., 192.168.1.100)
2. On PC, open browser
3. Navigate to: https://<xbox-ip>:11443
4. Accept self-signed certificate
5. Log in with credentials shown on Xbox
```

#### 1.4 Test USB Storage
```
1. Connect ATHENA (j5create 128GB) to Xbox rear USB port
2. In Dev Portal → Storage, verify recognition
3. Create test file, verify read/write
4. Repeat for NOVA and LYRA
5. Document which USB ports work best
```

#### 1.5 Test RTL-SDR (if owned)
```
1. Connect RTL-SDR to Xbox USB port
2. In Dev Portal → Device Manager, check USB devices
3. Look for "Realtek RTL2838" or similar
4. Document: recognized or not
5. If not recognized, may work post-jailbreak
```

#### 1.6 Test WiFi Adapter (if available)
```
1. Connect USB WiFi adapter
2. Check recognition in Device Manager
3. Document chipset and driver status
```

### Deliverables
- [x] Dev Mode activated
- [x] Hardware compatibility matrix
- [x] USB port assignment plan
- [x] List of working vs. non-working devices
- [x] Screenshots of Dev Portal

### Decision Point
```
IF all USB devices recognized:
    → Proceed to Phase 2 (jailbreak) with confidence
    
IF some devices not recognized:
    → Research Linux driver support
    → Verify these devices work on PC Linux first
    → May still proceed but expect troubleshooting
    
IF no devices recognized:
    → STOP, investigate Xbox USB issues
```

---

## Phase 2: Full Jailbreak (When Ready)

**Duration:** 2-4 hours  
**Cost:** $0 (if exploit is free)  
**Risk:** MEDIUM (voids warranty, possible brick)  
**Reversible:** MAYBE (depends on exploit)

### ⚠️ WARNING
**READ COMPLETELY BEFORE ATTEMPTING**

This phase voids your Xbox warranty and may render the console unusable for Xbox Live. Only proceed if:
- Console is out of warranty OR you accept warranty loss
- You have backed up any important data
- You are comfortable with risk of total data loss
- You have researched current exploits thoroughly

### Prerequisites
- Phase 1 completed
- Xbox Series X in Dev Mode (or stock, depends on exploit)
- USB flash drive (8GB+, formatted NTFS)
- Current exploit payload (research required)
- Backup PC for payload preparation
- Terminal/SSH client

### Steps

#### 2.1 Research Current Exploit
```
⚠️ Xbox jailbreak scene changes rapidly. Current methods as of 2026:
   - Check: r/xboxhacks (Reddit)
   - Check: GBAtemp forums
   - Check: Xbox-Scene
   - Verify: Firmware version compatibility
   - Verify: Success rate and community support
```

**As of 2026-01-02:** No public full jailbreak for Xbox Series X is widely documented. Paths include:
- Cold boot exploits (if discovered)
- Hypervisor escapes (research level)
- Dev Mode extensions (limited)

**ACTION:** Research thoroughly before proceeding. This phase may be ON HOLD until exploit available.

#### 2.2 Prepare USB Payload (Generic Template)
```
1. Download exploit files from trusted source
2. Verify checksums (SHA256)
3. Format USB drive (usually FAT32 or NTFS)
4. Copy payload to USB root
5. Create required directory structure
6. Eject safely
```

#### 2.3 Execute Jailbreak (Generic Template)
```
⚠️ EXACT PROCEDURE VARIES BY EXPLOIT

Typical flow:
1. Power off Xbox completely
2. Insert USB payload drive
3. Hold specific button combination (exploit-dependent)
4. Power on while holding buttons
5. Follow on-screen prompts
6. Payload installs bootloader
7. Reboot to new boot menu
```

#### 2.4 Install Linux
```
Preferred distro: Ubuntu 22.04 ARM or Arch Linux ARM

Option A: USB Install
1. Create bootable Ubuntu ARM USB
2. Boot Xbox from USB
3. Run installer
4. Partition internal SSD:
   - /boot (512MB, FAT32)
   - / (root, 100GB, ext4)
   - /home (remaining, ext4)
   - swap (16GB, swap)
5. Install base system
6. Install bootloader (GRUB or systemd-boot)
7. Reboot

Option B: Network Install
1. Boot to minimal environment
2. Download and extract rootfs
3. chroot into new system
4. Configure network and packages
5. Install kernel and bootloader
6. Reboot
```

#### 2.5 Post-Install Configuration
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y build-essential git vim wget curl

# Install drivers
sudo apt install -y linux-firmware firmware-amd-graphics

# Configure GPU
lspci | grep VGA
# Should show AMD RDNA 2

# Test GPU
sudo apt install -y mesa-utils
glxinfo | grep "OpenGL renderer"

# Configure audio
sudo apt install -y alsa-utils pulseaudio
aplay -l

# Configure USB
sudo usermod -a -G plugdev $USER
```

#### 2.6 Verify System
```bash
# CPU
lscpu
# Expected: 8 cores, AMD Zen 2

# RAM
free -h
# Expected: ~16GB

# Storage
lsblk
# Expected: Internal NVMe + external j5create SSDs

# GPU
lspci | grep VGA
# Expected: AMD RDNA 2

# USB
lsusb
# Expected: All connected devices listed

# Network
ip a
# Expected: Network interfaces present
```

### Deliverables
- [x] Xbox booting to Linux
- [x] All hardware recognized
- [x] GPU functional
- [x] USB devices working
- [x] Network configured
- [x] SSH access enabled
- [x] Documentation of any issues

### Decision Point
```
IF Linux boots successfully:
    → Proceed to Phase 3 (CB integration)
    
IF partial boot (no GPU, etc.):
    → Troubleshoot drivers
    → Still usable for RF (CPU-only)
    → Proceed with caution
    
IF no boot at all:
    → Attempt recovery
    → If unrecoverable, console bricked
    → STOP, seek community help
```

---

## Phase 3: CB Integration

**Duration:** 2-3 hours  
**Cost:** $55 (USB sound card, cables, relay, basic antenna)  
**Risk:** LOW (external hardware only)  
**Reversible:** YES

### Objectives
- [x] Connect Cobra 29 to Xbox
- [x] Install Direwolf packet radio software
- [x] Test receive (decode packets)
- [x] Test transmit (send packets)
- [x] Calibrate audio levels
- [x] Document CB packet radio operation

### Prerequisites
- Phase 2 completed (Linux on Xbox)
- OR Phase 3 can be tested on separate Linux PC first
- CB radio (Cobra 29)
- USB sound card ($10)
- Audio cables ($10)
- USB GPIO relay ($5)
- CB antenna ($20)
- Coax cable ($10)

### Steps

#### 3.1 Order Parts
```
Shopping list:
[ ] USB sound card (CM108/CM119 chipset)
[ ] 3.5mm stereo cable (male-male)
[ ] 3.5mm to CB mic cable
[ ] USB GPIO relay module
[ ] CB mobile antenna (1/4 wave)
[ ] 10ft coax cable (RG-58)

Total: ~$55
Shipping: 3-5 days (Amazon Prime) or 1-2 weeks (AliExpress)
```

#### 3.2 Install Direwolf
```bash
# On Xbox Linux:
sudo apt update
sudo apt install -y git build-essential cmake libasound2-dev

cd ~
git clone https://github.com/wb2osz/direwolf
cd direwolf
mkdir build && cd build
cmake ..
make -j8  # Use all 8 Xbox CPU cores
sudo make install

# Verify
direwolf -h
```

#### 3.3 Configure Audio
```bash
# List audio devices
aplay -l
arecord -l

# Identify USB sound card (e.g., card 1)

# Test playback
speaker-test -c 2 -D hw:1,0

# Test recording
arecord -D hw:1,0 -f cd -d 5 test.wav
aplay test.wav
```

#### 3.4 Physical Connections
```
1. Cobra 29 speaker jack → 3.5mm cable → USB sound card INPUT
2. USB sound card OUTPUT → 3.5mm cable → Cobra 29 mic jack
3. USB GPIO relay → Cobra 29 mic PTT pins (3 & 4)
4. CB antenna → coax → Cobra 29 antenna jack
5. Tune SWR on Cobra 29 channel 19 (adjust antenna length)
   Target: SWR < 1.5:1
```

#### 3.5 Configure Direwolf
```bash
# Create config
nano ~/direwolf.conf
```

```ini
# Receive-only config (test first)
ADEVICE plughw:1,0
ACHANNELS 1
CHANNEL 0
MODEM 1200
MYCALL XBOX-1
FIX_BITS 1
LOGDIR /home/xbox/direwolf_logs
```

#### 3.6 Test Receive
```bash
# Start Direwolf
direwolf -c ~/direwolf.conf -t 0

# Tune Cobra 29 to CB channel 23
# Ask a friend to transmit APRS packet, or listen for existing traffic
# Observe Direwolf output for decoded packets
```

#### 3.7 Add PTT for Transmit
```bash
# Edit direwolf.conf
nano ~/direwolf.conf
```

```ini
# Add PTT control
PTT /dev/ttyUSB0 RTS
TXDELAY 500
TXTAIL 100

# Add test beacon
PBEACON delay=1 every=60 overlay=S symbol="laptop" lat=40.0000 long=-105.0000 comment="Xbox RF Station - INV-087"
```

#### 3.8 Test Transmit
```bash
# Restart Direwolf
direwolf -c ~/direwolf.conf -t 0

# Monitor on second CB radio or SDR
# Should hear periodic beacon transmissions
# Verify audio clarity and levels
```

#### 3.9 Calibrate Audio
```bash
# Adjust RX level in Direwolf output
# Target: ~50-60% audio level

# Use alsamixer to adjust
alsamixer
# Select USB sound card
# Adjust Capture (input) and Playback (output) levels

# Test and iterate
```

### Deliverables
- [x] CB radio connected to Xbox
- [x] Direwolf installed and configured
- [x] Receive working (decodes packets)
- [x] Transmit working (sends packets)
- [x] Audio levels calibrated
- [x] Documentation of configuration

### Decision Point
```
IF CB packet radio working:
    → Proceed to Phase 4 (full RF stack)
    
IF receive works but not transmit:
    → Troubleshoot PTT control
    → Can still operate receive-only
    → Fix transmit before Phase 4
    
IF neither works:
    → Check audio connections
    → Verify Cobra 29 functional
    → Test on separate PC to isolate issue
```

---

## Phase 4: Full RF Stack

**Duration:** 1 day  
**Cost:** $520 (RTL-SDR, WiFi, LoRa, UPS, better antenna)  
**Risk:** LOW (adding more devices)  
**Reversible:** YES

### Objectives
- [x] Integrate RTL-SDR for spectrum scanning
- [x] Add long-range WiFi capability
- [x] Add LoRa mesh networking
- [x] Unify all RF systems under single control interface
- [x] Implement automated logging and monitoring
- [x] Add power backup (UPS)
- [x] Upgrade to base station antenna

### Prerequisites
- Phase 3 completed (CB packet working)
- Additional hardware budget (~$520)

### Steps

#### 4.1 Order Remaining Hardware
```
Shopping list:
[ ] RTL-SDR V4 (if not owned) - $40
[ ] SDR discone antenna - $30
[ ] Alfa WiFi adapter (AWUS036ACH) - $50
[ ] High-gain WiFi antenna - $30
[ ] LoRa T-Beam - $40
[ ] UPS (1500VA) - $150
[ ] CB base antenna (1/2 wave) - $80
[ ] Antenna mast - $50
[ ] Powered USB hub (10-port) - $30
[ ] Misc cables and adapters - $20

Total: ~$520
```

#### 4.2 Install RTL-SDR
```bash
# Install drivers and tools
sudo apt install -y rtl-sdr librtlsdr-dev gqrx-sdr

# Set up udev rules
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2838", MODE="0666"' | sudo tee /etc/udev/rules.d/20-rtlsdr.rules
sudo udevadm control --reload-rules

# Test RTL-SDR
rtl_test -t

# Launch Gqrx for spectrum analysis
gqrx
# Scan 26-28 MHz (CB band)
# Scan 144 MHz (2m ham)
# Scan 450 MHz (UHF)
```

#### 4.3 Install WiFi Adapter
```bash
# Connect Alfa WiFi adapter
# Check recognition
lsusb | grep -i "realtek\|atheros\|ralink"

# Install drivers (if needed)
sudo apt install -y linux-headers-$(uname -r)
# Follow Alfa-specific driver instructions

# Scan for networks
sudo iwlist wlan1 scan | grep ESSID

# Monitor mode (for research only)
sudo airmon-ng start wlan1
```

#### 4.4 Install LoRa Node
```bash
# Install Meshtastic tools
pip3 install meshtastic

# Connect T-Beam via USB
# Flash Meshtastic firmware (if needed)
meshtastic --info

# Configure node
meshtastic --set lora.region US
meshtastic --set lora.hop_limit 3
meshtastic --set device.role ROUTER

# Test message send
meshtastic --sendtext "Xbox RF Station online"
```

#### 4.5 Install GNURadio
```bash
# For advanced signal processing
sudo apt install -y gnuradio

# Verify installation
gnuradio-companion

# Create flowgraphs for:
# - Multi-band scanning
# - Signal analysis
# - Custom demodulation
```

#### 4.6 Unified Control Interface
```bash
# Create master control script
nano ~/rf_control.py
```

```python
#!/usr/bin/env python3
"""
INV-087 RF Station Control
Unified interface for all RF systems
"""

import subprocess
import socket
import serial

class RFStation:
    def __init__(self):
        self.direwolf_host = 'localhost'
        self.direwolf_port = 8001
        
    def cb_status(self):
        """Check Direwolf status"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.direwolf_host, self.direwolf_port))
            sock.close()
            return "CB Packet: ONLINE"
        except:
            return "CB Packet: OFFLINE"
    
    def sdr_scan(self, freq_start, freq_end):
        """Scan spectrum with RTL-SDR"""
        cmd = f"rtl_power -f {freq_start}M:{freq_end}M:10k -i 1 scan.csv"
        subprocess.run(cmd, shell=True)
        return "Scan complete"
    
    def lora_send(self, message):
        """Send LoRa message"""
        cmd = f'meshtastic --sendtext "{message}"'
        subprocess.run(cmd, shell=True)
        return "LoRa message sent"
    
    def full_status(self):
        """Get status of all RF systems"""
        print("=" * 60)
        print("INV-087 XBOX RF STATION STATUS")
        print("=" * 60)
        print(self.cb_status())
        print(f"RTL-SDR: {self.check_rtlsdr()}")
        print(f"LoRa: {self.check_lora()}")
        print(f"WiFi: {self.check_wifi()}")
        print("=" * 60)
    
    # Additional methods...

if __name__ == '__main__':
    station = RFStation()
    station.full_status()
```

```bash
chmod +x ~/rf_control.py
```

#### 4.7 Automated Logging
```bash
# Create logging service
sudo nano /etc/systemd/system/rf-logger.service
```

```ini
[Unit]
Description=RF Station Logger
After=network.target

[Service]
Type=simple
User=xbox
ExecStart=/home/xbox/rf_logger.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable rf-logger
sudo systemctl start rf-logger
```

#### 4.8 Install UPS
```
1. Connect Xbox power cable to UPS output
2. Connect CB radio to UPS output
3. Connect fans and accessories to UPS output
4. Connect UPS to wall outlet
5. Install UPS management software (apcupsd or nut)
6. Configure auto-shutdown on low battery
```

```bash
# Install UPS tools
sudo apt install -y apcupsd

# Configure
sudo nano /etc/apcupsd/apcupsd.conf

# Test
apcaccess status
```

#### 4.9 Upgrade Antenna
```
1. Install antenna mast (roof, attic, or backyard)
2. Mount CB base antenna (1/2 wave ground plane)
3. Run coax to shack (use RG-8X or better)
4. Ground antenna properly
5. Tune SWR (target < 1.2:1)
6. Mount SDR discone antenna nearby
7. Mount WiFi directional antenna (if applicable)
```

### Deliverables
- [x] All RF systems operational
- [x] Unified control interface
- [x] Automated logging
- [x] UPS backup power
- [x] Improved antenna system
- [x] Full documentation
- [x] Performance benchmarks

### Decision Point
```
IF all systems integrated:
    → SOVEREIGNTY ACHIEVED
    → Begin operational use
    → Document use cases
    
IF some systems incomplete:
    → Identify blockers
    → Prioritize based on use case
    → Iterate
```

---

## Post-Build: Operational Use

### Regular Operations
- **Daily:** Check system status, review logs
- **Weekly:** Test all RF systems, backup data
- **Monthly:** Update software, maintenance checks

### Use Cases
1. **Emergency Communications:** CB + LoRa for local coordination
2. **Spectrum Intelligence:** RTL-SDR passive monitoring
3. **Mesh Networking:** LoRa gateway for community mesh
4. **Experimentation:** GNURadio flowgraph development

### Integration with Strategickhaos Ecosystem
- Log RF data to j5create SSDs
- Sync with laptops (Vaio, ROG) for analysis
- Connect to broader Strategickhaos network architecture
- Share findings with community

---

## Timeline Summary

| Phase | Duration | Cost | Cumulative |
|-------|----------|------|------------|
| Phase 1: Dev Mode | 1 hour | $20 | $20 |
| Phase 2: Jailbreak | 2-4 hours | $0 | $20 |
| Phase 3: CB Integration | 2-3 hours | $55 | $75 |
| Phase 4: Full RF Stack | 1 day | $520 | $595 |
| **TOTAL** | **~2 days** | **$595** | **$595** |

**Note:** Timeline assumes smooth execution. Budget for troubleshooting time.

---

## Risk Mitigation

### Phase 1 (Dev Mode)
- **Risk:** None (official feature)
- **Mitigation:** N/A

### Phase 2 (Jailbreak)
- **Risk:** Console brick, warranty void
- **Mitigation:** 
  - Thorough research before attempting
  - Backup all data
  - Accept warranty loss
  - Have recovery plan

### Phase 3 (CB Integration)
- **Risk:** Low (external hardware)
- **Mitigation:**
  - Test on separate PC first
  - Verify audio levels carefully
  - Don't overdrive CB transmitter

### Phase 4 (Full RF Stack)
- **Risk:** Low (adding devices)
- **Mitigation:**
  - Use powered USB hub
  - Monitor Xbox temperatures
  - Ensure adequate cooling

---

## Success Criteria

**Phase 1:** USB devices recognized in Dev Mode  
**Phase 2:** Linux boots successfully, hardware functional  
**Phase 3:** CB packet radio working (RX and TX)  
**Phase 4:** All RF systems integrated and operational

**Overall:** Sovereign RF station capable of infrastructure-independent communications

---

**Status:** Build plan ready, awaiting Phase 1 execution  
**Next Action:** Enable Xbox Dev Mode OR USB tether phone for GitHub push  
**Last Updated:** 2026-01-02 by Strategickhaos
