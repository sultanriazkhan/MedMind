# main.py - SINGLE ENTRY POINT - FastAPI Only
import re
import json
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import io
import base64

# PDF & DOCX processing
try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    import subprocess
    subprocess.check_call(["pip", "install", "PyMuPDF"])
    import fitz

try:
    from docx import Document
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "python-docx"])
    from docx import Document

# OCR for images - using easyocr (lightweight)
try:
    import easyocr
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "easyocr"])
    import easyocr

# Initialize OCR reader (only once)
reader = None

def get_reader():
    global reader
    if reader is None:
        import easyocr
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    return reader

# ============ DATABASE SETUP ============
def init_db():
    conn = sqlite3.connect('lab_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_type TEXT,
            raw_text TEXT,
            results_json TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ============ CANONICAL TESTS & RANGES ============
CANONICAL_TESTS = {
    "hemoglobin": {"unit": "g/dL", "low": 12.0, "high": 16.0, "critical_low": 7.0, "critical_high": 20.0},
    "wbc": {"unit": "x10^3/uL", "low": 4.5, "high": 11.0, "critical_low": 1.0, "critical_high": 50.0},
    "platelets": {"unit": "x10^3/uL", "low": 150, "high": 450, "critical_low": 20, "critical_high": 1000},
    "creatinine": {"unit": "mg/dL", "low": 0.6, "high": 1.3, "critical_low": 0.4, "critical_high": 10.0},
    "glucose": {"unit": "mg/dL", "low": 70, "high": 100, "critical_low": 40, "critical_high": 500},
    "potassium": {"unit": "mmol/L", "low": 3.5, "high": 5.0, "critical_low": 2.5, "critical_high": 6.5},
    "alt": {"unit": "U/L", "low": 10, "high": 40, "critical_low": 5, "critical_high": 500},
    "cholesterol": {"unit": "mg/dL", "low": 125, "high": 200, "critical_low": 100, "critical_high": 400},
    "tsh": {"unit": "mIU/L", "low": 0.4, "high": 4.0, "critical_low": 0.1, "critical_high": 50},
    "egfr": {"unit": "mL/min/1.73m2", "low": 60, "high": 120, "critical_low": 15, "critical_high": 200}
}

# Alias mapping (small, deterministic)
ALIAS_MAP = {
    "hb": "hemoglobin", "hgb": "hemoglobin", "haemoglobin": "hemoglobin",
    "wbc count": "wbc", "white blood cells": "wbc",
    "plt": "platelets", "platelet count": "platelets",
    "cr": "creatinine", "creat": "creatinine",
    "glu": "glucose", "blood sugar": "glucose",
    "k": "potassium", "k+": "potassium",
    "alanine aminotransferase": "alt", "sgpt": "alt",
    "chol": "cholesterol", "total cholesterol": "cholesterol",
    "thyroid stimulating hormone": "tsh",
    "estimated gfr": "egfr", "gfr": "egfr"
}

# Explanation dictionary (rule-based, NO AI)
EXPLANATIONS = {
    ("hemoglobin", "low"): "Low hemoglobin suggests possible anemia. Consider iron studies.",
    ("hemoglobin", "high"): "Elevated hemoglobin may indicate dehydration or polycythemia.",
    ("hemoglobin", "critical"): "Critical hemoglobin requires immediate medical attention.",
    ("glucose", "low"): "Low glucose (hypoglycemia) may require carbohydrate intake.",
    ("glucose", "high"): "Elevated glucose suggests diabetes risk or poor glucose control.",
    ("creatinine", "high"): "High creatinine indicates possible kidney dysfunction.",
    ("creatinine", "low"): "Low creatinine may indicate low muscle mass or liver disease.",
    ("wbc", "high"): "Elevated WBC suggests infection or inflammation.",
    ("wbc", "low"): "Low WBC may indicate bone marrow suppression or viral infection.",
    ("platelets", "low"): "Low platelets (thrombocytopenia) increases bleeding risk.",
    ("platelets", "high"): "High platelets may indicate inflammation or iron deficiency.",
    ("alt", "high"): "Elevated ALT suggests possible liver injury.",
    ("cholesterol", "high"): "High cholesterol increases cardiovascular disease risk.",
    ("tsh", "high"): "High TSH suggests hypothyroidism.",
    ("tsh", "low"): "Low TSH suggests hyperthyroidism.",
    ("potassium", "high"): "High potassium (hyperkalemia) may affect heart rhythm.",
    ("potassium", "low"): "Low potassium (hypokalemia) may cause muscle weakness.",
    ("egfr", "low"): "Low eGFR indicates reduced kidney function."
}

# ============ TEXT EXTRACTION ============
def extract_text_from_image(file_bytes: bytes) -> str:
    """Extract text from image using EasyOCR"""
    try:
        import numpy as np
        from PIL import Image
        
        # Convert bytes to image
        image = Image.open(io.BytesIO(file_bytes))
        # Convert PIL image to numpy array
        image_np = np.array(image)
        
        # Perform OCR
        results = reader.readtext(image_np, detail=0)
        text = " ".join(results)
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OCR failed: {str(e)}")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using PyMuPDF"""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF parsing failed: {str(e)}")

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX using python-docx"""
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DOCX parsing failed: {str(e)}")

# ============ TEST EXTRACTION (DETERMINISTIC) ============
def extract_lab_tests(text: str) -> List[Dict[str, Any]]:
    """Extract lab tests using regex patterns"""
    extracted = []
    
    # Pattern: TestName Value Unit
    patterns = [
        # Pattern for "Hemoglobin 9.5 g/dL"
        r'([A-Za-z\s]+?)\s+([\d\.]+)\s+([gGuU]/[dD][lL]|mg/dL|mmol/L|U/L|uL|x10\^3/uL|mL/min/1\.73m2)',
        # Pattern for "Glucose: 180 mg/dL"
        r'([A-Za-z\s]+?)[:\s]+([\d\.]+)\s+([gGuU]/[dD][lL]|mg/dL|mmol/L|U/L|uL|x10\^3/uL)',
        # Pattern for simple "9.5 g/dL"
        r'([\d\.]+)\s+([gGuU]/[dD][lL]|mg/dL|mmol/L|U/L|uL|x10\^3/uL)'
    ]
    
    lines = text.lower().split('\n')
    for line in lines:
        # Try each pattern
        for pattern in patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 3:
                    test_name = match.group(1).strip()
                    value = float(match.group(2))
                    unit = match.group(3).lower()
                elif len(match.groups()) == 2:
                    # No test name in pattern
                    value = float(match.group(1))
                    unit = match.group(2).lower()
                    # Try to infer test from context
                    test_name = extract_test_from_context(line, value, unit)
                else:
                    continue
                
                # Normalize test name
                normalized = normalize_test_name(test_name)
                if normalized:
                    extracted.append({
                        "original_name": test_name,
                        "canonical_name": normalized,
                        "value": value,
                        "unit": unit
                    })
    
    # Remove duplicates (keep first occurrence)
    seen = set()
    unique_extracted = []
    for item in extracted:
        key = (item["canonical_name"], item["value"])
        if key not in seen:
            seen.add(key)
            unique_extracted.append(item)
    
    return unique_extracted

def extract_test_from_context(line: str, value: float, unit: str) -> str:
    """Infer test name from context"""
    # Simple inference based on units and nearby words
    if "hemoglobin" in line or "hb" in line or unit == "g/dl":
        return "hemoglobin"
    elif "glucose" in line or "glu" in line or (unit == "mg/dl" and value > 40 and value < 500):
        return "glucose"
    elif "creatinine" in line or "creat" in line:
        return "creatinine"
    elif "wbc" in line:
        return "wbc"
    elif "platelet" in line or "plt" in line:
        return "platelets"
    else:
        return "unknown"

def normalize_test_name(name: str) -> str:
    """Match test name to canonical list using rules"""
    name_clean = name.lower().strip()
    
    # Direct match
    if name_clean in CANONICAL_TESTS:
        return name_clean
    
    # Alias match
    if name_clean in ALIAS_MAP:
        return ALIAS_MAP[name_clean]
    
    # Fuzzy match (simple substring)
    for canonical in CANONICAL_TESTS:
        if canonical in name_clean or name_clean in canonical:
            return canonical
    
    return None

# ============ CLASSIFICATION ============
def classify_test(canonical_name: str, value: float) -> Dict[str, str]:
    """Classify test result using hardcoded ranges"""
    ranges = CANONICAL_TESTS.get(canonical_name)
    if not ranges:
        return {"status": "unknown", "reference_range": "N/A", "explanation": "Reference range not available"}
    
    ref_range = f"{ranges['low']}-{ranges['high']} {ranges['unit']}"
    
    # Check critical first
    if value <= ranges['critical_low']:
        status = "critical_low"
        explanation = get_explanation(canonical_name, "critical")
    elif value >= ranges['critical_high']:
        status = "critical_high"
        explanation = get_explanation(canonical_name, "critical")
    elif value < ranges['low']:
        status = "low"
        explanation = get_explanation(canonical_name, "low")
    elif value > ranges['high']:
        status = "high"
        explanation = get_explanation(canonical_name, "high")
    else:
        status = "normal"
        explanation = f"{canonical_name.title()} is within normal range."
    
    return {
        "status": status,
        "reference_range": ref_range,
        "explanation": explanation
    }

def get_explanation(test: str, status: str) -> str:
    """Get deterministic explanation from dictionary"""
    key = (test, status)
    if key in EXPLANATIONS:
        return EXPLANATIONS[key]
    else:
        return f"{test.title()} {status} - consult reference ranges for clinical significance."

# ============ MAIN PROCESSING PIPELINE ============
def process_file(file: UploadFile, text_input: Optional[str] = None) -> Dict[str, Any]:
    """Main pipeline - STEP 1: Ingestion Layer"""
    file_content = None
    
    if file:
        file_content = file.file.read()
        file_type = file.content_type
        
        # STEP 2: OCR for images
        if file_type.startswith('image/'):
            source_type = "image"
            raw_text = extract_text_from_image(file_content)
        elif file_type == 'application/pdf':
            source_type = "pdf"
            raw_text = extract_text_from_pdf(file_content)
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            source_type = "docx"
            raw_text = extract_text_from_docx(file_content)
        elif file_type == 'text/plain':
            source_type = "text"
            raw_text = file_content.decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_type}")
    elif text_input:
        source_type = "pasted_text"
        raw_text = text_input
    else:
        raise HTTPException(status_code=400, detail="No input provided")
    
    # STEP 3: Extract tests using regex
    extracted_tests = extract_lab_tests(raw_text)
    
    # STEP 4 & 5: Match to canonical tests and classify
    processed_tests = []
    summary = {"total_tests": 0, "normal": 0, "abnormal": 0, "critical": 0}
    
    for test in extracted_tests:
        if test["canonical_name"]:
            classification = classify_test(test["canonical_name"], test["value"])
            
            status_display = classification["status"].replace("_", " ").title()
            if "critical" in classification["status"]:
                summary["critical"] += 1
                summary["abnormal"] += 1
            elif classification["status"] != "normal":
                summary["abnormal"] += 1
            else:
                summary["normal"] += 1
            
            processed_tests.append({
                "name": test["canonical_name"].title(),
                "value": test["value"],
                "unit": CANONICAL_TESTS[test["canonical_name"]]["unit"],
                "status": status_display,
                "reference_range": classification["reference_range"],
                "explanation": classification["explanation"]
            })
            summary["total_tests"] += 1
    
    # Save to database
    conn = sqlite3.connect('lab_results.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO processed_results (timestamp, source_type, raw_text, results_json) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(), source_type, raw_text[:1000], json.dumps(processed_tests))
    )
    conn.commit()
    conn.close()
    
    return {
        "source_type": source_type,
        "raw_text": raw_text[:500] + "..." if len(raw_text) > 500 else raw_text,
        "tests": processed_tests,
        "summary": summary
    }

# ============ FASTAPI APP ============
app = FastAPI(title="MedMind Lab Processing System", version="1.0.0")

# HTML Interface
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>MedMind Lab System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        .tab {
            overflow: hidden;
            margin-bottom: 20px;
        }
        .tab button {
            background-color: #f1f1f1;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            font-size: 17px;
        }
        .tab button:hover {
            background-color: #ddd;
        }
        .tab button.active {
            background-color: #4CAF50;
            color: white;
        }
        .tabcontent {
            display: none;
            padding: 20px;
            border: 1px solid #ccc;
            border-top: none;
            border-radius: 0 0 5px 5px;
        }
        textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-family: monospace;
        }
        input[type="file"] {
            margin: 10px 0;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background-color: #45a049;
        }
        pre {
            background: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .result {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 MedMind Lab Processing System</h1>
        
        <div class="tab">
            <button class="tablinks" onclick="openTab(event, 'File')" id="defaultOpen">📁 Upload File</button>
            <button class="tablinks" onclick="openTab(event, 'Text')">📝 Paste Text</button>
        </div>
        
        <div id="File" class="tabcontent">
            <form id="fileForm">
                <label>Select file (Image, PDF, DOCX, TXT):</label><br>
                <input type="file" id="fileInput" accept=".jpg,.jpeg,.png,.pdf,.docx,.txt,image/*"><br>
                <button type="submit">Process File</button>
            </form>
        </div>
        
        <div id="Text" class="tabcontent">
            <form id="textForm">
                <label>Paste lab results:</label><br>
                <textarea rows="6" id="textInput" placeholder="Example:&#10;Hemoglobin 9.5 g/dL&#10;Glucose 180 mg/dL"></textarea><br>
                <button type="submit">Process Text</button>
            </form>
        </div>
        
        <div id="result" class="result" style="display:none;">
            <h3>Results:</h3>
            <pre id="resultContent"></pre>
        </div>
    </div>
    
    <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
        
        document.getElementById("fileForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const file = document.getElementById("fileInput").files[0];
            if (!file) {
                alert("Please select a file");
                return;
            }
            
            const formData = new FormData();
            formData.append("file", file);
            
            const response = await fetch("/process", {
                method: "POST",
                body: formData
            });
            
            const result = await response.json();
            document.getElementById("resultContent").textContent = JSON.stringify(result, null, 2);
            document.getElementById("result").style.display = "block";
        });
        
        document.getElementById("textForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const text = document.getElementById("textInput").value;
            if (!text) {
                alert("Please enter text");
                return;
            }
            
            const response = await fetch("/process", {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: "text_input=" + encodeURIComponent(text)
            });
            
            const result = await response.json();
            document.getElementById("resultContent").textContent = JSON.stringify(result, null, 2);
            document.getElementById("result").style.display = "block";
        });
        
        document.getElementById("defaultOpen").click();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    return HTML_PAGE

@app.post("/process")
async def process_lab_results(
    file: Optional[UploadFile] = None,
    text_input: Optional[str] = Form(None)
):
    """Main API endpoint for processing lab results"""
    try:
        result = process_file(file, text_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "MedMind Lab System", "version": "1.0.0"}

# ============ MAIN ENTRY POINT ============
if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🏥 MedMind Lab Processing System v1.0")
    print("=" * 60)
    print("✅ Single service running on port 8000")
    print("✅ No orchestrator | No background watchers")
    print("✅ Deterministic extraction (regex-based)")
    print("✅ OCR ready for images")
    print("📍 API: http://localhost:8000")
    print("📍 UI: http://localhost:8000")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")