"""
pipeline/test_registry.py

Central ontology loader and alias resolver for the Med-Mind pathology extraction engine.
Loads test definitions and unit normalization maps, and provides fuzzy + exact alias resolution.
"""

import json
import os
from functools import lru_cache
from typing import Optional

from rapidfuzz import process, fuzz

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TESTS_PATH = os.path.join(_BASE_DIR, "data", "tests.json")
_UNITS_PATH = os.path.join(_BASE_DIR, "data", "units.json")

FUZZY_THRESHOLD = 85  # Minimum score for fuzzy alias matching (0-100)


# ---------------------------------------------------------------------------
# Data Loaders
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_tests() -> dict:
    """
    Load and return the full pathology test ontology from data/tests.json.

    Returns:
        dict: Mapping of snake_case test key -> test metadata dict.

    Raises:
        FileNotFoundError: If tests.json is not found at expected path.
        ValueError: If the JSON is malformed.
    """
    if not os.path.exists(_TESTS_PATH):
        raise FileNotFoundError(f"tests.json not found at: {_TESTS_PATH}")
    try:
        with open(_TESTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed tests.json: {e}")


@lru_cache(maxsize=1)
def load_units() -> dict:
    """
    Load and return the unit normalization dictionary from data/units.json.

    Returns:
        dict: Mapping of raw unit string (lowercase) -> canonical unit string.

    Raises:
        FileNotFoundError: If units.json is not found at expected path.
        ValueError: If the JSON is malformed.
    """
    if not os.path.exists(_UNITS_PATH):
        raise FileNotFoundError(f"units.json not found at: {_UNITS_PATH}")
    try:
        with open(_UNITS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed units.json: {e}")


# ---------------------------------------------------------------------------
# Alias Index Builder
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _build_alias_index() -> dict:
    """
    Build a flat alias -> canonical_name lookup index from all tests.

    Returns:
        dict: Mapping of lowercased alias string -> test dict (canonical object).
    """
    tests = load_tests()
    index = {}
    for _key, test in tests.items():
        canonical = test["canonical_name"].lower()
        index[canonical] = test
        for alias in test.get("aliases", []):
            alias_lower = alias.strip().lower()
            if alias_lower:
                index[alias_lower] = test
    return index


@lru_cache(maxsize=1)
def get_all_aliases() -> list:
    """
    Return a list of all known alias strings (lowercased) across all tests.

    Returns:
        list[str]: All alias strings registered in the ontology.
    """
    return list(_build_alias_index().keys())


# ---------------------------------------------------------------------------
# Public Lookup Functions
# ---------------------------------------------------------------------------

def get_test_by_alias(alias: str) -> Optional[dict]:
    """
    Resolve a raw alias string to its canonical test object.

    Resolution strategy:
      1. Exact match (case-insensitive) against the alias index.
      2. Fuzzy match using RapidFuzz token_sort_ratio with a threshold of 85.

    Args:
        alias (str): Raw alias text extracted from a pathology report line.

    Returns:
        dict or None: The canonical test metadata dict, or None if no match found.

    Example:
        >>> get_test_by_alias("Hemogiobin")
        {'canonical_name': 'Hemoglobin', 'aliases': [...], 'loinc': '718-7', ...}
    """
    if not alias or not alias.strip():
        return None

    alias_clean = alias.strip().lower()
    index = _build_alias_index()

    # 1. Exact match
    if alias_clean in index:
        return index[alias_clean]

    # 2. Fuzzy match
    all_aliases = get_all_aliases()
    result = process.extractOne(
        alias_clean,
        all_aliases,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=FUZZY_THRESHOLD
    )
    if result:
        matched_alias, score, _idx = result
        return index.get(matched_alias)

    return None


def get_test_metadata(test_name: str) -> Optional[dict]:
    """
    Retrieve a test's full metadata dict by its canonical name or primary key.

    Performs case-insensitive lookup against canonical_name fields.

    Args:
        test_name (str): Canonical name or storage key (e.g. "Hemoglobin" or "hemoglobin").

    Returns:
        dict or None: Full test metadata dict, or None if not found.

    Example:
        >>> get_test_metadata("Hemoglobin")
        {'canonical_name': 'Hemoglobin', 'loinc': '718-7', ...}
    """
    if not test_name or not test_name.strip():
        return None

    tests = load_tests()
    name_lower = test_name.strip().lower()

    # Match by storage key
    if name_lower in tests:
        return tests[name_lower]

    # Match by canonical_name field (case-insensitive)
    for _key, test in tests.items():
        if test.get("canonical_name", "").lower() == name_lower:
            return test

    return None


def normalize_unit(unit: str) -> str:
    """
    Normalize a raw unit string to its canonical form using the units dictionary.

    Performs a case-insensitive lookup. Falls back to the original stripped string
    if no normalization mapping is found.

    Args:
        unit (str): Raw unit string from OCR or report text (e.g. "gm/dl", "cells/cumm").

    Returns:
        str: Canonical unit string (e.g. "g/dL", "/uL"), or original if not mapped.

    Example:
        >>> normalize_unit("gm/dl")
        'g/dL'
        >>> normalize_unit("cells/cumm")
        '/uL'
    """
    if not unit:
        return unit

    unit_map = load_units()
    unit_clean = unit.strip().lower()
    return unit_map.get(unit_clean, unit.strip())
