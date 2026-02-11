import re
from app.nlp import extract_skills


WEAK_PHRASES = ["maybe", "i think", "kind of", "sort of", "probably"]
STRONG_VERBS = ["implemented", "designed", "optimized", "built", "developed", "trained", "deployed"]
STAR_KEYWORDS = ["situation", "task", "action", "result"]


def evaluate_answer(question: str, answer: str, job_text: str):
    answer_lower = answer.lower()
    question_lower = question.lower()

    # ---------- 1️⃣ Relevance ----------
    question_words = set(question_lower.split())
    answer_words = set(answer_lower.split())
    overlap = len(question_words.intersection(answer_words))
    relevance_score = min((overlap / (len(question_words) + 1)) * 100, 100)

    # ---------- 2️⃣ Depth ----------
    word_count = len(answer_words)
    depth_score = min((word_count / 120) * 100, 100)

    technical_hits = sum(1 for verb in STRONG_VERBS if verb in answer_lower)
    depth_score += technical_hits * 5
    depth_score = min(depth_score, 100)

    # ---------- 3️⃣ Structure (STAR) ----------
    star_hits = sum(1 for word in STAR_KEYWORDS if word in answer_lower)

    number_presence = bool(re.search(r"\d+%|\d+", answer_lower))

    structure_score = star_hits * 20
    if number_presence:
        structure_score += 20

    structure_score = min(structure_score, 100)

    # ---------- 4️⃣ Confidence ----------
    weak_hits = sum(1 for phrase in WEAK_PHRASES if phrase in answer_lower)
    confidence_score = max(100 - (weak_hits * 15), 0)

    # ---------- Final Score ----------
    final_score = (
        0.35 * relevance_score +
        0.30 * depth_score +
        0.20 * structure_score +
        0.15 * confidence_score
    )

    feedback = []

    if relevance_score < 50:
        feedback.append("Your answer is not strongly aligned with the question.")
    if depth_score < 50:
        feedback.append("Try adding more technical depth and explanation.")
    if structure_score < 40:
        feedback.append("Structure your answer using the STAR method.")
    if confidence_score < 70:
        feedback.append("Avoid weak phrases like 'maybe' or 'I think'.")

    if not feedback:
        feedback.append("Strong and well-structured response.")

    return {
        "final_score": round(final_score, 2),
        "relevance_score": round(relevance_score, 2),
        "depth_score": round(depth_score, 2),
        "structure_score": round(structure_score, 2),
        "confidence_score": round(confidence_score, 2),
        "feedback": feedback
    }
