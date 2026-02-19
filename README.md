AI-RecruitX
Hybrid NLP-Based Interview Intelligence Platform
 Overview

AI-RecruitX is an AI-powered recruitment assistance platform designed to evaluate resume-job alignment and simulate structured technical interviews using a hybrid NLP scoring engine.

The system combines rule-based evaluation and semantic similarity techniques to provide intelligent, structured, and explainable candidate feedback.

 Problem Statement

Traditional resume screening and interview evaluation processes are:

Subjective

Time-consuming

Inconsistent

Dependent on keyword matching

AI-RecruitX introduces a semantic and structured AI-driven scoring framework to make evaluation more objective and scalable.

 System Architecture

User → FastAPI Backend → Hybrid NLP Evaluation Engine → SQLite Database

Core Modules

Resume-Job Semantic Matching

AI-Based Interview Question Generation

Hybrid Answer Evaluation Engine

Persistent Interview Session Tracking

 Hybrid Evaluation Model

The interview evaluation engine uses a weighted hybrid approach:

Rule-Based Components

Relevance Score (keyword overlap)

Depth Score (technical richness & impact)

Structure Score (STAR method detection)

Confidence Score (weak phrase detection)

AI-Based Component

TF-IDF Vectorization

Cosine Similarity

Semantic Alignment Scoring

Final Score

Weighted combination of rule-based metrics and semantic similarity.

This enables structured, explainable, and context-aware evaluation.

 Tech Stack

Python

FastAPI

SQLAlchemy

SQLite

Scikit-learn (TF-IDF + Cosine Similarity)

Uvicorn

 Key Features

Semantic resume-job matching

AI-generated interview questions

Hybrid NLP-based answer evaluation

Structured feedback generation

Persistent interview session storage

Modular API-based backend architecture

How to Run
git clone https://github.com/PriyaSumbria/AI-RecruitX.git
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload


Open API documentation:

http://127.0.0.1:8000/docs

 Future Scope

Speech-to-text integration for voice interviews

Emotion detection module

Recruiter analytics dashboard

Cloud deployment (PostgreSQL + Docker)

Bias and fairness evaluation improvements

 Project Structure
AI-RecruitX/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│
├── frontend/
├── docs/
└── README.md

 Author

Priya Sumbria
Computer Science Engineering
AI/ML Enthusiast

