from typing import List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os
from ..models.Book import Book, BookRead
from sqlmodel import Session
from .config import OPENAI_API_KEY

class BookRecommender:
    """
    Book recommendation engine using both traditional and AI-enhanced methods.
    """
    
    def __init__(self, session: Session = None):
        """
        Initialize the recommender.
        
        Args:
            session: Optional database session
        """
        self.session = session
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
    def _update_tfidf(self, books: List[Book]) -> None:
        """Update TF-IDF matrix with current books."""
        descriptions = [f"{book.title} {book.description} {' '.join(book.genres)}" 
                       for book in books]
        self.tfidf_matrix = self.tfidf.fit_transform(descriptions)
        
    def get_traditional_recommendations(self, book: Book, limit: int = 5) -> List[BookRead]:
        """
        Get book recommendations using traditional similarity metrics.
        
        Args:
            book: Source book to get recommendations for
            limit: Maximum number of recommendations to return
            
        Returns:
            List[BookRead]: List of recommended books
        """
        # Implement traditional recommendation logic
        # For now, return a simple list of books
        if self.session:
            return self.session.query(Book).limit(limit).all()
        return []
        
    async def get_ai_recommendations(self, book: Book, limit: int = 5) -> List[str]:
        """
        Get book recommendations using AI models.
        
        Args:
            book: Source book to get recommendations for
            limit: Maximum number of recommendations to return
            
        Returns:
            List[str]: List of recommended book titles
        """
        # Implement AI-based recommendation logic
        # For now, return dummy recommendations
        return [
            f"AI Recommended Book {i} for {book.title}"
            for i in range(limit)
        ]
        
    async def cleanup(self):
        """
        Cleanup resources used by the recommender.
        
        This method is called during application shutdown to ensure
        proper cleanup of ML models and other resources.
        """
        # Cleanup any ML models or resources
        self.session = None
