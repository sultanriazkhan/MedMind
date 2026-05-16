"""
pipeline/interpreter.py

Patient-centered interpretation layer for MedMind.

This version trusts the extractor's numeric classification and fallback
reference ranges. It does not label missing-range abnormal results as normal.

It remains deterministic/rule-based for FYP transparency.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


DISCLAIMER = (
    "This explanation is for educational support only and is not a medical diagnosis. "
    "A qualified healthcare professional should interpret results with symptoms, age, sex, history, medications, and the laboratory's own reference ranges."
)


STATUS_LABELS = {
    "normal": "Normal",
    "low": "Low",
    "high": "High",
    "critical_low": "Critically Low",
    "critical_high": "Critically High",
    "abnormal": "Abnormal",
    "invalid": "Needs Review",
    "unknown": "Unknown",
}

SEVERITY = {
    "normal": "none",
    "low": "mild_to_moderate",
    "high": "mild_to_moderate",
    "critical_low": "urgent",
    "critical_high": "urgent",
    "abnormal": "review",
    "invalid": "review",
    "unknown": "unknown",
}


TEST_EXPLANATIONS: Dict[str, Dict[str, str]] = {
    "Hemoglobin": {
        "plain_name": "Hemoglobin",
        "what_it_is": "Hemoglobin is the oxygen-carrying protein inside red blood cells.",
        "why_it_matters": "It helps assess whether your blood can carry enough oxygen. Low values commonly point toward anemia or blood loss.",
        "normal": "Your hemoglobin is within the expected range.",
        "low": "Your hemoglobin is below the expected range. This may suggest anemia, iron deficiency, blood loss, vitamin B12/folate deficiency, or chronic disease.",
        "high": "Your hemoglobin is above the expected range. This may occur with dehydration, smoking, high altitude, or increased red cell production.",
        "critical_low": "Your hemoglobin is critically low and may require urgent clinical review.",
        "critical_high": "Your hemoglobin is critically high and may require urgent clinical review.",
        "advice_normal": "Maintain a balanced diet with iron, folate, and vitamin B12.",
        "advice_low": "Discuss this with a clinician. Iron studies, ferritin, B12, folate, and bleeding evaluation may be considered.",
        "advice_high": "Review hydration, smoking status, altitude exposure, and discuss persistent elevation with a clinician.",
        "advice_critical_low": "Seek urgent medical review, especially if you have chest pain, breathlessness, fainting, severe weakness, or rapid heartbeat.",
        "advice_critical_high": "Seek medical review promptly, especially if symptoms such as headache, dizziness, visual changes, or clotting risk are present.",
    },
    "RBC": {
        "plain_name": "Red Blood Cell Count",
        "what_it_is": "Red blood cells carry oxygen from the lungs to body tissues.",
        "why_it_matters": "This value helps assess anemia, dehydration, and some blood disorders.",
        "normal": "Your red blood cell count is within the expected range.",
        "low": "Your red blood cell count is below the expected range. This can occur in anemia, bleeding, or nutritional deficiencies.",
        "high": "Your red blood cell count is above the expected range. This may occur with dehydration, smoking, altitude, or increased red cell production.",
        "advice_normal": "No immediate concern from this marker alone.",
        "advice_low": "Consider review with hemoglobin, hematocrit, MCV, iron studies, B12, and folate.",
        "advice_high": "Consider repeat testing and clinical review if persistently elevated.",
    },
    "Hematocrit": {
        "plain_name": "Hematocrit",
        "what_it_is": "Hematocrit is the percentage of blood volume made up of red blood cells.",
        "why_it_matters": "It helps assess anemia, dehydration, and red blood cell concentration.",
        "normal": "Your hematocrit is within the expected range.",
        "low": "Your hematocrit is below the expected range. This may suggest anemia, blood loss, or overhydration.",
        "high": "Your hematocrit is above the expected range. This may suggest dehydration or increased red blood cell concentration.",
        "advice_normal": "No immediate concern from this marker alone.",
        "advice_low": "Review with hemoglobin, RBC count, MCV, and iron studies.",
        "advice_high": "Review hydration status and discuss persistent elevation with a healthcare professional.",
    },
    "MCV": {
        "plain_name": "Mean Corpuscular Volume",
        "what_it_is": "MCV measures the average size of red blood cells.",
        "why_it_matters": "Low MCV suggests smaller red blood cells, commonly seen with iron deficiency or thalassemia trait. High MCV can occur with B12 or folate deficiency.",
        "normal": "Your MCV is within the expected range.",
        "low": "Your MCV is low, meaning red blood cells are smaller than expected. This pattern is often seen in iron deficiency anemia or thalassemia trait.",
        "high": "Your MCV is high, meaning red blood cells are larger than expected. This may occur with vitamin B12 deficiency, folate deficiency, liver disease, alcohol use, or some medications.",
        "advice_normal": "No immediate concern from this marker alone.",
        "advice_low": "Consider ferritin, iron/TIBC, and clinical review, especially if hemoglobin is also low.",
        "advice_high": "Consider B12, folate, liver function, thyroid testing, and medication review.",
    },
    "MCH": {
        "plain_name": "Mean Corpuscular Hemoglobin",
        "what_it_is": "MCH estimates the amount of hemoglobin in each red blood cell.",
        "why_it_matters": "Low MCH often supports iron deficiency or microcytic anemia patterns.",
        "normal": "Your MCH is within the expected range.",
        "low": "Your MCH is low, meaning red blood cells carry less hemoglobin than expected. This often fits iron deficiency or microcytic anemia.",
        "high": "Your MCH is above the expected range and may occur with macrocytic red blood cell patterns.",
        "advice_normal": "No immediate concern from this marker alone.",
        "advice_low": "Review with MCV, MCHC, RDW, ferritin, and iron studies.",
        "advice_high": "Review with MCV, B12, folate, liver and thyroid markers.",
    },
    "MCHC": {
        "plain_name": "Mean Corpuscular Hemoglobin Concentration",
        "what_it_is": "MCHC estimates hemoglobin concentration inside red blood cells.",
        "why_it_matters": "It helps characterize anemia patterns.",
        "normal": "Your MCHC is within the expected range.",
        "low": "Your MCHC is low and may support iron deficiency or hypochromic anemia.",
        "high": "Your MCHC is high and may require review for red cell disorders or sample-related issues.",
        "advice_normal": "Interpret together with hemoglobin, MCV, MCH, and RDW.",
        "advice_low": "Consider iron studies and clinician review if anemia is present.",
        "advice_high": "Consider repeat testing and professional review.",
    },
    "RDW": {
        "plain_name": "Red Cell Distribution Width",
        "what_it_is": "RDW measures variation in red blood cell size.",
        "why_it_matters": "High RDW can indicate mixed red blood cell sizes, often seen in iron deficiency, B12/folate deficiency, or recovering anemia.",
        "normal": "Your RDW is within the expected range.",
        "low": "Low RDW is usually less clinically significant by itself.",
        "high": "Your RDW is high, meaning red blood cell sizes vary more than expected. This may support iron deficiency or nutritional anemia patterns.",
        "advice_normal": "No immediate concern from this marker alone.",
        "advice_low": "Usually interpreted with other CBC markers.",
        "advice_high": "Review with hemoglobin, MCV, ferritin, iron studies, B12, and folate.",
    },
    "WBC": {
        "plain_name": "White Blood Cell Count",
        "what_it_is": "White blood cells are immune cells that help fight infection and inflammation.",
        "why_it_matters": "High values can occur with infection, inflammation, stress, steroids, or other conditions. Low values can reduce infection-fighting capacity.",
        "normal": "Your white blood cell count is within the expected range.",
        "low": "Your white blood cell count is below the expected range. This may occur after viral illness, with some medicines, or bone marrow suppression.",
        "high": "Your white blood cell count is above the expected range. This may suggest infection, inflammation, physical stress, medication effect, or other causes.",
        "critical_low": "Your white blood cell count is critically low and may increase infection risk.",
        "critical_high": "Your white blood cell count is critically high and needs prompt clinical review.",
        "advice_normal": "No immediate concern from this marker alone.",
        "advice_low": "Seek medical advice if you have fever, repeated infections, mouth ulcers, or feel very unwell.",
        "advice_high": "Review symptoms such as fever, cough, urinary symptoms, pain, inflammation, or recent steroid use.",
        "advice_critical_low": "Seek urgent medical review if fever or signs of infection are present.",
        "advice_critical_high": "Seek prompt clinical review, especially if fever, severe pain, weakness, or systemic symptoms are present.",
    },
    "Neutrophils": {
        "plain_name": "Neutrophils",
        "what_it_is": "Neutrophils are white blood cells that respond strongly to bacterial infection and inflammation.",
        "why_it_matters": "High neutrophils can occur with infection, inflammation, stress, or steroid use. Low neutrophils can increase infection risk.",
        "normal": "Your neutrophil percentage is within the expected range.",
        "low": "Your neutrophil percentage is below the expected range. This may reduce bacterial infection defense depending on the absolute neutrophil count.",
        "high": "Your neutrophil percentage is above the expected range. This may fit infection, inflammation, physical stress, or medication effects.",
        "advice_normal": "Interpret with total WBC count and symptoms.",
        "advice_low": "Review absolute neutrophil count and consult a clinician if infections or fever are present.",
        "advice_high": "Review for infection/inflammation symptoms and interpret with WBC count.",
    },
    "Lymphocytes": {
        "plain_name": "Lymphocytes",
        "what_it_is": "Lymphocytes are immune cells involved in viral defense and immune regulation.",
        "why_it_matters": "Low or high percentages can occur with infections, stress responses, or immune conditions.",
        "normal": "Your lymphocyte percentage is within the expected range.",
        "low": "Your lymphocyte percentage is below the expected range. This can occur with stress response, acute infection patterns, steroid use, or other causes.",
        "high": "Your lymphocyte percentage is above the expected range. This can occur with viral infections or some immune conditions.",
        "advice_normal": "Interpret with total WBC count and neutrophil percentage.",
        "advice_low": "Review with WBC count and symptoms. A clinician may consider absolute lymphocyte count.",
        "advice_high": "Review for viral symptoms and discuss persistent elevation with a healthcare professional.",
    },
    "Platelets": {
        "plain_name": "Platelet Count",
        "what_it_is": "Platelets help blood clot and prevent bleeding.",
        "why_it_matters": "Low platelets may increase bleeding risk. High platelets can occur with inflammation, infection, iron deficiency, or other conditions.",
        "normal": "Your platelet count is within the expected range.",
        "low": "Your platelet count is below the expected range and may increase bleeding or bruising risk depending on severity.",
        "high": "Your platelet count is above the expected range. This can occur with inflammation, infection, iron deficiency, or other causes.",
        "advice_normal": "No immediate concern from this marker alone.",
        "advice_low": "Seek medical advice if you have easy bruising, nosebleeds, gum bleeding, or tiny red skin spots.",
        "advice_high": "Discuss persistent elevation with a clinician. Iron status and inflammation markers may be reviewed.",
    },
    "HbA1c": {
        "plain_name": "HbA1c",
        "what_it_is": "HbA1c reflects average blood glucose over roughly the previous 2–3 months.",
        "why_it_matters": "It is used to assess diabetes risk and long-term glucose control.",
        "normal": "Your HbA1c is within the expected range.",
        "low": "Your HbA1c is below the expected range, which may occur with frequent low blood glucose or certain blood conditions.",
        "high": "Your HbA1c is above the expected range and may suggest increased diabetes risk or reduced glucose control.",
        "advice_normal": "Maintain balanced nutrition, activity, and routine monitoring if at risk.",
        "advice_low": "Discuss with a clinician if you have symptoms of low blood sugar or blood disorders.",
        "advice_high": "Consider lifestyle review, low-glycemic nutrition, activity after meals, and clinical follow-up.",
    },
    "LDL Cholesterol": {
        "plain_name": "LDL Cholesterol",
        "what_it_is": "LDL cholesterol is often called bad cholesterol because high levels can contribute to plaque buildup in arteries.",
        "why_it_matters": "Elevated LDL is associated with increased cardiovascular risk over time.",
        "normal": "Your LDL cholesterol is within the expected target range.",
        "low": "Low LDL is generally not a concern by itself unless clinically unexpected.",
        "high": "Your LDL cholesterol is above the expected target range and may increase cardiovascular risk.",
        "advice_normal": "Continue heart-healthy nutrition and regular activity.",
        "advice_low": "Discuss with a clinician if unexpectedly very low or if symptoms are present.",
        "advice_high": "Increase soluble fiber, reduce saturated/trans fats, exercise regularly, and discuss cardiovascular risk with a clinician.",
    },
    "Vitamin D": {
        "plain_name": "Vitamin D",
        "what_it_is": "Vitamin D supports bone health, immune function, and muscle function.",
        "why_it_matters": "Low vitamin D can contribute to bone weakness, fatigue, muscle aches, and deficiency risk.",
        "normal": "Your vitamin D is within the expected range.",
        "low": "Your vitamin D is below the expected range, suggesting insufficiency or deficiency.",
        "high": "Your vitamin D is above the expected range and may need supplement review.",
        "advice_normal": "Maintain safe sunlight exposure and dietary sources.",
        "advice_low": "Discuss supplementation, sunlight exposure, and dietary sources with a healthcare professional.",
        "advice_high": "Avoid excessive supplementation and discuss with a clinician.",
    },
    "Ferritin": {
        "plain_name": "Ferritin",
        "what_it_is": "Ferritin reflects stored iron in the body.",
        "why_it_matters": "Low ferritin can support iron deficiency, especially with anemia, low MCV, or fatigue.",
        "normal": "Your ferritin is within the expected range.",
        "low": "Your ferritin is below the expected range and may suggest low iron stores.",
        "high": "Your ferritin is above the expected range and can occur with inflammation, liver disease, iron overload, or infection.",
        "advice_normal": "No immediate concern from this marker alone.",
        "advice_low": "Review iron intake, menstrual/blood loss history, ferritin trend, and consider clinician-guided iron studies.",
        "advice_high": "Discuss inflammation markers, liver tests, iron studies, and clinical context.",
    },
}


def _safe_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return None


def normalize_status(status: Any) -> str:
    s = str(status or "unknown").lower().strip().replace(" ", "_")

    aliases = {
        "critically_low": "critical_low",
        "critically_high": "critical_high",
        "critical": "critical_high",
        "elevated": "high",
        "needs_review": "invalid",
        "within_range": "normal",
    }

    return aliases.get(s, s)


def classify_against_reference(
    value: Any,
    ref_low: Any = None,
    ref_high: Any = None,
) -> str:
    v = _safe_float(value)
    lo = _safe_float(ref_low)
    hi = _safe_float(ref_high)

    if v is None:
        return "unknown"

    if lo is not None and v < lo:
        return "low"

    if hi is not None and v > hi:
        return "high"

    if lo is not None or hi is not None:
        return "normal"

    return "unknown"


def _value_text(test: Dict[str, Any]) -> str:
    value = test.get("value")
    unit = test.get("unit") or ""
    return f"{value} {unit}".strip()


def _reference_range_text(test: Dict[str, Any]) -> str:
    ref_range = test.get("reference_range")

    if ref_range:
        source = test.get("range_source")
        if source == "fallback":
            return f"{ref_range} (generic adult reference)"
        return ref_range

    lo = test.get("reference_low")
    hi = test.get("reference_high")
    unit = test.get("unit") or ""

    if lo is not None and hi is not None:
        return f"{lo} - {hi} {unit}".strip()

    if lo is not None:
        return f"> {lo} {unit}".strip()

    if hi is not None:
        return f"< {hi} {unit}".strip()

    return "Reference range not available"


def build_patient_explanation(test: Dict[str, Any]) -> Dict[str, Any]:
    canonical = test.get("canonical_name", "Unknown")
    meta = TEST_EXPLANATIONS.get(canonical, {})

    # First use the extractor's numeric classification.
    status = normalize_status(test.get("flag"))

    # If flag missing/unknown, classify from reference values.
    if status not in STATUS_LABELS or status == "unknown":
        status = classify_against_reference(
            test.get("value"),
            test.get("reference_low"),
            test.get("reference_high"),
        )

    if status not in STATUS_LABELS:
        status = "unknown"

    plain_name = meta.get("plain_name", canonical)
    status_label = STATUS_LABELS.get(status, status.title())
    severity = SEVERITY.get(status, "unknown")

    if status in ("critical_low", "critical_high"):
        meaning = meta.get(
            status,
            f"{plain_name} appears to be in a critical range."
        )
        advice = meta.get(
            f"advice_{status}",
            "Please seek urgent medical attention or contact a healthcare professional immediately."
        )

    elif status in ("low", "high", "normal"):
        meaning = meta.get(
            status,
            f"{plain_name} is {status_label.lower()} compared with the available reference range."
        )
        advice = meta.get(
            f"advice_{status}",
            "Discuss this result with a healthcare professional if you have symptoms or concerns."
        )

    elif status == "invalid":
        meaning = (
            f"{plain_name} was extracted, but the system recommends technical review "
            "because the value/unit format may need confirmation."
        )
        advice = "Check the original report value and unit, then repeat processing if needed."

    else:
        meaning = (
            f"{plain_name} was extracted, but the system could not confidently classify it."
        )
        advice = "Review this result with the original lab report and a healthcare professional."

    return {
        "display_name": plain_name,
        "value_text": _value_text(test),
        "status": status_label,
        "severity": severity,
        "reference_range": _reference_range_text(test),
        "range_source": test.get("range_source", "unknown"),
        "what_it_is": meta.get(
            "what_it_is",
            f"{plain_name} is a laboratory test parameter."
        ),
        "why_it_matters": meta.get(
            "why_it_matters",
            "This result should be interpreted with the full report and clinical history."
        ),
        "what_your_result_means": meaning,
        "recommendation": advice,
        "disclaimer": DISCLAIMER,
    }


def enrich_lab_tests(tests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    enriched: List[Dict[str, Any]] = []

    for test in tests:
        item = dict(test)
        item["patient_explanation"] = build_patient_explanation(item)
        enriched.append(item)

    return enriched