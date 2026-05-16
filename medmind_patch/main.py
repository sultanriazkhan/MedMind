from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pathlib import Path

from pipeline.ingest import process_uploaded_file, process_text_input
from pipeline.extract import extract_lab_tests
from pipeline.interpreter import enrich_lab_tests
from pipeline.report_summary import build_report_summary
from db.sqlite import save_result, get_recent_results

app = FastAPI(
    title="MedMind Lab Processing System",
    version="2.0.0",
    description="Ontology-driven medical lab processing with OCR support",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5000",
        "http://localhost:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UI_PATH = Path(__file__).parent / "ui" / "index.html"


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    if UI_PATH.exists():
        return HTMLResponse(content=UI_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>MedMind API is running</h1>")


@app.post("/process")
async def process_lab_results(
    file: Optional[UploadFile] = File(None),
    text_input: Optional[str] = Form(None),
):
    try:
        if file:
            source_type, raw_text = process_uploaded_file(
                await file.read(),
                file.content_type
            )
        elif text_input:
            source_type, raw_text = process_text_input(text_input)
        else:
            raise HTTPException(status_code=400, detail="No input provided")

        extracted_tests = extract_lab_tests(raw_text)
        tests = enrich_lab_tests(extracted_tests)

        summary = {
            "total": len(tests),
            "high_confidence": 0,
            "low_confidence": 0,
        }

        for test in tests:
            if test.get("confidence", 0) >= 0.8:
                summary["high_confidence"] += 1
            else:
                summary["low_confidence"] += 1

        patient_summary = build_report_summary(tests)
        summary["patient_summary"] = patient_summary

        save_result(source_type, raw_text[:500], tests, summary)

        return {
            "success": True,
            "source_type": source_type,
            "raw_text": raw_text[:500] + ("..." if len(raw_text) > 500 else ""),
            "tests": tests,
            "summary": summary,
            "patient_summary": patient_summary,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )


@app.get("/recent-results")
async def recent_results():
    try:
        return {
            "success": True,
            "results": get_recent_results(limit=10)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "MedMind FastAPI Processing Backend",
        "version": "2.0.0",
    }