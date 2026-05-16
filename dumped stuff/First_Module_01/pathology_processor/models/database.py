# models/database.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging
from typing import Generator

from .orm_models import Base
from config import config

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self._engine = None
        self._session_factory = None
        self._initialize()
    
    def _initialize(self):
        """Initialize database connection"""
        # SQLite specific configuration
        if "sqlite" in self.db_url:
            self._engine = create_engine(
                self.db_url,
                connect_args={"check_same_thread": False},
                poolclass=QueuePool,
                pool_size=config.db_pool_size,
                max_overflow=config.db_max_overflow,
                echo=False
            )
            
            # Enable foreign keys for SQLite
            @event.listens_for(self._engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        else:
            # PostgreSQL configuration
            self._engine = create_engine(
                self.db_url,
                poolclass=QueuePool,
                pool_size=config.db_pool_size,
                max_overflow=config.db_max_overflow,
                pool_pre_ping=True,
                echo=False
            )
        
        self._session_factory = sessionmaker(bind=self._engine)
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self._engine)
        logger.info("Database tables created")
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get database session context manager"""
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()
    
    @property
    def engine(self):
        return self._engine

# Global database manager instance
db_manager = DatabaseManager(config.db_url)