# services/unit_normalizer.py
from typing import Optional, Tuple, Dict
import re

class UnitNormalizer:
    """Handles unit normalization and conversion"""
    
    # Unit conversion factors to SI units
    CONVERSIONS: Dict[str, Dict[str, float]] = {
        'hemoglobin': {
            'g/dL': 1.0,
            'mg/dL': 0.01,
            'g/L': 0.1,
            'mmol/L': 1.611  # Conversion factor for hemoglobin
        },
        'glucose': {
            'mg/dL': 1.0,
            'mmol/L': 0.0555
        },
        'creatinine': {
            'mg/dL': 1.0,
            'μmol/L': 88.4,
            'umol/L': 88.4
        }
    }
    
    # Standard unit mappings
    UNIT_SYNONYMS = {
        'mg/dl': 'mg/dL',
        'mg per dl': 'mg/dL',
        'g/dl': 'g/dL',
        'grams per deciliter': 'g/dL',
        'mmol/l': 'mmol/L',
        'umol/l': 'μmol/L',
        'mcg/dl': 'μg/dL',
        'ng/ml': 'ng/mL',
        'pg/ml': 'pg/mL'
    }
    
    @classmethod
    def normalize(cls, unit: Optional[str]) -> Optional[str]:
        """Normalize unit string to standard form"""
        if not unit:
            return None
        
        # Clean
        unit = unit.strip().lower()
        unit = re.sub(r'\s+', '', unit)
        unit = re.sub(r'per', '/', unit)
        
        # Look up synonym
        if unit in cls.UNIT_SYNONYMS:
            return cls.UNIT_SYNONYMS[unit]
        
        # Capitalize correctly
        if '/' in unit:
            parts = unit.split('/')
            parts = [p.capitalize() if p.isalpha() else p for p in parts]
            unit = '/'.join(parts)
        else:
            unit = unit.capitalize()
        
        return unit
    
    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str, test_name: str) -> Tuple[float, str]:
        """Convert value between units for a specific test"""
        # Normalize units
        from_unit = cls.normalize(from_unit)
        to_unit = cls.normalize(to_unit)
        
        if from_unit == to_unit:
            return value, to_unit
        
        # Find conversion factor
        test_key = cls._get_test_key(test_name)
        if test_key in cls.CONVERSIONS:
            conv = cls.CONVERSIONS[test_key]
            if from_unit in conv and to_unit in conv:
                # Convert via SI base
                value_in_si = value / conv[from_unit]
                converted = value_in_si * conv[to_unit]
                return round(converted, 2), to_unit
        
        return value, from_unit  # Return original if conversion not possible
    
    @staticmethod
    def _get_test_key(test_name: str) -> str:
        """Get normalized test key for conversion lookup"""
        test_name = test_name.lower()
        for key in UnitNormalizer.CONVERSIONS:
            if key in test_name:
                return key
        return test_name