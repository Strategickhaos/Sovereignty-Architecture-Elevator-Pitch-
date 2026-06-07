"""
PURE STDLIB XLSX reader.
XLSX is a ZIP file. Inside:
  xl/worksheets/sheet1.xml  — cell data
  xl/sharedStrings.xml      — string table
Parse with stdlib only. No openpyxl, no pandas.
"""
import zipfile
import xml.etree.ElementTree as ET


def read_xlsx(path: str, sheet_index: int = 0) -> list:
    """
    Read an XLSX file and return a list of dicts (row 1 = headers).

    Args:
        path: Path to the .xlsx file.
        sheet_index: 0-based index of which sheet to read.

    Returns:
        List of dicts keyed by header row values.
    """
    NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    ns = {"x": NS}

    with zipfile.ZipFile(path) as z:
        names = z.namelist()

        # 1. Read shared strings (may be absent)
        strings = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall(".//x:si", ns):
                parts = []
                for t in si.findall(".//x:t", ns):
                    if t.text:
                        parts.append(t.text)
                strings.append("".join(parts))

        # 2. Identify sheet files
        sheet_files = sorted(
            [n for n in names if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")]
        )
        if not sheet_files:
            return []
        sheet_path = sheet_files[sheet_index] if sheet_index < len(sheet_files) else sheet_files[0]

        # 3. Parse sheet XML
        root = ET.fromstring(z.read(sheet_path))

        rows: dict = {}
        for cell in root.findall(".//x:c", ns):
            ref = cell.get("r", "")
            if not ref:
                continue
            cell_type = cell.get("t", "")
            v_el = cell.find("x:v", ns)
            is_el = cell.find("x:is", ns)  # inline string

            col = "".join(c for c in ref if c.isalpha())
            row_num_str = "".join(c for c in ref if c.isdigit())
            if not row_num_str:
                continue
            row_num = int(row_num_str)

            if is_el is not None:
                t_el = is_el.find("x:t", ns)
                val = t_el.text if t_el is not None else ""
            elif v_el is not None and v_el.text is not None:
                if cell_type == "s":
                    # shared string index
                    try:
                        idx = int(v_el.text)
                        val = strings[idx] if idx < len(strings) else ""
                    except (ValueError, IndexError):
                        val = v_el.text
                elif cell_type in ("str", "inlineStr"):
                    val = v_el.text
                else:
                    val = v_el.text
            else:
                val = ""

            rows.setdefault(row_num, {})[col] = val

        if not rows:
            return []

        # 4. Row 1 = headers
        header_row = min(rows.keys())
        headers = rows[header_row]

        result = []
        for rownum in sorted(rows.keys()):
            if rownum == header_row:
                continue
            record = {}
            for col, val in rows[rownum].items():
                header = headers.get(col, col)
                record[header] = val
            result.append(record)

        return result


def read_xlsx_all_sheets(path: str) -> dict:
    """Read all sheets, return dict of sheet_name -> list[dict]."""
    NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    ns = {"x": NS}

    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        sheet_files = sorted(
            [n for n in names if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")]
        )

    result = {}
    for i, sf in enumerate(sheet_files):
        sheet_name = sf.split("/")[-1].replace(".xml", "")
        result[sheet_name] = read_xlsx(path, sheet_index=i)
    return result
