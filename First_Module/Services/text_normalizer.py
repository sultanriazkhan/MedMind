# services/text_normalizer.py
import re
import unicodedata
from typing import Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class NormalizationResult:
    original: str
    normalized: str
    cleaned: str
    tokens: list[str]
    ocr_corrections_applied: int

class TextNormalizer:
    """Handles all text normalization before processing"""
    
    # OCR common error patterns
    OCR_PATTERNS = [
        (r'[Oo]', '0'),  # O to 0
        (r'[Zz]', '2'),  # Z to 2
        (r'[Ss]', '5'),  # S to 5
        (r'rn', 'm'),    # rn to m
        (r'vv', 'w'),    # vv to w
    ]
    
    # Patterns to remove
    REMOVE_PATTERNS = [
        (r'[()\[\]{}<>]', ' '),      # brackets to space
        (r'[^\w\s\.\-\/]', ' '),     # remove special chars except . - /
        (r'\s+', ' '),               # multiple spaces to single
        (r'^\s+|\s+$', ''),          # trim
    ]
    
    @classmethod
    def normalize(cls, text: str) -> NormalizationResult:
        """Complete text normalization pipeline"""
        original = text
        
        # Step 1: Unicode normalization
        text = unicodedata.normalize('NFKD', text)
        
        # Step 2: Lowercase
        text = text.lower()
        
        ocr_corrections = 0
        
        # Step 3: OCR corrections
        for pattern, replacement in cls.OCR_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                ocr_corrections += len(matches)
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Step 4: Remove extra patterns
        for pattern, replacement in cls.REMOVE_PATTERNS:
            text = re.sub(pattern, replacement, text)
        
        # Step 5: Tokenize
        tokens = text.split()
        
        cleaned = text
        
        return NormalizationResult(
            original=original,
            normalized=text,
            cleaned=cleaned,
            tokens=tokens,
            ocr_corrections_applied=ocr_corrections
        )
    
    @classmethod
    def normalize_for_matching(cls, text: str) -> str:
        """Lightweight normalization for matching"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @classmethod
    def extract_numeric_value(cls, text: str) -> Tuple[float, str]:
        """Extract numeric value and remaining text"""
        # Pattern for numbers with decimals
        pattern = r'(\d+(?:\.\d+)?)\s*([^\d\s]*)'
        match = re.search(pattern, text)
        if match:
            value = float(match.group(1))
            unit = match.group(2).strip()
            remaining = text[:match.start()] + text[match.end():]
            return value, unit, remaining
        return None, text, text

class OCRCleanup:
    """Specialized OCR noise removal"""
    
    # Common OCR artifacts
    ARTIFACTS = [
        (r'(?m)^[\W_]+', ''),  # Leading noise
        (r'[\W_]+$', ''),      # Trailing noise
        (r'\|+', 'I'),         # Pipe to I
        (r'\+', '+'),          # Keep plus signs
        (r'\$', 'S'),          # Dollar to S
    ]
    
    @classmethod
    def clean(cls, text: str) -> str:
        """Remove OCR artifacts"""
        for pattern, replacement in cls.ARTIFACTS:
            text = re.sub(pattern, replacement, text)
        
        # Remove repeated characters that might be OCR errors
        text = re.sub(r'(.)\1{4,}', r'\1\1', text)
        
        return text.strip()