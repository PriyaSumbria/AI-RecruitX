from fastapi import FastAPI

app = FastAPI(title="AI-RecruitX")

@app.get("/")
def root():
    return {"status": "AI-RecruitX Phase 0 setup successful"}
