"""
Universal file extractor.
Dispatches to the correct reader based on file extension.
XLSX: zipfile+xml, PDF: raw bytes BT/ET, CSV: csv.DictReader, YAML: manual parser.
"""
import os
import csv


def extract(path: str) -> list:
    """
    Extract data from any supported file type.
    Returns list of dicts.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == ".xlsx":
        return _extract_xlsx(path)
    elif ext == ".csv":
        return _extract_csv(path)
    elif ext in (".yaml", ".yml"):
        return _extract_yaml(path)
    elif ext == ".pdf":
        return _extract_pdf(path)
    elif ext in (".txt", ".md"):
        return _extract_text(path)
    elif ext == ".json":
        return _extract_json(path)
    else:
        # Try as text
        return _extract_text(path)


def _extract_xlsx(path: str) -> list:
    from sagco.io.xlsx_reader import read_xlsx
    return read_xlsx(path)


def _extract_csv(path: str) -> list:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _extract_yaml(path: str) -> list:
    from sagco.io.yaml_reader import load_yaml_file
    data = load_yaml_file(path)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # Try to find a list value
        for v in data.values():
            if isinstance(v, list):
                return v
        return [data]
    return [{"value": str(data)}]


def _extract_pdf(path: str) -> list:
    from sagco.io.pdf_reader import extract_text_from_pdf
    text = extract_text_from_pdf(path)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return [{"line": i + 1, "text": l} for i, l in enumerate(lines)]


def _extract_text(path: str) -> list:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    return [{"line": i + 1, "text": l.rstrip()} for i, l in enumerate(lines)]


def _extract_json(path: str) -> list:
    import json
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    return [data]
