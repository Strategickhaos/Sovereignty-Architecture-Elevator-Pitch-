"""
ERU — Expected/Actual/Variance/PASS/PARTIAL/FAIL engine.
The core sovereignty verification algorithm.
"""


ERU_PASS = "PASS"
ERU_PARTIAL = "PARTIAL"
ERU_FAIL = "FAIL"
VARIANCE_0 = "VARIANCE_0"
OPEN_VARIANCE = "OPEN_VARIANCE"


def compute_variance(expected, actual) -> float:
    """
    Compute numeric variance between expected and actual.
    For strings, returns 0 if equal, 1 if not.
    For numbers, returns abs(expected - actual).
    """
    try:
        e = float(str(expected).replace("$", "").strip())
        a = float(str(actual).replace("$", "").strip())
        return abs(e - a)
    except (ValueError, TypeError):
        return 0.0 if str(expected).strip() == str(actual).strip() else 1.0


def eru_label(expected, actual, pass_threshold: float = 0, partial_threshold: float = 5) -> str:
    """
    Returns ERU status label: PASS / PARTIAL / FAIL.
    """
    var = compute_variance(expected, actual)
    if var <= pass_threshold:
        return ERU_PASS
    elif var <= partial_threshold:
        return ERU_PARTIAL
    else:
        return ERU_FAIL


def eru_variance_label(expected, actual) -> str:
    """
    Returns VARIANCE_0 if expected == actual, else OPEN_VARIANCE.
    Used in the SAGCO language stdlib.
    """
    var = compute_variance(expected, actual)
    return VARIANCE_0 if var == 0.0 else OPEN_VARIANCE


class ERUResult:
    """A full ERU analysis result."""

    def __init__(self, item_id, expected, actual, label: str, variance: float, notes: str = ""):
        self.item_id = item_id
        self.expected = expected
        self.actual = actual
        self.label = label
        self.variance = variance
        self.notes = notes

    def to_dict(self) -> dict:
        return {
            "id": self.item_id,
            "expected": self.expected,
            "actual": self.actual,
            "variance": self.variance,
            "eru": self.label,
            "notes": self.notes,
        }

    def __repr__(self):
        return f"ERUResult(id={self.item_id!r}, eru={self.label!r}, var={self.variance})"


def run_eru_on_rows(
    rows: list,
    expected_field: str = "Expected Price",
    actual_field: str = "Actual Price",
    id_field: str = "ID",
    pass_threshold: float = 0,
    partial_threshold: float = 5,
) -> list:
    """
    Run ERU analysis on a list of dicts.
    Returns list of ERUResult objects.
    """
    results = []
    for row in rows:
        item_id = row.get(id_field, "?")
        expected = row.get(expected_field, "")
        actual = row.get(actual_field, "")
        var = compute_variance(expected, actual)
        label = eru_label(expected, actual, pass_threshold, partial_threshold)
        results.append(ERUResult(item_id, expected, actual, label, var))
    return results


def eru_summary(results: list) -> dict:
    """Summarize ERU results."""
    total = len(results)
    passes = sum(1 for r in results if r.label == ERU_PASS)
    partials = sum(1 for r in results if r.label == ERU_PARTIAL)
    fails = sum(1 for r in results if r.label == ERU_FAIL)
    variances = [r.variance for r in results]
    mean_var = sum(variances) / total if total else 0
    return {
        "total": total,
        "PASS": passes,
        "PARTIAL": partials,
        "FAIL": fails,
        "pass_rate": round(passes / total * 100, 1) if total else 0,
        "mean_variance": round(mean_var, 4),
    }
