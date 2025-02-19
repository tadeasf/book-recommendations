from typing import Optional, TYPE_CHECKING, Annotated
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from pydantic import Field as PydanticField
from pydantic.types import conint

if TYPE_CHECKING:
    from .User import User
    from .Book import Book

class UserBook(SQLModel, table=True):
    """
    SQLModel UserBook model for tracking user's book interactions.
    
    This model represents the many-to-many relationship between users and books,
    storing additional data like ratings and timestamps.
    
    Attributes:
        id: Unique identifier for the user-book relationship
        user_id: Foreign key to the user
        book_id: Foreign key to the book
        rating: Optional rating (1-5) given by the user
        created_at: Timestamp when the relationship was created
        updated_at: Timestamp when the relationship was last updated
        user: Relationship to the User model
        book: Relationship to the Book model
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", description="ID of the user")
    book_id: int = Field(foreign_key="book.id", description="ID of the book")
    rating: Optional[Annotated[int, conint(ge=1, le=5)]] = Field(
        default=None,
        description="User's rating of the book (1-5 stars)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the relationship was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the relationship was last updated"
    )
    
    user: "User" = Relationship(back_populates="user_books")
    book: "Book" = Relationship(back_populates="user_books") 