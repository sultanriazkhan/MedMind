"""
STEP 5: Range Classification
Hard-coded global ranges only
"""
from typing import Dict, Any
from pipeline.extract import get_canonical_tests

CANONICAL_TESTS = get_canonical_tests()

def classify_test(canonical_name: str, value: float) -> Dict[str, str]:
    """Classify test result using hardcoded ranges"""
    ranges = CANONICAL_TESTS.get(canonical_name)
    if not ranges:
        return {
            "status": "unknown",
            "reference_range": "N/A",
            "explanation": "Reference range not available"
        }
    
    ref_range = f"{ranges['low']}-{ranges['high']} {ranges['unit']}"
    
    # Check critical first
    if value <= ranges['critical_low']:
        status = "critical_low"
    elif value >= ranges['critical_high']:
        status = "critical_high"
    elif value < ranges['low']:
        status = "low"
    elif value > ranges['high']:
        status = "high"
    else:
        status = "normal"
    
    # Get explanation from explain module
    from pipeline.explain import get_explanation
    explanation = get_explanation(canonical_name, status)
    
    return {
        "status": status.replace("_", " ").title(),
        "reference_range": ref_range,
        "explanation": explanation
    }