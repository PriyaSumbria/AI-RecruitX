from fastapi import FastAPI

app = FastAPI(title="AI-RecruitX")

@app.get("/")
def root():
    return {"status": "AI-RecruitX Phase 0 setup successful"}
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.parsers import pdf_to_text
from app.nlp import extract_skills
from app.matcher import match_resume_to_job
from app.matcher import match_resume_to_job, hybrid_match

app = FastAPI(title="AI-RecruitX")

# Allow local frontend dev (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "AI-RecruitX backend running"}

@app.post("/upload_resume")
async def upload_resume(file: UploadFile | None = File(None), paste_text: str | None = Form(None)):
    """
    Accept either a PDF upload (file) or pasted text (paste_text).
    Returns parsed_text and detected skills.
    """
    if file:
        # Basic MIME check; we only require PDF for file path
        if file.content_type != "application/pdf":
            return JSONResponse({"error": "Only PDF supported for file upload"}, status_code=400)
        raw_text = await pdf_to_text(file)
    elif paste_text:
        raw_text = paste_text
    else:
        return JSONResponse({"error": "Provide a PDF file or paste_text"}, status_code=400)

    skills = extract_skills(raw_text)
    return {"parsed_text": raw_text, "skills": skills}

@app.post("/match")
async def match(resume_text: str = Form(...), job_text: str = Form(...)):
    """
    Simple baseline match endpoint (keyword overlap).
    """
    result = match_resume_to_job(resume_text, job_text)
    return result


@app.post("/ai_match")
async def ai_match(resume_text: str = Form(...), job_text: str = Form(...), weight_semantic: float = Form(0.6)):
    """
    AI-powered hybrid match. weight_semantic: 0..1 (default 0.6)
    Returns semantic_score, keyword_score, final_score (all 0..100) and skill lists.
    """
    try:
        w = float(weight_semantic)
        if w < 0 or w > 1:
            w = 0.6
    except Exception:
        w = 0.6

    result = hybrid_match(resume_text, job_text, weight_semantic=w)
    return result
