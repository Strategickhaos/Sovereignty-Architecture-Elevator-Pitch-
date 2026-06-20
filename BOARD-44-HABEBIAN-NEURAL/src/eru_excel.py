"""
ERU Excel Report Generator — pure stdlib (zipfile + xml)
Produces eru_audit.xlsx with three sheets:
  ERU_AUDIT   — per-dendrite Expected/Reality/Variance/Understanding
  BURN_RATE   — module completion % and days-remaining
  MODULE_STATUS — axon fired, soma strength, synapse bond orders
"""
import zipfile, io, xml.etree.ElementTree as ET
from datetime import date
from typing import List


# ── XLSX plumbing ──────────────────────────────────────────────────────────────

_SHARED_STRINGS: List[str] = []
_SS_INDEX: dict = {}


def _ss(text: str) -> int:
    """Register shared string, return index."""
    if text not in _SS_INDEX:
        _SS_INDEX[text] = len(_SHARED_STRINGS)
        _SHARED_STRINGS.append(text)
    return _SS_INDEX[text]


def _cell_ref(col: int, row: int) -> str:
    letters = ""
    c = col
    while c > 0:
        c, rem = divmod(c - 1, 26)
        letters = chr(65 + rem) + letters
    return f"{letters}{row}"


def _s_cell(col, row, text):
    """String cell (shared strings)."""
    r = ET.Element("c", r=_cell_ref(col, row), t="s")
    ET.SubElement(r, "v").text = str(_ss(str(text)))
    return r


def _n_cell(col, row, value, style=0):
    """Numeric cell."""
    r = ET.Element("c", r=_cell_ref(col, row))
    if style:
        r.set("s", str(style))
    ET.SubElement(r, "v").text = str(value)
    return r


def _row(row_num, cells):
    r = ET.Element("row", r=str(row_num))
    for c in cells:
        r.append(c)
    return r


