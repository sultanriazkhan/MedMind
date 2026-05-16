"""
pipeline/report_summary.py
Creates a user-centered overall summary from enriched lab test results.
"""
from __future__ import annotations

from typing import Any, Dict, List


def build_report_summary(tests: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(tests)
    normal = []
    attention = []
    review = []
    urgent = []

    for t in tests:
        pe = t.get("patient_explanation", {})
        name = pe.get("display_name") or t.get("canonical_name", "Unknown test")
        status = pe.get("status", "Unknown")
        severity = pe.get("severity", "unknown")

        row = {
            "test": name,
            "value": pe.get("value_text", str(t.get("value", ""))),
            "status": status,
            "meaning": pe.get("what_your_result_means", ""),
        }

        if severity == "urgent":
            urgent.append(row)
        elif severity == "review":
            review.append(row)
        elif status.lower() == "normal":
            normal.append(row)
        else:
            attention.append(row)

    if urgent:
        overall = "Some results appear urgent and should be reviewed by a healthcare professional immediately."
    elif attention:
        overall = "Some results are outside the provided reference range and may need clinical review."
    elif review:
        overall = "The results were extracted, but some values need technical review because of unit/value formatting."
    elif total:
        overall = "All extracted results are within the provided reference ranges."
    else:
        overall = "No lab tests were extracted from the input."

    return {
        "total_tests": total,
        "normal_count": len(normal),
        "attention_count": len(attention),
        "review_count": len(review),
        "urgent_count": len(urgent),
        "overall_message": overall,
        "normal_results": normal,
        "results_needing_attention": attention,
        "results_needing_review": review,
        "urgent_results": urgent,
    }
