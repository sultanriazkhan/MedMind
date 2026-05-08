# services/pipeline.py
import hashlib
import time
import uuid
from typing import List, Dict, Any
from dataclasses import dataclass, field
import logging

from services.text_normalizer import TextNormalizer, OCRCleanup
from services.regex_extractor import RegexExtractor, ExtractedTest
from services.scispacy_fallback import ScispaCyFallback
from services.canonical_engine import CanonicalizationEngine
from services.range_classifier import RangeClassifier, ResultStatus
from services.unit_normalizer import UnitNormalizer
from models.database import db_manager
from models.orm_models import ProcessingLog

logger = logging.getLogger(__name__)

@dataclass
class ProcessingResult:
    request_id: str
    tests: List[Dict[str, Any]]
    processing_time_ms: float
    regex_matches: int
    fallback_matches: int
    canonicalized: int
    errors: List[str] = field(default_factory=list)

class ProcessingPipeline:
    """Main processing pipeline orchestrator"""
    
    def __init__(self):
        self.regex_extractor = RegexExtractor()
        self.scispacy = ScispaCyFallback()
        self.canonical_engine = CanonicalizationEngine()
        self.range_classifier = RangeClassifier()
    
    def process(self, raw_text: str) -> ProcessingResult:
        """Execute complete processing pipeline"""
        start_time = time.time()
        request_id = str(uuid.uuid4())
        errors = []
        
        try:
            # Step 1: Text Normalization
            normalized_text = self._normalize_text(raw_text)
            
            # Step 2: Line Segmentation
            lines = self._segment_lines(normalized_text)
            
            # Step 3: Regex-based Extraction (PRIMARY)
            regex_tests = self._extract_with_regex(lines)
            regex_matches = len(regex_tests)
            
            # Step 4: scispaCy Fallback for remaining text
            remaining_text = self._get_remaining_text(lines, regex_tests)
            fallback_tests = self._extract_with_scispacy(remaining_text)
            fallback_matches = len(fallback_tests)
            
            # Step 5-6: Combine and canonicalize
            all_tests = regex_tests + fallback_tests
            canonicalized_tests = self._canonicalize_tests(all_tests)
            
            # Step 7: Apply reference range classification
            classified_tests = self._classify_results(canonicalized_tests)
            
            # Step 8: Prepare output
            output_tests = self._prepare_output(classified_tests)
            
            processing_time = (time.time() - start_time) * 1000
            
            # Log processing
            self._log_processing(request_id, len(output_tests), processing_time, 
                                regex_matches, fallback_matches, errors)
            
            return ProcessingResult(
                request_id=request_id,
                tests=output_tests,
                processing_time_ms=processing_time,
                regex_matches=regex_matches,
                fallback_matches=fallback_matches,
                canonicalized=len([t for t in output_tests if t.get('canonical_name')]),
                errors=errors
            )
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            errors.append(str(e))
            
            return ProcessingResult(
                request_id=request_id,
                tests=[],
                processing_time_ms=(time.time() - start_time) * 1000,
                regex_matches=0,
                fallback_matches=0,
                canonicalized=0,
                errors=errors
            )
    
    def _normalize_text(self, text: str) -> str:
        """Apply text normalization"""
        # OCR cleanup
        text = OCRCleanup.clean(text)
        
        # Normalization
        result = TextNormalizer.normalize(text)
        
        return result.normalized
    
    def _segment_lines(self, text: str) -> List[str]:
        """Segment text into lines for processing"""
        lines = text.split('\n')
        # Remove empty lines
        lines = [line.strip() for line in lines if line.strip()]
        return lines
    
    def _extract_with_regex(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Primary regex-based extraction"""
        tests = []
        
        for line in lines:
            extracted = self.regex_extractor.extract_from_text(line)
            for test in extracted:
                tests.append({
                    'raw_text': test.raw_text,
                    'test_name': test.test_name,
                    'value': test.value,
                    'unit': test.unit,
                    'reference_range': test.reference_range,
                    'flag': test.flag,
                    'extraction_method': 'regex',
                    'confidence': test.confidence
                })
        
        return tests
    
    def _get_remaining_text(self, lines: List[str], extracted_tests: List[Dict]) -> str:
        """Get text that wasn't covered by regex extraction"""
        # Simple heuristic: join lines that don't match extracted patterns
        extracted_texts = set([t['raw_text'] for t in extracted_tests])
        
        remaining = []
        for line in lines:
            if line not in extracted_texts:
                remaining.append(line)
        
        return '\n'.join(remaining)
    
    def _extract_with_scispacy(self, text: str) -> List[Dict[str, Any]]:
        """scispaCy fallback extraction"""
        if not text.strip():
            return []
        
        candidates = self.scispacy.extract_test_candidates(text)
        
        tests = []
        for cand in candidates:
            if cand['value'] is not None:
                tests.append({
                    'raw_text': cand['raw_text'],
                    'test_name': cand['test_name'],
                    'value': cand['value'],
                    'unit': cand['unit'],
                    'reference_range': cand['reference_range'],
                    'extraction_method': 'scispacy',
                    'confidence': cand['confidence']
                })
        
        return tests
    
    def _canonicalize_tests(self, tests: List[Dict]) -> List[Dict]:
        """Apply canonicalization to all extracted tests"""
        canonicalized = []
        
        for test in tests:
            canonical = self.canonical_engine.canonicalize_with_context(test)
            canonicalized.append(canonical)
        
        return canonicalized
    
    def _classify_results(self, tests: List[Dict]) -> List[Dict]:
        """Apply reference range classification"""
        for test in tests:
            if test.get('canonical_test_id') and test.get('value'):
                status = self.range_classifier.classify(
                    canonical_test_id=test['canonical_test_id'],
                    value=test['value'],
                    unit=test.get('unit'),
                    gender=None,  # Could be extracted from report
                    age_years=None
                )
                test['status'] = status.value
            else:
                test['status'] = ResultStatus.UNKNOWN.value
        
        return tests
    
    def _prepare_output(self, tests: List[Dict]) -> List[Dict]:
        """Prepare final output format"""
        output = []
        
        for test in tests:
            output_test = {
                'raw_text': test.get('raw_text', ''),
                'raw_test_name': test.get('test_name', ''),
                'normalized_test_name': test.get('normalized_test_name', ''),
                'canonical_name': test.get('canonical_name'),
                'loinc_code': test.get('loinc_code'),
                'value': test.get('value'),
                'unit': UnitNormalizer.normalize(test.get('unit')),
                'reference_range': test.get('reference_range'),
                'status': test.get('status', ResultStatus.UNKNOWN.value),
                'match_type': test.get('match_type', 'unknown'),
                'similarity_score': test.get('similarity_score', 0.0),
                'confidence_score': test.get('confidence_score', 0.0)
            }
            output.append(output_test)
        
        return output
    
    def _log_processing(self, request_id: str, test_count: int, 
                       processing_time: float, regex_matches: int,
                       fallback_matches: int, errors: List[str]):
        """Log processing for analytics"""
        try:
            with db_manager.get_session() as session:
                log = ProcessingLog(
                    request_id=request_id,
                    extracted_tests_count=test_count,
                    processing_time_ms=processing_time,
                    success=1 if not errors else 0,
                    error_message='; '.join(errors) if errors else None
                )
                session.add(log)
        except Exception as e:
            logger.error(f"Failed to log processing: {e}")