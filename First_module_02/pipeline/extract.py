"""
STEP 3 & 4: Test Extraction + Canonical Matching
Deterministic extraction using regex and alias mapping
"""
import re
from typing import List, Dict, Any, Optional

# Canonical tests (10 only)
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

# Alias mapping (fixed with bug fix)
FUZZY_ALIASES = {
    "hb": "hemoglobin",
    "hgb": "hemoglobin",
    "haemoglobin": "hemoglobin",
    "bin": "hemoglobin",  # IMPORTANT FIX FOR YOUR BUG
    "wbc count": "wbc",
    "white blood cells": "wbc",
    "plt": "platelets",
    "platelet count": "platelets",
    "cr": "creatinine",
    "creat": "creatinine",
    "glu": "glucose",
    "blood sugar": "glucose",
    "k": "potassium",
    "k+": "potassium",
    "alanine aminotransferase": "alt",
    "sgpt": "alt",
    "chol": "cholesterol",
    "total cholesterol": "cholesterol",
    "thyroid stimulating hormone": "tsh",
    "estimated gfr": "egfr",
    "gfr": "egfr"
}

def extract_lab_tests(text: str) -> List[Dict[str, Any]]:
    """Extract lab tests using regex patterns (deterministic)"""
    extracted = []
    
    # Pattern 1: "Hemoglobin 9.5 g/dL"
    pattern1 = r'([A-Za-z\s]+?)\s+([\d\.]+)\s+([gGuU]/[dD][lL]|mg/dL|mmol/L|U/L|uL|x10\^3/uL|mL/min/1\.73m2)'
    # Pattern 2: "Glucose: 180 mg/dL"
    pattern2 = r'([A-Za-z\s]+?)[:\s]+([\d\.]+)\s+([gGuU]/[dD][lL]|mg/dL|mmol/L|U/L|uL|x10\^3/uL|mL/min/1\.73m2)'
    # Pattern 3: "9.5 g/dL" (no test name)
    pattern3 = r'([\d\.]+)\s+([gGuU]/[dD][lL]|mg/dL|mmol/L|U/L|uL|x10\^3/uL|mL/min/1\.73m2)'
    
    lines = text.lower().split('\n')
    for line in lines:
        # Try each pattern
        matches1 = re.finditer(pattern1, line, re.IGNORECASE)
        matches2 = re.finditer(pattern2, line, re.IGNORECASE)
        matches3 = re.finditer(pattern3, line, re.IGNORECASE)
        
        for match in matches1:
            test_name = match.group(1).strip()
            value = float(match.group(2))
            unit = match.group(3).lower()
            normalized = normalize_test_name(test_name)
            if normalized:
                extracted.append({
                    "original_name": test_name,
                    "canonical_name": normalized,
                    "value": value,
                    "unit": unit
                })
        
        for match in matches2:
            test_name = match.group(1).strip()
            value = float(match.group(2))
            unit = match.group(3).lower()
            normalized = normalize_test_name(test_name)
            if normalized:
                extracted.append({
                    "original_name": test_name,
                    "canonical_name": normalized,
                    "value": value,
                    "unit": unit
                })
        
        for match in matches3:
            value = float(match.group(1))
            unit = match.group(2).lower()
            # Try to infer test from context
            test_name = extract_test_from_context(line, value, unit)
            normalized = normalize_test_name(test_name)
            if normalized:
                extracted.append({
                    "original_name": "inferred",
                    "canonical_name": normalized,
                    "value": value,
                    "unit": unit
                })
    
    # Remove duplicates (keep first)
    seen = set()
    unique = []
    for item in extracted:
        key = (item["canonical_name"], item["value"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    
    return unique

def extract_test_from_context(line: str, value: float, unit: str) -> str:
    """Infer test name from context"""
    if "hemoglobin" in line or "hb" in line:
        return "hemoglobin"
    elif "glucose" in line or "glu" in line:
        return "glucose"
    elif "creatinine" in line or "creat" in line:
        return "creatinine"
    elif "wbc" in line:
        return "wbc"
    elif "platelet" in line or "plt" in line:
        return "platelets"
    elif "potassium" in line or "k+" in line:
        return "potassium"
    elif "alt" in line:
        return "alt"
    elif "cholesterol" in line:
        return "cholesterol"
    elif "tsh" in line:
        return "tsh"
    else:
        # Default based on unit
        if unit == "g/dl":
            return "hemoglobin"
        elif unit == "mg/dl" and 40 < value < 500:
            return "glucose"
        return "unknown"

def normalize_test_name(name: str) -> Optional[str]:
    """Match test name to canonical list using rules"""
    name_clean = name.lower().strip()
    
    # Direct match
    if name_clean in CANONICAL_TESTS:
        return name_clean
    
    # Alias match
    if name_clean in FUZZY_ALIASES:
        return FUZZY_ALIASES[name_clean]
    
    # Substring match
    for canonical in CANONICAL_TESTS:
        if canonical in name_clean or name_clean in canonical:
            return canonical
    
    return None

def get_canonical_tests():
    """Return canonical tests dictionary for other modules"""
    return CANONICAL_TESTS