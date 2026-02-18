from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.parsers import pdf_to_text
from app.nlp import extract_skills
from app.matcher import hybrid_match

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
async def upload_resume(
    file: UploadFile | None = File(None),
    paste_text: str | None = Form(None)
):
    if file:
        if file.content_type != "application/pdf":
            return JSONResponse(
                {"error": "Only PDF supported for file upload"},
                status_code=400
            )
        raw_text = await pdf_to_text(file)
    elif paste_text:
        raw_text = paste_text
    else:
        return JSONResponse(
            {"error": "Provide a PDF file or paste_text"},
            status_code=400
        )

    skills = extract_skills(raw_text)
    return {"parsed_text": raw_text, "skills": skills}

@app.post("/match")
async def match(resume_text: str = Form(...), job_text: str = Form(...)):
    return hybrid_match(resume_text, job_text)

@app.post("/ai_match")
async def ai_match(
    resume_text: str = Form(...),
    job_text: str = Form(...),
    weight_semantic: float = Form(0.6)
):
    try:
        w = float(weight_semantic)
        if not 0 <= w <= 1:
            w = 0.6
    except Exception:
        w = 0.6

    result = hybrid_match(resume_text, job_text, weight_semantic=w)
    result["is_suitable"] = result["final_score"] >= 75.0
    result["recommendation"] = (
        "Ready for Interview" if result["is_suitable"]
        else "Needs skill improvement"
    )
    return result

from app.interview_prep.interview_router import router as interview_router
app.include_router(interview_router)

from app.database.db import engine
from app.database import models

models.Base.metadata.create_all(bind=engine)
