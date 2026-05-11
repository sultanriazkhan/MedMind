"""
pipeline/extract.py
Ontology-driven extraction: normalize -> parse -> match -> validate -> confidence
Handles: freeform report text, CSV (with or without header), TSV
"""
import csv
import io
from typing import List, Dict, Any, Optional

from pipeline.normalize import normalize_report_text, standardize_units
from pipeline.patterns import PATHOLOGY_ROW_PATTERN, TEST_VALUE_PATTERN
from pipeline.test_registry import get_test_by_alias
from pipeline.validators import validate_value
from pipeline.confidence import calculate_confidence


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


def _build_result(
    raw_alias: str,
    value: float,
    raw_unit: str,
    flag_str: Optional[str],
    fuzzy_score: Optional[float] = None,
    regex_matched_full_row: bool = False,
) -> Optional[Dict[str, Any]]:
    """Resolve alias -> metadata -> confidence -> dict."""
    test_meta = get_test_by_alias(raw_alias)
    if not test_meta:
        return None

    canonical = test_meta["canonical_name"]
    unit = standardize_units(raw_unit) if raw_unit else ""

    # calculate_confidence signature:
    # (raw_alias, extracted_value, extracted_unit=None, fuzzy_score=None,
    #  regex_matched_full_row=False, test_meta=None) -> {"confidence": float, "reasons": list}
    result = calculate_confidence(
        raw_alias=raw_alias,
        extracted_value=value,
        extracted_unit=unit or None,
        fuzzy_score=fuzzy_score,
        regex_matched_full_row=regex_matched_full_row,
        test_meta=test_meta,
    )
    confidence = result.get("confidence", 0.0)
    reasons    = result.get("reasons", [])

    val_ok, _ = validate_value(value, canonical)
    flag = _parse_flag(flag_str)
    if flag == "normal" and not val_ok:
        flag = "invalid"

    return {
        "canonical_name": canonical,
        "loinc":          test_meta.get("loinc", ""),
        "category":       test_meta.get("category", ""),
        "raw_alias":      raw_alias,
        "value":          value,
        "unit":           unit or raw_unit,
        "flag":           flag,
        "confidence":     confidence,
        "reasons":        reasons,
    }


# ---------------------------------------------------------------------------
# CSV / TSV detection and parsing
# ---------------------------------------------------------------------------

_NAME_COLS  = {"test name", "test", "analyte", "parameter", "name", "investigation"}
_VALUE_COLS = {"sample value", "value", "result", "observed value", "observed", "reading"}
_UNIT_COLS  = {"unit", "units", "uom"}
_FLAG_COLS  = {"flag", "status", "abnormal flag", "interpretation"}


def _is_csv(text: str) -> bool:
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    return first_line.count(",") >= 2 or first_line.count("\t") >= 2


def _col_index(headers: List[str], candidates: set) -> Optional[int]:
    for i, h in enumerate(headers):
        if h.strip().lower() in candidates:
            return i
    return None


def _extract_csv(text: str) -> List[Dict[str, Any]]:
    dialect   = "excel-tab" if "\t" in text.splitlines()[0] else "excel"
    reader    = csv.reader(io.StringIO(text.strip()), dialect=dialect)
    rows      = list(reader)
    if not rows:
        return []

    results = []
    seen: set = set()

    header_row = [c.strip().lower() for c in rows[0]]
    name_idx  = _col_index(header_row, _NAME_COLS)
    val_idx   = _col_index(header_row, _VALUE_COLS)
    unit_idx  = _col_index(header_row, _UNIT_COLS)
    flag_idx  = _col_index(header_row, _FLAG_COLS)

    has_header = name_idx is not None and val_idx is not None
    data_rows  = rows[1:] if has_header else rows

    if not has_header:
        name_idx, val_idx, unit_idx, flag_idx = 0, 1, 2, None

    for row in data_rows:
        if not row or len(row) <= val_idx:
            continue
        try:
            raw_alias = row[name_idx].strip()
            value     = float(row[val_idx].strip())
            raw_unit  = row[unit_idx].strip() if unit_idx is not None and len(row) > unit_idx else ""
            flag_str  = row[flag_idx].strip() if flag_idx is not None and len(row) > flag_idx else None
        except (ValueError, IndexError):
            continue

        if not raw_alias:
            continue

        item = _build_result(raw_alias, value, raw_unit, flag_str,
                             fuzzy_score=None, regex_matched_full_row=False)
        if item is None:
            continue

        dedup_key = (item["canonical_name"].lower(), value)
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        results.append(item)

    return results


# ---------------------------------------------------------------------------
# Freeform line parsing
# ---------------------------------------------------------------------------

def _extract_from_line(line: str) -> Optional[Dict[str, Any]]:
    full_match = PATHOLOGY_ROW_PATTERN.match(line)
    if full_match:
        matched_full = True
        match = full_match
    else:
        match = TEST_VALUE_PATTERN.search(line)
        matched_full = False
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
        "raw_alias":   raw_alias,
        "value":       value,
        "raw_unit":    raw_unit,
        "flag_str":    flag_str,
        "full_match":  matched_full,
    }


def _extract_freeform(text: str) -> List[Dict[str, Any]]:
    cleaned = normalize_report_text(text)
    results = []
    seen: set = set()

    for line in cleaned.splitlines():
        line = line.strip()
        if not line:
            continue

        parsed = _extract_from_line(line)
        if not parsed:
            continue

        item = _build_result(
            parsed["raw_alias"], parsed["value"],
            parsed["raw_unit"],  parsed["flag_str"],
            fuzzy_score=None,
            regex_matched_full_row=parsed["full_match"],
        )
        if item is None:
            continue

        dedup_key = (item["canonical_name"].lower(), item["value"])
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        results.append(item)

    return results


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def extract_lab_tests(text: str) -> List[Dict[str, Any]]:
    """Auto-detect CSV/TSV vs freeform and extract lab tests."""
    if _is_csv(text):
        return _extract_csv(text)
    return _extract_freeform(text)


# ---------------------------------------------------------------------------
# Backward-compat shim used by classify.py
# ---------------------------------------------------------------------------

def get_canonical_tests():
    from pipeline.test_registry import load_tests
    raw = load_tests()
    out = {}
    for key, meta in raw.items():
        out[key] = {
            "unit":          (meta.get("expected_units") or [""])[0],
            "low":           meta.get("reference_low",   meta.get("min_value",    0)),
            "high":          meta.get("reference_high",  meta.get("max_value",    9999)),
            "critical_low":  meta.get("critical_low",    meta.get("min_value",    0)),
            "critical_high": meta.get("critical_high",   meta.get("max_value",    9999)),
        }
    return out