from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Any
from ..models.Book import Book, BookRead
from ..lib.dependencies import get_session
from ..lib.book_recommender import BookRecommender
from ..lib.security import get_api_key

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)

@router.get("/traditional/{book_id}", response_model=List[BookRead])
async def get_traditional_recommendations(
    *,
    session: Session = Depends(get_session),
    book_id: int,
    limit: int = 5,
    api_key: str = Depends(get_api_key)
) -> Any:
    """
    Get book recommendations based on traditional similarity metrics.
    
    Args:
        session: Database session
        book_id: ID of the book to get recommendations for
        limit: Maximum number of recommendations to return
        api_key: API key for authentication
        
    Returns:
        List[BookRead]: List of recommended books
        
    Raises:
        HTTPException: If book is not found or authentication fails
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    recommender = BookRecommender(session)
    recommendations = recommender.get_traditional_recommendations(book, limit)
    return recommendations

@router.get("/ai/{book_id}", response_model=List[str])
async def get_ai_recommendations(
    *,
    session: Session = Depends(get_session),
    book_id: int,
    limit: int = 5,
    api_key: str = Depends(get_api_key)
) -> Any:
    """
    Get AI-enhanced book recommendations.
    
    Args:
        session: Database session
        book_id: ID of the book to get recommendations for
        limit: Maximum number of recommendations to return
        api_key: API key for authentication
        
    Returns:
        List[str]: List of recommended book titles
        
    Raises:
        HTTPException: If book is not found or authentication fails
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    recommender = BookRecommender(session)
    recommendations = await recommender.get_ai_recommendations(book, limit)
    return recommendations
