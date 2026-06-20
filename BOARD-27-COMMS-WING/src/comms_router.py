#!/usr/bin/env python3
"""
SAGCO Comms Router — email + SMS classifier and citizen registrar.

Routes every inbound message through the SAGCO district model:
  financial_alert  → trinity
  otp_code         → trinity (CRITICAL)
  marketing        → memory_palace
  personal         → frequency_coast
  work             → eru

Usage:
  comms_router.py --scan-gmail
  comms_router.py --scan-sms
  comms_router.py --classify --sender "+1 833-738-4591" --body "Your OTP is 123456"
  comms_router.py --contacts
  comms_router.py --emit-citizens
"""
import argparse, json, re, sys, time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY  = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
REPORTS   = Path(__file__).resolve().parent.parent / "reports"
CONTACTS  = Path(__file__).resolve().parent.parent / "contacts"
REPORTS.mkdir(parents=True, exist_ok=True)
CONTACTS.mkdir(parents=True, exist_ok=True)

GENESIS_INCREMENT = 3449

# ── Classification rules ──────────────────────────────────────────────────────

OTP_PATTERNS = [
    r"\b\d{6}\b",                        # 6-digit OTP
    r"one.time.code",
    r"verification code",
    r"DO NOT SHARE",
    r"your code is",
]

FINANCIAL_SENDERS = {
    "+1 833-738-4591": "NFCU",
    "+1 855-967-1665": "Bridgecrest",
    "22891":           "Best Buy",
    "NFCU":            "Navy Federal Credit Union",
    "Chase":           "Chase Bank",
    "BankOfAmerica":   "Bank of America",
    "Amex":            "American Express",
    "Discover":        "Discover",
}

MARKETING_PATTERNS = [
    "SHOPPING EVENT", "sale", "offer", "discount", "% off",
    "deal", "promo", "subscribe", "unsubscribe", "Click here",
]

DOMAIN_DISTRICT = {
    "gmail.com":       "frequency_coast",
    "nfcu.org":        "trinity",
    "navy.mil":        "trinity",
    "snhu.edu":        "memory_palace",
    "getsequence.io":  "frequency_coast",
    "google.com":      "frequency_coast",
    "github.com":      "compiler_city",
    "anthropic.com":   "frequency_coast",
    "discord.com":     "frequency_coast",
}


def classify_message(sender: str, body: str, subject: str = "") -> dict:
    text = f"{sender} {subject} {body}".lower()

    # OTP detection — always CRITICAL, trinity
    for pattern in OTP_PATTERNS:
        if re.search(pattern, body, re.IGNORECASE):
            otp_match = re.search(r"\b\d{6}\b", body)
            return {
                "type":      "otp_code",
                "district":  "trinity",
                "severity":  "CRITICAL",
                "sensitive": True,
                "note":      "OTP detected — DO NOT share or log the code value",
                "otp_found": bool(otp_match),
            }

    # Financial senders
    for key, institution in FINANCIAL_SENDERS.items():
        if key.lower() in sender.lower():
            return {
                "type":        "financial_alert",
                "district":    "trinity",
                "severity":    "HIGH",
                "sensitive":   True,
                "institution": institution,
                "note":        f"Financial alert from {institution}",
            }

    # Marketing
    for pattern in MARKETING_PATTERNS:
        if pattern.lower() in text:
            return {
                "type":     "marketing",
                "district": "memory_palace",
                "severity": "LOW",
                "note":     "Marketing/promotional message",
            }

    # Work/ERU keywords
    if any(w in text for w in ["meeting", "invoice", "project", "contract", "deadline", "client"]):
        return {
            "type":     "work",
            "district": "eru",
            "severity": "MEDIUM",
            "note":     "Work-related communication",
        }

    # Default: personal / frequency_coast
    return {
        "type":     "personal",
        "district": "frequency_coast",
        "severity": "LOW",
        "note":     "Personal communication",
    }


def classify_domain(email_address: str) -> str:
    if "@" in email_address:
        domain = email_address.split("@")[1].lower()
        for known, district in DOMAIN_DISTRICT.items():
            if known in domain:
                return district
    return "frequency_coast"


