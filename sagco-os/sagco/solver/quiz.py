"""
Quiz generator: flashcards → quiz.csv with 4-option MCQ.
Uses stdlib random only.
"""
import csv
import os
import random


def make_mcq(correct_answer: str, all_answers: list, n_options: int = 4) -> dict:
    """
    Generate a multiple-choice question with n_options.
    Returns dict with correct, options (list), correct_index.
    """
    # Get distractors from all_answers excluding the correct one
    distractors = [a for a in all_answers if a != correct_answer]
    random.shuffle(distractors)
    distractors = distractors[: n_options - 1]

    # If not enough distractors, pad with generic ones
    generic_fillers = ["$5", "$10", "$15", "$20", "$25", "$30", "$35", "$40"]
    while len(distractors) < n_options - 1:
        filler = random.choice(generic_fillers)
        if filler not in distractors and filler != correct_answer:
            distractors.append(filler)

    options = distractors + [correct_answer]
    random.shuffle(options)
    correct_index = options.index(correct_answer)

    return {
        "options": options,
        "correct": correct_answer,
        "correct_index": correct_index,
        "correct_letter": "ABCD"[correct_index],
    }


def flashcards_to_quiz(cards: list) -> list:
    """
    Convert flashcard list to quiz questions (4-option MCQ).
    Returns list of quiz question dicts.
    """
    all_answers = [c.get("back", c.get("price", "?")) for c in cards]
    quiz_rows = []
    for card in cards:
        answer = card.get("back", f"${card.get('price', '?')} — {card.get('category', '')}")
        mcq = make_mcq(answer, all_answers)
        quiz_rows.append({
            "id": card.get("id", ""),
            "category": card.get("category", ""),
            "item": card.get("item", ""),
            "question": card.get("front", ""),
            "correct_answer": answer,
            "option_a": mcq["options"][0],
            "option_b": mcq["options"][1],
            "option_c": mcq["options"][2],
            "option_d": mcq["options"][3],
            "correct_letter": mcq["correct_letter"],
            "mnemonic": card.get("mnemonic", ""),
            "eru": card.get("eru", ""),
        })
    return quiz_rows


def save_quiz_csv(quiz_rows: list, path: str):
    """Save quiz to CSV."""
    if not quiz_rows:
        return
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    fieldnames = list(quiz_rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(quiz_rows)
