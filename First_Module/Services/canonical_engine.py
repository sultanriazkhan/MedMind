# services/canonical_engine.py
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from models.database import db_manager
from services.alias_resolver import AliasResolver, AliasResolutionResult
from services.text_normalizer import TextNormalizer

@dataclass
class CanonicalResult:
    raw_test_name: str
    normalized_test_name: str
    canonical_name: str
    canonical_test_id: int
    loinc_code: Optional[str]
    match_type: str
    confidence_score: float
    similarity_score: float

class CanonicalizationEngine:
    """Ensures all tests map to canonical identities"""
    
    def __init__(self):
        self._alias_resolver_cache = {}
    
    def canonicalize(self, raw_test_name: str) -> Optional[CanonicalResult]:
        """Convert raw test name to canonical form"""
        from services.text_normalizer import TextNormalizer
        
        # Step 1: Normalize
        normalized = TextNormalizer.normalize_for_matching(raw_test_name)
        
        # Step 2: Resolve alias
        with db_manager.get_session() as session:
            resolver = AliasResolver(session)
            result = resolver.resolve(raw_test_name)
            
            if not result:
                return None
            
            # Step 3: Get LOINC code
            loinc_code = self._get_loinc_code(session, result.canonical_id)
            
            return CanonicalResult(
                raw_test_name=raw_test_name,
                normalized_test_name=normalized,
                canonical_name=result.canonical_name,
                canonical_test_id=result.canonical_id,
                loinc_code=loinc_code,
                match_type=result.match_type,
                confidence_score=result.confidence,
                similarity_score=result.similarity_score
            )
    
    def _get_loinc_code(self, session, canonical_id: int) -> Optional[str]:
        """Retrieve LOINC code for canonical test"""
        from models.orm_models import CanonicalTest
        
        test = session.query(CanonicalTest).filter(CanonicalTest.id == canonical_id).first()
        return test.loinc_code if test else None
    
    def canonicalize_with_context(self, extraction: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich extracted test with canonical information"""
        if not extraction.get('test_name'):
            return extraction
        
        canonical = self.canonicalize(extraction['test_name'])
        
        if canonical:
            extraction.update({
                'normalized_test_name': canonical.normalized_test_name,
                'canonical_name': canonical.canonical_name,
                'canonical_test_id': canonical.canonical_test_id,
                'loinc_code': canonical.loinc_code,
                'match_type': canonical.match_type,
                'confidence_score': canonical.confidence_score,
                'similarity_score': canonical.similarity_score
            })
        else:
            # Unmapped test
            extraction.update({
                'normalized_test_name': TextNormalizer.normalize_for_matching(extraction['test_name']),
                'canonical_name': None,
                'canonical_test_id': None,
                'loinc_code': None,
                'match_type': 'unknown',
                'confidence_score': 0.0,
                'similarity_score': 0.0
            })
        
        return extraction