def _make_citizen(sender: str, subject: str, body_preview: str,
                  classification: dict) -> dict:
    tick = int(time.time() * 1000)
    cid  = f"sgc-artifact-{tick}-{tick % GENESIS_INCREMENT}"
    return {
        "cid":      cid,
        "name":     f"msg.{classification['type']}.{sender[:20]}",
        "kind":     "artifact",
        "born_in":  "genesis",
        "district": classification["district"],
        "status":   "active",
        "payload":  {
            "sender":  sender,
            "subject": subject,
            "preview": body_preview[:100] if not classification.get("sensitive") else "[REDACTED — sensitive]",
            "type":    classification["type"],
        },
        "tags":     ["comms", classification["type"], "board-27"],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def register_citizen(citizen: dict):
    if not REGISTRY.exists():
        return
    raw = json.loads(REGISTRY.read_text())
    citizens = raw.get("citizens", raw) if isinstance(raw, dict) else raw
    existing = {c["cid"] for c in citizens}
    if citizen["cid"] in existing:
        return
    citizens.append(citizen)
    if isinstance(raw, dict):
        raw["citizens"] = citizens
        REGISTRY.write_text(json.dumps(raw, indent=2))
    else:
        REGISTRY.write_text(json.dumps(citizens, indent=2))


# ── Known contacts registry ───────────────────────────────────────────────────

def load_contacts() -> dict:
    path = CONTACTS / "known_contacts.json"
    if path.exists():
        return json.loads(path.read_text())
    return {
        "contacts": [
            {"id": "nfcu",        "name": "Navy Federal CU",  "sender": "+1 833-738-4591", "district": "trinity",          "type": "financial"},
            {"id": "bridgecrest", "name": "Bridgecrest",       "sender": "+1 855-967-1665", "district": "trinity",          "type": "financial"},
            {"id": "bestbuy",     "name": "Best Buy",          "sender": "22891",           "district": "memory_palace",    "type": "marketing"},
            {"id": "nakitta",     "name": "Sister Nakitta",    "sender": "SN",              "district": "frequency_coast",  "type": "personal"},
            {"id": "sequence",    "name": "Sequence",          "sender": "getsequence.io",  "district": "frequency_coast",  "type": "work"},
        ]
    }


def save_contacts(contacts: dict):
    path = CONTACTS / "known_contacts.json"
    path.write_text(json.dumps(contacts, indent=2))


def show_contacts():
    contacts = load_contacts()
    print(f"\n  SAGCO Comms — Known Contacts\n")
    print(f"  {'Name':25s}  {'Sender':25s}  {'District':20s}  Type")
    print("  " + "─" * 80)
    for c in contacts.get("contacts", []):
        print(f"  {c['name']:25s}  {c['sender']:25s}  {c['district']:20s}  {c['type']}")


def classify_cmd(sender: str, body: str, subject: str = "", emit: bool = False):
    cl = classify_message(sender, body, subject)
    dist_mark = {
        "trinity": "🔵", "frequency_coast": "🟢", "memory_palace": "🟡",
        "eru": "🟣", "industrial": "🟠",
    }
    mark = dist_mark.get(cl["district"], "⚫")
    print(f"\n  {mark}  Classified: {cl['type']:20s}  district={cl['district']}  severity={cl['severity']}")
    if cl.get("note"):
        print(f"     Note: {cl['note']}")
    if cl.get("sensitive"):
        print(f"     ⚠  SENSITIVE — payload redacted in citizen record")
    if emit and not cl.get("sensitive"):
        citizen = _make_citizen(sender, subject, body[:100], cl)
        register_citizen(citizen)
        print(f"     Citizen registered: {citizen['cid']}")


def scan_sms_demo():
    """Demonstrate SMS classification with known Phone Link messages."""
    print(f"\n  SAGCO Comms — SMS Scanner (Phone Link demo)\n")
    messages = [
        ("+1 833-738-4591", "NFCU Free Alert: The one-time code for your card ending 1507 at WWW-GETSEQUENCE-IO for USD 719.76 is 268623. DO NOT SHARE YOUR CODE WITH ANYONE."),
        ("22891",           "Best Buy: APPLE SHOPPING EVENT IS ON! Ready, Set, GO."),
        ("+1 855-967-1665", "Bridgecrest: Domenic, unfortunately a balance remains on your account."),
        ("+1 361-429-2515", "Be safe"),
    ]
    for sender, body in messages:
        cl = classify_message(sender, body)
        mark = "🔴" if cl["severity"] == "CRITICAL" else "🟠" if cl["severity"] == "HIGH" else "🟡" if cl["severity"] == "MEDIUM" else "⚪"
        preview = "[REDACTED]" if cl.get("sensitive") else body[:50]
        print(f"  {mark}  [{cl['type']:15s}]  {sender:20s}  {cl['district']:20s}  {preview}")


def main():
    parser = argparse.ArgumentParser(description="SAGCO Comms Router")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan-gmail",  action="store_true")
    group.add_argument("--scan-sms",    action="store_true")
    group.add_argument("--classify",    action="store_true")
    group.add_argument("--contacts",    action="store_true")
    parser.add_argument("--sender",     default="")
    parser.add_argument("--body",       default="")
    parser.add_argument("--subject",    default="")
    parser.add_argument("--emit-citizens", action="store_true")
    args = parser.parse_args()

    if args.scan_gmail:
        print("  Gmail scan requires MCP Gmail tools.")
        print("  Run: python sagco-agents/sagco.py comms --scan-gmail")
        print("  (MCP Gmail server provides live inbox access)")
    elif args.scan_sms:
        scan_sms_demo()
    elif args.classify:
        classify_cmd(args.sender, args.body, args.subject, args.emit_citizens)
    elif args.contacts:
        show_contacts()

if __name__ == "__main__":
    main()
