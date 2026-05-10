from typing import Dict, List, Any, Optional

from Medical_base import (
    MEDICAL_KNOWLEDGE_BASE,
    normalize_test_name,
    get_normal_range
)


DEFAULT_EXPLANATION = {
    "meaning": "No medical interpretation available.",
    "causes": "Unknown",
    "effects": "Unknown",
    "solution": "Consult healthcare professional."
}


def get_explanation(
    test_name: str,
    value=None,
    status: Optional[str] = None,
    unit=None,
    gender=None,
    age=None
) -> Dict[str, Any]:

    standardized_name = normalize_test_name(test_name)

    if not standardized_name:
        default = DEFAULT_EXPLANATION.copy()

        default["meaning"] = (
            f"No explanation available for {test_name}"
        )

        return default

    test_data = MEDICAL_KNOWLEDGE_BASE.get(standardized_name)

    if not test_data:
        return DEFAULT_EXPLANATION

    if not status:
        status = "Normal"

    interpretation = test_data.get("interpretation", {})

    if not interpretation:
        interpretation = test_data.get(
            "Normal",
            DEFAULT_EXPLANATION
        )

    return {
        "test_name": test_name,
        "canonical_name": standardized_name,
        "value": value,
        "unit": unit,
        "reference_range": get_normal_range(test_name),
        "status": status,
        "meaning": interpretation.get("meaning"),
        "causes": interpretation.get("causes"),
        "effects": interpretation.get("effects"),
        "solution": interpretation.get("solution")
    }


def explain_full_report(
    report_data: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    results = []

    for test in report_data:

        result = get_explanation(
            test_name=test.get("test_name", ""),
            value=test.get("value"),
            status=test.get("status"),
            unit=test.get("unit"),
            gender=test.get("gender"),
            age=test.get("age")
        )

        results.append(result)

    return results