"""
MedMind Core Engine
FastAPI single entry point
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
from pathlib import Path

from pipeline.ingest import process_uploaded_file, process_text_input
from pipeline.extract import extract_lab_tests
from db.sqlite import save_result

app = FastAPI(
    title="MedMind Lab Processing System",
    version="2.0.0",
    description="Ontology-driven medical lab processing with OCR support",
)

UI_PATH = Path(__file__).parent / "ui" / "index.html"


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    if UI_PATH.exists():
        return HTMLResponse(content=UI_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>UI not found</h1>", status_code=404)


@app.post("/process")
async def process_lab_results(
    file: Optional[UploadFile] = File(None),
    text_input: Optional[str] = Form(None),
):
    try:
        if file:
            source_type, raw_text = process_uploaded_file(
                await file.read(), file.content_type
            )
        elif text_input:
            source_type, raw_text = process_text_input(text_input)
        else:
            raise HTTPException(status_code=400, detail="No input provided")

        tests = extract_lab_tests(raw_text)

        summary = {"total": len(tests), "high_confidence": 0, "low_confidence": 0}
        for t in tests:
            if t["confidence"] >= 0.8:
                summary["high_confidence"] += 1
            else:
                summary["low_confidence"] += 1

        save_result(source_type, raw_text[:500], tests, summary)

        return {
            "source_type": source_type,
            "raw_text": raw_text[:500] + ("..." if len(raw_text) > 500 else ""),
            "tests": tests,
            "summary": summary,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "MedMind", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")