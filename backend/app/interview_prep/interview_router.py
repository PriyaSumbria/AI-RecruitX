from fastapi import APIRouter, Form
from .question_generator import generate_questions
from .answer_evaluator import evaluate_answer
from .session_service import create_session, submit_answer, get_summary


router = APIRouter(prefix="/interview", tags=["Interview Prep"])

@router.post("/questions")
def get_questions(resume_text: str = Form(...), job_text: str = Form(...)):
    return generate_questions(resume_text, job_text)

@router.post("/evaluate")
def evaluate(
    question: str = Form(...),
    answer: str = Form(...),
    job_text: str = Form(...)
):
    return evaluate_answer(question, answer, job_text)

@router.post("/start")
def start(resume_text: str = Form(...), job_text: str = Form(...)):
    return create_session(resume_text, job_text)


@router.post("/submit")
def submit(
    session_id: str = Form(...),
    question: str = Form(...),
    answer: str = Form(...),
    job_text: str = Form(...)
):
    return submit_answer(session_id, question, answer, job_text)


@router.get("/summary/{session_id}")
def summary(session_id: str):
    return get_summary(session_id)
