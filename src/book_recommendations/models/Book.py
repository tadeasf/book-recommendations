from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship, JSON
from datetime import datetime
from pydantic import Field as PydanticField

if TYPE_CHECKING:
    from .UserBook import UserBook

class BookBase(SQLModel):
    """
    Base Book model with common attributes.
    
    Attributes:
        title: The title of the book
        author: The author's name
        description: A brief description or summary of the book
        isbn: International Standard Book Number (optional)
        genres: List of genres the book belongs to
        created_at: Timestamp when the book was added
        updated_at: Timestamp when the book was last updated
    """
    title: str = Field(description="The title of the book")
    author: str = Field(description="The author's name")
    description: str = Field(description="A brief description or summary of the book")
    isbn: Optional[str] = Field(default=None, description="International Standard Book Number")
    genres: List[str] = Field(
        sa_type=JSON,
        description="List of genres the book belongs to",
        default=[]
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the book was added"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the book was last updated"
    )

class Book(BookBase, table=True):
    """
    SQLModel Book model for database operations.
    
    Extends BookBase and adds:
        id: Unique identifier
        user_books: Relationship to UserBook model
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_books: List["UserBook"] = Relationship(back_populates="book")

class BookCreate(BookBase):
    """
    Pydantic model for creating a new book.
    
    Inherits all fields from BookBase.
    Used for validating request data when creating a new book.
    """
    genres: List[str] = PydanticField(
        description="List of genres the book belongs to",
        example=["Fiction", "Science Fiction", "Fantasy"],
        default=[]
    )

class BookRead(BookBase):
    """
    Pydantic model for reading book data.
    
    Extends BookBase and adds:
        id: The book's unique identifier
        
    Used for serializing book data in responses.
    """
    id: int = Field(description="The book's unique identifier")

class BookUpdate(SQLModel):
    """
    Pydantic model for updating a book.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        title: New title for the book
        author: New author name
        description: New book description
        isbn: New ISBN
        genres: New list of genres
    """
    title: Optional[str] = Field(default=None, description="New title for the book")
    author: Optional[str] = Field(default=None, description="New author name")
    description: Optional[str] = Field(default=None, description="New book description")
    isbn: Optional[str] = Field(default=None, description="New ISBN")
    genres: Optional[List[str]] = PydanticField(
        default=None,
        description="New list of genres",
        example=["Fiction", "Science Fiction", "Fantasy"]
    )
