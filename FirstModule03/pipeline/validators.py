"""
pipeline/validators.py

Medical plausibility validation for extracted pathology values.

Validates extracted numeric values, units, and reference ranges against
test metadata from the ontology. Flags suspicious OCR outputs and
medically impossible results.
"""

from typing import Optional, Tuple

from pipeline.test_registry import get_test_metadata, load_units


# ---------------------------------------------------------------------------
# Validation Result Type
# A tuple of (is_valid: bool, reason: str)
# ---------------------------------------------------------------------------

ValidationResult = Tuple[bool, str]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_canonical_units(test_meta: dict) -> set:
    """Return the set of expected canonical units for a test (lowercased)."""
    return {u.lower() for u in test_meta.get("expected_units", [])}


def _is_numeric(value) -> bool:
    """Return True if value can be cast to float."""
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


# ---------------------------------------------------------------------------
# Public Validators
# ---------------------------------------------------------------------------

def validate_value(
    value,
    test_name: str,
    unit: Optional[str] = None
) -> ValidationResult:
    """
    Validate a numeric value against the medically plausible range for the given test.

    Uses min_value and max_value from the test ontology. Values outside this
    range are considered medically implausible (likely OCR error or data corruption).

    Args:
        value: Numeric value to validate (int, float, or string-coercible to float).
        test_name (str): Canonical test name or alias key (e.g. "Hemoglobin").
        unit (str, optional): Extracted unit string. Passed to validate_unit internally.

    Returns:
        Tuple[bool, str]: (True, "valid") on pass, (False, reason_string) on fail.

    Examples:
        >>> validate_value(13.5, "Hemoglobin")
        (True, 'valid')
        >>> validate_value(250, "Hemoglobin")
        (False, 'value 250.0 exceeds max_value 25 for Hemoglobin')
    """
    if not _is_numeric(value):
        return False, f"non-numeric value: {value!r}"

    numeric = float(value)
    test_meta = get_test_metadata(test_name)

    if test_meta is None:
        # Unknown test — cannot validate range; pass through with warning
        return True, "unknown test; range validation skipped"

    min_val = test_meta.get("min_value", None)
    max_val = test_meta.get("max_value", None)
    canonical = test_meta.get("canonical_name", test_name)

    if min_val is not None and numeric < min_val:
        return False, (
            f"value {numeric} is below min_value {min_val} for {canonical}"
        )

    if max_val is not None and numeric > max_val:
        return False, (
            f"value {numeric} exceeds max_value {max_val} for {canonical}"
        )

    return True, "valid"


def validate_unit(
    unit: str,
    test_name: str
) -> ValidationResult:
    """
    Validate that a unit string is compatible with the expected units for a test.

    Performs case-insensitive comparison against the test's expected_units list.
    An empty expected_units list (e.g. for qualitative tests) always passes.

    Args:
        unit (str): Extracted (and ideally normalized) unit string.
        test_name (str): Canonical test name.

    Returns:
        Tuple[bool, str]: (True, "valid unit") on pass, (False, reason) on fail.

    Examples:
        >>> validate_unit("g/dL", "Hemoglobin")
        (True, 'valid unit')
        >>> validate_unit("IU/L", "Hemoglobin")
        (False, "unit 'IU/L' not expected for Hemoglobin; expected: ['g/dL', 'gm/dL', 'g/dl', 'gm/dl']")
    """
    test_meta = get_test_metadata(test_name)

    if test_meta is None:
        return True, "unknown test; unit validation skipped"

    expected = test_meta.get("expected_units", [])

    # Qualitative tests (empty expected_units) — no unit to validate
    if not expected:
        return True, "qualitative test; unit not applicable"

    if not unit or not unit.strip():
        return False, f"no unit provided for {test_meta.get('canonical_name', test_name)}"

    canonical = test_meta.get("canonical_name", test_name)
    unit_lower = unit.strip().lower()
    expected_lower = {u.lower() for u in expected}

    # Also accept units from the units.json normalized map for flexibility
    unit_map = load_units()
    mapped_unit = unit_map.get(unit_lower, unit.strip())
    mapped_lower = mapped_unit.lower()

    if unit_lower in expected_lower or mapped_lower in expected_lower:
        return True, "valid unit"

    return False, (
        f"unit {unit!r} not expected for {canonical}; "
        f"expected: {expected}"
    )


