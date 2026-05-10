"""
pipeline/extract.py
Ontology-driven extraction: normalize -> parse -> match -> validate -> confidence
"""
import re
from typing import List, Dict, Any, Optional

from pipeline.normalize import normalize_report_text, standardize_units
from pipeline.patterns import PATHOLOGY_ROW_PATTERN, TEST_VALUE_PATTERN, FLAG_PATTERN
from pipeline.test_registry import get_test_by_alias, normalize_unit
from pipeline.validators import validate_value, validate_unit, detect_suspicious_result
from pipeline.confidence import calculate_confidence


def _parse_flag(flag_str: Optional[str]) -> str:
    if not flag_str:
        return "normal"
    f = flag_str.strip().lower()
    if f in ("h", "high"):
        return "high"
    if f in ("l", "low"):
        return "low"
    if "crit" in f:
        return "critical"
    if "abn" in f or "*" in f:
        return "abnormal"
    return "normal"


def _extract_from_line(line: str) -> Optional[Dict[str, Any]]:
    match = PATHOLOGY_ROW_PATTERN.match(line)
    if not match:
        match = TEST_VALUE_PATTERN.search(line)
        if not match:
            return None

    raw_alias = match.group("test_name").strip()
    if not raw_alias:
        return None

    try:
        value = float(match.group("value"))
    except (TypeError, ValueError):
        return None

    raw_unit = (match.group("unit") or "").strip()
    flag_str = match.groupdict().get("flag")

    return {
        "raw_alias": raw_alias,
        "value": value,
        "raw_unit": raw_unit,
        "flag_str": flag_str,
    }


def extract_lab_tests(text: str) -> List[Dict[str, Any]]:
    cleaned = normalize_report_text(text)
    results = []
    seen = set()

    for line in cleaned.splitlines():
        line = line.strip()
        if not line:
            continue

        parsed = _extract_from_line(line)
        if not parsed:
            continue

        raw_alias = parsed["raw_alias"]
        value = parsed["value"]
        raw_unit = parsed["raw_unit"]
        flag_str = parsed["flag_str"]

        test_meta = get_test_by_alias(raw_alias)
        if not test_meta:
            continue

        canonical = test_meta["canonical_name"]
        dedup_key = (canonical.lower(), value)
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        unit = standardize_units(raw_unit) if raw_unit else ""

        val_ok, val_reason = validate_value(value, canonical)
        unit_ok, unit_reason = validate_unit(unit, canonical) if unit else (True, "no unit")
        sus_ok, sus_reason = detect_suspicious_result(value, canonical, unit or None)

        confidence = calculate_confidence(
            raw_alias=raw_alias,
            canonical_name=canonical,
            value=value,
            unit=unit,
            value_valid=val_ok,
            unit_valid=unit_ok,
            not_suspicious=sus_ok,
        )

        flag = _parse_flag(flag_str)
        if flag == "normal" and not val_ok:
            flag = "invalid"

        results.append({
            "canonical_name": canonical,
            "loinc": test_meta.get("loinc", ""),
            "category": test_meta.get("category", ""),
            "raw_alias": raw_alias,
            "value": value,
            "unit": unit or raw_unit,
            "flag": flag,
            "confidence": confidence,
        })

    return results


# Backward-compat shim used by classify.py
def get_canonical_tests():
    from pipeline.test_registry import load_tests
    raw = load_tests()
    out = {}
    for key, meta in raw.items():
        out[key] = {
            "unit": (meta.get("expected_units") or [""])[0],
            "low": meta.get("reference_low", meta.get("min_value", 0)),
            "high": meta.get("reference_high", meta.get("max_value", 9999)),
            "critical_low": meta.get("critical_low", meta.get("min_value", 0)),
            "critical_high": meta.get("critical_high", meta.get("max_value", 9999)),
        }
    return out