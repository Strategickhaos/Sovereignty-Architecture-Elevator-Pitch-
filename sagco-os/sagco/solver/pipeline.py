"""
SAGCO Solver Pipeline.
Orchestrates: extract → classify → normalize → ERU → flashcards → quiz → summary.
"""
import os


class SolverPipeline:
    """
    Full SAGCO solver pipeline.
    Usage:
        pipe = SolverPipeline(input_path="data/menu.xlsx", output_dir="outputs/")
        result = pipe.run()
    """

    def __init__(self, input_path: str, output_dir: str = "outputs/"):
        self.input_path = input_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def run(self) -> dict:
        """Execute the full pipeline. Returns result dict."""
        result = {
            "input": self.input_path,
            "steps": [],
            "rows": 0,
            "flashcards": 0,
            "quiz_questions": 0,
            "eru_summary": {},
            "outputs": [],
        }

        # Step 1: Extract
        from sagco.core.extractor import extract
        rows = extract(self.input_path)
        result["rows"] = len(rows)
        result["steps"].append(f"Extracted {len(rows)} rows from {self.input_path}")

        if not rows:
            result["steps"].append("No rows found — aborting pipeline")
            return result

        # Step 2: Classify
        from sagco.core.classifier import classify_rows
        classified = classify_rows(rows)
        result["steps"].append(f"Classified {len(classified)} rows")

        # Step 3: Normalize menu categories
        from sagco.solver.menus import normalize_rows
        rows = normalize_rows(rows)
        result["steps"].append("Normalized categories")

        # Step 4: ERU analysis
        from sagco.core.eru import run_eru_on_rows, eru_summary
        eru_results = run_eru_on_rows(rows)
        summary = eru_summary(eru_results)
        result["eru_summary"] = summary
        result["steps"].append(
            f"ERU: {summary['PASS']} PASS / {summary['PARTIAL']} PARTIAL / {summary['FAIL']} FAIL"
        )

        # Step 5: Generate flashcards
        from sagco.solver.flashcards import rows_to_flashcards, save_flashcards_csv
        cards = rows_to_flashcards(rows)
        flashcard_path = os.path.join(self.output_dir, "flashcards.csv")
        save_flashcards_csv(cards, flashcard_path)
        result["flashcards"] = len(cards)
        result["outputs"].append(flashcard_path)
        result["steps"].append(f"Generated {len(cards)} flashcards → {flashcard_path}")

        # Step 6: Generate quiz
        from sagco.solver.quiz import flashcards_to_quiz, save_quiz_csv
        quiz_rows = flashcards_to_quiz(cards)
        quiz_path = os.path.join(self.output_dir, "quiz.csv")
        save_quiz_csv(quiz_rows, quiz_path)
        result["quiz_questions"] = len(quiz_rows)
        result["outputs"].append(quiz_path)
        result["steps"].append(f"Generated {len(quiz_rows)} quiz questions → {quiz_path}")

        # Step 7: Summary report
        from sagco.solver.summary import generate_summary
        summary_path = os.path.join(self.output_dir, "summary.md")
        report = generate_summary(rows, eru_results, summary_path)
        result["outputs"].append(summary_path)
        result["steps"].append(f"Summary report → {summary_path}")

        return result


def run_demo(output_dir: str = "outputs/") -> dict:
    """Run the solver on the built-in Water Street menu."""
    demo_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "water_street_menu.yaml")
    demo_path = os.path.normpath(demo_path)
    if not os.path.exists(demo_path):
        # Fall back to flashcards CSV
        demo_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "oyster_flashcards.csv")
        demo_path = os.path.normpath(demo_path)
    pipe = SolverPipeline(demo_path, output_dir)
    return pipe.run()
