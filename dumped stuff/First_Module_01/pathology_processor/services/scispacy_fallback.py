# services/scispacy_fallback.py
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Try to import scispacy and spaCy, but handle gracefully if not available
try:
    import scispacy
    SCISPAXY_AVAILABLE = True
except ImportError:
    SCISPAXY_AVAILABLE = False
    logger.warning("scispaCy not available. Using fallback NER only.")

try:
    import spacy
except ImportError:
    spacy = None
    logger.warning("spaCy not available. NER features will be disabled.")

@dataclass
class NEREntity:
    text: str
    label: str  
    start: int
    end: int
    confidence: float

class ScispaCyFallback:
    """Fallback NER layer when regex extraction fails"""
    
    def __init__(self, model_name: str = "en_core_sci_sm"):
        self.model_name = model_name
        self.nlp = None
        self._initialize()
    
    def _initialize(self):
        """Initialize scispaCy model if available"""
        if SCISPAXY_AVAILABLE and spacy is not None:
            try:
                self.nlp = spacy.load(self.model_name)
                logger.info(f"Loaded scispaCy model: {self.model_name}")
            except OSError:
                logger.warning(f"Model {self.model_name} not found. Downloading...")
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", self.model_name])
                self.nlp = spacy.load(self.model_name)
        else:
            # Fallback to basic spaCy
            try:
                import spacy as spacy_module
                self.nlp = spacy_module.load("en_core_web_sm")
                logger.info("Loaded fallback spaCy model")
            except:
                logger.error("No NER model available")
    
    def extract_entities(self, text: str) -> List[NEREntity]:
        """Extract medical entities using scispaCy"""
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        # Medical entity labels in scispaCy
        medical_labels = {'CHEMICAL', 'DISEASE', 'GENE', 'PROTEIN', 'CELL', 
                         'ANATOMY', 'DRUG', 'LAB_TEST', 'UNIT', 'VALUE'}
        
        for ent in doc.ents:
            if ent.label_ in medical_labels or 'test' in ent.label_.lower():
                entities.append(NEREntity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=0.7  # Default confidence for NER
                ))
        
        return entities
    
    def extract_test_candidates(self, text: str) -> List[Dict[str, Any]]:
        """Extract potential lab test mentions"""
        entities = self.extract_entities(text)
        test_candidates = []
        
        for ent in entities:
            # Look for lab test patterns
            if ent.label == 'LAB_TEST' or 'test' in ent.label.lower():
                # Find surrounding context
                context_start = max(0, ent.start - 50)
                context_end = min(len(text), ent.end + 100)
                context = text[context_start:context_end]
                
                # Extract value if present
                value, unit, ref_range = self._extract_value_from_context(context)
                
                test_candidates.append({
                    'test_name': ent.text,
                    'value': value,
                    'unit': unit,
                    'reference_range': ref_range,
                    'raw_text': context,
                    'ner_label': ent.label,
                    'confidence': ent.confidence
                })
        
        return test_candidates
    
    def _extract_value_from_context(self, context: str) -> tuple:
        """Extract value, unit, reference range from context"""
        import re
        
        # Value extraction
        value_pattern = r'(\d+(?:\.\d+)?)'
        value_match = re.search(value_pattern, context)
        value = float(value_match.group(1)) if value_match else None
        
        # Unit extraction
        unit_pattern = r'(?:mg/dL|g/dL|mmol/L|μmol/L|pg/mL|ng/mL|u/L|IU/L|%)'
        unit_match = re.search(unit_pattern, context, re.IGNORECASE)
        unit = unit_match.group(0) if unit_match else None
        
        # Reference range extraction
        range_pattern = r'(\d+(?:\.\d+)?\s*[\-\–]\s*\d+(?:\.\d+)?)'
        range_match = re.search(range_pattern, context)
        ref_range = range_match.group(0) if range_match else None
        
        return value, unit, ref_range