# services/range_classifier.py
from typing import Optional, Dict, Any, Tuple
from enum import Enum
from datetime import datetime
from dateutil.relativedelta import relativedelta

from models.database import db_manager
from models.orm_models import ReferenceRange, CriticalThreshold

class ResultStatus(str, Enum):
    NORMAL = "Normal"
    LOW = "Low"
    HIGH = "High"
    CRITICAL_LOW = "Critical Low"
    CRITICAL_HIGH = "Critical High"
    OUT_OF_RANGE = "Out of Range"
    UNKNOWN = "Unknown"

class RangeClassifier:
    """Classifies lab results based on reference ranges and thresholds"""
    
    def classify(self, canonical_test_id: int, value: float, unit: str,
                gender: Optional[str] = None, age_years: Optional[float] = None) -> ResultStatus:
        """
        Classify result value against reference ranges
        
        Priority:
        1. Critical thresholds (low/high)
        2. Reference ranges (age/gender specific)
        3. Default reference range
        """
        with db_manager.get_session() as session:
            # Step 1: Check critical thresholds
            critical = session.query(CriticalThreshold).filter(
                CriticalThreshold.canonical_test_id == canonical_test_id
            ).first()
            
            if critical:
                if critical.critical_low and value <= critical.critical_low:
                    return ResultStatus.CRITICAL_LOW
                if critical.critical_high and value >= critical.critical_high:
                    return ResultStatus.CRITICAL_HIGH
            
            # Step 2: Find appropriate reference range
            reference = self._find_reference_range(session, canonical_test_id, unit, gender, age_years)
            
            if not reference:
                return ResultStatus.UNKNOWN
            
            # Step 3: Classify against reference range
            if reference.lower_bound and reference.upper_bound:
                if value < reference.lower_bound:
                    return ResultStatus.LOW
                elif value > reference.upper_bound:
                    return ResultStatus.HIGH
                else:
                    return ResultStatus.NORMAL
            elif reference.lower_bound:
                if value < reference.lower_bound:
                    return ResultStatus.LOW
                else:
                    return ResultStatus.NORMAL
            elif reference.upper_bound:
                if value > reference.upper_bound:
                    return ResultStatus.HIGH
                else:
                    return ResultStatus.NORMAL
            
            return ResultStatus.UNKNOWN
    
    def _find_reference_range(self, session, canonical_test_id: int, unit: str,
                              gender: Optional[str] = None, age_years: Optional[float] = None):
        """Find the most specific matching reference range"""
        
        # Convert age to days for comparison
        age_days = int(age_years * 365) if age_years else None
        
        # Priority order: gender+age > gender > age > default
        query = session.query(ReferenceRange).filter(
            ReferenceRange.canonical_test_id == canonical_test_id
        )
        
        # Try to find best match
        candidates = []
        
        for ref_range in query.all():
            # Check unit (allow None/empty for any unit)
            if ref_range.unit and ref_range.unit != unit and unit:
                continue
            
            # Check gender
            if ref_range.gender and gender:
                if ref_range.gender != gender:
                    continue
            
            # Check age
            if age_days:
                min_age = ref_range.min_age_days or -float('inf')
                max_age = ref_range.max_age_days or float('inf')
                if not (min_age <= age_days <= max_age):
                    continue
            
            # Score this match
            score = 0
            if ref_range.gender:
                score += 2
            if ref_range.min_age_days is not None or ref_range.max_age_days is not None:
                score += 1
            if ref_range.unit:
                score += 1
            
            candidates.append((score, ref_range))
        
        # Return highest scoring match
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1]
        
        return None