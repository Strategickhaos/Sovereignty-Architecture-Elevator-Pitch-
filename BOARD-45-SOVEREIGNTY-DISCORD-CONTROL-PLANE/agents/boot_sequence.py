"""
BOARD-45 Boot Sequence — enforces the correct dependency order:

  1. AUDIT (Loki)      — logs before anything else
  2. MEMORY (pgvector) — organism must remember decisions
  3. REASONING (OpenAI) — intelligence last, never first

"Reasoning without audit is risky. Audit first, intelligence second."

If a higher layer tries to initialize before its dependencies,
BootBlocked is raised. Same antibody pattern as PaymentGuard.
"""
import os
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


class BootBlocked(Exception):
    pass


@dataclass
class BootLayer:
    name:        str
    env_key:     str            # env var that activates this layer
    depends_on:  List[str]      # layer names that must be VARIANCE_0 first
    description: str
    eru_label:   str = "PENDING"
    active:      bool = False
    endpoint:    Optional[str] = None

    def check(self, active_layers: List[str]) -> "BootLayer":
        """Verify dependencies are active before this layer can boot."""
        missing = [d for d in self.depends_on if d not in active_layers]
        if missing:
            self.eru_label = "OPEN_VARIANCE"
            raise BootBlocked(
                f"BOOT_BLOCKED: {self.name} requires {missing} first.\n"
                f"  Reason: {_DEPENDENCY_REASON.get(self.name, 'dependency not met')}"
            )
        val = os.environ.get(self.env_key, "").strip()
        if not val:
            self.eru_label = "OPEN_VARIANCE"
            return self
        self.active    = True
        self.eru_label = "VARIANCE_0"
        return self


_DEPENDENCY_REASON = {
    "MEMORY":    "pgvector stores receipts and decisions — must exist before reasoning",
    "REASONING": "reasoning without audit is risky — logs + memory must be active first",
}


# ── The three open-variance layers in correct boot order ─────────────────────

BOOT_SEQUENCE: List[BootLayer] = [

    BootLayer(
        name        = "AUDIT",
        env_key     = "LOKI_ENDPOINT",
        depends_on  = [],           # no dependencies — first layer always
        description = "Loki log aggregation — every action has a receipt",
        endpoint    = "https://loki.strategickhaos.internal",
    ),

    BootLayer(
        name        = "MEMORY",
        env_key     = "PGVECTOR_CONN",
        depends_on  = ["AUDIT"],    # logs must exist before memory
        description = "pgvector — organism remembers decisions and receipts",
    ),

    BootLayer(
        name        = "REASONING",
        env_key     = "OPENAI_API_KEY",
        depends_on  = ["AUDIT", "MEMORY"],  # both required before reasoning
        description = "OpenAI — reasoning layer, last to boot",
    ),
]


def run_boot_sequence(strict: bool = True) -> dict:
    """
    Boot the three open-variance layers in dependency order.
    If strict=True, a missing dependency raises BootBlocked.
    If strict=False, logs the block and continues (for dry-run).

    Returns dict of layer name → eru_label.
    """
    active: List[str] = []
    results = {}

    print("━" * 55)
    print("SAGCO BOARD-45 BOOT SEQUENCE")
    print("Audit → Memory → Reasoning")
    print("━" * 55)

    for layer in BOOT_SEQUENCE:
        try:
            layer.check(active)
            if layer.active:
                active.append(layer.name)
                print(f"  ✓ [{layer.eru_label}] {layer.name:<12} — {layer.description}")
            else:
                print(f"  ○ [OPEN_VARIANCE ] {layer.name:<12} — {layer.env_key} not set")
        except BootBlocked as e:
            layer.eru_label = "BLOCKED"
            if strict:
                print(f"  ✗ [BLOCKED       ] {layer.name:<12} — dependency not met")
                print(f"    {e}")
            else:
                print(f"  ○ [BLOCKED       ] {layer.name:<12} — {e.args[0].split(chr(10))[0]}")
        results[layer.name] = layer.eru_label

    print("━" * 55)
    open_count = sum(1 for v in results.values() if v != "VARIANCE_0")
    if open_count == 0:
        print("  ALL LAYERS ACTIVE — VARIANCE_0")
    else:
        print(f"  {open_count} OPEN_VARIANCE items — close in order above")
        print()
        print("  Next action:")
        for layer in BOOT_SEQUENCE:
            if layer.eru_label != "VARIANCE_0":
                print(f"    Set {layer.env_key}")
                print(f"    Reason: {layer.description}")
                break   # only show the NEXT step, not all three
    print("━" * 55)

    return results


def close_variance(layer_name: str, value: str) -> str:
    """
    Write a layer's env key to the local .env file (never to code).
    Returns eru_label after setting.
    """
    layer = next((l for l in BOOT_SEQUENCE if l.name == layer_name), None)
    if not layer:
        return f"UNKNOWN_LAYER: {layer_name}"

    env_path = os.path.join(os.path.dirname(__file__), "../../.env.board45")
    lines = []
    try:
        with open(env_path) as f:
            lines = [l for l in f.readlines() if not l.startswith(f"{layer.env_key}=")]
    except FileNotFoundError:
        pass

    lines.append(f"{layer.env_key}={value}\n")
    with open(env_path, "w") as f:
        f.writelines(lines)

    os.environ[layer.env_key] = value
    return f"SET: {layer.env_key} → VARIANCE_0 (written to .env.board45)"


if __name__ == "__main__":
    # Dry run — shows what's missing without raising
    results = run_boot_sequence(strict=False)
    print()
    print("BOOT MAP:")
    for name, eru in results.items():
        print(f"  {name:<12} → {eru}")
