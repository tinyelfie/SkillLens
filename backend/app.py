from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import tempfile
import time
from fastapi.middleware.cors import CORSMiddleware

from extraction.text_extractor import extract_text
from pipeline.run_pipeline import run_pipeline
from backend.schemas import ATSResponse

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"

# ---------------- app ----------------
app = FastAPI(title="LLM-RAG ATS")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend at /ui/* and redirect root to it
app.mount("/ui", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def serve_index():
    """Redirect root to the frontend index.html."""
    return FileResponse(str(FRONTEND_DIR / "index.html"))


# ---------------- request schema (text-based) ----------------
class ATSRequest(BaseModel):
    resume_text: str
    jd_text: str


# ---------------- health check ----------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------- text-based pipeline endpoint ----------------
@app.post("/analyze", response_model=ATSResponse)
def analyze_resume(request: ATSRequest):
    """
    Accepts resume_text and jd_text as strings.
    Useful for testing and internal calls.
    """

    start_time = time.time()

    result = run_pipeline(
        resume_text=request.resume_text,
        jd_text=request.jd_text
    )

    processing_time_ms = int((time.time() - start_time) * 1000)

    return ATSResponse(
        **result,
        processing_time_ms=processing_time_ms
    )


# ---------------- file-based pipeline endpoint ----------------
@app.post("/analyze-files", response_model=ATSResponse)
def analyze_files(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):
    """
    Accepts resume and JD as PDF/DOCX files.
    Extracts text and calls the same pipeline.
    """

    allowed_extensions = {".pdf", ".docx"}

    resume_suffix = Path(resume.filename).suffix.lower()
    jd_suffix = Path(jd.filename).suffix.lower()

    if resume_suffix not in allowed_extensions or jd_suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    # ---------- save files temporarily ----------
    with tempfile.NamedTemporaryFile(delete=False, suffix=resume_suffix) as r_tmp:
        r_tmp.write(resume.file.read())
        resume_path = Path(r_tmp.name)

    with tempfile.NamedTemporaryFile(delete=False, suffix=jd_suffix) as j_tmp:
        j_tmp.write(jd.file.read())
        jd_path = Path(j_tmp.name)

    start_time = time.time()

    try:
        # ---------- extract text ----------
        resume_text = extract_text(resume_path)
        jd_text = extract_text(jd_path)

        if not resume_text.strip() or not jd_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Failed to extract text from one or more files"
            )

        # ---------- call pipeline ----------
        try:
            result = run_pipeline(resume_text, jd_text)
        except RuntimeError as e:
            raise HTTPException(status_code=503, detail=str(e))

        processing_time_ms = int((time.time() - start_time) * 1000)

        return ATSResponse(
            **result,
            processing_time_ms=processing_time_ms
        )

    finally:
        # ---------- cleanup ----------
        resume_path.unlink(missing_ok=True)
        jd_path.unlink(missing_ok=True)


# ---------------- optimized resume download ----------------
@app.post("/download-optimized-resume")
def download_optimized_resume(request: ATSRequest):
    """
    Generates optimized resume and returns it as a downloadable text file.
    """

    result = run_pipeline(
        resume_text=request.resume_text,
        jd_text=request.jd_text
    )

    optimized_text = result["optimized_resume"]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".txt",
        mode="w",
        encoding="utf-8"
    ) as tmp:
        tmp.write(optimized_text)
        file_path = tmp.name

    return FileResponse(
        path=file_path,
        filename="optimized_resume.txt",
        media_type="text/plain"
    )
