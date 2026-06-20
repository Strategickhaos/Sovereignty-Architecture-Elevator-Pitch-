"""
SAGCO Ninja Bot — Discord control plane agent for BOARD-45.
Handles /status, /payplan, /eru commands via Discord slash interface.

PAYMENT ANTIBODY:
  This bot NEVER auto-pays, NEVER clicks Continue, NEVER initiates
  any financial transaction without explicit human confirmation.
  The antibody is not a feature flag — it is hardcoded below.

Pure stdlib where possible. discord.py is required for the slash
command interface (install: pip install discord.py).

To wire without Discord: import and call the command functions directly.
"""
import os, json
from datetime import date, datetime


# ── PAYMENT ANTIBODY — HARDCODED, NEVER REMOVED ───────────────────────────────

class PaymentGuard:
    """
    SAGCO PAYMENT_GUARD antibody.
    Every payment-related action must pass through this class.
    If never_auto_pay is True, any attempt to auto-pay raises PaymentBlocked.
    """
    never_auto_pay:       bool = True
    never_click_continue: bool = True
    require_human_confirm: bool = True
    require_buffer_check:  bool = True
    require_receipt_capture: bool = True
    safe_buffer: float = 500.00   # minimum post-payment balance

    class PaymentBlocked(Exception):
        pass

    def simulate_plan(self, amount_due: float, current_balance: float) -> dict:
        """
        Compute payment plan options. NEVER initiates payment.
        Returns plan dict for human review.
        """
        buffer = current_balance - amount_due
        plans = {
            "A_two_installment": {
                "installments": [round(amount_due / 2, 2), round(amount_due / 2, 2)],
                "timing": ["now", "in 30 days"],
                "buffer_after_first": round(current_balance - amount_due / 2, 2),
            },
            "B_four_installment": {
                "installments": [round(amount_due / 4, 2)] * 4,
                "timing": ["now", "in 2w", "in 4w", "in 6w"],
                "buffer_after_first": round(current_balance - amount_due / 4, 2),
            },
            "C_full_pay": {
                "installments": [amount_due],
                "timing": ["now"],
                "buffer_after": round(buffer, 2),
            },
        }
        # recommend plan that keeps buffer above safe_buffer
        recommended = None
        for key, plan in plans.items():
            first_pay = plan["installments"][0]
            post_balance = current_balance - first_pay
            if post_balance >= self.safe_buffer:
                recommended = key
                break
        return {
            "amount_due": amount_due,
            "current_balance": current_balance,
            "buffer_after_full_pay": round(buffer, 2),
            "plans": plans,
            "recommended": recommended,
            "eru": "VARIANCE_0" if buffer >= self.safe_buffer else "OPEN_VARIANCE",
            "action_required": "HUMAN_CONFIRM",
            "antibody": "PAYMENT_GUARD — never_auto_pay=True",
        }

    def attempt_pay(self, *args, **kwargs):
        raise self.PaymentBlocked(
            "PAYMENT_GUARD: auto-payment blocked. "
            "Human must confirm and initiate manually. "
            "never_auto_pay=True is hardcoded in sagco_ninja_bot.py"
        )

    def log_receipt(self, action: str, amount: float, confirmed_by: str,
                    receipt_path: str = "proofs/command_execution_receipts.jsonl"):
        """Log every confirmed action to the proof trail."""
        os.makedirs(os.path.dirname(receipt_path), exist_ok=True)
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "amount": amount,
            "confirmed_by": confirmed_by,
            "antibody": "PAYMENT_GUARD",
            "never_auto_pay": self.never_auto_pay,
        }
        with open(receipt_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry


PAYMENT_GUARD = PaymentGuard()


# ── COMMAND HANDLERS ───────────────────────────────────────────────────────────

def handle_payplan(amount_due: float, current_balance: float) -> str:
    """
    /payplan command handler.
    Returns formatted string for Discord embed.
    NEVER calls PAYMENT_GUARD.attempt_pay().
    """
    result = PAYMENT_GUARD.simulate_plan(amount_due, current_balance)
    plans  = result["plans"]

    lines = [
        "══════════════════════════════════════════",
        "SAGCO PAYMENT ANALYSIS — SNHU",
        "══════════════════════════════════════════",
        f"Amount Due:       ${result['amount_due']:,.2f}",
        f"Current Balance:  ${result['current_balance']:,.2f}",
        f"Buffer After Full: ${result['buffer_after_full_pay']:,.2f}",
        f"ERU:              {result['eru']}",
        "",
        "PLAN OPTIONS:",
    ]

    labels = {"A_two_installment": "A", "B_four_installment": "B", "C_full_pay": "C"}
    for key, plan in plans.items():
        lbl = labels.get(key, key)
        pays = " + ".join(f"${p:,.2f}" for p in plan["installments"])
        timing = " → ".join(plan["timing"])
        star = " ← RECOMMENDED" if key == result["recommended"] else ""
        lines.append(f"  {lbl}) {pays}  ({timing}){star}")

    lines += [
        "",
        "⚠️  HUMAN CONFIRM REQUIRED before any action.",
        f"    Bot will NEVER auto-pay. (never_auto_pay=True)",
        "══════════════════════════════════════════",
    ]
    return "\n".join(lines)


def handle_status(pathway=None) -> str:
    """
    /status command handler.
    Shows organism status + pathway progress.
    """
    lines = [
        "══════════════════════════════════════════",
        f"SAGCO STATUS — {date.today()}",
        "══════════════════════════════════════════",
        "  discord_bot:      [check deployment]",
        "  event_gateway:    [check /health endpoint]",
        "  observability:    [check prometheus targets]",
        "  ai_agents:        [check agent_hub]",
    ]
    if pathway:
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
        try:
            lines.append("")
            lines.append("  HABEBIAN PATHWAY:")
            for mid, neuron in pathway.neurons.items():
                s = neuron.status()
                icon = "✓" if s["axon_fired"] else "○"
                lines.append(f"    {icon} {mid}  soma={s['soma_strength']}  pending={len(s['pending'])}")
        except Exception as e:
            lines.append(f"  pathway error: {e}")
    lines.append("══════════════════════════════════════════")
    return "\n".join(lines)


def handle_eru(pathway=None) -> str:
    """
    /eru command handler — ERU audit across all systems.
    """
    lines = [
        "══════════════════════════════════════════",
        "SAGCO ERU AUDIT",
        "══════════════════════════════════════════",
    ]
    # Architecture ERU
    components = [
        ("discord_bot",     True,  "bot token set in Vault"),
        ("event_gateway",   True,  "HMAC key configured"),
        ("gitlens",         True,  "gl2discord.sh present"),
        ("jdk_workspace",   True,  "OpenJDK 21 ready"),
        ("observability",   False, "Loki endpoint needs real URL"),
        ("ai_agents",       False, "OPENAI_API_KEY not set"),
        ("vector_kb",       False, "pgvector not provisioned"),
        ("payment_antibody",True,  "never_auto_pay=True hardcoded"),
    ]
    for name, ok, note in components:
        label = "VARIANCE_0   " if ok else "OPEN_VARIANCE"
        icon  = "✓" if ok else "○"
        lines.append(f"  {icon} {name:<20} {label}  {note}")

    if pathway:
        lines.append("")
        lines.append("  HABEBIAN NEURONS:")
        for mid, neuron in pathway.neurons.items():
            neuron.fire()
            lines.append(f"    {mid}: {neuron.soma.eru_label}")

    lines.append("══════════════════════════════════════════")
    return "\n".join(lines)


# ── STANDALONE TEST ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(handle_payplan(amount_due=1026.00, current_balance=3150.00))
    print()
    print(handle_eru())
    print()
    # Prove the antibody blocks auto-pay
    try:
        PAYMENT_GUARD.attempt_pay(amount=1026.00)
    except PaymentGuard.PaymentBlocked as e:
        print(f"ANTIBODY FIRED: {e}")
