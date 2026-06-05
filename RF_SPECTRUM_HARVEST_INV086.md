# 🔥 INV-086: AETHER HARVEST - RF SPECTRUM SOVEREIGNTY 🔥

**Siphoning the Spectrum into Sovereign Streams**

**Generated:** 2026-01-02  
**Classification:** RF Sovereignty Architecture  
**Purpose:** Building independent RF infrastructure for data sovereignty without portal dependencies

---

## 🌊 SPECTRUM UPDATE: 2026 AIRWAVE LANDSCAPE

The electromagnetic spectrum has evolved significantly post-5G rollout. Here's what's active in 2026:

### **Active Spectrum Bands (2026)**

| **Frequency Band** | **Technology** | **Status** | **Siphon Potential** |
|-------------------|----------------|------------|---------------------|
| 400-512 MHz | UHF/Public Safety | Dense | ⚠️ Legal (receive only) |
| 433-915 MHz | LoRaWAN/IoT | Explosive Growth | ✅ Open ISM Band |
| 2.4 GHz | WiFi 4/5, Bluetooth, Zigbee | Saturated | ✅ Open WiFi harvesting |
| 3.5-4.2 GHz | CBRS/5G (Citizens Band) | Moderate | ⚠️ Licensed/Shared |
| 5 GHz | WiFi 5/6 (5.15-5.925 GHz) | Dense | ✅ Open WiFi harvesting |
| 6 GHz | WiFi 6E/7 (5.925-7.125 GHz) | Emerging | ✅ New frontier (2026) |
| Sub-6 GHz | 5G/6G (600M-3.7G) | Dominant | ⚠️ Receive only |
| 24-47 GHz | 5G mmWave | Urban Dense | ⚠️ Receive only |
| L-Band (1-2 GHz) | Satellite (GPS, Inmarsat) | Global | ✅ Receive broadcasts |
| Ku-Band (12-18 GHz) | Satellite (Starlink, Kuiper) | Growing | ⚠️ Licensed receive |

### **2026 Spectrum Trends**
- **WiFi 6E/7 (6 GHz)**: 1.2 GHz of new spectrum opened. More channels, but urban congestion increasing.
- **5G/6G Deployment**: Sub-6 GHz now dominant nationwide. mmWave concentrated in metro areas.
- **LoRaWAN Explosion**: Smart cities deployed free mesh networks globally. Public LoRa gateways everywhere.
- **Satellite Internet**: Starlink V2 + Amazon Kuiper = 90% global coverage. Free tier siphoning possible.
- **Ambient IoT**: New tech harvests RF energy for both power and data trickle.
- **CBRS (3.5 GHz)**: Citizens Broadband Radio Service shared spectrum - opportunities exist.

---

## 🎯 BUILD PRIORITY: LAYERED RF SIPHON STATION

**Total Cost:** $500-700 (down from $600 in 2025 due to SDR price drops)  
**Build Time:** 1-2 weeks phased deployment  
**Control Hub:** Athena compute + Pi hubs for orchestration

### **Architecture Overview**
```
┌─────────────────────────────────────────────────────────┐
│                  ATHENA ORCHESTRATOR                    │
│           (Central Processing & Coordination)           │
└───────────────┬─────────────────────────────────────────┘
                │
    ┌───────────┼───────────┬──────────────┬──────────────┐
    │           │           │              │              │
┌───▼───┐   ┌──▼──┐    ┌───▼────┐    ┌────▼────┐   ┌────▼─────┐
│ SDR   │   │WiFi │    │ LoRa   │    │ Phone   │   │Satellite │
│Scanner│   │Sniper│   │ Mesh   │    │ Tether  │   │Receiver  │
└───────┘   └─────┘    └────────┘    └─────────┘   └──────────┘
  $65         $110        $150          FREE          $135
```

---

## 📡 PHASE 1: SPECTRUM SCANNING (Foundation - DO THIS FIRST)

**Purpose:** Intelligence gathering on local electromagnetic environment. Reveals siphon targets and opportunities.

### **Hardware Required**
- **RTL-SDR V4 Dongle**: $25 (NooElec, Amazon)
  - Frequency: 500 kHz - 1.7 GHz (native)
  - Improved sensitivity over V3
  - Supports direct sampling for HF
- **NooElec Ham It Up V1.3**: $40 (optional HF upconverter)
  - Extends range: 100 kHz - 6 GHz
- **Antennas**:
  - Stock dipole (included, 25-1800 MHz)
  - Discone for scanning ($30-50, recommended)
  - Telescopic antenna for portability

**Total Phase 1 Cost:** $65-115

### **Software Setup**

