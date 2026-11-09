from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from analyzer import analyze_resume


# Project paths
BASE_DIRECTORY = Path(__file__).resolve().parent
FRONTEND_DIRECTORY = BASE_DIRECTORY / "frontend"
MAIN_PAGE = FRONTEND_DIRECTORY / "mainpage.html"


# Verify frontend files when the server starts
if not FRONTEND_DIRECTORY.is_dir():
    raise RuntimeError(
        f"Frontend folder not found: {FRONTEND_DIRECTORY}"
    )

if not MAIN_PAGE.is_file():
    raise RuntimeError(
        f"Main page not found: {MAIN_PAGE}"
    )


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


# Make files inside frontend available through /static
app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIRECTORY)),
    name="static"
)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(str(MAIN_PAGE))


@app.get("/api/health")
def health_check():
    return {
        "application": "AI Career Companion",
        "status": "healthy"
    }


@app.post("/api/analyze")
def analyze(request: AnalysisRequest):
    try:
        return analyze_resume(
            request.resume_text,
            request.job_description
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=500,
            detail="The skills dataset could not be found."
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="The analysis could not be completed."
        ) from error