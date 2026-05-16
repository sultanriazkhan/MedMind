"""
pipeline/extract.py

Robust lab report extraction for MedMind.

Handles:
- Colon format:
  Hemoglobin: 8.2 g/dL

- Table-like rows:
  Hemoglobin 8.2 g/dL 12.0 - 15.5

- PDF cell extraction:
  Hemoglobin
  8.2
  g/dL

- Unicode scientific units:
  RBC Count: 3.1 × 10¹²/L
  WBC Count: 14.2 × 10⁹/L

- Missing reference ranges:
  Uses built-in fallback adult reference ranges.

Output:
A list of extracted test dictionaries enriched with:
- canonical_name
- value
- unit
- reference_low
- reference_high
- reference_range
- flag
- confidence
"""

from __future__ import annotations

import csv
import io
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    from pipeline.normalize import normalize_report_text, standardize_units, normalize_unicode
except Exception:
    def normalize_report_text(text: str) -> str:
        return text or ""

    def standardize_units(unit: str) -> str:
        return unit or ""

    def normalize_unicode(text: str) -> str:
        return text or ""

try:
    from pipeline.test_registry import get_test_by_alias, load_tests
except Exception:
    def get_test_by_alias(alias: str):
        return None

    def load_tests():
        return {}

try:
    from pipeline.confidence import calculate_confidence
except Exception:
    def calculate_confidence(**kwargs):
        return {"confidence": 0.85, "reasons": ["fallback confidence"]}

try:
    from pipeline.validators import validate_value
except Exception:
    def validate_value(value, test_name, unit=None):
        return True, "validation skipped"


# ---------------------------------------------------------------------------
# Numeric / unit helpers
# ---------------------------------------------------------------------------

_NUM = r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"

_SUPERSCRIPT_MAP = str.maketrans({
    "⁰": "0",
    "¹": "1",
    "²": "2",
    "³": "3",
    "⁴": "4",
    "⁵": "5",
    "⁶": "6",
    "⁷": "7",
    "⁸": "8",
    "⁹": "9",
    "⁻": "-",
})

_RANGE_RE = re.compile(
    rf"(?P<low>{_NUM})\s*(?:-|to|–|—)\s*(?P<high>{_NUM})",
    re.IGNORECASE,
)

_LESS_THAN_RE = re.compile(
    rf"(?:<|<=|less than|below)\s*(?P<high>{_NUM})",
    re.IGNORECASE,
)

_GREATER_THAN_RE = re.compile(
    rf"(?:>|>=|greater than|above)\s*(?P<low>{_NUM})",
    re.IGNORECASE,
)