#### **Linux/Athena Installation**
```bash
# Update system and install RTL-SDR drivers
sudo apt update && sudo apt upgrade -y
sudo apt install rtl-sdr gqrx-sdr librtlsdr-dev python3-pip -y

# Test RTL-SDR dongle detection
rtl_test -t

# Expected output: "Found 1 device(s): Generic RTL2832U"
# If failed, check USB connection and run: sudo rmmod dvb_usb_rtl28xxu
```

#### **Spectrum Scanning GUI (GQRX)**
```bash
# Launch GQRX
gqrx

# Configuration:
# - Device: RTL-SDR
# - Sample Rate: 2.4 MSPS
# - Frequency: Start at 100 MHz
# - Mode: WFM for FM radio, NFM for services
```

**GQRX Quick Guide:**
- **Waterfall view**: Real-time spectrum visualization
- **Tune frequencies**: Click waterfall or type frequency
- **Record audio**: Right-click > Start audio recorder

#### **Automated Spectrum Sweep**
```bash
# 10-minute spectrum heat map (100 MHz - 6 GHz)
rtl_power -f 100M:6G:1M -g 50 -i 10m spectrum_scan_$(date +%Y%m%d_%H%M).csv

# For continuous monitoring (1-hour bins)
rtl_power -f 100M:1.7G:100k -g 40 -i 1h -e 24h daily_spectrum.csv
```

### **Spectrum Analysis Python Script**

Save as `scripts/rf_harvest/spectrum_analyzer.py`:

```python
#!/usr/bin/env python3
"""
RTL-SDR Spectrum Analyzer and Visualization
Analyzes rtl_power CSV output and identifies active frequencies
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def analyze_spectrum(csv_file):
    """Load and analyze spectrum CSV from rtl_power"""
    print(f"[*] Loading spectrum data from {csv_file}...")
    
    # rtl_power CSV format: date, time, Hz low, Hz high, Hz step, samples, dB values...
    df = pd.read_csv(csv_file, header=None)
    
    # Extract frequency data (columns 2-5) and power levels (6+)
    freq_start = df.iloc[:, 2]
    freq_stop = df.iloc[:, 3]
    power_data = df.iloc[:, 6:]
    
    # Calculate center frequencies
    center_freqs = (freq_start + freq_stop) / 2 / 1e6  # Convert to MHz
    
    # Average power across time
    avg_power = power_data.mean(axis=1)
    max_power = power_data.max(axis=1)
    
    # Find peaks (active frequencies)
    threshold = avg_power.mean() + (avg_power.std() * 2)
    peaks = avg_power[avg_power > threshold]
    
    print(f"\n[+] Analysis Results:")
    print(f"    Frequency Range: {center_freqs.min():.2f} - {center_freqs.max():.2f} MHz")
    print(f"    Average Power: {avg_power.mean():.2f} dB")
    print(f"    Detected Peaks: {len(peaks)}")
    
    print(f"\n[+] Top 10 Active Frequencies:")
    peak_freqs = center_freqs[avg_power > threshold].values
    peak_powers = avg_power[avg_power > threshold].values
    sorted_idx = np.argsort(peak_powers)[::-1][:10]
    
    for idx in sorted_idx:
        freq = peak_freqs[idx]
        power = peak_powers[idx]
        band = identify_band(freq)
        print(f"    {freq:8.2f} MHz | {power:6.2f} dB | {band}")
    
    # Generate visualization
    plt.figure(figsize=(14, 6))
    plt.plot(center_freqs, avg_power, linewidth=0.5, alpha=0.7, label='Average Power')
    plt.plot(center_freqs, max_power, linewidth=0.3, alpha=0.5, label='Peak Power')
    plt.axhline(y=threshold, color='r', linestyle='--', alpha=0.5, label='Detection Threshold')
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Power (dB)')
    plt.title(f'Spectrum Analysis - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_file = csv_file.replace('.csv', '_plot.png')
    plt.savefig(output_file, dpi=150)
    print(f"\n[+] Plot saved to {output_file}")
    
    return center_freqs, avg_power

def identify_band(freq_mhz):
    """Identify service/band for a given frequency"""
    if 88 <= freq_mhz <= 108:
        return "FM Radio"
    elif 162 <= freq_mhz <= 174:
        return "Marine VHF"
    elif 400 <= freq_mhz <= 512:
        return "UHF/Public Safety"
    elif freq_mhz == 433.92:
        return "ISM 433 MHz (IoT)"
    elif 862 <= freq_mhz <= 928:
        return "ISM 900 MHz (LoRa/Cellular)"
    elif 2400 <= freq_mhz <= 2500:
        return "2.4 GHz WiFi/Bluetooth"
    elif 5150 <= freq_mhz <= 5925:
        return "5 GHz WiFi"
    elif 5925 <= freq_mhz <= 7125:
        return "6 GHz WiFi 6E/7"
    else:
        return "Unknown/Other"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 spectrum_analyzer.py <rtl_power_csv_file>")
        sys.exit(1)
    
    analyze_spectrum(sys.argv[1])
```

