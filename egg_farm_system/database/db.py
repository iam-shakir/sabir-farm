"""
Database initialization and session management
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
import logging

from config import DATABASE_URL

logger = logging.getLogger(__name__)

Base = declarative_base()

class DatabaseManager:
    """Manages database connection and sessions"""
    
    _engine = None
    _SessionLocal = None
    
    @classmethod
    def initialize(cls):
        """Initialize database connection and create tables"""
        try:
            cls._engine = create_engine(
                DATABASE_URL,
                echo=False,
                connect_args={"check_same_thread": False}
            )
            
            # Enable foreign keys for SQLite
            @event.listens_for(cls._engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
            
            # Create all tables
            Base.metadata.create_all(bind=cls._engine)
            cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    @classmethod
    def get_session(cls):
        """Get a new database session"""
        if cls._SessionLocal is None:
            cls.initialize()
        return cls._SessionLocal()
    
    @classmethod
    def close(cls):
        """Close database connection"""
        if cls._engine:
            cls._engine.dispose()
            logger.info("Database connection closed")

# Export Base for use in models
__all__ = ['Base', 'DatabaseManager']
