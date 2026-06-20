"""
xlsx_parser.py — Parses Word Frequency Analyser XLSX/CSV files.
Columns: Rank, Word, Lemma, POS, % of text, Occurrence
Falls back to CSV if openpyxl is not available.
"""
import csv
import os


def parse_csv(path: str) -> list:
    """Parse a CSV file with columns: Rank, Word, Lemma, POS, % of text, Occurrence."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            row = _normalise_row(raw)
            if row:
                rows.append(row)
    return rows


def parse_xlsx(path: str) -> list:
    """Parse an XLSX file. Falls back to CSV if openpyxl unavailable."""
    try:
        import openpyxl
    except ImportError:
        raise ImportError("openpyxl not installed — use CSV input instead.")

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = []
    headers = None
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            headers = [str(c).strip() if c is not None else "" for c in row]
            continue
        if headers and any(c is not None for c in row):
            raw = dict(zip(headers, row))
            norm = _normalise_row(raw)
            if norm:
                rows.append(norm)
    wb.close()
    return rows


def _normalise_row(raw: dict) -> dict | None:
    """Normalise column names to standard keys."""
    # Build a lowercase key lookup
    lookup = {k.lower().strip(): v for k, v in raw.items()}

    def get(*keys):
        for k in keys:
            if k in lookup and lookup[k] is not None and str(lookup[k]).strip() != "":
                return lookup[k]
        return None

    rank_val = get("rank")
    word_val = get("word")
    if rank_val is None or word_val is None:
        return None

    try:
        rank = int(float(str(rank_val)))
    except (ValueError, TypeError):
        return None

    word = str(word_val).strip()
    lemma = str(get("lemma") or word).strip()
    pos = str(get("pos") or "other").strip()

    pct_raw = get("% of text", "pct", "% of Text", "% Of Text")
    try:
        pct = float(str(pct_raw).replace("%", "").strip()) if pct_raw is not None else 0.0
    except (ValueError, TypeError):
        pct = 0.0

    occ_raw = get("occurrence", "occurrences", "count")
    try:
        occurrence = int(float(str(occ_raw))) if occ_raw is not None else 1
    except (ValueError, TypeError):
        occurrence = 1

    return {
        "rank": rank,
        "word": word,
        "lemma": lemma,
        "pos": pos,
        "pct": pct,
        "occurrence": occurrence,
    }


def load_frequency_data(path: str) -> list:
    """Auto-detect format and load frequency data."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm", ".xls"):
        try:
            return parse_xlsx(path)
        except ImportError as e:
            print(f"[xlsx_parser] Warning: {e} — trying CSV fallback.")
            csv_path = os.path.splitext(path)[0] + ".csv"
            if os.path.exists(csv_path):
                return parse_csv(csv_path)
            raise FileNotFoundError(f"No CSV fallback found for {path}") from e
    elif ext == ".csv":
        return parse_csv(path)
    else:
        # Try CSV anyway
        return parse_csv(path)
