"""
SAGCO built-in standard library functions.
ERU, GUARD, MORSE, SANITY, SOLVE — all pure Python, no external deps.
"""
import re


# ---------------------------------------------------------------------------
# ERU
# ---------------------------------------------------------------------------

def fn_eru(expected, actual):
    """
    Returns 'VARIANCE_0' if expected == actual (numerically or as strings),
    else 'OPEN_VARIANCE'.
    """
    if expected is None and actual is None:
        return "VARIANCE_0"
    try:
        e = float(str(expected).replace("$", "").strip())
        a = float(str(actual).replace("$", "").strip())
        return "VARIANCE_0" if e == a else "OPEN_VARIANCE"
    except (ValueError, TypeError, AttributeError):
        es = str(expected).strip() if expected is not None else ""
        as_ = str(actual).strip() if actual is not None else ""
        return "VARIANCE_0" if es == as_ else "OPEN_VARIANCE"


# ---------------------------------------------------------------------------
# GUARD
# ---------------------------------------------------------------------------

GUARD_BAD_PATTERNS = [
    r"\*\*",           # markdown bold
    r"\\frac",         # LaTeX fraction
    r"\\begin",        # LaTeX environment
    r"\\end",          # LaTeX environment
    r"∑", r"∫", r"∞",  # Unicode math
    r"\\sum", r"\\int", r"\\infty",
    r"\\alpha", r"\\beta", r"\\gamma",
    r"\^",             # exponent notation
    r"\\cdot", r"\\times",
]


def fn_guard(formula_str):
    """
    Checks formula_str for LaTeX/unicode math/markdown artifacts.
    Returns 'MOBIUS_READY' if clean, else 'NOT_READY'.
    """
    s = str(formula_str) if formula_str is not None else ""
    for pattern in GUARD_BAD_PATTERNS:
        if re.search(pattern, s):
            return "NOT_READY"
    return "MOBIUS_READY"


# ---------------------------------------------------------------------------
# MORSE
# ---------------------------------------------------------------------------

MORSE_MAP = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..',  '9': '----.',
    ' ': '/',
}


def fn_morse(text):
    """Encode text to Morse code. Spaces become '/'."""
    if text is None:
        return ""
    s = str(text).upper()
    parts = []
    for ch in s:
        if ch in MORSE_MAP:
            parts.append(MORSE_MAP[ch])
        # Skip unknown chars
    return " ".join(parts)


# ---------------------------------------------------------------------------
# SANITY
# ---------------------------------------------------------------------------

HALLUCINATION_MARKERS = [
    "**", "\\frac", "∑", "∫", "∞", "\\begin",
    "\\end", "\\alpha", "\\beta", "\\sum", "\\int",
    "\\infty", "\\cdot", "\\times", "\\hat", "\\bar",
]


def fn_sanity(text):
    """
    Returns 'SOVEREIGN' if text appears hallucination-free,
    else 'HALLUCINATION_RISK'.
    """
    s = str(text) if text is not None else ""
    for marker in HALLUCINATION_MARKERS:
        if marker in s:
            return "HALLUCINATION_RISK"
    return "SOVEREIGN"


# ---------------------------------------------------------------------------
# SOLVE
# ---------------------------------------------------------------------------

def fn_solve(expr_str):
    """
    Basic algebraic solver for linear equations.
    Handles: ax+b=0, ax+b=c, ax=b, x+b=c
    Returns solution as string or 'UNSOLVABLE'.
    """
    if expr_str is None:
        return "UNSOLVABLE"
    s = str(expr_str).strip().replace(" ", "")

    # Form: ax+b=c or ax=b or x=b
    m = re.match(r"^(-?\d*\.?\d*)x([+-]\d+\.?\d*)?=(-?\d+\.?\d*)$", s, re.IGNORECASE)
    if m:
        a_str = m.group(1) or "1"
        b_str = m.group(2) or "0"
        c_str = m.group(3) or "0"
        try:
            a = float(a_str) if a_str not in ("", "-") else (1.0 if a_str == "" else -1.0)
            b = float(b_str)
            c = float(c_str)
            if a == 0:
                return "UNSOLVABLE" if b != c else "ALL_REALS"
            x = (c - b) / a
            return str(int(x) if x == int(x) else round(x, 6))
        except (ValueError, ZeroDivisionError):
            return "UNSOLVABLE"

    # Try simple: number=number
    m2 = re.match(r"^(-?\d+\.?\d*)=(-?\d+\.?\d*)$", s)
    if m2:
        return "TRUE" if float(m2.group(1)) == float(m2.group(2)) else "FALSE"

    return "UNSOLVABLE"


# ---------------------------------------------------------------------------
# String utilities
# ---------------------------------------------------------------------------

def fn_len(s):
    return len(str(s)) if s is not None else 0


def fn_upper(s):
    return str(s).upper() if s is not None else ""


def fn_lower(s):
    return str(s).lower() if s is not None else ""


def fn_concat(*args):
    return "".join(str(a) for a in args if a is not None)


def fn_trim(s):
    return str(s).strip() if s is not None else ""


def fn_contains(haystack, needle):
    return str(needle).lower() in str(haystack).lower()


def fn_replace(s, old, new):
    return str(s).replace(str(old), str(new))


def fn_split(s, sep=","):
    return str(s).split(str(sep))


def fn_abs(x):
    try:
        return abs(float(x))
    except (ValueError, TypeError):
        return x


def fn_round(x, decimals=0):
    try:
        return round(float(x), int(decimals))
    except (ValueError, TypeError):
        return x


def fn_max(*args):
    nums = []
    for a in args:
        try:
            nums.append(float(a))
        except (ValueError, TypeError):
            pass
    return max(nums) if nums else None


def fn_min(*args):
    nums = []
    for a in args:
        try:
            nums.append(float(a))
        except (ValueError, TypeError):
            pass
    return min(nums) if nums else None


# ---------------------------------------------------------------------------
# STDLIB registry
# ---------------------------------------------------------------------------

STDLIB = {
    "ERU": fn_eru,
    "GUARD": fn_guard,
    "MORSE": fn_morse,
    "SANITY": fn_sanity,
    "SOLVE": fn_solve,
    "LEN": fn_len,
    "UPPER": fn_upper,
    "LOWER": fn_lower,
    "CONCAT": fn_concat,
    "TRIM": fn_trim,
    "CONTAINS": fn_contains,
    "REPLACE": fn_replace,
    "SPLIT": fn_split,
    "ABS": fn_abs,
    "ROUND": fn_round,
    "MAX": fn_max,
    "MIN": fn_min,
}
