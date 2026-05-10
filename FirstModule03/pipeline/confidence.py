"""
pipeline/confidence.py

Confidence scoring system for Med-Mind pathology extraction results.

Produces a normalized confidence score (0.0 - 1.0) and a list of human-readable
reasons by evaluating five independent factors:
  1. Alias match quality (exact vs fuzzy)
  2. Fuzzy match score (RapidFuzz)
  3. Unit validity
  4. Medical plausibility (value within range)
  5. Regex extraction quality

All weights are configurable at module level.
"""

from typing import Optional

from pipeline.validators import validate_value, validate_unit, detect_suspicious_result
from pipeline.test_registry import get_test_by_alias, normalize_unit


# ---------------------------------------------------------------------------
# Scoring weights (must sum to 1.0)
# ---------------------------------------------------------------------------

WEIGHT_ALIAS_MATCH   = 0.30   # How well the alias was resolved
WEIGHT_FUZZY_SCORE   = 0.20   # RapidFuzz match quality
WEIGHT_UNIT_VALID    = 0.20   # Unit is among expected units
WEIGHT_PLAUSIBILITY  = 0.20   # Value is within medical range and not suspicious
WEIGHT_REGEX_QUALITY = 0.10   # Quality of the regex extraction


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def calculate_confidence(
    raw_alias: str,
    extracted_value,
    extracted_unit: Optional[str] = None,
    fuzzy_score: Optional[float] = None,
    regex_matched_full_row: bool = False,
    test_meta: Optional[dict] = None,
) -> dict:
    """
    Calculate a composite confidence score for a single extracted pathology result.

    Args:
        raw_alias (str):
            The raw test name string as extracted from the report line
            (e.g. "Hemogiobin", "hb", "WBC count").

        extracted_value:
            The numeric value extracted from the report (int, float, or str).
            Non-numeric values will reduce the plausibility score.

        extracted_unit (str, optional):
            The unit string extracted from the report (e.g. "g/dL", "gm/dl").
            If None, unit validity score will be 0.

        fuzzy_score (float, optional):
            The RapidFuzz score (0-100) used to resolve the alias, if a fuzzy
            match was performed. Pass None for exact matches (will be scored as
            100). Pass 0 if no fuzzy match was attempted.

        regex_matched_full_row (bool):
            True if the PATHOLOGY_ROW_PATTERN matched the full row (higher quality).
            False if only TEST_VALUE_PATTERN or partial extraction was used.

        test_meta (dict, optional):
            Pre-resolved test metadata dict from test_registry.get_test_by_alias().
            If None, this function will attempt to resolve it from raw_alias.

    Returns:
        dict: Confidence result with keys:
            - "confidence" (float): Normalized score in [0.0, 1.0].
            - "reasons" (list[str]): Human-readable explanation of score factors.

    Example:
        >>> result = calculate_confidence(
        ...     raw_alias="hb",
        ...     extracted_value=13.5,
        ...     extracted_unit="g/dL",
        ...     fuzzy_score=None,
        ...     regex_matched_full_row=True,
        ... )
        >>> result
        {
            'confidence': 0.98,
            'reasons': [
                'exact alias match',
                'valid unit',
                'value within range',
                'full-row regex match'
            ]
        }
    """
    reasons = []
    score_components = {}

    # ------------------------------------------------------------------
    # 1. Alias match quality
    # ------------------------------------------------------------------
    if test_meta is None:
        test_meta = get_test_by_alias(raw_alias)

    if test_meta is None:
        # Complete miss — no test resolved
        alias_score = 0.0
        reasons.append("alias not resolved")
        # Short-circuit: if we can't identify the test, confidence is very low
        return {
            "confidence": round(alias_score, 4),
            "reasons": reasons,
        }

    canonical = test_meta.get("canonical_name", "unknown")
    aliases_lower = [a.lower() for a in test_meta.get("aliases", [])]
    canonical_lower = canonical.lower()
    raw_lower = raw_alias.strip().lower()

    if raw_lower == canonical_lower or raw_lower in aliases_lower:
        alias_score = 1.0
        reasons.append("exact alias match")
    elif fuzzy_score is not None and fuzzy_score >= 85:
        # Normalize fuzzy_score from [85, 100] → [0.5, 1.0]
        alias_score = 0.5 + (fuzzy_score - 85) / 30.0
        alias_score = min(alias_score, 1.0)
        reasons.append(f"fuzzy alias match (score={fuzzy_score:.0f})")
    else:
        alias_score = 0.3
        reasons.append("weak alias resolution")

    score_components["alias"] = alias_score * WEIGHT_ALIAS_MATCH

    # ------------------------------------------------------------------
    # 2. Fuzzy score component
    # ------------------------------------------------------------------
    if fuzzy_score is None:
        # Exact match — treat as perfect
        fuzz_component = 1.0
    elif fuzzy_score >= 95:
        fuzz_component = 1.0
    elif fuzzy_score >= 85:
        fuzz_component = 0.75 + (fuzzy_score - 85) / 40.0
    else:
        fuzz_component = fuzzy_score / 100.0

    score_components["fuzzy"] = fuzz_component * WEIGHT_FUZZY_SCORE

    # ------------------------------------------------------------------
    # 3. Unit validity
    # ------------------------------------------------------------------
    norm_unit = normalize_unit(extracted_unit) if extracted_unit else None

    if norm_unit:
        unit_valid, unit_reason = validate_unit(norm_unit, canonical)
        if unit_valid:
            unit_score = 1.0
            reasons.append("valid unit")
        else:
            unit_score = 0.2
            reasons.append(f"invalid unit: {unit_reason}")
    else:
        expected_units = test_meta.get("expected_units", [])
        if not expected_units:
            # Qualitative test — unit not required
            unit_score = 1.0
            reasons.append("qualitative test; unit not required")
        else:
            unit_score = 0.0
            reasons.append("unit missing")

    score_components["unit"] = unit_score * WEIGHT_UNIT_VALID

    # ------------------------------------------------------------------
    # 4. Medical plausibility
    # ------------------------------------------------------------------
    val_valid, val_reason = validate_value(extracted_value, canonical)
    sus_valid, sus_reason = detect_suspicious_result(extracted_value, canonical, norm_unit)

    if val_valid and sus_valid:
        plaus_score = 1.0
        reasons.append("value within range")
    elif val_valid and not sus_valid:
        plaus_score = 0.5
        reasons.append(f"suspicious result: {sus_reason}")
    else:
        plaus_score = 0.0
        reasons.append(f"implausible value: {val_reason}")

    score_components["plausibility"] = plaus_score * WEIGHT_PLAUSIBILITY

    # ------------------------------------------------------------------
    # 5. Regex extraction quality
    # ------------------------------------------------------------------
    if regex_matched_full_row:
        regex_score = 1.0
        reasons.append("full-row regex match")
    else:
        regex_score = 0.5
        reasons.append("partial regex match")

    score_components["regex"] = regex_score * WEIGHT_REGEX_QUALITY

    # ------------------------------------------------------------------
    # Final composite score
    # ------------------------------------------------------------------
    total = sum(score_components.values())
    total = max(0.0, min(1.0, total))  # clamp to [0, 1]

    return {
        "confidence": round(total, 4),
        "reasons": reasons,
    }
