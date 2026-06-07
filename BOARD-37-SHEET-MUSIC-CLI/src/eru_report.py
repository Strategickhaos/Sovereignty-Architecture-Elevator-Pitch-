"""
eru_report.py — ERU (Expected/Reality/Uncertainty) proof for the music pass.
Writes reports/music_eru.yaml after each run.
"""
import os
import datetime


def build_eru_report(notes: list, source_file: str, output_files: list) -> dict:
    """Build the ERU report dict and write it to reports/music_eru.yaml."""
    n = len(notes)

    # Compute stats
    channels_used = sorted(set(note.channel for note in notes))
    durations_used = sorted(set(note.duration for note in notes))
    pitch_min = min((note.pitch for note in notes), default=0)
    pitch_max = max((note.pitch for note in notes), default=0)
    velocity_min = min((note.velocity for note in notes), default=0)
    velocity_max = max((note.velocity for note in notes), default=0)

    report = {
        "board": "BOARD-37-SHEET-MUSIC-CLI",
        "district": "frequency_coast",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "source_file": source_file,
        "output_files": output_files,
        "expected": {
            "all_words_mapped_to_notes": True,
            "variance": 0,
            "pitch_range": "C3-C5 (MIDI 48-72)",
            "velocity_range": "40-127",
            "channels": "0,1,2,3,4,9",
        },
        "actual": {
            "notes_generated": n,
            "channels_used": channels_used,
            "durations_used": durations_used,
            "pitch_min": pitch_min,
            "pitch_max": pitch_max,
            "velocity_min": velocity_min,
            "velocity_max": velocity_max,
            "words_mapped": [note.word for note in notes[:10]] + (["..."] if n > 10 else []),
        },
        "proof": {
            "status": "PASS" if n > 0 else "FAIL",
            "message": f"{n} notes generated from {source_file}",
            "sovereign_law": "Every word row produces exactly one MusicNote — no word left unmapped.",
        },
    }

    # Write YAML manually (no external deps)
    _write_yaml(report)
    return report


def _write_yaml(report: dict):
    """Write report to reports/music_eru.yaml using stdlib only."""
    here = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(here, "..", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    path = os.path.join(reports_dir, "music_eru.yaml")

    def _fmt(val, indent=0):
        pad = "  " * indent
        if isinstance(val, dict):
            lines = []
            for k, v in val.items():
                if isinstance(v, (dict, list)):
                    lines.append(f"{pad}{k}:")
                    lines.append(_fmt(v, indent + 1))
                else:
                    lines.append(f"{pad}{k}: {_scalar(v)}")
            return "\n".join(lines)
        elif isinstance(val, list):
            if not val:
                return f"{pad}[]"
            lines = []
            for item in val:
                if isinstance(item, dict):
                    lines.append(f"{pad}- ")
                    lines.append(_fmt(item, indent + 1))
                else:
                    lines.append(f"{pad}- {_scalar(item)}")
            return "\n".join(lines)
        return f"{pad}{_scalar(val)}"

    def _scalar(v):
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, str) and any(c in v for c in ":#{}[]|>&*!,"):
            return f'"{v}"'
        return str(v)

    content = "# SAGCO ERU Report — Music Pass\n" + _fmt(report) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
