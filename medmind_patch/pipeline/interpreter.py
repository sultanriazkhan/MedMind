"""
pipeline/interpreter.py
Patient-centered interpretation layer for MedMind.

Purpose:
- Convert extracted lab values into user-friendly explanations.
- Keep this deterministic/rule-based for FYP transparency.
- Avoid diagnosis. Explain what the value may suggest and when to consult a clinician.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


DISCLAIMER = (
    "This explanation is for educational support only and is not a medical diagnosis. "
    "A qualified healthcare professional should interpret results with symptoms, age, sex, history, and medications."
)


# Patient-facing metadata for common CBC tests.
TEST_EXPLANATIONS: Dict[str, Dict[str, str]] = {
    "Hemoglobin": {
        "plain_name": "Hemoglobin",
        "what_it_is": "Hemoglobin is the protein in red blood cells that carries oxygen around your body.",
        "why_it_matters": "It helps show whether your blood can carry enough oxygen. Low values can be linked with anemia.",
        "normal": "Your hemoglobin is within the provided reference range, which usually suggests adequate oxygen-carrying capacity.",
        "low": "Your hemoglobin is below the provided range. This may suggest anemia or blood loss, especially if you feel tired, weak, dizzy, or short of breath.",
        "high": "Your hemoglobin is above the provided range. This may happen with dehydration, smoking, high altitude, or some blood conditions.",
        "advice_normal": "No immediate concern from this value alone. Maintain a balanced diet with iron, folate, and vitamin B12.",
        "advice_low": "Discuss this with a healthcare professional. They may suggest iron studies, B12/folate tests, or further evaluation.",
        "advice_high": "Repeat testing and hydration status may need review. Discuss persistent elevation with a healthcare professional.",
    },
    "RBC": {
        "plain_name": "Red Blood Cell Count",
        "what_it_is": "Red blood cells carry oxygen from the lungs to the rest of the body.",
        "why_it_matters": "This value helps assess anemia, dehydration, and some blood disorders.",
        "normal": "Your red blood cell count is within the provided reference range.",
        "low": "Your red blood cell count is below the provided range. This may be seen with anemia, bleeding, or nutritional deficiencies.",
        "high": "Your red blood cell count is above the provided range. This may occur with dehydration, smoking, high altitude, or increased red cell production.",
        "advice_normal": "No immediate concern from this value alone.",
        "advice_low": "Consider medical review, especially if you have fatigue, dizziness, pale skin, or shortness of breath.",
        "advice_high": "Consider repeating the test and discussing hydration, smoking status, altitude exposure, or other causes with a clinician.",
    },
    "WBC": {
        "plain_name": "White Blood Cell Count",
        "what_it_is": "White blood cells are part of your immune system and help fight infection.",
        "why_it_matters": "This value can rise with infection/inflammation and fall with some viral illnesses, medications, or bone marrow problems.",
        "normal": "Your white blood cell count is within the provided reference range, so there is no obvious sign of abnormal immune cell count from this value alone.",
        "low": "Your white blood cell count is below the provided range. This may reduce infection-fighting capacity or occur after some viral infections or medicines.",
        "high": "Your white blood cell count is above the provided range. This may suggest infection, inflammation, stress, or other medical causes.",
        "advice_normal": "No immediate concern from this value alone.",
        "advice_low": "Seek medical advice if you have fever, repeated infections, mouth ulcers, or feel very unwell.",
        "advice_high": "Consider clinical review, especially if you have fever, pain, cough, urinary symptoms, or persistent inflammation.",
    },
    "Platelets": {
        "plain_name": "Platelet Count",
        "what_it_is": "Platelets are blood cells that help with clotting and stop bleeding.",
        "why_it_matters": "Low platelets can increase bleeding risk, while high platelets can occur with inflammation, iron deficiency, or other conditions.",
        "normal": "Your platelet count is within the provided reference range, which usually suggests normal clotting-cell count.",
        "low": "Your platelet count is below the provided range. This may increase bleeding or bruising risk depending on how low it is.",
        "high": "Your platelet count is above the provided range. This can occur with inflammation, infection, iron deficiency, or other conditions.",
        "advice_normal": "No immediate concern from this value alone.",
        "advice_low": "Seek medical advice if you have easy bruising, nosebleeds, bleeding gums, blood in stool/urine, or tiny red skin spots.",
        "advice_high": "Discuss persistent elevation with a healthcare professional. They may check inflammation markers or iron status.",
    },
    "Hematocrit": {
        "plain_name": "Hematocrit",
        "what_it_is": "Hematocrit is the percentage of your blood volume made up of red blood cells.",
        "why_it_matters": "It helps assess anemia, dehydration, and overall red blood cell concentration.",
        "normal": "Your hematocrit is within the provided reference range.",
        "low": "Your hematocrit is below the provided range. This may suggest anemia, blood loss, or overhydration.",
        "high": "Your hematocrit is above the provided range. This may suggest dehydration or increased red blood cell concentration.",
        "advice_normal": "No immediate concern from this value alone.",
        "advice_low": "Discuss with a clinician if you have fatigue, weakness, dizziness, or shortness of breath.",
        "advice_high": "Review hydration status and discuss persistent elevation with a healthcare professional.",
    },
}


STATUS_LABELS = {
    "normal": "Normal",
    "low": "Low",
    "high": "High",
    "critical_low": "Critically Low",
    "critical_high": "Critically High",
    "invalid": "Needs Review",
    "unknown": "Unknown",
}


SEVERITY = {
    "normal": "none",
    "low": "mild_to_moderate",
    "high": "mild_to_moderate",
    "critical_low": "urgent",
    "critical_high": "urgent",
    "invalid": "review",
    "unknown": "unknown",
}


def _safe_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def classify_against_reference(value: Any, ref_low: Any = None, ref_high: Any = None) -> str:
    """Classify result using report-specific reference range when available."""
    v = _safe_float(value)
    lo = _safe_float(ref_low)
    hi = _safe_float(ref_high)
    if v is None or lo is None or hi is None:
        return "unknown"
    if lo > hi:
        return "unknown"
    if v < lo:
        return "low"
    if v > hi:
        return "high"
    return "normal"


def _reference_range_text(test: Dict[str, Any]) -> str:
    lo = test.get("reference_low")
    hi = test.get("reference_high")
    unit = test.get("unit") or ""
    if lo is not None and hi is not None:
        return f"{lo} - {hi} {unit}".strip()
    return "Reference range not provided in report"


def _value_text(test: Dict[str, Any]) -> str:
    value = test.get("value")
    unit = test.get("unit") or ""
    return f"{value} {unit}".strip()


def build_patient_explanation(test: Dict[str, Any]) -> Dict[str, Any]:
    
    canonical = test.get("canonical_name", "Unknown")
    meta = TEST_EXPLANATIONS.get(canonical, {})

    # Prefer report-specific reference range if parsed.
    ref_status = classify_against_reference(
        test.get("value"),
        test.get("reference_low"),
        test.get("reference_high"),
    )

    original_flag = str(test.get("flag", "normal")).lower().replace(" ", "_")
    if ref_status != "unknown":
        status = ref_status
    elif original_flag in STATUS_LABELS:
        status = original_flag
    elif original_flag == "critical":
        status = "critical_high"
    else:
        status = "unknown"

    # If the extractor marked invalid only because unit/value scaling was suspicious,
    # still show a review-friendly explanation instead of alarming the user.
    if original_flag == "invalid" and ref_status == "unknown":
        status = "invalid"

    plain_name = meta.get("plain_name", canonical)
    status_label = STATUS_LABELS.get(status, status.title())

    if status in ("critical_low", "critical_high"):
        meaning = f"{plain_name} is in a critical range."
        advice = "Please seek urgent medical attention or contact a healthcare professional immediately."
    elif status == "invalid":
        meaning = (
            f"{plain_name} was extracted, but the system wants this result reviewed because the unit or value format may need confirmation."
        )
        advice = "Check the original report value/unit and repeat processing after unit normalization if needed."
    else:
        meaning = meta.get(status, f"{plain_name} is marked as {status_label.lower()}.")
        advice = meta.get(f"advice_{status}", "Discuss this result with a healthcare professional if you have symptoms or concerns.")

    return {
        "display_name": plain_name,
        "value_text": _value_text(test),
        "status": status_label,
        "severity": SEVERITY.get(status, "unknown"),
        "reference_range": _reference_range_text(test),
        "what_it_is": meta.get("what_it_is", f"{plain_name} is a laboratory test parameter."),
        "why_it_matters": meta.get("why_it_matters", "This result should be interpreted with the full report and clinical history."),
        "what_your_result_means": meaning,
        "recommendation": advice,
        "disclaimer": DISCLAIMER,
    }


def enrich_lab_tests(tests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Attach patient_explanation to every extracted test result."""
    enriched: List[Dict[str, Any]] = []
    for test in tests:
        item = dict(test)
        item["patient_explanation"] = build_patient_explanation(item)
        enriched.append(item)
    return enriched