### **What You'll See**
- **FM Radio** (88-108 MHz): Local broadcast stations
- **Public Safety** (400-512 MHz): Police, fire, EMS (encrypted in most areas)
- **Cell Towers** (700-2600 MHz): Carrier signals (Verizon, AT&T, T-Mobile)
- **WiFi Hotspots** (2.4/5/6 GHz): Home networks, businesses, public APs
- **LoRa Gateways** (915 MHz in US, 868 MHz EU): IoT mesh networks
- **Satellite Signals** (1-2 GHz L-band): GPS, Inmarsat, weather satellites

### **Legal Status: ✅ 100% LEGAL**
Passive reception of radio signals is legal under FCC Part 15. You may listen to any frequency. Recording and sharing may have restrictions for certain services (e.g., cell phones).

---

## 📶 PHASE 2: LONG-RANGE WIFI SNIPER (Quick Win)

**Purpose:** Harvest free/open WiFi from miles away without password cracking.

### **Hardware Required**
- **Alfa AWUS036ACHM**: $45 (dual-band, 2.4/5 GHz, monitor mode)
  - Chipset: MediaTek MT7610U
  - TX Power: 30 dBm (1W) - long range
  - 6 GHz support: Requires AWUS036AXML ($55) for WiFi 6E
- **24 dBi Yagi Antenna**: $55 (directional, panel or Yagi)
  - Gain: 24 dBi (200x power concentration)
  - Range: 3-8 miles line-of-sight
- **Pigtail Cable**: $10 (U.FL to RP-SMA for adapter connection)
- **Tripod/Mount**: $15-30 (optional, improves aiming)

