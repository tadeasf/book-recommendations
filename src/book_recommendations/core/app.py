from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from ..lib.database import engine, create_db_and_tables
from ..lib.book_recommender import BookRecommender

class BookRecommendationsApp(FastAPI):
    """
    Enhanced FastAPI application with proper lifespan management.
    
    This class extends FastAPI to provide:
    1. Database connection management
    2. ML model initialization
    3. Graceful shutdown
    """
    def __init__(self, *args, **kwargs):
        """Initialize the application with lifespan management."""
        
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Startup: Initialize resources
            await self._startup()
            yield
            # Shutdown: Cleanup resources
            await self._shutdown()
            
        super().__init__(*args, **kwargs, lifespan=lifespan)
        
    async def _startup(self):
        """Initialize application resources."""
        # Create database tables
        create_db_and_tables()
        
        # Initialize ML models and other resources
        self.state.recommender = BookRecommender()
        
        print("🚀 Application startup complete")
        
    async def _shutdown(self):
        """Cleanup application resources."""
        # Close database connections
        if engine is not None:
            engine.dispose()
            
        # Cleanup ML models
        if hasattr(self.state, "recommender"):
            await self.state.recommender.cleanup()
            
        print("👋 Application shutdown complete") 