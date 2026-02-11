from app.nlp import extract_skills

def generate_questions(resume_text: str, job_text: str):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    questions = {
        "hr": [
            "Tell me about yourself.",
            "Why do you think you are a good fit for this role?",
            "What are your strengths and weaknesses?"
        ],
        "project_based": [
            "Explain one project from your resume that best matches this job role.",
            "What technical challenges did you face in your projects and how did you solve them?"
        ],
        "technical": [],
        "gap_based": []
    }

    for skill in matched_skills:
        questions["technical"].append(
            f"Explain your experience with {skill} and how you have used it in real-world projects."
        )

    for skill in missing_skills:
        questions["gap_based"].append(
            f"The job requires {skill}. How would you plan to learn or upskill in this area?"
        )

    return questions
s