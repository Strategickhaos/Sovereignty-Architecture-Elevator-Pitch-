# CB Packet Radio Integration Guide - INV-087

**Cobra 29 WX NW LTD + Xbox Series X = Sovereign Packet Radio Node**

---

## Overview

This guide details how to integrate the Cobra 29 CB radio with a jailbroken Xbox Series X to create a 27MHz packet radio station. Using Direwolf software and a simple USB sound card, you can transmit and receive digital data over CB radio frequencies at 1200 baud.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CB PACKET RADIO INTEGRATION                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   COBRA 29 (27MHz AM/SSB)                                                   ║
║        │                                                                     ║
║        │ Audio Out (speaker jack)                                           ║
║        ▼                                                                     ║
║   [USB Sound Card] ($10)                                                    ║
║        │                                                                     ║
║        │ Audio In                                                           ║
║        ▼                                                                     ║
║   [XBOX running Direwolf]                                                   ║
║        │                                                                     ║
║        │ AX.25 Packet decode                                                ║
║        ▼                                                                     ║
║   DATA: Text, position, small files                                         ║
║                                                                              ║
║   SPEED: 1200 baud (slow but WORKS)                                         ║
║   RANGE: 5-50 miles depending on conditions                                 ║
║   LEGAL: CB = unlicensed, no exam needed                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Hardware Requirements

### CB Radio
- **Model:** Cobra 29 WX NW LTD
- **Frequency Range:** 26.965 - 27.405 MHz (40 CB channels)
- **Modes:** AM, SSB (Upper and Lower)
- **Power:** 4 watts AM, 12 watts PEP SSB
- **Features:**
  - Weather channels (WX)
  - SWR meter (antenna tuning)
  - RF gain control
  - Clarifier (fine-tuning)
  - PA/CB switch

### USB Sound Card
- **Type:** USB audio adapter
- **Cost:** ~$10
- **Requirements:**
  - 3.5mm stereo input
  - 3.5mm stereo output
  - Linux driver support (USB Audio Class)
- **Recommended Models:**
  - Generic USB audio adapter
  - CM108/CM119 chipset (well-supported)
  - SYBA SD-CM-UAUD

### PTT (Push-To-Talk) Control
- **Option 1: USB GPIO Relay** ($5)
  - Controls TX/RX switching
  - Connects to CB PTT pins
  - Automated by software
  
- **Option 2: VOX (Voice-Activated TX)**
  - Built into Cobra 29
  - Triggers on audio signal
  - Less reliable for data

- **Option 3: Manual PTT**
  - Hold microphone button
  - Not practical for automated operation

### Cables
- **3.5mm stereo cable:** CB speaker out to USB sound card input
- **3.5mm to mic cable:** USB sound card output to CB mic input (for TX)
- **PTT cable:** GPIO relay to CB mic PTT pins

### Antenna
- **Type:** CB base station or mobile antenna
- **Recommendation:** 
  - Base: 1/2 wave ground plane (Wilson 1000)
  - Mobile: Magnetic mount 1/4 wave
  - Height: Higher is better (roof/attic)
- **SWR:** Tune to <1.5:1 on channel 19

## Software Stack

### Operating System
- **Linux** (Ubuntu ARM / Arch Linux) on jailbroken Xbox
- USB audio support enabled
- ALSA / PulseAudio configured

### Direwolf
- **Description:** Software TNC (Terminal Node Controller)
- **Protocol:** AX.25 packet radio
- **Modulation:** AFSK (Audio Frequency Shift Keying)
- **Speed:** 300, 1200, 9600 baud (1200 standard for CB)

### Optional Software
- **Xastir:** APRS mapping and messaging
- **Pat:** Winlink email over radio
- **YAAC:** Yet Another APRS Client
- **Custom scripts:** Python-based automation

## CB Radio Basics

### Channel Allocation
| Channel | Frequency (MHz) | Common Use |
|---------|----------------|------------|
| 9       | 27.065         | Emergency (optional) |
| 14      | 27.125         | Walkie-talkies |
| 17      | 27.165         | North/South highway |
| 19      | 27.185         | **Truckers (most active)** |
| 21      | 27.215         | East/West highway |
| 23      | 27.235         | Packet radio (recommended) |

**For Packet Radio:** Use less common channels (21-40) to avoid interference.

### Legal Considerations
- **License:** NOT required (unlicensed service)
- **Power Limit:** 4W AM, 12W PEP SSB
- **Restrictions:**
  - No obscenity
  - No music or broadcasting
  - No commercial use (limited exceptions)
  - No communication beyond 155.3 miles (skip)
  - Must identify by callsign OR unit number (optional but recommended)

