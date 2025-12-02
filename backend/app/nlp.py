import re

# Starter canonical skills list. Expand later to skills.json (~200-500).
SKILLS = [
    "python","pandas","numpy","sql","java","c++","javascript","react",
    "angular","nodejs","docker","kubernetes","git","linux","aws",
    "machine learning","deep learning","tensorflow","pytorch","scikit-learn"
]

def extract_skills(text: str):
    """
    Naive keyword matching for canonical skills.
    Returns sorted list of detected canonical skills.
    """
    text = (text or "").lower()
    found = set()
    for skill in SKILLS:
        # Use word-boundary match to avoid substring false positives
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.add(skill)
    return sorted(found)
