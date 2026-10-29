from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from analyzer import analyze_resume

app = FastAPI(
    title="AI Career Companion API",
    description=(
        "Analyzes a resume against a job description "
        "using NLP and skill extraction."
    ),
    version="1.0.0"
)

class AnalysisRequest(BaseModel):
    resume_text: str = Field(
        min_length=30,
        max_length=50_000
    )

    job_description: str = Field(
        min_length=30,
        max_length=50_000
    )

@app.get("/")
def home():
    return {
        "application": "AI Career Companion",
        "status": "running",
        "documentation": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/api/analyze")
def analyze(request: AnalysisRequest):
    try:
        result = analyze_resume(
            request.resume_text,
            request.job_description
        )

        return result

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=500,
            detail="The skills dataset could not be found."
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="The resume analysis could not be completed."
        ) from error