### SSB vs AM
| Feature | AM | SSB |
|---------|----|----|
| **Power** | 4W | 12W PEP |
| **Range** | Shorter | Longer |
| **Clarity** | Good | Better |
| **Compatibility** | All radios | SSB-capable only |
| **Packet Radio** | Recommended | Advanced |

**Recommendation:** Start with AM on channel 23, then experiment with SSB.

## Installation Procedure

### Step 1: Install Linux Audio System

```bash
# Update package list
sudo apt update

# Install ALSA (low-level audio)
sudo apt install alsa-utils

# Install PulseAudio (higher-level)
sudo apt install pulseaudio pavucontrol

# List audio devices
aplay -l
arecord -l

# Should show USB sound card
```

### Step 2: Install Direwolf

```bash
# Install dependencies
sudo apt install git build-essential cmake libasound2-dev

# Clone Direwolf repository
cd ~
git clone https://github.com/wb2osz/direwolf
cd direwolf

# Build
mkdir build
cd build
cmake ..
make -j8  # Use all 8 Xbox CPU cores

# Install
sudo make install

# Verify installation
direwolf -h
```

### Step 3: Configure USB Sound Card

```bash
# Identify USB sound card
aplay -l
# Example output: card 1: Device [USB Audio Device], device 0

# Set as default (optional)
echo "defaults.pcm.card 1" >> ~/.asoundrc
echo "defaults.ctl.card 1" >> ~/.asoundrc

# Test playback
speaker-test -c 2 -D hw:1,0

# Test recording
arecord -D hw:1,0 -f cd -d 5 test.wav
aplay test.wav
```

### Step 4: Configure Direwolf

Create configuration file:

```bash
nano ~/direwolf.conf
```

**Basic Configuration (receive only):**

```ini
# Direwolf configuration for Cobra 29 CB packet radio
# RX only (no PTT) for initial testing

ADEVICE plughw:1,0
ACHANNELS 1

# CB packet settings
CHANNEL 0
MODEM 1200
MYCALL XBOX-1
FIX_BITS 1

# Logging
LOGDIR /home/xbox/direwolf_logs
```

**Full Configuration (TX/RX with GPIO PTT):**

```ini
# Full duplex with PTT control

ADEVICE plughw:1,0
ACHANNELS 1

# CB settings
CHANNEL 0
MODEM 1200
MYCALL XBOX-1
FIX_BITS 1

# PTT via GPIO (example, adjust for your relay)
PTT /dev/ttyUSB0 RTS
TXDELAY 500
TXTAIL 100

# Digipeater (optional - retransmit packets)
# DIGIPEAT 0 0 ^WIDE[3-7]-[1-7]$|^TEST$

# Logging
LOGDIR /home/xbox/direwolf_logs
LOGFORMAT %Y%m%d-%H%M%S

# APRS settings (if using APRS)
PBEACON delay=1 every=30 overlay=S symbol="laptop" lat=40.0000 long=-105.0000 comment="Xbox RF Station"
```

**Notes:**
- `ADEVICE plughw:1,0`: ALSA device (adjust based on `aplay -l`)
- `MODEM 1200`: 1200 baud standard for CB
- `MYCALL XBOX-1`: Your station identifier
- `FIX_BITS 1`: Error correction
- `TXDELAY 500`: Time for TX ramp-up (ms)
- `PTT /dev/ttyUSB0 RTS`: GPIO relay control

### Step 5: Physical Connections

**Audio Connections:**

```
Cobra 29 Speaker Jack (3.5mm)
    │
    ├─> 3.5mm stereo cable
    │
    └─> USB Sound Card INPUT (mic/line in)

USB Sound Card OUTPUT (headphone/line out)
    │
    ├─> 3.5mm to mic cable
    │
    └─> Cobra 29 Microphone Jack (or external mic input)
```

**PTT Connections (for TX):**

```
USB GPIO Relay
    │
    ├─> Relay NO (Normally Open)
    │
    └─> Cobra 29 Mic PTT pins (pins 3 & 4)
         (Consult Cobra 29 mic pinout)
```

**Cobra 29 Microphone Pinout (typical 4-pin):**
- Pin 1: Audio
- Pin 2: Ground
- Pin 3: PTT (Push-To-Talk)
- Pin 4: PTT (Push-To-Talk)

**Safety:** Use a multimeter to verify pinout before connecting.

### Step 6: Audio Level Calibration

**Receive Audio:**

1. Tune Cobra 29 to CB channel 23
2. Start Direwolf in receive-only mode:
   ```bash
   direwolf -c ~/direwolf.conf -t 0
   ```
