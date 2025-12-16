import json
import re
import os

# Load the large ESCO library
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "skills_library.json")

with open(DATA_PATH, "r") as f:
    SKILL_DATA = json.load(f)
    # Create sets for faster lookup
    TECH_LOOKUP = set(SKILL_DATA["technical"])
    SOFT_LOOKUP = set(SKILL_DATA["soft"])

def extract_skills(text: str):
    text = (text or "").lower()
    
    # Simple mapping for common variations (you can expand this)
    text = text.replace("reactjs", "react").replace("nodejs", "node.js")

    found_tech = []
    found_soft = []

    # Combine all skills into one big list for a single pass search
    # This is much faster than running thousands of individual regex searches
    all_known_skills = SKILL_DATA["technical"] + SKILL_DATA["soft"]
    
    # Use a boundary-aware search
    for skill in all_known_skills:
        if skill in text: # Fast check first
            if re.search(r"\b" + re.escape(skill) + r"\b", text):
                if skill in TECH_LOOKUP:
                    found_tech.append(skill)
                else:
                    found_soft.append(skill)

    return {
        "technical": sorted(list(set(found_tech))),
        "soft": sorted(list(set(found_soft)))
    }