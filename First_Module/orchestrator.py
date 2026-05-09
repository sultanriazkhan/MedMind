# orchestrator.py
"""Main orchestrator that connects all services"""
import sys
import os
from pathlib import Path

# Add pathology_processor to Python path
sys.path.insert(0, str(Path(__file__).parent / 'pathology_processor'))

from flask import Flask, request, jsonify
import requests
import logging

# Import your pathology pipeline directly
from pathology_processor.services.pipeline import ProcessingPipeline

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service configurations
TEXT_EXTRACTOR_PORT = 5000      # Your text extractor Flask app
AI_EXPLAINER_PORT = 5001        # Your AI explainer Flask app  
PATHOLOGY_API_PORT = 8000       # Your FastAPI app (main.py)
ORCHESTRATOR_PORT = 5002        # This orchestrator

# Service URLs
TEXT_EXTRACTOR_URL = f"http://localhost:{TEXT_EXTRACTOR_PORT}"
AI_EXPLAINER_URL = f"http://localhost:{AI_EXPLAINER_PORT}/generate-explanations"
PATHOLOGY_API_URL = f"http://localhost:{PATHOLOGY_API_PORT}"

# Initialize pipeline directly (faster than API call)
pipeline = ProcessingPipeline()


def extract_text_from_file(file):
    """Extract text using your existing text_extractor.py logic"""
    filepath = f"/tmp/{file.filename}"
    file.save(filepath)
    
    filename = file.filename
    
    # Import extraction functions dynamically
    import importlib.util
    text_extractor_path = Path(__file__).parent / 'text_extractor.py'
    if not text_extractor_path.exists():
        raise FileNotFoundError(f"text_extractor.py not found at {text_extractor_path}")

    spec = importlib.util.spec_from_file_location("text_extractor", text_extractor_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load text_extractor module from {text_extractor_path}")

    text_extractor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(text_extractor)
    
    # Extract based on file type
    if filename.endswith('.pdf'):
        extracted_text = text_extractor.extract_pdf_text(filepath)
    elif filename.endswith('.docx'):
        extracted_text = text_extractor.extract_word_text(filepath)
    elif filename.endswith('.txt'):
        extracted_text = text_extractor.extract_text_file(filepath)
    elif filename.endswith(('.jpg', '.jpeg', '.png')):
        extracted_text = text_extractor.extract_image_text(filepath)
    else:
        extracted_text = "Unsupported file type"
    
    os.remove(filepath)
    return extracted_text


def add_ai_explanations(test_results):
    """Call AI explainer for clinical context"""
    if not test_results:
        return []
    
    # Format for AI explainer
    tests_for_ai = []
    for test in test_results:
        tests_for_ai.append({
            "test_name": test.get("canonical_name") or test.get("raw_test_name"),
            "value": test.get("value"),
            "status": test.get("status", "Unknown")
        })
    
    try:
        response = requests.post(AI_EXPLAINER_URL, json=tests_for_ai, timeout=30)
        if response.status_code == 200:
            ai_data = response.json()
            return ai_data.get("report", [])
    except Exception as e:
        logger.error(f"AI explainer error: {e}")
    
    return []


@app.route('/process', methods=['POST'])
def process_report():
    """Main endpoint - processes file or text and returns enriched results"""
    
    # Case 1: File upload
    if 'file' in request.files:
        file = request.files['file']
        if not file.filename:
            return jsonify({"error": "No file selected"}), 400
        
        extracted_text = extract_text_from_file(file)
        if not extracted_text or "Error" in extracted_text:
            return jsonify({"error": "Text extraction failed", "details": extracted_text}), 422
    
    # Case 2: Direct text input
    elif request.is_json:
        json_payload = request.get_json(silent=True)
        if json_payload and 'text' in json_payload:
            extracted_text = json_payload['text']
        else:
            return jsonify({"error": "Provide file or 'text' field"}), 400
    else:
        return jsonify({"error": "Provide file or 'text' field"}), 400
    
    # Step 1: Run pathology pipeline on extracted text
    logger.info("Running pathology pipeline...")
    result = pipeline.process(extracted_text)
    
    if not result.tests:
        return jsonify({
            "error": "No lab tests detected",
            "raw_text_preview": extracted_text[:500]
        }), 422
    
    # Step 2: Add AI explanations
    logger.info(f"Adding AI explanations for {len(result.tests)} tests...")
    ai_explanations = add_ai_explanations(result.tests)
    
    # Step 3: Merge results
    enriched_tests = []
    for i, test in enumerate(result.tests):
        enriched_test = {
            "raw_text": test.get("raw_text", ""),
            "test_name": test.get("raw_test_name", ""),
            "canonical_name": test.get("canonical_name"),
            "loinc_code": test.get("loinc_code"),
            "value": test.get("value"),
            "unit": test.get("unit"),
            "reference_range": test.get("reference_range"),
            "status": test.get("status", "Unknown"),
            "confidence_score": test.get("confidence_score", 0.0),
            
            # AI explanations
            "clinical_meaning": "Not available",
            "possible_causes": "Not available",
            "clinical_effects": "Not available",
            "recommendations": "Consult healthcare professional"
        }
        
        if i < len(ai_explanations):
            ai = ai_explanations[i]
            enriched_test.update({
                "clinical_meaning": ai.get("meaning", enriched_test["clinical_meaning"]),
                "possible_causes": ai.get("causes", enriched_test["possible_causes"]),
                "clinical_effects": ai.get("effects", enriched_test["clinical_effects"]),
                "recommendations": ai.get("solution", enriched_test["recommendations"])
            })
        
        enriched_tests.append(enriched_test)
    
    # Step 4: Return final response
    return jsonify({
        "success": True,
        "request_id": result.request_id,
        "processing_time_ms": result.processing_time_ms,
        "summary": {
            "total_tests": len(enriched_tests),
            "regex_matches": result.regex_matches,
            "fallback_matches": result.fallback_matches,
            "canonicalized": result.canonicalized,
            "ai_enriched": len([t for t in enriched_tests if t["clinical_meaning"] != "Not available"])
        },
        "tests": enriched_tests,
        "errors": result.errors
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check for all services"""
    services_status = {
        "orchestrator": "healthy",
        "pathology_pipeline": "healthy",
        "text_extractor": "unknown",
        "ai_explainer": "unknown",
        "fastapi": "unknown"
    }
    
    # Check AI explainer
    try:
        r = requests.get("http://localhost:5001/", timeout=2)
        services_status["ai_explainer"] = "healthy" if r.status_code == 200 else "unhealthy"
    except:
        services_status["ai_explainer"] = "offline"
    
    # Check FastAPI (your main.py)
    try:
        r = requests.get("http://localhost:8000/health", timeout=2)
        services_status["fastapi"] = "healthy" if r.status_code == 200 else "unhealthy"
    except:
        services_status["fastapi"] = "offline"
    
    return jsonify(services_status)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Pathology Report Orchestrator")
    print("="*60)
    print(f"📍 Text Extractor (expected): http://localhost:5000")
    print(f"📍 AI Explainer (expected):   http://localhost:5001")
    print(f"📍 FastAPI (your main.py):    http://localhost:8000")
    print(f"📍 Orchestrator running:      http://localhost:5002")
    print("\n📋 Usage:")
    print('   curl -X POST http://localhost:5002/process \\')
    print('     -F "file=@report.pdf"')
    print('   OR')
    print('   curl -X POST http://localhost:5002/process \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"text": "Hemoglobin 9.5 g/dL"}\'')
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5002, debug=True)