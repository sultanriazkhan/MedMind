"""
MedMind Core Engine - SINGLE ENTRY POINT
FastAPI only - No orchestrator - No background services
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import os
from pathlib import Path

# Import pipeline modules
from pipeline.ingest import process_uploaded_file, process_text_input
from pipeline.extract import extract_lab_tests
from pipeline.classify import classify_test
from db.sqlite import save_result

# Initialize FastAPI
app = FastAPI(
    title="MedMind Lab Processing System",
    version="1.0.0",
    description="Deterministic medical lab processing with OCR support"
)

# Serve UI
UI_PATH = Path(__file__).parent / "ui" / "index.html"

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serve the main UI"""
    if UI_PATH.exists():
        with open(UI_PATH, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    else:
        return HTMLResponse(content="<h1>UI not found</h1>", status_code=404)

@app.post("/process")
async def process_lab_results(
    file: Optional[UploadFile] = None,
    text_input: Optional[str] = Form(None)
):
    """
    Main processing endpoint
    
    Handles:
    - File uploads (images, PDF, DOCX, TXT)
    - Pasted text
    - OCR for images
    - Deterministic test extraction
    """
    try:
        # STEP 1-2: Ingestion + OCR
        if file:
            file_content = await file.read()
            source_type, raw_text = process_uploaded_file(file_content, file.content_type)
        elif text_input:
            source_type, raw_text = process_text_input(text_input)
        else:
            raise HTTPException(status_code=400, detail="No input provided")
        
        # STEP 3-4: Extract tests
        extracted_tests = extract_lab_tests(raw_text)
        
        # STEP 5-6: Classify and get explanations
        processed_tests = []
        summary = {"total_tests": 0, "normal": 0, "abnormal": 0, "critical": 0}
        
        for test in extracted_tests:
            if test["canonical_name"]:
                classification = classify_test(test["canonical_name"], test["value"])
                
                # Update summary
                if "critical" in classification["status"].lower():
                    summary["critical"] += 1
                    summary["abnormal"] += 1
                elif classification["status"].lower() != "normal":
                    summary["abnormal"] += 1
                else:
                    summary["normal"] += 1
                summary["total_tests"] += 1
                
                processed_tests.append({
                    "name": test["canonical_name"].title(),
                    "value": test["value"],
                    "unit": classification["reference_range"].split()[-1] if classification["reference_range"] != "N/A" else "",
                    "status": classification["status"],
                    "reference_range": classification["reference_range"],
                    "explanation": classification["explanation"]
                })
        
        # Save to database
        save_result(source_type, raw_text[:500], processed_tests, summary)
        
        return {
            "source_type": source_type,
            "raw_text": raw_text[:500] + "..." if len(raw_text) > 500 else raw_text,
            "tests": processed_tests,
            "summary": summary
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MedMind Lab System",
        "version": "1.0.0",
        "architecture": "single-service"
    }

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🏥 MedMind Lab Processing System v1.0")
    print("=" * 60)
    print("✅ SINGLE SERVICE (FastAPI only)")
    print("✅ NO orchestrator | NO background watchers")
    print("✅ NO TensorFlow | NO spacy")
    print("✅ Deterministic extraction (regex + rules)")
    print("✅ OCR ready (EasyOCR)")
    print("📍 Server: http://localhost:8000")
    print("📍 UI: http://localhost:8000")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")