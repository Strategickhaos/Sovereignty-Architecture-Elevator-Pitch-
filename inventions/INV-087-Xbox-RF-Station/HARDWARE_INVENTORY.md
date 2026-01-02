# Hardware Inventory - INV-087 Xbox RF Station

**Current Status:** BUILD IN PROGRESS  
**Last Updated:** 2026-01-02

---

## Core Components

### Compute Platform

| Item | Model | Status | Purpose | Notes |
|------|-------|--------|---------|-------|
| **Xbox Series X** | Microsoft Xbox Series X | ✅ OWNED | Main compute node | 12 TFLOPS GPU, 8-core Zen 2, 16GB RAM |
| **Power Cable** | Included | ✅ OWNED | Xbox power | |
| **HDMI Cable** | Standard | ✅ OWNED | Display output | |

**Specifications:**
- **CPU:** AMD Zen 2 @ 3.8 GHz (8 cores, 16 threads)
- **GPU:** AMD RDNA 2 @ 1.825 GHz (52 CUs, 12.15 TFLOPS)
- **RAM:** 16GB GDDR6
- **Storage:** 1TB NVMe SSD (internal)
- **Power:** ~150W typical, 315W max

### RF Hardware

#### CB Radio

| Item | Model | Status | Purpose | Price |
|------|-------|--------|---------|-------|
| **CB Transceiver** | Cobra 29 WX NW LTD | ✅ OWNED | 27MHz TX/RX | Owned |
| **CB Antenna** | TBD (1/4 or 1/2 wave) | ❌ NEEDED | RF transmission | $20-100 |
| **Coax Cable** | RG-58 or RG-8X | ❌ NEEDED | Antenna connection | $10-30 |
| **SWR Meter** | Built into Cobra 29 | ✅ OWNED | Antenna tuning | Included |

**Cobra 29 Specifications:**
- **Frequency:** 26.965-27.405 MHz (40 CB channels)
- **Modes:** AM, SSB (USB/LSB)
- **Power:** 4W AM, 12W PEP SSB
- **Features:** Weather channels, RF gain, SWR meter, PA mode

#### SDR (Software Defined Radio)

| Item | Model | Status | Purpose | Price |
|------|-------|--------|---------|-------|
| **RTL-SDR** | RTL-SDR V4 (white box?) | ⚠️ VERIFY | Spectrum scanning | Owned? |
| **SDR Antenna** | Dipole/discone | ❌ NEEDED | Wide-band receive | $20-50 |
| **SMA Adapter** | Varies | ❌ NEEDED | Antenna connection | $5-10 |

**RTL-SDR V4 Specifications:**
- **Frequency Range:** 24 MHz - 1.7 GHz
- **Bandwidth:** Up to 3.2 MHz
- **ADC:** 8-bit
- **Interface:** USB 2.0
- **Purpose:** Passive receive only (legal)

#### WiFi

| Item | Model | Status | Purpose | Price |
|------|-------|--------|---------|-------|
| **WiFi Adapter** | Alfa AWUS036ACH (or similar) | ❌ NEEDED | Long-range WiFi | $40-60 |
| **Antenna** | High-gain directional | ❌ NEEDED | Extended range | $20-40 |

**Alfa Specifications (typical):**
- **Bands:** 2.4 GHz, 5 GHz
- **Standards:** 802.11a/b/g/n/ac
- **TX Power:** High (check local regulations)
- **Interface:** USB 3.0

#### LoRa

| Item | Model | Status | Purpose | Price |
|------|-------|--------|---------|-------|
| **LoRa Node** | T-Beam or Heltec | ❌ NEEDED | Mesh networking | $30-50 |
| **LoRa Antenna** | 900MHz whip | Usually included | LoRa TX/RX | N/A |

**LoRa Specifications:**
- **Frequency:** 900 MHz (US) / 868 MHz (EU)
- **Range:** 1-10 miles per hop
- **Speed:** 0.3-37.5 kbps (varies)
- **Protocol:** Meshtastic

### Audio Interface

| Item | Model | Status | Purpose | Price |
|------|-------|--------|---------|-------|
| **USB Sound Card** | Generic CM108/CM119 | ❌ NEEDED | CB audio interface | $10 |
| **Audio Cable (3.5mm)** | Stereo male-male | ❌ NEEDED | CB speaker to sound card | $5 |
| **Mic Cable (3.5mm)** | Custom or adapter | ❌ NEEDED | Sound card to CB mic | $5-10 |

**USB Sound Card Requirements:**
- Linux compatible (USB Audio Class)
- 3.5mm input and output
- Decent SNR (60dB+)

### PTT (Push-To-Talk) Control

