def evaluate_answer(answer: str):
    score = min(len(answer.split()) / 10, 10)

    return {
        "score": round(score, 2),
        "feedback": "Try to be more structured and concise."
    }
