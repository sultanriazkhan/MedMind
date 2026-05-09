# orchestrator.py - CORRECTED VERSION
"""Main orchestrator that connects all services"""
import sys
import os
from pathlib import Path

# Add pathology_processor to Python path (CORRECTED)
pathology_path = Path(__file__).parent / 'pathology_processor'
sys.path.insert(0, str(pathology_path))

from flask import Flask, request, jsonify
import requests
import logging

# Import your pathology pipeline directly (CORRECTED - no pathology_processor prefix)
from pathology_processor.services.pipeline import ProcessingPipeline

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service configurations (CORRECTED PORTS)
TEXT_EXTRACTOR_PORT = 5000
AI_EXPLAINER_PORT = 5001      # AI explainer now on port 5001
ORCHESTRATOR_PORT = 5002

# Service URLs
AI_EXPLAINER_URL = f"http://localhost:{AI_EXPLAINER_PORT}/generate-explanations"

# Initialize pipeline
try:
    pipeline = ProcessingPipeline()
    logger.info("✅ Pathology pipeline initialized")
except Exception as e:
    logger.error(f"❌ Pipeline init failed: {e}")
    pipeline = None


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
    """Main endpoint - processes text and returns enriched results"""
    
    # Get text from request
    if not request.is_json:
        return jsonify({"error": "Expected JSON"}), 400
    
    data = request.get_json()
    extracted_text = data.get('text', '')
    
    if not extracted_text:
        return jsonify({"error": "No text provided"}), 400
    
    if pipeline is None:
        return jsonify({"error": "Pipeline not initialized"}), 500
    
    # Step 1: Run pathology pipeline
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
            "test_name": test.get("raw_test_name", ""),
            "canonical_name": test.get("canonical_name"),
            "value": test.get("value"),
            "unit": test.get("unit"),
            "reference_range": test.get("reference_range"),
            "status": test.get("status", "Unknown"),
            
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
    """Health check"""
    ai_status = "unknown"
    try:
        r = requests.get("http://localhost:5001/", timeout=2)
        ai_status = "healthy" if r.status_code == 200 else "unhealthy"
    except:
        ai_status = "offline"
    
    return jsonify({
        "orchestrator": "healthy",
        "pipeline": "ready" if pipeline else "failed",
        "ai_explainer": ai_status
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Pathology Report Orchestrator")
    print("="*60)
    print(f"📍 AI Explainer: http://localhost:5001")
    print(f"📍 Orchestrator: http://localhost:5002")
    print("\n📋 Test:")
    print('   curl -X POST http://localhost:5002/process \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"text": "Hemoglobin 9.5 g/dL Low"}\'')
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5002, debug=True)