_COLON_ROW_RE = re.compile(
    rf"""
    ^
    (?P<test_name>[A-Za-z][A-Za-z0-9\s\-/().%]+?)
    \s*
    (?::|=|-)
    \s*
    (?P<value>{_NUM})
    \s*
    (?P<unit>.*?)
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)

_GENERIC_ROW_RE = re.compile(
    rf"""
    ^
    (?P<test_name>[A-Za-z][A-Za-z0-9\s\-/().%]+?)
    \s+
    (?P<value>{_NUM})
    \s*
    (?P<unit>
        %|
        [A-Za-zµuU/%^.*×x0-9+\-\s]+?
    )?
    (?:
        \s+
        (?P<ref_low>{_NUM})
        \s*(?:-|to|–|—)\s*
        (?P<ref_high>{_NUM})
    )?
    (?:
        \s+
        (?P<flag>H|L|High|Low|Critical|Abnormal|Elevated|Normal|Good)
    )?
    \s*$
    """,
    re.VERBOSE | re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Built-in alias map
# ---------------------------------------------------------------------------

LOCAL_ALIAS_TO_CANONICAL = {
    "hb": "Hemoglobin",
    "hgb": "Hemoglobin",
    "hemoglobin": "Hemoglobin",
    "haemoglobin": "Hemoglobin",

    "rbc": "RBC",
    "rbc count": "RBC",
    "red blood cell count": "RBC",
    "red blood cells": "RBC",

    "hematocrit": "Hematocrit",
    "hct": "Hematocrit",
    "pcv": "Hematocrit",

    "mcv": "MCV",
    "mean corpuscular volume": "MCV",

    "mch": "MCH",
    "mean corpuscular hemoglobin": "MCH",

    "mchc": "MCHC",
    "mean corpuscular hemoglobin concentration": "MCHC",

    "rdw": "RDW",
    "rdw-cv": "RDW",
    "red cell distribution width": "RDW",

    "wbc": "WBC",
    "wbc count": "WBC",
    "white blood cell count": "WBC",
    "white blood cells": "WBC",
    "tlc": "WBC",
    "total leukocyte count": "WBC",

    "neutrophils": "Neutrophils",
    "neutrophil": "Neutrophils",
    "neut": "Neutrophils",

    "lymphocytes": "Lymphocytes",
    "lymphocyte": "Lymphocytes",
    "lymph": "Lymphocytes",

    "monocytes": "Monocytes",
    "mono": "Monocytes",

    "eosinophils": "Eosinophils",
    "eos": "Eosinophils",

    "basophils": "Basophils",
    "baso": "Basophils",

    "platelets": "Platelets",
    "platelet count": "Platelets",
    "plt": "Platelets",

    "esr": "ESR",
    "erythrocyte sedimentation rate": "ESR",

    "crp": "CRP",
    "c reactive protein": "CRP",
    "c-reactive protein": "CRP",

    "glucose": "Blood Glucose",
    "blood glucose": "Blood Glucose",
    "fasting glucose": "Blood Glucose",
    "fasting blood glucose": "Blood Glucose",

    "hba1c": "HbA1c",
    "hb a1c": "HbA1c",
    "glycated hemoglobin": "HbA1c",

    "ldl": "LDL Cholesterol",
    "ldl cholesterol": "LDL Cholesterol",

    "hdl": "HDL Cholesterol",
    "hdl cholesterol": "HDL Cholesterol",

    "triglycerides": "Triglycerides",
    "tg": "Triglycerides",

    "total cholesterol": "Cholesterol Total",
    "cholesterol": "Cholesterol Total",

    "vitamin d": "Vitamin D",
    "25 oh vitamin d": "Vitamin D",
    "25-oh vitamin d": "Vitamin D",

    "ferritin": "Ferritin",

    "creatinine": "Creatinine",
    "serum creatinine": "Creatinine",

    "bun": "BUN",
    "blood urea nitrogen": "BUN",

    "urea": "Urea",
    "uric acid": "Uric Acid",

    "alt": "ALT",
    "sgpt": "ALT",

    "ast": "AST",
    "sgot": "AST",

    "sodium": "Sodium",
    "na": "Sodium",

    "potassium": "Potassium",
    "k": "Potassium",

    "calcium": "Calcium",
    "magnesium": "Magnesium",

    "tsh": "TSH",
    "free t4": "Free T4",
    "ft4": "Free T4",
    "free t3": "Free T3",
    "ft3": "Free T3",
}


# ---------------------------------------------------------------------------
# Fallback adult reference ranges
# These are generic educational ranges for prototype classification.
# Real apps should apply age/sex/lab-specific ranges.
# ---------------------------------------------------------------------------

FALLBACK_RANGES: Dict[str, Dict[str, Any]] = {
    "Hemoglobin": {
        "low": 12.0,
        "high": 17.5,
        "unit": "g/dL",
        "critical_low": 7.0,
        "critical_high": 20.0,
    },
    "RBC": {
        "low": 4.2,
        "high": 5.9,
        "unit": "10^6/uL",
        "critical_low": 2.5,
        "critical_high": 7.0,
    },
    "Hematocrit": {
        "low": 36.0,
        "high": 52.0,
        "unit": "%",
        "critical_low": 20.0,
        "critical_high": 60.0,
    },
    "MCV": {
        "low": 80.0,
        "high": 100.0,
        "unit": "fL",
        "critical_low": 60.0,
        "critical_high": 120.0,
    },
    "MCH": {
        "low": 27.0,
        "high": 33.0,
        "unit": "pg",
        "critical_low": 20.0,
        "critical_high": 40.0,
    },
    "MCHC": {
        "low": 31.5,
        "high": 36.0,
        "unit": "g/dL",
        "critical_low": 25.0,
        "critical_high": 40.0,
    },
    "RDW": {
        "low": 11.5,
        "high": 14.5,
        "unit": "%",
        "critical_low": 10.0,
        "critical_high": 20.0,
    },
    "WBC": {
        "low": 4.0,
        "high": 11.0,
        "unit": "10^3/uL",
        "critical_low": 2.0,
        "critical_high": 30.0,
    },
    "Neutrophils": {
        "low": 40.0,
        "high": 70.0,
        "unit": "%",
        "critical_low": 20.0,
        "critical_high": 90.0,
    },
    "Lymphocytes": {
        "low": 20.0,
        "high": 40.0,
        "unit": "%",
        "critical_low": 10.0,
        "critical_high": 60.0,
    },
    "Monocytes": {
        "low": 2.0,
        "high": 10.0,
        "unit": "%",
        "critical_low": 0.0,
        "critical_high": 20.0,
    },
    "Eosinophils": {
        "low": 0.0,
        "high": 6.0,
        "unit": "%",
        "critical_low": 0.0,
        "critical_high": 15.0,
    },
    "Basophils": {
        "low": 0.0,
        "high": 2.0,
        "unit": "%",
        "critical_low": 0.0,
        "critical_high": 5.0,
    },
    "Platelets": {
        "low": 150.0,
        "high": 450.0,
        "unit": "10^3/uL",
        "critical_low": 50.0,
        "critical_high": 1000.0,
    },
    "ESR": {
        "low": 0.0,
        "high": 20.0,
        "unit": "mm/hr",
        "critical_low": 0.0,
        "critical_high": 100.0,
    },
    "CRP": {
        "low": 0.0,
        "high": 5.0,
        "unit": "mg/L",
        "critical_low": 0.0,
        "critical_high": 100.0,
    },
    "Blood Glucose": {
        "low": 70.0,
        "high": 100.0,
        "unit": "mg/dL",
        "critical_low": 50.0,
        "critical_high": 250.0,
    },
    "HbA1c": {
        "low": 4.0,
        "high": 5.7,
        "unit": "%",
        "critical_low": 3.0,
        "critical_high": 9.0,
    },
    "LDL Cholesterol": {
        "low": 0.0,
        "high": 100.0,
        "unit": "mg/dL",
        "critical_low": 0.0,
        "critical_high": 190.0,
    },
    "HDL Cholesterol": {
        "low": 40.0,
        "high": 100.0,
        "unit": "mg/dL",
        "critical_low": 20.0,
        "critical_high": 150.0,
        "higher_is_better": True,
    },
    "Triglycerides": {
        "low": 0.0,
        "high": 150.0,
        "unit": "mg/dL",
        "critical_low": 0.0,
        "critical_high": 500.0,
    },
    "Cholesterol Total": {
        "low": 0.0,
        "high": 200.0,
        "unit": "mg/dL",
        "critical_low": 0.0,
        "critical_high": 300.0,
    },
    "Vitamin D": {
        "low": 30.0,
        "high": 100.0,
        "unit": "ng/mL",
        "critical_low": 10.0,
        "critical_high": 150.0,
    },
    "Ferritin": {
        "low": 30.0,
        "high": 300.0,
        "unit": "ng/mL",
        "critical_low": 10.0,
        "critical_high": 1000.0,
    },
    "Creatinine": {
        "low": 0.6,
        "high": 1.3,
        "unit": "mg/dL",
        "critical_low": 0.2,
        "critical_high": 5.0,
    },
    "BUN": {
        "low": 7.0,
        "high": 20.0,
        "unit": "mg/dL",
        "critical_low": 3.0,
        "critical_high": 80.0,
    },
    "Urea": {
        "low": 15.0,
        "high": 45.0,
        "unit": "mg/dL",
        "critical_low": 5.0,
        "critical_high": 150.0,
    },
    "Uric Acid": {
        "low": 3.5,
        "high": 7.2,
        "unit": "mg/dL",
        "critical_low": 1.0,
        "critical_high": 12.0,
    },
    "ALT": {
        "low": 0.0,
        "high": 45.0,
        "unit": "U/L",
        "critical_low": 0.0,
        "critical_high": 500.0,
    },
    "AST": {
        "low": 0.0,
        "high": 40.0,
        "unit": "U/L",
        "critical_low": 0.0,
        "critical_high": 500.0,
    },
    "Sodium": {
        "low": 135.0,
        "high": 145.0,
        "unit": "mmol/L",
        "critical_low": 125.0,
        "critical_high": 155.0,
    },
    "Potassium": {
        "low": 3.5,
        "high": 5.1,
        "unit": "mmol/L",
        "critical_low": 2.8,
        "critical_high": 6.2,
    },
    "Calcium": {
        "low": 8.5,
        "high": 10.5,
        "unit": "mg/dL",
        "critical_low": 7.0,
        "critical_high": 12.5,
    },
    "Magnesium": {
        "low": 1.7,
        "high": 2.2,
        "unit": "mg/dL",
        "critical_low": 1.0,
        "critical_high": 4.0,
    },
    "TSH": {
        "low": 0.4,
        "high": 4.0,
        "unit": "mIU/L",
        "critical_low": 0.05,
        "critical_high": 20.0,
    },
    "Free T4": {
        "low": 0.8,
        "high": 1.8,
        "unit": "ng/dL",
        "critical_low": 0.3,
        "critical_high": 4.0,
    },
    "Free T3": {
        "low": 2.3,
        "high": 4.2,
        "unit": "pg/mL",
        "critical_low": 1.0,
        "critical_high": 8.0,
    },
}


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def normalize_text_for_extraction(text: str) -> str:
    text = text or ""
    text = normalize_unicode(text)
    text = text.translate(_SUPERSCRIPT_MAP)

    replacements = {
        "×": "x",
        "✕": "x",
        "µ": "u",
        "μ": "u",
        "㎕": "uL",
        "⁄": "/",
        "–": "-",
        "—": "-",
        "\t": " ",
        "\r": "\n",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Convert x 10 12 / L or x10¹²/L style into x10^12/L
    text = re.sub(r"x\s*10\s*([36912]+)\s*/\s*L", r"x10^\1/L", text, flags=re.IGNORECASE)
    text = re.sub(r"10\s*\^\s*([36912]+)\s*/\s*L", r"10^\1/L", text, flags=re.IGNORECASE)
    text = re.sub(r"10\s*\^\s*([36])\s*/\s*uL", r"10^\1/uL", text, flags=re.IGNORECASE)

    # Normalize bullet-like lines.
    text = re.sub(r"^[\s•\-*]+", "", text, flags=re.MULTILINE)

    return text


def normalize_unit(unit: str, canonical_name: str = "") -> str:
    unit = (unit or "").strip()
    unit = unit.translate(_SUPERSCRIPT_MAP)
    unit = unit.replace("µ", "u").replace("μ", "u").replace("×", "x")
    unit = re.sub(r"\s+", "", unit)

    lower = unit.lower()

    mapping = {
        "g/dl": "g/dL",
        "gm/dl": "g/dL",
        "mg/dl": "mg/dL",
        "ng/ml": "ng/mL",
        "pg/ml": "pg/mL",
        "iu/l": "IU/L",
        "u/l": "U/L",
        "mmol/l": "mmol/L",
        "meq/l": "mEq/L",
        "miu/l": "mIU/L",
        "miu/ml": "mIU/mL",
        "%": "%",
        "fl": "fL",
        "pg": "pg",
        "mm/hr": "mm/hr",
        "mm/h": "mm/hr",
        "mg/l": "mg/L",
    }

    if lower in mapping:
        return mapping[lower]

    # Convert SI blood count units to display-friendly units.
    if lower in {"x10^9/l", "10^9/l"}:
        if canonical_name in {"WBC", "Platelets"}:
            return "10^3/uL"
        return "10^9/L"

    if lower in {"x10^12/l", "10^12/l"}:
        if canonical_name == "RBC":
            return "10^6/uL"
        return "10^12/L"

    if lower in {"x10^3/ul", "10^3/ul", "k/ul"}:
        return "10^3/uL"

    if lower in {"x10^6/ul", "10^6/ul", "m/ul"}:
        return "10^6/uL"

    try:
        return standardize_units(unit)
    except Exception:
        return unit


def normalize_value_for_unit(value: float, unit: str, canonical_name: str) -> float:
    """
    Convert equivalent display units so comparison uses fallback ranges.
    """
    unit_l = (unit or "").lower()

    # RBC 3.1 x10^12/L is equivalent to 3.1 x10^6/uL, numeric unchanged.
    # WBC 14.2 x10^9/L is equivalent to 14.2 x10^3/uL, numeric unchanged.
    # Platelets 245 x10^9/L is equivalent to 245 x10^3/uL, numeric unchanged.
    return float(value)


# ---------------------------------------------------------------------------
# Alias resolution
# ---------------------------------------------------------------------------

def clean_alias(alias: str) -> str:
    alias = alias or ""
    alias = alias.strip()
    alias = re.sub(r"\s*\([^)]*\)\s*", " ", alias)
    alias = re.sub(r"\s+", " ", alias)
    alias = alias.strip(" :-")
    return alias


def _looks_like_narrative_alias(alias_key: str) -> bool:
    """
    Prevent prose/sentences from being extracted as test names.

    Example false positive:
    'ldl cholesterol mild dyslipidemia pattern with elevated ldl and triglycerides'
    """

    if not alias_key:
        return True

    words = alias_key.split()

    # Real test aliases are usually short.
    # Examples:
    # hemoglobin
    # rbc count
    # ldl cholesterol
    # fasting blood glucose
    if len(words) > 5:
        return True

    narrative_words = {
        "pattern",
        "with",
        "without",
        "suggests",
        "suggesting",
        "indicates",
        "indicating",
        "shows",
        "showing",
        "detected",
        "mild",
        "moderate",
        "severe",
        "risk",
        "because",
        "therefore",
        "recommend",
        "recommendation",
        "summary",
        "impression",
        "elevated",
        "reduced",
        "increased",
        "decreased",
    }

    if any(word in narrative_words for word in words):
        return True

    # Reject long sentence-like aliases.
    if "." in alias_key or "," in alias_key or ";" in alias_key:
        return True

    return False


def resolve_test(raw_alias: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:

    alias = clean_alias(raw_alias)
    key = alias.lower()

    if not key:
        return None, None

    # Reject obvious sentence fragments before alias matching.
    if _looks_like_narrative_alias(key):
        return None, None

    # 1. Ontology exact/fuzzy resolver first.
    try:
        meta = get_test_by_alias(alias)
        if meta:
            canonical = meta.get("canonical_name", alias)
            return canonical, meta
    except Exception:
        pass

    # 2. Local exact alias.
    if key in LOCAL_ALIAS_TO_CANONICAL:
        canonical = LOCAL_ALIAS_TO_CANONICAL[key]
        return canonical, {
            "canonical_name": canonical,
            "aliases": [alias],
            "category": guess_category(canonical),
            "loinc": "",
            "expected_units": [FALLBACK_RANGES.get(canonical, {}).get("unit", "")],
            "min_value": FALLBACK_RANGES.get(canonical, {}).get("critical_low", -999999),
            "max_value": FALLBACK_RANGES.get(canonical, {}).get("critical_high", 999999),
        }

    # 3. Parenthetical-cleaned exact alias.
    cleaned_no_paren = re.sub(r"\s*\([^)]*\)\s*", " ", alias)
    cleaned_no_paren = re.sub(r"\s+", " ", cleaned_no_paren).strip().lower()

    if cleaned_no_paren in LOCAL_ALIAS_TO_CANONICAL:
        canonical = LOCAL_ALIAS_TO_CANONICAL[cleaned_no_paren]
        return canonical, {
            "canonical_name": canonical,
            "aliases": [alias],
            "category": guess_category(canonical),
            "loinc": "",
            "expected_units": [FALLBACK_RANGES.get(canonical, {}).get("unit", "")],
            "min_value": FALLBACK_RANGES.get(canonical, {}).get("critical_low", -999999),
            "max_value": FALLBACK_RANGES.get(canonical, {}).get("critical_high", 999999),
        }

    return None, None


def guess_category(canonical: str) -> str:
    if canonical in {
        "Hemoglobin", "RBC", "Hematocrit", "MCV", "MCH", "MCHC", "RDW",
        "WBC", "Neutrophils", "Lymphocytes", "Monocytes", "Eosinophils",
        "Basophils", "Platelets",
    }:
        return "CBC"

    if canonical in {"LDL Cholesterol", "HDL Cholesterol", "Triglycerides", "Cholesterol Total"}:
        return "Lipid Profile"

    if canonical in {"ALT", "AST"}:
        return "LFT"

    if canonical in {"Creatinine", "BUN", "Urea", "Uric Acid"}:
        return "RFT"

    if canonical in {"TSH", "Free T4", "Free T3"}:
        return "Thyroid"

    return "General"


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def parse_range(text: str) -> Tuple[Optional[float], Optional[float]]:
    text = text or ""

    m = _RANGE_RE.search(text)
    if m:
        return float(m.group("low")), float(m.group("high"))

    m = _LESS_THAN_RE.search(text)
    if m:
        return None, float(m.group("high"))

    m = _GREATER_THAN_RE.search(text)
    if m:
        return float(m.group("low")), None

    return None, None


def classify_value(
    canonical_name: str,
    value: float,
    ref_low: Optional[float],
    ref_high: Optional[float],
) -> str:
    fallback = FALLBACK_RANGES.get(canonical_name, {})

    critical_low = fallback.get("critical_low")
    critical_high = fallback.get("critical_high")
    higher_is_better = fallback.get("higher_is_better", False)

    if critical_low is not None and value <= critical_low:
        return "critical_low"

    if critical_high is not None and value >= critical_high:
        return "critical_high"

    if ref_low is not None and value < ref_low:
        return "low"

    if ref_high is not None and value > ref_high:
        if higher_is_better:
            return "normal"
        return "high"

    return "normal"


def status_label_to_flag(status: str) -> str:
    s = (status or "").lower().strip()

    if s in {"h", "high", "elevated"}:
        return "high"

    if s in {"l", "low"}:
        return "low"

    if "critical" in s:
        return "critical_high"

    if s in {"normal", "good", "stable", "within range"}:
        return "normal"

    if s in {"abnormal", "borderline", "review"}:
        return "abnormal"

    return "normal"


# ---------------------------------------------------------------------------
# Row parsing
# ---------------------------------------------------------------------------

def extract_value_unit_remainder(text: str) -> Tuple[Optional[float], str, str]:
    text = (text or "").strip()

    m = re.search(_NUM, text)
    if not m:
        return None, "", text

    value = float(m.group(0))
    after = text[m.end():].strip()

    # Unit ends before a reference range or status word.
    unit = after

    split_markers = [
        r"\s+\d+(?:\.\d+)?\s*[-to–—]+",
        r"\s+<\s*\d",
        r"\s+>\s*\d",
        r"\s+Normal\b",
        r"\s+High\b",
        r"\s+Low\b",
        r"\s+Elevated\b",
        r"\s+Critical\b",
        r"\s+Abnormal\b",
        r"\s+Good\b",
    ]

    cut = len(after)

    for pattern in split_markers:
        sm = re.search(pattern, after, flags=re.IGNORECASE)
        if sm:
            cut = min(cut, sm.start())

    unit = after[:cut].strip()
    remainder = after[cut:].strip()

    return value, unit, remainder


def parse_line(line: str) -> Optional[Dict[str, Any]]:
    line = normalize_text_for_extraction(line).strip()

    if not line:
        return None

    # Remove list bullets.
    line = line.strip("•*- ")

    # Ignore obvious headers.
    if line.lower() in {
        "test name", "test", "result", "unit", "normal range", "reference range",
        "status", "trend", "complete blood count", "complete blood count & metabolic panel",
    }:
        return None

    # Colon/equal style.
    m = _COLON_ROW_RE.match(line)
    if m:
        raw_alias = m.group("test_name")
        raw_alias_clean = clean_alias(raw_alias)

        if _looks_like_narrative_alias(raw_alias_clean.lower()):
            return None

        canonical_check, _ = resolve_test(raw_alias_clean)
        if not canonical_check:
            return None
        value = float(m.group("value"))
        rest = m.group("unit") or ""

        unit = rest
        ref_low, ref_high = parse_range(rest)
        flag = None

        for word in ["Critical", "Elevated", "Abnormal", "High", "Low", "Normal", "Good"]:
            if re.search(rf"\b{word}\b", rest, re.IGNORECASE):
                flag = word
                unit = re.split(rf"\b{word}\b", unit, flags=re.IGNORECASE)[0].strip()
                break

        # Cut unit before reference range.
        range_match = _RANGE_RE.search(unit) or _LESS_THAN_RE.search(unit) or _GREATER_THAN_RE.search(unit)
        if range_match:
            unit = unit[:range_match.start()].strip()

        return {
            "raw_alias": raw_alias,
            "value": value,
            "raw_unit": unit,
            "flag_str": flag,
            "ref_low": ref_low,
            "ref_high": ref_high,
            "full_match": True,
        }

    # Generic row style.
    m = _GENERIC_ROW_RE.match(line)
    if m:
        raw_alias = m.group("test_name")
        value = float(m.group("value"))
        raw_unit = (m.group("unit") or "").strip()
        ref_low = float(m.group("ref_low")) if m.group("ref_low") else None
        ref_high = float(m.group("ref_high")) if m.group("ref_high") else None
        flag = m.group("flag")

        if raw_unit:
            # Remove accidental range/status text from unit.
            for word in ["Critical", "Elevated", "Abnormal", "High", "Low", "Normal", "Good"]:
                raw_unit = re.split(rf"\b{word}\b", raw_unit, flags=re.IGNORECASE)[0].strip()

            range_match = _RANGE_RE.search(raw_unit) or _LESS_THAN_RE.search(raw_unit) or _GREATER_THAN_RE.search(raw_unit)
            if range_match:
                ref_low2, ref_high2 = parse_range(raw_unit[range_match.start():])
                ref_low = ref_low if ref_low is not None else ref_low2
                ref_high = ref_high if ref_high is not None else ref_high2
                raw_unit = raw_unit[:range_match.start()].strip()

        return {
            "raw_alias": raw_alias,
            "value": value,
            "raw_unit": raw_unit,
            "flag_str": flag,
            "ref_low": ref_low,
            "ref_high": ref_high,
            "full_match": True,
        }

    return None


# ---------------------------------------------------------------------------
# PDF table-cell parsing
# ---------------------------------------------------------------------------

def is_probable_test_alias(text: str) -> bool:
    canonical, _meta = resolve_test(text)
    return canonical is not None


def extract_cell_table(text: str) -> List[Dict[str, Any]]:
    """
    Handles PDFs where text comes as:
    Hemoglobin
    8.2
    g/dL
    """
    lines = [
        line.strip()
        for line in normalize_text_for_extraction(text).splitlines()
        if line.strip()
    ]

    results = []
    seen = set()
    i = 0

    while i < len(lines):
        alias = lines[i]

        if not is_probable_test_alias(alias):
            i += 1
            continue

        if i + 1 >= len(lines):
            break

        value_match = re.search(_NUM, lines[i + 1])
        if not value_match:
            i += 1
            continue

        value = float(value_match.group(0))
        raw_unit = ""
        ref_low = None
        ref_high = None
        flag_str = None
        cursor = i + 2

        if cursor < len(lines):
            candidate = lines[cursor]
            if not is_probable_test_alias(candidate) and not re.search(_NUM, candidate):
                raw_unit = candidate
                cursor += 1

        if cursor < len(lines):
            candidate = lines[cursor]
            lo, hi = parse_range(candidate)
            if lo is not None or hi is not None:
                ref_low, ref_high = lo, hi
                cursor += 1

        if cursor < len(lines):
            candidate = lines[cursor]
            if candidate.lower() in {"normal", "high", "low", "critical", "elevated", "abnormal", "good"}:
                flag_str = candidate
                cursor += 1

        item = build_result(
            raw_alias=alias,
            value=value,
            raw_unit=raw_unit,
            flag_str=flag_str,
            ref_low=ref_low,
            ref_high=ref_high,
            regex_matched_full_row=True,
        )

        if item:
            key = (item["canonical_name"], item["value"])
            if key not in seen:
                seen.add(key)
                results.append(item)

        i = max(cursor, i + 1)

    return results


# ---------------------------------------------------------------------------
# CSV parsing
# ---------------------------------------------------------------------------

def is_csv_like(text: str) -> bool:
    first = text.strip().splitlines()[0] if text.strip() else ""
    return first.count(",") >= 2 or first.count("\t") >= 2


def extract_csv(text: str) -> List[Dict[str, Any]]:
    delimiter = "\t" if "\t" in text.splitlines()[0] else ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)

    results = []
    seen = set()

    for row in reader:
        lower = {k.lower().strip(): v for k, v in row.items() if k}

        raw_alias = (
            lower.get("test name")
            or lower.get("test")
            or lower.get("parameter")
            or lower.get("investigation")
            or ""
        )

        value_text = (
            lower.get("result")
            or lower.get("value")
            or lower.get("observed value")
            or ""
        )

        raw_unit = lower.get("unit") or lower.get("units") or ""
        flag = lower.get("status") or lower.get("flag") or ""
        range_text = lower.get("normal range") or lower.get("reference range") or lower.get("range") or ""

        value = None
        try:
            value = float(re.search(_NUM, value_text).group(0))
        except Exception:
            continue

        ref_low, ref_high = parse_range(range_text)

        item = build_result(
            raw_alias=raw_alias,
            value=value,
            raw_unit=raw_unit,
            flag_str=flag,
            ref_low=ref_low,
            ref_high=ref_high,
            regex_matched_full_row=True,
        )

        if item:
            key = (item["canonical_name"], item["value"])
            if key not in seen:
                seen.add(key)
                results.append(item)

    return results


# ---------------------------------------------------------------------------
# Result builder
# ---------------------------------------------------------------------------

def build_result(
    raw_alias: str,
    value: float,
    raw_unit: str,
    flag_str: Optional[str] = None,
    ref_low: Optional[float] = None,
    ref_high: Optional[float] = None,
    regex_matched_full_row: bool = False,
) -> Optional[Dict[str, Any]]:
    canonical, meta = resolve_test(raw_alias)

    if not canonical:
        return None

    unit = normalize_unit(raw_unit, canonical)
    value = normalize_value_for_unit(value, unit, canonical)

    fallback = FALLBACK_RANGES.get(canonical)

    # If report has no range, use built-in fallback range.
    range_source = "report"

    if ref_low is None and ref_high is None and fallback:
        ref_low = fallback.get("low")
        ref_high = fallback.get("high")
        range_source = "fallback"

    if not unit and fallback:
        unit = fallback.get("unit", "")

    if flag_str:
        extracted_flag = status_label_to_flag(flag_str)
    else:
        extracted_flag = classify_value(canonical, value, ref_low, ref_high)

    # Even if PDF says normal, numeric value should override when range exists.
    numeric_flag = classify_value(canonical, value, ref_low, ref_high)

    if numeric_flag != "normal":
        final_flag = numeric_flag
    else:
        final_flag = extracted_flag

    try:
        conf = calculate_confidence(
            raw_alias=raw_alias,
            extracted_value=value,
            extracted_unit=unit or None,
            fuzzy_score=None,
            regex_matched_full_row=regex_matched_full_row,
            test_meta=meta,
        )
    except Exception:
        conf = {"confidence": 0.85, "reasons": ["fallback extraction"]}

    confidence = conf.get("confidence", 0.85)
    reasons = conf.get("reasons", [])

    reference_range = None
    if ref_low is not None and ref_high is not None:
        reference_range = f"{ref_low:g} - {ref_high:g} {unit}".strip()
    elif ref_low is not None:
        reference_range = f"> {ref_low:g} {unit}".strip()
    elif ref_high is not None:
        reference_range = f"< {ref_high:g} {unit}".strip()

    return {
        "canonical_name": canonical,
        "loinc": meta.get("loinc", "") if meta else "",
        "category": meta.get("category", guess_category(canonical)) if meta else guess_category(canonical),
        "raw_alias": raw_alias.strip(),
        "value": value,
        "unit": unit,
        "flag": final_flag,
        "reference_low": ref_low,
        "reference_high": ref_high,
        "reference_range": reference_range or "Reference range not available",
        "range_source": range_source,
        "confidence": confidence,
        "reasons": reasons,
    }


# ---------------------------------------------------------------------------
# Main extraction
# ---------------------------------------------------------------------------

def extract_lab_tests(text: str) -> List[Dict[str, Any]]:
    text = normalize_text_for_extraction(text or "")

    if not text.strip():
        return []

    if is_csv_like(text):
        csv_results = extract_csv(text)
        if csv_results:
            return csv_results

    results = []
    seen = set()

    # Normal line-by-line extraction.
    for line in text.splitlines():
        parsed = parse_line(line)

        if not parsed:
            continue

        item = build_result(
            raw_alias=parsed["raw_alias"],
            value=parsed["value"],
            raw_unit=parsed["raw_unit"],
            flag_str=parsed.get("flag_str"),
            ref_low=parsed.get("ref_low"),
            ref_high=parsed.get("ref_high"),
            regex_matched_full_row=parsed.get("full_match", False),
        )

        if item:
            key = (item["canonical_name"], item["value"])
            if key not in seen:
                seen.add(key)
                results.append(item)

    if results:
        return results

    # PDF table-cell fallback.
    cell_results = extract_cell_table(text)

    if cell_results:
        return cell_results

    return []


# ---------------------------------------------------------------------------
# Backward compatibility for classify.py
# ---------------------------------------------------------------------------

def get_canonical_tests():
    out = {}

    for canonical, ranges in FALLBACK_RANGES.items():
        key = canonical.lower().replace(" ", "_").replace("/", "_")
        out[key] = {
            "unit": ranges.get("unit", ""),
            "low": ranges.get("low", 0),
            "high": ranges.get("high", 999999),
            "critical_low": ranges.get("critical_low", ranges.get("low", 0)),
            "critical_high": ranges.get("critical_high", ranges.get("high", 999999)),
        }

    try:
        raw = load_tests()
        for key, meta in raw.items():
            canonical = meta.get("canonical_name", key)
            fallback = FALLBACK_RANGES.get(canonical, {})
            out[key] = {
                "unit": fallback.get("unit", (meta.get("expected_units") or [""])[0]),
                "low": fallback.get("low", meta.get("reference_low", meta.get("min_value", 0))),
                "high": fallback.get("high", meta.get("reference_high", meta.get("max_value", 999999))),
                "critical_low": fallback.get("critical_low", meta.get("critical_low", meta.get("min_value", 0))),
                "critical_high": fallback.get("critical_high", meta.get("critical_high", meta.get("max_value", 999999))),
            }
    except Exception:
        pass

    return out