def generate_questions(resume_text: str, job_text: str):
    return {
        "hr": [
            "Tell me about yourself.",
            "Why do you want this role?"
        ],
        "technical": [
            "Explain the key skills mentioned in the job description.",
            "Describe one project from your resume relevant to this role."
        ],
        "behavioral": [
            "Describe a challenge you faced and how you handled it."
        ]
    }
