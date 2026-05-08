# models/orm_models.py
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, 
    DateTime, Index, Text, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class CanonicalTest(Base):
    __tablename__ = "canonical_tests"
    
    id = Column(Integer, primary_key=True)
    canonical_name = Column(String(255), nullable=False, unique=True)
    loinc_code = Column(String(20), index=True)
    category = Column(String(100), index=True)
    default_unit = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    aliases = relationship("TestAlias", back_populates="canonical_test", cascade="all, delete-orphan")
    reference_ranges = relationship("ReferenceRange", back_populates="canonical_test", cascade="all, delete-orphan")
    critical_thresholds = relationship("CriticalThreshold", back_populates="canonical_test", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_canonical_name", "canonical_name"),
        Index("idx_loinc_code", "loinc_code"),
    )

class TestAlias(Base):
    __tablename__ = "test_aliases"
    
    id = Column(Integer, primary_key=True)
    canonical_test_id = Column(Integer, ForeignKey("canonical_tests.id", ondelete="CASCADE"), nullable=False)
    alias = Column(String(255), nullable=False)
    normalized_alias = Column(String(255), nullable=False, index=True)
    alias_type = Column(String(50))  # abbreviation, synonym, common_name, ocr_variant
    confidence_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    canonical_test = relationship("CanonicalTest", back_populates="aliases")
    
    __table_args__ = (
        Index("idx_normalized_alias", "normalized_alias"),
        UniqueConstraint("canonical_test_id", "normalized_alias", name="uq_canonical_alias"),
    )

class ReferenceRange(Base):
    __tablename__ = "reference_ranges"
    
    id = Column(Integer, primary_key=True)
    canonical_test_id = Column(Integer, ForeignKey("canonical_tests.id"), nullable=False)
    gender = Column(String(10), nullable=True)  # M, F, null for both
    min_age_days = Column(Integer, nullable=True)
    max_age_days = Column(Integer, nullable=True)
    lower_bound = Column(Float, nullable=True)
    upper_bound = Column(Float, nullable=True)
    unit = Column(String(50))
    source = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    canonical_test = relationship("CanonicalTest", back_populates="reference_ranges")
    
    __table_args__ = (
        Index("idx_range_lookup", "canonical_test_id", "gender", "min_age_days", "max_age_days"),
        CheckConstraint("lower_bound IS NULL OR upper_bound IS NULL OR lower_bound <= upper_bound", 
                       name="ck_range_bounds"),
    )

class CriticalThreshold(Base):
    __tablename__ = "critical_thresholds"
    
    id = Column(Integer, primary_key=True)
    canonical_test_id = Column(Integer, ForeignKey("canonical_tests.id"), nullable=False)
    critical_low = Column(Float, nullable=True)
    critical_high = Column(Float, nullable=True)
    unit = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    canonical_test = relationship("CanonicalTest", back_populates="critical_thresholds")

class LOINCMapping(Base):
    __tablename__ = "loinc_mappings"
    
    id = Column(Integer, primary_key=True)
    loinc_code = Column(String(20), nullable=False, index=True)
    loinc_name = Column(String(500))
    component = Column(String(500))
    property = Column(String(100))
    time_aspect = Column(String(50))
    system = Column(String(100))
    scale_type = Column(String(50))
    method_type = Column(String(255))
    canonical_test_id = Column(Integer, ForeignKey("canonical_tests.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index("idx_loinc_lookup", "loinc_code", "canonical_test_id"),
    )

class ProcessingLog(Base):
    __tablename__ = "processing_logs"
    
    id = Column(Integer, primary_key=True)
    request_id = Column(String(36), index=True)
    raw_text_hash = Column(String(64), index=True)
    extracted_tests_count = Column(Integer)
    processing_time_ms = Column(Float)
    success = Column(Integer, default=1)  # boolean as integer for SQLite compatibility
    error_message = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index("idx_request_id", "request_id"),
        Index("idx_created_at", "created_at"),
    )