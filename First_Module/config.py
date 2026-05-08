# config.py
import os
from enum import Enum
from dataclasses import dataclass
from pathlib import Path

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class Config:
    # Database
    db_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 20
    
    # Extraction thresholds
    min_confidence_score: float = 0.7
    fuzzy_match_threshold: int = 85  # rapidfuzz score
    max_fuzzy_matches: int = 3
    
    # scispaCy
    scispacy_model: str = "en_core_sci_sm"
    
    # Cache
    cache_ttl_seconds: int = 3600
    cache_max_size: int = 10000
    
    # Performance
    batch_size: int = 100
    worker_threads: int = 4
    
    @classmethod
    def from_env(cls) -> "Config":
        env = os.getenv("ENVIRONMENT", "development")
        
        if env == "production":
            db_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/pathology")
        else:
            db_url = os.getenv("DATABASE_URL", "sqlite:///./pathology.db")
        
        return cls(db_url=db_url)

config = Config.from_env()