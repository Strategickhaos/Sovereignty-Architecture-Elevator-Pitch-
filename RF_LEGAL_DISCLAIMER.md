# 🔥 RF SPECTRUM OPERATIONS - LEGAL DISCLAIMER

**Document Version:** 1.0  
**Last Updated:** 2026-01-02  
**Applies To:** INV-086 RF Spectrum Harvest Project

---

## ⚖️ LEGAL FRAMEWORK

This document outlines the legal considerations for radio frequency (RF) spectrum operations as part of the Sovereignty Architecture project. **ALL** operations described in this project comply with FCC regulations and federal law.

### **IMPORTANT: READ BEFORE PROCEEDING**

The techniques and tools described in the RF Spectrum Harvest (INV-086) documentation are for **LEGAL, EDUCATIONAL, AND RESEARCH PURPOSES ONLY**. Users are solely responsible for ensuring compliance with all applicable laws and regulations.

---

## ✅ LEGAL OPERATIONS

### **1. Spectrum Scanning (Receive-Only)**
- **Legal Status:** ✅ **FULLY LEGAL**
- **Authority:** FCC Part 15.3 - General Exemption from Licensing
- **Details:** 
  - Passive reception of radio signals is legal across all frequencies
  - No license required for receiving (excluding cellular phone calls)
  - Recording signals is generally legal (with exceptions below)
  
**Restrictions:**
- ⚠️ Cellular phone conversations: Legal to receive, **ILLEGAL** to intentionally intercept or divulge content (18 U.S.C. § 2511)
- ⚠️ Encrypted communications: Legal to receive, **ILLEGAL** to decrypt without authorization
- ⚠️ Sharing recordings: May violate privacy laws depending on content

### **2. WiFi Scanning and Open Network Access**
- **Legal Status:** ✅ **LEGAL** (with conditions)
- **Authority:** Computer Fraud and Abuse Act (CFAA) - 18 U.S.C. § 1030
- **Details:**
  - Scanning for WiFi networks = legal (passive observation)
  - Connecting to **OPEN** networks (no password) = generally legal
  - Connecting to **PUBLIC** guest networks = legal if terms accepted
  
**LEGAL EXAMPLES:**
- ✅ Public library WiFi (explicitly public)
- ✅ Coffee shop guest networks (publicly advertised)
- ✅ "Free WiFi" networks in airports, hotels
- ✅ Networks with SSID containing "Open", "Guest", "Public"

**ILLEGAL ACTIONS:**
- 🚫 Cracking WEP/WPA/WPA2 passwords = **FELONY** (CFAA violation)
- 🚫 Accessing secured networks without permission = federal crime
- 🚫 Using network in ways that violate terms of service
- 🚫 Port scanning, exploiting, or attacking network resources

### **3. LoRa Mesh Networks (ISM Band)**
- **Legal Status:** ✅ **FULLY LEGAL**
- **Authority:** FCC Part 15.247 - Operation within 902-928 MHz band
- **Details:**
  - Unlicensed operation permitted in ISM (Industrial, Scientific, Medical) bands
  - Maximum power: 1 Watt (30 dBm) in US
  - Spread spectrum required (LoRa = CSS modulation, compliant)
  - Encrypted communications permitted

**Requirements:**
- Must operate within designated ISM frequencies:
  - US: 902-928 MHz
  - EU: 863-870 MHz
  - Other regions: Check local regulations
- Must not cause harmful interference
- No license required

### **4. USB Tethering (Cellular)**
- **Legal Status:** ✅ **FULLY LEGAL**
- **Authority:** Your cellular service agreement
- **Details:**
  - Using your own cellular data plan = legal
  - USB tethering = allowed by most carriers (check plan limits)
  - Sharing with local network = permitted under most agreements

**Check Your Plan:**
- Some carriers limit tethering or charge extra
- Speed throttling may apply after certain data usage
- Read carrier terms of service

### **5. Satellite Reception (Receive-Only)**
- **Legal Status:** ✅ **FULLY LEGAL**
- **Authority:** FCC Part 25 - Satellite Communications
- **Details:**
  - Receiving satellite broadcasts = fully legal
  - No license required for reception
  - Examples: Weather satellites, GPS, broadcast data

**Legal Services:**
- ✅ NOAA weather satellites (APT images)
- ✅ Inmarsat EGC (maritime safety broadcasts)
- ✅ GPS signals (receive-only)
- ✅ Othernet/Librecast broadcasts

**ILLEGAL ACTIONS:**
- 🚫 Transmitting to satellites without license = **FEDERAL CRIME**
- 🚫 Decrypting subscription services (e.g., DirecTV) = felony
- 🚫 Jamming satellite signals = FCC violation + criminal charges

---

## 🚫 ILLEGAL OPERATIONS (DO NOT PERFORM)

### **1. WPA/WPA2 Password Cracking**
- **Status:** 🚫 **FELONY**
- **Law:** Computer Fraud and Abuse Act (18 U.S.C. § 1030)
- **Penalties:** 
  - First offense: Up to 1 year imprisonment + fines
  - Subsequent offenses: Up to 10 years imprisonment
  - Civil liability: Actual damages + attorney fees
- **Examples:** Using aircrack-ng, hashcat, or similar tools to crack WiFi passwords

### **2. Unauthorized Network Access**
- **Status:** 🚫 **FELONY**
- **Law:** CFAA + state computer crime laws
- **Penalties:** 
  - Federal: 5-20 years imprisonment (depending on damages)
  - State: Varies (typically felony charges)
