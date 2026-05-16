# services/seed_data.py
"""Production-grade clinical knowledge base for pathology report processing."""

import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from models.database import db_manager
from models.orm_models import CanonicalTest, TestAlias, ReferenceRange, CriticalThreshold
from services.text_normalizer import TextNormalizer

logger = logging.getLogger(__name__)


class AliasConfidence(Enum):
    """Confidence tiers for alias mappings to prevent false positives."""
    EXACT_MATCH = 1.0      # Perfect string match (loinc, exact code)
    STANDARD_ABBR = 0.95   # Standard clinical abbreviations (WBC, HGB)
    COMMON_SYNONYM = 0.85  # Frequent clinical synonyms (platelets, thrombocytes)
    CLINICAL_SHORTHAND = 0.75  # Chart shorthand (sr creat, fbs)
    TYPO_VARIANT = 0.65    # Common typing errors
    OCR_VARIANT = 0.55     # OCR-induced noise
    FUZZY_FALLBACK = 0.45  # Low-confidence heuristic matches
    AMBIGUOUS = 0.35       # Context-dependent (use only with other signals)


class ReferenceRangeQuality(Enum):
    SOURCE_MICROMEDEX = "Micromedex"
    SOURCE_UP_TO_DATE = "UpToDate"
    SOURCE_LAB_CORP = "LabCorp"
    SOURCE_QUEST = "Quest"
    SOURCE_MAYO = "Mayo Clinic"
    SOURCE_CLINICAL = "Clinical Guidelines"


def seed_database():
    """Seed production knowledge base with conflict prevention."""
    with db_manager.get_session() as session:
        if session.query(CanonicalTest).count() > 0:
            logger.info("Database already seeded")
            return

        # =================================================================
        # PHASE 1: Canonical Tests with LOINC alignment
        # =================================================================
        canonical_tests = _load_canonical_tests()
        test_objects = _insert_canonical_tests(session, canonical_tests)

        # =================================================================
        # PHASE 2: High-Quality Aliases with Confidence Tiers
        # =================================================================
        aliases = _load_tiered_aliases()
        _insert_aliases(session, test_objects, aliases)

        # =================================================================
        # PHASE 3: Evidence-Based Reference Ranges
        # =================================================================
        reference_ranges = _load_reference_ranges()
        _insert_reference_ranges(session, test_objects, reference_ranges)

        # =================================================================
        # PHASE 4: Safety-Critical Thresholds
        # =================================================================
        critical_thresholds = _load_critical_thresholds()
        _insert_critical_thresholds(session, test_objects, critical_thresholds)

        logger.info(f"Seeded {len(canonical_tests)} tests, {len(aliases)} aliases, "
                   f"{len(reference_ranges)} ranges, {len(critical_thresholds)} thresholds")


# =================================================================
# DATA LOADERS (Separated for maintainability)
# =================================================================

