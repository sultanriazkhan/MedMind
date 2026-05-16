# tests/test_extraction.py
import pytest
from services.pipeline import ProcessingPipeline

def test_basic_extraction():
    pipeline = ProcessingPipeline()
    
    text = "Hemoglobin 13.5 g/dL 12-16"
    result = pipeline.process(text)
    
    assert len(result.tests) == 1
    test = result.tests[0]
    assert test['raw_test_name'] == 'Hemoglobin'
    assert test['value'] == 13.5
    assert test['unit'] == 'g/dL'
    assert test['reference_range'] == '12-16'

def test_alias_resolution():
    pipeline = ProcessingPipeline()
    
    text = "HGB 14.2 g/dL 13-17"
    result = pipeline.process(text)
    
    assert len(result.tests) == 1
    test = result.tests[0]
    assert test['canonical_name'] == 'hemoglobin'
    assert test['match_type'] == 'exact_alias'

def test_ocr_noise():
    pipeline = ProcessingPipeline()
    
    text = "Hemoglob1n 12.8 g/dL 11-15"  # OCR error
    result = pipeline.process(text)
    
    assert len(result.tests) == 1
    test = result.tests[0]
    assert test['canonical_name'] == 'hemoglobin'
    assert test['match_type'] == 'fuzzy'

def test_multiline_table():
    pipeline = ProcessingPipeline()
    
    text = """Test Name | Value | Unit | Ref Range
Hemoglobin | 14.2 | g/dL | 13-17
WBC | 7.5 | x10^3/uL | 4-11"""
    
    result = pipeline.process(text)
    assert len(result.tests) >= 2

def test_complete_report():
    pipeline = ProcessingPipeline()
    
    text = """
    PATIENT: John Doe
    DATE: 2024-01-15
    
    RESULTS:
    Hemoglobin 14.2 g/dL (13.5-17.5)
    WBC 7.8 x10^3/uL (4.0-11.0)
    Platelets 250 x10^3/uL (150-400)
    Creatinine 0.9 mg/dL (0.7-1.3)
    Glucose 95 mg/dL (70-100)
    """
    
    result = pipeline.process(text)
    assert len(result.tests) == 5
    
    # Check classifications
    for test in result.tests:
        assert test['status'] in ['Normal', 'Unknown']
    
    print(f"Processing time: {result.processing_time_ms:.2f}ms")
    print(f"Regex matches: {result.regex_matches}")
    print(f"Fallback matches: {result.fallback_matches}")