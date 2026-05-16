"""
pipeline/normalize.py

Text normalization functions for OCR and pathology report pre-processing.

Handles: whitespace, unicode, OCR character confusion, broken separators,
weird punctuation, and unit string standardization.
"""

import re
import unicodedata
from pipeline.test_registry import normalize_unit

# ---------------------------------------------------------------------------
# OCR character substitution map
# Common OCR mis-reads in pathology contexts
# ---------------------------------------------------------------------------

_OCR_CHAR_MAP = {
    # Digit-letter confusion
    "0": "O",    # not applied blindly — used only in letter-context rules below
    "1": "l",
    "8": "B",
    # Common specific OCR errors in pathology labels
    "H8": "Hb",
    "R8C": "RBC",
    "W8C": "WBC",
    "8UN": "BUN",
    "A1T": "ALT",
    "A5T": "AST",
    "C1": "Cl",    # Chloride
    "GL0BULIN": "GLOBULIN",
    "PR0LACTIN": "PROLACTIN",
    "PR0GESTERONE": "PROGESTERONE",
    "TEST0STERONE": "TESTOSTERONE",
    "A1BUMIN": "ALBUMIN",
    "F1BRINOGEN": "FIBRINOGEN",
}

# Regex patterns for common OCR string-level fixes (applied to whole-word matches)
_OCR_WORD_FIXES = [
    # Fix common OCR errors in test name words (case-insensitive)
    (re.compile(r"\bH8\b", re.IGNORECASE), "Hb"),
    (re.compile(r"\bR8C\b", re.IGNORECASE), "RBC"),
    (re.compile(r"\bW8C\b", re.IGNORECASE), "WBC"),
    (re.compile(r"\b8UN\b", re.IGNORECASE), "BUN"),
    (re.compile(r"\bA1T\b", re.IGNORECASE), "ALT"),
    (re.compile(r"\bA5T\b", re.IGNORECASE), "AST"),
    (re.compile(r"\bA1BUMIN\b", re.IGNORECASE), "ALBUMIN"),
    (re.compile(r"\bF1BRINOGEN\b", re.IGNORECASE), "FIBRINOGEN"),
    (re.compile(r"\bPR0LACTIN\b", re.IGNORECASE), "PROLACTIN"),
    (re.compile(r"\bTEST0STERONE\b", re.IGNORECASE), "TESTOSTERONE"),
    (re.compile(r"\bGL0BULIN\b", re.IGNORECASE), "GLOBULIN"),
    # Broken unit separators
    (re.compile(r"\bmg\s+dl\b", re.IGNORECASE), "mg/dL"),
    (re.compile(r"\bgm\s+dl\b", re.IGNORECASE), "g/dL"),
    (re.compile(r"\bg\s+dl\b", re.IGNORECASE), "g/dL"),
    (re.compile(r"\biu\s+l\b", re.IGNORECASE), "IU/L"),
    (re.compile(r"\bu\s+l\b", re.IGNORECASE), "U/L"),
    (re.compile(r"\bmeq\s+l\b", re.IGNORECASE), "mEq/L"),
    (re.compile(r"\bmmol\s+l\b", re.IGNORECASE), "mmol/L"),
    (re.compile(r"\bng\s+ml\b", re.IGNORECASE), "ng/mL"),
    (re.compile(r"\bpg\s+ml\b", re.IGNORECASE), "pg/mL"),
    (re.compile(r"\bmm\s+hr\b", re.IGNORECASE), "mm/hr"),
]

# Separator normalization: various broken or exotic separators -> " : "
_SEPARATOR_PATTERN = re.compile(r"\s*[|]{1,2}\s*|\s{2,}(?=\d)")

# Multiple spaces
_MULTI_SPACE = re.compile(r"[ \t]+")

# Tabs and carriage returns
_TABS_CR = re.compile(r"[\t\r]")

# Lines that are clearly headers or noise (all dashes, equals, page numbers)
_NOISE_LINE = re.compile(r"^[\s\-=_*#.]{3,}$")


# ---------------------------------------------------------------------------
# Public Functions
# ---------------------------------------------------------------------------

