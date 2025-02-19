from .Book import Book, BookBase, BookCreate, BookRead, BookUpdate
from .User import User, UserBase, UserCreate, UserRead
from .UserBook import UserBook

# Export all models
__all__ = [
    # Book models
    "Book",
    "BookBase",
    "BookCreate",
    "BookRead",
    "BookUpdate",
    # User models
    "User",
    "UserBase",
    "UserCreate",
    "UserRead",
    # UserBook model
    "UserBook",
]

# For Alembic migrations
from sqlmodel import SQLModel
Base = SQLModel
