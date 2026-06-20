"""
PURE STDLIB YAML reader.
Handles: key: value, nested dicts (indent), lists (- item), comments (#).
Not full YAML spec — just enough for SAGCO config files.
"""


def parse_yaml(text: str) -> dict:
    """
    Parse a simple YAML string into a Python dict/list structure.
    Supports:
      - key: value
      - nested dicts via indentation
      - lists via '- item'
      - inline comments with #
      - quoted strings (single and double)
      - booleans: true/false/yes/no
      - null: null/~
      - integers and floats
    """
    lines = text.splitlines()
    result, _ = _parse_block(lines, 0, 0)
    return result


def _strip_comment(s: str) -> str:
    """Remove inline # comments (not inside quotes)."""
    in_sq = False
    in_dq = False
    for i, c in enumerate(s):
        if c == "'" and not in_dq:
            in_sq = not in_sq
        elif c == '"' and not in_sq:
            in_dq = not in_dq
        elif c == "#" and not in_sq and not in_dq:
            return s[:i].rstrip()
    return s


def _parse_value(s: str):
    """Parse a scalar value string into Python object."""
    s = s.strip()
    if not s or s in ("null", "~"):
        return None
    if s.lower() in ("true", "yes"):
        return True
    if s.lower() in ("false", "no"):
        return False
    # quoted string
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    # number
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        pass
    return s


def _get_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _parse_block(lines: list, start: int, base_indent: int):
    """
    Parse a YAML block starting at `start` with `base_indent`.
    Returns (value, next_line_index).
    """
    # Collect non-empty, non-comment lines at this indent level
    # Detect if this block is a list or dict
    result = None
    i = start

    # Skip blank lines
    while i < len(lines) and lines[i].strip() == "":
        i += 1

    if i >= len(lines):
        return {}, i

    first_content = lines[i].lstrip(" ")

    # list block
    if first_content.startswith("- ") or first_content == "-":
        result = []
        while i < len(lines):
            line = lines[i]
            if line.strip() == "" or line.strip().startswith("#"):
                i += 1
                continue
            indent = _get_indent(line)
            if indent < base_indent:
                break
            stripped = line.strip()
            if stripped.startswith("- "):
                item_str = stripped[2:].strip()
                item_str = _strip_comment(item_str)
                if item_str == "" or item_str is None:
                    # sub-block
                    sub, i = _parse_block(lines, i + 1, indent + 2)
                    result.append(sub)
                elif ":" in item_str and not item_str.startswith('"') and not item_str.startswith("'"):
                    # inline dict
                    sub_dict = {}
                    k, _, v = item_str.partition(":")
                    sub_dict[k.strip()] = _parse_value(v.strip())
                    result.append(sub_dict)
                else:
                    result.append(_parse_value(item_str))
                    i += 1
            elif stripped == "-":
                i += 1
                sub, i = _parse_block(lines, i, indent + 2)
                result.append(sub)
            else:
                break
        return result, i

    # dict block
    result = {}
    while i < len(lines):
        line = lines[i]
        if line.strip() == "" or line.strip().startswith("#"):
            i += 1
            continue
        indent = _get_indent(line)
        if indent < base_indent:
            break
        stripped = _strip_comment(line.strip())
        if ":" in stripped:
            key, _, rest = stripped.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest == "" or rest is None:
                # value is next block
                i += 1
                # peek
                while i < len(lines) and (lines[i].strip() == "" or lines[i].strip().startswith("#")):
                    i += 1
                if i < len(lines):
                    next_indent = _get_indent(lines[i])
                    if next_indent > base_indent:
                        sub, i = _parse_block(lines, i, next_indent)
                        result[key] = sub
                    else:
                        result[key] = None
                else:
                    result[key] = None
            else:
                result[key] = _parse_value(rest)
                i += 1
        else:
            i += 1

    return result, i


def load_yaml_file(path: str) -> dict:
    """Load and parse a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return parse_yaml(f.read())
