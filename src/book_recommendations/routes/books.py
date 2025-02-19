from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Any
from ..models.Book import Book, BookCreate, BookRead, BookUpdate
from ..lib.dependencies import get_session
from ..lib.security import get_api_key

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

@router.post("/", response_model=BookRead)
async def create_book(
    *,
    session: Session = Depends(get_session),
    book: BookCreate,
    api_key: str = Depends(get_api_key)
) -> Any:
    """
    Create a new book.
    
    Args:
        session: Database session
        book: Book data to create
        api_key: API key for authentication
        
    Returns:
        BookRead: Created book data
        
    Raises:
        HTTPException: If book creation fails or authentication fails
    """
    db_book = Book.from_orm(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.get("/", response_model=List[BookRead])
async def read_books(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    api_key: str = Depends(get_api_key)
) -> Any:
    """
    Get a list of books with pagination.
    
    Args:
        session: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        api_key: API key for authentication
        
    Returns:
        List[BookRead]: List of books
        
    Raises:
        HTTPException: If authentication fails
    """
    books = session.exec(select(Book).offset(skip).limit(limit)).all()
    return books

@router.get("/{book_id}", response_model=BookRead)
async def read_book(
    *,
    session: Session = Depends(get_session),
    book_id: int,
    api_key: str = Depends(get_api_key)
) -> Any:
    """
    Get a specific book by ID.
    
    Args:
        session: Database session
        book_id: ID of the book to retrieve
        api_key: API key for authentication
        
    Returns:
        BookRead: Book data
        
    Raises:
        HTTPException: If book is not found or authentication fails
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.patch("/{book_id}", response_model=BookRead)
async def update_book(
    *,
    session: Session = Depends(get_session),
    book_id: int,
    book: BookUpdate,
    api_key: str = Depends(get_api_key)
) -> Any:
    """
    Update a specific book.
    
    Args:
        session: Database session
        book_id: ID of the book to update
        book: Updated book data
        api_key: API key for authentication
        
    Returns:
        BookRead: Updated book data
        
    Raises:
        HTTPException: If book is not found or authentication fails
    """
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_data = book.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
    
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.delete("/{book_id}", response_model=dict[str, bool])
async def delete_book(
    *,
    session: Session = Depends(get_session),
    book_id: int,
    api_key: str = Depends(get_api_key)
) -> Any:
    """
    Delete a specific book.
    
    Args:
        session: Database session
        book_id: ID of the book to delete
        api_key: API key for authentication
        
    Returns:
        dict[str, bool]: Success message
        
    Raises:
        HTTPException: If book is not found or authentication fails
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    session.delete(book)
    session.commit()
    return {"ok": True}
