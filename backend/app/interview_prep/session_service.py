from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.database.models import InterviewSession, InterviewAnswer
from .question_generator import generate_questions
from .answer_evaluator import evaluate_answer


def create_session(resume_text: str, job_text: str):
    db: Session = SessionLocal()

    session = InterviewSession()
    db.add(session)
    db.commit()
    db.refresh(session)

    questions = generate_questions(resume_text, job_text)

    db.close()

    return {
        "session_id": session.id,
        "questions": questions
    }


def submit_answer(session_id: str, question: str, answer: str, job_text: str):
    db: Session = SessionLocal()

    evaluation = evaluate_answer(question, answer, job_text)

    record = InterviewAnswer(
        session_id=session_id,
        question=question,
        answer=answer,
        final_score=evaluation["final_score"]
    )

    db.add(record)
    db.commit()
    db.close()

    return evaluation


def get_summary(session_id: str):
    db: Session = SessionLocal()

    answers = db.query(InterviewAnswer).filter(
        InterviewAnswer.session_id == session_id
    ).all()

    if not answers:
        db.close()
        return {"message": "No answers yet."}

    avg_score = sum(a.final_score for a in answers) / len(answers)

    db.close()

    return {
        "total_questions": len(answers),
        "average_score": round(avg_score, 2)
    }
