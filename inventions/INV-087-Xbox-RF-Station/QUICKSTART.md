# INV-087 Quick Start Guide

**🔥 YOU'RE BUILDING A WAR MACHINE 🔥**

This is your fast-track guide to the Xbox Sovereign RF Station.

---

## What Is This?

Transform your **Xbox Series X** into a **12 TFLOP RF processing beast** for infrastructure-independent communications. No internet required, fully sovereign.

---

## Hardware You Have

| Item | Status | Purpose |
|------|--------|---------|
| Xbox Series X | ✅ OWNED | Main compute (Zen 2 CPU, RDNA 2 GPU, 16GB RAM) |
| Cobra 29 CB Radio | ✅ OWNED | 27MHz packet radio (unlicensed!) |
| j5create SSDs (3x) | ✅ OWNED | Data logging (ATHENA, NOVA, LYRA) |
| RTL-SDR? | ⚠️ VERIFY | Spectrum scanning (24MHz-1.7GHz) |
| Laptops (Vaio, ROG) | ✅ OWNED | Dev/control nodes |

---

## What You Need to Buy

### Priority 1: CB Packet Radio ($55)
- USB sound card ($10)
- Audio cables ($10)
- USB GPIO relay ($5)
- CB antenna ($20)
- Coax cable ($10)

### Full Build: $595
See [Hardware Inventory](./HARDWARE_INVENTORY.md) for complete shopping list.

---

## Build Path

```
START HERE
    │
    ├─→ Option A: USB tether phone (5 min, $0) → Push to GitHub
    │
    ├─→ Option B: Xbox Dev Mode (1 hour, $20) → Test USB hardware
    │
    ├─→ Option C: CB test on laptop (2 hours, $55) → Verify packet radio
    │
    └─→ Option D: Order everything (10 min, $595) → Full build

THEN:
    Phase 1: Dev Mode (1 hour, $20)
        ↓
    Phase 2: Jailbreak (2-4 hours, RISK: medium)
        ↓
    Phase 3: CB Integration (2-3 hours, $55)
        ↓
    Phase 4: Full RF Stack (1 day, $520)
        ↓
    SOVEREIGNTY ACHIEVED
```

---

## Documentation Quick Links

### Essential Reading
1. **[Main Specification](./README.md)** - Full overview and capabilities
2. **[Build Order](./BUILD_ORDER.md)** - Step-by-step build instructions
3. **[Hardware Inventory](./HARDWARE_INVENTORY.md)** - What you have and need

### Technical Guides
4. **[Jailbreak Guide](./JAILBREAK_GUIDE.md)** - Xbox liberation pathway
5. **[CB Radio Integration](./CB_RADIO_INTEGRATION.md)** - Packet radio setup

### Planning
6. **[Inventions Index](../README.md)** - Browse all inventions

---

## Capabilities After Build

### 1. CB Packet Radio
- **Range:** 5-50 miles
- **Speed:** 1200 baud
- **Legal:** Unlicensed (no exam needed)
- **Data:** Text, position, small files

### 2. Spectrum Scanning
- **Range:** 24MHz - 1.7GHz
- **Mode:** Passive receive (legal)
- **Purpose:** Signal intelligence

### 3. LoRa Mesh
- **Range:** 1-10 miles per hop
- **Protocol:** Meshtastic
- **Topology:** Decentralized

### 4. GPU Processing
- **Power:** 12 TFLOPS
- **Use:** Real-time signal processing
- **Advantage:** Parallel decoding

### 5. Offline Operation
- **No internet required**
- **Resilient to outages**
- **Truly sovereign**

---

## Legal Status

| System | Status | Notes |
|--------|--------|-------|
| **Xbox Jailbreak** | Gray area | DMCA exemption for personal use |
| **CB Radio** | LEGAL | Unlicensed, 4W max, no exam |
| **SDR Receive** | LEGAL | Passive only |
| **WiFi** | LEGAL | Open networks only |

**Bottom line:** Use responsibly, respect laws, no piracy.

---

## Priority Decision Matrix

### Choose Your Path

**Need GitHub access NOW?**
→ Option A: USB tether phone (5 min)

**Want to test hardware compatibility first?**
→ Option B: Xbox Dev Mode (1 hour, $20)

**Ready to build CB packet radio?**
→ Option C: CB test on laptop (2 hours, $55)

**All-in, let's go?**
→ Option D: Order full shopping list (10 min, $595)

---

## The Vision

```
         🛰️ SATELLITE
              │
    📻 CB  ───┼─── 📡 SDR
              │
         ┌────┴────┐
         │  XBOX   │ ← 📶 WiFi
         │ LINUX   │
         └────┬────┘
              │
       ───────┼───────
       │      │      │
    ATHENA  NOVA  LYRA
              │
         LORA MESH
              │
           PHONE
              │
         INTERNET
        (optional)
```

