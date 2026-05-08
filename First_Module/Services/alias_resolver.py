# services/alias_resolver.py
import logging
from typing import Optional, List, Dict, Tuple
from sqlalchemy.orm import Session
from rapidfuzz import fuzz, process

from models.orm_models import CanonicalTest, TestAlias
from services.text_normalizer import TextNormalizer

logger = logging.getLogger(__name__)

class AliasResolutionResult:
    def __init__(self, canonical_id: int, canonical_name: str, 
                 match_type: str, similarity_score: float, 
                 matched_alias: str, confidence: float):
        self.canonical_id = canonical_id
        self.canonical_name = canonical_name
        self.match_type = match_type  # exact, canonical, fuzzy, synonym
        self.similarity_score = similarity_score
        self.matched_alias = matched_alias
        self.confidence = confidence

class AliasResolver:
    """Resolves test aliases to canonical test names with priority-based matching"""
    
    def __init__(self, db_session: Session, fuzzy_threshold: int = 85):
        self.db = db_session
        self.fuzzy_threshold = fuzzy_threshold
        self._cache = {}  # Simple in-memory cache
        self._load_all_aliases()
    
    def _load_all_aliases(self):
        """Preload all aliases for faster lookup"""
        try:
            # Preload canonical tests
            self.canonical_tests = {
                test.canonical_name: test.id 
                for test in self.db.query(CanonicalTest).all()
            }
            
            # Preload aliases
            self.aliases = {}
            aliases = self.db.query(TestAlias).all()
            for alias in aliases:
                normalized = alias.normalized_alias
                if normalized not in self.aliases:
                    self.aliases[normalized] = []
                self.aliases[normalized].append({
                    'canonical_id': alias.canonical_test_id,
                    'canonical_name': alias.canonical_test.canonical_name,
                    'confidence': alias.confidence_score
                })
            
            logger.info(f"Loaded {len(self.aliases)} unique aliases for {len(self.canonical_tests)} canonical tests")
        except Exception as e:
            logger.error(f"Error loading aliases: {e}")
            self.aliases = {}
            self.canonical_tests = {}
    
    def resolve(self, raw_test_name: str) -> Optional[AliasResolutionResult]:
        """
        Resolve test name to canonical form following priority order:
        1. Exact normalized alias match
        2. Canonical name exact match
        3. Medical synonym lookup
        4. Fuzzy matching fallback
        """
        # Normalize input
        normalized = TextNormalizer.normalize_for_matching(raw_test_name)
        
        # Check cache
        cache_key = normalized
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # STEP 1: Exact normalized alias match
        result = self._exact_alias_match(normalized)
        if result:
            self._cache[cache_key] = result
            return result
        
        # STEP 2: Canonical name exact match
        result = self._canonical_match(normalized)
        if result:
            self._cache[cache_key] = result
            return result
        
        # STEP 3: Medical synonym lookup (normalized variations)
        result = self._synonym_lookup(normalized)
        if result:
            self._cache[cache_key] = result
            return result
        
        # STEP 4: Fuzzy matching fallback
        result = self._fuzzy_match(normalized)
        if result:
            self._cache[cache_key] = result
        
        return result
    
    def _exact_alias_match(self, normalized: str) -> Optional[AliasResolutionResult]:
        """Check for exact match in aliases"""
        if normalized in self.aliases:
            # Return highest confidence match
            matches = self.aliases[normalized]
            best = max(matches, key=lambda x: x['confidence'])
            return AliasResolutionResult(
                canonical_id=best['canonical_id'],
                canonical_name=best['canonical_name'],
                match_type='exact_alias',
                similarity_score=1.0,
                matched_alias=normalized,
                confidence=best['confidence']
            )
        return None
    
    def _canonical_match(self, normalized: str) -> Optional[AliasResolutionResult]:
        """Check for exact match with canonical names"""
        if normalized in self.canonical_tests:
            return AliasResolutionResult(
                canonical_id=self.canonical_tests[normalized],
                canonical_name=normalized,
                match_type='canonical',
                similarity_score=1.0,
                matched_alias=normalized,
                confidence=1.0
            )
        return None
    
    def _synonym_lookup(self, normalized: str) -> Optional[AliasResolutionResult]:
        """Look for known synonyms and variations"""
        # Common synonym patterns
        synonyms = {
            'hb': 'hemoglobin',
            'hgb': 'hemoglobin',
            'wbc': 'white blood cell count',
            'plt': 'platelet count',
            'creat': 'creatinine',
            'bun': 'blood urea nitrogen',
            'alt': 'alanine aminotransferase',
            'ast': 'aspartate aminotransferase',
            'hct': 'hematocrit',
            'rbc': 'red blood cell count',
        }
        
        if normalized in synonyms:
            target = synonyms[normalized]
            if target in self.canonical_tests:
                return AliasResolutionResult(
                    canonical_id=self.canonical_tests[target],
                    canonical_name=target,
                    match_type='synonym',
                    similarity_score=0.95,
                    matched_alias=normalized,
                    confidence=0.95
                )
        return None
    
    def _fuzzy_match(self, normalized: str) -> Optional[AliasResolutionResult]:
        """Fallback fuzzy matching for OCR errors and typos"""
        # Compare with all aliases and canonical names
        candidates = {}
        
        # Add aliases
        for alias, matches in self.aliases.items():
            score = fuzz.ratio(normalized, alias)
            if score >= self.fuzzy_threshold:
                for match in matches:
                    candidates.setdefault(match['canonical_id'], []).append(score)
        
        # Add canonical names
        for canonical_name, canonical_id in self.canonical_tests.items():
            score = fuzz.ratio(normalized, canonical_name)
            if score >= self.fuzzy_threshold:
                candidates.setdefault(canonical_id, []).append(score)
        
        if candidates:
            # Get best match
            best_id = max(candidates.items(), key=lambda x: max(x[1]))[0]
            best_score = max(candidates[best_id])
            
            # Get canonical name
            for name, cid in self.canonical_tests.items():
                if cid == best_id:
                    return AliasResolutionResult(
                        canonical_id=best_id,
                        canonical_name=name,
                        match_type='fuzzy',
                        similarity_score=best_score / 100.0,
                        matched_alias=normalized,
                        confidence=0.8  # Lower confidence for fuzzy matches
                    )
        
        return None
    
    def batch_resolve(self, test_names: List[str]) -> List[Optional[AliasResolutionResult]]:
        """Resolve multiple test names efficiently"""
        return [self.resolve(name) for name in test_names]