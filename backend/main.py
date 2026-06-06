"""
backend/main.py

FastAPI application entry point.

Endpoints:
  GET  /health          — liveness check
  POST /analyze         — analyse resume PDF + job description text
  POST /analyze-text    — analyse plain text resume + job description (no PDF)
"""
import os
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from backend.schemas.output import AnalysisResponse, MatchRequest
from backend.services.pdf_parser import extract_text_from_pdf
from backend.graph.workflow import run_workflow

app = FastAPI(
    title="Resume–JD Matcher API",
    description="Agentic career coaching API powered by LangGraph + Groq (Llama 3.3 70B)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
def health_check():
    """Returns service liveness and the configured LLM model name."""
    return {
        "status": "ok",
        "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    }


# ── PDF + JD analysis ─────────────────────────────────────────────────────────

@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze(
    resume: UploadFile = File(..., description="Candidate resume as a PDF file"),
    job_description: str = Form(..., description="Job description text"),
):
    """
    Full pipeline analysis:
    - Upload a PDF resume
    - Paste job description text
    - Returns a FinalReport from all 6 agents
    """
    # Validate file type
    allowed_types = {"application/pdf", "application/octet-stream"}
    if resume.content_type not in allowed_types and not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Validate inputs
    if len(job_description.strip()) < 30:
        raise HTTPException(status_code=422, detail="Job description is too short (min 30 chars).")

    # Extract text from PDF
    raw_bytes = await resume.read()
    try:
        resume_text = extract_text_from_pdf(raw_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF parsing error: {exc}")

    # Save upload to /uploads (optional persistence)
    upload_path = os.path.join("uploads", resume.filename)
    try:
        with open(upload_path, "wb") as f:
            f.write(raw_bytes)
    except Exception:
        pass  # Non-fatal — file saving is best-effort

    # Run agent pipeline
    try:
        report = run_workflow(resume_text, job_description)
        return AnalysisResponse(success=True, report=report)
    except RuntimeError as exc:
        return AnalysisResponse(success=False, error=str(exc))
    except Exception as exc:
        return AnalysisResponse(success=False, error=f"Unexpected error: {exc}")


# ── Plain text analysis (no PDF) ──────────────────────────────────────────────

@app.post("/analyze-text", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_text(payload: MatchRequest):
    """
    Text-only analysis endpoint — useful for testing without a PDF.
    Supply raw resume text and job description as JSON body.
    """
    if len(payload.resume_text.strip()) < 50:
        raise HTTPException(status_code=422, detail="Resume text is too short (min 50 chars).")
    if len(payload.job_description.strip()) < 30:
        raise HTTPException(status_code=422, detail="Job description is too short (min 30 chars).")

    try:
        report = run_workflow(payload.resume_text, payload.job_description)
        return AnalysisResponse(success=True, report=report)
    except RuntimeError as exc:
        return AnalysisResponse(success=False, error=str(exc))
    except Exception as exc:
        return AnalysisResponse(success=False, error=f"Unexpected error: {exc}")


# ── Dev runner ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=os.getenv("FASTAPI_HOST", "0.0.0.0"),
        port=int(os.getenv("FASTAPI_PORT", 8000)),
        reload=True,
    )
