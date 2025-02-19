from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from pydantic import EmailStr, Field as PydanticField

if TYPE_CHECKING:
    from .UserBook import UserBook

class UserBase(SQLModel):
    """
    Base User model with common attributes.
    
    Attributes:
        username: Unique username for the user
        email: Valid email address
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated
    """
    username: str = Field(
        description="Unique username for the user",
        min_length=3,
        max_length=50
    )
    email: EmailStr = Field(description="Valid email address")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the user was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the user was last updated"
    )

class User(UserBase, table=True):
    """
    SQLModel User model for database operations.
    
    Extends UserBase and adds:
        id: Unique identifier
        user_books: Relationship to UserBook model
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_books: List["UserBook"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    """
    Pydantic model for creating a new user.
    
    Inherits all fields from UserBase.
    Used for validating request data when creating a new user.
    """
    pass

class UserRead(UserBase):
    """
    Pydantic model for reading user data.
    
    Extends UserBase and adds:
        id: The user's unique identifier
        
    Used for serializing user data in responses.
    """
    id: int = Field(description="The user's unique identifier") 