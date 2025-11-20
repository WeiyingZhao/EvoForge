"""
Database configuration and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from .config import settings

# Create engine with pgvector support
engine = create_engine(
    str(settings.DATABASE_URL),
    poolclass=NullPool,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for getting database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database with pgvector extension."""
    from sqlalchemy import text

    with engine.connect() as conn:
        # Enable pgvector extension
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    # Create all tables
    Base.metadata.create_all(bind=engine)
