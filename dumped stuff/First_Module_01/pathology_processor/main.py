# main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import time
import uuid
import requests

from api.routes import app as api_app
from models.database import db_manager
from services.seed_data import seed_database
from services.pipeline import ProcessingPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============ PYDANTIC MODELS FOR DIRECT API ============

class ProcessTextRequest(BaseModel):
    """Request model for direct text processing"""
    text: str = Field(..., description="Raw text from pathology/lab report", min_length=10)
    include_ai: bool = Field(False, description="Whether to include AI explanations (requires AI service)")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class TestResult(BaseModel):
    """Single test result model"""
    raw_text: str = ""
    raw_test_name: str = ""
    normalized_test_name: str = ""
    canonical_name: Optional[str] = None
    loinc_code: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: str = "Unknown"
    match_type: str = "unknown"
    similarity_score: float = 0.0
    confidence_score: float = 0.0

class ProcessTextResponse(BaseModel):
    """Response model for direct text processing"""
    success: bool
    request_id: str
    processing_time_ms: float
    total_tests: int
    tests: List[TestResult]
    summary: Dict[str, int]
    errors: List[str] = []

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    timestamp: str
    database: str
    pipeline_ready: bool

# ============ INITIALIZE PIPELINE ============
# Create pipeline instance for direct processing
try:
    pipeline = ProcessingPipeline()
    logger.info("✅ Processing pipeline initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize pipeline: {e}")
    pipeline = None

# ============ LIFESPAN MANAGER ============
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("="*60)
    logger.info("Starting Pathology Report Processing Engine...")
    logger.info("="*60)
    
    # Initialize database
    try:
        db_manager.create_tables()
        logger.info("✅ Database tables created/verified")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    # Seed initial data if needed
    try:
        seed_database()
        logger.info("✅ Seed data loaded")
    except Exception as e:
        logger.warning(f"⚠️ Seed data warning: {e}")
    
    logger.info("="*60)
    logger.info("Application started successfully")
    logger.info(f"📡 API Documentation: http://localhost:8000/docs")
    logger.info(f"🔬 Health Check: http://localhost:8000/health")
    logger.info(f"⚡ Process Endpoint: POST /api/process")
    logger.info("="*60)
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")

# Apply lifespan to API app
api_app.router.lifespan_context = lifespan

# ============ ADD CORS MIDDLEWARE ============
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ NEW ENDPOINTS FOR INTEGRATION ============