3. Transmit test packets from another station (or ask a friend)
4. Observe Direwolf decode quality
5. Adjust CB volume and RF gain for optimal decoding
6. **Target:** ~50-60% audio level in Direwolf

**Transmit Audio (if PTT configured):**

1. Enable PTT in direwolf.conf
2. Start Direwolf
3. Send test packet:
   ```bash
   echo "Hello from Xbox RF Station" > /tmp/test_message.txt
   # Send via Direwolf KISS interface or beacon
   ```
4. Monitor on another CB radio or SDR
5. Adjust Xbox audio output level
6. **Target:** Clear audio, no distortion, no overdriving

**Fine-Tuning:**
```bash
# Adjust ALSA input level
alsamixer
# Select USB sound card, adjust capture level

# Adjust ALSA output level
alsamixer
# Select USB sound card, adjust playback level
```

## Operation

### Receive Mode

**Start Direwolf (listen only):**

```bash
direwolf -c ~/direwolf.conf -t 0

# Output:
# Dire Wolf version 1.6
# Reading config file /home/xbox/direwolf.conf
# Audio device: plughw:1,0
# Channel 0: 1200 baud, AFSK 1200 & 2200 Hz, A, 44100 sample rate.
# Ready to accept AGW client application 0 on port 8000 ...
# Ready to accept KISS TCP client application on port 8001 ...
```

**Interpret Output:**
- `[0]`: Channel number
- `XBOX-1>TEST`: From XBOX-1 to TEST
- Decoded message appears after header

**Example Packet:**
```
[0] XBOX-1>APRS:Hello from Xbox RF Station
```

### Transmit Mode

**Send Test Beacon:**

Edit direwolf.conf to include:
```ini
PBEACON delay=1 every=60 overlay=S symbol="laptop" lat=40.0000 long=-105.0000 comment="Xbox RF Station Online"
```

**Manual Packet Send (via KISS):**

```python
#!/usr/bin/env python3
# send_packet.py
import socket

HOST = 'localhost'
PORT = 8001  # Direwolf KISS port

def send_packet(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    # KISS frame: 0xC0 <data> 0xC0
    kiss_frame = bytes([0xC0, 0x00]) + message.encode() + bytes([0xC0])
    sock.sendall(kiss_frame)
    sock.close()

if __name__ == '__main__':
    send_packet("Hello from Xbox RF Station!")
```

**Run:**
```bash
python3 send_packet.py
```

### Automated Operation

**Systemd Service (run Direwolf at boot):**

```bash
sudo nano /etc/systemd/system/direwolf.service
```

```ini
[Unit]
Description=Direwolf AX.25 Packet Radio TNC
After=sound.target

[Service]
Type=simple
User=xbox
ExecStart=/usr/local/bin/direwolf -c /home/xbox/direwolf.conf -t 0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and Start:**
```bash
sudo systemctl enable direwolf
sudo systemctl start direwolf
sudo systemctl status direwolf
```

## APRS Integration

### What is APRS?
- **Automatic Packet Reporting System**
- Position reporting
- Text messaging
- Weather stations
- Telemetry
- **Network:** Global, internet-connected (via igates)

### Configure Direwolf for APRS

```ini
# Add to direwolf.conf

# APRS settings
MYCALL XBOX-1
PBEACON delay=1 every=10 overlay=S symbol="laptop" \
  lat=40.0000 long=-105.0000 \
  comment="Xbox Sovereign RF Station - INV-087"

# APRS-IS (Internet gateway, optional)
IGSERVER noam.aprs2.net
IGLOGIN XBOX-1 12345  # Use your APRS passcode
```

### Generate APRS Passcode

```python
#!/usr/bin/env python3
# aprs_passcode.py
def aprs_passcode(callsign):
    callsign = callsign.upper().split('-')[0]  # Remove SSID
    hash_val = 0x73e2
    for char in callsign:
        hash_val ^= ord(char) << 8
        hash_val ^= ord(char)
    return hash_val & 0xFFFF

