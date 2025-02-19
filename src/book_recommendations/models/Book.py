from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship, JSON
from datetime import datetime

if TYPE_CHECKING:
    from .UserBook import UserBook

class BookBase(SQLModel):
    title: str
    author: str
    description: str
    isbn: Optional[str] = None
    genres: List[str] = Field(sa_type=JSON)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_books: List["UserBook"] = Relationship(back_populates="book")

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int

class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None
    genres: Optional[List[str]] = Field(default=None, sa_type=JSON)
