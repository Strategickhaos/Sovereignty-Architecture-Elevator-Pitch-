"""
text_score.py — Renders a beautiful terminal/text score from MusicNote objects.
"""

HEADER = (
    " ♩  {:<14} {:>5}  {:>5}  {:>6}  {:>5}  {:>9}  {:<10}\n"
    " {}\n"
)

ROW_FMT = " {}  {:<14} {:>5}  {:>5}  {:>6}  {:>5}  {:>9}  {:<10}"


def _note_symbol(duration: str) -> str:
    """Pick a unicode music symbol based on duration."""
    return {
        "whole":      "𝅝 ",
        "half":       "𝅗𝅥 ",
        "quarter":    "♩ ",
        "eighth":     "♪ ",
        "sixteenth":  "𝅘𝅥𝅯 ",
    }.get(duration, "♩ ")


def render_text_score(notes: list, max_rows: int = 50) -> str:
    """Render the score as a formatted text string."""
    lines = []

    # Title banner
    lines.append("")
    lines.append(" ╔══════════════════════════════════════════════════════════╗")
    lines.append(" ║   SAGCO  WORD  FREQUENCY  SCORE                         ║")
    lines.append(" ║   district: frequency_coast  ·  board: BOARD-37         ║")
    lines.append(" ╚══════════════════════════════════════════════════════════╝")
    lines.append("")

    sep = " " + "─" * 66
    header_row = (
        f" {'':2}  {'WORD':<14} {'RANK':>5}  {'OCCs':>5}  {'%':>6}  "
        f"{'NOTE':>5}  {'DURATION':>9}  {'INSTRUMENT':<10}"
    )
    lines.append(header_row)
    lines.append(sep)

    shown = 0
    for note in notes:
        if shown >= max_rows:
            remaining = len(notes) - max_rows
            lines.append(f"   ... {remaining} more notes ...")
            break
        sym = _note_symbol(note.duration)
        row = (
            f" {sym}  {note.word:<14} {note.rank:>5}  {note.occurrence:>5}  "
            f"{note.pct:>6.2f}  {note.note_name:>5}  {note.duration:>9}  "
            f"{note.instrument:<10}"
        )
        lines.append(row)
        shown += 1

    lines.append(sep)
    lines.append(f"   {len(notes)} notes total")
    lines.append("")
    return "\n".join(lines)


def print_score(notes: list, max_rows: int = 50):
    """Print the score to stdout."""
    print(render_text_score(notes, max_rows=max_rows))
