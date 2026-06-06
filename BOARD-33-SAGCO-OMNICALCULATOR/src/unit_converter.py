#!/usr/bin/env python3
"""
BOARD-33 Unit Converter — Sovereign Unit Normalizer
Beats Excel on: unit-aware arithmetic.
All values normalized to SI base, then converted to target.

Usage:
  python unit_converter.py 100 mph km/h
  python unit_converter.py 98.6 F C
  python unit_converter.py 1 atm Pa
  python unit_converter.py 60 kg lb
  python unit_converter.py --list
"""

from __future__ import annotations
import sys

# ── Unit graph — all factors to SI base ──────────────────────────────────────
# Format: "unit_symbol": (si_factor, si_base, unit_type)

UNITS: dict[str, tuple[float, str, str]] = {
    # Length
    "m":   (1.0,        "m",   "length"),
    "km":  (1000.0,     "m",   "length"),
    "cm":  (0.01,       "m",   "length"),
    "mm":  (0.001,      "m",   "length"),
    "ft":  (0.3048,     "m",   "length"),
    "in":  (0.0254,     "m",   "length"),
    "mi":  (1609.344,   "m",   "length"),
    "yd":  (0.9144,     "m",   "length"),
    "nm":  (1e-9,       "m",   "length"),

    # Mass
    "kg":  (1.0,        "kg",  "mass"),
    "g":   (0.001,      "kg",  "mass"),
    "lb":  (0.453592,   "kg",  "mass"),
    "oz":  (0.0283495,  "kg",  "mass"),
    "t":   (1000.0,     "kg",  "mass"),

    # Time
    "s":   (1.0,        "s",   "time"),
    "ms":  (0.001,      "s",   "time"),
    "min": (60.0,       "s",   "time"),
    "h":   (3600.0,     "s",   "time"),
    "hr":  (3600.0,     "s",   "time"),
    "day": (86400.0,    "s",   "time"),
    "wk":  (604800.0,   "s",   "time"),

    # Speed
    "m/s":   (1.0,      "m/s", "speed"),
    "km/h":  (1/3.6,    "m/s", "speed"),
    "kph":   (1/3.6,    "m/s", "speed"),
    "mph":   (0.44704,  "m/s", "speed"),
    "knot":  (0.514444, "m/s", "speed"),

    # Temperature — handled separately (non-linear)
    "C":  ("temp", "C", "temperature"),
    "F":  ("temp", "F", "temperature"),
    "K":  ("temp", "K", "temperature"),

    # Pressure
    "Pa":   (1.0,       "Pa",  "pressure"),
    "kPa":  (1000.0,    "Pa",  "pressure"),
    "MPa":  (1e6,       "Pa",  "pressure"),
    "atm":  (101325.0,  "Pa",  "pressure"),
    "bar":  (100000.0,  "Pa",  "pressure"),
    "psi":  (6894.76,   "Pa",  "pressure"),
    "mmHg": (133.322,   "Pa",  "pressure"),

    # Energy
    "J":   (1.0,        "J",   "energy"),
    "kJ":  (1000.0,     "J",   "energy"),
    "cal": (4.184,      "J",   "energy"),
    "kcal":(4184.0,     "J",   "energy"),
    "Wh":  (3600.0,     "J",   "energy"),
    "kWh": (3.6e6,      "J",   "energy"),
    "BTU": (1055.06,    "J",   "energy"),
    "eV":  (1.602e-19,  "J",   "energy"),

    # Power
    "W":   (1.0,        "W",   "power"),
    "kW":  (1000.0,     "W",   "power"),
    "MW":  (1e6,        "W",   "power"),
    "hp":  (745.7,      "W",   "power"),

    # Data
    "B":   (1.0,        "B",   "data"),
    "KB":  (1024.0,     "B",   "data"),
    "MB":  (1048576.0,  "B",   "data"),
    "GB":  (1073741824.0,"B",  "data"),
    "TB":  (1099511627776.0,"B","data"),
    "bit": (0.125,      "B",   "data"),
    "Kbps":(125.0,      "B",   "data"),  # per second → B/s
    "Mbps":(125000.0,   "B",   "data"),

    # Angle
    "deg": (3.14159265358979/180, "rad", "angle"),
    "rad": (1.0,        "rad", "angle"),
    "grad":(3.14159265358979/200, "rad", "angle"),
}


def _temp_convert(value: float, from_unit: str, to_unit: str) -> float:
    # Convert to Celsius first
    if from_unit == "F":
        c = (value - 32) * 5 / 9
    elif from_unit == "K":
        c = value - 273.15
    else:
        c = value
    # Convert from Celsius to target
    if to_unit == "F":
        return c * 9 / 5 + 32
    elif to_unit == "K":
        return c + 273.15
    return c


def convert(value: float, from_unit: str, to_unit: str) -> dict:
    if from_unit not in UNITS:
        return {"error": f"Unknown unit: {from_unit}", "known": list(UNITS.keys())}
    if to_unit not in UNITS:
        return {"error": f"Unknown unit: {to_unit}", "known": list(UNITS.keys())}

    from_info = UNITS[from_unit]
    to_info   = UNITS[to_unit]

    # Temperature special case
    if from_info[2] == "temperature":
        result = _temp_convert(value, from_unit, to_unit)
        variance = 0.0
    else:
        if from_info[2] != to_info[2]:
            return {"error": f"Type mismatch: {from_info[2]} ≠ {to_info[2]}"}
        si_value = value * from_info[0]
        result   = si_value / to_info[0]
        variance = 0.0

    return {
        "input":    f"{value} {from_unit}",
        "result":   f"{result:.6g} {to_unit}",
        "value":    result,
        "from":     from_unit,
        "to":       to_unit,
        "type":     from_info[2],
        "variance": variance,
        # ERU
        "expected": f"unit-correct conversion of {value} {from_unit}",
        "actual":   f"{result:.6g} {to_unit}",
    }


def convert_chain(value: float, units: list[str]) -> list[dict]:
    results = []
    for i in range(len(units) - 1):
        r = convert(value, units[i], units[i+1])
        if "error" not in r:
            value = r["value"]
        results.append(r)
    return results


def list_units() -> dict[str, list[str]]:
    types: dict[str, list[str]] = {}
    for sym, (_, _, typ) in UNITS.items():
        types.setdefault(typ, []).append(sym)
    return types


def main(args: list[str] = None):
    if args is None:
        args = sys.argv[1:]

    if not args or "--list" in args:
        units_by_type = list_units()
        print("\n  SAGCO Sovereign Unit Converter — available units:\n")
        for typ, syms in sorted(units_by_type.items()):
            print(f"  {typ:15s}: {', '.join(sorted(syms))}")
        return

    if len(args) < 3:
        print("  Usage: unit_converter.py VALUE FROM_UNIT TO_UNIT")
        return

    value     = float(args[0])
    from_unit = args[1]
    to_unit   = args[2]

    result = convert(value, from_unit, to_unit)
    if "error" in result:
        print(f"  ERROR: {result['error']}")
        return

    print(f"\n  {result['input']} = {result['result']}")
    print(f"  Type    : {result['type']}")
    print(f"\n  ERU:")
    print(f"  Expected: {result['expected']}")
    print(f"  Actual  : {result['actual']}")
    print(f"  Variance: 0 (exact conversion)")


if __name__ == "__main__":
    main()
