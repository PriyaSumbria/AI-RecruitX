from sqlalchemy import Column, String, Float, Text
from .db import Base
import uuid


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    average_score = Column(Float, default=0.0)


class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String)
    question = Column(Text)
    answer = Column(Text)
    final_score = Column(Float)

