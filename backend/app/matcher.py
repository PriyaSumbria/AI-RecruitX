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


# backend/app/matcher.py
from app.nlp import extract_skills
from app.semantic_matcher import semantic_score_percent
from typing import Dict, Any

def keyword_score_percent(resume_text: str, job_text: str) -> float:
    """
    Compute keyword overlap score as percentage:
    fraction of job skills present in resume (0-100)
    """
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))
    if not job_skills:
        # if job has no explicit skills, fallback to 0
        return 0.0
    matched = resume_skills & job_skills
    score = len(matched) / len(job_skills)
    return round(score * 100.0, 2)


def hybrid_match(resume_text: str, job_text: str, weight_semantic: float = 0.6) -> Dict[str, Any]:
    """
    Hybrid match combining semantic similarity and keyword overlap.
    weight_semantic: fraction given to semantic score (0..1)
    returns dict with semantic_score, keyword_score, final_score, matched, missing
    """
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)

    semantic = semantic_score_percent(resume_text, job_text)  # 0..100
    keyword = keyword_score_percent(resume_text, job_text)    # 0..100

    w = float(weight_semantic)
    final = round((w * semantic + (1.0 - w) * keyword), 2)

    return {
        "semantic_score": semantic,
        "keyword_score": keyword,
        "final_score": final,
        "matched_skills": matched,
        "missing_skills": missing
    }
