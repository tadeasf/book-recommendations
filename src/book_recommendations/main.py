from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, SQLModel, create_engine, select
from typing import List
import os
from .models.Book import Book, BookCreate, BookRead, BookUpdate
from .lib.book_recommender import BookRecommender

# Database setup
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/bookdb")
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI(title="Book Recommendations API")
recommender = BookRecommender()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Book endpoints
@app.post("/books/", response_model=BookRead)
def create_book(*, session: Session = Depends(get_session), book: BookCreate):
    db_book = Book.from_orm(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[BookRead])
def read_books(*, session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    books = session.exec(select(Book).offset(skip).limit(limit)).all()
    return books

@app.get("/books/{book_id}", response_model=BookRead)
def read_book(*, session: Session = Depends(get_session), book_id: int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.patch("/books/{book_id}", response_model=BookRead)
def update_book(*, session: Session = Depends(get_session), book_id: int, book: BookUpdate):
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

@app.delete("/books/{book_id}")
def delete_book(*, session: Session = Depends(get_session), book_id: int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    session.delete(book)
    session.commit()
    return {"ok": True}

# Recommendation endpoints
@app.get("/recommendations/traditional/{book_id}", response_model=List[BookRead])
def get_traditional_recommendations(
    *, 
    session: Session = Depends(get_session), 
    book_id: int, 
    n: int = 5
):
    books = session.exec(select(Book)).all()
    book_index = next((i for i, b in enumerate(books) if b.id == book_id), None)
    if book_index is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return recommender.get_traditional_recommendations(books, book_index, n)

@app.get("/recommendations/ai/{book_id}", response_model=List[str])
async def get_ai_recommendations(
    *, 
    session: Session = Depends(get_session), 
    book_id: int, 
    n: int = 5
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return await recommender.get_ai_enhanced_recommendations(book, n)