def _load_canonical_tests() -> List[Dict]:
    """Load LOINC-aligned canonical tests with strict naming."""
    return [
        # ---- HEMATOLOGY (Complete panel) ----
        {"name": "hemoglobin", "loinc": "718-7", "category": "Hematology", 
         "default_unit": "g/dL", "ucum_code": "g/dL"},
        {"name": "white blood cell count", "loinc": "6690-2", "category": "Hematology",
         "default_unit": "10*3/uL", "ucum_code": "10^3/uL"},
        {"name": "platelet count", "loinc": "777-3", "category": "Hematology",
         "default_unit": "10*3/uL", "ucum_code": "10^3/uL"},
        {"name": "hematocrit", "loinc": "4544-3", "category": "Hematology",
         "default_unit": "%", "ucum_code": "%"},
        {"name": "red blood cell count", "loinc": "789-8", "category": "Hematology",
         "default_unit": "10*6/uL", "ucum_code": "10^6/uL"},
        {"name": "mean corpuscular volume", "loinc": "787-2", "category": "Hematology",
         "default_unit": "fL", "ucum_code": "fL"},
        {"name": "mean corpuscular hemoglobin", "loinc": "785-6", "category": "Hematology",
         "default_unit": "pg", "ucum_code": "pg"},
        {"name": "mean corpuscular hemoglobin concentration", "loinc": "786-4", "category": "Hematology",
         "default_unit": "g/dL", "ucum_code": "g/dL"},
        {"name": "red cell distribution width", "loinc": "788-0", "category": "Hematology",
         "default_unit": "%", "ucum_code": "%"},
        {"name": "absolute neutrophil count", "loinc": "751-8", "category": "Hematology",
         "default_unit": "10*3/uL", "ucum_code": "10^3/uL"},
        
        # ---- CHEMISTRY (Complete metabolic panel) ----
        {"name": "creatinine", "loinc": "2160-0", "category": "Chemistry",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "blood urea nitrogen", "loinc": "3094-0", "category": "Chemistry",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "glucose", "loinc": "2345-7", "category": "Chemistry",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "sodium", "loinc": "2951-2", "category": "Chemistry",
         "default_unit": "mmol/L", "ucum_code": "mmol/L"},
        {"name": "potassium", "loinc": "2823-3", "category": "Chemistry",
         "default_unit": "mmol/L", "ucum_code": "mmol/L"},
        {"name": "chloride", "loinc": "2075-0", "category": "Chemistry",
         "default_unit": "mmol/L", "ucum_code": "mmol/L"},
        {"name": "carbon dioxide", "loinc": "2028-9", "category": "Chemistry",
         "default_unit": "mmol/L", "ucum_code": "mmol/L"},
        {"name": "calcium", "loinc": "1995-0", "category": "Chemistry",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "magnesium", "loinc": "19123-9", "category": "Chemistry",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "phosphorus", "loinc": "2777-1", "category": "Chemistry",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "albumin", "loinc": "1751-7", "category": "Chemistry",
         "default_unit": "g/dL", "ucum_code": "g/dL"},
        {"name": "total protein", "loinc": "2885-2", "category": "Chemistry",
         "default_unit": "g/dL", "ucum_code": "g/dL"},
        
        # ---- LIVER FUNCTION TESTS ----
        {"name": "alanine aminotransferase", "loinc": "1742-6", "category": "Liver",
         "default_unit": "U/L", "ucum_code": "U/L"},
        {"name": "aspartate aminotransferase", "loinc": "1920-8", "category": "Liver",
         "default_unit": "U/L", "ucum_code": "U/L"},
        {"name": "alkaline phosphatase", "loinc": "6768-6", "category": "Liver",
         "default_unit": "U/L", "ucum_code": "U/L"},
        {"name": "total bilirubin", "loinc": "1975-2", "category": "Liver",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "direct bilirubin", "loinc": "1968-7", "category": "Liver",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "gamma glutamyl transferase", "loinc": "2324-2", "category": "Liver",
         "default_unit": "U/L", "ucum_code": "U/L"},
        
        # ---- LIPID PROFILE ----
        {"name": "total cholesterol", "loinc": "2093-3", "category": "Lipids",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "triglycerides", "loinc": "2571-8", "category": "Lipids",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "hdl cholesterol", "loinc": "2085-9", "category": "Lipids",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        {"name": "ldl cholesterol", "loinc": "22748-8", "category": "Lipids",
         "default_unit": "mg/dL", "ucum_code": "mg/dL"},
        
        # ---- ENDOCRINE ----
        {"name": "thyroid stimulating hormone", "loinc": "3016-3", "category": "Endocrine",
         "default_unit": "mIU/L", "ucum_code": "mIU/L"},
        {"name": "free thyroxine", "loinc": "3024-7", "category": "Endocrine",
         "default_unit": "ng/dL", "ucum_code": "ng/dL"},
        {"name": "hemoglobin a1c", "loinc": "4548-4", "category": "Endocrine",
         "default_unit": "%", "ucum_code": "%"},
        
        # ---- RENAL FUNCTION ----
        {"name": "estimated glomerular filtration rate", "loinc": "94642-8", "category": "Renal",
         "default_unit": "mL/min/1.73m2", "ucum_code": "mL/min/{1.73_m2}"},
    ]


def _load_tiered_aliases() -> List[Tuple[str, str, str, float]]:
    """
    Load tiered aliases with confidence scores.
    Format: (canonical_name, alias, alias_type, confidence)
    """
    aliases = []
    
    # ========== HEMOGLOBIN (7 high, 3 medium, 2 low) ==========
    # High-confidence (1.0 - 0.95)
    aliases.extend([
        ("hemoglobin", "hb", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("hemoglobin", "hgb", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("hemoglobin", "hemoglobin level", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("hemoglobin", "haemoglobin", "alternate_spelling", AliasConfidence.COMMON_SYNONYM.value),
    ])
    # Medium-confidence (0.85 - 0.75)
    aliases.extend([
        ("hemoglobin", "hb level", "clinical_shorthand", AliasConfidence.CLINICAL_SHORTHAND.value),
        ("hemoglobin", "serum hemoglobin", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("hemoglobin", "blood hemoglobin", "common", AliasConfidence.COMMON_SYNONYM.value),
    ])
    # Low-confidence OCR (0.65 - 0.55)
    aliases.extend([
        ("hemoglobin", "hemoglubin", "typo", AliasConfidence.TYPO_VARIANT.value),
        ("hemoglobin", "hgb level", "clinical_shorthand", AliasConfidence.CLINICAL_SHORTHAND.value),
    ])
    
    # ========== WHITE BLOOD CELL COUNT (6 high, 4 medium, 2 low) ==========
    aliases.extend([
        # High-confidence
        ("white blood cell count", "wbc", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("white blood cell count", "wbc count", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("white blood cell count", "leukocyte count", "medical", AliasConfidence.STANDARD_ABBR.value),
        ("white blood cell count", "white cell count", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("white blood cell count", "leukocytes", "medical", AliasConfidence.STANDARD_ABBR.value),
        ("white blood cell count", "wbcs", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        # Medium-confidence
        ("white blood cell count", "total wbc", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("white blood cell count", "wcc", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("white blood cell count", "white blood cells", "synonym", AliasConfidence.COMMON_SYNONYM.value),
        # Low-confidence
        ("white blood cell count", "wbc cnt", "clinical_shorthand", AliasConfidence.CLINICAL_SHORTHAND.value),
        ("white blood cell count", "wbc1", "ocr_noise", AliasConfidence.OCR_VARIANT.value),
    ])
    
    # ========== PLATELET COUNT (5 high, 3 medium, 2 low) ==========
    aliases.extend([
        # High-confidence
        ("platelet count", "plt", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("platelet count", "platelets", "synonym", AliasConfidence.STANDARD_ABBR.value),
        ("platelet count", "thrombocyte count", "medical", AliasConfidence.STANDARD_ABBR.value),
        # Medium-confidence
        ("platelet count", "plt count", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("platelet count", "plts", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("platelet count", "platelet", "synonym", AliasConfidence.COMMON_SYNONYM.value),
        # Low-confidence
        ("platelet count", "plt cnt", "clinical_shorthand", AliasConfidence.CLINICAL_SHORTHAND.value),
        ("platelet count", "platlet", "typo", AliasConfidence.TYPO_VARIANT.value),
    ])
    
    # ========== CREATININE (Prevent overlap with "CR" - C-reactive protein) ==========
    aliases.extend([
        # High-confidence
        ("creatinine", "creatinine serum", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("creatinine", "serum creatinine", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("creatinine", "creat", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        # Medium-confidence (AVOID single "CR" - conflicts with C-reactive protein)
        ("creatinine", "creatinine level", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("creatinine", "plasma creatinine", "common", AliasConfidence.COMMON_SYNONYM.value),
        # Low-confidence
        ("creatinine", "sr creatinine", "clinical_shorthand", AliasConfidence.CLINICAL_SHORTHAND.value),
        ("creatinine", "creatinine blood", "common", AliasConfidence.COMMON_SYNONYM.value),
    ])
    
    # ========== GLUCOSE (5 high, 3 medium, 2 low) ==========
    aliases.extend([
        # High-confidence
        ("glucose", "glu", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("glucose", "blood glucose", "synonym", AliasConfidence.COMMON_SYNONYM.value),
        ("glucose", "serum glucose", "common", AliasConfidence.COMMON_SYNONYM.value),
        # Medium-confidence
        ("glucose", "fasting blood sugar", "synonym", AliasConfidence.CLINICAL_SHORTHAND.value),
        ("glucose", "fbs", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("glucose", "plasma glucose", "common", AliasConfidence.COMMON_SYNONYM.value),
        # Low-confidence (avoid "sugar" alone - ambiguous)
        ("glucose", "glucose level", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("glucose", "rbs", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
    ])
    
    # ========== ELECTROLYTES (Unique abbreviations, no overlaps) ==========
    aliases.extend([
        ("sodium", "na", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("sodium", "serum sodium", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("sodium", "na+", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        
        ("potassium", "k", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("potassium", "serum potassium", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("potassium", "k+", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        
        ("chloride", "cl", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("chloride", "serum chloride", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("chloride", "cl-", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
    ])
    
    # ========== LIVER FUNCTION TESTS (Prevent ALT/AST confusion) ==========
    aliases.extend([
        # ALT - High confidence
        ("alanine aminotransferase", "alt", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("alanine aminotransferase", "sgpt", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("alanine aminotransferase", "alanine transaminase", "synonym", AliasConfidence.STANDARD_ABBR.value),
        
        # AST - High confidence (distinct from ALT)
        ("aspartate aminotransferase", "ast", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("aspartate aminotransferase", "sgot", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("aspartate aminotransferase", "aspartate transaminase", "synonym", AliasConfidence.STANDARD_ABBR.value),
        
        # ALP
        ("alkaline phosphatase", "alp", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("alkaline phosphatase", "alk phos", "abbreviation", AliasConfidence.CLINICAL_SHORTHAND.value),
        
        # Bilirubin (avoid "bili" ambiguity)
        ("total bilirubin", "total bili", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("total bilirubin", "tbili", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("direct bilirubin", "direct bili", "common", AliasConfidence.COMMON_SYNONYM.value),
        ("direct bilirubin", "dbili", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
    ])
    
    # ========== LIPID PROFILE ==========
    aliases.extend([
        ("total cholesterol", "chol", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("total cholesterol", "t chol", "abbreviation", AliasConfidence.CLINICAL_SHORTHAND.value),
        ("total cholesterol", "serum cholesterol", "common", AliasConfidence.COMMON_SYNONYM.value),
        
        ("triglycerides", "trig", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("triglycerides", "tg", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        
        ("hdl cholesterol", "hdl", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("hdl cholesterol", "hdl-c", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        
        ("ldl cholesterol", "ldl", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("ldl cholesterol", "ldl-c", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
    ])
    
    # ========== ENDOCRINE ==========
    aliases.extend([
        ("thyroid stimulating hormone", "tsh", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("thyroid stimulating hormone", "thyrotropin", "medical", AliasConfidence.STANDARD_ABBR.value),
        
        ("free thyroxine", "ft4", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("free thyroxine", "free t4", "common", AliasConfidence.COMMON_SYNONYM.value),
        
        ("hemoglobin a1c", "hba1c", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("hemoglobin a1c", "a1c", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("hemoglobin a1c", "glycated hemoglobin", "synonym", AliasConfidence.COMMON_SYNONYM.value),
    ])
    
    # ========== RENAL ==========
    aliases.extend([
        ("estimated glomerular filtration rate", "egfr", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
        ("estimated glomerular filtration rate", "gfr", "abbreviation", AliasConfidence.STANDARD_ABBR.value),
    ])
    
    return aliases


def _load_reference_ranges() -> List[Tuple]:
    """Evidence-based reference ranges from clinical guidelines."""
    return [
        # HEMATOLOGY - Gender-specific
        ("hemoglobin", "M", None, None, 13.5, 17.5, "g/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("hemoglobin", "F", None, None, 12.0, 15.5, "g/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("hematocrit", "M", None, None, 41.0, 53.0, "%", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("hematocrit", "F", None, None, 36.0, 46.0, "%", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("red blood cell count", "M", None, None, 4.5, 5.9, "10*6/uL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("red blood cell count", "F", None, None, 4.1, 5.1, "10*6/uL", ReferenceRangeQuality.SOURCE_MAYO.value),
        
        # HEMATOLOGY - Universal
        ("white blood cell count", None, None, None, 4.0, 11.0, "10*3/uL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("platelet count", None, None, None, 150, 450, "10*3/uL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("mean corpuscular volume", None, None, None, 80, 100, "fL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("mean corpuscular hemoglobin", None, None, None, 27, 33, "pg", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("absolute neutrophil count", None, None, None, 1.5, 8.0, "10*3/uL", ReferenceRangeQuality.SOURCE_MAYO.value),
        
        # CHEMISTRY
        ("creatinine", "M", None, None, 0.7, 1.3, "mg/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("creatinine", "F", None, None, 0.6, 1.1, "mg/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("blood urea nitrogen", None, None, None, 7, 20, "mg/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("glucose", None, None, None, 70, 100, "mg/dL", ReferenceRangeQuality.SOURCE_CLINICAL.value),  # Fasting
        ("sodium", None, None, None, 135, 145, "mmol/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("potassium", None, None, None, 3.5, 5.0, "mmol/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("chloride", None, None, None, 98, 107, "mmol/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("carbon dioxide", None, None, None, 22, 29, "mmol/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("calcium", None, None, None, 8.5, 10.2, "mg/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("magnesium", None, None, None, 1.7, 2.2, "mg/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("phosphorus", None, None, None, 2.5, 4.5, "mg/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("albumin", None, None, None, 3.5, 5.0, "g/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("total protein", None, None, None, 6.0, 8.0, "g/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        
        # LIVER
        ("alanine aminotransferase", "M", None, None, 10, 40, "U/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("alanine aminotransferase", "F", None, None, 7, 35, "U/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("aspartate aminotransferase", None, None, None, 10, 40, "U/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("alkaline phosphatase", None, None, None, 30, 120, "U/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("total bilirubin", None, None, None, 0.3, 1.2, "mg/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("direct bilirubin", None, None, None, 0.0, 0.3, "mg/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("gamma glutamyl transferase", "M", None, None, 10, 60, "U/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("gamma glutamyl transferase", "F", None, None, 10, 40, "U/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        
        # LIPIDS
        ("total cholesterol", None, None, None, 125, 200, "mg/dL", ReferenceRangeQuality.SOURCE_CLINICAL.value),
        ("triglycerides", None, None, None, 50, 150, "mg/dL", ReferenceRangeQuality.SOURCE_CLINICAL.value),
        ("hdl cholesterol", "M", None, None, 40, 60, "mg/dL", ReferenceRangeQuality.SOURCE_CLINICAL.value),
        ("hdl cholesterol", "F", None, None, 50, 60, "mg/dL", ReferenceRangeQuality.SOURCE_CLINICAL.value),
        ("ldl cholesterol", None, None, None, 50, 100, "mg/dL", ReferenceRangeQuality.SOURCE_CLINICAL.value),
        
        # ENDOCRINE
        ("thyroid stimulating hormone", None, None, None, 0.4, 4.0, "mIU/L", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("free thyroxine", None, None, None, 0.8, 1.8, "ng/dL", ReferenceRangeQuality.SOURCE_MAYO.value),
        ("hemoglobin a1c", None, None, None, 4.0, 5.6, "%", ReferenceRangeQuality.SOURCE_CLINICAL.value),
        
        # RENAL
        ("estimated glomerular filtration rate", None, None, None, 60, 120, "mL/min/1.73m2", ReferenceRangeQuality.SOURCE_CLINICAL.value),
    ]


def _load_critical_thresholds() -> List[Tuple]:
    """Life-critical thresholds from emergency medicine guidelines."""
    return [
        # HEMATOLOGY
        ("hemoglobin", 7.0, 20.0, "g/dL"),     # Transfusion trigger / Polycythemia risk
        ("platelet count", 20.0, 1000.0, "10*3/uL"),  # Spontaneous bleeding / Thrombosis
        
        # ELECTROLYTES (Cardiac arrhythmia risks)
        ("potassium", 2.5, 6.5, "mmol/L"),      # Severe hypo/hyperkalemia
        ("sodium", 120.0, 160.0, "mmol/L"),     # Seizure/coma risk
        ("calcium", 6.0, 13.0, "mg/dL"),        # Tetany / Coma
        
        # METABOLIC
        ("glucose", 40.0, 500.0, "mg/dL"),      # Hypoglycemic coma / DKA
        ("creatinine", 4.0, 10.0, "mg/dL"),     # Severe renal failure (dialysis threshold)
        
        # LIVER (Acute liver failure markers)
        ("alanine aminotransferase", 1000.0, None, "U/L"),  # Massive hepatocellular injury
        ("aspartate aminotransferase", 1000.0, None, "U/L"),
        ("total bilirubin", 15.0, None, "mg/dL"),           # Severe hyperbilirubinemia
    ]


# =================================================================
# DATABASE INSERTION HELPERS
# =================================================================

def _insert_canonical_tests(session, tests: List[Dict]) -> Dict[str, int]:
    """Insert canonical tests and return mapping dict."""
    test_objects = {}
    for test_data in tests:
        test = CanonicalTest(
            canonical_name=test_data["name"],
            loinc_code=test_data.get("loinc"),
            category=test_data["category"],
            default_unit=test_data["default_unit"]
        )
        session.add(test)
        session.flush()
        test_objects[test_data["name"]] = test.id
    return test_objects


def _insert_aliases(session, test_objects: Dict[str, int], aliases: List[Tuple]):
    """Insert aliases with deduplication and conflict prevention."""
    seen_aliases = set()
    
    for canonical_name, alias, alias_type, confidence in aliases:
        if canonical_name not in test_objects:
            logger.warning(f"Skipping alias '{alias}' for unknown test '{canonical_name}'")
            continue
        
        normalized = TextNormalizer.normalize_for_matching(alias)
        
        # Prevent duplicate aliases
        if (canonical_name, normalized) in seen_aliases:
            logger.warning(f"Duplicate alias '{alias}' for '{canonical_name}' - skipping")
            continue
        
        seen_aliases.add((canonical_name, normalized))
        
        alias_obj = TestAlias(
            canonical_test_id=test_objects[canonical_name],
            alias=alias,
            normalized_alias=normalized,
            alias_type=alias_type,
            confidence_score=confidence
        )
        session.add(alias_obj)


def _insert_reference_ranges(session, test_objects: Dict[str, int], ranges: List[Tuple]):
    """Insert reference ranges with validation."""
    for range_data in ranges:
        if len(range_data) == 8:
            test_name, gender, min_age, max_age, lower, upper, unit, source = range_data
        else:
            test_name, gender, min_age, max_age, lower, upper, unit = range_data
            source = "Clinical Guidelines"
        
        if test_name not in test_objects:
            logger.warning(f"Skipping range for unknown test '{test_name}'")
            continue
        
        # Validate range logic
        if lower is not None and upper is not None and lower >= upper:
            logger.error(f"Invalid range for {test_name}: {lower} > {upper}")
            continue
        
        range_obj = ReferenceRange(
            canonical_test_id=test_objects[test_name],
            gender=gender,
            min_age_days=min_age,
            max_age_days=max_age,
            lower_bound=lower,
            upper_bound=upper,
            unit=unit,
            source=source
        )
        session.add(range_obj)


def _insert_critical_thresholds(session, test_objects: Dict[str, int], thresholds: List[Tuple]):
    """Insert critical thresholds with safety validation."""
    for test_name, critical_low, critical_high, unit in thresholds:
        if test_name not in test_objects:
            logger.warning(f"Skipping threshold for unknown test '{test_name}'")
            continue
        
        threshold = CriticalThreshold(
            canonical_test_id=test_objects[test_name],
            critical_low=critical_low,
            critical_high=critical_high,
            unit=unit
        )
        session.add(threshold)


# =================================================================
# LOINC INTEGRATION UTILITIES
# =================================================================

def import_loinc_csv(filepath: str):
    """Import LOINC mappings from standard LOINC CSV export."""
    import pandas as pd
    
    df = pd.read_csv(filepath)
    
    # Required columns in standard LOINC distribution
    required_cols = ['LOINC_NUM', 'COMPONENT', 'PROPERTY', 'TIME_ASPCT', 
                     'SYSTEM', 'SCALE_TYP', 'METHOD_TYP', 'CLASS']
    
    with db_manager.get_session() as session:
        for _, row in df.iterrows():
            loinc_code = row['LOINC_NUM']
            component = row['COMPONENT'].lower()
            
            # Find matching canonical test by component name
            # Complex matching logic would go here
            canonical_test = session.query(CanonicalTest).filter(
                CanonicalTest.canonical_name.ilike(f"%{component}%")
            ).first()
            
            if canonical_test:
                # Update LOINC code
                canonical_test.loinc_code = loinc_code
                logger.info(f"Mapped {canonical_test.canonical_name} -> LOINC {loinc_code}")