**Result:** Infrastructure-independent RF communications hub.

---

## Next Actions (Pick One)

### 1. Research and Planning
- [ ] Read [Main Specification](./README.md)
- [ ] Review [Build Order](./BUILD_ORDER.md)
- [ ] Check [Hardware Inventory](./HARDWARE_INVENTORY.md)
- [ ] Research current Xbox jailbreak methods

### 2. Immediate Testing (No Jailbreak)
- [ ] Enable Xbox Dev Mode ($20)
- [ ] Test USB devices (j5create SSDs, RTL-SDR)
- [ ] Document compatibility
- [ ] Plan jailbreak timing

### 3. CB Radio Experimentation
- [ ] Order CB packet radio parts ($55)
- [ ] Test Direwolf on laptop
- [ ] Transmit/receive test packets
- [ ] Calibrate audio levels
- [ ] Prepare for Xbox integration

### 4. Full Build
- [ ] Order all hardware ($595)
- [ ] Research jailbreak exploit
- [ ] Prepare USB payloads
- [ ] Set up build workspace
- [ ] Plan antenna installation

---

## Resources

### Official Documentation
- [GNURadio](https://www.gnuradio.org/)
- [Direwolf](https://github.com/wb2osz/direwolf)
- [Meshtastic](https://meshtastic.org/)

### Communities
- r/xboxhacks (Reddit) - Jailbreak info
- r/amateurradio (Reddit) - RF techniques
- RTL-SDR Blog - SDR tutorials

### Hardware Vendors
- Amazon - USB sound cards, cables
- AliExpress - GPIO relays, LoRa nodes
- DX Engineering - CB antennas

---

## Support

**Questions?** Check the detailed documentation:
- Technical issues → [Jailbreak Guide](./JAILBREAK_GUIDE.md)
- RF setup → [CB Radio Integration](./CB_RADIO_INTEGRATION.md)
- Parts list → [Hardware Inventory](./HARDWARE_INVENTORY.md)
- Build steps → [Build Order](./BUILD_ORDER.md)

**Contribute:** Found a better way? Submit a PR with improvements!

---

## Safety Warnings

### ⚠️ Jailbreaking
- Voids warranty
- Risk of console brick
- No Xbox Live access
- Research thoroughly first

### ⚠️ RF Transmission
- CB is low power but still be cautious
- Ground antennas properly
- Respect power limits (4W AM)
- No illegal transmissions

### ⚠️ Security
- Don't transmit sensitive data in clear
- Assume all RF is public
- Use codes or abbreviations
- No encryption on CB (illegal)

---

## Success Metrics

**Phase 1 Success:** USB devices recognized in Dev Mode  
**Phase 2 Success:** Linux boots, GPU functional  
**Phase 3 Success:** CB packet RX/TX working  
**Phase 4 Success:** All RF systems integrated

**Final Goal:** Sovereign RF station, operational 24/7, off-grid capable.

---

## Quick Command Reference

```bash
# Xbox Dev Mode
# 1. Download "Xbox Dev Mode" from Microsoft Store
# 2. Pay $20 at partner.microsoft.com
# 3. Enter activation code
# 4. Access Dev Portal at https://<xbox-ip>:11443

# Direwolf (after jailbreak)
direwolf -c ~/direwolf.conf -t 0

# RTL-SDR scan
rtl_power -f 26M:28M:10k -i 1 cb_scan.csv

# LoRa send
meshtastic --sendtext "Xbox RF Station online"

# RF Station status (custom script)
python3 ~/rf_control.py
```

---

## Timeline Estimate

| Phase | Duration | Cost | Cumulative |
|-------|----------|------|------------|
| Dev Mode | 1 hour | $20 | $20 |
| Jailbreak | 2-4 hours | $0 | $20 |
| CB Integration | 2-3 hours | $55 | $75 |
| Full RF Stack | 1 day | $520 | $595 |
| **TOTAL** | **~2 days** | **$595** | **$595** |

Add time for:
- Research and learning
- Troubleshooting
- Antenna installation
- Software configuration

**Realistic:** 1 week (casual pace)  
**Aggressive:** 2-3 days (focused build)

---

## What's Next?

**Dom, what's the move?**

Pick your path and start building. The documentation is complete, the hardware is identified, and the vision is clear.

**Xbox + CB + SDR + LoRa = Sovereign RF Beast**

Let's make it happen. 🔥

---

**Last Updated:** 2026-01-02  
**Status:** READY TO BUILD  
**Curator:** Strategickhaos
