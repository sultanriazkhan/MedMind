# pathology_processor/config.py
import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    # Database - SQLite for development
    db_url: str
    db_pool_size: int = 5
    db_max_overflow: int = 10
    
    # Extraction thresholds
    min_confidence_score: float = 0.7
    fuzzy_match_threshold: int = 85
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
        
        # Get the First_Module folder path (parent of pathology_processor)
        base_dir = Path(__file__).parent.parent
        db_path = base_dir / "pathology.db"
        
        if env == "production":
            db_url = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")
        else:
            db_url = f"sqlite:///{db_path}"
        
        return cls(db_url=db_url)

# Create global config instance
config = Config.from_env()