| Item | Model | Status | Purpose | Price |
|------|-------|--------|---------|-------|
| **USB GPIO Relay** | 5V relay module | ❌ NEEDED | Automated PTT | $5-10 |
| **PTT Cable** | Custom 4-pin to relay | ❌ NEEDED | CB mic PTT connection | DIY |

**Alternatives:**
- VOX (voice-activated TX) - Built into Cobra 29, free but unreliable for data
- Manual PTT - Not practical for automated operation

### External Storage

| Item | Model | Status | Purpose | Capacity |
|------|-------|--------|---------|----------|
| **SSD Enclosure 1** | j5create (ATHENA) | ✅ OWNED | Data logging | 128GB |
| **SSD Enclosure 2** | j5create (NOVA) | ✅ OWNED | Backup / archive | 64GB |
| **SSD Enclosure 3** | j5create (LYRA) | ✅ OWNED | Media / tools | 64GB |

**Total External Storage:** 256GB  
**Purpose:** Logs, recordings, backups, offline maps, documentation

### Peripherals

| Item | Model | Status | Purpose | Notes |
|------|-------|--------|---------|-------|
| **USB Keyboard** | Generic | ❌ NEEDED | Linux setup | $10-20 |
| **USB Mouse** | Generic | ❌ NEEDED | Linux navigation | $5-15 |
| **USB Hub** | Powered 7-10 port | ⚠️ RECOMMENDED | Multiple devices | $20-40 |

**Note:** Xbox has 3 USB-A ports (back) + 1 USB-A port (front). USB hub highly recommended for:
- RTL-SDR
- USB sound card
- GPIO relay
- Keyboard/mouse
- WiFi adapter
- LoRa node
- External storage

### Power and Thermal Management

| Item | Model | Status | Purpose | Notes |
|------|-------|--------|---------|-------|
| **Power Strip** | Surge-protected | ✅ OWNED | Multi-device power | Multiple owned |
| **UPS** | APC or CyberPower | ⚠️ RECOMMENDED | Power backup | $100-200 |
| **External Fans** | USB or AC powered | ✅ OWNED | Xbox cooling | Multiple owned |
| **Thermal Paste** | Arctic MX-4 | ⚠️ OPTIONAL | Reapply if needed | $10 |

**Power Budget:**
- Xbox: 150W typical, 315W max
- CB Radio: 15W (4W RF + overhead)
- Accessories: 20W
- **Total:** ~185W typical

### Antenna Accessories

| Item | Purpose | Status | Price |
|------|---------|--------|-------|
| **White Panels** | DIY reflectors | ✅ OWNED | Owned |
| **Coax Connectors** | PL-259, SO-239, SMA | ❌ NEEDED | $10 |
| **Antenna Mast** | Height for CB antenna | ⚠️ OPTIONAL | $20-100 |
| **Grounding Kit** | Electrical safety | ⚠️ RECOMMENDED | $15-30 |

### Development Systems

| Item | Model | Status | Purpose | Notes |
|------|-------|--------|---------|-------|
| **Laptop 1** | Sony Vaio | ✅ OWNED | Dev/control | Specs TBD |
| **Laptop 2** | Asus ROG | ✅ OWNED | Dev/control | Gaming laptop |

