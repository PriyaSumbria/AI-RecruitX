from app.nlp import extract_skills
from app.semantic_matcher import semantic_score_percent

def hybrid_match(resume_text, job_text, weight_semantic=0.6):
    # Extract categorized skills for both
    res_cats = extract_skills(resume_text)
    job_cats = extract_skills(job_text)

    # Helper to calculate overlap
    def calculate_metrics(res_list, job_list):
        res_set, job_set = set(res_list), set(job_list)
        matched = sorted(list(res_set & job_set))
        missing = sorted(list(job_set - res_set))
        score = (len(matched) / len(job_set) * 100) if job_set else 100
        return score, matched, missing

    # Calculate scores for both categories
    t_score, t_matched, t_missing = calculate_metrics(res_cats["technical"], job_cats["technical"])
    s_score, s_matched, s_missing = calculate_metrics(res_cats["soft"], job_cats["soft"])

    # Final Keyword Score (weighted: 70% Tech, 30% Soft)
    keyword_score = round((t_score * 0.7) + (s_score * 0.3), 2)
    
    # Semantic Score (AI meaning)
    semantic_score = semantic_score_percent(resume_text, job_text)

    # Final Hybrid Score
    final_score = round((weight_semantic * semantic_score) + ((1 - weight_semantic) * keyword_score), 2)

    return {
        "final_score": final_score,
        "is_suitable": final_score >= 60.0,
        "detail": {
            "technical_score": round(t_score, 2),
            "soft_score": round(s_score, 2),
            "semantic_score": semantic_score
        },
        "matched_skills": t_matched + s_matched,
        "missing_technical": t_missing,
        "missing_soft": s_missing
    }