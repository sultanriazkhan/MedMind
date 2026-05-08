# api/routes.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from services.pipeline import ProcessingPipeline
from models.database import db_manager
from models.orm_models import CanonicalTest, TestAlias

# Initialize
app = FastAPI(title="Pathology Report Processing Engine", version="1.0.0")
pipeline = ProcessingPipeline()

# Schemas
class ProcessRequest(BaseModel):
    text: str = Field(..., description="Raw text from pathology/lab report")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Hemoglobin 13.5 g/dL 12-16\nWBC 7.2 x10^3/uL 4-11\nPlatelets 250 x10^3/uL 150-400",
                "metadata": {"source": "pdf", "patient_id": "12345"}
            }
        }

class TestResult(BaseModel):
    raw_text: str
    raw_test_name: str
    normalized_test_name: str
    canonical_name: Optional[str]
    loinc_code: Optional[str]
    value: Optional[float]
    unit: Optional[str]
    reference_range: Optional[str]
    status: str
    match_type: str
    similarity_score: float
    confidence_score: float

class ProcessResponse(BaseModel):
    request_id: str
    tests: List[TestResult]
    processing_time_ms: float
    summary: Dict[str, int]
    errors: List[str]

class CanonicalTestCreate(BaseModel):
    canonical_name: str
    loinc_code: Optional[str] = None
    category: Optional[str] = None
    default_unit: Optional[str] = None

class TestAliasCreate(BaseModel):
    canonical_test_name: str
    alias: str
    alias_type: str
    confidence_score: float = 1.0

# API Endpoints
@app.post("/v1/process", response_model=ProcessResponse)
async def process_report(request: ProcessRequest):
    """Process pathology/lab report text"""
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text too short or empty")
    
    result = pipeline.process(request.text)
    
    tests = [TestResult(**test) if isinstance(test, dict) else test for test in result.tests]
    
    return ProcessResponse(
        request_id=result.request_id,
        tests=tests,
        processing_time_ms=result.processing_time_ms,
        summary={
            "total_tests": len(tests),
            "regex_matches": result.regex_matches,
            "fallback_matches": result.fallback_matches,
            "canonicalized": result.canonicalized
        },
        errors=result.errors
    )

@app.get("/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/v1/canonical-tests")
async def add_canonical_test(test: CanonicalTestCreate):
    """Add a new canonical test"""
    with db_manager.get_session() as session:
        existing = session.query(CanonicalTest).filter(
            CanonicalTest.canonical_name == test.canonical_name
        ).first()
        
        if existing:
            raise HTTPException(status_code=409, detail="Test already exists")
        
        new_test = CanonicalTest(
            canonical_name=test.canonical_name,
            loinc_code=test.loinc_code,
            category=test.category,
            default_unit=test.default_unit
        )
        session.add(new_test)
        session.flush()
        
        return {"id": new_test.id, "message": "Canonical test added"}

@app.post("/v1/aliases")
async def add_alias(alias: TestAliasCreate):
    """Add an alias for a canonical test"""
    from services.text_normalizer import TextNormalizer
    
    with db_manager.get_session() as session:
        test = session.query(CanonicalTest).filter(
            CanonicalTest.canonical_name == alias.canonical_test_name
        ).first()
        
        if not test:
            raise HTTPException(status_code=404, detail="Canonical test not found")
        
        existing = session.query(TestAlias).filter(
            TestAlias.canonical_test_id == test.id,
            TestAlias.normalized_alias == TextNormalizer.normalize_for_matching(alias.alias)
        ).first()
        
        if existing:
            raise HTTPException(status_code=409, detail="Alias already exists")
        
        new_alias = TestAlias(
            canonical_test_id=test.id,
            alias=alias.alias,
            normalized_alias=TextNormalizer.normalize_for_matching(alias.alias),
            alias_type=alias.alias_type,
            confidence_score=alias.confidence_score
        )
        session.add(new_alias)
        
        return {"message": "Alias added"}

@app.get("/v1/canonical-tests/{test_name}")
async def lookup_test(test_name: str):
    """Look up canonical test by name"""
    from services.alias_resolver import AliasResolver
    from services.text_normalizer import TextNormalizer
    
    normalized = TextNormalizer.normalize_for_matching(test_name)
    
    with db_manager.get_session() as session:
        resolver = AliasResolver(session)
        result = resolver.resolve(test_name)
        
        if result:
            return {
                "found": True,
                "canonical_name": result.canonical_name,
                "canonical_id": result.canonical_id,
                "match_type": result.match_type,
                "confidence": result.confidence
            }
        else:
            return {"found": False, "message": "Test not found in alias database"}

@app.get("/v1/stats")
async def get_stats():
    """Get system statistics"""
    with db_manager.get_session() as session:
        test_count = session.query(CanonicalTest).count()
        alias_count = session.query(TestAlias).count()
        
        return {
            "canonical_tests": test_count,
            "aliases": alias_count,
            "alias_per_test": alias_count / test_count if test_count > 0 else 0
        }