- **Examples:** 
  - Accessing secured WiFi without permission
  - Bypassing captive portals
  - Exploiting vulnerabilities in network equipment

### **3. Building Unlicensed Cellular Towers**
- **Status:** 🚫 **FEDERAL CRIME**
- **Law:** Communications Act of 1934 + FCC regulations
- **Penalties:**
  - $10,000+ per day in fines
  - Equipment seizure and forfeiture
  - Criminal prosecution (felony)
  - Up to 5 years imprisonment
- **Examples:**
  - OpenBTS without proper licensing
  - srsRAN with real transmissions
  - IMSI catchers (Stingray-style devices)

**LIMITED EXCEPTION:**
- Lab testing in Faraday cage (no external emissions)
- Must use test SIMs only (no real subscriber connections)
- Still risky - consult attorney before attempting

### **4. Radio Jamming**
- **Status:** 🚫 **FEDERAL CRIME**
- **Law:** Communications Act § 333 - Willful Interference
- **Penalties:**
  - $10,000+ fines per violation
  - Criminal prosecution (felony)
  - Equipment forfeiture
- **Examples:**
  - WiFi jamming devices
  - Cell phone jammers
  - GPS jammers
  - Any intentional interference with licensed services

### **5. Amateur Radio Without License**
- **Status:** 🚫 **ILLEGAL**
- **Law:** FCC Part 97 - Amateur Radio Service
- **Penalties:**
  - $10,000+ fines
  - Equipment forfeiture
  - Loss of licensing eligibility
- **Solution:** Get licensed!
  - Technician license: $15 exam, covers VHF/UHF
  - Study free at [hamstudy.org](https://hamstudy.org)
  - Exam available online or in-person

---

## ⚠️ GRAY AREAS (PROCEED WITH CAUTION)

### **1. Open WiFi Legal Ambiguity**
Some jurisdictions have unclear laws about accessing open WiFi:
- **Michigan:** Conviction for accessing open WiFi without "authorization"
- **Safe Practice:** Only connect to explicitly public networks
- **Red Flags:** Hidden SSIDs, residential-looking networks

### **2. CBRS (Citizens Broadband Radio Service)**
- **Status:** ⚠️ **REQUIRES REGISTRATION**
- **Band:** 3550-3700 MHz
- **Rules:** Must register with SAS (Spectrum Access System)
- **Note:** Receive-only = legal, transmit = license required

### **3. Software Defined Radio Export**
- **Status:** ⚠️ **RESTRICTED**
- **Law:** International Traffic in Arms Regulations (ITAR)
- **Note:** Some SDR software/hardware subject to export controls
- **Safe Practice:** Don't export military-grade SDR tech

---

## 📋 BEST PRACTICES

1. **Receive-Only First**: Start with passive reception (legal)
2. **Read Terms**: Always read WiFi terms of service before connecting
3. **Document Permission**: Get written permission for any questionable operations
4. **Stay Updated**: Laws change - check regulations regularly
5. **Consult Attorney**: When in doubt, consult a telecommunications attorney
6. **Respect Privacy**: Don't intercept, record, or share private communications
7. **No Malicious Intent**: Even legal tools can be illegal if used maliciously

---

## 🎓 EDUCATIONAL USE

This project is designed for **EDUCATIONAL PURPOSES** including:
- Learning about RF spectrum and wireless technologies
- Understanding cybersecurity and network security
- Research into mesh networks and decentralized communications
- Personal sovereignty and infrastructure independence

**Academic Exemptions:**
- Educational institutions may have broader research exemptions
- Always coordinate with your institution's IRB (Institutional Review Board)
- Document research protocols and obtain necessary approvals

---

## 🚨 REPORTING ILLEGAL ACTIVITY

If you witness illegal RF operations:
- **FCC Violations:** [fcc.gov/enforcement](https://www.fcc.gov/enforcement)
- **Cybercrime:** [ic3.gov](https://www.ic3.gov) (FBI)
- **Local Law Enforcement:** For immediate threats

---

## 📚 LEGAL RESOURCES

- **FCC Part 15:** [fcc.gov/part15](https://www.fcc.gov/general/part-15-radio-frequency-devices)
- **Computer Fraud and Abuse Act:** [18 U.S.C. § 1030](https://www.law.cornell.edu/uscode/text/18/1030)
- **ARRL (Amateur Radio):** [arrl.org/fcc-rules](http://www.arrl.org/fcc-rules)
- **EFF Privacy Guide:** [eff.org/issues/privacy](https://www.eff.org/issues/privacy)

---

## ⚖️ DISCLAIMER

**THE AUTHOR(S) AND CONTRIBUTORS TO THIS PROJECT:**
- Do not encourage or condone illegal activities
- Are not responsible for misuse of this information
- Recommend consulting with a legal professional before any questionable activities
- Assume no liability for legal consequences of user actions

**BY USING THIS DOCUMENTATION, YOU AGREE:**
- You are solely responsible for compliance with applicable laws
- You will use this information for legal purposes only
- You understand the legal risks and consequences
- You will not hold the project authors liable for your actions

---

## ✅ ACKNOWLEDGMENT

By proceeding with INV-086 RF Spectrum Harvest implementation, you acknowledge that you have read, understood, and agree to comply with all applicable laws and regulations. You accept full responsibility for your actions.

**This is not legal advice. Consult a qualified attorney for legal guidance.**

---

**Document Authenticity:**  
This legal disclaimer is an integral part of the INV-086 project and must not be removed or modified.

**Last Review:** 2026-01-02  
**Next Review:** 2027-01-02

🔥 **Build Smart. Build Legal. Build Sovereign.** 🔥