def _sheet_xml(rows_xml: list) -> bytes:
    ws = ET.Element("worksheet", xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main")
    sd = ET.SubElement(ws, "sheetData")
    for r in rows_xml:
        sd.append(r)
    return b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ET.tostring(ws)


# ── ERU colour helper ──────────────────────────────────────────────────────────

def _eru_label(variance: float, received: bool) -> str:
    if not received:
        return "PENDING"
    if variance == 0.0:
        return "VARIANCE_0"
    if variance <= 0.1:
        return "LOW_VARIANCE"
    if variance <= 0.3:
        return "MED_VARIANCE"
    return "OPEN_VARIANCE"


# ── Sheet builders ─────────────────────────────────────────────────────────────

def _build_eru_audit(pathway) -> bytes:
    HDR = ["MODULE", "SIGNAL_TYPE", "LABEL", "WEIGHT",
           "RECEIVED", "VARIANCE", "ERU_LABEL", "UNDERSTANDING"]
    rows = []
    r = 1
    rows.append(_row(r, [_s_cell(i+1, r, h) for i, h in enumerate(HDR)]))
    r += 1
    for neuron in pathway.neurons.values():
        for d in neuron.dendrites:
            eru = _eru_label(d.eru_variance, d.received)
            understanding = (
                "COMPLETE — signal integrated into soma"
                if d.received and eru == "VARIANCE_0"
                else "OPEN — dendrite not yet received" if not d.received
                else f"VARIANCE {d.eru_variance:.2f} — review needed"
            )
            cells = [
                _s_cell(1, r, neuron.module_id),
                _s_cell(2, r, d.signal_type),
                _s_cell(3, r, d.label),
                _n_cell(4, r, d.weight),
                _s_cell(5, r, "YES" if d.received else "NO"),
                _n_cell(6, r, round(d.eru_variance, 4)),
                _s_cell(7, r, eru),
                _s_cell(8, r, understanding),
            ]
            rows.append(_row(r, cells))
            r += 1
    return _sheet_xml(rows)


def _build_burn_rate(pathway, today: date = None) -> bytes:
    if today is None:
        today = date.today()
    HDR = ["MODULE", "LABEL", "BEGINS", "DUE", "DAYS_LEFT",
           "SOMA_%", "AXON_FIRED", "ERU", "BURN_%"]
    rows = []
    r = 1
    rows.append(_row(r, [_s_cell(i+1, r, h) for i, h in enumerate(HDR)]))
    r += 1
    for neuron in pathway.neurons.values():
        result = neuron.fire()
        days_left = (neuron.due - today).days
        soma_pct = round(result["strength"] * 100, 1)
        # burn% = how much of the module window is consumed
        span = (neuron.due - neuron.begins).days or 1
        elapsed = max(0, (today - neuron.begins).days)
        burn_pct = round(min(100.0, elapsed / span * 100), 1)
        cells = [
            _s_cell(1, r, neuron.module_id),
            _s_cell(2, r, neuron.label),
            _s_cell(3, r, str(neuron.begins)),
            _s_cell(4, r, str(neuron.due)),
            _n_cell(5, r, days_left),
            _n_cell(6, r, soma_pct),
            _s_cell(7, r, "FIRED" if result["fired"] else "PENDING"),
            _s_cell(8, r, result["eru"]),
            _n_cell(9, r, burn_pct),
        ]
        rows.append(_row(r, cells))
        r += 1
    return _sheet_xml(rows)


def _build_module_status(pathway) -> bytes:
    HDR = ["MODULE", "SOMA_STRENGTH", "THRESHOLD", "FIRED",
           "RECEIVED", "PENDING", "ERU"]
    rows = []
    r = 1
    rows.append(_row(r, [_s_cell(i+1, r, h) for i, h in enumerate(HDR)]))
    r += 1
    for neuron in pathway.neurons.values():
        s = neuron.status()
        cells = [
            _s_cell(1, r, neuron.module_id),
            _n_cell(2, r, s["soma_strength"]),
            _n_cell(3, r, neuron.soma.threshold),
            _s_cell(4, r, "YES" if s["axon_fired"] else "NO"),
            _s_cell(5, r, "; ".join(s["received"]) or "—"),
            _s_cell(6, r, "; ".join(s["pending"]) or "—"),
            _s_cell(7, r, s["eru"]),
        ]
        rows.append(_row(r, cells))
        r += 1

    # Synapse block
    r += 1
    rows.append(_row(r, [_s_cell(1, r, "── SYNAPSES ──")]))
    r += 1
    rows.append(_row(r, [
        _s_cell(1, r, "SYNAPSE"),
        _s_cell(2, r, "BOND_ORDER"),
        _s_cell(3, r, "LIVE"),
        _s_cell(4, r, "ERU"),
    ]))
    r += 1
    for syn in pathway.synapses:
        result = syn.transmit()
        rows.append(_row(r, [
            _s_cell(1, r, syn.label),
            _n_cell(2, r, syn.bond_order),
            _s_cell(3, r, "YES" if result["transmitted"] else "NO"),
            _s_cell(4, r, result.get("eru", "BLOCKED")),
        ]))
        r += 1
    return _sheet_xml(rows)


# ── Shared strings XML ─────────────────────────────────────────────────────────

def _build_shared_strings() -> bytes:
    sst = ET.Element(
        "sst",
        xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        count=str(len(_SHARED_STRINGS)),
        uniqueCount=str(len(_SHARED_STRINGS)),
    )
    for s in _SHARED_STRINGS:
        si = ET.SubElement(sst, "si")
        ET.SubElement(si, "t").text = s
    return b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ET.tostring(sst)


# ── Workbook shell ─────────────────────────────────────────────────────────────

_CONTENT_TYPES = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml"
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/sharedStrings.xml"
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml"
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml"
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet3.xml"
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>"""

_ROOT_RELS = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
                Target="xl/workbook.xml"/>
</Relationships>"""

_WORKBOOK_XML = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="ERU_AUDIT"     sheetId="1" r:id="rId1"/>
    <sheet name="BURN_RATE"     sheetId="2" r:id="rId2"/>
    <sheet name="MODULE_STATUS" sheetId="3" r:id="rId3"/>
  </sheets>
</workbook>"""

_WB_RELS = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
                Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
                Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
                Target="worksheets/sheet3.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings"
                Target="sharedStrings.xml"/>
</Relationships>"""


# ── Public API ─────────────────────────────────────────────────────────────────

def generate_eru_excel(pathway, out_path: str = "eru_audit.xlsx"):
    """Generate a three-sheet XLSX ERU report for a Habebian pathway."""
    # Reset shared strings for a fresh build
    global _SHARED_STRINGS, _SS_INDEX
    _SHARED_STRINGS = []
    _SS_INDEX = {}

    sheet1 = _build_eru_audit(pathway)
    sheet2 = _build_burn_rate(pathway)
    sheet3 = _build_module_status(pathway)
    ss_xml = _build_shared_strings()

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", _CONTENT_TYPES)
        zf.writestr("_rels/.rels", _ROOT_RELS)
        zf.writestr("xl/workbook.xml", _WORKBOOK_XML)
        zf.writestr("xl/_rels/workbook.xml.rels", _WB_RELS)
        zf.writestr("xl/sharedStrings.xml", ss_xml)
        zf.writestr("xl/worksheets/sheet1.xml", sheet1)
        zf.writestr("xl/worksheets/sheet2.xml", sheet2)
        zf.writestr("xl/worksheets/sheet3.xml", sheet3)

    with open(out_path, "wb") as f:
        f.write(buf.getvalue())
    return out_path
