# main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from api.routes import app as api_app
from models.database import db_manager
from services.seed_data import seed_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Pathology Report Processing Engine...")
    
    # Initialize database
    db_manager.create_tables()
    
    # Seed initial data if needed
    seed_database()
    
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")

# Apply lifespan to API app
api_app.router.lifespan_context = lifespan

def main():
    """Main entry point"""
    uvicorn.run(
        "main:api_app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=4,
        log_level="info"
    )

if __name__ == "__main__":
    main()