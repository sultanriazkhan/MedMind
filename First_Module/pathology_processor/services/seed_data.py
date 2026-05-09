# services/seed_data.py
import csv
import logging
from pathlib import Path

from models.database import db_manager
from models.orm_models import CanonicalTest, TestAlias, ReferenceRange, CriticalThreshold
from services.text_normalizer import TextNormalizer

logger = logging.getLogger(__name__)

def seed_database():
    """Seed initial reference data"""
    with db_manager.get_session() as session:
        # Check if already seeded
        if session.query(CanonicalTest).count() > 0:
            logger.info("Database already seeded")
            return
        
        # Seed canonical tests
        canonical_tests = [
            # Hematology
            {"name": "hemoglobin", "loinc": "718-7", "category": "Hematology", "default_unit": "g/dL"},
            {"name": "white blood cell count", "loinc": "6690-2", "category": "Hematology", "default_unit": "x10^3/uL"},
            {"name": "platelet count", "loinc": "777-3", "category": "Hematology", "default_unit": "x10^3/uL"},
            {"name": "hematocrit", "loinc": "4544-3", "category": "Hematology", "default_unit": "%"},
            {"name": "red blood cell count", "loinc": "789-8", "category": "Hematology", "default_unit": "x10^6/uL"},
            
            # Chemistry
            {"name": "creatinine", "loinc": "2160-0", "category": "Chemistry", "default_unit": "mg/dL"},
            {"name": "blood urea nitrogen", "loinc": "3094-0", "category": "Chemistry", "default_unit": "mg/dL"},
            {"name": "glucose", "loinc": "2345-7", "category": "Chemistry", "default_unit": "mg/dL"},
            {"name": "sodium", "loinc": "2951-2", "category": "Chemistry", "default_unit": "mmol/L"},
            {"name": "potassium", "loinc": "2823-3", "category": "Chemistry", "default_unit": "mmol/L"},
            {"name": "chloride", "loinc": "2075-0", "category": "Chemistry", "default_unit": "mmol/L"},
            {"name": "calcium", "loinc": "1995-0", "category": "Chemistry", "default_unit": "mg/dL"},
            
            # Liver function
            {"name": "alanine aminotransferase", "loinc": "1742-6", "category": "Liver", "default_unit": "U/L"},
            {"name": "aspartate aminotransferase", "loinc": "1920-8", "category": "Liver", "default_unit": "U/L"},
            {"name": "alkaline phosphatase", "loinc": "6768-6", "category": "Liver", "default_unit": "U/L"},
            {"name": "total bilirubin", "loinc": "1975-2", "category": "Liver", "default_unit": "mg/dL"},
            
            # Lipids
            {"name": "total cholesterol", "loinc": "2093-3", "category": "Lipids", "default_unit": "mg/dL"},
            {"name": "triglycerides", "loinc": "2571-8", "category": "Lipids", "default_unit": "mg/dL"},
            {"name": "hdl cholesterol", "loinc": "2085-9", "category": "Lipids", "default_unit": "mg/dL"},
            {"name": "ldl cholesterol", "loinc": "22748-8", "category": "Lipids", "default_unit": "mg/dL"},
        ]
        
        test_objects = {}
        for test_data in canonical_tests:
            test = CanonicalTest(
                canonical_name=test_data["name"],
                loinc_code=test_data["loinc"],
                category=test_data["category"],
                default_unit=test_data["default_unit"]
            )
            session.add(test)
            session.flush()
            test_objects[test_data["name"]] = test.id
        
        # Seed aliases
        aliases = [
            # Hemoglobin aliases
            ("hemoglobin", "hb", "abbreviation", 1.0),
            ("hemoglobin", "hgb", "abbreviation", 1.0),
            ("hemoglobin", "haemoglobin", "alternate_spelling", 0.95),
            ("hemoglobin", "hemoglobin hb", "common", 0.9),
            
            # WBC aliases
            ("white blood cell count", "wbc", "abbreviation", 1.0),
            ("white blood cell count", "wbc count", "common", 1.0),
            ("white blood cell count", "white blood cells", "synonym", 0.95),
            ("white blood cell count", "total wbc count", "common", 0.95),
            
            # Platelet aliases
            ("platelet count", "plt", "abbreviation", 1.0),
            ("platelet count", "platelets", "synonym", 1.0),
            
            # Creatinine aliases
            ("creatinine", "creatinine serum", "common", 0.95),
            ("creatinine", "sr. creatinine", "abbreviation", 0.9),
            ("creatinine", "serum creatinine", "common", 0.98),
            ("creatinine", "creat", "abbreviation", 0.95),
            
            # Glucose aliases
            ("glucose", "glu", "abbreviation", 0.95),
            ("glucose", "fasting blood sugar", "synonym", 0.9),
            ("glucose", "fbs", "abbreviation", 0.95),
            ("glucose", "fasting glucose", "common", 0.95),
        ]
        
        for canonical_name, alias, alias_type, confidence in aliases:
            if canonical_name in test_objects:
                alias_obj = TestAlias(
                    canonical_test_id=test_objects[canonical_name],
                    alias=alias,
                    normalized_alias=TextNormalizer.normalize_for_matching(alias),
                    alias_type=alias_type,
                    confidence_score=confidence
                )
                session.add(alias_obj)
        
        # Seed reference ranges
        reference_ranges = [
            # Hemoglobin - Male
            ("hemoglobin", "M", None, None, 13.5, 17.5, "g/dL"),
            # Hemoglobin - Female
            ("hemoglobin", "F", None, None, 12.0, 15.5, "g/dL"),
            
            # WBC
            ("white blood cell count", None, None, None, 4.0, 11.0, "x10^3/uL"),
            
            # Platelets
            ("platelet count", None, None, None, 150, 400, "x10^3/uL"),
            
            # Creatinine - Male
            ("creatinine", "M", None, None, 0.7, 1.3, "mg/dL"),
            # Creatinine - Female
            ("creatinine", "F", None, None, 0.6, 1.1, "mg/dL"),
            
            # Glucose - Fasting
            ("glucose", None, None, None, 70, 100, "mg/dL"),
            
            # Sodium
            ("sodium", None, None, None, 135, 145, "mmol/L"),
            
            # Potassium
            ("potassium", None, None, None, 3.5, 5.0, "mmol/L"),
            
            # Calcium
            ("calcium", None, None, None, 8.5, 10.2, "mg/dL"),
            
            # ALT
            ("alanine aminotransferase", None, None, None, 10, 40, "U/L"),
            
            # AST
            ("aspartate aminotransferase", None, None, None, 10, 40, "U/L"),
            
            # Cholesterol
            ("total cholesterol", None, None, None, 125, 200, "mg/dL"),
            
            # Triglycerides
            ("triglycerides", None, None, None, 50, 150, "mg/dL"),
        ]
        
        for test_name, gender, min_age, max_age, lower, upper, unit in reference_ranges:
            if test_name in test_objects:
                range_obj = ReferenceRange(
                    canonical_test_id=test_objects[test_name],
                    gender=gender,
                    min_age_days=min_age,
                    max_age_days=max_age,
                    lower_bound=lower,
                    upper_bound=upper,
                    unit=unit,
                    source="seed_data"
                )
                session.add(range_obj)
        
        # Seed critical thresholds
        critical_thresholds = [
            ("hemoglobin", 7.0, 20.0, "g/dL"),      # Critical low/high
            ("platelet count", 20, 1000, "x10^3/uL"),
            ("potassium", 2.5, 6.5, "mmol/L"),
            ("sodium", 120, 160, "mmol/L"),
            ("glucose", 40, 500, "mg/dL"),
        ]
        
        for test_name, critical_low, critical_high, unit in critical_thresholds:
            if test_name in test_objects:
                threshold = CriticalThreshold(
                    canonical_test_id=test_objects[test_name],
                    critical_low=critical_low,
                    critical_high=critical_high,
                    unit=unit
                )
                session.add(threshold)
        
        logger.info(f"Seeded {len(canonical_tests)} canonical tests, {len(aliases)} aliases, "
                   f"{len(reference_ranges)} reference ranges, {len(critical_thresholds)} critical thresholds")

def import_loinc_csv(filepath: str):
    """Import LOINC codes from CSV file"""
    with db_manager.get_session() as session:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Find matching canonical test
                canonical_test = session.query(CanonicalTest).filter(
                    CanonicalTest.canonical_name.ilike(f"%{row['COMPONENT']}%")
                ).first()
                
                # Import LOINC mapping
                # Implementation depends on LOINC CSV structure
                pass