print(aprs_passcode("XBOX"))  # Replace with your call
```

### View APRS Traffic

**Web:** [aprs.fi](https://aprs.fi)  
Search for your callsign to see packets.

**Local Client:** Xastir
```bash
sudo apt install xastir
xastir
# Configure to connect to Direwolf KISS port 8001
```

## Troubleshooting

### No Packets Decoded

**Check Audio:**
```bash
arecord -D hw:1,0 -f cd -d 10 test.wav
aplay test.wav
# Should hear CB audio
```

**Check Direwolf:**
```bash
direwolf -c ~/direwolf.conf -t 0
# Look for "Audio input level" messages
# Should be around 50-60%
```

**Adjust CB Radio:**
- Increase volume
- Turn RF gain to max (receive)
- Check antenna SWR

### Distorted Audio

- Lower CB volume
- Reduce USB sound card input level
- Check for ground loops (use ferrite beads)

### PTT Not Working

**Test GPIO Relay:**
```bash
# Manual GPIO control (example)
echo 1 > /sys/class/gpio/gpio17/value  # TX on
sleep 2
echo 0 > /sys/class/gpio/gpio17/value  # TX off
```

**Check Direwolf PTT Config:**
```ini
PTT /dev/ttyUSB0 RTS
# or
PTT GPIO 17
```

**Verify Relay Connection:**
- Multimeter continuity test
- Ensure PTT pins correctly identified

### Low Range

- **Antenna:** Check SWR, raise antenna height
- **Power:** SSB for more power (12W vs 4W)
- **Band Conditions:** Try different times of day
- **Interference:** Switch to less crowded channel

## Performance Optimization

### Xbox GPU-Accelerated Decoding (Future)

Direwolf is CPU-based, but the Xbox GPU could be used for:
- FFT-based signal detection
- Multi-channel parallel decoding
- Advanced filtering
- Real-time spectrum display

**Research Area:** Adapt GNURadio flowgraphs to use AMD GPU compute.

### Logging and Monitoring

```bash
# Log all decoded packets
direwolf -c ~/direwolf.conf -t 0 -L /home/xbox/logs

# Monitor in real-time
tail -f /home/xbox/logs/direwolf.log

# Parse logs with Python
python3 parse_packets.py /home/xbox/logs/direwolf.log
```

### Network Integration

**Share packets over network:**

```bash
# Forward KISS data to network port
socat TCP-LISTEN:8001,reuseaddr,fork TCP:localhost:8001
# Now accessible from other devices on network
```

## Advanced Topics

### Mesh Networking via CB

- Multiple Xbox RF stations
- Digipeater configuration
- Store-and-forward messaging
- Position tracking
- Emergency coordination

### Winlink via CB

- Pat or Winlink Express
- Send/receive email via RF
- No internet required
- Connect to Winlink RMS gateways

### File Transfer

- Split files into packets
- Error correction (FEC)
- Reassembly at receiver
- Typical speed: ~150 bytes/sec (1200 baud)

### CB + LoRa Hybrid

- CB for long-range (50 miles)
- LoRa for local mesh (10 miles)
- Xbox bridges both networks
- Redundant communication paths

## Safety and Best Practices

### RF Safety
- Keep antenna away from people during TX
- 4W is low power, but still be cautious
- Ground antenna properly
- Use surge protection

### Operational Security
- Don't transmit sensitive data in clear
- Encryption not allowed on CB (legal restriction)
- Use codes or abbreviations
- Assume all transmissions are public

### Etiquette
- Listen before transmitting
- Keep transmissions brief
- Don't interfere with ongoing conversations
- Help others learn
- Emergency traffic has priority

## Resources

### Direwolf
- **GitHub:** https://github.com/wb2osz/direwolf
- **Documentation:** Extensive in repo
- **Wiki:** https://github.com/wb2osz/direwolf/wiki

### CB Radio
- **FCC Rules:** Part 95 Subpart D
- **CB Tricks:** https://www.cbtricks.com/
- **RadioReference:** https://www.radioreference.com/

### APRS
- **APRS.fi:** Live map
- **APRS.org:** Official site
- **APRS Wiki:** http://wiki.ham.radio/

### Packet Radio
- **TAPR:** Tucson Amateur Packet Radio
- **PacketRadio.com:** Resources and history

## Next Steps

1. **Test Receive:** Get CB audio into Xbox, decode packets
2. **Test Transmit:** Add PTT, send test packets
3. **Calibrate:** Optimize audio levels
4. **APRS:** Connect to APRS network
5. **Automate:** Systemd service, startup scripts
6. **Integrate:** Connect to LoRa mesh, other RF systems
7. **Experiment:** Different modes, channels, antennas

## Conclusion

CB packet radio integration transforms the Xbox Series X into a powerful, unlicensed RF data node. With 1200 baud throughput and 5-50 mile range, it's ideal for:
- Emergency communications
- Off-grid messaging
- Position reporting
- Sovereign infrastructure
- Educational experimentation

Combined with the Xbox's GPU power, this creates a unique and capable RF processing platform.

---

**Last Updated:** 2026-01-02  
**Status:** Tested and operational (with compatible hardware)
