from fastapi import APIRouter, Form
from .question_generator import generate_questions
from .answer_evaluator import evaluate_answer

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
