# services/regex_extractor.py
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class MatchConfidence(Enum):
    HIGH = 0.9
    MEDIUM = 0.7
    LOW = 0.5

@dataclass
class ExtractedTest:
    raw_text: str
    test_name: Optional[str]
    value: Optional[float]
    unit: Optional[str]
    reference_range: Optional[str]
    flag: Optional[str]  # H, L, N
    confidence: float
    match_pattern: str

class RegexExtractor:
    """Primary extraction engine using regex patterns"""
    
    # Comprehensive patterns for lab test extraction
    PATTERNS = {
        # Standard: TEST NAME VALUE UNIT REF RANGE
        'standard': re.compile(
            r'^([A-Za-z\s\(\)\-]+?)\s+'  # Test name
            r'(\d+(?:\.\d+)?)\s*'        # Value
            r'([A-Za-z\/\%\d\+\-]+)?\s*' # Unit (optional)
            r'([\(\<]?\d+(?:\.\d+)?\s*[\-\–]\s*\d+(?:\.\d+)?[\)\>]?|\d+(?:\.\d+)?[\-\–]\d+(?:\.\d+)?|<[\d\.]+|>[\d\.]+|[\d\.]+\s*[\-\–]\s*[\d\.]*)?'  # Reference range
        ),
        
        # Table-like: TEST | VALUE | UNIT | REF
        'table': re.compile(
            r'([A-Za-z\s\(\)\-]+?)\s*[\|\t]\s*'
            r'(\d+(?:\.\d+)?)\s*[\|\t]\s*'
            r'([A-Za-z\/\%]+)?\s*[\|\t]\s*'
            r'(\d+(?:\.\d+)?\s*[\-\–]\s*\d+(?:\.\d+)?)'
        ),
        
        # With flag: TEST VALUE UNIT FLAG REF
        'with_flag': re.compile(
            r'([A-Za-z\s\(\)\-]+?)\s+'
            r'(\d+(?:\.\d+)?)\s+'
            r'([A-Za-z\/\%]+)?\s+'
            r'([HLN])\s+'
            r'([\(\<]?\d+(?:\.\d+)?\s*[\-\–]\s*\d+(?:\.\d+)?[\)\>]?)'
        ),
        
        # Simple: TEST VALUE UNIT
        'simple': re.compile(
            r'([A-Za-z\s\(\)\-]+?)\s+'
            r'(\d+(?:\.\d+)?)\s+'
            r'([A-Za-z\/\%]+)'
        ),
        
        # With parentheses: TEST (abbr) VALUE UNIT
        'parentheses': re.compile(
            r'([A-Za-z\s]+?)\s*\(([A-Z]+)\)\s+'
            r'(\d+(?:\.\d+)?)\s+'
            r'([A-Za-z\/\%]+)?'
        ),
        
        # Reference range extraction
        'ref_range': re.compile(
            r'(?:ref|reference|normal|range)[:\s]*'
            r'(\d+(?:\.\d+)?\s*[\-\–]\s*\d+(?:\.\d+)?|<[\d\.]+|>[\d\.]+)',
            re.IGNORECASE
        ),
        
        # Unit extraction
        'unit': re.compile(r'([A-Za-z\/\%\+]+)(?:\s|$|,|;)'),
        
        # Value extraction
        'value': re.compile(r'(\d+(?:\.\d+)?)'),
    }
    
    # Common test name patterns that indicate end of test name
    TEST_NAME_ENDINGS = r'(?=\s+\d|$|,|;|\||\t)'
    
    def extract_from_text(self, text: str) -> List[ExtractedTest]:
        """Extract all tests from text using regex patterns"""
        extracted_tests = []
        
        # Try each pattern
        for pattern_name, pattern in self.PATTERNS.items():
            if pattern_name in ['ref_range', 'unit', 'value']:
                continue  # Skip helper patterns
            
            matches = pattern.finditer(text)
            for match in matches:
                test = self._parse_match(match, pattern_name, text)
                if test and test.value is not None:
                    extracted_tests.append(test)
        
        # Deduplicate by test name and value
        extracted_tests = self._deduplicate_tests(extracted_tests)
        
        return extracted_tests
    
    def _parse_match(self, match: re.Match, pattern_name: str, full_text: str) -> Optional[ExtractedTest]:
        """Parse regex match into ExtractedTest object"""
        groups = match.groups()
        
        if len(groups) < 2:
            return None
        
        # Extract components based on pattern
        if pattern_name == 'standard':
            test_name, value_str, unit, ref_range = groups[0], groups[1], groups[2], groups[3] if len(groups) > 3 else None
            flag = None
        elif pattern_name == 'with_flag':
            test_name, value_str, unit, flag, ref_range = groups
        elif pattern_name == 'simple':
            test_name, value_str, unit = groups
            ref_range = None
            flag = None
        elif pattern_name == 'parentheses':
            test_name, abbr, value_str, unit = groups
            test_name = f"{test_name} ({abbr})"
            ref_range = None
            flag = None
        else:
            return None
        
        # Clean test name
        test_name = self._clean_test_name(test_name)
        if not test_name or len(test_name) < 2:
            return None
        
        # Parse value
        try:
            value = float(value_str)
        except (ValueError, TypeError):
            return None
        
        # Clean unit
        unit = self._clean_unit(unit) if unit else None
        
        # Clean reference range
        if ref_range:
            ref_range = self._clean_reference_range(ref_range)
        
        confidence = MatchConfidence.HIGH.value if pattern_name in ['standard', 'with_flag'] else MatchConfidence.MEDIUM.value
        
        return ExtractedTest(
            raw_text=match.group(0),
            test_name=test_name,
            value=value,
            unit=unit,
            reference_range=ref_range,
            flag=flag,
            confidence=confidence,
            match_pattern=pattern_name
        )
    
    def _clean_test_name(self, name: str) -> str:
        """Clean and validate test name"""
        # Remove common artifacts
        name = re.sub(r'[^\w\s\(\)\-/]', ' ', name)
        name = re.sub(r'\s+', ' ', name)
        name = name.strip()
        
        # Ensure it starts with letter
        if name and not name[0].isalpha():
            name = name[1:] if len(name) > 1 else ''
        
        return name
    
    def _clean_unit(self, unit: str) -> str:
        """Clean unit string"""
        unit = re.sub(r'[^\w\/\%\+\-]', '', unit)
        unit = unit.strip()
        return unit if unit else None
    
    def _clean_reference_range(self, ref_range: str) -> str:
        """Clean reference range string"""
        # Remove parentheses and brackets
        ref_range = re.sub(r'[\(\)\[\]\<\>]', '', ref_range)
        # Normalize dash
        ref_range = re.sub(r'[\-\–]', '-', ref_range)
        ref_range = ref_range.strip()
        return ref_range if ref_range else None
    
    def _deduplicate_tests(self, tests: List[ExtractedTest]) -> List[ExtractedTest]:
        """Remove duplicate test extractions"""
        seen = set()
        unique_tests = []
        
        for test in tests:
            key = f"{test.test_name}_{test.value}"
            if key not in seen:
                seen.add(key)
                unique_tests.append(test)
        
        return unique_tests
    
    def post_process_tables(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Handle table-like structures in reports"""
        extracted = []
        
        for line in lines:
            # Check if line looks like a table row
            if '|' in line or '\t' in line:
                parts = re.split(r'[\|\t]+', line)
                if len(parts) >= 3:
                    test = ExtractedTest(
                        raw_text=line,
                        test_name=self._clean_test_name(parts[0]),
                        value=float(parts[1]) if parts[1].replace('.', '').isdigit() else None,
                        unit=self._clean_unit(parts[2]) if len(parts) > 2 else None,
                        reference_range=self._clean_reference_range(parts[3]) if len(parts) > 3 else None,
                        flag=None,
                        confidence=MatchConfidence.MEDIUM.value,
                        match_pattern='table_row'
                    )
                    if test.value is not None:
                        extracted.append(test)
        
        return extracted