"""
pipeline/extract.py
Ontology-driven extraction: normalize -> parse -> match -> validate -> confidence.

FIXED VERSION:
- Handles pasted tables whose line breaks were flattened by the UI.
- Handles CBC rows like: Hemoglobin (Hb) 13.8 g/dL 13.0 – 17.0
- Handles units like thousand/µL and million/µL.
- Extracts report reference ranges when present.
"""
import csv
import io
import re
from typing import List, Dict, Any, Optional, Tuple

from pipeline.normalize import normalize_report_text, standardize_units, normalize_unicode
from pipeline.patterns import PATHOLOGY_ROW_PATTERN, TEST_VALUE_PATTERN
from pipeline.test_registry import get_test_by_alias, load_tests
from pipeline.validators import validate_value
from pipeline.confidence import calculate_confidence


_NUM = r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"
_RANGE_RE = re.compile(rf"(?P<low>{_NUM})\s*(?:-|to|–|—)\s*(?P<high>{_NUM})", re.IGNORECASE)

# Generic row parser used before the stricter ontology regex.
# It intentionally accepts wider unit text because OCR/UI output may contain
# units not listed in UNIT_PATTERN yet, e.g. million/uL, thousand/uL.
_GENERIC_ROW_RE = re.compile(
    rf"^\s*(?P<test_name>.+?)\s+"
    rf"(?P<value>{_NUM})\s*"
    rf"(?P<unit>%|[A-Za-z0-9µuU/^./]+(?:/[A-Za-z0-9µuU^./]+)?)?"
    rf"(?:\s+(?P<ref_low>{_NUM})\s*(?:-|to|–|—)\s*(?P<ref_high>{_NUM}))?"
    rf"(?:\s+(?P<flag>H|L|High|Low|Critical|Abnormal|\*))?\s*$",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Flattened text repair
# ---------------------------------------------------------------------------

def _known_test_markers() -> List[str]:
    """Return known aliases sorted longest-first for safe flattened text splitting."""
    markers = set()
    try:
        for _key, meta in load_tests().items():
            if meta.get("canonical_name"):
                markers.add(meta["canonical_name"])
            for alias in meta.get("aliases", []):
                if alias and len(alias.strip()) >= 3:
                    markers.add(alias.strip())
    except Exception:
        # Small fallback for CBC demo if ontology fails to load.
        markers.update(["Hemoglobin", "RBC Count", "WBC Count", "Platelets", "Hematocrit"])

    # Prefer longer phrases first: "RBC Count" before "RBC".
    return sorted(markers, key=len, reverse=True)


def repair_flattened_lab_text(text: str) -> str:
    """
    Convert a flattened pasted report into line-like rows.

    Example input from UI:
        Hemoglobin (Hb) 13.8 g/dL 13.0 – 17.0 RBC Count 5.1 ...

    Output:
        Hemoglobin (Hb) 13.8 g/dL 13.0 – 17.0
        RBC Count 5.1 ...
    """
    if not text or "\n" in text.strip():
        return text

    repaired = text.strip()
    for marker in _known_test_markers():
        # Insert newline before a test marker only when it appears after whitespace.
        # This avoids breaking the first word and avoids matching inside other words.
        pattern = re.compile(rf"(?<!^)\s+(?={re.escape(marker)}(?:\b|\s|\())", re.IGNORECASE)
        repaired = pattern.sub("\n", repaired)

    return repaired.strip()


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


def _clean_alias_for_lookup(raw_alias: str) -> Tuple[str, Optional[dict]]:
    """Resolve alias; if exact lookup fails, remove parenthetical abbreviations."""
    raw_alias = (raw_alias or "").strip(" :-\t")
    meta = get_test_by_alias(raw_alias)
    if meta:
        return raw_alias, meta

    no_paren = re.sub(r"\s*\([^)]*\)\s*", " ", raw_alias).strip(" :-\t")
    meta = get_test_by_alias(no_paren)
    if meta:
        return no_paren, meta

    # If alias is "Hemoglobin Hb" after OCR cleanup, try first phrase before two spaces etc.
    return raw_alias, None


def _status_from_reference_range(value: float, ref_low: Optional[float], ref_high: Optional[float]) -> str:
    if ref_low is None or ref_high is None:
        return "normal"
    if value < ref_low:
        return "low"
    if value > ref_high:
        return "high"
    return "normal"


def _value_for_medical_validation(canonical_name: str, value: float, unit: str) -> float:
    """
    Convert display values to the ontology scale only for validation/confidence.

    WBC and Platelets ontology stores plausible limits as absolute counts per uL,
    while reports commonly display them as 10^3/uL.
    Example: WBC 7.4 10^3/uL means 7400/uL for plausibility checks.
    RBC ontology already uses million/uL-style values, so RBC is not converted.
    """
    c = (canonical_name or "").lower()
    u = (unit or "").lower()
    if c in {"wbc", "platelets"} and u in {"10^3/ul", "x10^3/ul", "k/ul", "thou/ul"}:
        return value * 1000.0
    return value


def _build_result(
    raw_alias: str,
    value: float,
    raw_unit: str,
    flag_str: Optional[str],
    fuzzy_score: Optional[float] = None,
    regex_matched_full_row: bool = False,
    ref_low: Optional[float] = None,
    ref_high: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    """Resolve alias -> metadata -> confidence -> result dict."""
    lookup_alias, test_meta = _clean_alias_for_lookup(raw_alias)
    if not test_meta:
        return None

    canonical = test_meta["canonical_name"]
    unit = standardize_units(raw_unit) if raw_unit else ""
    validation_value = _value_for_medical_validation(canonical, value, unit)

    result = calculate_confidence(
        raw_alias=lookup_alias,
        extracted_value=validation_value,
        extracted_unit=unit or None,
        fuzzy_score=fuzzy_score,
        regex_matched_full_row=regex_matched_full_row,
        test_meta=test_meta,
    )
    confidence = result.get("confidence", 0.0)
    reasons = result.get("reasons", [])

    val_ok, _ = validate_value(validation_value, canonical, unit or None)
    flag = _parse_flag(flag_str)

    # Prefer the lab report's own reference range for user-facing high/low status.
    if flag == "normal" and ref_low is not None and ref_high is not None:
        flag = _status_from_reference_range(value, ref_low, ref_high)

    # Only mark invalid if medically implausible after unit-aware validation.
    if flag == "normal" and not val_ok:
        flag = "invalid"

    item = {
        "canonical_name": canonical,
        "loinc": test_meta.get("loinc", ""),
        "category": test_meta.get("category", ""),
        "raw_alias": raw_alias.strip(),
        "value": value,
        "unit": unit or raw_unit,
        "flag": flag,
        "confidence": confidence,
        "reasons": reasons,
    }

    if ref_low is not None and ref_high is not None:
        item["reference_range"] = f"{ref_low:g} - {ref_high:g} {unit or raw_unit}".strip()
        item["reference_low"] = ref_low
        item["reference_high"] = ref_high

    return item


# ---------------------------------------------------------------------------
# CSV / TSV detection and parsing
# ---------------------------------------------------------------------------

_NAME_COLS = {"test name", "test", "analyte", "parameter", "name", "investigation"}
_VALUE_COLS = {"sample value", "value", "result", "observed value", "observed", "reading"}
_UNIT_COLS = {"unit", "units", "uom"}
_FLAG_COLS = {"flag", "status", "abnormal flag", "interpretation"}
_RANGE_COLS = {"reference range", "range", "normal range", "ref range"}


def _is_csv(text: str) -> bool:
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    return first_line.count(",") >= 2 or first_line.count("\t") >= 2


def _col_index(headers: List[str], candidates: set) -> Optional[int]:
    for i, h in enumerate(headers):
        if h.strip().lower() in candidates:
            return i
    return None


def _parse_range(range_text: str) -> Tuple[Optional[float], Optional[float]]:
    if not range_text:
        return None, None
    m = _RANGE_RE.search(range_text)
    if not m:
        return None, None
    try:
        return float(m.group("low")), float(m.group("high"))
    except ValueError:
        return None, None


def _extract_csv(text: str) -> List[Dict[str, Any]]:
    dialect = "excel-tab" if "\t" in text.splitlines()[0] else "excel"
    reader = csv.reader(io.StringIO(text.strip()), dialect=dialect)
    rows = list(reader)
    if not rows:
        return []

    results = []
    seen: set = set()

    header_row = [c.strip().lower() for c in rows[0]]
    name_idx = _col_index(header_row, _NAME_COLS)
    val_idx = _col_index(header_row, _VALUE_COLS)
    unit_idx = _col_index(header_row, _UNIT_COLS)
    flag_idx = _col_index(header_row, _FLAG_COLS)
    range_idx = _col_index(header_row, _RANGE_COLS)

    has_header = name_idx is not None and val_idx is not None
    data_rows = rows[1:] if has_header else rows

    if not has_header:
        name_idx, val_idx, unit_idx, flag_idx, range_idx = 0, 1, 2, None, 3

    for row in data_rows:
        if not row or len(row) <= val_idx:
            continue
        try:
            raw_alias = row[name_idx].strip()
            value = float(row[val_idx].strip())
            raw_unit = row[unit_idx].strip() if unit_idx is not None and len(row) > unit_idx else ""
            flag_str = row[flag_idx].strip() if flag_idx is not None and len(row) > flag_idx else None
            ref_low, ref_high = _parse_range(row[range_idx]) if range_idx is not None and len(row) > range_idx else (None, None)
        except (ValueError, IndexError):
            continue

        if not raw_alias:
            continue

        item = _build_result(
            raw_alias, value, raw_unit, flag_str,
            fuzzy_score=None, regex_matched_full_row=True,
            ref_low=ref_low, ref_high=ref_high,
        )
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
    # First use a generic row parser that accepts units like million/uL.
    generic = _GENERIC_ROW_RE.match(line)
    if generic:
        raw_alias = generic.group("test_name").strip(" :-\t")
        try:
            value = float(generic.group("value"))
        except (TypeError, ValueError):
            return None
        ref_low = float(generic.group("ref_low")) if generic.group("ref_low") else None
        ref_high = float(generic.group("ref_high")) if generic.group("ref_high") else None
        return {
            "raw_alias": raw_alias,
            "value": value,
            "raw_unit": (generic.group("unit") or "").strip(),
            "flag_str": generic.groupdict().get("flag"),
            "full_match": True,
            "ref_low": ref_low,
            "ref_high": ref_high,
        }

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
    ref_low, ref_high = _parse_range(line[match.end():])

    return {
        "raw_alias": raw_alias,
        "value": value,
        "raw_unit": raw_unit,
        "flag_str": flag_str,
        "full_match": matched_full,
        "ref_low": ref_low,
        "ref_high": ref_high,
    }


def _extract_freeform(text: str) -> List[Dict[str, Any]]:
    text = repair_flattened_lab_text(text)
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
            parsed["raw_unit"], parsed["flag_str"],
            fuzzy_score=None,
            regex_matched_full_row=parsed["full_match"],
            ref_low=parsed.get("ref_low"),
            ref_high=parsed.get("ref_high"),
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
    text = repair_flattened_lab_text(text or "")
    if _is_csv(text):
        return _extract_csv(text)
    return _extract_freeform(text)


# ---------------------------------------------------------------------------
# Backward-compat shim used by classify.py
# ---------------------------------------------------------------------------

def get_canonical_tests():
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
