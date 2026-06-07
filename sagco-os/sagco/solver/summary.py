"""
Summary report generator: produces summary.md text report from processed data.
"""
import os
from datetime import datetime


def generate_summary(rows: list, eru_results: list = None, output_path: str = None) -> str:
    """
    Generate a Markdown summary report from processed rows and ERU results.
    Returns the report as a string.
    """
    from sagco.core.frequency import category_frequency, price_distribution
    from sagco.solver.menus import normalize_category

    lines = [
        "# SAGCO OS — Solve Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"## Data Summary",
        f"- Total rows: {len(rows)}",
        "",
    ]

    # Category breakdown
    cat_freq = category_frequency(rows)
    if cat_freq:
        lines.append("## Category Breakdown")
        for cat, count in sorted(cat_freq.items(), key=lambda x: -x[1]):
            lines.append(f"- {cat}: {count}")
        lines.append("")

    # Price stats
    price_stats = price_distribution(rows)
    if price_stats["count"] > 0:
        lines.append("## Price Statistics")
        lines.append(f"- Count: {price_stats['count']}")
        lines.append(f"- Min: ${price_stats['min']}")
        lines.append(f"- Max: ${price_stats['max']}")
        lines.append(f"- Mean: ${price_stats['mean']}")
        lines.append(f"- Median: ${price_stats['median']}")
        lines.append("")

    # ERU summary
    if eru_results:
        from sagco.core.eru import eru_summary
        summary = eru_summary(eru_results)
        lines.append("## ERU Analysis")
        lines.append(f"- Total analyzed: {summary['total']}")
        lines.append(f"- PASS: {summary['PASS']} ({summary['pass_rate']}%)")
        lines.append(f"- PARTIAL: {summary['PARTIAL']}")
        lines.append(f"- FAIL: {summary['FAIL']}")
        lines.append(f"- Mean variance: {summary['mean_variance']}")
        lines.append("")

    # Sample rows
    if rows:
        lines.append("## Sample Items (first 10)")
        lines.append("| ID | Category | Item | Price | ERU |")
        lines.append("|---|---|---|---|---|")
        for row in rows[:10]:
            row_id = row.get("ID", row.get("id", ""))
            cat = row.get("Category", row.get("category", ""))
            item = row.get("Item", row.get("item", ""))
            price = row.get("Price", row.get("price", ""))
            eru = row.get("ERU", row.get("eru", ""))
            lines.append(f"| {row_id} | {cat} | {item} | {price} | {eru} |")
        lines.append("")

    report = "\n".join(lines)

    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

    return report