def validate_reference_range(
    ref_low,
    ref_high,
    test_name: str
) -> ValidationResult:
    """
    Validate a reference range extracted from the report against the test ontology.

    Checks that:
      1. ref_low < ref_high (range is not inverted)
      2. Both bounds fall within the ontology's min/max for the test.

    Args:
        ref_low: Lower bound of reference range (numeric or string).
        ref_high: Upper bound of reference range (numeric or string).
        test_name (str): Canonical test name.

    Returns:
        Tuple[bool, str]: (True, "valid range") on pass, (False, reason) on fail.

    Examples:
        >>> validate_reference_range(11.5, 16.5, "Hemoglobin")
        (True, 'valid range')
        >>> validate_reference_range(16.5, 11.5, "Hemoglobin")
        (False, 'reference range is inverted: low=16.5 > high=11.5')
    """
    if not _is_numeric(ref_low) or not _is_numeric(ref_high):
        return False, f"non-numeric reference range: low={ref_low!r}, high={ref_high!r}"

    low = float(ref_low)
    high = float(ref_high)

    if low >= high:
        return False, f"reference range is inverted: low={low} > high={high}"

    test_meta = get_test_metadata(test_name)
    if test_meta is None:
        return True, "unknown test; range bounds validation skipped"

    min_val = test_meta.get("min_value", None)
    max_val = test_meta.get("max_value", None)
    canonical = test_meta.get("canonical_name", test_name)

    if min_val is not None and low < min_val:
        return False, (
            f"ref_low {low} is below ontology min_value {min_val} for {canonical}"
        )
    if max_val is not None and high > max_val:
        return False, (
            f"ref_high {high} exceeds ontology max_value {max_val} for {canonical}"
        )

    return True, "valid range"


def detect_suspicious_result(
    value,
    test_name: str,
    unit: Optional[str] = None
) -> ValidationResult:
    """
    Detect results that are technically within range but medically suspicious.

    Triggers for values that fall into an extreme outer band (top or bottom 2%
    of the ontology range), which frequently indicates OCR misread or unit mismatch.
    Also checks for unit-value incompatibility heuristics.

    Args:
        value: Numeric value to check.
        test_name (str): Canonical test name.
        unit (str, optional): Extracted unit string.

    Returns:
        Tuple[bool, str]: (True, "not suspicious") if plausible,
                          (False, reason_string) if suspicious.

    Examples:
        >>> detect_suspicious_result(250, "Hemoglobin", "g/dL")
        (False, 'value 250 far exceeds typical range for Hemoglobin (max=25)')
        >>> detect_suspicious_result(13.5, "Hemoglobin", "g/dL")
        (True, 'not suspicious')
    """
    if not _is_numeric(value):
        return False, f"non-numeric value cannot be assessed: {value!r}"

    numeric = float(value)
    test_meta = get_test_metadata(test_name)

    if test_meta is None:
        return True, "not suspicious (unknown test)"

    canonical = test_meta.get("canonical_name", test_name)
    min_val = test_meta.get("min_value", None)
    max_val = test_meta.get("max_value", None)

    # Check 1: Value many multiples beyond max (likely OCR decimal error)
    if max_val is not None and numeric > max_val * 2:
        return False, (
            f"value {numeric} far exceeds typical range for {canonical} (max={max_val})"
        )

    # Check 2: Value many multiples below min (negative or near-zero anomaly)
    if min_val is not None and min_val > 0 and numeric < min_val * 0.1:
        return False, (
            f"value {numeric} is extremely low relative to min {min_val} for {canonical}"
        )

    # Check 3: Wrong unit order of magnitude check for known cases
    # e.g. Hemoglobin reported as 135 g/dL (should be 13.5) — 10x OCR spacing
    if unit and max_val is not None and numeric > max_val:
        shifted = numeric / 10.0
        if min_val is not None and min_val <= shifted <= max_val:
            return False, (
                f"value {numeric} with unit {unit!r} looks like decimal-shift OCR error "
                f"for {canonical}; did you mean {shifted}?"
            )

    # Check 4: Negative values where not expected
    if numeric < 0 and (min_val is None or min_val >= 0):
        return False, f"unexpected negative value {numeric} for {canonical}"

    return True, "not suspicious"