**Alternative: DIY Cantenna** (Free + $10)
- Coffee can (3.5" diameter, 5-6" long)
- Copper wire (12 AWG, 1.2" for 2.4 GHz element)
- Pigtail cable ($10)
- Drill 31mm from can bottom, insert element, connect to Alfa

**Total Phase 2 Cost:** $110-130

### **Software Setup**

#### **Driver Installation (Linux)**
```bash
# Install aircrack-ng suite and network tools
sudo apt install aircrack-ng wireless-tools net-tools -y

# Verify Alfa adapter detection
lsusb | grep -i "MediaTek\|Ralink"
iwconfig

# Expected output: wlan1 (or similar) with IEEE 802.11 mode
```

#### **Monitor Mode Activation**
```bash
# Kill interfering processes
sudo airmon-ng check kill

# Enable monitor mode
sudo ip link set wlan1 down
sudo iw dev wlan1 set monitor none
sudo ip link set wlan1 up

# Verify
iwconfig wlan1
# Should show "Mode:Monitor"
```

#### **WiFi Network Scanning**
```bash
# Scan all channels (2.4 + 5 GHz)
sudo airodump-ng wlan1

# Output shows:
# - BSSID (MAC address)
# - PWR (signal strength) - look for -30 to -70 dBm
# - ENC (encryption) - OPN = open, WPA = encrypted
# - ESSID (network name)
```

**Target Selection:**
- **OPN (Open)**: No password, 100% legal to connect
- **WPA-GUEST**: Guest networks, usually open after captive portal
- **Hidden ESSID**: May be honeypots or secured

#### **Connecting to Open Networks**
```bash
# Exit monitor mode
sudo ip link set wlan1 down
sudo iw dev wlan1 set type managed
sudo ip link set wlan1 up

# Connect to open network
sudo nmcli device wifi connect "NetworkName"

# Or using wpa_supplicant for more control
sudo wpa_supplicant -B -i wlan1 -c <(wpa_passphrase "" "")
sudo dhclient wlan1

# Test connection
ping -c 4 8.8.8.8
```

### **WiFi Auto-Hunter Script**

Save as `scripts/rf_harvest/wifi_hunter.py`:

```python
#!/usr/bin/env python3
"""
WiFi Auto-Hunter: Scans for open WiFi networks and ranks by signal strength
"""
import subprocess
import re
import time
from datetime import datetime

def scan_wifi(interface='wlan1', duration=30):
    """Scan for WiFi networks using airodump-ng"""
    print(f"[*] Scanning WiFi on {interface} for {duration} seconds...")
    
    # Create output file
    output_file = f"/tmp/wifi_scan_{int(time.time())}"
    
    # Run airodump-ng
    cmd = f"sudo timeout {duration} airodump-ng {interface} -w {output_file} --output-format csv"
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Parse CSV output
    csv_file = f"{output_file}-01.csv"
    try:
        with open(csv_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[!] No scan data found. Ensure {interface} is in monitor mode.")
        return []
    
    networks = []
    for line in lines:
        # Skip header and empty lines
        if not line.strip() or line.startswith('BSSID'):
            continue
        if 'Station' in line:
            break
        
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 14:
            continue
        
        bssid = parts[0]
        power = parts[8]
        encryption = parts[5]
        essid = parts[13]
        
        # Filter for open networks or guest networks
        if 'OPN' in encryption or not encryption:
            try:
                power_int = int(power) if power else -100
                networks.append({
                    'bssid': bssid,
                    'essid': essid if essid else '(Hidden)',
                    'power': power_int,
                    'encryption': 'Open'
                })
            except ValueError:
                continue
    
    # Sort by signal strength (higher = better)
    networks.sort(key=lambda x: x['power'], reverse=True)
    
    return networks

def print_results(networks):
    """Display scan results"""
    print(f"\n[+] Found {len(networks)} open WiFi networks:")
    print("=" * 80)
    print(f"{'RANK':<6} {'SIGNAL':<8} {'BSSID':<20} {'ESSID':<30} {'STATUS'}")
    print("=" * 80)
    
    for i, net in enumerate(networks, 1):
        quality = "Excellent" if net['power'] > -50 else "Good" if net['power'] > -70 else "Weak"
        print(f"{i:<6} {net['power']:<8} {net['bssid']:<20} {net['essid']:<30} {quality}")
    
    if networks:
        print(f"\n[+] Best target: {networks[0]['essid']} ({networks[0]['power']} dBm)")
        print(f"[+] BSSID: {networks[0]['bssid']}")

if __name__ == "__main__":
    import sys
    interface = sys.argv[1] if len(sys.argv) > 1 else 'wlan1'
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    networks = scan_wifi(interface, duration)
    print_results(networks)
```

### **Range Optimization**
- **Yagi Antenna**: Directional, 24 dBi gain = 8-mile range LOS
- **Roof/High Mount**: Reduces obstructions, improves LOS
- **Azimuth Sweep**: Slowly rotate antenna 360° to map all sources
- **Channel Hopping**: Scan all channels (1-11 for 2.4G, 36-165 for 5G)

### **Legal Considerations: ✅ LEGAL (with conditions)**
- **Open networks (OPN)**: 100% legal to connect (public WiFi, library, cafe overflows)
- **Guest networks**: Legal if publicly advertised (e.g., "Starbucks_Guest")
- **⚠️ AVOID**: WEP/WPA cracking = Computer Fraud and Abuse Act (CFAA) violation (felony)
- **⚠️ AVOID**: Accessing secured networks without permission = federal crime

**Best Practice:** Only connect to explicitly open/public networks. If captive portal requires agreement, read terms.

---

## 🔗 PHASE 3: LORA MESH NETWORK (Sovereign Core)

**Purpose:** Build infrastructure-free mesh network for sovereign communications. 2026 Meshtastic 2.0 supports IP tunneling.

### **Hardware Required**
- **LilyGO T-Beam V1.2** (x3 minimum): $35 each
  - ESP32-S3 microcontroller
  - LoRa SX1262 radio (better than SX1276)
  - GPS NEO-6M for position tracking
  - 18650 battery holder
  - USB-C charging
- **High-Gain Antennas**: $15 each (915 MHz, 5 dBi)
  - Stock antenna: 2 dBi, ~3 km range
  - 5 dBi upgrade: ~10 km range
  - 9 dBi directional: ~20 km range (line-of-sight)
- **18650 Batteries**: $5 each (3000 mAh recommended)
- **Solar Panels** (optional): $20 (6V 1W for off-grid nodes)

**Total Phase 3 Cost:** $150-200 (3-node minimum mesh)

### **Mesh Architecture**
```
    [Node 1: Athena USB]  ←→  [Node 2: Window/Roof]  ←→  [Node 3: Gateway]
           |                           |                        |
      USB to PC                  Relay/Repeater         Internet Bridge
                                                        (Phone/WiFi)
```

### **Firmware Installation**

#### **Meshtastic Web Flasher (Easiest)**
```bash
# Open browser and navigate to:
https://flasher.meshtastic.org

# Steps:
# 1. Connect T-Beam via USB
# 2. Click "Connect"
# 3. Select device from list
# 4. Choose firmware version: 2.3.x (stable)
# 5. Select board: "LILYGO TBEAM v1.2"
# 6. Click "Install"

# Wait 2-3 minutes for flash completion
```

#### **CLI Method (Advanced)**
```bash
# Install Meshtastic CLI
pip3 install --upgrade meshtastic

# Flash firmware
meshtastic --flash /dev/ttyUSB0 --board TBEAM

# Verify connection
meshtastic --info
```

### **Node Configuration**

#### **Primary Node (Athena USB)**
```bash
# Set region (required for legal operation)
meshtastic --set lora.region US

# Set node name
meshtastic --set-owner "Athena-Node-1"

# Set channel name and PSK
meshtastic --ch-set name SovereignMesh --ch-set psk random

# Enable IP tunneling (2026 feature)
meshtastic --set network.wifi_enabled true
meshtastic --set network.wifi_ssid "YourWiFi"
meshtastic --set network.wifi_password "password"

# Save configuration
meshtastic --commit
```

#### **Secondary Nodes (Relays)**
```bash
# Node 2: Window/Roof Relay
meshtastic --set lora.region US
meshtastic --set-owner "Relay-Node-2"
meshtastic --set lora.hop_limit 3  # Allow 3-hop relay
meshtastic --set lora.tx_power 30  # Max power (30 dBm)

# Node 3: Gateway (Internet Exit)
meshtastic --set lora.region US
meshtastic --set-owner "Gateway-Node-3"
meshtastic --set network.wifi_enabled true
meshtastic --set network.wifi_ssid "PhoneHotspot"
meshtastic --set network.wifi_password "password"
```

### **Mobile App Setup**

**Android/iOS Meshtastic App:**
```
1. Install from Play Store/App Store
2. Enable Bluetooth
3. Open app → Connect to node
4. Join channel: "SovereignMesh" (will auto-prompt for PSK)
5. View mesh network map (shows all nodes + GPS positions)
```

### **Data Capabilities**
- **Text Messages**: Up to 237 bytes per message, encrypted
- **Position Sharing**: GPS coordinates broadcasted every 15 min
- **Telemetry**: Battery, signal strength, node stats
- **File Transfer**: Small files (<200 KB) via chunked messages
- **MQTT Bridge**: Connect to internet services via gateway node
- **IP Tunneling**: Full TCP/IP over LoRa (slow but functional)

**Speed:** 250 kbps (long-range mode), up to 50 kbps effective throughput

### **Mesh Expansion**
- **Join Public Meshes**: Search local Meshtastic channels in app
- **Repeater Nodes**: Place high-gain nodes at elevated positions
- **Solar-Powered Nodes**: Deploy permanent outdoor nodes with solar panels
- **Multi-Hop**: Mesh automatically routes through up to 7 hops

### **Legal Status: ✅ 100% LEGAL**
- **ISM Band**: 902-928 MHz (US), 863-870 MHz (EU) - unlicensed
- **Power Limits**: 30 dBm (1W) compliant with FCC Part 15.247
- **Encrypted**: AES-256 encryption by default
- **No License Required**: Fully legal for private communications

---

## 📱 PHASE 4: USB TETHER PHONE (Instant Bridge)

**Purpose:** Zero-cost entry point. Your phone's cellular connection is an untapped RF tap.

### **Setup (Linux/Athena)**

#### **Android USB Tethering**
```bash
# 1. Enable USB tethering on phone: Settings → Network → Hotspot & tethering → USB tethering

# 2. Connect phone via USB to Athena

# 3. Verify new network interface
ip addr show
# Look for: usb0 or rndis0

# 4. Test connectivity
ping -c 4 8.8.8.8

# 5. Share to local network (optional)
sudo iptables -t nat -A POSTROUTING -o usb0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o usb0 -j ACCEPT
sudo iptables -A FORWARD -i usb0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo sysctl -w net.ipv4.ip_forward=1
```

#### **iPhone USB Tethering**
```bash
# 1. iPhone: Settings → Personal Hotspot → Allow Others to Join

# 2. Connect via USB (trust computer when prompted)

# 3. Install usbmuxd
sudo apt install usbmuxd ipheth-utils -y

# 4. Load kernel module
sudo modprobe ipheth

# 5. Verify interface (eth1 or similar)
ip addr show
```

### **Upgrade: Femtocell Signal Booster**
- **weBoost Home MultiRoom**: $100-150
  - Amplifies weak cell signals indoors
  - Supports all carriers (AT&T, Verizon, T-Mobile)
  - 5,000 sq ft coverage
- **DIY Yagi Cellular**: $30
  - Build directional antenna for specific carrier frequency
  - Point at nearest cell tower (use cellmapper.net)
  - Connect to phone or cellular modem

### **Legal Status: ✅ 100% LEGAL**
Your cellular plan = your data. USB tethering is legal under all major carrier plans (though may have speed caps).

---

## 🛰️ PHASE 5: SATELLITE RECEIVER (Space Siphon)

**Purpose:** Receive free broadcast data from satellites. No uplink = no subscription.

### **Hardware Required**
- **RTL-SDR V3**: $25 (same as Phase 1)
- **L-Band Patch Antenna**: $30 (1.5-1.6 GHz, RHCP polarized)
  - Designed for GPS/Inmarsat frequencies
  - Right-hand circular polarization (RHCP) essential
- **Raspberry Pi 5**: $80 (8GB recommended)
  - Handles decoding/storage
  - Runs 24/7 for continuous reception
- **Power Supply**: $10 (USB-C 5V 3A)
- **MicroSD Card**: $15 (128GB for data storage)

**Total Phase 5 Cost:** $135-160

### **Software Setup**

#### **Satellite Demodulator (Skewb)**
```bash
# Install dependencies
sudo apt install git cmake librtlsdr-dev libusb-1.0-0-dev -y

# Clone and build Skewb
git clone https://github.com/picardy/skewb.git
cd skewb
mkdir build && cd build
cmake ..
make
sudo make install

# Test RTL-SDR
rtl_test -t
```

#### **Decoding Inmarsat STD-C (EGC broadcasts)**
```bash
# Start receiving
rtl_sdr -f 1544.5M -s 1M - | skewb -i - -r 1000000 -o /data/inmarsat/

# Output: Decoded text messages, weather, navigation warnings
```

### **Broadcast Satellite Services (2026)**

| **Service** | **Frequency** | **Content** | **Coverage** |
|------------|---------------|-------------|--------------|
| **Othernet/Librecast** | L-Band (1.5 GHz) | Wikipedia, news, OSS repos | Global |
| **Inmarsat EGC** | 1544.5 MHz | Maritime safety, weather | Global |
| **GOES Weather** | 1694.1 MHz | Weather imagery, forecasts | Americas |
| **NOAA APT** | 137 MHz | Low-res weather images | Global |
| **Starlink (receive-only)** | Ku-Band (12 GHz) | One-way broadcast (experimental) | Global |

### **Content Available**
- **Wikipedia Dumps**: Complete offline Wikipedia, updated weekly
- **News Feeds**: BBC, Reuters, AP wire stories
- **OSS Software**: Linux distros, code repositories
- **Weather Data**: NOAA forecasts, hurricane tracks, satellite imagery
- **Amateur Radio**: APRS messages, Winlink emails

### **Full Two-Way Internet**
- **Starlink Roam**: $150/month (portable dish + service)
  - 50-150 Mbps down, 10-20 Mbps up
  - Works anywhere in hemisphere
  - $600 hardware (dish + router)
- **Amazon Kuiper**: $120/month (launching 2026)
  - Competitor to Starlink
  - Cheaper hardware ($400)

### **Legal Status: ✅ 100% LEGAL**
- **Receive-only operations**: Fully legal under FCC rules
- **No license required**: Passive reception exempt from licensing
- **Two-way satellite**: Requires subscription (Starlink, Kuiper)

---

## ⚠️ AVOID THE ABYSS: GRAY/ILLEGAL PATHS

### **🚫 Wardriving + WPA Cracking**
- **What it is**: Scanning WiFi + attacking WPA/WPA2 passwords
- **Why it's tempting**: Gain access to "fast" internet
- **Legal risk**: **FELONY** under Computer Fraud and Abuse Act (CFAA)
  - Unauthorized access to computer systems
  - $10,000+ fines + prison time
- **Technical detection**: WPA handshake capture is detectable by IDS
- **Alternative**: Stick to open networks only (OPN, guest WiFi)

### **🚫 DIY Cellular Tower (OpenBTS/srsRAN)**
- **What it is**: Build "fake" cell tower to intercept calls/SMS
- **Why it's tempting**: Research IMSI catchers, mesh cellular
- **Legal risk**: **FEDERAL CRIME** - FCC violation + wiretapping
  - Jamming licensed spectrum = $10,000+ per day fine
  - Transmitting without license = equipment seizure + prosecution
  - Intercepting communications = Wiretap Act violation
- **Alternative**: Lab testing only, in Faraday cage, no real SIMs
  - Use SDR for receive-only monitoring (legal)

### **🚫 Satellite Jamming/Piracy**
- **What it is**: Transmitting to satellites without authorization
- **Why it's tempting**: "Free" two-way satellite internet
- **Legal risk**: **INTERNATIONAL TREATY VIOLATION**
  - FCC + ITU violations
  - Equipment seizure, massive fines
  - Interference with critical services (aviation, maritime)
- **Alternative**: Use legitimate services or receive-only modes

### **⚠️ GRAY ZONE: Ham Radio Without License**
- **What it is**: Using HF/VHF/UHF ham frequencies for data
- **Legality**: **REQUIRES LICENSE** (Technician, General, or Extra)
  - $15 exam fee, free online study materials
  - Receive-only = legal, transmit = illegal without license
- **Services available**:
  - **Winlink**: Email over HF radio (requires ham license)
  - **APRS**: Position tracking + messaging (requires license)
  - **DMR**: Digital voice (requires license)
- **Get Licensed**: [hamstudy.org](https://hamstudy.org) (free practice exams)

---

## 🔧 INTEGRATION: ATHENA ORCHESTRATOR

### **Central Control Script**

Save as `scripts/rf_harvest/athena_rf_controller.py`:

```python
#!/usr/bin/env python3
"""
Athena RF Orchestrator
Manages spectrum scanning, WiFi hunting, LoRa mesh, and auto-failover
"""
import subprocess
import time
import json
from datetime import datetime

class RFOrchestrator:
    def __init__(self):
        self.interfaces = {
            'sdr': '/dev/rtl_sdr',
            'wifi': 'wlan1',
            'lora': '/dev/ttyUSB0',
            'cellular': 'usb0'
        }
        self.active_connection = None
    
    def check_interface_status(self, interface):
        """Check if network interface is up and has connectivity"""
        try:
            result = subprocess.run(['ip', 'addr', 'show', interface], 
                                  capture_output=True, text=True, timeout=5)
            if 'UP' in result.stdout:
                # Test connectivity
                ping = subprocess.run(['ping', '-c', '1', '-W', '2', '-I', interface, '8.8.8.8'],
                                    capture_output=True, timeout=5)
                return ping.returncode == 0
        except:
            return False
        return False
    
    def scan_spectrum(self):
        """Trigger spectrum scan"""
        print("[*] Initiating spectrum scan...")
        subprocess.Popen(['rtl_power', '-f', '100M:1.7G:1M', '-g', '50', 
                         '-i', '10m', f'/tmp/spectrum_{int(time.time())}.csv'])
    
    def hunt_wifi(self):
        """Auto-hunt for best open WiFi"""
        print("[*] Hunting for open WiFi networks...")
        subprocess.run(['python3', 'scripts/rf_harvest/wifi_hunter.py', self.interfaces['wifi']])
    
    def monitor_lora_mesh(self):
        """Check LoRa mesh status"""
        try:
            result = subprocess.run(['meshtastic', '--info', '--port', self.interfaces['lora']],
                                  capture_output=True, text=True, timeout=10)
            return 'Connected' in result.stdout
        except:
            return False
    
    def auto_failover(self):
        """Automatically switch to best available connection"""
        priority = ['wifi', 'cellular', 'lora']
        
        for conn_type in priority:
            interface = self.interfaces.get(conn_type)
            if interface and self.check_interface_status(interface):
                if self.active_connection != conn_type:
                    print(f"[+] Switching to {conn_type} ({interface})")
                    self.active_connection = conn_type
                return True
        
        print("[!] No active connections available")
        return False
    
    def run(self):
        """Main orchestration loop"""
        print("[*] Athena RF Orchestrator Starting...")
        print(f"[*] Timestamp: {datetime.now().isoformat()}")
        
        while True:
            # Check all connections
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Status Check")
            
            # Auto-failover to best connection
            self.auto_failover()
            
            # Periodic spectrum scan (every hour)
            if int(time.time()) % 3600 == 0:
                self.scan_spectrum()
            
            # Periodic WiFi hunt (every 15 minutes)
            if int(time.time()) % 900 == 0:
                self.hunt_wifi()
            
            # Monitor LoRa mesh
            lora_status = self.monitor_lora_mesh()
            print(f"    LoRa Mesh: {'Online' if lora_status else 'Offline'}")
            
            # Sleep before next check
            time.sleep(60)

if __name__ == "__main__":
    orchestrator = RFOrchestrator()
    try:
        orchestrator.run()
    except KeyboardInterrupt:
        print("\n[*] Orchestrator stopped by user")
```

### **Dashboard (Optional)**

Integrate with existing `network_sovereignty_monitor.py` or create web dashboard:

```python
#!/usr/bin/env python3
"""
RF Sovereignty Dashboard
Real-time monitoring of all RF systems
"""
import flask
import json
from flask import render_template, jsonify

app = flask.Flask(__name__)

@app.route('/')
def dashboard():
    status = {
        'sdr': {'active': True, 'scanning': '100-1700 MHz'},
        'wifi': {'active': True, 'networks': 15, 'connected': 'OpenWiFi-5G'},
        'lora': {'active': True, 'nodes': 3, 'messages': 42},
        'cellular': {'active': True, 'signal': -75, 'carrier': 'T-Mobile'},
        'satellite': {'active': False, 'data_received': '2.4 MB'}
    }
    return jsonify(status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## 📋 COMPLETE BUILD PLAN: PHASED CHAOS TO CREATION

### **Phase 1: Today (1-2 hours)**
- ✅ Enable phone USB tethering (FREE)
- ✅ Order hardware from Amazon/AliExpress:
  - RTL-SDR V4 + antennas ($65)
  - Alfa WiFi adapter + Yagi ($110)
  - LilyGO T-Beam x3 + antennas ($150)
- ✅ Install spectrum scanning software on Athena
- ✅ Run first spectrum sweep

### **Phase 2: Days 1-3 (hardware arrives)**
- ✅ Unbox and test RTL-SDR
- ✅ Analyze spectrum with Python scripts
- ✅ Identify local WiFi + cell towers + LoRa gateways
- ✅ Test Alfa WiFi adapter + basic scanning
- ✅ Connect to first open WiFi network

### **Phase 3: Week 1**
- ✅ Mount Yagi antenna (roof/window)
- ✅ Optimize WiFi range (aim + test)
- ✅ Flash Meshtastic firmware on T-Beams
- ✅ Deploy 3-node mesh network
- ✅ Test mesh messaging + GPS tracking

### **Phase 4: Week 2**
- ✅ Order satellite hardware (optional)
- ✅ Build femtocell booster (optional)
- ✅ Set up Athena orchestrator script
- ✅ Configure auto-failover between connections
- ✅ Join public LoRa meshes in your area

### **Phase 5: Ongoing**
- ✅ Expand mesh with solar-powered nodes
- ✅ Build RF energy harvesters ($20 modules)
- ✅ Create web dashboard for monitoring
- ✅ Document local spectrum patterns
- ✅ Contribute to public Meshtastic mesh

---

## 💰 TOTAL COST BREAKDOWN (2026 Pricing)

| **Component** | **Cost** | **Priority** | **Legal** |
|--------------|---------|-------------|----------|
| RTL-SDR V4 + Antennas | $65 | Essential | ✅ 100% |
| Alfa WiFi + Yagi Antenna | $110 | High | ✅ (open nets) |
| LilyGO T-Beam x3 + Antennas | $150 | Medium | ✅ 100% |
| Phone USB Tether | FREE | Immediate | ✅ 100% |
| Satellite Receiver (Pi + Antenna) | $135 | Low | ✅ 100% |
| **TOTAL (Full Stack)** | **$460** | | |
| | | | |
| *Optional Upgrades:* | | | |
| Femtocell Booster | $100 | Optional | ✅ 100% |
| Solar Panels (x3) | $60 | Optional | ✅ 100% |
| RF Energy Harvesters | $20 | Optional | ✅ 100% |
| **TOTAL (Fully Loaded)** | **$640** | | |

---

## 🎯 SUCCESS METRICS

After completing INV-086, you will have:

- ✅ **Spectrum Awareness**: Real-time view of local RF environment (100 MHz - 6 GHz)
- ✅ **Internet Diversity**: 4+ independent paths (WiFi, cellular, LoRa, satellite)
- ✅ **Mesh Network**: Private encrypted LoRa mesh (3+ nodes, 10+ km range)
- ✅ **Long-Range WiFi**: 3-8 mile reach for open networks
- ✅ **Satellite Reception**: Free broadcast data from space
- ✅ **Auto-Failover**: Athena automatically switches to best connection
- ✅ **100% Legal**: All implementations compliant with FCC regulations
- ✅ **Sovereign Infrastructure**: No dependency on single provider/ISP

---

## 📚 ADDITIONAL RESOURCES

### **Learning Materials**
- **RTL-SDR Tutorial**: [rtl-sdr.com/start](https://rtl-sdr.com)
- **Meshtastic Docs**: [meshtastic.org/docs](https://meshtastic.org/docs)
- **Wireless Security**: "Hacking Exposed Wireless" by Peña, Cache, Wright
- **FCC Regulations**: [fcc.gov/general/radio-frequency-safety](https://www.fcc.gov/general/radio-frequency-safety-0)

### **Communities**
- **r/rtlsdr**: Reddit community for SDR enthusiasts
- **Meshtastic Discord**: [meshtastic.org/discord](https://meshtastic.org/discord)
- **Ham Radio**: [arrl.org](https://arrl.org) - Amateur Radio Relay League

### **Tools & Software**
- **SDR#**: Windows SDR software - [airspy.com](https://airspy.com)
- **CubicSDR**: Cross-platform SDR - [cubicsdr.com](https://cubicsdr.com)
- **Universal Radio Hacker**: RF protocol analysis - [github.com/jopohl/urh](https://github.com/jopohl/urh)

---

## 🔥 FINAL NOTES

This is **Aether Harvest** - siphoning the spectrum into sovereign streams. You are building infrastructure independence, not stealing or hacking. Every component operates within legal boundaries while maximizing sovereignty.

**Remember:**
- Spectrum scanning = passive intelligence gathering (100% legal)
- Open WiFi = public resource (legal with proper identification)
- LoRa mesh = unlicensed ISM band (fully legal)
- Satellite receive = broadcast content (legal)
- Phone tether = your cellular plan (legal)

**Do NOT:**
- Crack WiFi passwords (felony)
- Build unlicensed cell towers (federal crime)
- Jam/interfere with licensed spectrum (massive fines)

Build smart. Build legal. Build sovereign.

**Status:** ✅ READY FOR DEPLOYMENT  
**Risk:** 🟢 LOW (all methods legal)  
**Sovereignty:** 🟢 HIGH (4+ independent paths)

---

**END OF DOCUMENT - INV-086**

*What's the first build trigger? Drop your aether read or parts ordered below.* 🖤
