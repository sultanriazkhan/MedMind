"""
STEP 6: Explanation Engine
Rule-based only - NO AI MODELS
"""
from typing import Dict

# Explanation dictionary (deterministic)
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
    ("egfr", "low"): "Low eGFR indicates reduced kidney function.",
    ("egfr", "high"): "High eGFR is generally good but may indicate hyperfiltration.",
}

def get_explanation(test: str, status: str) -> str:
    """Get deterministic explanation from dictionary"""
    # Normalize status for lookup
    status_key = status.split()[0] if " " in status else status
    status_key = status_key.lower()
    
    if "critical" in status_key:
        status_key = "critical"
    
    key = (test, status_key)
    if key in EXPLANATIONS:
        return EXPLANATIONS[key]
    else:
        # Default explanation
        if status_key == "normal":
            return f"{test.title()} is within normal range."
        else:
            return f"{test.title()} {status_key} - consult reference ranges for clinical significance."