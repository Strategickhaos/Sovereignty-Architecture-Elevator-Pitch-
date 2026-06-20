"""
PURE STDLIB PDF reader.
Reads PDF as bytes, extracts text between BT/ET markers.
Not a full PDF parser — handles basic text extraction.
"""
import re


def read_pdf_bytes(path: str) -> bytes:
    """Read raw PDF bytes."""
    with open(path, "rb") as f:
        return f.read()


def extract_text_from_pdf(path: str) -> str:
    """
    Extract text from PDF using raw byte parsing.
    Finds BT/ET blocks and extracts text from Tj and TJ operators.
    """
    data = read_pdf_bytes(path)
    text_parts = []

    # Find all BT...ET blocks
    bt_et_pattern = re.compile(rb"BT\s*(.*?)\s*ET", re.DOTALL)
    for match in bt_et_pattern.finditer(data):
        block = match.group(1)
        # Extract strings from (text)Tj or [(text)]TJ
        tj_pattern = re.compile(rb"\(([^)]*)\)\s*Tj")
        for m in tj_pattern.finditer(block):
            try:
                text_parts.append(m.group(1).decode("latin-1", errors="replace"))
            except Exception:
                pass
        # TJ operator: [(str1) offset (str2) ...] TJ
        tj_array_pattern = re.compile(rb"\[([^\]]*)\]\s*TJ")
        for m in tj_array_pattern.finditer(block):
            inner = m.group(1)
            str_pattern = re.compile(rb"\(([^)]*)\)")
            for sm in str_pattern.finditer(inner):
                try:
                    text_parts.append(sm.group(1).decode("latin-1", errors="replace"))
                except Exception:
                    pass

    return " ".join(text_parts)


def search_pdf_text(path: str, keyword: str) -> list:
    """Search PDF text for a keyword, return list of matching snippets."""
    text = extract_text_from_pdf(path)
    results = []
    keyword_lower = keyword.lower()
    words = text.split()
    for i, word in enumerate(words):
        if keyword_lower in word.lower():
            start = max(0, i - 5)
            end = min(len(words), i + 6)
            results.append(" ".join(words[start:end]))
    return results
