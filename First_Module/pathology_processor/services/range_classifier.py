# services/range_classifier.py
from typing import Optional, Dict, Any, Tuple, List, Union, cast
from enum import Enum
from datetime import datetime
import logging

from models.database import db_manager
from models.orm_models import ReferenceRange, CriticalThreshold

logger = logging.getLogger(__name__)

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
    
    def classify(
        self, 
        canonical_test_id: int, 
        value: float, 
        unit: Optional[str] = None,
        gender: Optional[str] = None, 
        age_years: Optional[float] = None
    ) -> ResultStatus:
        """
        Classify result value against reference ranges
        
        Priority:
        1. Critical thresholds (low/high)
        2. Reference ranges (age/gender specific)
        3. Default reference range
        
        Args:
            canonical_test_id: ID of the canonical test
            value: Numeric value to classify
            unit: Unit of measurement (can be None)
            gender: Patient gender ('M', 'F', or None)
            age_years: Patient age in years (optional)
        """
        with db_manager.get_session() as session:
            # Step 1: Check critical thresholds
            critical = session.query(CriticalThreshold).filter(
                CriticalThreshold.canonical_test_id == canonical_test_id
            ).first()
            
            if critical:
                # Cast to proper types - at runtime these are actual values, not Column objects
                critical_low = cast(Optional[float], critical.critical_low)
                critical_high = cast(Optional[float], critical.critical_high)
                
                # Check critical low (if defined)
                if critical_low is not None and value <= critical_low:
                    return ResultStatus.CRITICAL_LOW
                
                # Check critical high (if defined)
                if critical_high is not None and value >= critical_high:
                    return ResultStatus.CRITICAL_HIGH
            
            # Step 2: Find appropriate reference range
            reference = self._find_reference_range(
                session, canonical_test_id, unit, gender, age_years
            )
            
            if not reference:
                return ResultStatus.UNKNOWN
            
            # Step 3: Classify against reference range
            # Cast to proper types - at runtime these are actual values
            lower_bound = cast(Optional[float], reference.lower_bound)
            upper_bound = cast(Optional[float], reference.upper_bound)
            
            # Case 1: Both bounds defined
            if lower_bound is not None and upper_bound is not None:
                if value < lower_bound:
                    return ResultStatus.LOW
                elif value > upper_bound:
                    return ResultStatus.HIGH
                else:
                    return ResultStatus.NORMAL
            
            # Case 2: Only lower bound defined
            elif lower_bound is not None:
                if value < lower_bound:
                    return ResultStatus.LOW
                else:
                    return ResultStatus.NORMAL
            
            # Case 3: Only upper bound defined
            elif upper_bound is not None:
                if value > upper_bound:
                    return ResultStatus.HIGH
                else:
                    return ResultStatus.NORMAL
            
            # Case 4: No bounds defined
            return ResultStatus.UNKNOWN
    
    def _find_reference_range(
        self, 
        session, 
        canonical_test_id: int, 
        unit: Optional[str], 
        gender: Optional[str], 
        age_years: Optional[float]
    ) -> Optional[ReferenceRange]:
        """Find the most specific matching reference range"""
        
        # Convert age to days for comparison (if provided)
        age_days: Optional[int] = None
        if age_years is not None:
            age_days = int(age_years * 365)
        
        # Get all reference ranges for this test
        query = session.query(ReferenceRange).filter(
            ReferenceRange.canonical_test_id == canonical_test_id
        )
        
        # Collect candidates with scores
        candidates: List[Tuple[int, ReferenceRange]] = []
        
        for ref_range in query.all():
            # Cast to proper types
            ref_unit = cast(Optional[str], ref_range.unit)
            ref_gender = cast(Optional[str], ref_range.gender)
            ref_min_age = cast(Optional[int], ref_range.min_age_days)
            ref_max_age = cast(Optional[int], ref_range.max_age_days)
            
            # Check unit (allow None/empty for any unit)
            if ref_unit and unit and ref_unit != unit:
                continue
            
            # Check gender
            if ref_gender and gender and ref_gender != gender:
                continue
            
            # Check age (if age_days is provided)
            if age_days is not None:
                min_age = ref_min_age if ref_min_age is not None else -float('inf')
                max_age = ref_max_age if ref_max_age is not None else float('inf')
                if not (min_age <= age_days <= max_age):
                    continue
            
            # Calculate score for this match (higher is better)
            score = 0
            if ref_gender:
                score += 2
            if ref_min_age is not None or ref_max_age is not None:
                score += 1
            if ref_unit:
                score += 1
            
            candidates.append((score, ref_range))
        
        # Return highest scoring match
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1]
        
        return None
    
    def classify_batch(
        self, 
        tests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Classify multiple tests in batch
        
        Args:
            tests: List of test dictionaries with keys:
                - canonical_test_id (int)
                - value (float)
                - unit (str, optional)
                - gender (str, optional)
                - age_years (float, optional)
        
        Returns:
            List of tests with 'status' field added
        """
        classified_tests: List[Dict[str, Any]] = []
        
        for test in tests:
            # Create a copy to avoid modifying original
            classified_test = test.copy()
            
            # Safely extract values
            canonical_test_id = test.get('canonical_test_id')
            value = test.get('value')
            unit = test.get('unit')
            gender = test.get('gender')
            age_years = test.get('age_years')
            
            # Validate required fields
            if canonical_test_id is not None and value is not None:
                try:
                    # Ensure correct types
                    test_id_int = int(canonical_test_id) if not isinstance(canonical_test_id, int) else canonical_test_id
                    value_float = float(value) if not isinstance(value, float) else value
                    
                    # Get unit as string or None
                    unit_str = str(unit) if unit is not None else None
                    
                    # Get gender as string or None
                    gender_str = str(gender) if gender is not None else None
                    
                    # Get age as float or None
                    age_float = float(age_years) if age_years is not None else None
                    
                    # Classify
                    status = self.classify(
                        canonical_test_id=test_id_int,
                        value=value_float,
                        unit=unit_str,
                        gender=gender_str,
                        age_years=age_float
                    )
                    classified_test['status'] = status.value
                    
                except (ValueError, TypeError) as e:
                    logger.warning(f"Failed to classify test {test.get('test_name', 'unknown')}: {e}")
                    classified_test['status'] = ResultStatus.UNKNOWN.value
            else:
                classified_test['status'] = ResultStatus.UNKNOWN.value
            
            classified_tests.append(classified_test)
        
        return classified_tests
    
    def is_within_normal_range(
        self,
        canonical_test_id: int,
        value: float,
        unit: Optional[str] = None,
        gender: Optional[str] = None,
        age_years: Optional[float] = None
    ) -> bool:
        """
        Check if a value is within normal range
        
        Returns:
            True if normal, False otherwise (including unknown)
        """
        status = self.classify(canonical_test_id, value, unit, gender, age_years)
        return status == ResultStatus.NORMAL
    
    def get_reference_range_string(
        self,
        canonical_test_id: int,
        unit: Optional[str] = None,
        gender: Optional[str] = None,
        age_years: Optional[float] = None
    ) -> Optional[str]:
        """
        Get formatted reference range string
        
        Returns:
            Formatted string like "12.0-16.0" or None if not found
        """
        with db_manager.get_session() as session:
            reference = self._find_reference_range(
                session, canonical_test_id, unit, gender, age_years
            )
            
            if not reference:
                return None
            
            # Cast to proper types
            lower = cast(Optional[float], reference.lower_bound)
            upper = cast(Optional[float], reference.upper_bound)
            
            if lower is not None and upper is not None:
                return f"{lower}-{upper}"
            elif lower is not None:
                return f">={lower}"
            elif upper is not None:
                return f"<={upper}"
            else:
                return None