from app.nlp import extract_skills

def match_resume_to_job(resume_text: str, job_text: str):
    """
    Baseline match using keyword overlap of canonical skills.
    match_score = fraction of job skills present in resume (0-100)
    """
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    match_score = round(len(matched) / max(len(job_skills), 1) * 100, 2)
    return {
        "match_score": match_score,
        "matched_skills": matched,
        "missing_skills": missing
    }
