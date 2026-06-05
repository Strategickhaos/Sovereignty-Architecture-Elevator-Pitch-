# 🔥 RF Harvest Scripts - INV-086

This directory contains automation scripts for the RF Spectrum Harvest (INV-086) project.

## 📁 Contents

### **Spectrum Analysis**
- `spectrum_analyzer.py` - Analyzes RTL-SDR spectrum scans and generates visualizations
- `sdr_config.ini` - Configuration file for RTL-SDR operations

### **WiFi Operations**
- `wifi_hunter.py` - Automated open WiFi network discovery and ranking

### **Mesh Networking**
- `meshtastic_config.ini` - Configuration template for LoRa mesh nodes

### **System Orchestration**
- `athena_rf_controller.py` - Central RF orchestrator with auto-failover

---

## 🚀 Quick Start

### **Prerequisites**

Install required packages:

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install rtl-sdr gqrx-sdr aircrack-ng python3-pip -y

# Python packages
pip3 install pandas matplotlib numpy
```

For Meshtastic (optional):
```bash
pip3 install meshtastic
```

### **Usage Examples**

#### **1. Spectrum Scanning**

```bash
# Capture spectrum data (10 minutes)
rtl_power -f 100M:1.7G:1M -g 50 -i 10m spectrum_scan.csv

# Analyze and visualize
python3 spectrum_analyzer.py spectrum_scan.csv
```

#### **2. WiFi Hunting**

```bash
# Put adapter in monitor mode
sudo ip link set wlan1 down
sudo iw dev wlan1 set monitor none
sudo ip link set wlan1 up

# Scan for open networks (30 seconds)
python3 wifi_hunter.py wlan1 30
```

#### **3. RF Orchestrator**

```bash
# Start the orchestrator (requires root)
sudo python3 athena_rf_controller.py
```

---

## ⚙️ Configuration

### **SDR Configuration**

Edit `sdr_config.ini` to customize:
- Frequency ranges
- Gain settings
- Output directories
- Visualization options

### **Meshtastic Configuration**

Edit `meshtastic_config.ini` for your mesh network:
- Region (US, EU, etc.)
- Channel name and encryption
- Power settings
- Position broadcast intervals

Apply configuration to device:
```bash
# Set region (REQUIRED)
meshtastic --set lora.region US

# Set node name
meshtastic --set-owner "YourNodeName"

# Set channel
meshtastic --ch-set name YourChannel --ch-set psk random
```

---

## 🔒 Security & Legal

**IMPORTANT:** All scripts are designed for legal operations only.

- ✅ Spectrum scanning (receive-only) is legal
- ✅ Connecting to open WiFi networks is legal
- ✅ LoRa mesh on ISM bands is legal
- 🚫 WPA cracking is illegal
- 🚫 Unauthorized network access is illegal

See `../RF_LEGAL_DISCLAIMER.md` for complete legal information.

---

## 🐛 Troubleshooting

### **RTL-SDR Not Detected**

```bash
# Check USB connection
lsusb | grep Realtek

# Test device
rtl_test -t

# If conflict with DVB drivers
sudo rmmod dvb_usb_rtl28xxu
```

### **WiFi Adapter Issues**

```bash
# Check adapter
iwconfig

# Install drivers (if needed)
sudo apt install firmware-realtek

# Kill conflicting processes
sudo airmon-ng check kill
```

### **Permission Errors**

Most RF operations require root:
```bash
sudo python3 script_name.py
```

Or add user to dialout group:
```bash
sudo usermod -aG dialout $USER
# Log out and back in
```

---

## 📊 Output Files

Scripts generate various output files:

| **File** | **Location** | **Description** |
|----------|--------------|-----------------|
| `spectrum_*.csv` | `/tmp/` | Raw spectrum scan data |
| `spectrum_*_plot.png` | Same as CSV | Spectrum visualization |
| `wifi_scan_*.csv` | `/tmp/` | WiFi scan results |

---

## 🔧 Advanced Usage

### **Continuous Spectrum Monitoring**

```bash
# 24-hour continuous scan (1-hour bins)
rtl_power -f 100M:1.7G:100k -g 40 -i 1h -e 24h daily_spectrum.csv &

# Analyze each hour
watch -n 3600 'python3 spectrum_analyzer.py /path/to/latest.csv'
```

### **Automated WiFi Connection**

```bash
# Exit monitor mode
sudo ip link set wlan1 down
sudo iw dev wlan1 set type managed
sudo ip link set wlan1 up

# Connect to best network
BEST_SSID=$(python3 wifi_hunter.py wlan1 30 | grep "Best target" | cut -d: -f2 | cut -d'(' -f1 | xargs)
sudo nmcli device wifi connect "$BEST_SSID"
```

### **Orchestrator as Systemd Service**

Create `/etc/systemd/system/rf-orchestrator.service`:

```ini
[Unit]
Description=RF Spectrum Orchestrator
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/rf_harvest
ExecStart=/usr/bin/python3 /opt/rf_harvest/athena_rf_controller.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable rf-orchestrator
sudo systemctl start rf-orchestrator
```

---

## 🤝 Contributing

Improvements welcome! Focus areas:
- Additional spectrum analysis algorithms
- Better signal classification
- Auto-failover optimizations
- Dashboard integration

---

## 📚 Resources

- **RTL-SDR Blog:** https://rtl-sdr.com
- **Meshtastic Docs:** https://meshtastic.org/docs
- **Aircrack-ng Wiki:** https://aircrack-ng.org
- **FCC Regulations:** https://fcc.gov

---

## 📄 License

Part of the Sovereignty Architecture project. Use responsibly and legally.

**Last Updated:** 2026-01-02