@api_app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint for service discovery"""
    # Check database status
    db_status = "unknown"
    try:
        with db_manager.get_session() as session:
            from models.orm_models import CanonicalTest
            count = session.query(CanonicalTest).count()
            db_status = f"connected ({count} tests)"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy" if pipeline else "degraded",
        service="pathology-processor",
        version="1.0.0",
        timestamp=__import__('datetime').datetime.now().isoformat(),
        database=db_status,
        pipeline_ready=pipeline is not None
    )

@api_app.get("/ready", tags=["System"])
async def readiness_check():
    """Kubernetes-style readiness probe"""
    is_ready = pipeline is not None
    return {
        "ready": is_ready,
        "message": "Ready to process" if is_ready else "Pipeline not initialized"
    }

@api_app.get("/live", tags=["System"])
async def liveness_check():
    """Kubernetes-style liveness probe"""
    return {"alive": True, "timestamp": __import__('time').time()}

@api_app.post("/api/process", response_model=ProcessTextResponse, tags=["Processing"])
async def process_text_direct(request: ProcessTextRequest):
    """
    Direct text processing endpoint for orchestrator integration.
    This bypasses the AI explainer and returns structured test data.
    """
    if not pipeline:
        raise HTTPException(status_code=503, detail="Processing pipeline not initialized")
    
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    try:
        # Process the text
        result = pipeline.process(request.text)
        
        processing_time = (time.time() - start_time) * 1000
        
        # Convert to response model
        test_results = []
        for test in result.tests:
            test_results.append(TestResult(
                raw_text=test.get('raw_text', ''),
                raw_test_name=test.get('raw_test_name', ''),
                normalized_test_name=test.get('normalized_test_name', ''),
                canonical_name=test.get('canonical_name'),
                loinc_code=test.get('loinc_code'),
                value=test.get('value'),
                unit=test.get('unit'),
                reference_range=test.get('reference_range'),
                status=test.get('status', 'Unknown'),
                match_type=test.get('match_type', 'unknown'),
                similarity_score=test.get('similarity_score', 0.0),
                confidence_score=test.get('confidence_score', 0.0)
            ))
        
        return ProcessTextResponse(
            success=True,
            request_id=request_id,
            processing_time_ms=processing_time,
            total_tests=len(test_results),
            tests=test_results,
            summary={
                "regex_matches": result.regex_matches,
                "fallback_matches": result.fallback_matches,
                "canonicalized": result.canonicalized
            },
            errors=result.errors
        )
        
    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        processing_time = (time.time() - start_time) * 1000
        return ProcessTextResponse(
            success=False,
            request_id=request_id,
            processing_time_ms=processing_time,
            total_tests=0,
            tests=[],
            summary={},
            errors=[str(e)]
        )

@api_app.post("/api/process-batch", tags=["Processing"])
async def process_batch(texts: List[str]):
    """Process multiple texts in batch"""
    if not pipeline:
        raise HTTPException(status_code=503, detail="Processing pipeline not initialized")
    
    start_time = time.time()
    results = []
    
    for text in texts:
        result = pipeline.process(text)
        results.append({
            "tests": [
                {
                    "test_name": t.get('raw_test_name'),
                    "value": t.get('value'),
                    "status": t.get('status')
                }
                for t in result.tests
            ],
            "test_count": len(result.tests)
        })
    
    processing_time = (time.time() - start_time) * 1000
    
    return {
        "success": True,
        "total_texts": len(texts),
        "processing_time_ms": processing_time,
        "results": results
    }

@api_app.get("/api/stats", tags=["System"])
async def get_system_stats():
    """Get system statistics"""
    with db_manager.get_session() as session:
        from models.orm_models import CanonicalTest, TestAlias, ReferenceRange
        
        test_count = session.query(CanonicalTest).count()
        alias_count = session.query(TestAlias).count()
        range_count = session.query(ReferenceRange).count()
        
        return {
            "canonical_tests": test_count,
            "aliases": alias_count,
            "reference_ranges": range_count,
            "pipeline_ready": pipeline is not None,
            "alias_per_test": alias_count / test_count if test_count > 0 else 0
        }

@api_app.get("/api/test/{test_name}", tags=["Lookup"])
async def lookup_test(test_name: str):
    """Look up a test by name (for debugging)"""
    from services.alias_resolver import AliasResolver
    from services.text_normalizer import TextNormalizer
    
    with db_manager.get_session() as session:
        resolver = AliasResolver(session)
        result = resolver.resolve(test_name)
        
        if result:
            return {
                "found": True,
                "input": test_name,
                "canonical_name": result.canonical_name,
                "canonical_id": result.canonical_id,
                "match_type": result.match_type,
                "confidence": result.confidence,
                "similarity": result.similarity_score
            }
        else:
            return {
                "found": False,
                "input": test_name,
                "message": "Test not found in alias database"
            }
# ============ MAIN ENTRY POINT ============
def main():
    """Main entry point"""
    port = 8000
    host = "0.0.0.0"
    
    print("\n" + "="*60)
    print("🔬 Pathology Report Processing Engine")
    print("="*60)
    print(f"📍 Server: http://{host}:{port}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    print(f"🔍 Health: http://{host}:{port}/health")
    print(f"⚡ Process: POST http://{host}:{port}/api/process")
    print("="*60 + "\n")
    uvicorn.run(
        "main:api_app",
        host=host,
        port=port,
        reload=False,
        workers=1,
        log_level="info",
        access_log=True
    )
    
if __name__ == "__main__":
    main()