def normalize_whitespace(text: str) -> str:
    """
    Collapse multiple spaces/tabs into a single space and strip leading/trailing whitespace.

    Args:
        text (str): Input string.

    Returns:
        str: Text with normalized whitespace.

    Example:
        >>> normalize_whitespace("Hb  :   13.5   g/dL")
        'Hb : 13.5 g/dL'
    """
    text = _TABS_CR.sub(" ", text)
    text = _MULTI_SPACE.sub(" ", text)
    return text.strip()


def normalize_unicode(text: str) -> str:
    """
    Normalize unicode characters to their closest ASCII equivalents.

    Converts unicode fractions, dashes, quotes, and other special characters
    to ASCII-compatible forms. Uses NFKD decomposition.

    Args:
        text (str): Input string (may contain unicode).

    Returns:
        str: ASCII-safe normalized string.

    Example:
        >>> normalize_unicode("Hb\u00a013.5 g/dL")   # non-breaking space
        'Hb 13.5 g/dL'
    """
    # NFKD normalization decomposes ligatures, fullwidth chars, etc.
    text = unicodedata.normalize("NFKD", text)
    # Replace common unicode punctuation explicitly
    replacements = {
        "\u2013": "-",   # en dash
        "\u2014": "-",   # em dash
        "\u2212": "-",   # minus sign
        "\u00b5": "u",   # micro sign -> u (for unit prefixes)
        "\u00b0": " ",   # degree sign
        "\u00b1": "+/-", # plus-minus
        "\u00a0": " ",   # non-breaking space
        "\u2019": "'",   # right single quotation mark
        "\u201c": '"',   # left double quotation mark
        "\u201d": '"',   # right double quotation mark
        "\u2264": "<=",  # ≤
        "\u2265": ">=",  # ≥
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    # Drop any remaining non-ASCII combining characters
    text = "".join(c for c in text if ord(c) < 128 or not unicodedata.combining(c))
    return text


def normalize_ocr_errors(text: str) -> str:
    """
    Apply word-level OCR error corrections to a line of text.

    Fixes common OCR character confusions specific to pathology report labels
    and unit strings (e.g. "H8" -> "Hb", "mg dl" -> "mg/dL").

    Args:
        text (str): A single line or short text segment.

    Returns:
        str: Text with known OCR errors corrected.

    Example:
        >>> normalize_ocr_errors("H8 13.5 gm dl")
        'Hb 13.5 mg/dL'
    """
    for pattern, replacement in _OCR_WORD_FIXES:
        text = pattern.sub(replacement, text)
    return text


def clean_line(line: str) -> str:
    """
    Apply full normalization pipeline to a single report line.

    Order of operations:
        1. normalize_unicode
        2. normalize_ocr_errors
        3. normalize_whitespace

    Args:
        line (str): Raw report line from ingest.

    Returns:
        str: Cleaned, normalized line ready for regex extraction.

    Example:
        >>> clean_line("  H8  :  13.5  gm dl  H  ")
        'Hb : 13.5 mg/dL H'
    """
    line = normalize_unicode(line)
    line = normalize_ocr_errors(line)
    line = normalize_whitespace(line)
    return line


def normalize_report_text(text: str) -> str:
    """
    Normalize an entire pathology report text string.

    Applies full normalization across all lines, removing noise lines
    (headers, separator rows) and blank lines.

    Args:
        text (str): Full raw report text (multiline string).

    Returns:
        str: Cleaned multiline string with normalized lines joined by newlines.

    Example:
        >>> normalize_report_text("---\\nHb : 13.5 g/dL\\n   \\nWBC : 9000 /uL")
        'Hb : 13.5 g/dL\\nWBC : 9000 /uL'
    """
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = clean_line(line)
        if not line:
            continue
        if _NOISE_LINE.match(line):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def standardize_units(unit_str: str) -> str:
    """
    Normalize an extracted unit string to its canonical form.

    Delegates to test_registry.normalize_unit after basic whitespace cleanup.

    Args:
        unit_str (str): Raw unit string from extraction (e.g. "gm/dl", "cells/cumm").

    Returns:
        str: Canonical unit string (e.g. "g/dL", "/uL"), or original if not in map.

    Example:
        >>> standardize_units("gm/dl")
        'g/dL'
        >>> standardize_units("cells/cumm")
        '/uL'
    """
    if not unit_str:
        return unit_str
    unit_str = normalize_whitespace(unit_str)
    return normalize_unit(unit_str)
