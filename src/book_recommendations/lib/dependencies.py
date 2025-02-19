from sqlmodel import Session
from .database import engine

def get_session():
    """
    FastAPI dependency that provides a SQLModel database session.
    
    Yields:
        Session: Database session that will be automatically closed after use
    """
    with Session(engine) as session:
        yield session 