**Purpose:**
- Initial configuration
- Remote SSH into Xbox
- Spectrum monitoring (SDR#, GQRX)
- Development and testing

---

## Shopping List

### Priority 1: Critical Path (CB Packet Radio)
| Item | Est. Cost | Purpose |
|------|-----------|---------|
| USB Sound Card | $10 | CB audio interface |
| 3.5mm Audio Cables (2x) | $10 | CB connections |
| USB GPIO Relay | $5 | PTT control |
| CB Antenna (1/4 wave mobile) | $20 | Initial testing |
| Coax Cable (10ft) | $10 | Antenna connection |
| **Subtotal** | **$55** | |

### Priority 2: Extended Capability
| Item | Est. Cost | Purpose |
|------|-----------|---------|
| RTL-SDR V4 (if not owned) | $40 | Spectrum scanning |
| SDR Antenna (discone) | $30 | Wide-band receive |
| Powered USB Hub (10-port) | $30 | Device expansion |
| **Subtotal** | **$100** | |

### Priority 3: Advanced Features
| Item | Est. Cost | Purpose |
|------|-----------|---------|
| Alfa WiFi Adapter | $50 | Long-range WiFi |
| High-gain WiFi Antenna | $30 | Extended range |
| LoRa T-Beam | $40 | Mesh networking |
| **Subtotal** | **$120** | |

### Priority 4: Infrastructure
| Item | Est. Cost | Purpose |
|------|-----------|---------|
| UPS (1500VA) | $150 | Power backup |
| CB Base Antenna (1/2 wave) | $80 | Better performance |
| Antenna Mast/Mount | $50 | Height advantage |
| Grounding Kit | $20 | Safety |
| **Subtotal** | **$300** | |

**Grand Total (All Priorities):** ~$575

---

## Immediate Next Steps

### Option A: USB Tether Phone ($0, 5 minutes)
- Use phone USB tethering for internet
- Push work to GitHub
- Order parts online

### Option B: Xbox Dev Mode ($20, 1 hour)
- Enable official Dev Mode
- Test USB hardware compatibility
- Verify j5create SSDs work
- Check if RTL-SDR recognized

### Option C: CB Packet Test ($55, 2 hours)
- Order Priority 1 parts ($55)
- Connect Cobra 29 to laptop
- Install Direwolf on laptop
- Test CB packet transmission

### Option D: Order Everything ($575, 10 minutes)
- Order all parts at once
- Begin while waiting for delivery
- Parallel work: jailbreak research

---

## Verification Checklist

### Hardware Owned (Confirmed)
- [x] Xbox Series X
- [x] Cobra 29 WX NW LTD CB radio
- [x] j5create SSD enclosures (ATHENA 128GB, NOVA 64GB, LYRA 64GB)
- [x] Sony Vaio laptop
- [x] Asus ROG laptop
- [x] Power strips (multiple)
- [x] Fans (multiple)
- [x] White panels (antenna reflectors)

### Hardware Status Unknown
- [ ] RTL-SDR V4 (mentioned as "white box?") - **VERIFY**
- [ ] USB hub (if any existing)
- [ ] USB keyboard/mouse
- [ ] Existing cables (HDMI, USB, audio)

### Hardware Needed (Confirmed)
- [ ] USB sound card
- [ ] Audio cables (3.5mm)
- [ ] USB GPIO relay
- [ ] CB antenna
- [ ] Coax cable
- [ ] Keyboard and mouse (if not owned)

### Software Needed
- [ ] Xbox Dev Mode activation ($20 one-time)
- [ ] Linux distro (free)
- [ ] Direwolf (free, open-source)
- [ ] GNURadio (free, open-source)
- [ ] Gqrx (free, open-source)

---

## Inventory by Location

### RF Station (Xbox Setup)
- Xbox Series X
- Cobra 29 CB radio
- j5create SSDs (3x)
- RTL-SDR (if confirmed)
- USB hub
- Keyboard/mouse
- Fans (cooling)
- Power strips

### Development Systems
- Sony Vaio laptop
- Asus ROG laptop

### Antenna Farm (Future)
- CB antenna
- SDR antenna
- WiFi directional antenna
- LoRa antenna
- Antenna mast/mount
- Coax runs

---

## Future Expansion

### Additional Hardware (Aspirational)
| Item | Cost | Purpose |
|------|------|---------|
| HackRF One | $300 | Full TX/RX 1MHz-6GHz |
| BladeRF 2.0 | $420 | High-performance SDR |
| LimeSDR | $300 | Full-duplex SDR |
| USRP B200 | $700 | Professional SDR |
| LoRa Gateway | $150 | Multi-channel LoRa |
| GPS Module | $40 | Position/time sync |
| Iridium Modem | $1000+ | Satellite communications |

### Software Expansion
- Custom GNURadio flowgraphs
- GPU-accelerated signal processing (AMD ROCm)
- Automated logging and analysis
- Web interface for monitoring
- Integration with Strategickhaos ecosystem

---

## Maintenance Schedule

### Weekly
- Clean dust from Xbox vents
- Check cable connections
- Verify SSD mounts
- Review logs for errors

### Monthly
- SWR check on CB antenna
- Backup critical data
- Update Linux packages
- Test all RF systems

### Quarterly
- Full system backup
- Thermal paste check (if temps rising)
- Antenna inspection (weather damage)
- Inventory audit

---

## Notes

### Thermal Management
Xbox Series X is designed for gaming bursts, not 24/7 RF processing. Monitor temperatures:
- Use `sensors` command in Linux
- External fans recommended
- Consider undervolting if temps high
- Keep in well-ventilated area

### Power Considerations
- Xbox + CB radio = ~165W
- UPS recommended for clean power
- Surge protection essential (RF equipment sensitive)
- Consider solar setup for true off-grid

### RF Safety
- CB is low power (4W), but still:
  - Ground antenna properly
  - Keep away from people during TX
  - Use proper coax (not cheap RG-59)
  - Lightning protection on outdoor antennas

---

**Inventory Status:** 60% complete (core owned, accessories needed)  
**Ready to Build:** YES (can start with Phase 1 Dev Mode)  
**Budget Needed:** $55 minimum (CB packet), $575 full build

**Last Updated:** 2026-01-02 by Strategickhaos
