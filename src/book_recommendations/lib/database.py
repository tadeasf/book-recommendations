from sqlmodel import SQLModel, create_engine
from .config import DB_URL

# Database configuration
engine = create_engine(DB_URL)

def create_db_and_tables():
    """
    Create all database tables defined by SQLModel models.
    
    This function should be called when the application starts up to ensure
    all necessary database tables exist.
    """
    SQLModel.metadata.create_all(engine) 